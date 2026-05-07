"""RQ2 Chart: Premium slope chart — MQM degradation across transforms.

Grey-and-pop design: all models in light grey, 4 focal models in brand colour
with inline labels. No legend box. Tufte-inspired minimal design.

Output: thesis/main/figures/rq2/degradation_slope.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEGRADATION = ROOT / "output" / "evaluation-results" / "rq2" / "degradation.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq2" / "degradation_slope.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq2" / "plots" / "degradation_slope.png"

TRANSFORMS_ORDER = [
    "original", "original_in_paper", "jpeg_compression", "noise",
    "aspect_ratio", "low_contrast", "rotation", "blurred_in_paper",
]

X_LABELS = [
    "Original", "In-Paper", "JPEG", "Noise",
    "Aspect", "Low Contr.", "Rotation", "Blur-in-P.",
]

# Focal models (best, most robust, most volatile, worst) with brand colours
FOCAL = {
    "gpt-5.2":        {"color": "#10A37F", "label": "GPT-5.2"},         # OpenAI green
    "gemini-3.1-pro":  {"color": "#4285F4", "label": "Gemini 3.1 Pro"}, # Google blue
    "llama4-scout":    {"color": "#7B61FF", "label": "LLaMA Scout"},     # Meta purple
    "gemma3-4b-it":    {"color": "#E04E39", "label": "Gemma-3 4B"},     # Google red
}

# All model short names for right-side labels
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
    data = json.load(open(DEGRADATION))
    models = data["models"]

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.4,
    })

    fig, ax = plt.subplots(figsize=(7, 4.5))

    x = np.arange(len(TRANSFORMS_ORDER))

    # Sort models by original score descending
    sorted_models = sorted(models, key=lambda e: -e.get("original", {}).get("score", 0))

    # Pass 1: Draw background lines (all non-focal in grey)
    for entry in sorted_models:
        model = entry["model"]
        if model in FOCAL:
            continue

        scores = [entry.get(t, {}).get("score", np.nan) for t in TRANSFORMS_ORDER]

        ax.plot(x, scores,
                color="#A0A0A0",
                linewidth=0.8,
                linestyle="-",
                alpha=0.55,
                zorder=1)

        # Subtle right-side label
        last_valid = next((s for s in reversed(scores) if not np.isnan(s)), None)
        last_idx = len(scores) - 1 - next((i for i, s in enumerate(reversed(scores)) if not np.isnan(s)), 0)
        if last_valid is not None:
            ax.annotate(
                MODEL_SHORT.get(model, model),
                xy=(last_idx + 0.12, last_valid),
                fontsize=5, color="#777777", va="center",
                zorder=1,
            )

    # Pass 2: Draw focal lines on top with brand colours
    for entry in sorted_models:
        model = entry["model"]
        if model not in FOCAL:
            continue

        style = FOCAL[model]
        scores = [entry.get(t, {}).get("score", np.nan) for t in TRANSFORMS_ORDER]

        ax.plot(x, scores,
                color=style["color"],
                linewidth=2.2,
                linestyle="-",
                marker="o",
                markersize=4.5,
                markeredgecolor="white",
                markeredgewidth=0.8,
                alpha=0.95,
                zorder=4)

        # Bold inline label at right endpoint
        last_valid = next((s for s in reversed(scores) if not np.isnan(s)), None)
        last_idx = len(scores) - 1 - next((i for i, s in enumerate(reversed(scores)) if not np.isnan(s)), 0)
        if last_valid is not None:
            ax.annotate(
                style["label"],
                xy=(last_idx + 0.12, last_valid),
                fontsize=6.5, fontweight="bold",
                color=style["color"], va="center",
                zorder=5,
            )

        # Left-side score label
        ax.annotate(
            f'{scores[0]:.0f}',
            xy=(-0.15, scores[0]),
            fontsize=6, color=style["color"],
            ha="right", va="center", fontweight="bold",
            zorder=5,
        )

    # Minimal zone indicators (thin vertical lines, not shaded blocks)
    for xpos in [1.5, 6.5]:
        ax.axvline(xpos, color="#999999", linewidth=0.8, linestyle="--", zorder=0)

    # Zone labels — very subtle
    ax.text(0.5, 91, "Baselines", ha="center", fontsize=5.5, color="#777777", style="italic")
    ax.text(4.0, 91, "Image transforms", ha="center", fontsize=5.5, color="#777777", style="italic")
    ax.text(7.0, 91, "Diagnostic", ha="center", fontsize=5.5, color="#777777", style="italic")

    # Axes
    ax.set_xticks(x)
    ax.set_xticklabels(X_LABELS, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("Atomic MQM", fontsize=9, labelpad=8)
    ax.set_xlim(-0.4, len(x) + 0.8)
    ax.set_ylim(30, 93)

    # Minimal grid — horizontal only, very faint
    ax.yaxis.grid(True, alpha=0.12, linewidth=0.4, color="#888888")
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["left"].set_linewidth(0.6)
    ax.spines["bottom"].set_color("#888888")
    ax.spines["bottom"].set_linewidth(0.6)

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
