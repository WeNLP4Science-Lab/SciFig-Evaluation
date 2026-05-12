"""Migrate 66 German-only figures (paper_language=English) to multi_language.

Maps german_fig_001..066 → multi_fig_112..177.
Restructures model outputs from single-annotation to multi-annotation format.
Removes originals from german_only after successful migration.

Usage:
    python3 scripts/migrate_german_to_multi.py [--dry-run]
"""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
GENERATION_DIR = ROOT / "output" / "generation"
GENERATION_EP_DIR = ROOT / "output" / "generation_english_prompt"

MODELS = ["gpt-5.2", "gemini-3.1-pro", "llama4-maverick", "gemma3-27b-it", "qwen3-vl-32b"]

# german_fig_001 → multi_fig_112, ..., german_fig_066 → multi_fig_177
MAPPING = {f"german_fig_{i:03d}": f"multi_fig_{i + 111:03d}" for i in range(1, 67)}


def migrate_groundtruth(src_key: str, dst_key: str, dry_run: bool) -> bool:
    src = GROUNDTRUTH_DIR / "german_only" / f"{src_key}.json"
    dst = GROUNDTRUTH_DIR / "multi_language" / f"{dst_key}.json"
    if not src.exists():
        print(f"  WARN: groundtruth {src} missing, skipping")
        return False
    if dry_run:
        print(f"  GT: {src.name} → {dst.name}")
        return True
    shutil.copy2(src, dst)
    # Update figure_key inside the JSON is not needed since groundtruth doesn't have it
    src.unlink()
    return True


def migrate_figure(src_key: str, dst_key: str, dry_run: bool) -> bool:
    src = FIGURES_DIR / "german_only" / f"{src_key}.png"
    dst = FIGURES_DIR / "multi_language" / f"{dst_key}.png"
    if not src.exists():
        print(f"  WARN: figure {src} missing, skipping")
        return False
    if dry_run:
        print(f"  FIG: {src.name} → {dst.name}")
        return True
    shutil.copy2(src, dst)
    src.unlink()
    return True


def migrate_native_output(model: str, src_key: str, dst_key: str, dry_run: bool) -> bool:
    """Migrate output/generation/{model}/german_only → multi_language.

    Transform: {"model_annotation": "..."} → {"model_annotations": {"German": "..."}}
    """
    src = GENERATION_DIR / model / "german_only" / f"{src_key}.json"
    dst = GENERATION_DIR / model / "multi_language" / f"{dst_key}.json"
    if not src.exists():
        return False
    if dry_run:
        print(f"  GEN/{model}: {src.name} → {dst.name}")
        return True

    with open(src) as f:
        data = json.load(f)

    # Transform single annotation to multi-annotation dict
    annotation = data.pop("model_annotation", "")
    data["model_annotations"] = {"German": annotation}
    data["figure_key"] = dst_key

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    src.unlink()
    return True


def migrate_english_prompt_output(model: str, src_key: str, dst_key: str, dry_run: bool) -> bool:
    """Migrate output/generation_english_prompt/{model}/german_only → multi_language.

    Transform: {"model_annotation": "...", "target_language": "German"}
            → {"model_annotations": {"German": "..."}, "target_languages": ["German"]}
    """
    src = GENERATION_EP_DIR / model / "german_only" / f"{src_key}.json"
    dst = GENERATION_EP_DIR / model / "multi_language" / f"{dst_key}.json"
    if not src.exists():
        return False
    if dry_run:
        print(f"  GEN_EP/{model}: {src.name} → {dst.name}")
        return True

    with open(src) as f:
        data = json.load(f)

    annotation = data.pop("model_annotation", "")
    target_lang = data.pop("target_language", "German")
    data["model_annotations"] = {target_lang: annotation}
    data["target_languages"] = [target_lang]
    data["figure_key"] = dst_key

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    src.unlink()
    return True


def main():
    parser = argparse.ArgumentParser(description="Migrate German-only figures to multi-language")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    args = parser.parse_args()

    print(f"Migrating {len(MAPPING)} figures from german_only → multi_language")
    if args.dry_run:
        print("=== DRY RUN ===\n")

    gt_ok = fig_ok = 0
    native_ok = {m: 0 for m in MODELS}
    ep_ok = {m: 0 for m in MODELS}

    for src_key, dst_key in sorted(MAPPING.items()):
        print(f"\n{src_key} → {dst_key}")
        if migrate_groundtruth(src_key, dst_key, args.dry_run):
            gt_ok += 1
        if migrate_figure(src_key, dst_key, args.dry_run):
            fig_ok += 1
        for model in MODELS:
            if migrate_native_output(model, src_key, dst_key, args.dry_run):
                native_ok[model] += 1
            if migrate_english_prompt_output(model, src_key, dst_key, args.dry_run):
                ep_ok[model] += 1

    print(f"\n{'=' * 50}")
    print(f"Summary:")
    print(f"  Groundtruth migrated: {gt_ok}/{len(MAPPING)}")
    print(f"  Figures migrated:     {fig_ok}/{len(MAPPING)}")
    for model in MODELS:
        print(f"  Native output ({model}): {native_ok[model]}/{len(MAPPING)}")
        print(f"  English prompt ({model}): {ep_ok[model]}/{len(MAPPING)}")


if __name__ == "__main__":
    main()
