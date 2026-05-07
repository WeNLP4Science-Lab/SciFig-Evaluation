"""RQ2: Compute transform degradation results.

Extracts per-model per-transform MQM scores, deltas from original,
bootstrap CIs on deltas, and robustness ranking.

Output: output/evaluation-results/rq2/degradation.json
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ADV_RESULTS = ROOT / "dashboard" / "public" / "data" / "adversarial_results.json"
EVAL_DIR = ROOT / "output" / "evaluation" / "transforms"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq2"

TRANSFORMS = [
    "original", "original_in_paper",
    "jpeg_compression", "noise", "aspect_ratio",
    "low_contrast", "rotation", "blurred_in_paper",
]

TRANSFORM_LABELS = {
    "original": "Original",
    "original_in_paper": "In-Paper",
    "jpeg_compression": "JPEG",
    "noise": "Noise",
    "aspect_ratio": "Aspect",
    "low_contrast": "Low Contr.",
    "rotation": "Rotation",
    "blurred_in_paper": "Blur-in-Paper",
}

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


def bootstrap_ci_delta(orig_scores, trans_scores, n_resamples=10000):
    """Bootstrap CI on the mean delta (transform - original)."""
    diffs = np.array(trans_scores) - np.array(orig_scores)
    n = len(diffs)
    if n < 2:
        return float(np.mean(diffs)), float(np.mean(diffs)), float(np.mean(diffs))
    rng = np.random.default_rng(42)
    boot = [np.mean(rng.choice(diffs, size=n, replace=True)) for _ in range(n_resamples)]
    return float(np.mean(diffs)), float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


def load_per_figure_scores():
    """Load per-figure scores from evaluation/transforms for bootstrap."""
    scores = defaultdict(lambda: defaultdict(dict))
    # scores[model][transform][fig_key] = score (judge-averaged)

    for judge_dir in EVAL_DIR.glob("azure/*"):
        judge = judge_dir.name
        for model_dir in judge_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model = model_dir.name
            for transform_dir in model_dir.iterdir():
                if not transform_dir.is_dir():
                    continue
                transform = transform_dir.name
                for f in transform_dir.rglob("*.json"):
                    try:
                        d = json.load(open(f))
                        fig = d["figure_key"]
                        if fig not in scores[model][transform]:
                            scores[model][transform][fig] = []
                        scores[model][transform][fig].append(d["mqm_score"])
                    except Exception:
                        pass

    # Average across judges per figure
    averaged = defaultdict(lambda: defaultdict(dict))
    for model in scores:
        for transform in scores[model]:
            for fig, judge_scores in scores[model][transform].items():
                averaged[model][transform][fig] = np.mean(judge_scores)

    return averaged


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load aggregated data
    adv = json.load(open(ADV_RESULTS))
    tm = adv["transform_mqm"]

    # Load per-figure for bootstrap
    per_fig = load_per_figure_scores()

    results = []
    for row in tm:
        model = row["model"]
        orig = row.get("original", 0)
        entry = {
            "model": model,
            "model_short": MODEL_SHORT.get(model, model),
        }

        for t in TRANSFORMS:
            score = row.get(t, None)
            if score is not None:
                delta = score - orig if t != "original" else 0
                entry[t] = {
                    "score": round(score, 1),
                    "delta": round(delta, 1),
                }

                # Bootstrap CI on delta if we have per-figure data
                if t != "original" and model in per_fig:
                    orig_figs = per_fig[model].get("original", {})
                    trans_figs = per_fig[model].get(t, {})
                    common = sorted(set(orig_figs.keys()) & set(trans_figs.keys()))
                    if len(common) >= 5:
                        o_scores = [orig_figs[f] for f in common]
                        t_scores = [trans_figs[f] for f in common]
                        mean_d, ci_lo, ci_hi = bootstrap_ci_delta(o_scores, t_scores)
                        entry[t]["delta_ci_lo"] = round(ci_lo, 1)
                        entry[t]["delta_ci_hi"] = round(ci_hi, 1)

        # Robustness = mean absolute delta across degradation transforms
        deltas = [abs(entry[t]["delta"]) for t in TRANSFORMS
                  if t not in ("original", "original_in_paper") and t in entry]
        entry["mean_abs_delta"] = round(np.mean(deltas), 1) if deltas else 0
        entry["max_drop"] = round(min(entry[t]["delta"] for t in TRANSFORMS
                                       if t not in ("original",) and t in entry), 1)

        results.append(entry)

    # Sort by robustness (smallest mean_abs_delta = most robust)
    results.sort(key=lambda r: r["mean_abs_delta"])

    # Per-transform average degradation
    transform_summary = {}
    for t in TRANSFORMS:
        if t == "original":
            continue
        deltas = [r[t]["delta"] for r in results if t in r]
        transform_summary[t] = {
            "mean_delta": round(np.mean(deltas), 1),
            "median_delta": round(float(np.median(deltas)), 1),
            "worst_model": min(results, key=lambda r: r.get(t, {}).get("delta", 0))["model"],
            "best_model": max(results, key=lambda r: r.get(t, {}).get("delta", float("-inf")))["model"],
        }

    output = {
        "description": "RQ2: Transform degradation analysis. 45 adversarial figures, 2 judges averaged.",
        "models": results,
        "transform_summary": transform_summary,
    }

    with open(OUTPUT_DIR / "degradation.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print
    print(f"{'Model':22s} {'Orig':>6s} {'InPap':>6s} {'JPEG':>6s} {'Noise':>6s} {'Aspct':>6s} {'LoCon':>6s} {'Rotat':>6s} {'BlurP':>6s} {'|Δ|':>5s}")
    print("-" * 95)
    for r in sorted(results, key=lambda x: -x.get("original", {}).get("score", 0)):
        m = r["model_short"]
        def fmt(t):
            if t not in r: return "   --"
            if t == "original": return f"{r[t]['score']:6.1f}"
            d = r[t]["delta"]
            return f"{d:+5.1f}"
        orig = r.get("original", {}).get("score", 0)
        print(f"{m:22s} {orig:6.1f} {fmt('original_in_paper')} {fmt('jpeg_compression')} {fmt('noise')} {fmt('aspect_ratio')} {fmt('low_contrast')} {fmt('rotation')} {fmt('blurred_in_paper')} {r['mean_abs_delta']:5.1f}")

    print(f"\nTransform severity (mean delta across models):")
    for t in sorted(transform_summary, key=lambda x: transform_summary[x]["mean_delta"]):
        ts = transform_summary[t]
        print(f"  {TRANSFORM_LABELS.get(t,t):15s}: {ts['mean_delta']:+5.1f}")

    print(f"\nSaved to {OUTPUT_DIR / 'degradation.json'}")


if __name__ == "__main__":
    main()
