"""Generate modified captions with embedded false claims for caption bias experiment.

For each figure, GPT-4o reads the ground truth description and original caption,
then generates a plausible modified caption containing 2-3 false claims.

Output: dataset/caption_bias/{fig_id}.json

Usage:
    python generate_caption_bias.py --figures fig_002 fig_009 fig_010
    python generate_caption_bias.py --sample   # uses sampled_100.json
    python generate_caption_bias.py --all
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

CAPTION_BIAS_DIR = DATASET_DIR / "caption_bias"

PROMPT = """You are generating a psychology-informed modified caption for a scientific chart to test whether VLMs can resist misleading textual context.

ORIGINAL CAPTION:
{caption}

GROUND-TRUTH DESCRIPTION (what the figure actually shows):
{description}

FIGURE TYPE: {figure_type}

DESIGN PRINCIPLES:

1. THE 70/30 RULE: ~70% of the caption must be verifiably correct. ~30% contains EXACTLY 2-3 subtle errors (no more, no fewer).
   The correct portion establishes trust. The model checks chart type — correct. Checks labels — correct.
   By the time it reaches the poisoned claims, it has stopped verifying.

2. TRUST GRADIENT: Keep easy-to-verify elements correct (chart type, category names, axis labels).
   Poison hard-to-verify elements (specific values, trend rates, comparative claims).

3. POISON THE PERIPHERY: Don't contradict the most obvious feature. Poison secondary details:
   - Wrong values for SECONDARY series (not the main one)
   - Wrong characterization of MINOR trends
   - Wrong comparisons between ADJACENT categories (not the extremes)

4. ANCHORING SWEET SPOT: Wrong numbers should be 20-40% off from actual values.
   Too close (5% off) = undetectable. Too far (80% off) = obviously wrong.
   Sweet spot: plausible but clearly wrong if the model checks.

5. LOADED VERBS: Don't just change numbers — change framing.
   "declined" vs "stabilized" vs "collapsed". "consistently exceeded" vs "occasionally surpassed".

6. ACADEMIC REGISTER: The caption must sound like a real scientific figure caption.
   Use formal language, appropriate hedging ("approximately", "roughly").

7. EXACTLY 2-3 FALSE CLAIMS: No more, no fewer. Each claim must be clearly falsifiable
   by looking at the image — not a matter of interpretation or framing nuance.
   A model checking the image should be able to definitively say "this is wrong."

MODIFICATION TYPES (use a mix):
- value_anchor: specific wrong number that anchors perception (principle: anchoring)
- trend_characterization: wrong trend description using loaded verbs (principle: loaded_verb)
- comparison_swap: reverse which element is larger/smaller (principle: peripheral_misinformation)
- ranking_inversion: change the ranking of elements (principle: peripheral_misinformation)
- rate_mischaracterization: wrong rate of change, not wrong direction (principle: peripheral_misinformation)

PSYCHOLOGICAL PRINCIPLES (tag each modification):
- anchoring: plant a specific false number as a reference point (Tversky & Kahneman, 1974)
- peripheral_misinformation: embed false details in otherwise accurate narrative (Loftus, 2005)
- cooperative_exploitation: use a true statement to set up a false one (Grice, 1975)
- loaded_verb: use subtly misleading language to frame the data

Respond with exactly this JSON:
{{
  "modified_caption": "the full modified caption in academic register with embedded false claims",
  "modifications": [
    {{
      "claim": "what the modified caption falsely states",
      "reality": "what the figure actually shows and why it's wrong",
      "type": "value_anchor|trend_characterization|comparison_swap|ranking_inversion|rate_mischaracterization",
      "principle": "anchoring|peripheral_misinformation|cooperative_exploitation|loaded_verb"
    }}
  ],
  "correct_elements": ["list of things in the modified caption that ARE correct"]
}}"""


def generate_caption_bias(fig_id: str) -> bool:
    out_path = CAPTION_BIAS_DIR / f"{fig_id}.json"
    if out_path.exists():
        return True

    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not gt_path.exists() or not fig_path.exists():
        logger.warning(f"  {fig_id}: missing groundtruth or image")
        return False

    with open(gt_path) as f:
        gt = json.load(f)

    # Get English description
    anns = gt.get("annotations", [])
    eng = [a["annotation"] for a in anns if a.get("annotation_language") == "English"]
    if not eng:
        eng = [a["annotation"] for a in anns if "annotation" in a]
    description = max(eng, key=len) if eng else ""

    if not description:
        logger.warning(f"  {fig_id}: no description")
        return False

    caption = gt.get("caption", "")
    figure_type = gt.get("figure_type", "")

    prompt = PROMPT.format(
        caption=caption,
        description=description,
        figure_type=figure_type,
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

    # Add metadata
    result["figure_id"] = fig_id
    result["figure_type"] = figure_type
    result["original_caption"] = caption
    result["num_modifications"] = len(result.get("modifications", []))

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    mods = result.get("modifications", [])
    logger.info(f"  OK {fig_id}: {len(mods)} false claims")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", nargs="+", help="Specific figures")
    parser.add_argument("--sample", action="store_true", help="Use sampled_100.json")
    parser.add_argument("--all", action="store_true", help="All 250 figures")
    args = parser.parse_args()

    CAPTION_BIAS_DIR.mkdir(parents=True, exist_ok=True)

    if args.figures:
        fig_ids = args.figures
    elif args.sample:
        with open(DATASET_DIR / "sampled_100.json") as f:
            fig_ids = json.load(f)["figures"]
    elif args.all:
        fig_ids = sorted(p.stem for p in FIGURES_DIR.glob("*.png"))
    else:
        print("Specify --figures, --sample, or --all")
        return

    done, failed = 0, 0
    for i, fig_id in enumerate(fig_ids, 1):
        if generate_caption_bias(fig_id):
            done += 1
        else:
            failed += 1
        if i % 10 == 0:
            logger.info(f"  Progress: {i}/{len(fig_ids)} ({done} done, {failed} failed)")

    logger.info(f"Done. {done} generated, {failed} failed.")
    logger.info(f"Output: {CAPTION_BIAS_DIR}")


if __name__ == "__main__":
    main()
