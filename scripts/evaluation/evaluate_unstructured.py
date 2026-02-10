"""Evaluate paragraph-only (unstructured) LLM annotations using MQM.

Reads generated outputs from output/generation/ and writes evaluation
results to output/evaluation/.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/evaluation/evaluate_unstructured.py
"""

import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from evaluation.mqm_evaluator import evaluate_annotation

GENERATION_DIR = ROOT / "output" / "generation"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "evaluation"

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
    "bulgarian_only": [f"bulgarian_fig_{i:03d}" for i in range(1, 5)],
    "chinese_only": [f"chinese_fig_{i:03d}" for i in range(1, 5)],
    "english_only": [f"english_fig_{i:03d}" for i in range(1, 5)],
    "german_only": [f"german_fig_{i:03d}" for i in range(1, 5)],
    "multi_language": [f"multi_fig_{i:03d}" for i in range(1, 5)],
}


def run(model_name: str = "gpt-4o-mini", judge_model: str = "openai/gpt-4o-mini"):
    gen_model_dir = GENERATION_DIR / model_name
    eval_output_dir = OUTPUT_DIR / model_name

    logger.info(f"Evaluating model: {model_name}")
    logger.info(f"Judge model: {judge_model}")
    logger.info(f"Source: {gen_model_dir}")
    logger.info(f"Output: {eval_output_dir}")
    print()

    total = 0
    success = 0
    errors = 0

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

            # Handle multi-language (model_annotations dict) vs single (model_annotation str)
            if "model_annotations" in gen:
                # Multi-language: evaluate each language separately
                logger.info(f"  [{subfolder}] {fig_key} — multi-language evaluation")
                mqm_by_lang = {}
                failed = False

                for lang, annotation in gen["model_annotations"].items():
                    logger.info(f"         evaluating {lang}...")
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
                        logger.info(f"         {lang}: MQM={result['mqm_score']}, {result['error_count']} errors")
                    except Exception as e:
                        logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                        failed = True
                        break

                if failed:
                    errors += 1
                    continue

                # Compute average MQM across languages
                avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)

                eval_result = {
                    "figure_key": fig_key,
                    "model_name": model_name,
                    "figure_type": gen.get("figure_type", ""),
                    "evaluation_type": "unstructured",
                    "mqm_by_language": mqm_by_lang,
                    "mqm_score_avg": round(avg_mqm, 2),
                }

            else:
                # Single language
                annotation = gen.get("model_annotation", "")
                logger.info(f"  [{subfolder}] {fig_key} ({gen.get('figure_type', '')})...")

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
                    errors += 1
                    continue

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
            success += 1

    print()
    logger.info(f"Done. {success}/{total} evaluated, {errors} failures.")


if __name__ == "__main__":
    run()
