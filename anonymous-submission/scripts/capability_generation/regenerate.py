"""
Manual regeneration with human feedback.

Usage:
    python regenerate.py --figure fig_003 --category counting \
        --feedback "question was too easy, needs conditional threshold"

After regeneration, run validate.py and filter.py on the affected figures.
"""

from __future__ import annotations

import json
import argparse
import base64
import sys
from openai import AzureOpenAI

from config import (
    AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION,
    GENERATOR_MODEL, TEMPERATURE, MAX_TOKENS,
    GROUNDTRUTH_DIR, FIGURES_DIR, GENERATION_DIR, PROMPTS_DIR,
)


def load_system_prompt() -> str:
    return (PROMPTS_DIR / "system.txt").read_text()


def load_prompt(category: str) -> str:
    return (PROMPTS_DIR / f"{category}.txt").read_text()


def load_groundtruth(fig_id: str) -> dict:
    with open(GROUNDTRUTH_DIR / f"{fig_id}.json") as f:
        return json.load(f)


def get_description(gt: dict) -> str:
    annotations = gt.get("annotations", [])
    english = [a["annotation"] for a in annotations if a.get("annotation_language") == "English"]
    if not english:
        english = [a["annotation"] for a in annotations if "annotation" in a]
    return max(english, key=len) if english else ""


def encode_image(fig_id: str) -> str | None:
    path = FIGURES_DIR / f"{fig_id}.png"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def regenerate(client: AzureOpenAI, fig_id: str, category: str, feedback: str) -> list[dict]:
    gt = load_groundtruth(fig_id)
    description = get_description(gt)
    img_b64 = encode_image(fig_id)
    system_prompt = load_system_prompt()

    base_prompt = load_prompt(category).format(
        chart_type=gt.get("figure_type", "Unknown"),
        description=description,
    )

    feedback_block = f"""
IMPORTANT — PREVIOUS ATTEMPT FEEDBACK:
The previous questions for this figure were rejected. Here is the reviewer's feedback:
"{feedback}"

Generate 3 NEW questions that address this feedback. Do NOT repeat the same mistakes.
"""

    full_prompt = base_prompt + "\n" + feedback_block

    content_parts = []
    if img_b64:
        content_parts.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}})
    content_parts.append({"type": "text", "text": full_prompt})

    try:
        response = client.chat.completions.create(
            model=GENERATOR_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content_parts},
            ],
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        questions = data.get("questions", [])
        for q in questions:
            q["category"] = category
            q["regenerated"] = True
            q["feedback"] = feedback
        return questions
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Regenerate questions with feedback")
    parser.add_argument("--figure", required=True)
    parser.add_argument("--category", required=True,
                        choices=["counting", "computation", "comparison", "pattern_analysis"])
    parser.add_argument("--feedback", required=True)
    args = parser.parse_args()

    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT, api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )

    print(f"Regenerating {args.category} for {args.figure}")
    print(f"Feedback: {args.feedback}")
    print("-" * 60)

    questions = regenerate(client, args.figure, args.category, args.feedback)

    if not questions:
        print("No questions generated.")
        sys.exit(1)

    gen_path = GENERATION_DIR / f"{args.figure}.json"
    if gen_path.exists():
        with open(gen_path) as f:
            data = json.load(f)
    else:
        data = {"figure_id": args.figure, "candidates": {}}

    data["candidates"][args.category] = questions
    data["total_candidates"] = sum(len(qs) for qs in data["candidates"].values())

    with open(gen_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n{len(questions)} new questions generated:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q['question'][:100]}")

    print(f"\nNext steps:")
    print(f"  python validate.py --figures {args.figure}")
    print(f"  python filter.py")


if __name__ == "__main__":
    main()
