"""RQ4 Chart: A-R-I radar chart — behavioural profile per focal model.

Three axes: Admittance, Resistance, Inductance.
Grey-and-pop: focal models in brand colour, others as grey fill.

Output: thesis/main/figures/rq4/ari_radar.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ARI_DATA = ROOT / "output" / "evaluation-results" / "rq4" / "ari.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq4" / "ari_radar.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq4" / "plots" / "ari_radar.png"

FOCAL = [
    {"model": "gemini-3.1-pro",  "color": "#4285F4", "label": "Gemini 3.1 Pro"},
    {"model": "gpt-5.2",         "color": "#10A37F", "label": "GPT-5.2"},
    {"model": "claude-opus-4.6", "color": "#D97706", "label": "Claude Opus 4.6"},
    {"model": "qwen3-vl-32b",    "color": "#6366F1", "label": "Qwen3-VL 32B"},
    {"model": "gemma3-4b-it",    "color": "#E04E39", "label": "Gemma-3 4B"},
]

AXES = ["Admittance", "Resistance", "Inductance"]


def main():
    data = json.load(open(ARI_DATA))
    models = {m["model"]: m for m in data["models"]}

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
    })

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    n_axes = len(AXES)
    angles = np.linspace(0, 2 * np.pi, n_axes, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    # Configure axes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(AXES, fontsize=10, fontweight="bold")

    # Y-axis (radial)
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=6, color="#888888")
    ax.yaxis.grid(True, color="#DDDDDD", linewidth=0.5)
    ax.xaxis.grid(True, color="#CCCCCC", linewidth=0.5)

    # Background: all non-focal models as faint grey fills
    for m in data["models"]:
        if m["model"] in [f["model"] for f in FOCAL]:
            continue
        vals = [m["admittance"], m["resistance"], m["inductance"]]
        vals += vals[:1]
        ax.fill(angles, vals, alpha=0.03, color="#888888", zorder=1)
        ax.plot(angles, vals, linewidth=0.4, color="#BBBBBB", alpha=0.4, zorder=1)

    # Focal models
    for fm in FOCAL:
        m = models[fm["model"]]
        vals = [m["admittance"], m["resistance"], m["inductance"]]
        vals += vals[:1]

        ax.fill(angles, vals, alpha=0.08, color=fm["color"], zorder=2)
        ax.plot(angles, vals, linewidth=2.2, color=fm["color"], alpha=0.9,
                marker="o", markersize=5, markeredgecolor="white", markeredgewidth=0.8,
                label=fm["label"], zorder=3)

        # Value labels at each vertex
        for i, (angle, val) in enumerate(zip(angles[:-1], vals[:-1])):
            ha = "left" if angle < np.pi else "right"
            if abs(angle - np.pi/2) < 0.1:
                ha = "center"
            offset = 0.08
            ax.text(angle, val + offset, f"{val:.2f}",
                    fontsize=6, color=fm["color"], fontweight="bold",
                    ha=ha, va="center", zorder=4)

    # Legend outside
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05),
              ncol=3, fontsize=7, frameon=True, framealpha=0.95,
              edgecolor="#CCCCCC", handletextpad=0.4, columnspacing=1.0)

    plt.tight_layout()

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
