"""Renumber remaining german_only files to a contiguous sequence.

After migration, german_only has german_fig_067..152 (86 files).
This script renumbers them to german_fig_001..086.

To avoid collisions (renaming 067→001 while 001 might still exist),
we first rename to a temporary prefix, then to the final names.

Usage:
    python3 scripts/renumber_german.py [--dry-run]
"""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth" / "german_only"
FIGURES_DIR = ROOT / "Dataset" / "figures" / "german_only"
GENERATION_DIR = ROOT / "output" / "generation"
GENERATION_EP_DIR = ROOT / "output" / "generation_english_prompt"

MODELS = ["gpt-5.2", "gemini-3.1-pro", "llama4-maverick", "gemma3-27b-it", "qwen3-vl-32b"]


def _collect_dirs():
    """All directories containing german_only files to rename."""
    dirs = [
        (GROUNDTRUTH_DIR, ".json"),
        (FIGURES_DIR, ".png"),
    ]
    for model in MODELS:
        dirs.append((GENERATION_DIR / model / "german_only", ".json"))
        dirs.append((GENERATION_EP_DIR / model / "german_only", ".json"))
    return dirs


def main():
    parser = argparse.ArgumentParser(description="Renumber german_only files to contiguous sequence")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Discover existing keys from groundtruth
    existing = sorted(p.stem for p in GROUNDTRUTH_DIR.glob("german_fig_*.json"))
    print(f"Found {len(existing)} german_only figures: {existing[0]} .. {existing[-1]}")

    # Build mapping: old_key → new_key
    mapping = {}
    for new_num, old_key in enumerate(existing, start=1):
        new_key = f"german_fig_{new_num:03d}"
        if old_key != new_key:
            mapping[old_key] = new_key

    print(f"Need to rename {len(mapping)} files (per directory)")
    if not mapping:
        print("Nothing to rename — already contiguous.")
        return

    dirs = _collect_dirs()

    if args.dry_run:
        print("\n=== DRY RUN ===")
        for old_key, new_key in sorted(mapping.items()):
            print(f"  {old_key} → {new_key}")
        print(f"\nAcross {len(dirs)} directories")
        return

    # Phase 1: rename to temporary names to avoid collisions
    tmp_prefix = "_tmp_rename_"
    for directory, ext in dirs:
        if not directory.exists():
            continue
        for old_key in mapping:
            src = directory / f"{old_key}{ext}"
            if src.exists():
                tmp = directory / f"{tmp_prefix}{old_key}{ext}"
                src.rename(tmp)

    # Phase 2: rename from temporary to final names, updating figure_key in JSONs
    renamed = 0
    for directory, ext in dirs:
        if not directory.exists():
            continue
        for old_key, new_key in mapping.items():
            tmp = directory / f"{tmp_prefix}{old_key}{ext}"
            dst = directory / f"{new_key}{ext}"
            if not tmp.exists():
                continue
            if ext == ".json":
                # Update figure_key inside JSON if present
                with open(tmp) as f:
                    data = json.load(f)
                if "figure_key" in data:
                    data["figure_key"] = new_key
                    with open(tmp, "w") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
            tmp.rename(dst)
            renamed += 1

    print(f"Renamed {renamed} files across {len(dirs)} directories")

    # Verify
    final = sorted(p.stem for p in GROUNDTRUTH_DIR.glob("german_fig_*.json"))
    expected = [f"german_fig_{i:03d}" for i in range(1, len(existing) + 1)]
    if final == expected:
        print(f"Verified: german_fig_001 .. german_fig_{len(existing):03d}")
    else:
        print(f"WARNING: verification failed!")
        print(f"  Expected: {expected[0]}..{expected[-1]}")
        print(f"  Got: {final[0]}..{final[-1]}")


if __name__ == "__main__":
    main()
