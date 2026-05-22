"""
Run v3 inductance identification (dual numeric + text) for all figures.

Skips figures already in identifications_v3/.
Uses upscaled OCR results.
Does NOT touch admittance — keeps existing v2 admittance.

Usage:
    python run_inductance_v3.py --limit 10
    python run_inductance_v3.py --workers 8
    python run_inductance_v3.py
"""

from __future__ import annotations

import json
import argparse
import base64
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from openai import AzureOpenAI

from config import (
    AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION,
    MODEL, TEMPERATURE, RESULTS_DIR, FIGURES_DIR, PROMPTS_DIR, DATASET_DIR,
)

V3_DIR = RESULTS_DIR / "identifications_v3"
OCR_DIR = RESULTS_DIR / "ocr_results"
GT_DIR = DATASET_DIR / "groundtruth"


def get_description(fig_id: str) -> str:
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


def process_figure(client, prompt_template, fig_id):
    out_path = V3_DIR / f"{fig_id}.json"
    if out_path.exists():
        return None  # skip existing

    ocr_path = OCR_DIR / f"{fig_id}.json"
    if not ocr_path.exists():
        return None

    with open(ocr_path) as f:
        ocr_data = json.load(f)

    fig_path = FIGURES_DIR / f"{fig_id}.png"
    if not fig_path.exists():
        return None

    with open(fig_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    description = get_description(fig_id)
    text_list = "\n".join(
        f'  - "{t["text"]}" (confidence: {t["confidence"]})'
        for t in ocr_data["texts"]
    )
    prompt = prompt_template.format(texts=text_list, description=description)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            max_tokens=3000,
            response_format={"type": "json_object"},
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        result = json.loads(response.choices[0].message.content)
        result["figure_id"] = fig_id
        result["version"] = "v3-dual"

        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)

        return result
    except Exception as e:
        return {"figure_id": fig_id, "error": str(e)}


def get_figure_ids(limit=None):
    all_ids = sorted(p.stem for p in OCR_DIR.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    V3_DIR.mkdir(parents=True, exist_ok=True)
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )
    prompt_template = (PROMPTS_DIR / "identify_from_ocr.txt").read_text()
    fig_ids = get_figure_ids(args.limit)

    # Count existing
    existing = sum(1 for f in fig_ids if (V3_DIR / f"{f}.json").exists())
    remaining = len(fig_ids) - existing

    print(f"V3 inductance identification: {len(fig_ids)} figures ({existing} done, {remaining} remaining)")
    print(f"Model: {MODEL} | temp={TEMPERATURE} | workers={args.workers}")
    print("-" * 60)

    if remaining == 0:
        print("All done.")
        return

    done, failed = 0, 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process_figure, client, prompt_template, fid): fid
            for fid in fig_ids
            if not (V3_DIR / f"{fid}.json").exists()
        }
        for future in as_completed(futures):
            fid = futures[future]
            try:
                result = future.result()
                if result and "error" not in result:
                    done += 1
                    num_c = len(result.get("inductance_numeric_candidates", []))
                    txt_c = len(result.get("inductance_text_candidates", []))
                    if (done + failed) % 25 == 0:
                        print(f"  [{done+failed}/{remaining}] {done} done, {failed} failed")
                elif result and "error" in result:
                    failed += 1
                    print(f"  {fid}: ERROR {result['error'][:80]}")
            except Exception as e:
                failed += 1
                print(f"  {fid}: ERROR {e}")

    print("-" * 60)
    print(f"Done. {done} succeeded, {failed} failed.")
    print(f"Output: {V3_DIR}")


if __name__ == "__main__":
    main()
