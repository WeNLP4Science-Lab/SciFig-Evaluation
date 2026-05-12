"""Generate figure descriptions using ENGLISH prompts for ALL languages.

Same as run_transforms.py but forces English prompts regardless of figure language.
This is a prompt ablation experiment to measure the effect of native-language prompting.

Output: output/experiments/transforms_english_prompt/<model>/<transform>/<subfolder>/<fig_key>.json

Usage:
    python3 scripts/experiments/run_transforms_english_prompt.py gpt-5.2 --transform original --workers 4
    python3 scripts/experiments/run_transforms.py --list-models
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
OUTPUT_DIR = ROOT / "output" / "experiments" / "transforms_english_prompt"

ALL_TRANSFORMS = [
    "original",
    "jpeg_compression",
    "noise",
    "aspect_ratio",
    "low_contrast",
    "rotation",
    "axis_blurred",
    "selective_blur",
    "blurred_in_paper",
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_transform_image_path(subfolder, fig_key, transform):
    """Get the path to a transformed image."""
    if transform == "original":
        return FIGURES_DIR / subfolder / fig_key / "original.png"
    return FIGURES_DIR / subfolder / fig_key / "transforms" / f"{transform}.png"


def _process_figure(annotator, prompts, transform, subfolder, fig_key):
    """Process a single transformed figure."""
    fig_path = _get_transform_image_path(subfolder, fig_key, transform)
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / annotator.model_name / transform / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not fig_path.exists():
        logger.warning(f"  SKIP {transform}/{subfolder}/{fig_key} — no transformed image")
        return True, fig_key, "skip"
    if not gt_path.exists():
        logger.warning(f"  SKIP {transform}/{subfolder}/{fig_key} — no groundtruth")
        return True, fig_key, "skip"

    with open(gt_path) as f:
        gt = json.load(f)

    figure_type = gt["figure_type"]

    if subfolder == "multi_language":
        languages = sorted(set(a["annotation_language"] for a in gt["annotations"]))
    else:
        languages = [gt["paper_language"]]

    try:
        if len(languages) == 1:
            prompt_text = get_prompt(prompts, "English", figure_type)
            description = annotator.annotate_figure(
                prompt=prompt_text,
                image_path=fig_path,
                caption="",
                paper_title="",
            )

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "model_name": annotator.model_name,
                "transform": transform,
                "condition": "image_only",
                "model_annotation": description,
            }
        else:
            annotations_by_lang = {}
            for lang in languages:
                prompt_text = get_prompt(prompts, "English", figure_type)
                desc = annotator.annotate_figure(
                    prompt=prompt_text,
                    image_path=fig_path,
                    caption="",
                    paper_title="",
                )
                annotations_by_lang[lang] = desc

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "model_name": annotator.model_name,
                "transform": transform,
                "condition": "image_only",
                "model_annotations": annotations_by_lang,
            }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {transform}/{subfolder}/{fig_key}")
        return True, fig_key, "done"

    except Exception as e:
        logger.error(f"  FAIL {transform}/{subfolder}/{fig_key}: {e}")
        return False, fig_key, str(e)


def run(model_name="gpt-5.2", workers=4, transform_filter=None, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        adv = json.load(f)

    transforms = list(ALL_TRANSFORMS)
    if transform_filter:
        transforms = [t for t in transforms if t == transform_filter]
        if not transforms:
            logger.error(f"Unknown transform: {transform_filter}. Available: {ALL_TRANSFORMS}")
            return

    annotator = get_annotator(model_name)
    prompts = load_prompts()

    # Build work items
    work_items = []
    skipped = 0
    for transform in transforms:
        for subfolder, fig_keys in adv["samples"].items():
            if subfolder_filter and subfolder != subfolder_filter:
                continue
            for fig_key in fig_keys:
                out_path = OUTPUT_DIR / annotator.model_name / transform / subfolder / f"{fig_key}.json"
                fig_path = _get_transform_image_path(subfolder, fig_key, transform)
                if out_path.exists():
                    skipped += 1
                elif fig_path.exists():
                    work_items.append((transform, subfolder, fig_key))

    total = len(work_items) + skipped
    logger.info(f"Transform generation | model={annotator.model_name}")
    logger.info(f"Transforms: {transforms}")
    logger.info(f"Total: {total} ({skipped} done, {len(work_items)} to generate)")

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
        for t, sub, fk in work_items:
            ok, k, s = _process_figure(annotator, prompts, t, sub, fk)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, annotator, prompts, t, sub, fk): fk
                for t, sub, fk in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock:
                        errors += 1

    logger.info(f"Done. {success}/{total} generated, {errors} failures.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate descriptions for adversarial-transformed figures")
    p.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--transform", default=None, help="Filter to specific transform")
    p.add_argument("--subfolder", default=None, help="Filter to specific subfolder")
    p.add_argument("--list-models", action="store_true", help="List available models and exit")
    a = p.parse_args()

    if a.list_models:
        models = sorted(_get_all_models().keys())
        print(f"Available models ({len(models)}):")
        for m in models:
            print(f"  {m}")
        sys.exit(0)

    run(a.model, a.workers, a.transform, a.subfolder)
