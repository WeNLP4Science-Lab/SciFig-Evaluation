"""Extract atoms per language for the 25 parallel multi-language figures.

Creates atom files for each language annotation of each figure, enabling
cross-lingual ablation where the same figure is evaluated in BG, CN, DE, EN.

Output: atomic_mqm/atoms_crosslingual/{figure_key}_{language}.json

Usage:
    python3 scripts/experiments/extract_crosslingual_atoms.py
"""

import json
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

GT_DIR = ROOT / "Dataset" / "groundtruth" / "multi_language"
OUTPUT_DIR = ROOT / "atomic_mqm" / "atoms_crosslingual"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

# The 25 parallel figures
PARALLEL_FIGURES = [
    "multi_fig_001", "multi_fig_002", "multi_fig_006", "multi_fig_007",
    "multi_fig_008", "multi_fig_009", "multi_fig_010", "multi_fig_011",
    "multi_fig_012", "multi_fig_013", "multi_fig_014", "multi_fig_015",
    "multi_fig_016", "multi_fig_017", "multi_fig_018", "multi_fig_019",
    "multi_fig_020", "multi_fig_021", "multi_fig_022", "multi_fig_024",
    "multi_fig_025", "multi_fig_026", "multi_fig_040", "multi_fig_041",
    "multi_fig_042",
]

LANGUAGES = ["Bulgarian", "Chinese", "German", "English"]

LANG_SHORT = {
    "Bulgarian": "bg",
    "Chinese": "cn",
    "German": "de",
    "English": "en",
}

# Severity assignment based on content
def assign_severity(sentence, is_first=False):
    """Assign severity based on content type."""
    s = sentence.lower()
    # Critical: chart type, purpose, axis labels, data series names
    if is_first:
        return "critical"
    if any(kw in s for kw in ["chart", "diagram", "plot", "график", "图", "diagramm",
                               "purpose", "shows", "represents", "illustrates",
                               "показва", "展示", "zeigt", "darstellt"]):
        return "critical"
    # Important: values, ranges, scale types, data elements
    if any(kw in s for kw in ["axis", "scale", "range", "value", "percent",
                               "ос", "скала", "стойност", "процент",
                               "轴", "范围", "值", "百分",
                               "achse", "skala", "wert", "prozent"]):
        return "important"
    # Default to important for data content
    return "important"


def extract_atoms_from_annotation(text):
    """Split annotation into sentence-level atoms."""
    import re
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?。！？])\s*', text.strip())
    # Filter empty
    sentences = [s.strip() for s in sentences if s.strip()]

    atoms = []
    for i, sent in enumerate(sentences):
        atoms.append({
            "id": f"sent_{i}",
            "severity": assign_severity(sent, is_first=(i == 0)),
            "value": sent,
        })
    return atoms


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_atoms = 0

    for fig_key in PARALLEL_FIGURES:
        gt_file = GT_DIR / f"{fig_key}.json"
        if not gt_file.exists():
            logger.warning(f"No groundtruth for {fig_key}")
            continue

        gt = json.load(open(gt_file))

        for lang in LANGUAGES:
            # Find annotation for this language
            annotation = None
            for ann in gt.get("annotations", []):
                if ann.get("annotation_language") == lang:
                    annotation = ann["annotation"]
                    break

            if not annotation:
                logger.warning(f"No {lang} annotation for {fig_key}")
                continue

            atoms = extract_atoms_from_annotation(annotation)

            result = {
                "figure_key": fig_key,
                "figure_type": gt.get("figure_type", ""),
                "subfolder": "multi_language",
                "language": lang,
                "reference_description": annotation,
                "atoms": atoms,
            }

            out_file = OUTPUT_DIR / f"{fig_key}_{LANG_SHORT[lang]}.json"
            with open(out_file, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            total_files += 1
            total_atoms += len(atoms)
            logger.info(f"  {fig_key}_{LANG_SHORT[lang]}: {len(atoms)} atoms")

    logger.info(f"Done. {total_files} files, {total_atoms} total atoms")


if __name__ == "__main__":
    main()
