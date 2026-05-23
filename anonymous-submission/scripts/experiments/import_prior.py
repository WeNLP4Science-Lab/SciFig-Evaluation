"""Import prior description outputs into the 250-figure structure.

Maps fig_XXX to the original english_fig_XXX / multi_fig_XXX using the
original_file field in groundtruth JSONs.

For multi-language figures, extracts only the English description.

Usage:
    python import_prior.py                     # all models with prior outputs
    python import_prior.py --models gpt-5.2 gemma3-27b-it
    python import_prior.py --dry-run           # preview only
"""

from __future__ import annotations

import json
import argparse
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    MODELS, DESCRIPTIONS_DIR, PRIOR_GENERATION_DIR,
    load_figure_mapping, get_thesis_subfolder,
)


def import_model(model_name: str, mapping: dict, dry_run: bool = False):
    model_cfg = MODELS[model_name]
    thesis_name = model_cfg.get("thesis_name")
    if not thesis_name:
        print(f"  {model_name}: no thesis outputs (needs fresh generation)")
        return 0, 0

    out_dir = DESCRIPTIONS_DIR / model_name
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    imported, missing = 0, 0

    for acl_id, thesis_key in sorted(mapping.items()):
        subfolder = get_thesis_subfolder(thesis_key)
        thesis_path = PRIOR_GENERATION_DIR / thesis_name / subfolder / f"{thesis_key}.json"

        if not thesis_path.exists():
            print(f"    {acl_id} -> {thesis_key}: NOT FOUND")
            missing += 1
            continue

        out_path = out_dir / f"{acl_id}.json"
        if out_path.exists():
            imported += 1
            continue

        with open(thesis_path) as f:
            thesis_data = json.load(f)

        # Extract description text
        if "model_annotation" in thesis_data:
            description = thesis_data["model_annotation"]
        elif "model_annotations" in thesis_data:
            # Multi-language: take English
            annotations = thesis_data["model_annotations"]
            description = annotations.get("English", "")
            if not description:
                # Fallback to first available
                description = next(iter(annotations.values()), "")
        else:
            print(f"    {acl_id}: no annotation field found")
            missing += 1
            continue

        # Build output
        result = {
            "figure_id": acl_id,
            "model_name": model_name,
            "description": description,
            "figure_type": thesis_data.get("figure_type", ""),
        }

        if not dry_run:
            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        imported += 1

    return imported, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", help="Specific models to import")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mapping = load_figure_mapping()
    print(f"Loaded {len(mapping)} ACL-to-thesis figure mappings")
    print("-" * 60)

    model_names = args.models or [
        m for m, cfg in MODELS.items() if cfg.get("thesis_name")
    ]

    for model_name in model_names:
        if model_name not in MODELS:
            print(f"  {model_name}: unknown model, skipping")
            continue

        print(f"\n{model_name}:")
        imported, missing = import_model(model_name, mapping, args.dry_run)
        print(f"  Imported: {imported}, Missing: {missing}")

    print("\n" + "-" * 60)
    if args.dry_run:
        print("DRY RUN — no files written")
    else:
        print(f"Output: {DESCRIPTIONS_DIR}")


if __name__ == "__main__":
    main()
