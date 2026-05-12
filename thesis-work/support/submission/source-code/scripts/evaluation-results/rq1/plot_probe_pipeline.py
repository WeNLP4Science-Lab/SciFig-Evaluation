"""Redraw probe design workflow — UML activity diagram with subtle colours.

Flow: Corpus → LLM Seeder → Candidate Probes → Three-Expert Review → Probe Families (A1-A5).
Colour-coded by stage. Clean UML-inspired design.

Output: thesis/main/figures/probe_pipeline_v2.pdf
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

PDF_OUT = "thesis/main/figures/probe_pipeline_v2.pdf"
PNG_OUT = "output/evaluation-results/rq1/plots/probe_pipeline_v2.png"

# Colour scheme
C_INPUT = "#4477AA"     # blue - input/data
C_PROCESS = "#228833"   # green - processing
C_REVIEW = "#EE6677"    # red/pink - human review
C_OUTPUT = "#AA3377"    # purple - output families
C_ARROW = "#666666"
C_BG = "#FAFAFA"


def box(ax, x, y, w, h, text, color, fontsize=6, style="round,pad=0.01", alpha=0.12, textcolor=None):
    b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle=style,
                        facecolor=color, alpha=alpha,
                        edgecolor=color, linewidth=0.7)
    ax.add_patch(b)
    tc = textcolor if textcolor else color
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=tc, fontweight="medium", zorder=5,
            linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->,head_width=0.06,head_length=0.03",
                                color=C_ARROW, linewidth=0.7))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.03, label, ha="center", va="bottom",
                fontsize=4.5, color="#888888", style="italic")


def diamond(ax, x, y, size, text, color):
    s = size
    pts = np.array([[x, y+s], [x+s, y], [x, y-s], [x-s, y], [x, y+s]])
    ax.fill(pts[:,0], pts[:,1], color=color, alpha=0.1, zorder=2)
    ax.plot(pts[:,0], pts[:,1], color=color, linewidth=0.7, zorder=3)
    ax.text(x, y, text, ha="center", va="center", fontsize=5,
            color=color, fontweight="medium", zorder=5)


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 6,
    })

    fig, ax = plt.subplots(figsize=(6.5, 2.5))
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.05, 1.05)
    ax.axis("off")

    # Stage 1: Input corpus (left)
    box(ax, 0.08, 0.65, 0.12, 0.18,
        "Figure Corpus\n1,005 figures\nEN DE ZH BG", C_INPUT, fontsize=5.5)

    box(ax, 0.08, 0.25, 0.12, 0.14,
        "Prompt Templates\ncontra · inexist\nunanswerable", C_INPUT, fontsize=5, alpha=0.08)

    # Stage 2: LLM Seeder
    box(ax, 0.28, 0.5, 0.13, 0.16,
        "LLM Seeder\ncandidate\ngeneration", C_PROCESS, fontsize=5.5)

    arrow(ax, 0.14, 0.60, 0.215, 0.53)
    arrow(ax, 0.14, 0.30, 0.215, 0.47, "templates")

    # Stage 3: Candidate probes
    box(ax, 0.48, 0.5, 0.12, 0.14,
        "Candidate\nProbes", C_PROCESS, fontsize=5.5, alpha=0.08)

    arrow(ax, 0.345, 0.5, 0.42, 0.5, "per figure\nper family")

    # Stage 4: Three-expert review
    # Reviewers
    for i, (name, dy) in enumerate([("Researcher", 0.15), ("Consultant", 0.0), ("PhD Student", -0.15)]):
        box(ax, 0.63, 0.5 + dy, 0.09, 0.10,
            name, C_REVIEW, fontsize=5, alpha=0.08)

    arrow(ax, 0.54, 0.5, 0.585, 0.5)

    # Decision diamond
    diamond(ax, 0.76, 0.5, 0.06, "Accept\nRevise\nReject", C_REVIEW)

    arrow(ax, 0.675, 0.65, 0.72, 0.55)
    arrow(ax, 0.675, 0.5, 0.70, 0.5)
    arrow(ax, 0.675, 0.35, 0.72, 0.45)

    # Stage 5: Probe families output
    families = [
        ("A1", "Hallucination\ncontra · inexist · unans.", 0.82),
        ("A2", "Caption Bias\ncaption · mismatch", 0.62),
        ("A3", "Visual Degradation\nblur · noise · rotation", 0.42),
        ("A4", "Prompt Reverse\nconfirm · deny", 0.22),
        ("A5", "Misleading Det.\nfalse alarm", 0.05),
    ]

    for fam_id, desc, fy in families:
        box(ax, 0.92, fy, 0.14, 0.12,
            f"{fam_id}\n{desc}", C_OUTPUT, fontsize=4.5, alpha=0.10)

    # Arrow from diamond to families
    arrow(ax, 0.82, 0.5, 0.85, 0.82, "accepted")
    for _, _, fy in families:
        ax.plot([0.85, 0.85], [0.82, fy], color=C_ARROW, linewidth=0.4, alpha=0.4)
        ax.plot([0.85, 0.855], [fy, fy], color=C_ARROW, linewidth=0.4, alpha=0.4)

    # Stage labels at top
    stages = [
        (0.08, "Input"),
        (0.28, "Generation"),
        (0.48, "Candidates"),
        (0.68, "Expert Review"),
        (0.92, "Probe Families"),
    ]
    for x, label in stages:
        ax.text(x, 0.98, label, ha="center", va="top", fontsize=6,
                fontweight="bold", color="#444444")

    plt.tight_layout()
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
