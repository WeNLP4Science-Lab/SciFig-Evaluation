"""Evaluate structured LLM annotations using MQM + breakdown verification.

Option C approach:
  - Paragraph MQM score (identical method to unstructured — fair comparison)
  - Breakdown accuracy as a supplementary metric

Reads generated outputs from output/generation_structured/ and writes
evaluation results to output/evaluation_structured/.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/evaluation/evaluate_structured.py
"""

import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from evaluation.mqm_evaluator import evaluate_annotation

GENERATION_DIR = ROOT / "output" / "generation_structured"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "evaluation_structured"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SUBFOLDERS = [
    "bulgarian_only",
    "chinese_only",
    "english_only",
    "german_only",
    "multi_language",
]

SAMPLE_PREFIXES = {
    "bulgarian_only": [f"bulgarian_fig_{i:03d}" for i in range(1, 11)],
    "chinese_only": [f"chinese_fig_{i:03d}" for i in range(1, 11)],
    "english_only": [f"english_fig_{i:03d}" for i in range(1, 11)],
    "german_only": [f"german_fig_{i:03d}" for i in range(1, 11)],
    "multi_language": [f"multi_fig_{i:03d}" for i in range(1, 11)],
}

# Expected breakdown fields per figure type
EXPECTED_FIELDS = {
    "Line Plot": {
        "required": ["figure_type_detected", "x_axis", "y_axis", "num_lines", "lines", "has_legend"],
        "array_field": "lines",
        "count_field": "num_lines",
    },
    "Bar Chart": {
        "required": ["figure_type_detected", "category_axis", "value_axis", "num_bars", "bars",
                      "is_grouped", "is_stacked", "has_legend"],
        "array_field": "bars",
        "count_field": "num_bars",
    },
    "Pie Chart": {
        "required": ["figure_type_detected", "num_slices", "slices", "has_legend", "labels_on_slices"],
        "array_field": "slices",
        "count_field": "num_slices",
    },
}

DEFAULT_EXPECTED = {
    "required": ["figure_type_detected", "num_visual_elements", "has_legend"],
    "array_field": None,
    "count_field": None,
}


def verify_breakdown_programmatic(breakdown: dict, figure_type: str) -> dict:
    """Run programmatic checks on breakdown fields. No LLM needed.

    Returns dict with check results and issues found.
    """
    spec = EXPECTED_FIELDS.get(figure_type, DEFAULT_EXPECTED)
    issues = []

    # Check field presence
    required = spec["required"]
    present = [f for f in required if f in breakdown]
    missing = [f for f in required if f not in breakdown]
    field_completeness = len(present) / len(required) if required else 1.0

    if missing:
        issues.append(f"Missing required fields: {missing}")

    # Check count consistency (e.g., num_lines matches len(lines))
    count_consistent = None
    array_field = spec.get("array_field")
    count_field = spec.get("count_field")

    if array_field and count_field:
        array_val = breakdown.get(array_field, [])
        count_val = breakdown.get(count_field)
        if isinstance(array_val, list) and isinstance(count_val, (int, float)):
            count_consistent = len(array_val) == int(count_val)
            if not count_consistent:
                issues.append(
                    f"Count mismatch: {count_field}={count_val} but "
                    f"{array_field} has {len(array_val)} items"
                )

    # Check for empty/null values in array items
    empty_fields_in_items = 0
    total_fields_in_items = 0
    if array_field and isinstance(breakdown.get(array_field), list):
        for item in breakdown[array_field]:
            if isinstance(item, dict):
                for k, v in item.items():
                    total_fields_in_items += 1
                    if v is None or v == "" or v == "null" or v == "N/A":
                        empty_fields_in_items += 1

    item_completeness = (
        (total_fields_in_items - empty_fields_in_items) / total_fields_in_items
        if total_fields_in_items > 0 else 1.0
    )

    # Check has_legend is boolean
    has_legend = breakdown.get("has_legend")
    if has_legend is not None and not isinstance(has_legend, bool):
        issues.append(f"has_legend should be boolean, got: {type(has_legend).__name__}")

    return {
        "field_completeness": round(field_completeness, 3),
        "count_consistent": count_consistent,
        "item_completeness": round(item_completeness, 3),
        "fields_present": present,
        "fields_missing": missing,
        "issues": issues,
        "total_checks": len(required) + (1 if count_field else 0),
        "checks_passed": len(present) + (1 if count_consistent else 0),
    }


