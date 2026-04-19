"""Generate figure descriptions for in-paper transformed images.

Unlike regular transforms, in-paper images show the figure embedded in a paper page.
The prompt includes the figure number so the model knows which figure to describe.

Transforms: original_in_paper, blurred_in_paper

Output: output/experiments/transforms/<model>/<transform>/<subfolder>/<fig_key>.json

Usage:
    python3 scripts/experiments/run_inpaper_transforms.py gpt-5.2 --workers 4
    python3 scripts/experiments/run_inpaper_transforms.py gpt-5.2 --transform blurred_in_paper
    python3 scripts/experiments/run_inpaper_transforms.py --list-models
"""

import argparse
import json
import logging
import os
import re
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
OUTPUT_DIR = ROOT / "output" / "experiments" / "transforms"

INPAPER_TRANSFORMS = ["original_in_paper", "blurred_in_paper"]
FIGURE_NUMBERS_FILE = ADVERSARIAL_DIR / "benchmarks" / "inpaper_figure_numbers.json"
EXCLUDED_FILE = ADVERSARIAL_DIR / "benchmarks" / "inpaper_excluded.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _load_figure_numbers():
    """Load verified figure numbers from mapping file."""
    with open(FIGURE_NUMBERS_FILE) as f:
        data = json.load(f)
    return {k: v["figure_number"] for k, v in data["figures"].items() if v.get("figure_number")}


def _load_excluded():
    """Load excluded figure keys for in-paper experiments."""
    with open(EXCLUDED_FILE) as f:
        data = json.load(f)
    return {e["figure_key"] for e in data.get("excluded", [])}


def _get_inpaper_image_path(subfolder, fig_key, transform):
    """Get the path to an in-paper image."""
    if transform == "original_in_paper":
        # original_in_paper is at the figure root level
        for ext in [".png", ".jpeg", ".jpg"]:
            p = FIGURES_DIR / subfolder / fig_key / f"original_in_paper{ext}"
            if p.exists():
                return p
    elif transform == "blurred_in_paper":
        # blurred_in_paper is in transforms/
        for ext in [".png", ".jpeg", ".jpg"]:
            p = FIGURES_DIR / subfolder / fig_key / "transforms" / f"blurred_in_paper{ext}"
            if p.exists():
                return p
    return None


def _parse_figure_number(figure_filename):
    """Extract figure number from groundtruth filename.

    Handles both formats:
    - 025_2502.20339v1_Figure5.png -> 5
    - ISA.2025.1.02_fig1.png -> 1
    """
    m = re.search(r'[Ff]ig(?:ure)?[._\s-]*(\d+)', figure_filename)
    if m:
        return m.group(1)
    return None


def _build_user_text(fig_num):
    """Build the user text for in-paper prompts."""
    return f"This image shows a page from a scientific paper. Please focus only on Figure {fig_num} in this page."


def _annotate_inpaper(annotator, system_prompt, image_path, instruction):
    """Call the model with in-paper instruction instead of caption.

    Bypasses the normal annotate_figure() to avoid the 'Caption:' prefix.
    Sends instruction directly as user text alongside the image.
    """
    import base64
    from openai import AzureOpenAI, OpenAI

    b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    mime = "image/jpeg" if image_path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"

    user_content = [
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "high"}},
        {"type": "text", "text": f"Instruction: {instruction}"},
    ]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    # Use Azure if available, otherwise OpenRouter
    if hasattr(annotator, '_deployment_name'):
        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-12-01-preview",
        )
        model = annotator._deployment_name
        token_param = "max_completion_tokens" if "gpt-5" in model or "gpt-4.1" in model else "max_tokens"
    else:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        model = annotator.router_model_id
        token_param = "max_tokens"

    import time
    delay = 1.0
    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                **{token_param: 2048},
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt == 3:
                raise
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= 2.0


def _process_figure(annotator, prompts, transform, subfolder, fig_key, figure_numbers):
    """Process a single in-paper figure."""
    fig_path = _get_inpaper_image_path(subfolder, fig_key, transform)
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / annotator.model_name / transform / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not fig_path:
        logger.warning(f"  SKIP {transform}/{subfolder}/{fig_key} — no in-paper image")
        return True, fig_key, "skip_no_image"

    if not gt_path.exists():
        logger.warning(f"  SKIP {transform}/{subfolder}/{fig_key} — no groundtruth")
        return True, fig_key, "skip_no_gt"

    with open(gt_path) as f:
        gt = json.load(f)

    figure_type = gt["figure_type"]
    fig_num = figure_numbers.get(fig_key)

    if not fig_num:
        logger.warning(f"  SKIP {transform}/{subfolder}/{fig_key} — no figure number in mapping")
        return True, fig_key, "skip_no_fignum"

    if subfolder == "multi_language":
        languages = sorted(set(a["annotation_language"] for a in gt["annotations"]))
    else:
        languages = [gt["paper_language"]]

    instruction = _build_user_text(fig_num)

    try:
        if len(languages) == 1:
            prompt_text = get_prompt(prompts, languages[0], figure_type)
            description = _annotate_inpaper(annotator, prompt_text, fig_path, instruction)

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "figure_number": fig_num,
                "model_name": annotator.model_name,
                "transform": transform,
                "condition": "in_paper",
                "model_annotation": description,
            }
        else:
            annotations_by_lang = {}
            for lang in languages:
                prompt_text = get_prompt(prompts, lang, figure_type)
                desc = _annotate_inpaper(annotator, prompt_text, fig_path, instruction)
                annotations_by_lang[lang] = desc

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "figure_number": fig_num,
                "model_name": annotator.model_name,
                "transform": transform,
                "condition": "in_paper",
                "model_annotations": annotations_by_lang,
            }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {transform}/{subfolder}/{fig_key} (Figure {fig_num})")
        return True, fig_key, "done"

    except Exception as e:
        logger.error(f"  FAIL {transform}/{subfolder}/{fig_key}: {e}")
        return False, fig_key, str(e)


def run(model_name="gpt-5.2", workers=4, transform_filter=None, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        adv = json.load(f)

    transforms = list(INPAPER_TRANSFORMS)
    if transform_filter:
        transforms = [t for t in transforms if t == transform_filter]
        if not transforms:
            logger.error(f"Unknown transform: {transform_filter}. Available: {INPAPER_TRANSFORMS}")
            return

    annotator = get_annotator(model_name)
    prompts = load_prompts()
    figure_numbers = _load_figure_numbers()
    excluded = _load_excluded()

    work_items = []
    skipped = 0
    for transform in transforms:
        for subfolder, fig_keys in adv["samples"].items():
            if subfolder_filter and subfolder != subfolder_filter:
                continue
            for fig_key in fig_keys:
                if fig_key in excluded:
                    skipped += 1
                    continue
                out_path = OUTPUT_DIR / annotator.model_name / transform / subfolder / f"{fig_key}.json"
                fig_path = _get_inpaper_image_path(subfolder, fig_key, transform)
                if out_path.exists():
                    skipped += 1
                elif fig_path:
                    work_items.append((transform, subfolder, fig_key))

    total = len(work_items) + skipped
    logger.info(f"In-paper transform generation | model={annotator.model_name}")
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
            ok, k, s = _process_figure(annotator, prompts, t, sub, fk, figure_numbers)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, annotator, prompts, t, sub, fk, figure_numbers): fk
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
    p = argparse.ArgumentParser(description="Generate descriptions for in-paper transformed figures")
    p.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--transform", default=None, choices=INPAPER_TRANSFORMS, help="Filter to specific transform")
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
