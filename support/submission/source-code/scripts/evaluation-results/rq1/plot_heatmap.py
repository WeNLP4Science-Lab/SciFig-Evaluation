"""RQ1 Chart: Heatmap — Model x Language MQM scores.

Shows all 13 models across languages with both judges averaged.
Annotated cells, RdYlGn diverging colormap.

Output: thesis/main/figures/rq1/heatmap_model_lang.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent.parent.parent
LEADERBOARD = ROOT / "output" / "evaluation-results" / "rq1" / "leaderboard.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq1" / "heatmap_model_lang.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq1" / "plots" / "heatmap_model_lang.png"

MODEL_SHORT = {
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
    "phi-4-multimodal": "Phi-4 Multimodal",
    "gemma3-12b-it": "Gemma-3 12B",
    "gemma3-4b-it": "Gemma-3 4B",
}


def main():
    data = json.load(open(LEADERBOARD))
    langs = ["EN", "BG", "CN", "DE", "Multi", "Overall"]
    lang_labels = ["English", "Bulgarian", "Chinese", "German", "Multi", "Overall"]

    models = [d["model"] for d in data]
    model_labels = [MODEL_SHORT.get(m, m) for m in models]

    # Build matrix
    matrix = np.zeros((len(models), len(langs)))
    for i, d in enumerate(data):
        for j, lang in enumerate(langs):
            v = d.get(f"avg_{lang}", {})
            matrix[i, j] = v.get("mean", 0) if v else 0

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
    })

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    sns.heatmap(
        matrix,
        annot=True, fmt=".0f",
        xticklabels=lang_labels,
        yticklabels=model_labels,
        cmap="RdYlGn",
        center=65,
        vmin=40, vmax=85,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Atomic MQM", "shrink": 0.8},
        annot_kws={"size": 7, "weight": "bold"},
        ax=ax,
    )

    ax.set_xticklabels(lang_labels, rotation=30, ha="right", fontsize=8)
    ax.set_yticklabels(model_labels, rotation=0, fontsize=7.5)
    ax.tick_params(left=False, bottom=False)

    # Bold the best per column
    for j in range(len(langs)):
        col = matrix[:, j]
        best_i = np.argmax(col)
        # Add a subtle box around best cell
        ax.add_patch(plt.Rectangle((j, best_i), 1, 1, fill=False, edgecolor="black", linewidth=1.5))

    plt.tight_layout()

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
