"""
Apply blur for inductance only using v3 selections.
Does NOT touch admittance images or admittance probes.

Reads:  inductance_selections.json (curated picks)
        ocr_results/ (for bounding boxes)
        dataset/figures/ (original images)
        dataset/adversarial/probes/ (existing probes - updates inductance only)

Writes: dataset/adversarial/inductance/ (blurred images)
        dataset/adversarial/probes/ (updates inductance section only)
        dataset/adversarial/regions.json (updates inductance entries only)

Usage:
    python blur_inductance_v3.py
    python blur_inductance_v3.py --figures fig_001 fig_005
"""

from __future__ import annotations

import json
import argparse
import os
import cv2
import numpy as np
from pathlib import Path

from config import (
    FIGURES_DIR, INDUCTANCE_DIR, ADVERSARIAL_DIR,
    RESULTS_DIR, BLUR_KERNEL, BLUR_GRAY_BLEND,
)

OCR_DIR = RESULTS_DIR / "ocr_results"
PROBES_DIR = ADVERSARIAL_DIR / "probes"
SELECTIONS_PATH = RESULTS_DIR / "inductance_selections.json"
REGIONS_PATH = ADVERSARIAL_DIR / "regions.json"


def _normalize(s):
    s = s.lower().strip()
    s = s.replace('l', '1').replace('o', '0')
    s = ''.join(c for c in s if c.isalnum())
    return s


def _similarity(a, b):
    if not a or not b:
        return 0.0
    a_norm, b_norm = _normalize(a), _normalize(b)
    if a_norm == b_norm:
        return 1.0
    if a_norm in b_norm or b_norm in a_norm:
        return min(len(a_norm), len(b_norm)) / max(len(a_norm), len(b_norm))
    common = sum(1 for c in a_norm if c in b_norm)
    return common / max(len(a_norm), len(b_norm))


def find_bbox(ocr_texts, target_text):
    target_lower = target_text.lower().strip()
    target_norm = _normalize(target_text)

    for t in ocr_texts:
        if t["text"].lower().strip() == target_lower:
            return t["bbox"]

    for t in ocr_texts:
        if _normalize(t["text"]) == target_norm:
            return t["bbox"]

    scored = []
    for t in ocr_texts:
        sim = _similarity(target_text, t["text"])
        if sim >= 0.6:
            scored.append((t, sim))

    if scored:
        target_len = len(target_text)
        scored.sort(key=lambda x: (x[1], -abs(len(x[0]["text"]) - target_len)), reverse=True)
        return scored[0][0]["bbox"]

    return None


def apply_blur(image_path, bbox, output_path):
    img = cv2.imread(image_path)
    if img is None:
        return False

    x1, y1 = bbox["x_min"], bbox["y_min"]
    x2, y2 = bbox["x_max"], bbox["y_max"]

    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return False

    roi = img[y1:y2, x1:x2]

    if BLUR_GRAY_BLEND > 0:
        gray_mask = np.full_like(roi, 200)
        roi = cv2.addWeighted(roi, 1 - BLUR_GRAY_BLEND, gray_mask, BLUR_GRAY_BLEND, 0)

    kernel = BLUR_KERNEL if BLUR_KERNEL % 2 == 1 else BLUR_KERNEL + 1
    blurred = cv2.GaussianBlur(roi, (kernel, kernel), 0)
    img[y1:y2, x1:x2] = blurred

    cv2.imwrite(output_path, img)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    INDUCTANCE_DIR.mkdir(parents=True, exist_ok=True)
    PROBES_DIR.mkdir(parents=True, exist_ok=True)

    with open(SELECTIONS_PATH) as f:
        sel_data = json.load(f)

    selections = sel_data["selections"]
    skipped = sel_data.get("skipped_inductance", [])

    # Load existing regions
    if REGIONS_PATH.exists():
        with open(REGIONS_PATH) as f:
            regions = json.load(f)
    else:
        regions = {}

    fig_ids = args.figures if args.figures else sorted(selections.keys())

    print(f"Blurring inductance for {len(fig_ids)} figures (skipping {len(skipped)})")
    print(f"Blur kernel: {BLUR_KERNEL} | Gray blend: {BLUR_GRAY_BLEND}")
    print("-" * 60)

    done, failed, skip_count = 0, 0, 0

    for i, fig_id in enumerate(fig_ids, 1):
        if fig_id in skipped:
            skip_count += 1
            continue

        sel = selections.get(fig_id)
        if not sel:
            skip_count += 1
            continue

        target_text = sel["selected_text"]
        question = sel.get("question", "")
        sel_type = sel.get("type", "")

        # Find bbox from OCR
        ocr_path = OCR_DIR / f"{fig_id}.json"
        if not ocr_path.exists():
            failed += 1
            print(f"  {fig_id}: OCR not found")
            continue

        with open(ocr_path) as f:
            ocr_data = json.load(f)

        bbox = find_bbox(ocr_data["texts"], target_text)
        if not bbox:
            failed += 1
            print(f"  {fig_id}: \"{target_text}\" not found in OCR")
            continue

        # Apply blur
        fig_path = str(FIGURES_DIR / f"{fig_id}.png")
        out_path = str(INDUCTANCE_DIR / f"{fig_id}.png")

        if apply_blur(fig_path, bbox, out_path):
            done += 1

            # Update regions - only inductance
            if fig_id not in regions:
                regions[fig_id] = {"figure_id": fig_id}
            regions[fig_id]["inductance"] = {
                "text": target_text,
                "bbox": bbox,
                "question": question,
                "type": sel_type,
            }

            # Update probe - only inductance section
            probe_path = PROBES_DIR / f"{fig_id}.json"
            if probe_path.exists():
                with open(probe_path) as f:
                    probe = json.load(f)
            else:
                probe = {"figure_id": fig_id, "selective_blur": {}}

            probe["selective_blur"]["inductance"] = {
                "blurred_text": target_text,
                "question": question,
                "candidate_type": sel_type,
                "expected_behavior": "Model should attempt to infer from visual context or sequence pattern",
            }

            # Add OCR texts if not present
            if "ocr_texts" not in probe:
                texts = [t["text"] for t in ocr_data["texts"]
                         if t["text"].strip() and len(t["text"]) > 1]
                seen = set()
                unique = []
                for t in texts:
                    if t.lower() not in seen:
                        unique.append(t)
                        seen.add(t.lower())
                probe["ocr_texts"] = unique

            with open(probe_path, "w") as f:
                json.dump(probe, f, indent=2)
        else:
            failed += 1
            print(f"  {fig_id}: blur failed")

        if (i) % 50 == 0:
            print(f"  [{i}/{len(fig_ids)}] {done} done, {failed} failed, {skip_count} skipped")

    # Save regions
    with open(REGIONS_PATH, "w") as f:
        json.dump(regions, f, indent=2)

    print("-" * 60)
    print(f"Done. {done} blurred, {failed} failed, {skip_count} skipped.")
    print(f"Inductance images: {INDUCTANCE_DIR}")
    print(f"Probes updated: {PROBES_DIR}")


if __name__ == "__main__":
    main()
