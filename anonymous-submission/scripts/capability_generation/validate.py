"""
Stage 2: Validate candidate questions using Mistral Large 3.

Sends all 3 questions per category in ONE call (image + 3 questions).
4 calls per figure instead of 12.

Reads from:  results/capability_generation/generation/
Writes to:   results/capability_generation/validation/

Usage:
    python validate.py --limit 50
    python validate.py --workers 4
    python validate.py --figures fig_001
"""

from __future__ import annotations

import json
import argparse
import base64
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import AzureOpenAI, OpenAI

from config import (
    AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION,
    OPENROUTER_API_KEY, VALIDATOR_MODEL, VALIDATOR_BACKEND, TEMPERATURE,
    GENERATION_DIR, VALIDATION_DIR, FIGURES_DIR, PROMPTS_DIR,
)


def get_validator_client():
    if VALIDATOR_BACKEND == "openrouter":
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            timeout=120,
        )
    return AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT, api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION, timeout=180,
    )


def load_validate_prompt() -> str:
    return (PROMPTS_DIR / "validate.txt").read_text()


def encode_image(fig_id: str) -> str | None:
    path = FIGURES_DIR / f"{fig_id}.png"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def validate_category(client: AzureOpenAI, prompt_template: str,
                      img_b64: str, category: str, questions: list[dict]) -> list[dict]:
    """Validate all 3 questions for one category in a single API call."""
    q_texts = [q.get("question", "") for q in questions]
    # Pad to 3 if fewer
    while len(q_texts) < 3:
        q_texts.append("N/A")

    prompt = prompt_template.format(
        category=category,
        q1=q_texts[0],
        q2=q_texts[1],
        q3=q_texts[2],
    )

    try:
        response = client.chat.completions.create(
            model=VALIDATOR_MODEL,
            temperature=TEMPERATURE,
            max_tokens=2048,
            response_format={"type": "json_object"},
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        content = response.choices[0].message.content
        scores = json.loads(content)

        # Attach scores to each question
        result = []
        for i, q in enumerate(questions):
            key = f"question_{i+1}"
            score = scores.get(key, {"overall": "ERROR"})
            result.append({**q, "validation": score})
        return result

    except Exception as e:
        print(f"      ERROR: {e}", file=sys.stderr)
        return [{**q, "validation": {"error": str(e), "overall": "ERROR"}} for q in questions]


def validate_figure(client: AzureOpenAI, prompt_template: str, fig_id: str) -> dict | None:
    src = GENERATION_DIR / f"{fig_id}.json"
    if not src.exists():
        return None

    with open(src) as f:
        data = json.load(f)

    img_b64 = encode_image(fig_id)
    if not img_b64:
        return None

    result = {
        "figure_id": fig_id,
        "figure_type": data.get("figure_type", ""),
        "generator_model": data.get("generator_model", ""),
        "validator_model": VALIDATOR_MODEL,
        "categories": {},
    }

    accepted_total, rejected_total = 0, 0

    for cat, questions in data.get("candidates", {}).items():
        validated = validate_category(client, prompt_template, img_b64, cat, questions)
        result["categories"][cat] = validated
        for v in validated:
            if v.get("validation", {}).get("overall") == "ACCEPT":
                accepted_total += 1
            else:
                rejected_total += 1

    result["summary"] = {
        "total_candidates": accepted_total + rejected_total,
        "accepted": accepted_total,
        "rejected": rejected_total,
    }

    out_path = VALIDATION_DIR / f"{fig_id}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None) -> list[str]:
    if figures:
        return figures
    all_ids = sorted(p.stem for p in GENERATION_DIR.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent workers")
    args = parser.parse_args()

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    client = get_validator_client()
    prompt_template = load_validate_prompt()
    fig_ids = get_figure_ids(args.limit, args.figures)

    print(f"Validating {len(fig_ids)} figures (4 calls per figure)")
    print(f"Validator: {VALIDATOR_MODEL} | temp={TEMPERATURE} | workers={args.workers}")
    print("-" * 60)

    total_accept, total_reject = 0, 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(validate_figure, client, prompt_template, fid): fid
            for fid in fig_ids
        }
        for future in as_completed(futures):
            fid = futures[future]
            try:
                result = future.result()
                if result:
                    s = result["summary"]
                    total_accept += s["accepted"]
                    total_reject += s["rejected"]
                    print(f"  {fid}: {s['accepted']}/{s['total_candidates']} accepted")
                else:
                    print(f"  {fid}: SKIPPED")
            except Exception as e:
                print(f"  {fid}: ERROR {e}")

    total = total_accept + total_reject
    print("-" * 60)
    if total:
        print(f"Done. {total_accept}/{total} accepted ({total_accept/total*100:.1f}%)")
    print(f"Output: {VALIDATION_DIR}")


if __name__ == "__main__":
    main()
