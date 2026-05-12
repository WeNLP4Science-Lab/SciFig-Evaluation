"""Generate figure descriptions for adversarial-transformed images.

Runs a generator model on transformed versions of selected figures.
Uses Azure OpenAI for GPT models.

Output: output/generation_adversarial/<model>/<transform>/<subfolder>/<fig_key>.json

Usage:
    python3 scripts/llm_generation/run_adversarial.py --model gpt-5.2 --workers 4
    python3 scripts/llm_generation/run_adversarial.py --model gpt-5.2 --transform jpeg_compression
"""

import argparse
import base64
import json
import logging
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT / "scripts"))
from llm_generation.prompts import load_prompts, get_prompt

TRANSFORMS_DIR = ROOT / "transforms"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
OUTPUT_DIR = ROOT / "output" / "generation_adversarial"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_azure_client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-12-01-preview",
    )


def _encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _retry(func, max_retries=3, backoff=2.0):
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= backoff


# Azure deployment name mapping
AZURE_DEPLOYMENTS = {
    "gpt-5.2": "gpt-5-2",
    "gpt-4o": "gpt-4o",
    "gpt-5.4-mini": "gpt-5.4-mini",
}


def generate_description(client, deployment_name, prompt, image_path, caption, paper_title=""):
    """Generate a figure description using Azure OpenAI."""
    b64 = _encode_image(image_path)
    user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

    user_content = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
        {"type": "text", "text": user_text},
    ]

    # Newer models use max_completion_tokens
    token_param = "max_completion_tokens" if any(v in deployment_name for v in ["gpt-5", "gpt-4.1"]) else "max_tokens"

    def _call():
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_content},
            ],
            **{token_param: 2048},
        )
        return response.choices[0].message.content.strip()

    return _retry(_call)


def _process_figure(client, deployment_name, prompts, transform, subfolder, fig_key, model_name):
    """Process a single transformed figure."""
    fig_path = TRANSFORMS_DIR / transform / "figures" / subfolder / f"{fig_key}.png"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / model_name / transform / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"
    if not fig_path.exists() or not gt_path.exists():
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
            prompt_text = get_prompt(prompts, languages[0], figure_type)
            description = generate_description(client, deployment_name, prompt_text, fig_path, gt["caption"], gt.get("paper_title", ""))

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_title": gt.get("paper_title", ""),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "caption": gt["caption"],
                "model_name": model_name,
                "transform": transform,
                "model_annotation": description,
            }
        else:
            annotations_by_lang = {}
            for lang in languages:
                prompt_text = get_prompt(prompts, lang, figure_type)
                desc = generate_description(client, deployment_name, prompt_text, fig_path, gt["caption"], gt.get("paper_title", ""))
                annotations_by_lang[lang] = desc

            result = {
                "figure_key": fig_key,
                "task_id": gt["task_id"],
                "arxiv_id": gt.get("arxiv_id"),
                "paper_title": gt.get("paper_title", ""),
                "paper_language": gt["paper_language"],
                "figure_type": figure_type,
                "caption": gt["caption"],
                "model_name": model_name,
                "transform": transform,
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


def run(model_name="gpt-5.2", workers=4, transform_filter=None, max_figures=None):
    # Load adversarial samples
    with open(ROOT / "adversarial_samples.json") as f:
        adv = json.load(f)

    transforms = adv["transforms"]
    if transform_filter:
        transforms = [t for t in transforms if t == transform_filter]

    deployment_name = AZURE_DEPLOYMENTS.get(model_name, model_name)
    client = _get_azure_client()
    prompts = load_prompts()

    # Build work items
    work_items = []
    skipped = 0
    for transform in transforms:
        for subfolder, fig_keys in adv["samples"].items():
            keys = fig_keys[:max_figures] if max_figures else fig_keys
            for fig_key in keys:
                out_path = OUTPUT_DIR / model_name / transform / subfolder / f"{fig_key}.json"
                fig_path = TRANSFORMS_DIR / transform / "figures" / subfolder / f"{fig_key}.png"
                if out_path.exists():
                    skipped += 1
                elif fig_path.exists():
                    work_items.append((transform, subfolder, fig_key))

    logger.info(f"Adversarial generation | model={model_name} | deployment={deployment_name}")
    logger.info(f"Transforms: {transforms}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to generate)")

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
            ok, k, s = _process_figure(client, deployment_name, prompts, t, sub, fk, model_name)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, client, deployment_name, prompts, t, sub, fk, model_name): fk
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

    logger.info(f"Done. {success}/{len(work_items) + skipped} generated, {errors} failures.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate descriptions for adversarial-transformed figures")
    p.add_argument("--model", default="gpt-5.2", help="Model name")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--transform", default=None, help="Filter to specific transform")
    p.add_argument("--max-figures", type=int, default=None, help="Limit figures per subfolder (for testing)")
    a = p.parse_args()
    run(a.model, a.workers, a.transform, a.max_figures)