def evaluate_single(
    fig_key: str,
    gen: dict,
    fig_path: Path,
    judge_model: str,
    model_name: str,
) -> dict | None:
    """Evaluate a single-language structured output. Returns eval dict or None on failure."""
    annotation = gen.get("model_annotation", "")
    breakdown = gen.get("breakdown", {})
    figure_type = gen.get("figure_type", "")

    # Tier 1: Paragraph MQM (same as unstructured)
    try:
        mqm_result = evaluate_annotation(
            image_path=fig_path,
            annotation=annotation,
            caption=gen.get("caption", ""),
            paper_title=gen.get("paper_title", ""),
            figure_type=figure_type,
            judge_model=judge_model,
        )
    except Exception as e:
        logger.error(f"  FAIL {fig_key} (MQM): {e}")
        return None

    # Tier 2: Breakdown verification (programmatic)
    breakdown_result = verify_breakdown_programmatic(breakdown, figure_type)

    return {
        "figure_key": fig_key,
        "model_name": model_name,
        "figure_type": figure_type,
        "evaluation_type": "structured",
        **mqm_result,
        "breakdown_verification": breakdown_result,
    }


def run(model_name: str = "gpt-4o-mini", judge_model: str = "openai/gpt-4o-mini"):
    gen_model_dir = GENERATION_DIR / model_name
    eval_output_dir = OUTPUT_DIR / model_name

    logger.info(f"Evaluating model: {model_name} (structured)")
    logger.info(f"Judge model: {judge_model}")
    logger.info(f"Source: {gen_model_dir}")
    logger.info(f"Output: {eval_output_dir}")
    print()

    total = 0
    success = 0
    error_count = 0

    for subfolder in SUBFOLDERS:
        fig_folder = FIGURES_DIR / subfolder
        gen_folder = gen_model_dir / subfolder
        out_folder = eval_output_dir / subfolder
        out_folder.mkdir(parents=True, exist_ok=True)

        for fig_key in SAMPLE_PREFIXES[subfolder]:
            total += 1
            gen_path = gen_folder / f"{fig_key}.json"
            fig_path = fig_folder / f"{fig_key}.png"
            out_path = out_folder / f"{fig_key}.json"

            if not gen_path.exists():
                logger.warning(f"  SKIP {fig_key} — generation output not found")
                continue
            if not fig_path.exists():
                logger.warning(f"  SKIP {fig_key} — figure image not found")
                continue
            if out_path.exists():
                logger.info(f"  SKIP {fig_key} — already evaluated")
                success += 1
                continue

            with open(gen_path) as f:
                gen = json.load(f)

            if "model_annotations" in gen:
                # Multi-language: evaluate each language
                logger.info(f"  [{subfolder}] {fig_key} — multi-language evaluation")
                mqm_by_lang = {}
                breakdown_by_lang = {}
                failed = False

                annotations = gen["model_annotations"]
                breakdowns = gen.get("breakdowns", {})

                for lang in sorted(annotations.keys()):
                    annotation = annotations[lang]
                    breakdown = breakdowns.get(lang, {})
                    figure_type = gen.get("figure_type", "")

                    logger.info(f"         evaluating {lang}...")
                    try:
                        mqm_result = evaluate_annotation(
                            image_path=fig_path,
                            annotation=annotation,
                            caption=gen.get("caption", ""),
                            paper_title=gen.get("paper_title", ""),
                            figure_type=figure_type,
                            judge_model=judge_model,
                        )
                        mqm_by_lang[lang] = mqm_result
                        breakdown_by_lang[lang] = verify_breakdown_programmatic(
                            breakdown, figure_type
                        )
                        logger.info(
                            f"         {lang}: MQM={mqm_result['mqm_score']}, "
                            f"{mqm_result['error_count']} errors, "
                            f"breakdown completeness={breakdown_by_lang[lang]['field_completeness']}"
                        )
                    except Exception as e:
                        logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                        failed = True
                        break

                if failed:
                    error_count += 1
                    continue

                avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)

                eval_result = {
                    "figure_key": fig_key,
                    "model_name": model_name,
                    "figure_type": gen.get("figure_type", ""),
                    "evaluation_type": "structured",
                    "mqm_by_language": mqm_by_lang,
                    "mqm_score_avg": round(avg_mqm, 2),
                    "breakdown_verification_by_language": breakdown_by_lang,
                }

            else:
                # Single language
                logger.info(f"  [{subfolder}] {fig_key} ({gen.get('figure_type', '')})...")
                eval_result = evaluate_single(fig_key, gen, fig_path, judge_model, model_name)

                if eval_result is None:
                    error_count += 1
                    continue

                logger.info(
                    f"  OK   {fig_key}: MQM={eval_result['mqm_score']}, "
                    f"{eval_result['error_count']} errors, "
                    f"breakdown completeness={eval_result['breakdown_verification']['field_completeness']}"
                )

            with open(out_path, "w") as f:
                json.dump(eval_result, f, indent=2, ensure_ascii=False)
            success += 1

    print()
    logger.info(f"Done. {success}/{total} evaluated, {error_count} failures.")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")
