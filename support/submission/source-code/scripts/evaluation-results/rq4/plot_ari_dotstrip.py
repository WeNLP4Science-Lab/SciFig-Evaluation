"""RQ4 Chart: A-R-I dot-strip (small multiples) with connecting lines.

Three aligned horizontal dot plots — one per A-R-I axis.
Models on Y-axis, thin lines connect each model's three dots.
Grey-and-pop: focal models in brand colour.

Output: thesis/main/figures/rq4/ari_dotstrip.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ARI_DATA = ROOT / "output" / "evaluation-results" / "rq4" / "ari.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq4" / "ari_dotstrip.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq4" / "plots" / "ari_dotstrip.png"

FOCAL = {
    "gemini-3.1-pro":  {"color": "#4285F4", "label": "Gemini 3.1 Pro"},
    "gpt-5.2":         {"color": "#10A37F", "label": "GPT-5.2"},
    "claude-opus-4.6": {"color": "#D97706", "label": "Claude Opus 4.6"},
    "qwen3-vl-32b":    {"color": "#6366F1", "label": "Qwen3-VL 32B"},
    "gemma3-4b-it":    {"color": "#E04E39", "label": "Gemma-3 4B"},
}

AXES = [
    ("admittance", "Admittance (A)"),
    ("resistance", "Resistance (R)"),
    ("inductance", "Inductance (I)"),
]


def main():
    data = json.load(open(ARI_DATA))
    models = data["models"]  # already sorted by A+R+I

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.5,
    })

    fig, axes = plt.subplots(1, 3, figsize=(7.5, 4.2), sharey=True)

    n = len(models)
    y = np.arange(n)

    for ax_idx, (key, title) in enumerate(AXES):
        ax = axes[ax_idx]

        vals = [m[key] for m in models]

        # Background dots (non-focal)
        for i, m in enumerate(models):
            if m["model"] in FOCAL:
                continue
            ax.scatter(m[key], y[i], s=30, color="#B0B0B0", alpha=0.5,
                       edgecolors="white", linewidth=0.3, zorder=2)

        # Focal dots on top
        for i, m in enumerate(models):
            if m["model"] not in FOCAL:
                continue
            fm = FOCAL[m["model"]]
            ax.scatter(m[key], y[i], s=55, color=fm["color"], alpha=0.9,
                       edgecolors="white", linewidth=0.6, zorder=4,
                       marker="o")

            # Value annotation
            offset = 0.04 if m[key] < 0.85 else -0.06
            ax.annotate(f"{m[key]:.2f}", xy=(m[key] + offset, y[i]),
                        fontsize=5.5, color=fm["color"], fontweight="bold",
                        va="center", ha="left" if offset > 0 else "right",
                        zorder=5)

        ax.set_title(title, fontsize=9, fontweight="bold", pad=8)
        ax.set_xlim(-0.05, 1.1)
        ax.axvline(0.5, color="#E0E0E0", linewidth=0.6, linestyle="--", zorder=0)

        # Grid
        ax.xaxis.grid(True, alpha=0.1, linewidth=0.4)
        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#888888")
        ax.spines["bottom"].set_color("#888888")
        ax.tick_params(colors="#555555", length=3)

        if ax_idx == 0:
            ax.set_yticks(y)
            ax.set_yticklabels([m["model_short"] for m in models], fontsize=7)
            # Colour focal model labels
            for i, m in enumerate(models):
                if m["model"] in FOCAL:
                    ax.get_yticklabels()[i].set_fontweight("bold")
                    ax.get_yticklabels()[i].set_color(FOCAL[m["model"]]["color"])

    # Draw connecting lines across subplots (using figure coordinates)
    for i, m in enumerate(models):
        if m["model"] not in FOCAL:
            continue
        fm = FOCAL[m["model"]]
        for ax_idx in range(2):
            key_l = AXES[ax_idx][0]
            key_r = AXES[ax_idx + 1][0]

            # Transform data coords to figure coords
            pt_l = axes[ax_idx].transData.transform((m[key_l], y[i]))
            pt_r = axes[ax_idx + 1].transData.transform((m[key_r], y[i]))

            # Convert to figure coords
            pt_l_fig = fig.transFigure.inverted().transform(pt_l)
            pt_r_fig = fig.transFigure.inverted().transform(pt_r)

            line = matplotlib.lines.Line2D(
                [pt_l_fig[0], pt_r_fig[0]], [pt_l_fig[1], pt_r_fig[1]],
                transform=fig.transFigure, color=fm["color"],
                linewidth=0.8, alpha=0.3, zorder=0,
            )
            fig.lines.append(line)

    plt.tight_layout()

    # Re-draw connecting lines after tight_layout (coordinates change)
    fig.lines.clear()
    fig.canvas.draw()
    for i, m in enumerate(models):
        if m["model"] not in FOCAL:
            continue
        fm = FOCAL[m["model"]]
        for ax_idx in range(2):
            key_l = AXES[ax_idx][0]
            key_r = AXES[ax_idx + 1][0]
            pt_l = axes[ax_idx].transData.transform((m[key_l], y[i]))
            pt_r = axes[ax_idx + 1].transData.transform((m[key_r], y[i]))
            pt_l_fig = fig.transFigure.inverted().transform(pt_l)
            pt_r_fig = fig.transFigure.inverted().transform(pt_r)
            line = matplotlib.lines.Line2D(
                [pt_l_fig[0], pt_r_fig[0]], [pt_l_fig[1], pt_r_fig[1]],
                transform=fig.transFigure, color=fm["color"],
                linewidth=0.8, alpha=0.25, zorder=0, linestyle="-",
            )
            fig.lines.append(line)

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
