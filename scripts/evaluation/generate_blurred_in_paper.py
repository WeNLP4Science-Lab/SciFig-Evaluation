"""Generate blurred_in_paper transform for adversarial figures.

For each figure, locates the figure region within the paper page snapshot
(original_in_paper.jpeg) using multi-scale template matching, then applies
heavy Gaussian blur to make the figure unreadable while preserving
surrounding text and context.

Output: adversarial_experiments/figures/{subfolder}/{fig_key}/transforms/blurred_in_paper.png

Usage:
    python3 scripts/evaluation/generate_blurred_in_paper.py
    python3 scripts/evaluation/generate_blurred_in_paper.py --figure english_fig_002
    python3 scripts/evaluation/generate_blurred_in_paper.py --subfolder english_only
"""

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
ADVERSARIAL_DIR = ROOT / "adversarial_experiments"
FIGURES_DIR = ADVERSARIAL_DIR / "figures"
SAMPLES_FILE = ADVERSARIAL_DIR / "samples.json"
OVERRIDES_FILE = FIGURES_DIR / "blurred_in_paper_overrides.json"


def find_figure_bbox(page_img, figure_img, scales=None):
    """Locate figure within a paper page using multi-scale template matching.

    Returns (x, y, w, h, confidence) of the best match, or None if no good match.
    """
    if scales is None:
        scales = np.arange(0.15, 1.05, 0.05)

    page_gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
    fig_gray = cv2.cvtColor(figure_img, cv2.COLOR_BGR2GRAY)
    fig_h, fig_w = fig_gray.shape[:2]
    page_h, page_w = page_gray.shape[:2]

    best_val = -1
    best_loc = None
    best_scale = None

    for scale in scales:
        scaled_w = int(fig_w * scale)
        scaled_h = int(fig_h * scale)

        # Skip if scaled template is larger than the page
        if scaled_w >= page_w or scaled_h >= page_h:
            continue
        # Skip tiny templates
        if scaled_w < 20 or scaled_h < 20:
            continue

        scaled_fig = cv2.resize(fig_gray, (scaled_w, scaled_h), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(page_gray, scaled_fig, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale

    if best_val < 0.3 or best_loc is None:
        return None

    x, y = best_loc
    w = int(fig_w * best_scale)
    h = int(fig_h * best_scale)
    return x, y, w, h, best_val


def _load_overrides():
    """Load manual bounding box overrides for figures where template matching fails."""
    if OVERRIDES_FILE.exists():
        with open(OVERRIDES_FILE) as f:
            data = json.load(f)
        # Strip the _description key
        return {k: v for k, v in data.items() if not k.startswith("_")}
    return {}


def blur_region(page_img, x, y, w, h, blur_ksize=99):
    """Apply heavy Gaussian blur to a region of the image."""
    result = page_img.copy()
    region = result[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(region, (blur_ksize, blur_ksize), 0)
    result[y:y+h, x:x+w] = blurred
    return result


def process_figure(subfolder, fig_key, overrides, force=False):
    """Process a single figure. Returns (success, message)."""
    fig_dir = FIGURES_DIR / subfolder / fig_key
    page_path = fig_dir / "original_in_paper.jpeg"
    orig_path = fig_dir / "original.png"
    out_path = fig_dir / "transforms" / "blurred_in_paper.png"

    if out_path.exists() and not force:
        return True, "skip"

    if not page_path.exists():
        return False, f"no page snapshot: {page_path}"

    page_img = cv2.imread(str(page_path))
    if page_img is None:
        return False, f"failed to read page: {page_path}"

    override_key = f"{subfolder}/{fig_key}"
    if override_key in overrides:
        x, y, w, h = overrides[override_key]
        source = "override"
        confidence = 1.0
    else:
        if not orig_path.exists():
            return False, f"no original image: {orig_path}"
        figure_img = cv2.imread(str(orig_path))
        if figure_img is None:
            return False, f"failed to read figure: {orig_path}"

        bbox = find_figure_bbox(page_img, figure_img)
        if bbox is None:
            return False, "template matching failed — could not locate figure on page"
        x, y, w, h, confidence = bbox
        source = "matched"

    blurred_page = blur_region(page_img, x, y, w, h)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), blurred_page)

    return True, f"{source} bbox=({x},{y},{w},{h}) conf={confidence:.3f}"


def main():
    parser = argparse.ArgumentParser(description="Generate blurred_in_paper adversarial transform")
    parser.add_argument("--figure", default=None, help="Process only this figure key")
    parser.add_argument("--subfolder", default=None, help="Process only this subfolder")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()

    with open(SAMPLES_FILE) as f:
        samples = json.load(f)["samples"]

    overrides = _load_overrides()

    success_count = 0
    fail_count = 0
    skip_count = 0

    for subfolder, fig_keys in samples.items():
        if args.subfolder and subfolder != args.subfolder:
            continue
        for fig_key in fig_keys:
            if args.figure and fig_key != args.figure:
                continue

            ok, msg = process_figure(subfolder, fig_key, overrides, force=args.force)
            if msg == "skip":
                skip_count += 1
                continue
            elif ok:
                success_count += 1
                print(f"  OK   {subfolder}/{fig_key} — {msg}")
            else:
                fail_count += 1
                print(f"  FAIL {subfolder}/{fig_key} — {msg}")

    total = success_count + fail_count + skip_count
    print(f"\nDone. {total} figures: {success_count} generated, {skip_count} skipped, {fail_count} failed.")


if __name__ == "__main__":
    main()
