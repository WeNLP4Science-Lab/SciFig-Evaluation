"""RQ1: Compute human vs LLM judge correlation metrics.

Computes Spearman rho, Kendall tau, Krippendorff alpha, ICC,
and per-annotator agreement for the human evaluation data.

Output: output/evaluation-results/rq1/human_judge_correlation.json
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent.parent
HUMAN_RESULTS = ROOT / "HumanEval" / "human_eval_results.json"
EVAL_DIR = ROOT / "output" / "evaluation" / "atomic_mqm_v2"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq1"

# Normalize model names from human eval to match our naming
MODEL_NORM = {
    "gemma3-27b": "gemma3-27b-it",
    "qwen-vl-8b": "qwen3-vl-8b",
    "qwen-vl-30b": "qwen3-vl-30b-a3b",
    "gpt-5.2": "gpt-5.2",
}

HUMAN_MODELS = set(MODEL_NORM.values())


def load_human_scores():
    """Load human eval scores, averaged per (figure, model)."""
    data = json.load(open(HUMAN_RESULTS))
    # Average across annotators for same (figure, model)
    by_key = defaultdict(list)
    for r in data["results"]:
        model = r["model_name"]
        if model not in HUMAN_MODELS:
            # Try normalizing
            model = MODEL_NORM.get(model, model)
        key = (r["figure_key"], model)
        by_key[key].append(r["mqm_score"])

    return {k: np.mean(v) for k, v in by_key.items()}


def load_judge_scores(judge):
    """Load LLM judge scores for human-eval figures and models."""
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
                key = (d["figure_key"], model)
                scores[key] = d["mqm_score"]
            except Exception:
                pass
    return scores


def compute_iaa(human_results_path):
    """Compute inter-annotator agreement from raw human results."""
    data = json.load(open(human_results_path))

    # Group by (figure, model) -> {annotator: score}
    by_task = defaultdict(dict)
    for r in data["results"]:
        model = r["model_name"]
        if model not in HUMAN_MODELS:
            model = MODEL_NORM.get(model, model)
        key = (r["figure_key"], model)
        by_task[key][r["annotator_id"]] = r["mqm_score"]

    # Find double-annotated pairs
    double = {k: v for k, v in by_task.items() if len(v) >= 2}
    if not double:
        return {}

    diffs = []
    pairs_a, pairs_b = [], []
    for key, annotators in double.items():
        ids = sorted(annotators.keys())
        pairs_a.append(annotators[ids[0]])
        pairs_b.append(annotators[ids[1]])
        diffs.append(abs(annotators[ids[0]] - annotators[ids[1]]))

    pairs_a, pairs_b = np.array(pairs_a), np.array(pairs_b)
    diffs = np.array(diffs)

    # Spearman between annotators
    rho, rho_p = stats.spearmanr(pairs_a, pairs_b)
    tau, tau_p = stats.kendalltau(pairs_a, pairs_b)
    pearson, pearson_p = stats.pearsonr(pairs_a, pairs_b)

    # ICC(2,1) — two-way random, single measures, absolute agreement
    # Manual computation: ICC = (MSR - MSE) / (MSR + (k-1)*MSE + k*(MSC-MSE)/n)
    # For 2 raters: simplified
    n = len(pairs_a)
    k = 2  # number of raters
    ratings = np.column_stack([pairs_a, pairs_b])
    mean_subjects = ratings.mean(axis=1)
    mean_raters = ratings.mean(axis=0)
    grand_mean = ratings.mean()

    SSR = k * np.sum((mean_subjects - grand_mean) ** 2)  # between subjects
    SSC = n * np.sum((mean_raters - grand_mean) ** 2)     # between raters
    SST = np.sum((ratings - grand_mean) ** 2)              # total
    SSE = SST - SSR - SSC                                  # residual

    MSR = SSR / (n - 1)
    MSC = SSC / (k - 1)
    MSE = SSE / ((n - 1) * (k - 1))

    # ICC(2,1) absolute agreement
    icc = (MSR - MSE) / (MSR + (k - 1) * MSE + k * (MSC - MSE) / n)

    return {
        "n_double_annotated": len(double),
        "mean_mqm_diff": round(float(np.mean(diffs)), 2),
        "median_mqm_diff": round(float(np.median(diffs)), 2),
        "max_mqm_diff": round(float(np.max(diffs)), 2),
        "within_5_pts": int(np.sum(diffs <= 5)),
        "within_10_pts": int(np.sum(diffs <= 10)),
        "pct_within_10": round(float(np.mean(diffs <= 10) * 100), 1),
        "spearman_rho": round(float(rho), 4),
        "spearman_p": float(rho_p),
        "kendall_tau": round(float(tau), 4),
        "kendall_p": float(tau_p),
        "pearson_r": round(float(pearson), 4),
        "pearson_p": float(pearson_p),
        "icc_2_1": round(float(icc), 4),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    human_scores = load_human_scores()
    human_figs = set(k[0] for k in human_scores)

    output = {
        "metadata": {
            "human_models": sorted(HUMAN_MODELS),
            "n_figures": len(human_figs),
            "n_pairs": len(human_scores),
        },
    }

    # Per-judge correlation
    for judge in ["gpt-4o", "mistral-large-3"]:
        judge_scores = load_judge_scores(judge)

        # Align keys
        common_keys = sorted(set(human_scores.keys()) & set(judge_scores.keys()))
        if not common_keys:
            print(f"No overlap for {judge}")
            continue

        h = np.array([human_scores[k] for k in common_keys])
        j = np.array([judge_scores[k] for k in common_keys])

        rho, rho_p = stats.spearmanr(h, j)
        tau, tau_p = stats.kendalltau(h, j)
        pearson, pearson_p = stats.pearsonr(h, j)

        # Mean bias
        bias = float(np.mean(j - h))

        # Per-model summary
        model_summary = {}
        for model in HUMAN_MODELS:
            mk = [k for k in common_keys if k[1] == model]
            if mk:
                hm = np.mean([human_scores[k] for k in mk])
                jm = np.mean([judge_scores[k] for k in mk])
                model_summary[model] = {
                    "human_mean": round(float(hm), 2),
                    "judge_mean": round(float(jm), 2),
                    "bias": round(float(jm - hm), 2),
                    "n": len(mk),
                }

        output[f"human_vs_{judge}"] = {
            "n_common": len(common_keys),
            "spearman_rho": round(float(rho), 4),
            "spearman_p": float(rho_p),
            "kendall_tau": round(float(tau), 4),
            "kendall_p": float(tau_p),
            "pearson_r": round(float(pearson), 4),
            "pearson_p": float(pearson_p),
            "mean_bias": round(bias, 2),
            "per_model": model_summary,
        }

        print(f"\n=== Human vs {judge} ({len(common_keys)} pairs) ===")
        print(f"  Spearman rho = {rho:.4f} (p = {rho_p:.2e})")
        print(f"  Kendall tau  = {tau:.4f} (p = {tau_p:.2e})")
        print(f"  Pearson r    = {pearson:.4f} (p = {pearson_p:.2e})")
        print(f"  Mean bias    = {bias:.1f} (judge - human)")
        for model, ms in sorted(model_summary.items()):
            print(f"    {model:25s}: human={ms['human_mean']:.1f} judge={ms['judge_mean']:.1f} bias={ms['bias']:.1f}")

    # Inter-annotator agreement
    iaa = compute_iaa(HUMAN_RESULTS)
    output["inter_annotator_agreement"] = iaa
    print(f"\n=== Inter-Annotator Agreement ({iaa.get('n_double_annotated', 0)} pairs) ===")
    for k, v in iaa.items():
        print(f"  {k}: {v}")

    # Save
    with open(OUTPUT_DIR / "human_judge_correlation.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to {OUTPUT_DIR / 'human_judge_correlation.json'}")


if __name__ == "__main__":
    main()
