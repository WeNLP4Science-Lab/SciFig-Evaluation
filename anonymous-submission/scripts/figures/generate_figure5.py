"""Generate Figure 5: Cross-dimensional micro-scatter grid.

2x3 grid: rows = (MQM, Capability), cols = (Admittance, Resistance, Inductance)
Each model has consistent color + marker identity.

Output: paper/figures/figure5_scatter.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from model_identity import MODEL_IDENTITY, MODEL_ORDER

STATS_PATH = Path(__file__).resolve().parents[2] / "results" / "statistics" / "all_statistics.json"
OUT_PATH = Path(__file__).resolve().parents[2] / "paper" / "figures" / "figure5_scatter.pdf"

# Capability scores from thesis (placeholder)
CAPABILITY_SCORES = {
    "gpt-5.2": 78.4,
    "gemini-3.1-pro": 81.0,
    "llama4-maverick": 48.5,
    "qwen3-vl-235b-a22b": 58.4,
    "qwen3-vl-8b": 51.0,
    "qwen3-vl-30b-a3b": 40.6,
    "gemma3-27b-it": 27.2,
    "phi-4-multimodal": 8.6,
}


def load_data():
    with open(STATS_PATH) as f:
        stats = json.load(f)
    cis = stats["bootstrap_cis"]

    data = {}
    for mid in MODEL_ORDER:
        info = MODEL_IDENTITY[mid]
        mqm = cis["baseline_mqm"].get(mid, {}).get("mean")

        act_adm = cis.get("active_probes", {}).get("admittance", {}).get(mid, {})
        admittance = act_adm.get("admits", {}).get("mean") if act_adm else None

        resistance = cis.get("resistance", {}).get(mid, {}).get("mean")

        act_ind = cis.get("active_probes", {}).get("inductance", {}).get(mid, {})
        inductance = act_ind.get("correct_given_fab", {}).get("mean") if act_ind else None

        capability = CAPABILITY_SCORES.get(mid)

        if mqm is not None:
            data[mid] = {
                "mqm": mqm,
                "capability": capability,
                "admittance": admittance * 100 if admittance else None,
                "resistance": resistance,
                "inductance": inductance * 100 if inductance else None,
            }
    return data


def create_figure(data):
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 3.8), constrained_layout=True)

    x_dims = [
        ("mqm", "MQM Score"),
        ("capability", "Capability (%)"),
    ]
    y_dims = [
        ("admittance", "Admittance (%)"),
        ("resistance", "Resistance"),
        ("inductance", "Inductance (%)"),
    ]

    for row, (x_key, x_label) in enumerate(x_dims):
        for col, (y_key, y_label) in enumerate(y_dims):
            ax = axes[row, col]

            for mid in MODEL_ORDER:
                d = data[mid]
                info = MODEL_IDENTITY[mid]
                x_val = d.get(x_key)
                y_val = d.get(y_key)

                if x_val is not None and y_val is not None:
                    ax.scatter(x_val, y_val,
                              color=info["color"],
                              marker=info["marker"],
                              s=45, zorder=3, edgecolors="white", linewidth=0.3)

            # Diagonal guide
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.plot(xlim, ylim, color="#eeeeee", linewidth=0.7, linestyle="--", zorder=0)
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            ax.set_xlabel(x_label, fontsize=6.5)
            ax.set_ylabel(y_label, fontsize=6.5)
            ax.tick_params(labelsize=5.5)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.grid(alpha=0.1)

    # Legend
    legend_elements = []
    for mid in MODEL_ORDER:
        info = MODEL_IDENTITY[mid]
        legend_elements.append(
            Line2D([0], [0], marker=info["marker"], color="w",
                   markerfacecolor=info["color"], markersize=5,
                   label=info["label"], markeredgecolor="white", markeredgewidth=0.3)
        )

    fig.legend(handles=legend_elements, loc="lower center",
              ncol=4, fontsize=6, frameon=False,
              bbox_to_anchor=(0.5, -0.06))

    fig.savefig(str(OUT_PATH), dpi=300, bbox_inches="tight")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    data = load_data()
    create_figure(data)
