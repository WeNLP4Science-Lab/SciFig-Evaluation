"""RQ4 Chart: Stacked bar — admittance response breakdown per model.

Shows proportion of admits/fabricates/silent responses for axis blur.

Output: thesis/main/figures/rq4/admittance_stacked.pdf
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ADV_RESULTS = ROOT / "dashboard" / "public" / "data" / "adversarial_results.json"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq4" / "admittance_stacked.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq4" / "plots" / "admittance_stacked.png"

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2", "gemini-3.1-pro": "Gemini 3.1P",
    "claude-opus-4.6": "Claude 4.6", "qwen3-vl-235b-a22b": "Qwen 235B",
    "qwen3-vl-32b": "Qwen 32B", "qwen3-vl-30b-a3b": "Qwen 30B",
    "qwen3-vl-8b": "Qwen 8B", "llama4-maverick": "LLaMA Mav.",
    "llama4-scout": "LLaMA Scout", "gemma3-27b-it": "Gemma 27B",
    "phi-4-multimodal": "Phi-4", "gemma3-12b-it": "Gemma 12B",
    "gemma3-4b-it": "Gemma 4B",
}


def main():
    adv = json.load(open(ADV_RESULTS))
    pa = adv["passive_admittance"]

    # Judge-averaged counts for axis blur
    model_data = []
    for r in pa:
        model = r["model"]
        admits = np.mean([r.get("gpt-4o_axis_blurred_admits", 0), r.get("mistral-large-3_axis_blurred_admits", 0)])
        fabs = np.mean([r.get("gpt-4o_axis_blurred_fabricates", 0), r.get("mistral-large-3_axis_blurred_fabricates", 0)])
        silent = np.mean([r.get("gpt-4o_axis_blurred_silent", 0), r.get("mistral-large-3_axis_blurred_silent", 0)])
        total = admits + fabs + silent
        if total == 0:
            total = 1
        model_data.append({
            "model": model,
            "short": MODEL_SHORT.get(model, model),
            "admits_pct": admits / total * 100,
            "fabs_pct": fabs / total * 100,
            "silent_pct": silent / total * 100,
            "admits_rate": admits / total,
        })

    # Sort by admittance rate (most honest at top)
    model_data.sort(key=lambda x: -x["admits_rate"])

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.linewidth": 0.5,
    })

    fig, ax = plt.subplots(figsize=(5.5, 3.8))

    y = np.arange(len(model_data))
    labels = [m["short"] for m in model_data]

    admits = [m["admits_pct"] for m in model_data]
    fabs = [m["fabs_pct"] for m in model_data]
    silent = [m["silent_pct"] for m in model_data]

    # Stacked bars
    bars1 = ax.barh(y, admits, height=0.65, color="#228833", alpha=0.85,
                    label="Admits", edgecolor="white", linewidth=0.3)
    bars2 = ax.barh(y, fabs, left=admits, height=0.65, color="#CC3311", alpha=0.85,
                    label="Fabricates", edgecolor="white", linewidth=0.3)
    bars3 = ax.barh(y, silent, left=[a + f for a, f in zip(admits, fabs)],
                    height=0.65, color="#888888", alpha=0.6,
                    label="Silent", edgecolor="white", linewidth=0.3)

    # Percentage labels
    for i, (a, f, s) in enumerate(zip(admits, fabs, silent)):
        if a > 12:
            ax.text(a / 2, y[i], f"{a:.0f}%", ha="center", va="center",
                    fontsize=5.5, color="white", fontweight="bold")
        if f > 12:
            ax.text(a + f / 2, y[i], f"{f:.0f}%", ha="center", va="center",
                    fontsize=5.5, color="white", fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("Response proportion (%)", fontsize=8)
    ax.set_xlim(0, 100)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1),
              ncol=3, fontsize=7, frameon=True, framealpha=0.95,
              edgecolor="#CCCCCC")

    plt.tight_layout(rect=[0, 0.06, 1, 1])

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
