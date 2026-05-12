"""RQ3 Chart: Vertical grouped bar — capability accuracy by question category.

Groups = 5 question categories. Bars = focal models (6 representative).
Model logos above each bar group in the legend. Premium vertical design.

Output: thesis/main/figures/rq3/capability_grouped_bar.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image as PILImage
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CAP_DATA = ROOT / "output" / "evaluation-results" / "rq3" / "capability.json"
LOGOS_DIR = ROOT / "thesis" / "main" / "figures"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq3" / "capability_grouped_bar.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq3" / "plots" / "capability_grouped_bar.png"

CATEGORIES = ["computation", "value_reading", "comparison", "trend_analysis", "counting"]
CAT_LABELS = ["Computation", "Value\nReading", "Comparison", "Trend\nAnalysis", "Counting"]

# 6 focal models spanning the range, with brand colours and logos
FOCAL_MODELS = [
    {"model": "gemini-3.1-pro",  "label": "Gemini",   "color": "#4285F4", "logo": "geminilogo.png"},
    {"model": "gpt-5.2",         "label": "GPT-5.2",  "color": "#10A37F", "logo": "gptlogo.jpg"},
    {"model": "claude-opus-4.6", "label": "Claude",   "color": "#D97706", "logo": "claudelogo.png"},
    {"model": "qwen3-vl-32b",    "label": "Qwen 32B", "color": "#6366F1", "logo": "qwenlogo.png"},
    {"model": "llama4-maverick",  "label": "LLaMA M.", "color": "#7B61FF", "logo": "llama4logo.png"},
    {"model": "gemma3-4b-it",    "label": "Gemma 4B", "color": "#E04E39", "logo": "gemmalogo.png"},
]


def load_circular_logo(logo_file, size=30):
    """Load logo, crop to square, apply circular mask, resize."""
    try:
        pil_img = PILImage.open(logo_file).convert("RGBA")
        w, h = pil_img.size
        s = min(w, h)
        left, top = (w - s) // 2, (h - s) // 2
        pil_img = pil_img.crop((left, top, left + s, top + s))
        pil_img = pil_img.resize((size, size), PILImage.LANCZOS)
        img = np.array(pil_img).astype(np.float32) / 255.0
        yy, xx = np.ogrid[:size, :size]
        center = size / 2
        mask = ((xx - center)**2 + (yy - center)**2) <= (center * 0.92)**2
        img[:, :, 3] = np.where(mask, img[:, :, 3], 0.0)
        return img
    except Exception:
        return None


def main():
    data = json.load(open(CAP_DATA))
    models_data = {m["model"]: m for m in data["models"]}

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.5,
    })

    fig, ax = plt.subplots(figsize=(7, 4.5))

    n_cats = len(CATEGORIES)
    n_models = len(FOCAL_MODELS)
    bar_width = 0.12
    group_gap = 0.3

    x_base = np.arange(n_cats) * (n_models * bar_width + group_gap)

    for j, fm in enumerate(FOCAL_MODELS):
        model = fm["model"]
        md = models_data.get(model, {})
        vals = [md.get(f"avg_{cat}", 0) * 100 for cat in CATEGORIES]
        x_pos = x_base + j * bar_width

        bars = ax.bar(x_pos, vals, width=bar_width * 0.88,
                      color=fm["color"], alpha=0.85,
                      edgecolor="white", linewidth=0.4,
                      label=fm["label"], zorder=3)

        # Value labels on top of bars
        for bar, val in zip(bars, vals):
            if val > 5:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2,
                        f"{val:.0f}", ha="center", va="bottom",
                        fontsize=5, color=fm["color"], fontweight="bold")

    # X-axis labels centered on groups
    group_centers = x_base + (n_models - 1) * bar_width / 2
    ax.set_xticks(group_centers)
    ax.set_xticklabels(CAT_LABELS, fontsize=8, fontweight="medium")

    ax.set_ylabel("Accuracy (%)", fontsize=9, labelpad=8)
    ax.set_ylim(0, 105)
    ax.set_xlim(-0.15, x_base[-1] + n_models * bar_width + 0.1)

    # Minimal grid
    ax.yaxis.grid(True, alpha=0.12, linewidth=0.4, color="#888888")
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["left"].set_linewidth(0.6)
    ax.spines["bottom"].set_color("#888888")
    ax.spines["bottom"].set_linewidth(0.6)
    ax.tick_params(colors="#555555", length=3)

    # Legend with logos — horizontal, below chart
    legend_handles = []
    for fm in FOCAL_MODELS:
        logo_file = LOGOS_DIR / fm["logo"]
        logo_img = load_circular_logo(logo_file, size=22)
        if logo_img is not None:
            # Create a custom legend entry with logo
            from matplotlib.patches import Patch
            legend_handles.append(Patch(facecolor=fm["color"], edgecolor="white",
                                        linewidth=0.5, label=fm["label"]))
        else:
            from matplotlib.patches import Patch
            legend_handles.append(Patch(facecolor=fm["color"], edgecolor="white",
                                        linewidth=0.5, label=fm["label"]))

    ax.legend(handles=legend_handles,
              loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=6, fontsize=7, frameon=True, framealpha=0.95,
              edgecolor="#CCCCCC", handletextpad=0.4, columnspacing=1.0,
              handlelength=1.2)


    plt.tight_layout(rect=[0, 0.1, 1, 1])

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
