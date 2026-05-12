"""Redraw corpus composition chart — compact vertical layout.

Stacked horizontal bars for figure-type distribution per language.
Compact summary stats below. Designed to sit side-by-side with pipeline.

Output: thesis/main/figures/corpus_composition_v2.pdf
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PDF_OUT = "thesis/main/figures/corpus_composition_v2.pdf"
PNG_OUT = "output/evaluation-results/rq1/plots/corpus_composition_v2.png"

LANGUAGES = ["English", "German", "Chinese", "Bulgarian", "Multi-language"]
LANG_COLORS_BG = ["#4477AA", "#228833", "#EE6677", "#AA3377", "#666666"]

# Figure type counts per language
DATA = {
    "Line plot": [145, 44, 61, 104, 117],
    "Bar chart": [85, 41, 76, 140, 55],
    "Pie chart": [47, 1, 15, 56, 5],
    "Other":     [2, 0, 7, 4, 0],
}
TOTALS = [279, 86, 159, 304, 177]

TYPE_COLORS = ["#4477AA", "#EE6677", "#228833", "#CCBB44"]
TYPE_LABELS = list(DATA.keys())


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 7,
        "axes.linewidth": 0.4,
    })

    fig, ax = plt.subplots(figsize=(3.2, 3.6))

    y = np.arange(len(LANGUAGES))
    left = np.zeros(len(LANGUAGES))

    for j, (typ, counts) in enumerate(DATA.items()):
        bars = ax.barh(y, counts, left=left, height=0.55,
                       color=TYPE_COLORS[j], alpha=0.85,
                       edgecolor="white", linewidth=0.3,
                       label=typ)
        # In-bar labels for segments > 30
        for i, (c, l) in enumerate(zip(counts, left)):
            if c > 30:
                ax.text(l + c / 2, y[i], str(c), ha="center", va="center",
                        fontsize=5.5, color="white", fontweight="bold")
        left += counts

    # Total annotations at end
    for i, total in enumerate(TOTALS):
        ax.text(total + 3, y[i], f"{total}", ha="left", va="center",
                fontsize=6, color="#555555", fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(LANGUAGES, fontsize=7)
    ax.set_xlabel("Figures", fontsize=7)
    ax.set_xlim(0, 340)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")
    ax.tick_params(colors="#555555", length=2)

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1),
              ncol=4, fontsize=5.5, frameon=False, handletextpad=0.3,
              columnspacing=0.6, handlelength=1.0)

    # Summary line below
    ax.text(0.5, -0.22, "1,005 figures  ·  1,411 annotations  ·  8 annotators  ·  5 subsets  ·  4 languages",
            transform=ax.transAxes, ha="center", fontsize=5.5, color="#777777")

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
