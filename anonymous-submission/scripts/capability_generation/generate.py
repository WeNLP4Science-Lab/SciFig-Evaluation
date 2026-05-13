"""
Stage 1: Generate 3 candidate questions per category using GPT-4o.

Generator receives: image + description + chart type.
Runs with concurrency for speed.

Output: results/capability_generation/generation/{fig_id}.json

Usage:
    python generate.py --limit 50
    python generate.py --workers 10       # concurrency level
    python generate.py --figures fig_001 fig_050
    python generate.py                    # all 250
"""

from __future__ import annotations

import json
import argparse
import base64
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import AzureOpenAI

from config import (
    AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION,
    GENERATOR_MODEL, TEMPERATURE, MAX_TOKENS,
    GROUNDTRUTH_DIR, FIGURES_DIR, GENERATION_DIR, PROMPTS_DIR, CATEGORIES,
)


def load_prompt(category: str) -> str:
    return (PROMPTS_DIR / f"{category}.txt").read_text()


def load_system_prompt() -> str:
    return (PROMPTS_DIR / "system.txt").read_text()


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


def generate_questions(client: AzureOpenAI, system_prompt: str,
                       category: str, gt: dict, description: str,
                       img_b64: str) -> list[dict]:
    prompt = load_prompt(category).format(
        chart_type=gt.get("figure_type", "Unknown"),
        description=description,
    )
    try:
        response = client.chat.completions.create(
            model=GENERATOR_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ]},
            ],
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        questions = data.get("questions", [])
        for q in questions:
            q["category"] = category
        return questions
    except Exception as e:
        print(f"    ERROR ({category}): {e}", file=sys.stderr)
        return []


def process_figure(client: AzureOpenAI, system_prompt: str, fig_id: str) -> dict | None:
    gt = load_groundtruth(fig_id)
    description = get_description(gt)
    img_b64 = encode_image(fig_id)

    if not description or not img_b64:
        return None

    result = {
        "figure_id": fig_id,
        "figure_type": gt.get("figure_type", ""),
        "generator_model": GENERATOR_MODEL,
        "temperature": TEMPERATURE,
        "candidates": {},
    }

    total = 0
    for cat in CATEGORIES:
        questions = generate_questions(client, system_prompt, cat, gt, description, img_b64)
        result["candidates"][cat] = questions
        total += len(questions)

    result["total_candidates"] = total

    out_path = GENERATION_DIR / f"{fig_id}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None) -> list[str]:
    if figures:
        return figures
    all_ids = sorted(p.stem for p in GROUNDTRUTH_DIR.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent workers")
    args = parser.parse_args()

    GENERATION_DIR.mkdir(parents=True, exist_ok=True)
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT, api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )
    system_prompt = load_system_prompt()
    fig_ids = get_figure_ids(args.limit, args.figures)

    print(f"Generating 3 questions x {len(CATEGORIES)} categories x {len(fig_ids)} figures")
    print(f"Model: {GENERATOR_MODEL} | temp={TEMPERATURE} | workers={args.workers}")
    print("-" * 60)

    done, failed = 0, 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process_figure, client, system_prompt, fid): fid
            for fid in fig_ids
        }
        for future in as_completed(futures):
            fid = futures[future]
            try:
                result = future.result()
                if result:
                    done += 1
                    print(f"  [{done+failed}/{len(fig_ids)}] {fid}: {result['total_candidates']} questions")
                else:
                    failed += 1
                    print(f"  [{done+failed}/{len(fig_ids)}] {fid}: SKIPPED")
            except Exception as e:
                failed += 1
                print(f"  [{done+failed}/{len(fig_ids)}] {fid}: ERROR {e}")

    print("-" * 60)
    print(f"Done. {done} succeeded, {failed} failed.")
    print(f"Output: {GENERATION_DIR}")


if __name__ == "__main__":
    main()
