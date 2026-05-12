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
    "noise": "Gaussian noise (sigma=30)",
    "grayscale": "Convert to grayscale",
    "aspect_ratio": "Stretch width by 1.2x (mild distortion)",
    "low_contrast": "Reduce contrast by 50%",
}


def apply_jpeg_compression(img: Image.Image) -> Image.Image:
    """Apply heavy JPEG compression artifacts."""
    from io import BytesIO
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=15)
    buf.seek(0)
    return Image.open(buf).copy()


def apply_aspect_ratio(img: Image.Image) -> Image.Image:
    """Stretch width by 1.2x (mild horizontal distortion)."""
    w, h = img.size
    return img.resize((int(w * 1.2), h), Image.Resampling.LANCZOS)


def apply_low_contrast(img: Image.Image) -> Image.Image:
    """Reduce contrast by 50% (faded/washed out appearance)."""
    from PIL import ImageEnhance
    return ImageEnhance.Contrast(img).enhance(0.5)


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
    "noise": apply_noise,
    "grayscale": apply_grayscale,
    "aspect_ratio": apply_aspect_ratio,
    "low_contrast": apply_low_contrast,
}


def main():
    parser = argparse.ArgumentParser(description="Apply adversarial transforms to figures")
    parser.add_argument(
        "--figures", nargs="+",
        default=["english_fig_017", "english_fig_012", "english_fig_020", "english_fig_013", "english_fig_021"],
        help="Figure keys to transform (ignored if --adversarial-samples is set)",
    )
    parser.add_argument("--subfolder", default="english_only")
    parser.add_argument("--adversarial-samples", default=None,
                        help="Path to adversarial_samples.json for multi-subfolder transforms")
    args = parser.parse_args()

    # Build list of (subfolder, [fig_keys]) pairs
    if args.adversarial_samples:
        with open(args.adversarial_samples) as f:
            adv = json.load(f)
        subfolder_figures = list(adv["samples"].items())
    else:
        subfolder_figures = [(args.subfolder, args.figures)]

    total_count = 0
    for subfolder, fig_keys in subfolder_figures:
        src_figures_dir = DATASET_DIR / "figures" / subfolder
        src_gt_dir = DATASET_DIR / "groundtruth" / subfolder

        for transform_name, description in TRANSFORMS.items():
            out_fig_dir = TRANSFORMS_DIR / transform_name / "figures" / subfolder
            out_gt_dir = TRANSFORMS_DIR / transform_name / "groundtruth" / subfolder
            out_fig_dir.mkdir(parents=True, exist_ok=True)
            out_gt_dir.mkdir(parents=True, exist_ok=True)

            transform_fn = TRANSFORM_FNS[transform_name]

            for fig_key in fig_keys:
                src_img = src_figures_dir / f"{fig_key}.png"
                src_gt = src_gt_dir / f"{fig_key}.json"

                if not src_img.exists():
                    print(f"  SKIP {fig_key} – image not found: {src_img}")
                    continue

                out_path = out_fig_dir / f"{fig_key}.png"
                if out_path.exists():
                    continue

                img = Image.open(src_img)
                transformed = transform_fn(img)
                transformed.save(out_path, format="PNG")

                if src_gt.exists():
                    shutil.copy2(src_gt, out_gt_dir / f"{fig_key}.json")

                total_count += 1
                print(f"  {transform_name}/{subfolder}/{fig_key} – saved ({img.size[0]}x{img.size[1]})")

    # Update manifest
    all_figures = {}
    for subfolder, fig_keys in subfolder_figures:
        all_figures[subfolder] = fig_keys
    manifest = {
        "figures_by_subfolder": all_figures,
        "total_figures": sum(len(v) for v in all_figures.values()),
        "transforms": {k: v for k, v in TRANSFORMS.items()},
    }
    manifest_path = TRANSFORMS_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    total_figs = sum(len(v) for v in all_figures.values())
    print(f"\nDone. {total_figs} figures x {len(TRANSFORMS)} transforms = {total_figs * len(TRANSFORMS)} images ({total_count} new)")
    print(f"Output: {TRANSFORMS_DIR}")


if __name__ == "__main__":
    main()
