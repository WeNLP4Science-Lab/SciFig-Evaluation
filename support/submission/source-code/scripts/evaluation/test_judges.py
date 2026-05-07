"""Quick test: run all 3 judges on a few figures across all models.

Usage:
    python3 scripts/evaluation/test_judges.py [--limit N] [--workers N] [--subfolder X]
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from evaluation.mqm_evaluator import evaluate_judge_a, evaluate_judge_b, evaluate_judge_c
from llm_generation.prompts import load_prompts, get_prompt

GENERATION_DIR = ROOT / "output" / "generation"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_BASE = ROOT / "output" / "evaluation"

SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "english_only": "English",
    "german_only": "German",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

PROMPTS = load_prompts()


def _judge_slug(judge_model):
    return judge_model.split("/")[-1]


def _get_reference(gt, lang):
    for a in gt.get("annotations", []):
        if a.get("annotation_language") == lang:
            return a.get("annotation", "")
    return ""


def _run_one(model_name, fig_key, subfolder, judge_model, skip_ref_only=False):
    """Run judges for one figure/model combo. Returns list of (judge_type, result_or_error)."""
    gen_path = GENERATION_DIR / model_name / subfolder / f"{fig_key}.json"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"

    with open(gen_path) as f:
        gen = json.load(f)
    with open(gt_path) as f:
        gt = json.load(f)

    annotation = gen.get("model_annotation", "")
    figure_type = gen.get("figure_type", "")
    caption = gen.get("caption", "")
    paper_title = gen.get("paper_title", "")
    lang = SUBFOLDER_TO_LANGUAGE.get(subfolder, gt.get("paper_language", "English"))
    reference = _get_reference(gt, lang)
    slug = _judge_slug(judge_model)

    results = []

    judge_types = ["reference_free", "reference_with_image"] if skip_ref_only else ["reference_free", "reference_only", "reference_with_image"]
    for judge_type in judge_types:
        out_dir = OUTPUT_BASE / judge_type / slug / model_name / subfolder
        out_path = out_dir / f"{fig_key}.json"

        if out_path.exists():
            results.append((judge_type, "skip"))
            continue

        try:
            if judge_type == "reference_free":
                gen_prompt = get_prompt(PROMPTS, lang, figure_type)
                result = evaluate_judge_a(
                    image_path=fig_path, annotation=annotation, caption=caption,
                    paper_title=paper_title, figure_type=figure_type,
                    generation_prompt=gen_prompt, judge_model=judge_model,
                )
            elif judge_type == "reference_only":
                result = evaluate_judge_b(
                    annotation=annotation, reference=reference, caption=caption,
                    paper_title=paper_title, figure_type=figure_type, judge_model=judge_model,
                )
            else:
                result = evaluate_judge_c(
                    image_path=fig_path, annotation=annotation, reference=reference,
                    caption=caption, paper_title=paper_title, figure_type=figure_type,
                    judge_model=judge_model,
                )

            eval_result = {
                "figure_key": fig_key, "model_name": model_name,
                "figure_type": figure_type, "judge_type": judge_type,
                "judge_model": judge_model, **result,
            }

            out_dir.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(eval_result, f, indent=2, ensure_ascii=False)

            results.append((judge_type, result))
            logger.info(f"  OK {model_name}/{fig_key} [{judge_type}] MQM={result['mqm_score']} errors={result['error_count']}")

        except Exception as e:
            logger.error(f"  FAIL {model_name}/{fig_key} [{judge_type}]: {e}")
            results.append((judge_type, str(e)))

    return model_name, fig_key, results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3, help="Number of figures to test")
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers")
    parser.add_argument("--subfolder", default="german_only")
    parser.add_argument("--judge", default="openai/gpt-4o-mini")
    parser.add_argument("--skip-ref-only", action="store_true", help="Skip reference_only judge type")
    args = parser.parse_args()

    models = sorted(d.name for d in GENERATION_DIR.iterdir() if d.is_dir())
    fig_keys = sorted(
        p.stem for p in (GENERATION_DIR / models[0] / args.subfolder).glob("*.json")
    )[:args.limit]

    n_judges = 2 if args.skip_ref_only else 3
    logger.info(f"Testing {len(fig_keys)} figures x {len(models)} models x {n_judges} judges = {len(fig_keys)*len(models)*n_judges} evaluations")
    logger.info(f"Figures: {fig_keys}")
    logger.info(f"Models: {models}")
    logger.info(f"Judge: {args.judge}")
    print()

    work = [(m, fk) for m in models for fk in fig_keys]

    done, failed = 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {
            ex.submit(_run_one, m, fk, args.subfolder, args.judge, args.skip_ref_only): (m, fk)
            for m, fk in work
        }
        for f in as_completed(futs):
            try:
                model_name, fig_key, results = f.result()
                for jt, r in results:
                    if isinstance(r, str) and r != "skip":
                        failed += 1
                    else:
                        done += 1
            except Exception as e:
                m, fk = futs[f]
                logger.error(f"  UNEXPECTED {m}/{fk}: {e}")
                failed += n_judges

    print()
    logger.info(f"Done. {done} succeeded, {failed} failed out of {len(work)*n_judges} total.")


if __name__ == "__main__":
    main()
