"""RQ1 Chart 1: Dumbbell chart — per-judge scores with model logos.

A dumbbell (connected dot) chart showing GPT-4o and Mistral scores per model,
connected by a line. The gap between dots shows judge disagreement.
Model logos on the y-axis. Sorted by average score.

Output: thesis/main/figures/rq1/leaderboard_dumbbell.pdf
        output/evaluation-results/rq1/plots/leaderboard_dumbbell.png
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
LEADERBOARD = ROOT / "output" / "evaluation-results" / "rq1" / "leaderboard.json"
LOGOS_DIR = ROOT / "thesis" / "main" / "figures"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq1" / "leaderboard_dumbbell.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq1" / "plots" / "leaderboard_dumbbell.png"

# Model display names and logo mapping
MODEL_DISPLAY = {
    "gpt-5.2": "GPT-5.2",
    "gemini-3.1-pro": "Gemini 3.1 Pro",
    "claude-opus-4.6": "Claude Opus 4.6",
    "qwen3-vl-235b-a22b": "Qwen3-VL 235B",
    "qwen3-vl-32b": "Qwen3-VL 32B",
    "qwen3-vl-30b-a3b": "Qwen3-VL 30B",
    "qwen3-vl-8b": "Qwen3-VL 8B",
    "llama4-maverick": "LLaMA-4 Maverick",
    "llama4-scout": "LLaMA-4 Scout",
    "gemma3-27b-it": "Gemma-3 27B",
    "gemma3-12b-it": "Gemma-3 12B",
    "gemma3-4b-it": "Gemma-3 4B",
    "phi-4-multimodal": "Phi-4 Multimodal",
}

MODEL_LOGO = {
    "gpt-5.2": "gptlogo.jpg",
    "gemini-3.1-pro": "geminilogo.png",
    "claude-opus-4.6": "claudelogo.png",
    "qwen3-vl-235b-a22b": "qwenlogo.png",
    "qwen3-vl-32b": "qwenlogo.png",
    "qwen3-vl-30b-a3b": "qwenlogo.png",
    "qwen3-vl-8b": "qwenlogo.png",
    "llama4-maverick": "llama4logo.png",
    "llama4-scout": "llama4logo.png",
    "gemma3-27b-it": "gemmalogo.png",
    "gemma3-12b-it": "gemmalogo.png",
    "gemma3-4b-it": "gemmalogo.png",
    "phi-4-multimodal": "philogo.png",
}

# Model family colors (Paul Tol palette)
FAMILY_COLORS = {
    "gpt": "#4477AA",
    "gemini": "#EE6677",
    "claude": "#AA3377",
    "qwen": "#228833",
    "llama": "#CCBB44",
    "gemma": "#66CCEE",
    "phi": "#BBBBBB",
}

def get_family(model):
    for fam in FAMILY_COLORS:
        if fam in model.lower():
            return fam
    return "phi"


def load_logo(model, size=0.035):
    """Load and return an OffsetImage for the model logo."""
    logo_file = LOGOS_DIR / MODEL_LOGO.get(model, "")
    if not logo_file.exists():
        return None
    try:
        img = mpimg.imread(str(logo_file))
        return OffsetImage(img, zoom=size)
    except Exception:
        return None


def main():
    data = json.load(open(LEADERBOARD))

    # Sort by average overall (already sorted by rank)
    models = [d["model"] for d in data]
    gpt4o = [d.get("gpt-4o_Overall", {}).get("mean", 0) for d in data]
    mistral = [d.get("mistral-large-3_Overall", {}).get("mean", 0) for d in data]
    avg = [(g + m) / 2 for g, m in zip(gpt4o, mistral)]

    # Reverse for bottom-to-top (best at top)
    n = len(models)
    y_pos = list(range(n))

    # --- Figure setup ---
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.linewidth": 0.6,
        "figure.dpi": 300,
    })

    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw connecting lines (dumbbells)
    for i, (g, m) in enumerate(zip(gpt4o, mistral)):
        fam = get_family(models[i])
        color = FAMILY_COLORS[fam]
        ax.plot([g, m], [y_pos[i], y_pos[i]], color=color, linewidth=1.8, alpha=0.4, zorder=1)

    # Draw GPT-4o dots
    ax.scatter(gpt4o, y_pos, color="#CC3311", s=50, zorder=3, label="GPT-4o (judge)",
               marker="D", edgecolors="white", linewidth=0.5)

    # Draw Mistral dots
    ax.scatter(mistral, y_pos, color="#0077BB", s=50, zorder=3, label="Mistral Large 3 (judge)",
               marker="o", edgecolors="white", linewidth=0.5)

    # Draw average markers
    ax.scatter(avg, y_pos, color="black", s=20, zorder=4, marker="|", linewidths=1.2)

    # Add circular model logos to the right of y-axis labels
    from PIL import Image as PILImage
    LOGO_PX = 40  # uniform logo size in pixels

    for i, model in enumerate(models):
        logo_file = LOGOS_DIR / MODEL_LOGO.get(model, "")
        if not logo_file.exists():
            continue
        try:
            pil_img = PILImage.open(logo_file).convert("RGBA")
            # Crop to square center
            w, h = pil_img.size
            s = min(w, h)
            left, top = (w - s) // 2, (h - s) // 2
            pil_img = pil_img.crop((left, top, left + s, top + s))
            # Resize to uniform size
            pil_img = pil_img.resize((LOGO_PX, LOGO_PX), PILImage.LANCZOS)

            img = np.array(pil_img).astype(np.float32) / 255.0

            # Create circular mask
            yy, xx = np.ogrid[:LOGO_PX, :LOGO_PX]
            center = LOGO_PX / 2
            mask = ((xx - center)**2 + (yy - center)**2) <= (center * 0.92)**2
            img[:, :, 3] = np.where(mask, img[:, :, 3], 0.0)

            oi = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(oi, (41, y_pos[i]),
                                xycoords="data",
                                box_alignment=(0.5, 0.5),
                                frameon=False, pad=0,
                                clip_on=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Logo error for {model}: {e}")

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels([MODEL_DISPLAY.get(m, m) for m in models], fontsize=8)
    ax.set_xlabel("Atomic MQM Score", fontsize=10, fontweight="medium")
    # Add CI whiskers
    gpt4o_ci_lo = [d.get("gpt-4o_Overall", {}).get("ci_lo", 0) for d in data]
    gpt4o_ci_hi = [d.get("gpt-4o_Overall", {}).get("ci_hi", 0) for d in data]
    mistral_ci_lo = [d.get("mistral-large-3_Overall", {}).get("ci_lo", 0) for d in data]
    mistral_ci_hi = [d.get("mistral-large-3_Overall", {}).get("ci_hi", 0) for d in data]

    for i in range(n):
        ax.plot([gpt4o_ci_lo[i], gpt4o_ci_hi[i]], [y_pos[i] - 0.12, y_pos[i] - 0.12],
                color="#CC3311", linewidth=0.7, alpha=0.4, zorder=2)
        ax.plot([mistral_ci_lo[i], mistral_ci_hi[i]], [y_pos[i] + 0.12, y_pos[i] + 0.12],
                color="#0077BB", linewidth=0.7, alpha=0.4, zorder=2)

    # Add score annotations on best and worst
    ax.annotate(f'{avg[0]:.1f}', xy=(avg[0] + 0.5, y_pos[0] + 0.3), fontsize=7, color='#333333', fontweight='bold')
    ax.annotate(f'{avg[-1]:.1f}', xy=(avg[-1] + 0.5, y_pos[-1] + 0.3), fontsize=7, color='#333333', fontweight='bold')

    ax.set_xlim(40, 85)
    ax.set_ylim(-0.8, n - 0.2)

    # Light grid
    ax.xaxis.grid(True, alpha=0.2, linestyle="-", linewidth=0.5)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)

    # Spine styling
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.4)
    ax.spines["bottom"].set_linewidth(0.4)

    # Family grouping bands
    family_ranges = {
        "Proprietary": (0, 2),
        "Qwen": (3, 6),
        "LLaMA": (7, 8),
        "Gemma/Phi": (9, 12),
    }
    for label, (start, end) in family_ranges.items():
        ax.axhspan(start - 0.45, end + 0.45, alpha=0.04, color="grey", zorder=0)

    # Legend
    legend = ax.legend(loc="lower right", fontsize=7.5, framealpha=0.9,
                       edgecolor="#CCCCCC", handletextpad=0.5)
    legend.get_frame().set_linewidth(0.5)

    # Annotation: average line explanation
    ax.annotate("| = avg", xy=(0.98, 0.02), xycoords="axes fraction",
                fontsize=7, color="black", ha="right", va="bottom")

    plt.tight_layout()

    # Save
    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"Saved: {PDF_OUT}")
    print(f"Saved: {PNG_OUT}")


if __name__ == "__main__":
    main()
