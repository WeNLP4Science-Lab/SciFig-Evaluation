"""Generate resistance probes using Mistral Large 3 (ablation study).

Same prompt as generate_resistance_probes.py but uses Mistral Large 3
instead of GPT-4o to test whether the probe generator model affects
resistance scores.

Output: dataset/resistance_probes_mistral/{fig_id}.json

Usage:
    python generate_resistance_probes_ablation.py --sample50
    python generate_resistance_probes_ablation.py --figures fig_002 fig_009
"""

from __future__ import annotations

import json
import argparse
import logging
import random
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    FIGURES_DIR, GROUNDTRUTH_DIR, DATASET_DIR,
    AZURE_API_VERSION,
    get_azure_endpoint, get_azure_api_key,
)
from models import encode_image

# Reuse the same prompt from generate_resistance_probes.py
from generate_resistance_probes import PROMPT

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

PROBES_DIR = DATASET_DIR / "resistance_probes_mistral"
MISTRAL_MODEL = "mistral-large-3"


def generate_probes(fig_id: str) -> bool:
    out_path = PROBES_DIR / f"{fig_id}.json"
    if out_path.exists():
        return True

    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not gt_path.exists() or not fig_path.exists():
        return False

    with open(gt_path) as f:
        gt = json.load(f)

    anns = gt.get("annotations", [])
    eng = [a["annotation"] for a in anns if a.get("annotation_language") == "English"]
    if not eng:
        eng = [a["annotation"] for a in anns if "annotation" in a]
    description = max(eng, key=len) if eng else ""

    if not description:
        logger.warning(f"  {fig_id}: no description, skipping")
        return False

    prompt = PROMPT.format(
        description=description,
        figure_type=gt.get("figure_type", ""),
        caption=gt.get("caption", ""),
    )

    from openai import AzureOpenAI
    client = AzureOpenAI(
        azure_endpoint=get_azure_endpoint(),
        api_key=get_azure_api_key(),
        api_version=AZURE_API_VERSION,
    )

    b64 = encode_image(fig_path)

    try:
        response = client.chat.completions.create(
            model=MISTRAL_MODEL,
            temperature=0,
            max_tokens=1500,
            response_format={"type": "json_object"},
            messages=[
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
                    {"type": "text", "text": prompt},
                ]},
            ],
        )
        result = json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"  {fig_id}: ERROR {str(e)[:60]}")
        return False

    result["figure_id"] = fig_id
    result["figure_type"] = gt.get("figure_type", "")
    result["probe_generator"] = MISTRAL_MODEL

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    types = [p["type"] for p in result.get("probes", [])]
    logger.info(f"  OK {fig_id}: {types}")
    return True


def sample_50(seed=42):
    """Stratified random sample of 50 from the sampled 100."""
    with open(DATASET_DIR / "sampled_100.json") as f:
        fig_ids = json.load(f)["figures"]

    # Group by figure type
    by_type = {}
    for fig_id in fig_ids:
        gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
        if gt_path.exists():
            with open(gt_path) as f:
                gt = json.load(f)
            ft = gt.get("figure_type", "Other")
            by_type.setdefault(ft, []).append(fig_id)

    # Sample 50% from each type (20 bar, 20 line, 10 pie)
    rng = random.Random(seed)
    sampled = []
    for ft, figs in sorted(by_type.items()):
        n = len(figs) // 2
        sampled.extend(rng.sample(figs, n))

    return sorted(sampled)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--sample50", action="store_true")
    args = parser.parse_args()

    PROBES_DIR.mkdir(parents=True, exist_ok=True)

    if args.figures:
        fig_ids = args.figures
    elif args.sample50:
        fig_ids = sample_50()
        logger.info(f"Sampled 50 figures (20 bar, 20 line, 10 pie)")
    else:
        print("Specify --figures or --sample50")
        return

    done, failed = 0, 0
    for i, fig_id in enumerate(fig_ids, 1):
        if generate_probes(fig_id):
            done += 1
        else:
            failed += 1
        if i % 10 == 0:
            logger.info(f"  Progress: {i}/{len(fig_ids)} ({done} done, {failed} failed)")

    logger.info(f"Done. {done} generated, {failed} failed.")
    logger.info(f"Output: {PROBES_DIR}")


if __name__ == "__main__":
    main()
