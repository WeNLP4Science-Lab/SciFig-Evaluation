"""Apply adversarial image transforms to test model robustness.

Transforms preserve the semantic content (groundtruth stays valid) but
degrade the image in ways that challenge model understanding.

Five transforms:
  1. jpeg_compression  – Heavy JPEG artifacts (quality=15)
  2. low_resolution    – Downscale to 25% then upscale back
  3. gaussian_blur     – Strong blur (radius=4)
  4. noise             – Gaussian noise overlay
  5. grayscale         – Convert to grayscale (removes color cues)

Usage:
    python3 scripts/evaluation/adversarial_transforms.py [--figures FIG1 FIG2 ...] [--subfolder X]
"""

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = ROOT / "Dataset"
TRANSFORMS_DIR = ROOT / "transforms"

TRANSFORMS = {
    "jpeg_compression": "Heavy JPEG compression (quality=15)",
    "low_resolution": "Downscale to 25% then upscale back",
    "gaussian_blur": "Gaussian blur (radius=4)",
    "noise": "Gaussian noise (sigma=30)",
    "grayscale": "Convert to grayscale",
}


def apply_jpeg_compression(img: Image.Image) -> Image.Image:
    """Apply heavy JPEG compression artifacts."""
    from io import BytesIO
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=15)
    buf.seek(0)
    return Image.open(buf).copy()


def apply_low_resolution(img: Image.Image) -> Image.Image:
    """Downscale to 25% then upscale back to original size."""
    w, h = img.size
    small = img.resize((w // 4, h // 4), Image.Resampling.BILINEAR)
    return small.resize((w, h), Image.Resampling.NEAREST)


def apply_gaussian_blur(img: Image.Image) -> Image.Image:
    """Apply strong Gaussian blur."""
    return img.filter(ImageFilter.GaussianBlur(radius=4))


def apply_noise(img: Image.Image) -> Image.Image:
    """Add Gaussian noise."""
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 30, arr.shape)
    noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)


def apply_grayscale(img: Image.Image) -> Image.Image:
    """Convert to grayscale (removes color information)."""
    return img.convert("L").convert("RGB")


TRANSFORM_FNS = {
    "jpeg_compression": apply_jpeg_compression,
    "low_resolution": apply_low_resolution,
    "gaussian_blur": apply_gaussian_blur,
    "noise": apply_noise,
    "grayscale": apply_grayscale,
}


def main():
    parser = argparse.ArgumentParser(description="Apply adversarial transforms to figures")
    parser.add_argument(
        "--figures", nargs="+",
        default=["english_fig_017", "english_fig_012", "english_fig_020", "english_fig_013", "english_fig_021"],
        help="Figure keys to transform",
    )
    parser.add_argument("--subfolder", default="english_only")
    args = parser.parse_args()

    src_figures_dir = DATASET_DIR / "figures" / args.subfolder
    src_gt_dir = DATASET_DIR / "groundtruth" / args.subfolder

    for transform_name, description in TRANSFORMS.items():
        # Output structure: transforms/<transform_name>/figures/<subfolder>/
        out_fig_dir = TRANSFORMS_DIR / transform_name / "figures" / args.subfolder
        out_gt_dir = TRANSFORMS_DIR / transform_name / "groundtruth" / args.subfolder
        out_fig_dir.mkdir(parents=True, exist_ok=True)
        out_gt_dir.mkdir(parents=True, exist_ok=True)

        transform_fn = TRANSFORM_FNS[transform_name]

        for fig_key in args.figures:
            src_img = src_figures_dir / f"{fig_key}.png"
            src_gt = src_gt_dir / f"{fig_key}.json"

            if not src_img.exists():
                print(f"  SKIP {fig_key} – image not found: {src_img}")
                continue

            # Apply transform
            img = Image.open(src_img)
            transformed = transform_fn(img)
            out_path = out_fig_dir / f"{fig_key}.png"
            transformed.save(out_path, format="PNG")

            # Copy groundtruth unchanged
            if src_gt.exists():
                shutil.copy2(src_gt, out_gt_dir / f"{fig_key}.json")

            print(f"  {transform_name}/{fig_key} – saved ({img.size[0]}x{img.size[1]})")

    # Write a manifest
    manifest = {
        "source_subfolder": args.subfolder,
        "figures": args.figures,
        "transforms": {k: v for k, v in TRANSFORMS.items()},
    }
    manifest_path = TRANSFORMS_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone. {len(args.figures)} figures x {len(TRANSFORMS)} transforms = {len(args.figures) * len(TRANSFORMS)} images")
    print(f"Output: {TRANSFORMS_DIR}")


if __name__ == "__main__":
    main()
