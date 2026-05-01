"""Verify text_span correctness in evaluation outputs.

Checks:
  1. Span existence: text_span is an exact substring of the model annotation
  2. Span consistency: annotatable errors have text_span, missing-info errors have null
  3. Category/sub_type validation: values are from the valid set
  4. Score recomputation: MQM score matches stored value

Usage:
    python3 scripts/evaluation/verify_spans.py <eval_dir> [--model MODEL] [--verbose]

Examples:
    python3 scripts/evaluation/verify_spans.py output/evaluation/reference_free/gpt-4o-mini
    python3 scripts/evaluation/verify_spans.py output/evaluation/reference_free/gpt-4o-mini --model gpt-5.2
    python3 scripts/evaluation/verify_spans.py output/evaluation/reference_only/gpt-4o-mini --verbose
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from evaluation.mqm_evaluator import (
    VALID_CATEGORIES, VALID_SEVERITIES, VALID_SUB_TYPES,
    NON_ANNOTATABLE_SUB_TYPES, MQM_WEIGHTS, compute_mqm_score,
)

GENERATION_DIR = ROOT / "output" / "generation"

# All annotatable sub_types (everything except missing-info ones)
ANNOTATABLE_SUB_TYPES = set()
for subs in VALID_SUB_TYPES.values():
    ANNOTATABLE_SUB_TYPES |= subs
ANNOTATABLE_SUB_TYPES -= NON_ANNOTATABLE_SUB_TYPES


def _load_annotation(model_name, subfolder, fig_key, lang=None):
    """Load the model annotation text from the generation output."""
    gen_path = GENERATION_DIR / model_name / subfolder / f"{fig_key}.json"
    if not gen_path.exists():
        return None
    with open(gen_path) as f:
        gen = json.load(f)
    if lang and "model_annotations" in gen:
        return gen["model_annotations"].get(lang, "")
    return gen.get("model_annotation", "")


def verify_file(eval_path, model_name, verbose=False):
    """Verify a single evaluation JSON file. Returns dict of issues."""
    with open(eval_path) as f:
        data = json.load(f)

    fig_key = data.get("figure_key", eval_path.stem)
    subfolder = eval_path.parent.name
    issues = []

    # Determine if multi-language or single
    if "mqm_by_language" in data:
        # Multi-language: check each language
        for lang, lang_result in data["mqm_by_language"].items():
            annotation = _load_annotation(model_name, subfolder, fig_key, lang)
            lang_issues = _verify_errors(
                lang_result.get("errors", []), annotation, fig_key, lang, verbose
            )
            # Verify score
            score_issue = _verify_score(lang_result, fig_key, lang)
            if score_issue:
                lang_issues.append(score_issue)
            issues.extend(lang_issues)
    else:
        annotation = _load_annotation(model_name, subfolder, fig_key)
        issues = _verify_errors(
            data.get("errors", []), annotation, fig_key, None, verbose
        )
        score_issue = _verify_score(data, fig_key, None)
        if score_issue:
            issues.append(score_issue)

    return issues


def _verify_errors(errors, annotation, fig_key, lang=None, verbose=False):
    """Verify error entries against the annotation text."""
    issues = []
    prefix = f"{fig_key}" + (f" ({lang})" if lang else "")

    for i, err in enumerate(errors):
        cat = err.get("category", "")
        sub = err.get("sub_type", "")
        sev = err.get("severity", "")
        text_span = err.get("text_span")

        # Check 3: Category validation
        if cat not in VALID_CATEGORIES:
            issues.append({
                "figure": prefix, "error_idx": i, "type": "invalid_category",
                "detail": f"Unknown category: {cat!r}",
            })

        # Check 3: Sub-type validation
        valid_subs = VALID_SUB_TYPES.get(cat, set())
        if sub and sub not in valid_subs:
            issues.append({
                "figure": prefix, "error_idx": i, "type": "invalid_sub_type",
                "detail": f"Unknown sub_type {sub!r} for category {cat!r}",
            })

        # Check 3: Severity validation
        if sev not in VALID_SEVERITIES:
            issues.append({
                "figure": prefix, "error_idx": i, "type": "invalid_severity",
                "detail": f"Unknown severity: {sev!r}",
            })

        # Check 2: Span consistency
        if sub in NON_ANNOTATABLE_SUB_TYPES:
            if text_span is not None:
                issues.append({
                    "figure": prefix, "error_idx": i, "type": "unexpected_span",
                    "detail": f"Non-annotatable sub_type {sub!r} should have text_span=null, got: {text_span!r:.80}",
                })
        elif sub in ANNOTATABLE_SUB_TYPES:
            if text_span is None:
                issues.append({
                    "figure": prefix, "error_idx": i, "type": "missing_span",
                    "detail": f"Annotatable sub_type {sub!r} should have a text_span, got null",
                })

        # Check 1: Span existence in annotation
        if text_span is not None and annotation is not None:
            if text_span not in annotation:
                # Try case-insensitive and whitespace-normalized match
                norm_span = " ".join(text_span.split()).lower()
                norm_annotation = " ".join(annotation.split()).lower()
                if norm_span in norm_annotation:
                    if verbose:
                        issues.append({
                            "figure": prefix, "error_idx": i, "type": "span_fuzzy_match",
                            "detail": f"text_span matches after normalization: {text_span!r:.80}",
                        })
                else:
                    issues.append({
                        "figure": prefix, "error_idx": i, "type": "span_not_found",
                        "detail": f"text_span not found in annotation: {text_span!r:.80}",
                    })

    return issues


def _verify_score(result, fig_key, lang=None):
    """Verify that stored MQM score matches recomputed score."""
    prefix = f"{fig_key}" + (f" ({lang})" if lang else "")
    errors = result.get("errors", [])
    stored_score = result.get("mqm_score")
    if stored_score is None:
        return None

    recomputed, _ = compute_mqm_score(errors)
    recomputed = round(recomputed, 2)
    if abs(stored_score - recomputed) > 0.01:
        return {
            "figure": prefix, "error_idx": -1, "type": "score_mismatch",
            "detail": f"Stored MQM={stored_score}, recomputed={recomputed}",
        }
    return None


def run(eval_dir, model_filter=None, verbose=False):
    eval_path = Path(eval_dir)
    if not eval_path.exists():
        print(f"ERROR: {eval_path} does not exist")
        sys.exit(1)

    # Discover all evaluation JSONs
    models = [model_filter] if model_filter else sorted(
        d.name for d in eval_path.iterdir() if d.is_dir()
    )

    total_files = 0
    total_errors_checked = 0
    all_issues = []
    issue_counts = {}

    for model_name in models:
        model_dir = eval_path / model_name
        if not model_dir.exists():
            print(f"WARNING: {model_dir} does not exist, skipping")
            continue

        for subfolder_dir in sorted(model_dir.iterdir()):
            if not subfolder_dir.is_dir():
                continue
            for eval_file in sorted(subfolder_dir.glob("*.json")):
                total_files += 1
                try:
                    file_issues = verify_file(eval_file, model_name, verbose)
                    # Count errors checked
                    with open(eval_file) as f:
                        data = json.load(f)
                    if "mqm_by_language" in data:
                        for lr in data["mqm_by_language"].values():
                            total_errors_checked += len(lr.get("errors", []))
                    else:
                        total_errors_checked += len(data.get("errors", []))

                    all_issues.extend(file_issues)
                    for issue in file_issues:
                        t = issue["type"]
                        issue_counts[t] = issue_counts.get(t, 0) + 1

                except Exception as e:
                    all_issues.append({
                        "figure": eval_file.stem, "error_idx": -1,
                        "type": "parse_error", "detail": str(e),
                    })
                    issue_counts["parse_error"] = issue_counts.get("parse_error", 0) + 1

    # Report
    print(f"\n{'='*60}")
    print(f"Span Verification Report")
    print(f"{'='*60}")
    print(f"Directory:        {eval_path}")
    print(f"Models checked:   {len(models)}")
    print(f"Files checked:    {total_files}")
    print(f"Errors checked:   {total_errors_checked}")
    print(f"Issues found:     {len(all_issues)}")
    print()

    if issue_counts:
        print("Issue breakdown:")
        for itype, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            pct = count / total_errors_checked * 100 if total_errors_checked else 0
            label = {
                "span_not_found": "Span NOT found in annotation (exact or normalized)",
                "span_fuzzy_match": "Span found only after normalization (whitespace/case)",
                "missing_span": "Annotatable error missing text_span",
                "unexpected_span": "Non-annotatable error has text_span (should be null)",
                "invalid_category": "Invalid category value",
                "invalid_sub_type": "Invalid sub_type value",
                "invalid_severity": "Invalid severity value",
                "score_mismatch": "MQM score doesn't match recomputed value",
                "parse_error": "Could not parse evaluation file",
            }.get(itype, itype)
            print(f"  {count:4d} ({pct:5.1f}%)  {label}")
        print()

    # Show sample issues
    if all_issues and verbose:
        print("Sample issues (first 20):")
        print("-" * 60)
        for issue in all_issues[:20]:
            print(f"  [{issue['type']}] {issue['figure']} error#{issue['error_idx']}")
            print(f"    {issue['detail']}")
        print()

    # Summary
    span_errors = issue_counts.get("span_not_found", 0)
    missing_spans = issue_counts.get("missing_span", 0)
    if total_errors_checked > 0:
        span_match_rate = (total_errors_checked - span_errors) / total_errors_checked * 100
        print(f"Span match rate:  {span_match_rate:.1f}% ({total_errors_checked - span_errors}/{total_errors_checked})")
    else:
        print("No errors to verify.")

    clean = len(all_issues) == 0
    print(f"\nResult: {'PASS' if clean else 'ISSUES FOUND'}")
    return clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify text_span correctness in evaluation outputs")
    parser.add_argument("eval_dir", help="Path to evaluation output directory")
    parser.add_argument("--model", default=None, help="Check only this model")
    parser.add_argument("--verbose", action="store_true", help="Show detailed issue list")
    args = parser.parse_args()
    ok = run(args.eval_dir, args.model, args.verbose)
    sys.exit(0 if ok else 1)
