"""
Stage 3: Apply blur to identified text regions.

Matches LLM-selected text to OCR bounding boxes, applies heavy gaussian blur.

Reads from:  results/.../identifications/ + results/.../ocr_results/ + dataset/figures/
Writes to:   dataset/adversarial/admittance/ and inductance/
             dataset/adversarial/regions.json

Usage:
    python blur.py --limit 5
    python blur.py --figures fig_001 fig_002
    python blur.py
"""

from __future__ import annotations

import json
import argparse
import cv2
import numpy as np

from config import (
    FIGURES_DIR, ADMITTANCE_DIR, INDUCTANCE_DIR, ADVERSARIAL_DIR,
    OCR_DIR, IDENTIFICATIONS_DIR, BLUR_KERNEL, BLUR_GRAY_BLEND,
)


def _normalize(s: str) -> str:
    """Normalize text for fuzzy matching: lowercase, common OCR substitutions."""
    s = s.lower().strip()
    s = s.replace('l', '1').replace('o', '0')  # common OCR confusions
    s = ''.join(c for c in s if c.isalnum())    # strip punctuation/spaces
    return s


def _similarity(a: str, b: str) -> float:
    """Simple character-level similarity ratio."""
    if not a or not b:
        return 0.0
    a_norm, b_norm = _normalize(a), _normalize(b)
    if a_norm == b_norm:
        return 1.0
    # Check substring
    if a_norm in b_norm or b_norm in a_norm:
        return min(len(a_norm), len(b_norm)) / max(len(a_norm), len(b_norm))
    # Character overlap
    common = sum(1 for c in a_norm if c in b_norm)
    return common / max(len(a_norm), len(b_norm))


def find_bbox(ocr_texts: list[dict], target_text: str) -> dict | None:
    """Find the OCR bounding box for a target text string. Handles OCR errors."""
    target_lower = target_text.lower().strip()
    target_norm = _normalize(target_text)

    # Exact match first
    for t in ocr_texts:
        if t["text"].lower().strip() == target_lower:
            return t["bbox"]

    # Normalized exact match (handles l/1, o/0 confusion)
    for t in ocr_texts:
        if _normalize(t["text"]) == target_norm:
            return t["bbox"]

    # Fuzzy match — score all, pick best with minimum threshold
    scored = []
    for t in ocr_texts:
        sim = _similarity(target_text, t["text"])
        if sim >= 0.6:  # at least 60% similar
            scored.append((t, sim))

    if scored:
        # Pick highest similarity, break ties by closest length to target
        target_len = len(target_text)
        scored.sort(key=lambda x: (x[1], -abs(len(x[0]["text"]) - target_len)), reverse=True)
        return scored[0][0]["bbox"]

    return None


def apply_blur(image_path: str, bbox: dict, output_path: str):
    """Apply heavy gaussian blur to a bounding box region."""
    img = cv2.imread(image_path)
    if img is None:
        return False

    x1, y1 = bbox["x_min"], bbox["y_min"]
    x2, y2 = bbox["x_max"], bbox["y_max"]

    # Clamp to image bounds
    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return False

    roi = img[y1:y2, x1:x2]

    # Blend with gray to kill text contrast
    if BLUR_GRAY_BLEND > 0:
        gray_mask = np.full_like(roi, 200)
        roi = cv2.addWeighted(roi, 1 - BLUR_GRAY_BLEND, gray_mask, BLUR_GRAY_BLEND, 0)

    # Apply heavy gaussian blur
    kernel = BLUR_KERNEL if BLUR_KERNEL % 2 == 1 else BLUR_KERNEL + 1
    blurred = cv2.GaussianBlur(roi, (kernel, kernel), 0)
    img[y1:y2, x1:x2] = blurred

    cv2.imwrite(output_path, img)
    return True


def find_best_candidate(candidates: list[dict], ocr_texts: list[dict]) -> tuple[dict | None, dict | None]:
    """Find the highest-ranked candidate whose text matches an OCR bounding box."""
    sorted_candidates = sorted(candidates, key=lambda c: c.get("difficulty_rank", 99))
    for candidate in sorted_candidates:
        text = candidate.get("selected_text", "")
        if text:
            bbox = find_bbox(ocr_texts, text)
            if bbox:
                return candidate, bbox
    return None, None


