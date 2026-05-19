"""
Stage 1: Extract text elements and bounding boxes from figures using EasyOCR.

Output: results/adversarial_transforms/selective_blur/ocr_results/{fig_id}.json

Usage:
    python ocr_extract.py --limit 5
    python ocr_extract.py --figures fig_001 fig_002
    python ocr_extract.py                    # all 250
"""

from __future__ import annotations

import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import easyocr

from config import FIGURES_DIR, OCR_DIR


# Initialize reader once (heavy model load)
reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader


def extract_texts(fig_id: str) -> dict | None:
    out_path = OCR_DIR / f"{fig_id}.json"
    if out_path.exists():
        return None  # skip existing

    fig_path = FIGURES_DIR / f"{fig_id}.png"
    if not fig_path.exists():
        return None

    r = get_reader()
    ocr_results = r.readtext(str(fig_path))

    texts = []
    for bbox, text, confidence in ocr_results:
        x_min = int(min(p[0] for p in bbox))
        x_max = int(max(p[0] for p in bbox))
        y_min = int(min(p[1] for p in bbox))
        y_max = int(max(p[1] for p in bbox))

        texts.append({
            "text": text,
            "confidence": round(confidence, 3),
            "bbox": {"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max},
        })

    result = {
        "figure_id": fig_id,
        "total_texts": len(texts),
        "texts": texts,
    }

    out_path = OCR_DIR / f"{fig_id}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None) -> list[str]:
    if figures:
        return figures
    all_ids = sorted(p.stem for p in FIGURES_DIR.glob("*.png"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    OCR_DIR.mkdir(parents=True, exist_ok=True)
    fig_ids = get_figure_ids(args.limit, args.figures)

    print(f"Extracting text from {len(fig_ids)} figures using EasyOCR")
    print("-" * 60)

    # OCR is CPU-heavy, run sequentially
    for i, fig_id in enumerate(fig_ids, 1):
        result = extract_texts(fig_id)
        if result:
            print(f"  [{i}/{len(fig_ids)}] {fig_id}: {result['total_texts']} texts found")
        else:
            print(f"  [{i}/{len(fig_ids)}] {fig_id}: SKIPPED")

    print("-" * 60)
    print(f"Done. Output: {OCR_DIR}")


if __name__ == "__main__":
    main()
