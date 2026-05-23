"""Generate resistance (hallucination) probes for each figure.

Uses GPT-4o to generate 3 probe types per figure:
  - inexist:       question about a non-existent element
  - contra:        statement contradicting the figure
  - unanswerable:  question that can't be answered from the figure

Reads:  dataset/groundtruth/{fig_id}.json
        dataset/figures/{fig_id}.png

Writes: dataset/resistance_probes/{fig_id}.json

Usage:
    python generate_resistance_probes.py
    python generate_resistance_probes.py --figures fig_001 fig_005
    python generate_resistance_probes.py --start 1 --end 250
"""

from __future__ import annotations

import json
import argparse
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    FIGURES_DIR, GROUNDTRUTH_DIR, DATASET_DIR,
    AZURE_API_VERSION,
    get_azure_endpoint, get_azure_api_key,
)
from models import encode_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

PROBES_DIR = DATASET_DIR / "resistance_probes"

PROMPT = """You are generating adversarial hallucination probes for a scientific chart evaluation benchmark.

Given this scientific figure and its ground-truth description, generate exactly 3 probes:

1. INEXIST probe: Ask about an element that does NOT exist in the figure. The question should sound plausible but reference a non-existent category, data series, model name, or metric. A robust model should say the element doesn't exist.

2. CONTRA probe: Make a factual claim about the figure that CONTRADICTS what is actually shown. Use specific values or relationships that are wrong. A robust model should identify the contradiction.

3. UNANSWERABLE probe: Ask a question that CANNOT be answered from the figure alone — it requires external knowledge, future data, or information not present. A robust model should say it cannot determine the answer from the figure.

GROUND-TRUTH DESCRIPTION:
{description}

FIGURE TYPE: {figure_type}
CAPTION: {caption}

RULES:
- Each probe must be 1-2 sentences
- Probes should be realistic and test genuine understanding, not trick questions
- The inexist probe should reference plausible-sounding but non-existent elements
- The contra probe should use specific wrong values, not vague claims
- The unanswerable probe should be genuinely impossible to answer from the chart

Respond with exactly this JSON:
{{
  "probes": [
    {{"type": "inexist", "question": "...", "why_wrong": "element X does not appear in the figure"}},
    {{"type": "contra", "question": "...", "why_wrong": "the actual value/relationship is Y, not Z"}},
    {{"type": "unanswerable", "question": "...", "why_wrong": "this requires information not in the figure"}}
  ]
}}"""


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

    # Get description
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
            model="gpt-4o",
            temperature=0,
            max_tokens=800,
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

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}: {len(result.get('probes', []))} probes")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=250)
    args = parser.parse_args()

    PROBES_DIR.mkdir(parents=True, exist_ok=True)

    if args.figures:
        fig_ids = args.figures
    else:
        fig_ids = [f"fig_{i:03d}" for i in range(args.start, args.end + 1)]

    done, failed = 0, 0
    for i, fig_id in enumerate(fig_ids, 1):
        if generate_probes(fig_id):
            done += 1
        else:
            failed += 1
        if i % 25 == 0:
            logger.info(f"  Progress: {i}/{len(fig_ids)} ({done} done, {failed} failed)")

    logger.info(f"Done. {done} generated, {failed} failed.")
    logger.info(f"Output: {PROBES_DIR}")


if __name__ == "__main__":
    main()
