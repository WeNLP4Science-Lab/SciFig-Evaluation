"""MQM evaluation of model descriptions using chart-type-specific checklists.

The judge assesses each checklist item on two axes (coverage + correctness)
and scans for global constraint violations. A rule-based engine then maps
the judge output to MQM penalties using the PDF weight table.

Usage:
    python evaluate_mqm.py gpt-5.2 --workers 4
    python evaluate_mqm.py phi-5 --figures fig_001 fig_005
    python evaluate_mqm.py --all-models --workers 4
"""

from __future__ import annotations

import json
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    MODELS, FIGURES_DIR, GROUNDTRUTH_DIR, RESULTS_DIR,
    AZURE_API_VERSION,
    get_azure_endpoint, get_azure_api_key,
)
from models import encode_image
from checklists import (
    get_checklist, get_global_constraints, get_bindings,
    compute_penalties, deduplicate_penalties, compute_mqm,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

DESCRIPTIONS_DIR = RESULTS_DIR / "generation" / "description_tasks" / "baseline_descriptions"
MQM_DIR = RESULTS_DIR / "evaluation" / "description_tasks" / "baseline_descriptions"

JUDGE_MODEL = "gpt-4o"

# ── System prompt: rules in privileged position ──

SYSTEM_PROMPT = """You are an expert evaluator for scientific chart descriptions.

<VERIFICATION_PROCEDURE>
1. FIRST compare the model description against the REFERENCE description to find discrepancies.
   Read both texts carefully — check what the model actually says, not what you expect it to say.
2. For any discrepancy found, verify against the IMAGE to confirm whether the model is truly wrong.
   If the image confirms the reference is correct and the model is wrong → flag as error.
   If the image shows the model has a valid alternative reading → do NOT flag as error.
   If the image is ambiguous → defer to the reference.
</VERIFICATION_PROCEDURE>

<CRITICAL_RULES>
COLOUR DECISION PROCEDURE (apply BEFORE any colour-related assessment):
1. Map BOTH the model's colour term AND the image colour to one of these 11 basic families:
   red (crimson, scarlet, maroon, dark red, wine, burgundy, rose)
   orange (amber, rust, burnt orange)
   yellow (gold, golden, mustard, lemon)
   green (lime, dark green, olive, forest green, emerald, teal)
   blue (light blue, dark blue, navy, cyan, sky blue, azure, cobalt, turquoise, steel blue)
   purple (violet, indigo, magenta, lavender, lilac, plum, mauve)
   pink (hot pink, salmon, coral, fuchsia, rosa)
   brown (tan, beige, chocolate, coffee, khaki)
   gray (grey, silver, charcoal, slate, light grey, dark grey)
   black
   white (cream, ivory, off-white)
2. SAME family = NOT an error. DIFFERENT family = error.
3. State the family mapping in your reasoning.

NUMERICAL TOLERANCE:
- Percentages: accept within +/-3 percentage points
- Axis ranges/tick values: accept within +/-10% of stated value
- Values marked "approximately"/"roughly"/"about"/"~": accept any reasonable image reading
- Two equally valid approximations: NOT an error

WORDING TOLERANCE:
- Accept semantic equivalence: "increases"/"rises"/"grows", "x-axis"/"horizontal axis"
- Accept different valid specificity: "the blue line" vs "the line representing Method A"
</CRITICAL_RULES>

<ACCURACY_SUB_TYPES>
When correctness is "partial" or "wrong", specify one of these sub_types:
- "Incorrect Numerical Value": wrong numbers, percentages, or quantities
- "Incorrect Trend Interpretation": wrong pattern or direction of change
- "Incorrect Axis or Legend Interpretation": wrong axis labels, units, or legend info
- "Incorrect Label Mapping": wrong category names or values assigned to visual elements
</ACCURACY_SUB_TYPES>"""

# ── User prompt template ──

USER_PROMPT = """Evaluate this model-generated chart description against the image and reference.

<CHART_TYPE>{figure_type}</CHART_TYPE>

<CHECKLIST>
{checklist_text}
</CHECKLIST>

<GLOBAL_CONSTRAINTS>
{constraints_text}
</GLOBAL_CONSTRAINTS>


<REFERENCE>
{groundtruth}
</REFERENCE>

<MODEL_OUTPUT>
{description}
</MODEL_OUTPUT>

<TASK>
Evaluate in four steps:

STEP 0 — POPULATE CHECKLIST FROM REFERENCE:
Read the REFERENCE description carefully. For each checklist item, extract the expected
answer — the concrete facts from the reference that this item should match.
For element-based items (values, colours, labels), list each element with its expected value.
For example:
  pie_06 (values): Frustration=25.1%, Neutral=23.1%, Happiness=8.1%, Excitement=14.1%, ...
  pie_05 (colours): Frustration=light blue, Neutral=dark blue, Happiness=blue, Excitement=red, ...
  pie_11 (largest/smallest): largest=Frustration, smallest=Happiness
For non-element items, state the expected fact:
  pie_01 (chart type): pie chart
  pie_03 (slice count): 6

STEP 1 — SCORE MODEL AGAINST POPULATED CHECKLIST:
For each checklist item, compare the MODEL description against the expected answer from Step 0.

1. COVERAGE — Is this item addressed in the model description?
   "complete": fully addressed
   "partial": partially addressed, some aspects missing
   "missing": not addressed at all
   Include "detail" explaining what is missing if partial or missing.

2. CORRECTNESS — Does what the model states match the expected answer from Step 0?
   "correct": matches (within tolerance rules)
   "partial": some aspects match, some don't
   "wrong": completely incorrect
   "n/a": only if coverage is "missing"
   If "partial" or "wrong", include:
     - "sub_type": one of the 4 accuracy sub-types
     - "text_span": exact quote from the model description containing the error
     - "detail": brief explanation of what is wrong
   For colour items: apply the colour family mapping before deciding.

STEP 2 — BINDING VERIFICATION (for element-based items only):
{binding_instructions}

STEP 3 — IMAGE VERIFICATION:
For any discrepancy found in Steps 1 or 2, verify against the IMAGE:
  - If the image confirms the reference is correct and the model is wrong → keep the error
  - If the image shows the model has a valid alternative reading → remove the error
  - If the image is ambiguous → defer to the reference

STEP 4 — GLOBAL CONSTRAINTS:
Scan the FULL model description for violations of each constraint.
Each violation needs "text_span" (exact quote) and "explanation".
If no violations for a constraint, return empty violations list.

IMPORTANT: Do NOT flag as a global violation anything already penalised under
a checklist item. Global constraints only capture errors OUTSIDE the checklist.

Return this JSON:
{{
  "populated": {{
    "pie_06": {{"expected": {{"Frustration": "25.1%", "Happiness": "8.1%", "Excitement": "14.1%"}}}},
    "pie_05": {{"expected": {{"Frustration": "light blue", "Happiness": "blue", "Excitement": "red"}}}},
    "pie_11": {{"expected": {{"largest": "Frustration", "smallest": "Happiness"}}}},
    "pie_01": {{"expected": "pie chart"}},
    "pie_03": {{"expected": "6 slices"}}
  }},
  "checklist": [
    {{
      "id": "item_id",
      "reasoning": "Expected from reference: X. Model says: Y. Match/mismatch. Image confirms.",
      "coverage": {{
        "status": "complete"
      }},
      "correctness": {{
        "status": "correct"
      }}
    }},
    {{
      "id": "item_id",
      "reasoning": "Model mentions this but some parts are missing and one value is wrong.",
      "coverage": {{
        "status": "partial",
        "detail": "Units not mentioned"
      }},
      "correctness": {{
        "status": "wrong",
        "sub_type": "Incorrect Numerical Value",
        "text_span": "with a value of approximately 60%",
        "detail": "Says 60% but image shows 45%"
      }}
    }},
    {{
      "id": "item_id",
      "reasoning": "Not addressed anywhere in the description.",
      "coverage": {{
        "status": "missing",
        "detail": "Error bars visible in image but not mentioned"
      }},
      "correctness": {{
        "status": "n/a"
      }}
    }}
  ],
  "global": [
    {{
      "id": "global_hallucination",
      "violations": [
        {{"text_span": "exact quote", "explanation": "why this is fabricated"}}
      ]
    }},
    {{"id": "global_interpretation", "violations": []}},
    {{"id": "global_ambiguity", "violations": []}},
    {{"id": "global_overgeneralization", "violations": []}},
    {{"id": "global_verbose", "violations": []}},
    {{"id": "global_poor_structure", "violations": []}},
    {{"id": "global_missing_takeaway", "violations": []}}
  ],
  "bindings": [
    {{
      "checklist_id": "pie_06",
      "comparisons": [
        {{"label": "Frustration", "reference_value": "25.1%", "model_value": "25.1%", "match": true}},
        {{"label": "Happiness", "reference_value": "8.1%", "model_value": "14.1%", "match": false}},
        {{"label": "Excitement", "reference_value": "14.1%", "model_value": "8.1%", "match": false}}
      ]
    }},
    {{
      "checklist_id": "pie_05",
      "comparisons": [
        {{"label": "Frustration", "reference_value": "light blue", "model_value": "light blue", "match": true}},
        {{"label": "Happiness", "reference_value": "blue", "model_value": "light purple", "match": false}}
      ]
    }}
  ]
}}
</TASK>"""


def _format_checklist(checklist: list[dict]) -> str:
    lines = []
    for item in checklist:
        lines.append(f"[{item['id']}] {item['item']}")
    return "\n".join(lines)


def _format_constraints(constraints: list[dict]) -> str:
    lines = []
    for c in constraints:
        lines.append(f"[{c['id']}] {c['constraint']}")
    return "\n".join(lines)


def _format_bindings(bindings: list[dict]) -> str:
    if not bindings:
        return "No binding verification needed for this chart type."
    lines = ["For each binding below, extract per-element values from BOTH the reference and the model description, match by label, and compare:"]
    for b in bindings:
        lines.append(f"")
        lines.append(f"[{b['checklist_id']}] {b['attribute']} binding:")
        lines.append(f"  {b['instruction']}")
        lines.append(f"  Report each element as: label, reference_value, model_value, match (true/false)")
        lines.append(f"  Apply tolerance rules (numerical tolerance, colour family mapping) before deciding match.")
    return "\n".join(lines)




def evaluate_figure(model_name: str, fig_id: str) -> tuple[bool, str]:
    out_dir = MQM_DIR / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    desc_path = DESCRIPTIONS_DIR / model_name / f"{fig_id}.json"
    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not desc_path.exists() or not gt_path.exists() or not fig_path.exists():
        return False, "missing"

    with open(desc_path) as f:
        desc_data = json.load(f)
    with open(gt_path) as f:
        gt_data = json.load(f)

    description = desc_data.get("description", "")
    figure_type = gt_data.get("figure_type", "Bar Chart")

    # Get ground-truth human annotation
    anns = gt_data.get("annotations", [])
    eng = [a["annotation"] for a in anns if a.get("annotation_language") == "English"]
    if not eng:
        eng = [a["annotation"] for a in anns if "annotation" in a]
    groundtruth = max(eng, key=len) if eng else ""

    if not description or not groundtruth:
        return False, "empty"

    checklist = get_checklist(figure_type)
    constraints = get_global_constraints()
    bindings = get_bindings(figure_type)

    user_prompt = USER_PROMPT.format(
        figure_type=figure_type,
        checklist_text=_format_checklist(checklist),
        constraints_text=_format_constraints(constraints),
        binding_instructions=_format_bindings(bindings),
        groundtruth=groundtruth,
        description=description,
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
            model=JUDGE_MODEL,
            temperature=0,
            max_tokens=4000,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
                    {"type": "text", "text": user_prompt},
                ]},
            ],
        )
        judge_output = json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    # Rule-based engine: map judge output to penalties
    penalties = compute_penalties(judge_output, checklist)
    mqm_raw = compute_mqm(penalties, checklist)

    # Deduplicated score (removes double-counting)
    deduped = deduplicate_penalties(penalties)
    mqm_deduped = compute_mqm(deduped, checklist)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "figure_type": figure_type,
        "judge_model": JUDGE_MODEL,
        "num_items": len(checklist),
        "num_penalties_raw": len(penalties),
        "num_penalties_deduped": len(deduped),
        "total_penalty_raw": sum(p["weight"] for p in penalties),
        "total_penalty_deduped": sum(p["weight"] for p in deduped),
        "mqm_raw": round(mqm_raw, 2),
        "mqm_deduped": round(mqm_deduped, 2),
        "penalties_raw": penalties,
        "penalties_deduped": deduped,
        "judge_output": judge_output,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}: MQM_raw={mqm_raw:.1f} MQM_dedup={mqm_deduped:.1f} ({len(penalties)}→{len(deduped)} penalties)")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", nargs="?", help="Model name")
    parser.add_argument("--all-models", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.all_models:
        model_names = sorted(MODELS.keys())
    elif args.model:
        model_names = [args.model]
    else:
        print("Specify a model name or --all-models")
        return

    for model_name in model_names:
        desc_dir = DESCRIPTIONS_DIR / model_name
        if not desc_dir.exists():
            logger.info(f"{model_name}: no descriptions found, skipping")
            continue

        fig_ids = args.figures or sorted(p.stem for p in desc_dir.glob("*.json"))

        work, skipped = [], 0
        for fid in fig_ids:
            if (MQM_DIR / model_name / f"{fid}.json").exists():
                skipped += 1
            else:
                work.append(fid)

        logger.info(f"MQM evaluation | model={model_name}")
        logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to evaluate)")

        if not work:
            logger.info("Nothing to do.")
            continue

        success, errors = 0, 0
        lock = threading.Lock()

        if args.workers == 1:
            for fid in work:
                ok, s = evaluate_figure(model_name, fid)
                if ok: success += 1
                else: errors += 1
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = {ex.submit(evaluate_figure, model_name, fid): fid for fid in work}
                for f in as_completed(futs):
                    ok, s = f.result()
                    with lock:
                        if ok: success += 1
                        else: errors += 1

        logger.info(f"  {model_name}: {success} ok, {errors} errors, {skipped} skipped.")

    logger.info("All done.")


if __name__ == "__main__":
    main()
