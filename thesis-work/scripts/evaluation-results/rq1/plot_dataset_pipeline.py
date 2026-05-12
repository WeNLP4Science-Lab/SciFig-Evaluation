"""Redraw dataset construction pipeline — compact, premium.

4 language lanes flowing left to right: Venue → Papers → Figures → Annotation → GT.
Clean, minimal, colour-coded by language.

Output: thesis/main/figures/dataset_pipeline_v2.pdf
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

PDF_OUT = "thesis/main/figures/dataset_pipeline_v2.pdf"
PNG_OUT = "output/evaluation-results/rq1/plots/dataset_pipeline_v2.png"

LANGS = [
    {"name": "English",   "color": "#4477AA", "venue": "arXiv",           "papers": 225, "figs": 279, "anns": 476},
    {"name": "German",    "color": "#228833", "venue": "Wirtschaftsd.",   "papers": 84,  "figs": 86,  "anns": 267},
    {"name": "Chinese",   "color": "#EE6677", "venue": "CCL / ACL Anth.", "papers": 69, "figs": 159, "anns": 275},
    {"name": "Bulgarian", "color": "#AA3377", "venue": "ISA / UNWE",     "papers": 278, "figs": 304, "anns": 519},
]

STAGES = ["Native Venue", "Papers", "Figures", "Annotation", "Ground Truth"]
STAGE_X = [0.08, 0.27, 0.46, 0.65, 0.85]


def draw_box(ax, x, y, w, h, text, color, fontsize=5.5, bold=False, alpha=0.15):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle="round,pad=0.008",
                          facecolor=color, alpha=alpha,
                          edgecolor=color, linewidth=0.6)
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=color if alpha < 0.3 else "white", fontweight=weight, zorder=5)


def draw_arrow(ax, x1, y1, x2, y2, color):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->,head_width=0.08,head_length=0.04",
                                color=color, linewidth=0.6, alpha=0.5))


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 6,
    })

    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.axis("off")

    # Stage headers
    for i, (stage, x) in enumerate(zip(STAGES, STAGE_X)):
        ax.text(x, 0.97, stage, ha="center", va="top", fontsize=6.5,
                fontweight="bold", color="#444444")

    # Draw lanes
    n = len(LANGS)
    for i, lang in enumerate(LANGS):
        y = 0.78 - i * 0.22
        color = lang["color"]

        # Language label
        ax.plot([0.02, 0.02], [y - 0.06, y + 0.06], color=color, linewidth=2.5,
                solid_capstyle="round", zorder=3)

        # Stage boxes
        draw_box(ax, STAGE_X[0], y, 0.13, 0.10, lang["venue"], color, fontsize=5)
        draw_box(ax, STAGE_X[1], y, 0.10, 0.10, f'{lang["papers"]}\npapers', color, fontsize=5)
        draw_box(ax, STAGE_X[2], y, 0.10, 0.10, f'{lang["figs"]}\nfigures', color, fontsize=5)
        draw_box(ax, STAGE_X[3], y, 0.12, 0.10, f'Label Studio\n{lang["name"][:2].upper()}', color, fontsize=5)
        draw_box(ax, STAGE_X[4], y, 0.10, 0.10, f'{lang["anns"]}\nrecords', color, fontsize=5, alpha=0.25)

        # Arrows between stages
        gap = 0.015
        for j in range(len(STAGE_X) - 1):
            x1 = STAGE_X[j] + 0.055
            x2 = STAGE_X[j+1] - 0.055
            draw_arrow(ax, x1, y, x2, y, color)

    # Convergence bracket on the right
    y_top = 0.78 + 0.06
    y_bot = 0.78 - 3 * 0.22 - 0.06
    x_brace = 0.95
    ax.plot([x_brace, x_brace], [y_bot, y_top], color="#666666", linewidth=0.8)
    ax.plot([x_brace - 0.01, x_brace], [y_top, y_top], color="#666666", linewidth=0.8)
    ax.plot([x_brace - 0.01, x_brace], [y_bot, y_bot], color="#666666", linewidth=0.8)
    ax.text(x_brace + 0.02, (y_top + y_bot) / 2, "1,005\nfigures\n1,411\nannotations",
            ha="left", va="center", fontsize=5.5, color="#555555", fontweight="bold")

    plt.tight_layout()

    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
