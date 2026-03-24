"""Reference-with-image evaluation (image + groundtruth + model output).

The judge has access to both the figure image and the human expert reference
annotation, providing the most comprehensive evaluation context.

Usage:
    python3 scripts/evaluation/evaluate_reference_with_image.py <model_name> [--judge MODEL] [--workers N] [--subfolder X]
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

GENERATION_DIR = ROOT / "output" / "generation"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

ALL_SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]

SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "english_only": "English",
    "german_only": "German",
}


def _judge_slug(judge_model):
    """Convert judge model ID to a filesystem-safe slug."""
    return judge_model.split("/")[-1]


def _output_dir(judge_model):
    return ROOT / "output" / "evaluation" / "reference_with_image" / _judge_slug(judge_model)


def _load_samples(samples_path):
    """Load samples.json and return a dict of {subfolder: set(fig_keys)}."""
    with open(samples_path) as f:
        data = json.load(f)
    result = {}
    for subfolder, types in data["samples"].items():
        keys = set()
        for fig_type, figs in types.items():
            keys.update(figs)
        result[subfolder] = keys
    return result


def _discover(subfolder, model_name, sample_keys=None):
    folder = GENERATION_DIR / model_name / subfolder
    keys = sorted(p.stem for p in folder.glob("*.json")) if folder.exists() else []
    if sample_keys is not None and subfolder in sample_keys:
        keys = [k for k in keys if k in sample_keys[subfolder]]
    return keys


def _get_reference(gt, lang):
    """Extract reference annotation for a given language from groundtruth."""
    for a in gt.get("annotations", []):
        if a.get("annotation_language") == lang:
            return a.get("annotation", "")
    return ""


def _process(fig_key, subfolder, model_name, judge_model):
    gen_path = GENERATION_DIR / model_name / subfolder / f"{fig_key}.json"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
    out_path = _output_dir(judge_model) / model_name / subfolder / f"{fig_key}.json"

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
                logger.warning(f"  SKIP {fig_key} ({lang}) — no reference annotation")
                continue
            try:
                result = evaluate_judge_c(
                    image_path=fig_path, annotation=annotation, reference=reference,
                    caption=gen.get("caption", ""), paper_title=gen.get("paper_title", ""),
                    figure_type=gen.get("figure_type", ""), judge_model=judge_model,
                )
                mqm_by_lang[lang] = result
            except Exception as e:
                logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                return False, fig_key, str(e)

        if not mqm_by_lang:
            return True, fig_key, "skip"

        avg_mqm = sum(r["mqm_score"] for r in mqm_by_lang.values()) / len(mqm_by_lang)
        eval_result = {
            "figure_key": fig_key, "model_name": gen.get("model_name", model_name),
            "figure_type": gen.get("figure_type", ""), "judge_type": "reference_with_image",
            "judge_model": judge_model,
            "mqm_by_language": mqm_by_lang, "mqm_score_avg": round(avg_mqm, 2),
        }
        logger.info(f"  OK   {fig_key}: avg MQM={avg_mqm:.1f} ({len(mqm_by_lang)} langs)")
    else:
        annotation = gen.get("model_annotation", "")
        lang = SUBFOLDER_TO_LANGUAGE.get(subfolder, gt.get("paper_language", "English"))
        reference = _get_reference(gt, lang)
        if not reference:
            return True, fig_key, "skip"

        try:
            result = evaluate_judge_c(
                image_path=fig_path, annotation=annotation, reference=reference,
                caption=gen.get("caption", ""), paper_title=gen.get("paper_title", ""),
                figure_type=gen.get("figure_type", ""), judge_model=judge_model,
            )
        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")
            return False, fig_key, str(e)

        eval_result = {
            "figure_key": fig_key, "model_name": gen.get("model_name", model_name),
            "figure_type": gen.get("figure_type", ""), "judge_type": "reference_with_image",
            "judge_model": judge_model,
            **result,
        }
        logger.info(f"  OK   {fig_key}: MQM={result['mqm_score']}, {result['error_count']} errors")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(eval_result, f, indent=2, ensure_ascii=False)
    return True, fig_key, "done"


def run(model_name, judge_model="openai/gpt-4o-mini", workers=1, subfolder_filter=None, samples_path=None):
    subfolders = [subfolder_filter] if subfolder_filter else ALL_SUBFOLDERS
    sample_keys = _load_samples(samples_path) if samples_path else None
    out_base = _output_dir(judge_model)
    logger.info(f"Reference-with-image | model={model_name} | judge={judge_model} | workers={workers}")
    if samples_path:
        logger.info(f"Samples filter: {samples_path}")
    logger.info(f"Output: {out_base / model_name}")

    work_items, skipped = [], 0
    for sub in subfolders:
        (out_base / model_name / sub).mkdir(parents=True, exist_ok=True)
        for fig_key in _discover(sub, model_name, sample_keys):
            out_path = out_base / model_name / sub / f"{fig_key}.json"
            gt_path = GROUNDTRUTH_DIR / sub / f"{fig_key}.json"
            fig_path = FIGURES_DIR / sub / f"{fig_key}.png"
            if out_path.exists():
                skipped += 1
            elif gt_path.exists() and fig_path.exists():
                work_items.append((fig_key, sub))

    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to evaluate)")
    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors, lock = skipped, 0, threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok: success += 1
            else: errors += 1
            d = success + errors - skipped
            if d % 10 == 0 or not ok:
                logger.info(f"  Progress: {d}/{len(work_items)} (errors={errors})")

    if workers == 1:
        for fk, sub in work_items:
            ok, k, s = _process(fk, sub, model_name, judge_model)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_process, fk, sub, model_name, judge_model): fk for fk, sub in work_items}
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock: errors += 1

    logger.info(f"Done. {success}/{len(work_items)+skipped} evaluated, {errors} failures.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Reference-with-image MQM evaluation (image + groundtruth)")
    p.add_argument("model", help="Model name to evaluate")
    p.add_argument("--judge", default="openai/gpt-4o-mini", help="Judge model")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--subfolder", default=None)
    p.add_argument("--samples", default=None, help="Path to samples.json to filter figures")
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.subfolder, a.samples)
