"""Evaluate paragraph-only (unstructured) LLM annotations using MQM.

Reads generated outputs from output/generation/ and writes evaluation
results to output/evaluation/.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/evaluation/evaluate_unstructured.py <model_name> [--workers N] [--subfolder X] [--judge MODEL]
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

GENERATION_DIR = ROOT / "output" / "generation"
FIGURES_DIR = ROOT / "Dataset" / "figures"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
OUTPUT_DIR = ROOT / "output" / "evaluation"

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

    if "model_annotations" in gen:
        # Multi-language: evaluate each language separately
        mqm_by_lang = {}
        for lang, annotation in sorted(gen["model_annotations"].items()):
            try:
                result = evaluate_annotation(
                    image_path=fig_path,
                    annotation=annotation,
                    caption=gen.get("caption", ""),
                    paper_title=gen.get("paper_title", ""),
                    figure_type=gen.get("figure_type", ""),
                    judge_model=judge_model,
                )
                mqm_by_lang[lang] = result
            except Exception as e:
                logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                return False, fig_key, str(e)

        avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)
        eval_result = {
            "figure_key": fig_key,
            "model_name": model_name,
            "figure_type": gen.get("figure_type", ""),
            "evaluation_type": "unstructured",
            "mqm_by_language": mqm_by_lang,
            "mqm_score_avg": round(avg_mqm, 2),
        }
        logger.info(f"  OK   {fig_key}: avg MQM={avg_mqm:.1f} ({len(mqm_by_lang)} langs)")

    else:
        annotation = gen.get("model_annotation", "")
        try:
            result = evaluate_annotation(
                image_path=fig_path,
                annotation=annotation,
                caption=gen.get("caption", ""),
                paper_title=gen.get("paper_title", ""),
                figure_type=gen.get("figure_type", ""),
                judge_model=judge_model,
            )
        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")
            return False, fig_key, str(e)

        eval_result = {
            "figure_key": fig_key,
            "model_name": model_name,
            "figure_type": gen.get("figure_type", ""),
            "evaluation_type": "unstructured",
            **result,
        }
        logger.info(f"  OK   {fig_key}: MQM={result['mqm_score']}, {result['error_count']} errors")

    with open(out_path, "w") as f:
        json.dump(eval_result, f, indent=2, ensure_ascii=False)
    return True, fig_key, "done"


def run(model_name: str, judge_model: str = "openai/gpt-4o-mini",
        workers: int = 1, subfolder_filter: str | None = None):
    subfolders = [subfolder_filter] if subfolder_filter else ALL_SUBFOLDERS
    eval_output_dir = OUTPUT_DIR / model_name

    logger.info(f"Evaluating model: {model_name}")
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
    parser = argparse.ArgumentParser(description="Evaluate unstructured LLM annotations using MQM")
    parser.add_argument("model", help="Model name to evaluate")
    parser.add_argument("--judge", type=str, default="openai/gpt-4o-mini", help="Judge model (OpenRouter ID)")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--subfolder", type=str, default=None, help="Process only this subfolder")
    args = parser.parse_args()
    run(args.model, args.judge, args.workers, args.subfolder)
