"""Rewrite numeric inductance questions with cite-then-generate to prevent hallucination."""

import json
import sys
import argparse
from pathlib import Path
from openai import AzureOpenAI

sys.path.insert(0, str(Path(__file__).parent))
from config import *

GT_DIR = DATASET_DIR / "groundtruth"
PROBES_DIR = ADVERSARIAL_DIR / "probes"

PROMPT = """A scientific chart has a blurred element on one of its axes. The blurred text is "{blurred_value}".

GROUND-TRUTH DESCRIPTION:
{description}

STRICT RULES:
1. The description above is your ONLY source of facts. If a specific value, component name, or relationship is NOT explicitly stated in the description, you MUST NOT reference it in your question.
2. NEVER fabricate specific data values unless the description explicitly states that exact value.
3. The ANSWER to your question must be exactly "{blurred_value}".

APPROACH:
- First, extract any sentences from the description that mention "{blurred_value}" or describe elements near this value.
- Write a question that asks about a specific model, category, data point, or relationship mentioned in the description, where the answer is "{blurred_value}".
- The question should reference real element names from the description (model names, categories, metrics) — not axis positions like "the 4th tick mark."
- If the description mentions a data point at or near this value, ask about that data point.
- If the blurred value is a year, ask about what happens in that year as described.

HERE ARE EXAMPLES of good questions (notice they reference specific chart elements from descriptions, not tick positions):

Example 1: Blurred "60" on y-axis of a bar chart about model accuracy.
Description mentions: "vertical axis displays accuracy values from 0 to 80... ProLong-8b achieves approximately 60 on university"
Good question: "What is the score of ProLong-8b on the university category?"
Answer: 60

Example 2: Blurred "80%" on x-axis of a bar chart about sparsity.
Description mentions: "horizontal axis shows sparsity rates from 10% to 80%... at 80% sparsity the gap between configurations is largest"
Good question: "Which sparsity rate has the largest gap between Per-Layer and Per-Output modes?"
Answer: 80%

Example 3: Blurred "0.2" on y-axis of a bar chart about agreement.
Description mentions: "vertical axis shows Fleiss Kappa from 0.0 to 1.0... the bar at Ambiguity Std 0.94 reaches approximately 0.2"
Good question: "What is the Fleiss Kappa value at Ambiguity Std of 0.94?"
Answer: 0.2

BAD questions (avoid these):
- "What is the 4th tick mark on the vertical axis?" — too mechanical, references axis position not chart data
- "What value is between 40 and 80?" — gives away neighbors, trivially answerable

Before writing the question, provide evidence by quoting the exact sentence(s) from the description that support your question.

Respond with exactly this JSON:
{{"evidence_from_description": "exact quoted text supporting the question", "question": "the evaluation question whose answer is {blurred_value}"}}"""


def get_description(fig_id):
    gt_path = GT_DIR / f"{fig_id}.json"
    if not gt_path.exists():
        return ""
    with open(gt_path) as f:
        data = json.load(f)
    anns = data.get("annotations", [])
    eng = [a["annotation"] for a in anns if a.get("annotation_language") == "English"]
    if not eng:
        eng = [a["annotation"] for a in anns if "annotation" in a]
    return max(eng, key=len) if eng else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=10)
    parser.add_argument("--end", type=int, default=250)
    args = parser.parse_args()

    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )

    done, skipped = 0, 0
    for i in range(args.start, args.end + 1):
        fig_id = f"fig_{i:03d}"
        probe_path = PROBES_DIR / f"{fig_id}.json"
        if not probe_path.exists():
            continue

        with open(probe_path) as f:
            probe = json.load(f)

        ind = probe.get("selective_blur", {}).get("inductance", {})
        if not ind or ind.get("candidate_type") != "numeric":
            skipped += 1
            continue

        blurred = ind["blurred_text"]
        description = get_description(fig_id)
        if not description:
            skipped += 1
            continue

        prompt = PROMPT.format(blurred_value=blurred, description=description)

        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                max_tokens=400,
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}],
            )
            result = json.loads(response.choices[0].message.content)

            probe["selective_blur"]["inductance"]["question"] = result.get("question", "")
            probe["selective_blur"]["inductance"]["evidence"] = result.get("evidence_from_description", "")

            with open(probe_path, "w") as f:
                json.dump(probe, f, indent=2)

            done += 1
            if done % 25 == 0:
                print(f"  [{done}] done")

        except Exception as e:
            print(f"  {fig_id}: ERROR {str(e)[:60]}")

    print(f"Done. {done} rewritten, {skipped} skipped.")


if __name__ == "__main__":
    main()
