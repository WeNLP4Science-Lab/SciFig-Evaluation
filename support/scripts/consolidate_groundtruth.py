"""Consolidate groundtruth files from one-per-annotation to one-per-figure.

Reads from Dataset/groundtruth/<folder>/ and writes consolidated files to
Dataset/groundtruth_consolidated/<folder>/<figure_key>.json.

Each consolidated file contains shared metadata at the top level and an
`annotations` array with all human annotations for that figure.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_DIR = BASE_DIR / "Dataset" / "groundtruth"
OUTPUT_DIR = BASE_DIR / "Dataset" / "groundtruth_consolidated"

# Metadata fields copied from the first annotation to the top level
METADATA_FIELDS = [
    "task_id",
    "arxiv_id",
    "paper_title",
    "paper_language",
    "figure_filename",
    "caption",
]

# Fields kept per annotation
ANNOTATION_FIELDS = [
    "annotation_id",
    "annotated_by",
    "annotation_language",
    "figure_type",
    "annotation",
]

# Folder name → regex that captures the figure key from the file stem
FOLDER_PATTERNS = {
    "bulgarian_only": None,   # 1:1 mapping, stem is the key
    "chinese_only": None,     # 1:1 mapping, stem is the key
    "german_only": None,      # 1:1 mapping, stem is the key
    "english_only": re.compile(r"^(english_fig_\d{3})(?:_\d+)?$"),
    "multi_language": re.compile(r"^(multi_fig_\d{3})_\d+_\w+$"),
}


def extract_figure_key(folder: str, stem: str) -> str:
    """Extract the figure key from a filename stem based on folder conventions."""
    pattern = FOLDER_PATTERNS[folder]
    if pattern is None:
        return stem
    m = pattern.match(stem)
    if m:
        return m.group(1)
    # Fallback: return stem as-is (shouldn't happen with well-formed data)
    print(f"  WARNING: could not parse figure key from '{stem}' in {folder}", file=sys.stderr)
    return stem


def majority_vote(values: list[str]) -> str:
    """Return the most common value. Ties broken by first occurrence order."""
    counts = Counter(values)
    max_count = max(counts.values())
    for v in values:
        if counts[v] == max_count:
            return v
    return values[0]  # unreachable, but satisfies type checkers


def consolidate_folder(folder: str) -> dict:
    """Consolidate all annotation files in a folder. Returns stats dict."""
    folder_path = INPUT_DIR / folder
    out_path = OUTPUT_DIR / folder
    out_path.mkdir(parents=True, exist_ok=True)

    # Read all JSON files and group by figure key
    groups: dict[str, list[dict]] = {}
    json_files = sorted(folder_path.glob("*.json"))

    for fpath in json_files:
        with open(fpath) as f:
            data = json.load(f)
        key = extract_figure_key(folder, fpath.stem)
        groups.setdefault(key, []).append(data)

    # Build consolidated files
    for key, annotations in sorted(groups.items()):
        first = annotations[0]
        consolidated = {field: first[field] for field in METADATA_FIELDS}
        consolidated["figure_type"] = majority_vote(
            [a["figure_type"] for a in annotations]
        )
        consolidated["annotations"] = [
            {field: a[field] for field in ANNOTATION_FIELDS}
            for a in annotations
        ]

        out_file = out_path / f"{key}.json"
        with open(out_file, "w") as f:
            json.dump(consolidated, f, indent=2, ensure_ascii=False)

    return {
        "input_files": len(json_files),
        "output_files": len(groups),
        "total_annotations": sum(len(v) for v in groups.values()),
    }


def main():
    print(f"Input:  {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    total_in = 0
    total_out = 0
    total_annotations = 0

    for folder in FOLDER_PATTERNS:
        if not (INPUT_DIR / folder).exists():
            print(f"  SKIP {folder} (not found)")
            continue

        stats = consolidate_folder(folder)
        total_in += stats["input_files"]
        total_out += stats["output_files"]
        total_annotations += stats["total_annotations"]

        print(
            f"  {folder:20s}  {stats['input_files']:4d} files → "
            f"{stats['output_files']:4d} consolidated  "
            f"({stats['total_annotations']} annotations)"
        )

    print()
    print(f"  {'TOTAL':20s}  {total_in:4d} files → {total_out:4d} consolidated  ({total_annotations} annotations)")


if __name__ == "__main__":
    main()
