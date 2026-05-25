"""Generate Figure 2: MQM degradation across conditions.

Two-panel composite:
  Panel (a): Slope chart with 3 highlighted models, rest in grey
  Panel (b): Delta heatmap showing drop from matched baseline

Output: paper/figures/figure2_degradation.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# Paths
STATS_DIR = Path(__file__).resolve().parents[2] / "results" / "statistics"
OUT_PATH = Path(__file__).resolve().parents[2] / "paper" / "figures" / "figure2_degradation.pdf"

# Model config
MODELS = [
    ("gpt-5.2", "GPT-5.2"),
    ("gemini-3.1-pro", "Gemini"),
    ("llama4-maverick", "Llama 4"),
    ("qwen3-vl-235b-a22b", "Qwen-235B"),
    ("qwen3-vl-8b", "Qwen-8B"),
    ("qwen3-vl-30b-a3b", "Qwen-30B"),
    ("gemma3-27b-it", "Gemma"),
    ("phi-4-multimodal", "Phi-4"),
]

# Conditions in display order
CONDITIONS = [
    ("original", "Original\n(no cap.)"),
    ("noise", "Noise"),
    ("low_contrast", "Low\nContrast"),
    ("rotation", "Rotation"),
    ("in_paper", "In-Paper"),
    ("caption_bias", "Caption\nBias"),
    ("admittance_blur", "Adm.\nBlur"),
    ("inductance_blur", "Ind.\nBlur"),
]

# Highlight models
HIGHLIGHT = {
    "gpt-5.2": ("#1f77b4", "-", "o", 2.2),      # blue, solid
    "gemini-3.1-pro": ("#2ca02c", "--", "s", 2.2), # green, dashed
    "phi-4-multimodal": ("#d62728", "-.", "^", 2.0), # red, dashdot
}

# Okabe-Ito inspired palette
GREY = "#b0b0b0"

# Group separators
GROUP_BOUNDARIES = [3.5, 4.5, 5.5]  # after rotation, after in-paper, after caption_bias
GROUP_LABELS = ["Perceptual", "Context", "Adversarial"]
GROUP_POSITIONS = [1.5, 4.0, 6.5]


def load_data():
    """Load MQM scores from evaluation files."""
    base_dir = Path(__file__).resolve().parents[2] / "results" / "evaluation" / "description_tasks"

    # Get matched baseline (on the 100 sampled figures)
    trans_dir = base_dir / "transforms"

    data = {}
    for model_id, model_name in MODELS:
        # Get figures in original transform (the 100 sample)
        orig_dir = trans_dir / "original" / model_id
        sample_figs = set(f.stem for f in orig_dir.glob("*.json")) if orig_dir.exists() else set()

        # Matched baseline
        bl_dir = base_dir / "baseline_descriptions" / model_id
        bl_scores = {}
        for f in bl_dir.glob("*.json"):
            if f.stem in sample_figs:
                d = json.load(open(f))
                bl_scores[f.stem] = d.get("mqm_deduped", d.get("mqm_raw", 0))

        baseline_mean = np.mean(list(bl_scores.values())) if bl_scores else 0

        # Transform scores
        scores = [baseline_mean]
        for cond_id, cond_label in CONDITIONS:
            c_dir = trans_dir / cond_id / model_id
            if c_dir.exists():
                vals = []
                for f in c_dir.glob("*.json"):
                    d = json.load(open(f))
                    s = d.get("mqm_deduped", d.get("mqm_raw"))
                    if s is not None:
                        vals.append(s)
                scores.append(np.mean(vals) if vals else 0)
            else:
                scores.append(0)

        data[model_id] = {
            "name": model_name,
            "baseline": baseline_mean,
            "scores": scores,  # [baseline, orig, noise, ...]
        }

    return data


def create_figure(data):
    """Create the two-panel degradation figure."""
    fig, ax1 = plt.subplots(1, 1, figsize=(7.2, 3.0),
                            constrained_layout=True)

    x_labels = ["Baseline\n(+cap.)"] + [cl for _, cl in CONDITIONS]
    x = np.arange(len(x_labels))

    # ── Panel (a): Slope chart ──
    for model_id, model_name in MODELS:
        scores = data[model_id]["scores"]

        if model_id in HIGHLIGHT:
            color, ls, marker, lw = HIGHLIGHT[model_id]
            ax1.plot(x, scores, color=color, linestyle=ls, marker=marker,
                     markersize=5, linewidth=lw, label=model_name, zorder=3)
        else:
            ax1.plot(x, scores, color=GREY, linestyle="-", linewidth=0.8,
                     alpha=0.5, zorder=1)
            # Add model name at the right end
            ax1.annotate(model_name, (x[-1] + 0.15, scores[-1]),
                        fontsize=6, color="#808080", va="center")

    # Group separators
    for gb in GROUP_BOUNDARIES:
        ax1.axvline(gb + 0.5, color="#e0e0e0", linewidth=0.8, linestyle=":", zorder=0)

    # Group labels at top
    for label, pos in zip(GROUP_LABELS, GROUP_POSITIONS):
        ax1.text(pos + 0.5, 97, label, ha="center", fontsize=7, color="#888888",
                fontstyle="italic")

    ax1.set_ylabel("MQM Score", fontsize=9)
    ax1.set_ylim(0, 100)
    ax1.set_xlim(-0.3, len(x_labels) - 0.3)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, fontsize=6.5, rotation=0)
    ax1.legend(fontsize=7.5, loc="lower left", framealpha=0.9, edgecolor="#cccccc")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", alpha=0.2)
    ax1.set_title("MQM across evaluation conditions", fontsize=9, pad=8, loc="left")

    fig.savefig(str(OUT_PATH), dpi=300, bbox_inches="tight")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    data = load_data()
    create_figure(data)
