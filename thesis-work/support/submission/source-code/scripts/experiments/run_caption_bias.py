"""Generate figure descriptions under caption bias conditions.

Two conditions:
  1. modified_caption: image + poisoned caption (tests resistance)
  2. image_only: image alone, no caption (tests caption dependency)

Output: output/experiments/caption_bias/<condition>/<model>/<subfolder>/<fig_key>.json

Usage:
    python3 scripts/experiments/run_caption_bias.py gpt-5.2 --condition modified_caption --workers 4
    python3 scripts/experiments/run_caption_bias.py gpt-5.2 --condition image_only
    python3 scripts/experiments/run_caption_bias.py --list-models
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator, _get_all_models
from llm_generation.prompts import load_prompts, get_prompt

ADVERSARIAL_DIR = ROOT / "adversarial_experiments"
SAMPLES_FILE = ADVERSARIAL_DIR / "samples.json"
FIGURES_DIR = ADVERSARIAL_DIR / "figures"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
CAPTION_BIAS_DIR = ADVERSARIAL_DIR / "benchmarks" / "adversarial" / "caption_bias"
OUTPUT_DIR = ROOT / "output" / "experiments" / "caption_bias"

CONDITIONS = ["modified_caption", "image_only"]

SUBFOLDER_TO_LANG_FILE = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _load_modified_captions():
    """Load all modified captions across languages."""
    captions = {}
    for lang_file in CAPTION_BIAS_DIR.glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        captions.update(data)
    return captions


def _process_figure(annotator, prompts, condition, subfolder, fig_key, modified_captions):
    """Process a single figure under a caption bias condition."""
    fig_path = FIGURES_DIR / subfolder / fig_key / "original.png"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / condition / annotator.model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not fig_path.exists():
        return False, fig_key, f"no image: {fig_path}"
    if not gt_path.exists():
        return False, fig_key, f"no groundtruth: {gt_path}"

    with open(gt_path) as f:
        gt = json.load(f)

    figure_type = gt["figure_type"]

    if subfolder == "multi_language":
        languages = sorted(set(a["annotation_language"] for a in gt["annotations"]))
    else:
        languages = [gt["paper_language"]]

    # Determine caption and paper_title based on condition
    if condition == "modified_caption":
        caption_data = modified_captions.get(fig_key, {})
        caption = caption_data.get("modified_caption", gt["caption"])
        paper_title = gt.get("paper_title", "")
    elif condition == "image_only":
        caption = ""
        paper_title = ""

    try:
        if len(languages) == 1:
            prompt_text = get_prompt(prompts, languages[0], figure_type)
            description = annotator.annotate_figure(
                prompt=prompt_text,
                image_path=fig_path,
                caption=caption,
                paper_title=paper_title,
            )

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "paper_title": gt.get("paper_title", ""),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "condition": condition,
                "caption_used": caption,
                "model_name": annotator.model_name,
                "model_annotation": description,
            }
        else:
            annotations_by_lang = {}
            for lang in languages:
                prompt_text = get_prompt(prompts, lang, figure_type)
                desc = annotator.annotate_figure(
                    prompt=prompt_text,
                    image_path=fig_path,
                    caption=caption,
                    paper_title=paper_title,
                )
                annotations_by_lang[lang] = desc

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "paper_title": gt.get("paper_title", ""),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "condition": condition,
                "caption_used": caption,
                "model_name": annotator.model_name,
                "model_annotations": annotations_by_lang,
            }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {condition}/{subfolder}/{fig_key}")
        return True, fig_key, "done"

    except Exception as e:
        logger.error(f"  FAIL {condition}/{subfolder}/{fig_key}: {e}")
        return False, fig_key, str(e)


def run(model_name="gpt-5.2", condition="modified_caption", workers=4, subfolder_filter=None):
    if condition not in CONDITIONS:
        logger.error(f"Unknown condition: {condition}. Available: {CONDITIONS}")
        return

    with open(SAMPLES_FILE) as f:
        samples = json.load(f)["samples"]

    annotator = get_annotator(model_name)
    prompts = load_prompts()
    modified_captions = _load_modified_captions() if condition == "modified_caption" else {}

    # Build work items
    work_items = []
    skipped = 0
    for subfolder, fig_keys in samples.items():
        if subfolder_filter and subfolder != subfolder_filter:
            continue
        for fig_key in fig_keys:
            out_path = OUTPUT_DIR / condition / annotator.model_name / subfolder / f"{fig_key}.json"
            if out_path.exists():
                skipped += 1
            else:
                work_items.append((subfolder, fig_key))

    total = len(work_items) + skipped
    logger.info(f"Caption bias | model={annotator.model_name} | condition={condition}")
    logger.info(f"Total: {total} ({skipped} done, {len(work_items)} to run)")

    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok:
                success += 1
            else:
                errors += 1
            d = success + errors - skipped
            if d % 10 == 0 or not ok:
                logger.info(f"  Progress: {d}/{len(work_items)} (errors={errors})")

    if workers == 1:
        for sub, fk in work_items:
            ok, k, s = _process_figure(annotator, prompts, condition, sub, fk, modified_captions)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, annotator, prompts, condition, sub, fk, modified_captions): fk
                for sub, fk in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock:
                        errors += 1

    logger.info(f"Done. {success}/{total} completed, {errors} errors.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate descriptions under caption bias conditions")
    p.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    p.add_argument("--condition", required=True, choices=CONDITIONS, help="Caption condition")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    p.add_argument("--list-models", action="store_true")
    a = p.parse_args()

    if a.list_models:
        models = sorted(_get_all_models().keys())
        print(f"Available models ({len(models)}):")
        for m in models:
            print(f"  {m}")
        sys.exit(0)

    run(a.model, a.condition, a.workers, a.subfolder)
