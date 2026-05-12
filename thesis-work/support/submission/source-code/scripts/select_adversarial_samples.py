"""Select a balanced subset of sample figures for adversarial robustness testing.

Selects 30 figures (10 per figure type) from the 120 evaluation samples,
balanced across languages. Uses a fixed random seed for reproducibility.

Usage:
    python3 scripts/select_adversarial_samples.py
    python3 scripts/select_adversarial_samples.py --count-per-type 10 --seed 42
"""

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def select_samples(samples_path, count_per_type=10, seed=42):
    with open(samples_path) as f:
        data = json.load(f)

    random.seed(seed)

    # Collect all figures by figure type across all subfolders
    by_type = {"line_plot": [], "bar_chart": [], "pie_chart": []}

    for subfolder, types in data["samples"].items():
        for fig_type, figs in types.items():
            # Normalize pie_chart variants
            norm_type = "pie_chart" if "pie_chart" in fig_type else fig_type
            if norm_type in by_type:
                for fig_key in figs:
                    by_type[norm_type].append((subfolder, fig_key))

    selected = {}

    for fig_type, candidates in by_type.items():
        # Group by subfolder for balanced selection
        by_subfolder = {}
        for subfolder, fig_key in candidates:
            by_subfolder.setdefault(subfolder, []).append(fig_key)

        # Determine how many per subfolder (round-robin balanced)
        subfolders = sorted(by_subfolder.keys())
        picks = []
        remaining = count_per_type

        # Allocate proportionally, at least 1 per subfolder if possible
        per_sub = max(1, remaining // len(subfolders))
        for sub in subfolders:
            available = by_subfolder[sub]
            random.shuffle(available)
            n = min(per_sub, len(available), remaining)
            for fig_key in available[:n]:
                picks.append((sub, fig_key))
                remaining -= 1
            if remaining <= 0:
                break

        # Fill any remaining slots from subfolders with leftover figures
        if remaining > 0:
            all_remaining = []
            picked_keys = {(s, k) for s, k in picks}
            for sub in subfolders:
                for fig_key in by_subfolder[sub]:
                    if (sub, fig_key) not in picked_keys:
                        all_remaining.append((sub, fig_key))
            random.shuffle(all_remaining)
            picks.extend(all_remaining[:remaining])

        for subfolder, fig_key in picks:
            selected.setdefault(subfolder, []).append(fig_key)

    # Build output
    adversarial_samples = {
        "description": "Subset of evaluation samples selected for adversarial robustness testing.",
        "selection": {
            "method": "Balanced random sampling across figure types and languages",
            "seed": seed,
            "count_per_type": count_per_type,
            "total": sum(len(v) for v in selected.values()),
        },
        "transforms": [
            "jpeg_compression",
            "low_resolution",
            "gaussian_blur",
            "noise",
            "grayscale",
        ],
        "samples": {subfolder: sorted(figs) for subfolder, figs in sorted(selected.items())},
    }

    return adversarial_samples


def main():
    parser = argparse.ArgumentParser(description="Select adversarial test samples")
    parser.add_argument("--samples", default=str(ROOT / "samples.json"))
    parser.add_argument("--count-per-type", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default=str(ROOT / "adversarial_samples.json"))
    args = parser.parse_args()

    result = select_samples(args.samples, args.count_per_type, args.seed)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Selected {result['selection']['total']} figures for adversarial testing:")
    for subfolder, figs in result["samples"].items():
        print(f"  {subfolder}: {len(figs)} figures")
    print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
