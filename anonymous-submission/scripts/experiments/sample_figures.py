"""Stratified random sampling of 100 figures from the 250-figure dataset.

Samples proportionally by chart type (bar/line/pie) with a fixed seed
for reproducibility.

Output: dataset/sampled_100.json

Usage:
    python sample_figures.py                # find best seed
    python sample_figures.py --seed 137     # use specific seed
"""

from __future__ import annotations

import json
import random
import argparse
from pathlib import Path
from collections import Counter

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import GROUNDTRUTH_DIR, DATASET_DIR

TARGET = 100
TARGET_DISTRIBUTION = {
    "Bar Chart": 40,
    "Line Plot": 40,
    "Pie Chart": 20,
}

def load_figures_by_type() -> dict[str, list[str]]:
    by_type = {"Bar Chart": [], "Line Plot": [], "Pie Chart": []}
    for gt_file in sorted(GROUNDTRUTH_DIR.glob("*.json")):
        fig_id = gt_file.stem
        with open(gt_file) as f:
            data = json.load(f)
        ft = data.get("figure_type", "")
        if ft in by_type:
            by_type[ft].append(fig_id)
    return by_type


def sample_with_seed(by_type: dict, seed: int) -> list[str]:
    rng = random.Random(seed)
    sampled = []
    for chart_type, target_n in TARGET_DISTRIBUTION.items():
        pool = list(by_type[chart_type])
        rng.shuffle(pool)
        sampled.extend(pool[:target_n])
    return sorted(sampled)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2111, help="Random seed")
    args = parser.parse_args()

    by_type = load_figures_by_type()
    print(f"Full dataset: {sum(len(v) for v in by_type.values())} figures")
    for ct, figs in by_type.items():
        print(f"  {ct}: {len(figs)}")
    print()

    seed = args.seed
    sampled = sample_with_seed(by_type, seed)

    # Chart type distribution
    type_counts = Counter()
    fig_types = {}
    for fig_id in sampled:
        with open(GROUNDTRUTH_DIR / f"{fig_id}.json") as f:
            gt = json.load(f)
        type_counts[gt["figure_type"]] += 1
        fig_types[fig_id] = gt["figure_type"]

    print(f"Seed: {seed}")
    print(f"Sampled {len(sampled)} figures:")
    for ct, count in sorted(type_counts.items()):
        print(f"  {ct}: {count}")

    # Inductance probe coverage
    probes_dir = DATASET_DIR / "adversarial" / "probes"
    inductance_all = []
    inductance_text = []
    inductance_numeric = []
    for fig_id in sampled:
        probe_path = probes_dir / f"{fig_id}.json"
        if probe_path.exists():
            with open(probe_path) as f:
                probe = json.load(f)
            ind = probe.get("selective_blur", {}).get("inductance", {})
            if ind and ind.get("question"):
                inductance_all.append(fig_id)
                if ind.get("candidate_type") == "text":
                    inductance_text.append(fig_id)
                else:
                    inductance_numeric.append(fig_id)

    print(f"\nInductance probes in sample:")
    print(f"  Total: {len(inductance_all)}")
    print(f"  Text-based: {len(inductance_text)}")
    print(f"  Numeric: {len(inductance_numeric)}")

    # Build per-figure metadata
    figures_detail = []
    for fig_id in sampled:
        entry = {
            "figure_id": fig_id,
            "figure_type": fig_types[fig_id],
        }

        probe_path = probes_dir / f"{fig_id}.json"
        if probe_path.exists():
            with open(probe_path) as f:
                probe = json.load(f)
            ind = probe.get("selective_blur", {}).get("inductance", {})
            adm = probe.get("selective_blur", {}).get("admittance", {})
            entry["has_inductance"] = bool(ind and ind.get("question"))
            entry["inductance_type"] = ind.get("candidate_type", "") if entry["has_inductance"] else ""
            entry["has_admittance"] = bool(adm and adm.get("question"))
        else:
            entry["has_inductance"] = False
            entry["inductance_type"] = ""
            entry["has_admittance"] = False

        figures_detail.append(entry)

    # Save
    output = {
        "sampling_method": "Stratified random sampling proportional to chart type distribution",
        "seed": seed,
        "total": len(sampled),
        "distribution": dict(type_counts),
        "inductance_coverage": {
            "total": len(inductance_all),
            "text_based": len(inductance_text),
            "numeric": len(inductance_numeric),
        },
        "figures": sampled,
        "figures_detail": figures_detail,
    }

    out_path = DATASET_DIR / "sampled_100.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
