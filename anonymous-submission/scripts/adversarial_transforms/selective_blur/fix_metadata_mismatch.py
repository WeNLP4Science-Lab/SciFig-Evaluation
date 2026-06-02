"""Regenerate selective-blur images for figures where the dashboard probe
metadata claims a different blurred element than what the current image actually
blurs (off-by-one bug introduced by a stale regeneration pass).

The metadata + model-evaluation results are authoritative. This script realigns
the images to match by re-blurring the original figure with the OCR bbox of the
text that the probe metadata claims is blurred.

Run from the repo root:
    python scripts/adversarial_transforms/selective_blur/fix_metadata_mismatch.py
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = PROJECT_ROOT / "dataset"
FIGURES_DIR = DATASET_DIR / "figures"
ADVERSARIAL_DIR = DATASET_DIR / "adversarial"
ADMITTANCE_DIR = ADVERSARIAL_DIR / "admittance"
INDUCTANCE_DIR = ADVERSARIAL_DIR / "inductance"
PROBES_DIR = ADVERSARIAL_DIR / "probes"
DASHBOARD_PROBES_DIR = PROJECT_ROOT / "dashboard" / "public" / "probes"
OCR_DIR = PROJECT_ROOT / "results" / "tasks" / "adversarial_transforms" / "selective_blur" / "ocr_results"
ID_DIR = PROJECT_ROOT / "results" / "tasks" / "adversarial_transforms" / "selective_blur" / "identifications"

BLUR_KERNEL = 75
BLUR_GRAY_BLEND = 0.7


def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("l", "1").replace("o", "0")
    return "".join(c for c in s if c.isalnum())


def _similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    an, bn = _normalize(a), _normalize(b)
    if an == bn:
        return 1.0
    if an in bn or bn in an:
        return min(len(an), len(bn)) / max(len(an), len(bn))
    common = sum(1 for c in an if c in bn)
    return common / max(len(an), len(bn))


def find_bbox(ocr_texts, target_text):
    """Find the best-matching OCR bbox for target_text."""
    target_lower = target_text.lower().strip()
    target_norm = _normalize(target_text)

    # Exact match first
    for item in ocr_texts:
        if item["text"].lower().strip() == target_lower:
            return item["bbox"]

    # Normalized match
    for item in ocr_texts:
        if _normalize(item["text"]) == target_norm:
            return item["bbox"]

    # Best similarity
    best, best_score = None, 0.0
    for item in ocr_texts:
        score = _similarity(target_text, item["text"])
        if score > best_score:
            best, best_score = item, score
    if best and best_score >= 0.7:
        return best["bbox"]
    return None


def apply_blur(figure_path, bbox, output_path):
    img = cv2.imread(str(figure_path))
    if img is None:
        return False, "cv2_read_failed"
    h, w = img.shape[:2]
    x1, y1 = max(0, bbox["x_min"]), max(0, bbox["y_min"])
    x2, y2 = min(w, bbox["x_max"]), min(h, bbox["y_max"])
    if x2 <= x1 or y2 <= y1:
        return False, "empty_bbox"
    roi = img[y1:y2, x1:x2].copy()
    if BLUR_GRAY_BLEND > 0:
        gray_mask = np.full_like(roi, 200)
        roi = cv2.addWeighted(roi, 1 - BLUR_GRAY_BLEND, gray_mask, BLUR_GRAY_BLEND, 0)
    kernel = BLUR_KERNEL if BLUR_KERNEL % 2 == 1 else BLUR_KERNEL + 1
    blurred = cv2.GaussianBlur(roi, (kernel, kernel), 0)
    img[y1:y2, x1:x2] = blurred
    cv2.imwrite(str(output_path), img)
    return True, "ok"


def collect_mismatches():
    """Return list of (fig_id, probe_type, claimed_text) for figures where the
    dashboard probe's blurred_text matches a non-first identification candidate.
    These are the off-by-N cases the eval was scored against."""
    out = []
    for probe_path in sorted(DASHBOARD_PROBES_DIR.glob("*.json")):
        fid = probe_path.stem
        id_path = ID_DIR / f"{fid}.json"
        if not id_path.exists():
            continue
        with open(probe_path) as f:
            probe = json.load(f)
        with open(id_path) as f:
            ident = json.load(f)
        sb = probe.get("selective_blur") or {}
        for kind in ("admittance", "inductance"):
            entry = sb.get(kind)
            if not entry:
                continue
            claimed = (entry.get("blurred_text") or "").strip()
            cands = [c.get("selected_text", "").strip() for c in ident.get(f"{kind}_candidates", [])]
            if not cands or not claimed:
                continue
            if claimed != cands[0] and claimed in cands:
                out.append((fid, kind, claimed))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report only, do not write files")
    args = parser.parse_args()

    mismatches = collect_mismatches()
    print(f"Found {len(mismatches)} mismatched probes to fix")
    print(f"  admittance: {sum(1 for _,k,_ in mismatches if k == 'admittance')}")
    print(f"  inductance: {sum(1 for _,k,_ in mismatches if k == 'inductance')}")
    print()

    fixed, skipped, failed = 0, 0, 0
    for fid, kind, claimed in mismatches:
        ocr_path = OCR_DIR / f"{fid}.json"
        if not ocr_path.exists():
            print(f"  SKIP {fid:9} {kind:11} '{claimed}' -- no OCR")
            skipped += 1
            continue
        with open(ocr_path) as f:
            ocr = json.load(f)
        bbox = find_bbox(ocr.get("texts", []), claimed)
        if not bbox:
            print(f"  FAIL {fid:9} {kind:11} '{claimed}' -- no bbox match")
            failed += 1
            continue
        fig_path = FIGURES_DIR / f"{fid}.png"
        out_dir = ADMITTANCE_DIR if kind == "admittance" else INDUCTANCE_DIR
        out_path = out_dir / f"{fid}.png"
        if not fig_path.exists():
            print(f"  SKIP {fid:9} {kind:11} '{claimed}' -- no source figure")
            skipped += 1
            continue
        if args.dry_run:
            print(f"  WOULD {fid:9} {kind:11} blur '{claimed}' at bbox={bbox}")
            fixed += 1
            continue
        ok, reason = apply_blur(fig_path, bbox, out_path)
        if ok:
            print(f"  FIXED {fid:9} {kind:11} '{claimed}'")
            fixed += 1
        else:
            print(f"  FAIL  {fid:9} {kind:11} '{claimed}' -- {reason}")
            failed += 1

    print()
    print(f"Summary: fixed={fixed} skipped={skipped} failed={failed}")
    if not args.dry_run and fixed > 0:
        print()
        print("Next: sync regenerated images to dashboard/public/")
        print(f"  cp {ADMITTANCE_DIR}/*.png dashboard/public/adversarial_admittance/")
        print(f"  cp {INDUCTANCE_DIR}/*.png dashboard/public/adversarial_inductance/")


if __name__ == "__main__":
    sys.exit(main())
