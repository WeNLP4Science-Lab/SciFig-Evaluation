"""Export the dataset (groundtruth + figure images) for the dashboard UI.

Scans all subfolders in Dataset/groundtruth/, extracts metadata and
annotations from each groundtruth JSON, copies figure images, and writes
a dataset.json manifest for the Vite dashboard.

Usage:
    python3 scripts/evaluation/export_dataset.py
"""

from dotenv import load_dotenv

import json
import shutil
from datetime import datetime
from pathlib import Path

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
DASHBOARD_PUBLIC = ROOT / "dashboard" / "public"

ALL_SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]
TRANSFORMS_DIR = ROOT / "transforms"


def export():
    out_dir = DASHBOARD_PUBLIC / "data"
    img_dir = DASHBOARD_PUBLIC / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    figures = []
    subfolder_counts = {}

    for subfolder in ALL_SUBFOLDERS:
        gt_dir = GROUNDTRUTH_DIR / subfolder
        if not gt_dir.exists():
            print(f"  Skipping {subfolder} (not found)")
            continue

        count = 0
        for gt_path in sorted(gt_dir.glob("*.json")):
            fig_key = gt_path.stem

            with open(gt_path) as f:
                gt = json.load(f)

            # Extract annotations
            annotations = []
            for ann in gt.get("annotations", []):
                annotations.append({
                    "annotation_language": ann.get("annotation_language", ""),
                    "annotation": ann.get("annotation", ""),
                    "annotated_by": ann.get("annotated_by"),
                    "figure_type": ann.get("figure_type", ""),
                })

            # Copy figure image
            fig_src = FIGURES_DIR / subfolder / f"{fig_key}.png"
            fig_rel = f"figures/{subfolder}/{fig_key}.png"
            if fig_src.exists():
                dest = img_dir / subfolder / f"{fig_key}.png"
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(fig_src, dest)

            figures.append({
                "figure_key": fig_key,
                "subfolder": subfolder,
                "paper_title": gt.get("paper_title", ""),
                "paper_language": gt.get("paper_language", ""),
                "caption": gt.get("caption", ""),
                "figure_type": gt.get("figure_type", ""),
                "figure_image": fig_rel,
                "annotations": annotations,
            })
            count += 1

        subfolder_counts[subfolder] = count
        print(f"  {subfolder}: {count} figures")

    # Include adversarial transforms
    if TRANSFORMS_DIR.exists():
        for transform_dir in sorted(TRANSFORMS_DIR.iterdir()):
            if not transform_dir.is_dir():
                continue
            transform_name = transform_dir.name
            gt_base = transform_dir / "groundtruth"
            fig_base = transform_dir / "figures"
            if not gt_base.exists():
                continue

            for sub_dir in sorted(gt_base.iterdir()):
                if not sub_dir.is_dir():
                    continue
                subfolder_key = f"transform_{transform_name}"
                count = 0
                for gt_path in sorted(sub_dir.glob("*.json")):
                    fig_key = gt_path.stem
                    with open(gt_path) as f:
                        gt = json.load(f)

                    annotations = []
                    for ann in gt.get("annotations", []):
                        annotations.append({
                            "annotation_language": ann.get("annotation_language", ""),
                            "annotation": ann.get("annotation", ""),
                            "annotated_by": ann.get("annotated_by"),
                            "figure_type": ann.get("figure_type", ""),
                        })

                    # Copy transformed figure image
                    fig_src = fig_base / sub_dir.name / f"{fig_key}.png"
                    fig_rel = f"figures/{subfolder_key}/{fig_key}.png"
                    if fig_src.exists():
                        dest = img_dir / subfolder_key / f"{fig_key}.png"
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        if not dest.exists():
                            shutil.copy2(fig_src, dest)

                    figures.append({
                        "figure_key": fig_key,
                        "subfolder": subfolder_key,
                        "paper_title": gt.get("paper_title", ""),
                        "paper_language": gt.get("paper_language", ""),
                        "caption": gt.get("caption", ""),
                        "figure_type": gt.get("figure_type", ""),
                        "figure_image": fig_rel,
                        "annotations": annotations,
                    })
                    count += 1

                if count:
                    subfolder_counts[subfolder_key] = count
                    print(f"  {subfolder_key}: {count} figures")

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "subfolders": sorted(subfolder_counts.keys()),
        "subfolder_counts": subfolder_counts,
        "figures": figures,
    }

    manifest_path = out_dir / "dataset.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = len(figures)
    print(f"\nExported {total} figures across {len(subfolder_counts)} subfolders")
    print(f"Manifest: {manifest_path}")
    print(f"Images:   {img_dir}")


if __name__ == "__main__":
    export()
