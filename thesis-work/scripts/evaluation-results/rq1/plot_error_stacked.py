"""RQ1 Chart: Stacked bar — Error category proportions per model.

Horizontal 100% stacked bars showing Accuracy/Completeness/Clarity
split by Major/Minor for each model.

Output: thesis/main/figures/rq1/error_stacked.pdf
"""

import json
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
EVAL_DIR = ROOT / "output" / "evaluation" / "atomic_mqm_v2"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq1" / "error_stacked.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq1" / "plots" / "error_stacked.png"

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2",
    "gemini-3.1-pro": "Gemini 3.1P",
    "claude-opus-4.6": "Claude 4.6",
    "qwen3-vl-235b-a22b": "Qwen 235B",
    "qwen3-vl-32b": "Qwen 32B",
    "qwen3-vl-30b-a3b": "Qwen 30B",
    "qwen3-vl-8b": "Qwen 8B",
    "llama4-maverick": "LLaMA Mav.",
    "llama4-scout": "LLaMA Scout",
    "gemma3-27b-it": "Gemma 27B",
    "phi-4-multimodal": "Phi-4",
    "gemma3-12b-it": "Gemma 12B",
    "gemma3-4b-it": "Gemma 4B",
}

# 6 segments: Acc/Maj, Acc/Min, Comp/Maj, Comp/Min, Clar/Maj, Clar/Min
SEGMENTS = [
    ("Accuracy", "Major"),
    ("Accuracy", "Minor"),
    ("Completeness", "Major"),
    ("Completeness", "Minor"),
    ("Clarity and Readability", "Major"),
    ("Clarity and Readability", "Minor"),
]

COLORS = ["#CC3311", "#EE7733", "#004488", "#6699CC", "#555555", "#AAAAAA"]
LABELS = ["Acc/Maj", "Acc/Min", "Comp/Maj", "Comp/Min", "Clar/Maj", "Clar/Min"]


def main():
    # Collect errors per model
    model_errors = defaultdict(lambda: defaultdict(int))
    model_total = defaultdict(int)
    model_n = defaultdict(int)

    for judge_dir in EVAL_DIR.glob("azure/*"):
        for model_dir in judge_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model = model_dir.name
            for f in model_dir.rglob("*.json"):
                try:
                    d = json.load(open(f))
                    model_n[model] += 1
                    for e in d.get("errors", []):
                        cat = e.get("category", "?")
                        sev = e.get("severity", "?")
                        model_errors[model][(cat, sev)] += 1
                        model_total[model] += 1
                except Exception:
                    pass

    # Sort by total errors per eval (ascending = best first)
    models = sorted(model_errors.keys(),
                    key=lambda m: model_total[m] / max(model_n[m], 1))

    # Build data matrix (proportions)
    data = np.zeros((len(models), len(SEGMENTS)))
    totals = []
    for i, model in enumerate(models):
        total = model_total[model]
        totals.append(total / model_n[model])
        for j, (cat, sev) in enumerate(SEGMENTS):
            data[i, j] = model_errors[model][(cat, sev)] / total * 100 if total > 0 else 0

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
    })

    fig, ax = plt.subplots(figsize=(5.5, 3.8))

    y = np.arange(len(models))
    left = np.zeros(len(models))

    for j in range(len(SEGMENTS)):
        bars = ax.barh(y, data[:, j], left=left, height=0.65,
                       color=COLORS[j], label=LABELS[j],
                       edgecolor="white", linewidth=0.3)
        # Label segments > 15%
        for i, (val, l) in enumerate(zip(data[:, j], left)):
            if val > 15:
                ax.text(l + val / 2, y[i], f"{val:.0f}", ha="center", va="center",
                        fontsize=5.5, color="white", fontweight="bold")
        left += data[:, j]

    # Annotate total errors/fig at right
    for i, (model, total) in enumerate(zip(models, totals)):
        ax.text(101, y[i], f"{total:.1f}", ha="left", va="center",
                fontsize=6.5, color="#333333")

    ax.set_yticks(y)
    ax.set_yticklabels([MODEL_SHORT.get(m, m) for m in models], fontsize=7)
    ax.set_xlabel("Error proportion (%)", fontsize=8)
    ax.set_xlim(0, 108)
    ax.set_ylim(-0.5, len(models) - 0.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.4)
    ax.spines["bottom"].set_linewidth(0.4)

    # Legend
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.12),
              ncol=6, fontsize=6, frameon=False, handletextpad=0.4,
              columnspacing=0.8)

    # Label for the right annotations
    ax.text(104, len(models) - 0.3, "E/fig", ha="center", fontsize=6, color="#666666")

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
