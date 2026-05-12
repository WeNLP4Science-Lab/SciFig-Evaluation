"""Export adversarial transform images for the dashboard.

Copies original + transformed figure images and the manifest to the dashboard public dir.

Usage:
    python3 scripts/evaluation/export_adversarial_data.py
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TRANSFORMS_DIR = ROOT / "transforms"
DATASET_DIR = ROOT / "Dataset"
DASHBOARD_PUBLIC = ROOT / "dashboard" / "public"


def export():
    manifest_path = TRANSFORMS_DIR / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    img_dir = DASHBOARD_PUBLIC / "figures"
    transforms = list(manifest["transforms"].keys())
    figures_by_subfolder = manifest["figures_by_subfolder"]

    copied = 0
    for subfolder, fig_keys in figures_by_subfolder.items():
        # Copy original images
        orig_dir = img_dir / subfolder
        orig_dir.mkdir(parents=True, exist_ok=True)
        for fig_key in fig_keys:
            src = DATASET_DIR / "figures" / subfolder / f"{fig_key}.png"
            dest = orig_dir / f"{fig_key}.png"
            if src.exists() and not dest.exists():
                shutil.copy2(src, dest)
                copied += 1

        # Copy transformed images
        for transform in transforms:
            t_dir = img_dir / f"transform_{transform}" / subfolder
            t_dir.mkdir(parents=True, exist_ok=True)
            for fig_key in fig_keys:
                src = TRANSFORMS_DIR / transform / "figures" / subfolder / f"{fig_key}.png"
                dest = t_dir / f"{fig_key}.png"
                if src.exists() and not dest.exists():
                    shutil.copy2(src, dest)
                    copied += 1

    # Copy manifest
    out_manifest = DASHBOARD_PUBLIC / "data" / "adversarial_manifest.json"
    shutil.copy2(manifest_path, out_manifest)

    total_figs = sum(len(v) for v in figures_by_subfolder.values())
    print(f"Exported {total_figs} figures x {len(transforms)} transforms ({copied} images copied)")
    print(f"Manifest: {out_manifest}")


if __name__ == "__main__":
    export()
