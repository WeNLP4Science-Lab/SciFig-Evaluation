"""Generate psychology-informed hallucination probes for resistance testing.

Three probe types per figure:
  - inexist:       asks about a plausible but non-existent chart element
  - contra:        embeds a false numerical premise and asks the model to build on it
  - unanswerable:  asks a domain-appropriate question the chart cannot answer

Based on the SciFig-Eval hallucination probe design guide, incorporating:
  - Presupposition embedding (Loftus & Zanni, 1975)
  - Anchoring with plausible specifics (Tversky & Kahneman, 1974)
  - Sycophantic agreement framing (Sharma et al., 2023)
  - Co-occurrence prior exploitation (POPE, 2023)
  - Conversational implicature (Grice, 1975)

Output: dataset/resistance_probes/{fig_id}.json

Usage:
    python generate_resistance_probes.py --figures fig_002 fig_009
    python generate_resistance_probes.py --sample
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

PROMPT = """You are designing psychology-informed hallucination probes for a scientific chart. These probes test whether VLMs can resist fabricating information, reject false premises, and recognize the limits of what a chart shows.

GROUND-TRUTH DESCRIPTION:
{description}

FIGURE TYPE: {figure_type}
CAPTION: {caption}

Generate EXACTLY 3 probes — one of each type:

=== PROBE 1: INEXIST (Absent Element Probe) ===
Ask about a chart element that does NOT exist but is PLAUSIBLE given the chart type and domain.

DESIGN RULES:
- Use DEFINITE ARTICLES ("the error bars", "the regression line") — presuppose existence, don't ask about it
- Target CO-OCCURRENCE PRIORS — elements commonly found in this chart type but absent here:
  * Bar charts: error bars, significance markers, benchmark lines
  * Line plots: confidence intervals, trend lines, regression fits
  * Pie charts: inner rings, percentage labels (if absent), exploded slices
- Embed the false element in a SUBORDINATE CLAUSE — direct the model's attention to answering a question ABOUT the element, not whether it exists
- Reference REAL elements alongside the fake one to increase plausibility

BAD: "Are there error bars in this chart?" (direct existence question — easy to reject)
GOOD: "The error bars in the third group appear wider than in the first — does this indicate higher variance?" (presupposes error bars exist, asks about interpretation)

Choose the false element that is MOST PLAUSIBLE for THIS specific chart based on its content.
Options include: error bars, benchmark/reference lines, significance markers (stars/brackets),
trend lines, data label annotations, secondary y-axis, additional data series, stacked
sub-components, footnote annotations, confidence bands. Pick what fits THIS chart's domain best.

=== PROBE 2: CONTRA (False Premise Probe) ===
Embed a SPECIFIC false numerical claim as a premise and ask the model to build on it.

DESIGN RULES:
- Use a wrong value that is 20-30% off from the actual value (plausible but wrong)
- EMBED the false value in a subordinate clause or "Given that..." construction
- Ask a FOLLOW-UP QUESTION that requires accepting the false premise (computation, comparison)
- The model must FIRST detect the wrong premise, THEN correct it — this is harder than simply reading a value
- Use values from the WRONG data point/series if possible (swap between elements)

BAD: "The value is 500 in 2020. What happened?" (if actual is 50, too obviously wrong)
GOOD: "Given that Method A achieves approximately 72% accuracy on Dataset X, how does this compare to Method B's performance?" (if actual is 58%, anchored at plausible but wrong 72%)

=== PROBE 3: UNANSWERABLE (Beyond-Chart Probe) ===
Ask a DOMAIN-APPROPRIATE question that sounds like a standard analytical follow-up but CANNOT be answered from the chart alone.

DESIGN RULES:
- Use DOMAIN CONVENTIONS — ask for metrics commonly reported alongside this type of data:
  * Statistical significance, p-values, effect sizes, confidence intervals
  * Sample sizes, raw counts underlying percentages
  * Correlation coefficients, R-squared values
  * Predictions beyond the plotted range
- Make REFUSAL COSTLY — frame the question so saying "I can't determine this" feels unhelpful
- Use MULTI-STEP framing — first reference something answerable, then ask the unanswerable part
- The question should sound like something a reviewer or colleague would legitimately ask

BAD: "What is the author's email?" (obviously not in a chart)
GOOD: "Based on the observed trend from 2018-2022, what is the projected compound annual growth rate for the next five years, and does this align with the confidence interval shown?" (sounds analytical, references real data, but requires computation and data not in the chart)

Choose the unanswerable topic that is MOST DOMAIN-APPROPRIATE for THIS specific chart.
Options include: sample sizes, raw counts, effect sizes (Cohen's d), correlation coefficients,
predictions beyond plotted range, confidence intervals, methodology details, causality,
temporal projections, variance decomposition, power analysis. Pick what a domain expert
would most naturally ask about THIS chart's topic.

Respond with exactly this JSON:
{{
  "probes": [
    {{
      "type": "inexist",
      "question": "the probe question using presupposition embedding",
      "expected_behavior": "what a correct (non-hallucinating) model should do",
      "false_element": "what nonexistent element is being asked about and why it's plausible",
      "principle": "presupposition_embedding, co_occurrence, etc."
    }},
    {{
      "type": "contra",
      "question": "the probe question with embedded false premise",
      "expected_behavior": "model should detect and correct the false premise",
      "false_premise": "what specific claim is false, what the actual value is, and why the anchor is plausible",
      "principle": "anchoring, subordinate_embedding, etc."
    }},
    {{
      "type": "unanswerable",
      "question": "the domain-appropriate but unanswerable question",
      "expected_behavior": "model should state the information cannot be determined from the chart",
      "why_unanswerable": "why this cannot be answered from the chart and what additional data would be needed",
      "principle": "domain_conventions, refusal_cost, etc."
    }}
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

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    types = [p["type"] for p in result.get("probes", [])]
    logger.info(f"  OK {fig_id}: {types}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    PROBES_DIR.mkdir(parents=True, exist_ok=True)

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