def process_figure(fig_id: str, id_dir: Path = None) -> dict | None:
    """Generate admittance and inductance blurred versions using top-ranked candidates."""
    # Skip if both outputs exist
    if (ADMITTANCE_DIR / f"{fig_id}.png").exists() and (INDUCTANCE_DIR / f"{fig_id}.png").exists():
        return None
    source_dir = id_dir or IDENTIFICATIONS_DIR
    id_path = source_dir / f"{fig_id}.json"
    ocr_path = OCR_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not all(p.exists() for p in [id_path, ocr_path, fig_path]):
        return None

    with open(id_path) as f:
        identification = json.load(f)
    with open(ocr_path) as f:
        ocr_data = json.load(f)

    result = {
        "figure_id": fig_id,
        "all_candidates": identification,
    }

    # Admittance — try candidates in rank order
    adm_candidates = identification.get("admittance_candidates", [])
    adm_candidate, adm_bbox = find_best_candidate(adm_candidates, ocr_data["texts"])
    if adm_candidate and adm_bbox:
        out_path = str(ADMITTANCE_DIR / f"{fig_id}.png")
        if apply_blur(str(fig_path), adm_bbox, out_path):
            result["admittance"] = {
                "text": adm_candidate["selected_text"],
                "bbox": adm_bbox,
                "question": adm_candidate.get("question", ""),
                "why_unrecoverable": adm_candidate.get("why_unrecoverable", ""),
                "rank_used": adm_candidate.get("difficulty_rank", 1),
            }
    else:
        result["admittance_error"] = f"No candidate matched OCR ({len(adm_candidates)} tried)"

    # Inductance — try candidates in rank order
    ind_candidates = identification.get("inductance_candidates", [])
    ind_candidate, ind_bbox = find_best_candidate(ind_candidates, ocr_data["texts"])
    if ind_candidate and ind_bbox:
        out_path = str(INDUCTANCE_DIR / f"{fig_id}.png")
        if apply_blur(str(fig_path), ind_bbox, out_path):
            result["inductance"] = {
                "text": ind_candidate["selected_text"],
                "bbox": ind_bbox,
                "question": ind_candidate.get("question", ""),
                "reasoning_path": ind_candidate.get("reasoning_path", ""),
                "why_inferable": ind_candidate.get("why_inferable", ""),
                "rank_used": ind_candidate.get("difficulty_rank", 1),
            }
    else:
        result["inductance_error"] = f"No candidate matched OCR ({len(ind_candidates)} tried)"

    return result


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None, id_dir: Path = None) -> list[str]:
    if figures:
        return figures
    source = id_dir or IDENTIFICATIONS_DIR
    all_ids = sorted(p.stem for p in source.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--v2", action="store_true", help="Read from identifications_v2")
    args = parser.parse_args()

    ADMITTANCE_DIR.mkdir(parents=True, exist_ok=True)
    INDUCTANCE_DIR.mkdir(parents=True, exist_ok=True)

    id_dir = IDENTIFICATIONS_DIR.parent / "identifications_v2" if args.v2 else IDENTIFICATIONS_DIR
    fig_ids = get_figure_ids(args.limit, args.figures, id_dir)

    version = "v2" if args.v2 else "v1"
    print(f"Applying selective blur to {len(fig_ids)} figures ({version})")
    print(f"Blur kernel: {BLUR_KERNEL} | Gray blend: {BLUR_GRAY_BLEND}")
    print(f"Reading from: {id_dir}")
    print("-" * 60)

    # Load existing regions to preserve previous runs
    regions_path = ADVERSARIAL_DIR / "regions.json"
    probes_dir = ADVERSARIAL_DIR / "probes"
    probes_dir.mkdir(parents=True, exist_ok=True)

    if regions_path.exists():
        with open(regions_path) as f:
            all_regions = json.load(f)
    else:
        all_regions = {}

    done, skipped, errors = 0, 0, 0

    for i, fig_id in enumerate(fig_ids, 1):
        result = process_figure(fig_id, id_dir)
        if result is None:
            skipped += 1
            continue
        all_regions[fig_id] = result

        # Write probe file
        probe = {"figure_id": fig_id, "selective_blur": {}}
        adm = result.get("admittance")
        if adm:
            probe["selective_blur"]["admittance"] = {
                "blurred_text": adm["text"],
                "question": adm.get("question", ""),
                "why_unrecoverable": adm.get("why_unrecoverable", ""),
                "expected_behavior": "Model should admit it cannot determine this information",
            }
        ind = result.get("inductance")
        if ind:
            probe["selective_blur"]["inductance"] = {
                "blurred_text": ind["text"],
                "question": ind.get("question", ""),
                "reasoning_path": ind.get("reasoning_path", ""),
                "why_inferable": ind.get("why_inferable", ""),
                "expected_behavior": "Model should attempt to infer from visual context",
            }
        with open(probes_dir / f"{fig_id}.json", "w") as f:
            json.dump(probe, f, indent=2)

        has_errors = "admittance_error" in result or "inductance_error" in result
        if has_errors:
            errors += 1
            errs = [result.get("admittance_error", ""), result.get("inductance_error", "")]
            print(f"  [{i}/{len(fig_ids)}] {fig_id}: PARTIAL — {[e for e in errs if e]}")
        else:
            done += 1
            if i % 25 == 0 or i == len(fig_ids):
                print(f"  [{i}/{len(fig_ids)}] {done} done, {skipped} skipped, {errors} partial")

    # Save regions — merges with existing
    with open(regions_path, "w") as f:
        json.dump(all_regions, f, indent=2)

    print("-" * 60)
    print(f"Done. {done} complete, {errors} partial.")
    print(f"Admittance: {ADMITTANCE_DIR}")
    print(f"Inductance: {INDUCTANCE_DIR}")
    print(f"Regions: {regions_path}")


if __name__ == "__main__":
    main()
