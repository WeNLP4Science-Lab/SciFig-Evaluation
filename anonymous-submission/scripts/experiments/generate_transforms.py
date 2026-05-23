"""Generate transformed versions of all figure images.

Creates degraded copies of the original figures for robustness testing.
These are saved as dataset artifacts (not model outputs).

Transforms:
  noise         - Gaussian noise (sigma=25)
  low_contrast  - Reduced contrast (alpha=0.3, beta=50)
  rotation      - 15° clockwise rotation with white fill

Output: dataset/transforms/{transform_name}/{fig_id}.png

Usage:
    python generate_transforms.py                    # all transforms
    python generate_transforms.py --transform noise  # specific transform
    python generate_transforms.py --figures fig_001 fig_005
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import cv2
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import FIGURES_DIR, DATASET_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

TRANSFORMS_DIR = DATASET_DIR / "transforms"

TRANSFORMS = {
    "noise": {
        "description": "Gaussian noise (sigma=25)",
        "params": {"sigma": 25},
    },
    "low_contrast": {
        "description": "Reduced contrast (alpha=0.3, beta=50)",
        "params": {"alpha": 0.3, "beta": 50},
    },
    "rotation": {
        "description": "15° clockwise rotation with white fill",
        "params": {"angle": 15},
    },
}


def apply_noise(img, sigma=25):
    noise = np.random.normal(0, sigma, img.shape).astype(np.int16)
    noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return noisy


def apply_low_contrast(img, alpha=0.3, beta=50):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


def apply_rotation(img, angle=15):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))


TRANSFORM_FUNCS = {
    "noise": apply_noise,
    "low_contrast": apply_low_contrast,
    "rotation": apply_rotation,
}


def generate_transform(fig_id: str, transform_name: str) -> bool:
    out_dir = TRANSFORMS_DIR / transform_name
    out_path = out_dir / f"{fig_id}.png"

    if out_path.exists():
        return True

    fig_path = FIGURES_DIR / f"{fig_id}.png"
    if not fig_path.exists():
        logger.warning(f"  {fig_id}: original image not found")
        return False

    img = cv2.imread(str(fig_path))
    if img is None:
        logger.warning(f"  {fig_id}: failed to read image")
        return False

    params = TRANSFORMS[transform_name]["params"]
    func = TRANSFORM_FUNCS[transform_name]
    transformed = func(img, **params)

    cv2.imwrite(str(out_path), transformed)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transform", default="all", help="Transform name or 'all'")
    parser.add_argument("--figures", nargs="+", help="Specific figures")
    args = parser.parse_args()

    transforms = list(TRANSFORMS.keys()) if args.transform == "all" else [args.transform]
    fig_ids = args.figures or sorted(p.stem for p in FIGURES_DIR.glob("*.png"))

    for t in transforms:
        if t not in TRANSFORMS:
            logger.error(f"Unknown transform: {t}. Available: {list(TRANSFORMS.keys())}")
            continue

        out_dir = TRANSFORMS_DIR / t
        out_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating {t}: {TRANSFORMS[t]['description']}")

        done, skipped, failed = 0, 0, 0
        for fig_id in fig_ids:
            out_path = out_dir / f"{fig_id}.png"
            if out_path.exists():
                skipped += 1
                continue
            if generate_transform(fig_id, t):
                done += 1
            else:
                failed += 1

        logger.info(f"  {t}: {done} generated, {skipped} skipped, {failed} failed")

    logger.info("Done.")


if __name__ == "__main__":
    main()
