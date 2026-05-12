"""Scaling plot: parameter count vs MQM score per model family.

Output: thesis/main/figures/rq1/scaling_plot.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PDF_OUT = "thesis/main/figures/rq1/scaling_plot.pdf"
PNG_OUT = "output/evaluation-results/rq1/plots/scaling_plot.png"

# (params_B, MQM, label, family, color)
MODELS = [
    (4,    48.5, "Gemma 4B",   "Gemma",  "#E04E39"),
    (5.6,  57.4, "Phi-4",      "Phi",    "#888888"),
    (8,    66.7, "Qwen 8B",    "Qwen",   "#228833"),
    (12,   53.6, "Gemma 12B",  "Gemma",  "#E04E39"),
    (27,   58.8, "Gemma 27B",  "Gemma",  "#E04E39"),
    (30,   66.8, "Qwen 30B",   "Qwen",   "#228833"),
    (32,   70.4, "Qwen 32B",   "Qwen",   "#228833"),
    (109,  67.1, "LL Scout",   "LLaMA",  "#7B61FF"),
    (235,  70.8, "Qwen 235B",  "Qwen",   "#228833"),
    (400,  67.8, "LL Mav",     "LLaMA",  "#7B61FF"),
]

PROPRIETARY = [
    (500, 68.6, "Claude",  "#D97706"),
    (600, 72.7, "Gemini",  "#4285F4"),
    (700, 75.5, "GPT-5.2", "#10A37F"),
]

def main():
    plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.linewidth": 0.5})
    fig, ax = plt.subplots(figsize=(5, 3.5))

    # Open-source by family
    families = {}
    for p, m, l, f, c in MODELS:
        if f not in families: families[f] = {"x":[],"y":[],"c":c}
        families[f]["x"].append(p); families[f]["y"].append(m)

    for fam, d in families.items():
        ax.plot(d["x"], d["y"], color=d["c"], linewidth=1.5, alpha=0.7, marker="o",
                markersize=5, markeredgecolor="white", markeredgewidth=0.5, zorder=3, label=fam)
        for p, m, l, f, c in MODELS:
            if f == fam:
                ax.annotate(l, xy=(p*1.08, m+0.5), fontsize=5, color=d["c"], alpha=0.8)

    # Proprietary as separate markers
    for p, m, l, c in PROPRIETARY:
        ax.scatter(p, m, s=60, color=c, marker="*", edgecolors="white", linewidth=0.5, zorder=4)
        ax.annotate(l, xy=(p*1.05, m+0.5), fontsize=5.5, color=c, fontweight="bold")

    ax.axvspan(450, 800, alpha=0.04, color="#888888", zorder=0)
    ax.text(600, 46, "Proprietary\n(est. params)", ha="center", fontsize=5, color="#AAAAAA", style="italic")

    ax.set_xscale("log")
    ax.set_xlabel("Parameters (B, log scale)", fontsize=9)
    ax.set_ylabel("Atomic MQM", fontsize=9)
    ax.set_xlim(3, 900)
    ax.set_ylim(44, 80)
    ax.legend(loc="lower right", fontsize=6, framealpha=0.9, edgecolor="#CCCCCC")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888"); ax.spines["bottom"].set_color("#888888")
    ax.yaxis.grid(True, alpha=0.1, linewidth=0.4)
    plt.tight_layout()
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")

if __name__ == "__main__":
    main()
