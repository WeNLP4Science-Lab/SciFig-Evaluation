"""Generate Figure 3: A-R-I Behavioural Profiles (Dumbbell Chart).

Three panels showing paired active/passive comparisons:
  Panel (a): Admittance (admits %)
  Panel (b): Resistance (by probe type)
  Panel (c): Inductance (correct %)

Output: paper/figures/figure3_ari.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

STATS_PATH = Path(__file__).resolve().parents[2] / "results" / "statistics" / "all_statistics.json"
OUT_PATH = Path(__file__).resolve().parents[2] / "paper" / "figures" / "figure3_ari.pdf"

MODELS = [
    ("phi-4-multimodal", "Phi-4"),
    ("gemma3-27b-it", "Gemma"),
    ("qwen3-vl-30b-a3b", "Qwen-30B"),
    ("qwen3-vl-8b", "Qwen-8B"),
    ("qwen3-vl-235b-a22b", "Qwen-235B"),
    ("llama4-maverick", "Llama 4"),
    ("gpt-5.2", "GPT-5.2"),
    ("gemini-3.1-pro", "Gemini"),
]

# Colors
MODEL_COLORS = {
    "gemini-3.1-pro": "#2ca02c",
    "gpt-5.2": "#1f77b4",
    "phi-4-multimodal": "#d62728",
}
DEFAULT_COLOR = "#666666"

ACTIVE_MARKER = "o"
PASSIVE_MARKER = "s"


def load_stats():
    with open(STATS_PATH) as f:
        return json.load(f)


def get_mean(stat_dict):
    if not stat_dict or stat_dict.get("mean") is None:
        return None
    return stat_dict["mean"]


def create_figure(stats):
    cis = stats["bootstrap_cis"]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.2, 3.2),
                                         sharey=True, constrained_layout=True)

    y_positions = np.arange(len(MODELS))

    # ── Panel (a): Admittance ──
    for i, (mid, mname) in enumerate(MODELS):
        color = MODEL_COLORS.get(mid, DEFAULT_COLOR)
        lw = 2.0 if mid in MODEL_COLORS else 1.0
        alpha = 1.0 if mid in MODEL_COLORS else 0.6

        act = cis.get("active_probes", {}).get("admittance", {}).get(mid, {})
        pas = cis.get("passive_probes", {}).get("admittance", {}).get(mid, {})

        act_val = get_mean(act.get("admits", {}))
        pas_val = get_mean(pas.get("admits", {}))

        if act_val is not None and pas_val is not None:
            act_pct = act_val * 100
            pas_pct = pas_val * 100
            ax1.plot([pas_pct, act_pct], [i, i], color=color, linewidth=lw, alpha=alpha, zorder=2)
            ax1.scatter(act_pct, i, color=color, marker=ACTIVE_MARKER, s=40, zorder=3, alpha=alpha)
            ax1.scatter(pas_pct, i, color=color, marker=PASSIVE_MARKER, s=40, zorder=3, alpha=alpha)

    ax1.set_xlabel("Admits (%)", fontsize=8)
    ax1.set_title("(a) Admittance", fontsize=9, fontweight="bold", pad=8)
    ax1.set_xlim(-5, 100)
    ax1.axvline(50, color="#e0e0e0", linewidth=0.5, linestyle=":", zorder=0)

    # ── Panel (b): Resistance ──
    for i, (mid, mname) in enumerate(MODELS):
        color = MODEL_COLORS.get(mid, DEFAULT_COLOR)
        lw = 2.0 if mid in MODEL_COLORS else 1.0
        alpha = 1.0 if mid in MODEL_COLORS else 0.6

        r_by_type = cis.get("resistance_by_type", {}).get(mid, {})
        inexist = get_mean(r_by_type.get("inexist", {}))
        contra = get_mean(r_by_type.get("contra", {}))
        unanswerable = get_mean(r_by_type.get("unanswerable", {}))

        vals = [v for v in [inexist, contra, unanswerable] if v is not None]
        if vals:
            lo, hi = min(vals), max(vals)
            ax2.plot([lo, hi], [i, i], color=color, linewidth=lw, alpha=alpha, zorder=2)
            # Plot each type
            if inexist is not None:
                ax2.scatter(inexist, i, color=color, marker="v", s=35, zorder=3, alpha=alpha)
            if contra is not None:
                ax2.scatter(contra, i, color=color, marker="D", s=30, zorder=3, alpha=alpha)
            if unanswerable is not None:
                ax2.scatter(unanswerable, i, color=color, marker="^", s=35, zorder=3, alpha=alpha)

    ax2.set_xlabel("Resistance Score", fontsize=8)
    ax2.set_title("(b) Resistance", fontsize=9, fontweight="bold", pad=8)
    ax2.set_xlim(-0.05, 1.05)
    ax2.axvline(0.5, color="#e0e0e0", linewidth=0.5, linestyle=":", zorder=0)

    # ── Panel (c): Inductance ──
    for i, (mid, mname) in enumerate(MODELS):
        color = MODEL_COLORS.get(mid, DEFAULT_COLOR)
        lw = 2.0 if mid in MODEL_COLORS else 1.0
        alpha = 1.0 if mid in MODEL_COLORS else 0.6

        act = cis.get("active_probes", {}).get("inductance", {}).get(mid, {})
        pas = cis.get("passive_probes", {}).get("inductance", {}).get(mid, {})

        act_val = get_mean(act.get("correct_given_fab", {}))
        pas_val = get_mean(pas.get("correct_given_fab", {}))

        if act_val is not None and pas_val is not None:
            act_pct = act_val * 100
            pas_pct = pas_val * 100
            ax3.plot([pas_pct, act_pct], [i, i], color=color, linewidth=lw, alpha=alpha, zorder=2)
            ax3.scatter(act_pct, i, color=color, marker=ACTIVE_MARKER, s=40, zorder=3, alpha=alpha)
            ax3.scatter(pas_pct, i, color=color, marker=PASSIVE_MARKER, s=40, zorder=3, alpha=alpha)

    ax3.set_xlabel("Correct (%)", fontsize=8)
    ax3.set_title("(c) Inductance", fontsize=9, fontweight="bold", pad=8)
    ax3.set_xlim(-5, 100)
    ax3.axvline(50, color="#e0e0e0", linewidth=0.5, linestyle=":", zorder=0)

    # ── Shared y-axis ──
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels([m[1] for m in MODELS], fontsize=8)

    # ── Styling ──
    for ax in [ax1, ax2, ax3]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", alpha=0.15)
        ax.tick_params(axis="x", labelsize=7)

    # ── Legend ──
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker=ACTIVE_MARKER, color="grey", label="Active", markersize=6, linestyle="None"),
        Line2D([0], [0], marker=PASSIVE_MARKER, color="grey", label="Passive", markersize=6, linestyle="None"),
    ]
    # For resistance panel
    resistance_legend = [
        Line2D([0], [0], marker="v", color="grey", label="Inexist", markersize=5, linestyle="None"),
        Line2D([0], [0], marker="D", color="grey", label="Contra", markersize=5, linestyle="None"),
        Line2D([0], [0], marker="^", color="grey", label="Unanswer.", markersize=5, linestyle="None"),
    ]

    ax1.legend(handles=legend_elements, fontsize=6, loc="upper right", framealpha=0.8, edgecolor="#ddd")
    ax2.legend(handles=resistance_legend, fontsize=6, loc="upper left", framealpha=0.8, edgecolor="#ddd")
    ax3.legend(handles=legend_elements, fontsize=6, loc="upper left", framealpha=0.8, edgecolor="#ddd")

    fig.savefig(str(OUT_PATH), dpi=300, bbox_inches="tight")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    stats = load_stats()
    create_figure(stats)
