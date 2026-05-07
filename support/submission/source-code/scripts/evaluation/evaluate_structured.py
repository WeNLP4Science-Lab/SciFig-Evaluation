"""Evaluate structured LLM annotations using MQM + breakdown verification.

Option C approach:
  - Paragraph MQM score (identical method to unstructured — fair comparison)
  - Breakdown accuracy as a supplementary metric

Reads generated outputs from output/generation_structured/ and writes
evaluation results to output/evaluation_structured/.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/evaluation/evaluate_structured.py <model_name> [--workers N] [--subfolder X] [--judge MODEL]
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
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

ALL_SUBFOLDERS = [
    "bulgarian_only",
    "chinese_only",
    "english_only",
    "german_only",
    "multi_language",
]

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
    """Run programmatic checks on breakdown fields. No LLM needed."""
    spec = EXPECTED_FIELDS.get(figure_type, DEFAULT_EXPECTED)
    issues = []

    required = spec["required"]
    present = [f for f in required if f in breakdown]
    missing = [f for f in required if f not in breakdown]
    field_completeness = len(present) / len(required) if required else 1.0

    if missing:
        issues.append(f"Missing required fields: {missing}")

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


def _discover_figures(subfolder: str, model_name: str) -> list[str]:
    """Discover all figure keys that have generation output."""
    gen_folder = GENERATION_DIR / model_name / subfolder
    if not gen_folder.exists():
        return []
    return sorted(p.stem for p in gen_folder.glob("*.json"))


def _process_figure(fig_key, subfolder, gen_folder, fig_folder, out_folder, judge_model):
    """Evaluate a single figure. Returns (ok, fig_key, status)."""
    gen_path = gen_folder / f"{fig_key}.json"
    fig_path = fig_folder / f"{fig_key}.png"
    out_path = out_folder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not gen_path.exists() or not fig_path.exists():
        return True, fig_key, "skip"

    with open(gen_path) as f:
        gen = json.load(f)

    model_name = gen.get("model_name", "")
    figure_type = gen.get("figure_type", "")

    if "model_annotations" in gen:
        # Multi-language
        mqm_by_lang = {}
        breakdown_by_lang = {}
        annotations = gen["model_annotations"]
        breakdowns = gen.get("breakdowns", {})

        for lang in sorted(annotations.keys()):
            annotation = annotations[lang]
            breakdown = breakdowns.get(lang, {})

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
                breakdown_by_lang[lang] = verify_breakdown_programmatic(breakdown, figure_type)
            except Exception as e:
                logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                return False, fig_key, str(e)

        avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)
        eval_result = {
            "figure_key": fig_key,
            "model_name": model_name,
            "figure_type": figure_type,
            "evaluation_type": "structured",
            "mqm_by_language": mqm_by_lang,
            "mqm_score_avg": round(avg_mqm, 2),
            "breakdown_verification_by_language": breakdown_by_lang,
        }
        logger.info(f"  OK   {fig_key}: avg MQM={avg_mqm:.1f} ({len(mqm_by_lang)} langs)")

    else:
        # Single language
        annotation = gen.get("model_annotation", "")
        breakdown = gen.get("breakdown", {})

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
            return False, fig_key, str(e)

        breakdown_result = verify_breakdown_programmatic(breakdown, figure_type)

        eval_result = {
            "figure_key": fig_key,
            "model_name": model_name,
            "figure_type": figure_type,
            "evaluation_type": "structured",
            **mqm_result,
            "breakdown_verification": breakdown_result,
        }
        logger.info(
            f"  OK   {fig_key}: MQM={mqm_result['mqm_score']}, "
            f"{mqm_result['error_count']} errors"
        )

    with open(out_path, "w") as f:
        json.dump(eval_result, f, indent=2, ensure_ascii=False)
    return True, fig_key, "done"


def run(model_name: str, judge_model: str = "openai/gpt-4o-mini",
        workers: int = 1, subfolder_filter: str | None = None):
    subfolders = [subfolder_filter] if subfolder_filter else ALL_SUBFOLDERS
    eval_output_dir = OUTPUT_DIR / model_name

    logger.info(f"Evaluating model: {model_name} (structured)")
    logger.info(f"Judge model: {judge_model}")
    logger.info(f"Workers: {workers}")
    logger.info(f"Subfolders: {subfolders}")
    logger.info(f"Output: {eval_output_dir}")
    print()

    work_items = []
    skipped = 0
    for subfolder in subfolders:
        fig_folder = FIGURES_DIR / subfolder
        gen_folder = GENERATION_DIR / model_name / subfolder
        out_folder = eval_output_dir / subfolder
        out_folder.mkdir(parents=True, exist_ok=True)

        for fig_key in _discover_figures(subfolder, model_name):
            fig_path = fig_folder / f"{fig_key}.png"
            out_path = out_folder / f"{fig_key}.json"

            if not fig_path.exists():
                continue
            if out_path.exists():
                skipped += 1
                continue

            work_items.append((fig_key, subfolder, gen_folder, fig_folder, out_folder))

    total = len(work_items) + skipped
    logger.info(f"Total: {total} ({skipped} already done, {len(work_items)} to evaluate)")
    print()

    if not work_items:
        logger.info("Nothing to do — all figures already evaluated.")
        return

    success = skipped
    errors = 0
    lock = threading.Lock()

    def _on_complete(ok, fig_key, status):
        nonlocal success, errors
        with lock:
            if ok:
                success += 1
            else:
                errors += 1
            done = success + errors - skipped
            if done % 10 == 0 or not ok:
                logger.info(f"  Progress: {done}/{len(work_items)} "
                            f"(success={success - skipped}, errors={errors})")

    if workers == 1:
        for fig_key, subfolder, gen_folder, fig_folder, out_folder in work_items:
            ok, key, status = _process_figure(
                fig_key, subfolder, gen_folder, fig_folder, out_folder, judge_model
            )
            _on_complete(ok, key, status)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _process_figure, fig_key, subfolder, gen_folder, fig_folder, out_folder, judge_model
                ): fig_key
                for fig_key, subfolder, gen_folder, fig_folder, out_folder in work_items
            }
            for future in as_completed(futures):
                try:
                    ok, key, status = future.result()
                    _on_complete(ok, key, status)
                except Exception as e:
                    fig_key = futures[future]
                    logger.error(f"  UNEXPECTED {fig_key}: {e}")
                    with lock:
                        errors += 1

    print()
    logger.info(f"Done. {success}/{total} evaluated, {errors} failures.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate structured LLM annotations using MQM + breakdown verification"
    )
    parser.add_argument("model", help="Model name to evaluate")
    parser.add_argument("--judge", type=str, default="openai/gpt-4o-mini", help="Judge model (OpenRouter ID)")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--subfolder", type=str, default=None, help="Process only this subfolder")
    args = parser.parse_args()
    run(args.model, args.judge, args.workers, args.subfolder)
