"""MQM evaluation for transform descriptions (Category 1: full-visibility transforms).

Evaluates model descriptions of transformed figures against groundtruth using
the original (clean) image + groundtruth reference. The judge sees the original
image so it can fully assess completeness and accuracy.

Category 1 transforms: original, jpeg_compression, noise, aspect_ratio,
low_contrast, rotation, original_in_paper

Output: output/evaluation/transforms/{judge}/{model}/{transform}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/evaluation/evaluate_transforms.py gpt-5.2 --judge gpt-4o --workers 4
    python3 scripts/evaluation/evaluate_transforms.py gpt-5.2 --judge gpt-4o --transform original_in_paper
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

from evaluation.mqm_evaluator import evaluate_judge_c

TRANSFORMS_DIR = ROOT / "output" / "experiments" / "transforms"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
SAMPLES_FILE = ROOT / "adversarial_experiments" / "samples.json"
OUTPUT_DIR = ROOT / "output" / "evaluation" / "transforms"

CATEGORY_1_TRANSFORMS = [
    "original",
    "jpeg_compression",
    "noise",
    "aspect_ratio",
    "low_contrast",
    "rotation",
    "original_in_paper",
    "blurred_in_paper",
]

SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "english_only": "English",
    "german_only": "German",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_reference(gt, lang):
    for a in gt.get("annotations", []):
        if a.get("annotation_language") == lang:
            return a.get("annotation", "")
    return ""


def _process(fig_key, subfolder, model_name, transform, judge_model):
    gen_path = TRANSFORMS_DIR / model_name / transform / subfolder / f"{fig_key}.json"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
    out_path = OUTPUT_DIR / judge_model / model_name / transform / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"
    if not gen_path.exists() or not gt_path.exists() or not fig_path.exists():
        return True, fig_key, "skip"

    with open(gen_path) as f:
        gen = json.load(f)
    with open(gt_path) as f:
        gt = json.load(f)

    if "model_annotations" in gen:
        mqm_by_lang = {}
        for lang, annotation in sorted(gen["model_annotations"].items()):
            reference = _get_reference(gt, lang)
            if not reference:
                continue
            try:
                result = evaluate_judge_c(
                    image_path=fig_path, annotation=annotation, reference=reference,
                    caption="", paper_title="",
                    figure_type=gen.get("figure_type", ""), judge_model=judge_model,
                )
                mqm_by_lang[lang] = result
            except Exception as e:
                logger.error(f"  FAIL {transform}/{fig_key} ({lang}): {e}")
                return False, fig_key, str(e)

        if not mqm_by_lang:
            return True, fig_key, "skip"

        avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)
        eval_result = {
            "figure_key": fig_key, "model_name": model_name,
            "transform": transform, "figure_type": gen.get("figure_type", ""),
            "judge_type": "reference_with_image", "judge_model": judge_model,
            "mqm_by_language": mqm_by_lang, "mqm_score_avg": round(avg_mqm, 2),
        }
        logger.info(f"  OK   {transform}/{subfolder}/{fig_key}: avg MQM={avg_mqm:.1f} ({len(mqm_by_lang)} langs)")
    else:
        annotation = gen.get("model_annotation", "")
        lang = SUBFOLDER_TO_LANGUAGE.get(subfolder, gt.get("paper_language", "English"))
        reference = _get_reference(gt, lang)
        if not reference:
            return True, fig_key, "skip"

        try:
            result = evaluate_judge_c(
                image_path=fig_path, annotation=annotation, reference=reference,
                caption="", paper_title="",
                figure_type=gen.get("figure_type", ""), judge_model=judge_model,
            )
        except Exception as e:
            logger.error(f"  FAIL {transform}/{fig_key}: {e}")
            return False, fig_key, str(e)

        eval_result = {
            "figure_key": fig_key, "model_name": model_name,
            "transform": transform, "figure_type": gen.get("figure_type", ""),
            "judge_type": "reference_with_image", "judge_model": judge_model,
            **result,
        }
        logger.info(f"  OK   {transform}/{subfolder}/{fig_key}: MQM={result['mqm_score']}, {result['error_count']} errors")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(eval_result, f, indent=2, ensure_ascii=False)
    return True, fig_key, "done"


def run(model_name, judge_model="azure/gpt-4o", workers=4, transform_filter=None, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        samples = json.load(f)

    transforms = list(CATEGORY_1_TRANSFORMS)
    if transform_filter:
        transforms = [t for t in transforms if t == transform_filter]
        if not transforms:
            logger.error(f"Unknown transform: {transform_filter}. Available: {CATEGORY_1_TRANSFORMS}")
            return

    logger.info(f"Transform MQM evaluation | model={model_name} | judge={judge_model} | workers={workers}")
    logger.info(f"Transforms: {transforms}")

    work_items = []
    skipped = 0
    for transform in transforms:
        for subfolder, fig_keys in samples["samples"].items():
            if subfolder_filter and subfolder != subfolder_filter:
                continue
            for fig_key in fig_keys:
                gen_path = TRANSFORMS_DIR / model_name / transform / subfolder / f"{fig_key}.json"
                out_path = OUTPUT_DIR / judge_model / model_name / transform / subfolder / f"{fig_key}.json"
                gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
                fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
                if out_path.exists():
                    skipped += 1
                elif gen_path.exists() and gt_path.exists() and fig_path.exists():
                    work_items.append((fig_key, subfolder, transform))

    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to evaluate)")
    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok: success += 1
            else: errors += 1
            d = success + errors - skipped
            if d % 10 == 0 or not ok:
                logger.info(f"  Progress: {d}/{len(work_items)} (errors={errors})")

    if workers == 1:
        for fk, sub, t in work_items:
            ok, k, s = _process(fk, sub, model_name, t, judge_model)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_process, fk, sub, model_name, t, judge_model): fk for fk, sub, t in work_items}
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock: errors += 1

    # Summary
    print(f"\n=== SUMMARY ({model_name} judged by {judge_model}) ===")
    by_transform = {}
    for transform in transforms:
        scores = []
        eval_dir = OUTPUT_DIR / judge_model / model_name / transform
        if eval_dir.exists():
            for ef in eval_dir.rglob("*.json"):
                data = json.load(open(ef))
                s = data.get("mqm_score_avg") or data.get("mqm_score")
                if s is not None:
                    scores.append(s)
        if scores:
            avg = sum(scores) / len(scores)
            by_transform[transform] = (avg, len(scores))
            print(f"  {transform}: MQM={avg:.2f} ({len(scores)} figures)")

    if by_transform:
        all_scores = [s for t, (s, _) in by_transform.items() for _ in range(1)]
        print(f"  ---")
        for t, (avg, n) in sorted(by_transform.items(), key=lambda x: -x[1][0]):
            print(f"  {t}: {avg:.2f}")

    logger.info(f"Done. {success}/{len(work_items)+skipped} evaluated, {errors} failures.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="MQM evaluation for transform descriptions")
    p.add_argument("model", help="Model name to evaluate")
    p.add_argument("--judge", default="azure/gpt-4o", help="Judge model (e.g. azure/gpt-4o)")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--transform", default=None, help="Filter to specific transform")
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.transform, a.subfolder)
