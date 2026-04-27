"""RQ1 Chart: Scatter — Human MQM vs LLM Judge MQM.

Two-panel scatter showing human scores vs each judge,
colored by model, with identity line and regression.

Output: thesis/main/figures/rq1/scatter_human_judge.pdf
"""

import json
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent.parent
HUMAN_RESULTS = ROOT / "HumanEval" / "human_eval_results.json"
EVAL_DIR = ROOT / "output" / "evaluation" / "atomic_mqm_v2"
PDF_OUT = ROOT / "thesis" / "main" / "figures" / "rq1" / "scatter_human_judge.pdf"
PNG_OUT = ROOT / "output" / "evaluation-results" / "rq1" / "plots" / "scatter_human_judge.png"

MODEL_NORM = {
    "gemma3-27b": "gemma3-27b-it",
    "qwen-vl-8b": "qwen3-vl-8b",
    "qwen-vl-30b": "qwen3-vl-30b-a3b",
    "gpt-5.2": "gpt-5.2",
}

MODEL_DISPLAY = {
    "gpt-5.2": "GPT-5.2",
    "qwen3-vl-30b-a3b": "Qwen3-VL 30B",
    "qwen3-vl-8b": "Qwen3-VL 8B",
    "gemma3-27b-it": "Gemma-3 27B",
}

# Paul Tol palette
MODEL_COLORS = {
    "gpt-5.2": "#4477AA",
    "qwen3-vl-30b-a3b": "#228833",
    "qwen3-vl-8b": "#CCBB44",
    "gemma3-27b-it": "#EE6677",
}

HUMAN_MODELS = set(MODEL_NORM.values())


def load_human_scores():
    data = json.load(open(HUMAN_RESULTS))
    by_key = defaultdict(list)
    for r in data["results"]:
        model = r["model_name"]
        if model not in HUMAN_MODELS:
            model = MODEL_NORM.get(model, model)
        by_key[(r["figure_key"], model)].append(r["mqm_score"])
    return {k: np.mean(v) for k, v in by_key.items()}


def load_judge_scores(judge):
    scores = {}
    judge_dir = EVAL_DIR / "azure" / judge
    if not judge_dir.exists():
        return scores
    for model in HUMAN_MODELS:
        model_dir = judge_dir / model
        if not model_dir.exists():
            continue
        for f in model_dir.rglob("*.json"):
            try:
                d = json.load(open(f))
                scores[(d["figure_key"], model)] = d["mqm_score"]
            except Exception:
                pass
    return scores


def main():
    human = load_human_scores()
    human_figs = set(k[0] for k in human)

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.linewidth": 0.6,
    })

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(9.5, 3.3), sharey=True)

    # Panel 0: Human vs Human (inter-annotator)
    data_raw = json.load(open(HUMAN_RESULTS))
    by_task = defaultdict(dict)
    for r in data_raw["results"]:
        model = r["model_name"]
        if model not in HUMAN_MODELS:
            model = MODEL_NORM.get(model, model)
        key = (r["figure_key"], model)
        by_task[key][r["annotator_id"]] = r["mqm_score"]

    for model in sorted(HUMAN_MODELS):
        h1, h2 = [], []
        for key, annots in by_task.items():
            if key[1] != model or len(annots) < 2:
                continue
            ids = sorted(annots.keys())
            h1.append(annots[ids[0]])
            h2.append(annots[ids[1]])
        if h1:
            ax0.scatter(h1, h2, s=18, alpha=0.7,
                        color=MODEL_COLORS[model],
                        label=MODEL_DISPLAY[model],
                        edgecolors="white", linewidth=0.3, zorder=3)

    ax0.plot([0, 100], [0, 100], "k--", alpha=0.2, linewidth=0.8, zorder=1)
    # Regression
    all_h1 = [annots[sorted(annots.keys())[0]] for annots in by_task.values() if len(annots) >= 2]
    all_h2 = [annots[sorted(annots.keys())[1]] for annots in by_task.values() if len(annots) >= 2]
    if all_h1:
        rho_hh, _ = stats.spearmanr(all_h1, all_h2)
        r_hh, _ = stats.pearsonr(all_h1, all_h2)
        slope, intercept = np.polyfit(all_h1, all_h2, 1)
        x_fit = np.linspace(20, 100, 100)
        ax0.plot(x_fit, slope * x_fit + intercept, color="#AA3377", linewidth=1.2, alpha=0.6, zorder=2)
        ax0.text(0.04, 0.96, f"$\\rho$={rho_hh:.2f}\n$r$={r_hh:.2f}",
                 transform=ax0.transAxes, fontsize=7, va="top", ha="left",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#CCCCCC", linewidth=0.5))

    ax0.set_title("Human vs Human", fontsize=9, fontweight="medium")
    ax0.set_xlabel("Annotator 1 MQM", fontsize=8)
    ax0.set_ylabel("Annotator 2 / Judge MQM", fontsize=8)
    ax0.set_xlim(25, 105)
    ax0.set_ylim(15, 105)
    ax0.set_aspect("equal")
    ax0.grid(True, alpha=0.15, linewidth=0.4)
    ax0.spines["top"].set_visible(False)
    ax0.spines["right"].set_visible(False)

    for ax, judge, title in [
        (ax1, "gpt-4o", "Human vs GPT-4o"),
        (ax2, "mistral-large-3", "Human vs Mistral"),
    ]:
        judge_scores = load_judge_scores(judge)
        common = sorted(set(human.keys()) & set(judge_scores.keys()))

        h_all, j_all = [], []
        for model in sorted(HUMAN_MODELS):
            mk = [k for k in common if k[1] == model]
            h = [human[k] for k in mk]
            j = [judge_scores[k] for k in mk]
            h_all.extend(h)
            j_all.extend(j)

            ax.scatter(h, j, s=18, alpha=0.7,
                       color=MODEL_COLORS[model],
                       label=MODEL_DISPLAY[model],
                       edgecolors="white", linewidth=0.3,
                       zorder=3)

        h_all, j_all = np.array(h_all), np.array(j_all)

        # Identity line
        ax.plot([0, 100], [0, 100], "k--", alpha=0.2, linewidth=0.8, zorder=1)

        # Regression line
        slope, intercept = np.polyfit(h_all, j_all, 1)
        x_fit = np.linspace(30, 100, 100)
        ax.plot(x_fit, slope * x_fit + intercept, color="#AA3377",
                linewidth=1.2, alpha=0.6, zorder=2)

        # Stats
        rho, rho_p = stats.spearmanr(h_all, j_all)
        r, r_p = stats.pearsonr(h_all, j_all)

        ax.text(0.04, 0.96,
                f"$\\rho$={rho:.2f}\n$r$={r:.2f}",
                transform=ax.transAxes, fontsize=7,
                va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#CCCCCC", linewidth=0.5))

        ax.set_title(title, fontsize=9, fontweight="medium")
        ax.set_xlabel("Human MQM (avg)", fontsize=8)
        ax.set_xlim(25, 105)
        ax.set_ylim(15, 105)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.15, linewidth=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # ax0 already has ylabel set

    # Shared legend
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=7,
               frameon=True, framealpha=0.9, edgecolor="#CCCCCC",
               bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout(rect=[0, 0.06, 1, 1])

    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    fig.savefig(PNG_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
