"""
Stage 2: Send image + OCR texts to GPT-4o to identify blur targets.

GPT-4o sees the image AND the OCR-extracted text list.
It selects the best admittance and inductance targets by text string.

Reads from:  results/.../ocr_results/
Writes to:   results/.../identifications/

Usage:
    python identify.py --limit 5
    python identify.py --figures fig_001 fig_002
    python identify.py --workers 8
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
    MODEL, TEMPERATURE, OCR_DIR, IDENTIFICATIONS_DIR, FIGURES_DIR, PROMPTS_DIR,
)


def load_prompt() -> str:
    return (PROMPTS_DIR / "identify_from_ocr.txt").read_text()


def encode_image(fig_id: str) -> str | None:
    path = FIGURES_DIR / f"{fig_id}.png"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def identify_targets(client: AzureOpenAI, prompt_template: str, fig_id: str) -> dict | None:
    out_path = IDENTIFICATIONS_DIR / f"{fig_id}.json"
    if out_path.exists():
        return None  # skip existing

    ocr_path = OCR_DIR / f"{fig_id}.json"
    if not ocr_path.exists():
        return None

    with open(ocr_path) as f:
        ocr_data = json.load(f)

    img_b64 = encode_image(fig_id)
    if not img_b64:
        return None

    # Format texts for the prompt
    text_list = "\n".join(
        f'  - "{t["text"]}" (confidence: {t["confidence"]})'
        for t in ocr_data["texts"]
    )

    prompt = prompt_template.format(texts=text_list)

    try:
        response = client.chat.completions.create(
            model=MODEL,
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
        result = json.loads(content)
        result["figure_id"] = fig_id
        result["model"] = MODEL

        out_path = IDENTIFICATIONS_DIR / f"{fig_id}.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)

        return result
    except Exception as e:
        print(f"  {fig_id}: ERROR {e}", file=sys.stderr)
        return None


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None) -> list[str]:
    if figures:
        return figures
    all_ids = sorted(p.stem for p in OCR_DIR.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    IDENTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT, api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )
    prompt_template = load_prompt()
    fig_ids = get_figure_ids(args.limit, args.figures)

    print(f"Identifying blur targets for {len(fig_ids)} figures")
    print(f"Model: {MODEL} | temp={TEMPERATURE} | workers={args.workers}")
    print("-" * 60)

    done, failed = 0, 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(identify_targets, client, prompt_template, fid): fid
            for fid in fig_ids
        }
        for future in as_completed(futures):
            fid = futures[future]
            try:
                result = future.result()
                if result:
                    done += 1
                    adm = result.get("admittance", {}).get("selected_text", "?")
                    ind = result.get("inductance", {}).get("selected_text", "?")
                    print(f"  [{done+failed}/{len(fig_ids)}] {fid}: admit=\"{adm}\" | induct=\"{ind}\"")
                else:
                    failed += 1
                    print(f"  [{done+failed}/{len(fig_ids)}] {fid}: SKIPPED")
            except Exception as e:
                failed += 1
                print(f"  [{done+failed}/{len(fig_ids)}] {fid}: ERROR {e}")

    print("-" * 60)
    print(f"Done. {done} succeeded, {failed} failed.")
    print(f"Output: {IDENTIFICATIONS_DIR}")


if __name__ == "__main__":
    main()
