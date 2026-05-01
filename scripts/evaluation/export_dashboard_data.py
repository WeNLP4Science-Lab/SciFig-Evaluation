"""Export evaluation data for the dashboard UI.

Bundles evaluation JSONs + generation annotations + figure images into
a manifest JSON + copied images for the Vite dashboard.

Usage:
    python3 scripts/evaluation/export_dashboard_data.py --judge gpt-4o --judge gpt-4o-mini
    python3 scripts/evaluation/export_dashboard_data.py --judge gpt-4o --subfolder english_only
    python3 scripts/evaluation/export_dashboard_data.py --judge gpt-4o --samples samples.json --output manifest_sample.json
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GENERATION_DIR = ROOT / "output" / "generation"
FIGURES_DIR = ROOT / "Dataset" / "figures"
EVAL_BASE = ROOT / "output" / "evaluation"
DASHBOARD_PUBLIC = ROOT / "dashboard" / "public"

JUDGE_TYPES = ["reference_free", "reference_only", "reference_with_image"]
ALL_SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]


def _load_samples(samples_path):
    """Load samples.json and return a dict of {subfolder: set(fig_keys)}."""
    with open(samples_path) as f:
        data = json.load(f)
    result = {}
    for subfolder, types in data["samples"].items():
        keys = set()
        for fig_type, figs in types.items():
            keys.update(figs)
        result[subfolder] = keys
    return result


def export(judge_slugs, subfolder_filter=None, samples_path=None, output_name="manifest.json"):
    subfolders = [subfolder_filter] if subfolder_filter else ALL_SUBFOLDERS
    sample_keys = _load_samples(samples_path) if samples_path else None
    out_dir = DASHBOARD_PUBLIC / "data"
    img_dir = DASHBOARD_PUBLIC / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    # Discover models from evaluation dirs across all judges
    models = set()
    for judge_slug in judge_slugs:
        for jt in JUDGE_TYPES:
            jt_dir = EVAL_BASE / jt / judge_slug
            if jt_dir.exists():
                for m in jt_dir.iterdir():
                    if m.is_dir():
                        models.add(m.name)
    models = sorted(models)

    figures = []
    seen = set()

    for model_name in models:
        for subfolder in subfolders:
            gen_dir = GENERATION_DIR / model_name / subfolder
            if not gen_dir.exists():
                continue

            for gen_path in sorted(gen_dir.glob("*.json")):
                fig_key = gen_path.stem
                # Filter by samples if provided
                if sample_keys is not None:
                    if subfolder not in sample_keys or fig_key not in sample_keys[subfolder]:
                        continue
                combo_key = (model_name, subfolder, fig_key)
                if combo_key in seen:
                    continue
                seen.add(combo_key)

                with open(gen_path) as f:
                    gen = json.load(f)

                annotation = gen.get("model_annotation", "")
                if "model_annotations" in gen:
                    parts = []
                    for lang, text in sorted(gen["model_annotations"].items()):
                        parts.append(f"[{lang}]\n{text}")
                    annotation = "\n\n".join(parts)

                # Collect judge results keyed by judge model
                judges = {}
                for judge_slug in judge_slugs:
                    judge_results = {}
                    for jt in JUDGE_TYPES:
                        eval_path = EVAL_BASE / jt / judge_slug / model_name / subfolder / f"{fig_key}.json"
                        if eval_path.exists():
                            with open(eval_path) as f:
                                judge_results[jt] = json.load(f)
                    if judge_results:
                        judges[judge_slug] = judge_results

                if not judges:
                    continue

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
                    "model_name": model_name,
                    "figure_type": gen.get("figure_type", ""),
                    "annotation": annotation,
                    "caption": gen.get("caption", ""),
                    "paper_title": gen.get("paper_title", ""),
                    "subfolder": subfolder,
                    "figure_image": fig_rel,
                    "judges": judges,
                })

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "judge_models": judge_slugs,
        "models": models,
        "subfolders": sorted(set(f["subfolder"] for f in figures)),
        "total_figures": len(figures),
        "figures": figures,
    }

    manifest_path = out_dir / output_name
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(figures)} figure evaluations for {len(models)} models")
    print(f"Judges: {', '.join(judge_slugs)}")
    print(f"Manifest: {manifest_path}")
    print(f"Images: {img_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export evaluation data for dashboard")
    parser.add_argument("--judge", required=True, action="append", dest="judges",
                        help="Judge model slug (can specify multiple: --judge gpt-4o --judge gpt-4o-mini)")
    parser.add_argument("--subfolder", default=None, help="Filter to specific subfolder")
    parser.add_argument("--samples", default=None, help="Path to samples.json to filter figures")
    parser.add_argument("--output", default="manifest.json", help="Output filename (default: manifest.json)")
    args = parser.parse_args()
    export(args.judges, args.subfolder, args.samples, args.output)
