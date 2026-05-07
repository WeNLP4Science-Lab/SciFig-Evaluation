"""Discussion Chart 1: A vs R scatter with I as dot size.

Maps the theoretical A-R-I space (Figure 4.1) with real model data.
Quadrant labels match the design chapter archetypes.
Brand colours for focal models, grey for others.

Output: thesis/main/figures/discussion/ari_scatter.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ARI_DATA = ROOT / "output" / "evaluation-results" / "rq4" / "ari.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "discussion" / "ari_scatter.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq4" / "plots" / "ari_scatter.png"

FOCAL = {
    "gemini-3.1-pro":  {"color": "#4285F4", "label": "Gemini"},
    "gpt-5.2":         {"color": "#10A37F", "label": "GPT-5.2"},
    "claude-opus-4.6": {"color": "#D97706", "label": "Claude"},
    "qwen3-vl-32b":    {"color": "#6366F1", "label": "Qwen 32B"},
    "llama4-scout":    {"color": "#7B61FF", "label": "LLaMA Scout"},
    "gemma3-4b-it":    {"color": "#E04E39", "label": "Gemma 4B"},
    "phi-4-multimodal": {"color": "#888888", "label": "Phi-4"},
}

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2", "gemini-3.1-pro": "Gemini",
    "claude-opus-4.6": "Claude", "qwen3-vl-235b-a22b": "Qw-235B",
    "qwen3-vl-32b": "Qw-32B", "qwen3-vl-30b-a3b": "Qw-30B",
    "qwen3-vl-8b": "Qw-8B", "llama4-maverick": "LL-Mav",
    "llama4-scout": "LL-Scout", "gemma3-27b-it": "Gma-27B",
    "phi-4-multimodal": "Phi-4", "gemma3-12b-it": "Gma-12B",
    "gemma3-4b-it": "Gma-4B",
}


def main():
    data = json.load(open(ARI_DATA))
    models = data["models"]

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.5,
    })

    fig, ax = plt.subplots(figsize=(5.5, 5))

    # Quadrant shading
    ax.axhspan(0.5, 1.05, xmin=0.5/1.1*1.0, alpha=0.04, color="#228833", zorder=0)  # top-right: faithful
    ax.axhspan(-0.05, 0.5, xmax=0.5/1.1*1.0, alpha=0.04, color="#CC3311", zorder=0)  # bottom-left: fabricator

    # Quadrant dividers
    ax.axhline(0.5, color="#CCCCCC", linewidth=0.6, linestyle="--", zorder=0)
    ax.axvline(0.5, color="#CCCCCC", linewidth=0.6, linestyle="--", zorder=0)

    # Quadrant labels
    ax.text(0.8, 0.95, "Faithful\nreader", fontsize=7, color="#228833",
            ha="center", va="top", style="italic", alpha=0.7)
    ax.text(0.15, 0.05, "Silent\nfabricator", fontsize=7, color="#CC3311",
            ha="center", va="bottom", style="italic", alpha=0.7)
    ax.text(0.8, 0.05, "Honest but\ncredulous", fontsize=7, color="#CCBB44",
            ha="center", va="bottom", style="italic", alpha=0.6)
    ax.text(0.15, 0.95, "Over-confident\ninferrer", fontsize=7, color="#AA3377",
            ha="center", va="top", style="italic", alpha=0.6)

    # Target zone
    from matplotlib.patches import FancyBboxPatch
    target = FancyBboxPatch((0.6, 0.7), 0.4, 0.3, boxstyle="round,pad=0.02",
                             facecolor="#228833", alpha=0.06, edgecolor="#228833",
                             linewidth=0.8, linestyle="--", zorder=0)
    ax.add_patch(target)
    ax.text(0.95, 0.97, "target", fontsize=6, color="#228833", ha="right", va="top", alpha=0.5)

    # Plot non-focal models
    for m in models:
        if m["model"] in FOCAL:
            continue
        size = m["inductance"] * 200 + 20
        ax.scatter(m["admittance"], m["resistance"], s=size,
                   color="#909090", alpha=0.45, edgecolors="white", linewidth=0.3, zorder=2)
        ax.annotate(MODEL_SHORT.get(m["model"], m["model"]),
                    xy=(m["admittance"] + 0.015, m["resistance"] - 0.02),
                    fontsize=5, color="#777777", va="top", zorder=2)

    # Plot focal models
    for m in models:
        if m["model"] not in FOCAL:
            continue
        fm = FOCAL[m["model"]]
        size = m["inductance"] * 250 + 30
        ax.scatter(m["admittance"], m["resistance"], s=size,
                   color=fm["color"], alpha=0.85, edgecolors="white",
                   linewidth=0.8, zorder=4)
        # Label with offset to avoid overlap
        offx, offy = 0.02, -0.025
        if m["model"] == "gemini-3.1-pro":
            offx, offy = -0.02, 0.03
        elif m["model"] == "gpt-5.2":
            offx, offy = 0.03, 0.02
        elif m["model"] == "claude-opus-4.6":
            offx, offy = 0.03, 0.02
        ax.annotate(f"{fm['label']}\n({m['inductance']:.1f})",
                    xy=(m["admittance"] + offx, m["resistance"] + offy),
                    fontsize=6.5, fontweight="bold", color=fm["color"],
                    va="center", zorder=5)

    ax.set_xlabel("Admittance (A)", fontsize=10, fontweight="medium", labelpad=8)
    ax.set_ylabel("Resistance (R)", fontsize=10, fontweight="medium", labelpad=8)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.02)

    # Size legend for Inductance
    for i_val, label in [(0.2, "I=0.2"), (0.6, "I=0.6"), (1.0, "I=1.0")]:
        ax.scatter([], [], s=i_val * 250 + 30, color="#B0B0B0", alpha=0.5,
                   edgecolors="white", label=label)
    ax.legend(loc="lower right", fontsize=6, framealpha=0.9, edgecolor="#CCCCCC",
              title="Inductance", title_fontsize=6.5, handletextpad=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")
    ax.tick_params(colors="#555555", length=3)

    plt.tight_layout()

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
