"""Discussion Chart 2: Rank flow (bump chart) across RQ1 → RQ3 → RQ4.

Shows how model rankings shift across description, comprehension, and behaviour.
Highlights rank inversions. Grey-and-pop design.

Output: thesis/main/figures/discussion/rank_flow.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
LEADERBOARD = ROOT / "output" / "evaluation-results" / "rq1" / "leaderboard.json"
CAPABILITY = ROOT / "output" / "evaluation-results" / "rq3" / "capability.json"
ARI_DATA = ROOT / "output" / "evaluation-results" / "rq4" / "ari.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "discussion" / "rank_flow.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq4" / "plots" / "rank_flow.png"

FOCAL = {
    "gemini-3.1-pro":  {"color": "#4285F4", "label": "Gemini"},
    "gpt-5.2":         {"color": "#10A37F", "label": "GPT-5.2"},
    "claude-opus-4.6": {"color": "#D97706", "label": "Claude"},
    "qwen3-vl-32b":    {"color": "#6366F1", "label": "Qwen 32B"},
    "llama4-scout":    {"color": "#7B61FF", "label": "LLaMA Scout"},
    "gemma3-4b-it":    {"color": "#E04E39", "label": "Gemma 4B"},
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
    lb = json.load(open(LEADERBOARD))
    cap = json.load(open(CAPABILITY))
    ari = json.load(open(ARI_DATA))

    # Build rankings
    # RQ1: by avg_Overall
    rq1_order = [m["model"] for m in lb]  # already sorted
    rq1_rank = {m: i + 1 for i, m in enumerate(rq1_order)}

    # RQ3: by avg_overall
    rq3_order = [m["model"] for m in sorted(cap["models"], key=lambda x: -x.get("avg_overall", 0))]
    rq3_rank = {m: i + 1 for i, m in enumerate(rq3_order)}

    # RQ4: by A+R+I sum
    rq4_order = [m["model"] for m in sorted(ari["models"], key=lambda x: -(x["admittance"] + x["resistance"] + x["inductance"]))]
    rq4_rank = {m: i + 1 for i, m in enumerate(rq4_order)}

    # Common models
    all_models = sorted(set(rq1_rank.keys()) & set(rq3_rank.keys()) & set(rq4_rank.keys()))

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.4,
    })

    fig, ax = plt.subplots(figsize=(6, 5.5))

    x_positions = [0, 1, 2]
    x_labels = ["RQ1\nDescription", "RQ3\nComprehension", "RQ4\nBehaviour"]
    n = len(all_models)

    # Draw non-focal models in grey
    for model in all_models:
        if model in FOCAL:
            continue
        ranks = [rq1_rank[model], rq3_rank[model], rq4_rank[model]]
        ax.plot(x_positions, ranks, color="#999999", linewidth=0.8, alpha=0.5,
                marker="o", markersize=3, markeredgecolor="white", markeredgewidth=0.2,
                zorder=1)

    # Draw focal models
    for model in all_models:
        if model not in FOCAL:
            continue
        fm = FOCAL[model]
        ranks = [rq1_rank[model], rq3_rank[model], rq4_rank[model]]
        ax.plot(x_positions, ranks, color=fm["color"], linewidth=2.2, alpha=0.9,
                marker="o", markersize=7, markeredgecolor="white", markeredgewidth=0.8,
                zorder=4)

        # Labels at left and right endpoints
        ax.annotate(f"{fm['label']} ({ranks[0]})",
                    xy=(-0.08, ranks[0]), fontsize=6.5, color=fm["color"],
                    fontweight="bold", va="center", ha="right", zorder=5)
        ax.annotate(f"({ranks[2]}) {fm['label']}",
                    xy=(2.08, ranks[2]), fontsize=6.5, color=fm["color"],
                    fontweight="bold", va="center", ha="left", zorder=5)

        # Rank number at middle
        ax.annotate(f"{ranks[1]}", xy=(1, ranks[1] - 0.3),
                    fontsize=5.5, color=fm["color"], fontweight="bold",
                    ha="center", va="bottom", zorder=5)

    # Non-focal labels at edges (subtle)
    for model in all_models:
        if model in FOCAL:
            continue
        short = MODEL_SHORT.get(model, model)
        r1 = rq1_rank[model]
        r4 = rq4_rank[model]
        ax.annotate(short, xy=(-0.08, r1), fontsize=4.5, color="#AAAAAA",
                    va="center", ha="right", zorder=1)
        ax.annotate(short, xy=(2.08, r4), fontsize=4.5, color="#AAAAAA",
                    va="center", ha="left", zorder=1)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, fontsize=9, fontweight="medium")
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(n + 0.5, 0.5)  # rank 1 at top
    ax.set_ylabel("Rank", fontsize=10, labelpad=8)

    ax.yaxis.grid(True, alpha=0.08, linewidth=0.4)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(colors="#666666", length=3)

    plt.tight_layout()

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
