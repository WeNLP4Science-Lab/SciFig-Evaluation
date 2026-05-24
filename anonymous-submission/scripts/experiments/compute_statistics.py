"""Compute all statistics from collected results.

Reads collected_results.json and computes:
  Group 1: Bootstrap confidence intervals
  Group 2: Paired bootstrap significance tests
  Group 3: Effect sizes (Cliff's delta)
  Group 4: Stability (split-half, stratified, saturation)
  Group 5: Ablation statistics

Output: results/statistics/all_statistics.json

Usage:
    python compute_statistics.py
    python compute_statistics.py --bootstrap-n 1000   # faster for testing
"""

from __future__ import annotations

import json
import argparse
import logging
import random
import math
from collections import Counter
from pathlib import Path
from itertools import combinations

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import RESULTS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

STATS_DIR = RESULTS_DIR / "statistics"


# ── Statistical primitives ──

def bootstrap_ci(scores, B=10000, ci=0.95):
    """Bootstrap confidence interval for the mean."""
    if not scores:
        return {"mean": None, "ci_lower": None, "ci_upper": None, "n": 0}

    n = len(scores)
    observed_mean = sum(scores) / n
    means = []
    for _ in range(B):
        sample = [scores[random.randint(0, n - 1)] for _ in range(n)]
        means.append(sum(sample) / n)

    means.sort()
    alpha = (1 - ci) / 2
    lo = means[int(alpha * B)]
    hi = means[int((1 - alpha) * B)]

    return {
        "mean": round(observed_mean, 4),
        "ci_lower": round(lo, 4),
        "ci_upper": round(hi, 4),
        "n": n,
    }


def paired_bootstrap_test(scores_a, scores_b, B=10000):
    """Paired bootstrap test for difference in means."""
    if not scores_a or not scores_b or len(scores_a) != len(scores_b):
        return {"diff": None, "p_value": None, "ci_lower": None, "ci_upper": None, "n": 0}

    n = len(scores_a)
    observed_diff = sum(scores_a) / n - sum(scores_b) / n

    diffs = []
    count_opposite = 0
    for _ in range(B):
        indices = [random.randint(0, n - 1) for _ in range(n)]
        mean_a = sum(scores_a[i] for i in indices) / n
        mean_b = sum(scores_b[i] for i in indices) / n
        d = mean_a - mean_b
        diffs.append(d)
        if observed_diff >= 0 and d <= 0:
            count_opposite += 1
        elif observed_diff < 0 and d >= 0:
            count_opposite += 1

    p_value = count_opposite / B
    diffs.sort()
    ci_lo = diffs[int(0.025 * B)]
    ci_hi = diffs[int(0.975 * B)]

    return {
        "diff": round(observed_diff, 4),
        "p_value": round(p_value, 4),
        "ci_lower": round(ci_lo, 4),
        "ci_upper": round(ci_hi, 4),
        "significant_05": p_value < 0.05,
        "significant_01": p_value < 0.01,
        "significant_001": p_value < 0.001,
        "n": n,
    }


def cliffs_delta(scores_a, scores_b):
    """Cliff's delta effect size for ordinal data."""
    if not scores_a or not scores_b:
        return {"delta": None, "interpretation": None}

    n_a, n_b = len(scores_a), len(scores_b)
    more = sum(1 for a in scores_a for b in scores_b if a > b)
    less = sum(1 for a in scores_a for b in scores_b if a < b)
    delta = (more - less) / (n_a * n_b)

    abs_d = abs(delta)
    if abs_d < 0.147:
        interp = "negligible"
    elif abs_d < 0.33:
        interp = "small"
    elif abs_d < 0.474:
        interp = "medium"
    else:
        interp = "large"

    return {"delta": round(delta, 4), "interpretation": interp}


def spearman_rho(ranks_a, ranks_b):
    """Spearman rank correlation."""
    if len(ranks_a) != len(ranks_b) or len(ranks_a) < 3:
        return None
    n = len(ranks_a)
    d_sq = sum((a - b) ** 2 for a, b in zip(ranks_a, ranks_b))
    rho = 1 - (6 * d_sq) / (n * (n ** 2 - 1))
    return round(rho, 4)


def rank_models(model_scores):
    """Rank models by mean score (highest = rank 1)."""
    means = {m: sum(s) / len(s) for m, s in model_scores.items() if s}
    sorted_models = sorted(means, key=means.get, reverse=True)
    return {m: i + 1 for i, m in enumerate(sorted_models)}


# ── Group 1: Bootstrap CIs ──

def compute_bootstrap_cis(collected, B):
    """Compute bootstrap CIs for all main metrics."""
    logger.info("Group 1: Bootstrap CIs")
    results = {}

    # Baseline MQM
    results["baseline_mqm"] = {}
    for model, entries in collected["baseline_mqm"].items():
        scores = [e["mqm"] for e in entries if e["mqm"] is not None]
        results["baseline_mqm"][model] = bootstrap_ci(scores, B)
    logger.info(f"  Baseline MQM: {len(results['baseline_mqm'])} models")

    # Per-dimension baseline MQM
    results["baseline_mqm_dimensions"] = {}
    for model, entries in collected["baseline_mqm"].items():
        dims = {}
        for dim_key in ["penalty_accuracy", "penalty_completeness", "penalty_clarity"]:
            vals = [e[dim_key] for e in entries if dim_key in e]
            if vals:
                dims[dim_key] = bootstrap_ci(vals, B)
        results["baseline_mqm_dimensions"][model] = dims

    # Per chart type baseline MQM
    results["baseline_mqm_by_chart"] = {}
    for model, entries in collected["baseline_mqm"].items():
        by_type = {}
        for ct in ["Bar Chart", "Line Plot", "Pie Chart"]:
            scores = [e["mqm"] for e in entries if e["chart_type"] == ct and e["mqm"] is not None]
            if scores:
                by_type[ct] = bootstrap_ci(scores, B)
        results["baseline_mqm_by_chart"][model] = by_type

    # Transform MQM
    results["transform_mqm"] = {}
    for transform, model_data in collected["transform_mqm"].items():
        results["transform_mqm"][transform] = {}
        for model, entries in model_data.items():
            scores = [e["mqm"] for e in entries if e["mqm"] is not None]
            results["transform_mqm"][transform][model] = bootstrap_ci(scores, B)
    logger.info(f"  Transform MQM: {len(results['transform_mqm'])} transforms")

    # Resistance overall and per probe type
    results["resistance"] = {}
    results["resistance_by_type"] = {}
    for model, entries in collected["resistance"].items():
        all_scores = []
        by_type = {}
        for e in entries:
            for pt in ["inexist", "contra", "unanswerable"]:
                s = e.get(pt)
                if s is not None:
                    all_scores.append(s)
                    by_type.setdefault(pt, []).append(s)
        results["resistance"][model] = bootstrap_ci(all_scores, B)
        results["resistance_by_type"][model] = {pt: bootstrap_ci(scores, B) for pt, scores in by_type.items()}
    logger.info(f"  Resistance: {len(results['resistance'])} models")

    # Caption bias resistance
    results["caption_bias"] = {}
    for model, entries in collected["caption_bias"].items():
        per_fig_resistance = []
        for e in entries:
            img = e["followed_image"]
            cap = e["followed_caption"]
            if img + cap > 0:
                per_fig_resistance.append(img / (img + cap))
        results["caption_bias"][model] = bootstrap_ci(per_fig_resistance, B)
    logger.info(f"  Caption bias: {len(results['caption_bias'])} models")

    # Caption bias by modification type
    results["caption_bias_by_type"] = {}
    for model, entries in collected["caption_bias"].items():
        by_type = {}
        for e in entries:
            for ev in e.get("evaluations", []):
                t = ev.get("type", "unknown")
                mapped = ev.get("mapped_to", "")
                if mapped in ("image", "caption"):
                    by_type.setdefault(t, []).append(1.0 if mapped == "image" else 0.0)
        results["caption_bias_by_type"][model] = {t: bootstrap_ci(scores, B) for t, scores in by_type.items()}

    # Active probes
    results["active_probes"] = {}
    for probe_type in ["admittance", "inductance"]:
        results["active_probes"][probe_type] = {}
        for model, entries in collected["active_probes"].get(probe_type, {}).items():
            admits_scores = [1.0 if e["admits"] else 0.0 for e in entries]
            fab_scores = [1.0 if e["fabricates"] else 0.0 for e in entries]
            fab_entries = [e for e in entries if e["fabricates"]]
            correct_scores = [1.0 if e["correct"] else 0.0 for e in fab_entries] if fab_entries else []
            results["active_probes"][probe_type][model] = {
                "admits": bootstrap_ci(admits_scores, B),
                "fabricates": bootstrap_ci(fab_scores, B),
                "correct_given_fab": bootstrap_ci(correct_scores, B),
            }
    logger.info(f"  Active probes: done")

    # Passive probes
    results["passive_probes"] = {}
    for probe_type in ["admittance", "inductance"]:
        results["passive_probes"][probe_type] = {}
        for model, entries in collected["passive_probes"].get(probe_type, {}).items():
            mentioned_scores = [1.0 if e.get("mentioned") else 0.0 for e in entries]
            admits_scores = [1.0 if e["admits"] else 0.0 for e in entries]
            fab_scores = [1.0 if e["fabricates"] else 0.0 for e in entries]
            fab_entries = [e for e in entries if e["fabricates"]]
            correct_scores = [1.0 if e["correct"] else 0.0 for e in fab_entries] if fab_entries else []
            results["passive_probes"][probe_type][model] = {
                "mentioned": bootstrap_ci(mentioned_scores, B),
                "admits": bootstrap_ci(admits_scores, B),
                "fabricates": bootstrap_ci(fab_scores, B),
                "correct_given_fab": bootstrap_ci(correct_scores, B),
            }
    logger.info(f"  Passive probes: done")

    # Capability (will be empty if no evaluation results)
    results["capability"] = {}
    for model, entries in collected.get("capability", {}).items():
        if entries:
            results["capability"][model] = {"n": len(entries)}
    if not results["capability"]:
        logger.info("  Capability: no evaluation results (0 for all models)")
    else:
        logger.info(f"  Capability: {len(results['capability'])} models")

    return results


# ── Group 2: Paired bootstrap significance ──

def compute_significance(collected, B):
    """Paired bootstrap significance tests between models."""
    logger.info("Group 2: Significance tests")
    results = {}

    # Baseline MQM significance
    results["baseline_mqm"] = {}
    model_fig_scores = {}
    for model, entries in collected["baseline_mqm"].items():
        model_fig_scores[model] = {e["figure_id"]: e["mqm"] for e in entries if e["mqm"] is not None}

    models = list(model_fig_scores.keys())
    # Find best model
    means = {m: sum(s.values()) / len(s) for m, s in model_fig_scores.items() if s}
    best_model = max(means, key=means.get)

    for model in models:
        if model == best_model:
            continue
        # Get common figures
        common = sorted(set(model_fig_scores[best_model]) & set(model_fig_scores[model]))
        if len(common) < 10:
            continue
        scores_best = [model_fig_scores[best_model][f] for f in common]
        scores_other = [model_fig_scores[model][f] for f in common]
        results["baseline_mqm"][f"{best_model}_vs_{model}"] = paired_bootstrap_test(scores_best, scores_other, B)

    logger.info(f"  Baseline MQM: {len(results['baseline_mqm'])} pairs tested vs {best_model}")

    # Resistance significance
    results["resistance"] = {}
    model_resistance = {}
    for model, entries in collected["resistance"].items():
        fig_scores = {}
        for e in entries:
            scores = [e.get(pt) for pt in ["inexist", "contra", "unanswerable"] if e.get(pt) is not None]
            if scores:
                fig_scores[e["figure_id"]] = sum(scores) / len(scores)
        model_resistance[model] = fig_scores

    means_r = {m: sum(s.values()) / len(s) for m, s in model_resistance.items() if s}
    best_r = max(means_r, key=means_r.get)

    for model in model_resistance:
        if model == best_r:
            continue
        common = sorted(set(model_resistance[best_r]) & set(model_resistance[model]))
        if len(common) < 10:
            continue
        scores_best = [model_resistance[best_r][f] for f in common]
        scores_other = [model_resistance[model][f] for f in common]
        results["resistance"][f"{best_r}_vs_{model}"] = paired_bootstrap_test(scores_best, scores_other, B)

    logger.info(f"  Resistance: {len(results['resistance'])} pairs tested vs {best_r}")

    # Caption bias significance
    results["caption_bias"] = {}
    model_cb = {}
    for model, entries in collected["caption_bias"].items():
        fig_scores = {}
        for e in entries:
            img, cap = e["followed_image"], e["followed_caption"]
            if img + cap > 0:
                fig_scores[e["figure_id"]] = img / (img + cap)
        model_cb[model] = fig_scores

    means_cb = {m: sum(s.values()) / len(s) for m, s in model_cb.items() if s}
    best_cb = max(means_cb, key=means_cb.get)

    for model in model_cb:
        if model == best_cb:
            continue
        common = sorted(set(model_cb[best_cb]) & set(model_cb[model]))
        if len(common) < 10:
            continue
        scores_best = [model_cb[best_cb][f] for f in common]
        scores_other = [model_cb[model][f] for f in common]
        results["caption_bias"][f"{best_cb}_vs_{model}"] = paired_bootstrap_test(scores_best, scores_other, B)

    logger.info(f"  Caption bias: {len(results['caption_bias'])} pairs tested vs {best_cb}")

    return results


# ── Group 3: Effect sizes ──

def compute_effect_sizes(collected):
    """Cliff's delta for key model comparisons."""
    logger.info("Group 3: Effect sizes")
    results = {}

    # Baseline MQM
    results["baseline_mqm"] = {}
    model_scores = {m: [e["mqm"] for e in entries if e["mqm"] is not None]
                    for m, entries in collected["baseline_mqm"].items()}

    for m1, m2 in combinations(model_scores.keys(), 2):
        if model_scores[m1] and model_scores[m2]:
            results["baseline_mqm"][f"{m1}_vs_{m2}"] = cliffs_delta(model_scores[m1], model_scores[m2])

    logger.info(f"  Baseline MQM: {len(results['baseline_mqm'])} pairs")

    # Resistance
    results["resistance"] = {}
    model_r = {}
    for model, entries in collected["resistance"].items():
        scores = []
        for e in entries:
            vals = [e.get(pt) for pt in ["inexist", "contra", "unanswerable"] if e.get(pt) is not None]
            if vals:
                scores.append(sum(vals) / len(vals))
        model_r[model] = scores

    for m1, m2 in combinations(model_r.keys(), 2):
        if model_r[m1] and model_r[m2]:
            results["resistance"][f"{m1}_vs_{m2}"] = cliffs_delta(model_r[m1], model_r[m2])

    logger.info(f"  Resistance: {len(results['resistance'])} pairs")

    return results


# ── Group 4: Stability ──

def compute_stability(collected, B):
    """Split-half reliability, stratified stability, saturation curves."""
    logger.info("Group 4: Stability")
    results = {}

    # Split-half reliability for baseline MQM
    model_fig_scores = {}
    for model, entries in collected["baseline_mqm"].items():
        model_fig_scores[model] = {e["figure_id"]: e["mqm"] for e in entries if e["mqm"] is not None}

    all_figs = set()
    for scores in model_fig_scores.values():
        all_figs.update(scores.keys())
    all_figs = sorted(all_figs)

    rhos = []
    rng = random.Random(42)
    for _ in range(100):
        rng.shuffle(all_figs)
        half1 = set(all_figs[:len(all_figs) // 2])
        half2 = set(all_figs[len(all_figs) // 2:])

        means1 = {}
        means2 = {}
        for model, scores in model_fig_scores.items():
            s1 = [scores[f] for f in half1 if f in scores]
            s2 = [scores[f] for f in half2 if f in scores]
            if s1 and s2:
                means1[model] = sum(s1) / len(s1)
                means2[model] = sum(s2) / len(s2)

        if len(means1) >= 3:
            models_common = sorted(set(means1) & set(means2))
            ranks1 = sorted(range(len(models_common)), key=lambda i: means1[models_common[i]], reverse=True)
            ranks2 = sorted(range(len(models_common)), key=lambda i: means2[models_common[i]], reverse=True)
            rank_map1 = {i: r + 1 for r, i in enumerate(ranks1)}
            rank_map2 = {i: r + 1 for r, i in enumerate(ranks2)}
            r1 = [rank_map1[i] for i in range(len(models_common))]
            r2 = [rank_map2[i] for i in range(len(models_common))]
            rho = spearman_rho(r1, r2)
            if rho is not None:
                rhos.append(rho)

    if rhos:
        rhos.sort()
        results["split_half_mqm"] = {
            "mean_rho": round(sum(rhos) / len(rhos), 4),
            "ci_lower": round(rhos[int(0.025 * len(rhos))], 4),
            "ci_upper": round(rhos[int(0.975 * len(rhos))], 4),
            "n_splits": len(rhos),
        }
        logger.info(f"  Split-half MQM: rho={results['split_half_mqm']['mean_rho']}")

    # Stratified stability (per chart type rankings)
    chart_types = ["Bar Chart", "Line Plot", "Pie Chart"]
    type_rankings = {}
    for ct in chart_types:
        type_means = {}
        for model, entries in collected["baseline_mqm"].items():
            scores = [e["mqm"] for e in entries if e["chart_type"] == ct and e["mqm"] is not None]
            if scores:
                type_means[model] = sum(scores) / len(scores)
        if type_means:
            type_rankings[ct] = rank_models({m: [v] for m, v in type_means.items()})

    results["stratified_rankings"] = type_rankings

    if len(type_rankings) >= 2:
        type_pairs = list(combinations(chart_types, 2))
        results["stratified_rho"] = {}
        for ct1, ct2 in type_pairs:
            if ct1 in type_rankings and ct2 in type_rankings:
                common = sorted(set(type_rankings[ct1]) & set(type_rankings[ct2]))
                if len(common) >= 3:
                    r1 = [type_rankings[ct1][m] for m in common]
                    r2 = [type_rankings[ct2][m] for m in common]
                    rho = spearman_rho(r1, r2)
                    results["stratified_rho"][f"{ct1}_vs_{ct2}"] = rho
        logger.info(f"  Stratified stability: {len(results['stratified_rho'])} pairs")

    # Saturation curve (MQM at incremental sizes)
    # Use sampled_100 figures if available
    sampled_path = Path("dataset/sampled_100.json")
    if sampled_path.exists():
        with open(sampled_path) as f:
            sampled_figs = json.load(f)["figures"]
    else:
        sampled_figs = all_figs[:100]

    sizes = [20, 40, 60, 80, 100]
    results["saturation_mqm"] = {}

    for model, entries in collected["baseline_mqm"].items():
        fig_scores = {e["figure_id"]: e["mqm"] for e in entries
                      if e["figure_id"] in set(sampled_figs) and e["mqm"] is not None}
        available = [f for f in sampled_figs if f in fig_scores]

        curve = {}
        for size in sizes:
            if size > len(available):
                continue
            sample_means = []
            for _ in range(50):
                sample = random.sample(available, size)
                sample_mean = sum(fig_scores[f] for f in sample) / size
                sample_means.append(sample_mean)
            sample_means.sort()
            curve[size] = {
                "mean": round(sum(sample_means) / len(sample_means), 4),
                "ci_lower": round(sample_means[int(0.025 * len(sample_means))], 4),
                "ci_upper": round(sample_means[int(0.975 * len(sample_means))], 4),
            }
        results["saturation_mqm"][model] = curve

    logger.info(f"  Saturation curves: {len(results['saturation_mqm'])} models")

    # Scale validation: resistance on 100 vs 250
    results["scale_validation"] = {}
    sampled_set = set(sampled_figs) if sampled_figs else set()
    for model, entries in collected["resistance"].items():
        scores_100 = []
        scores_250 = []
        for e in entries:
            vals = [e.get(pt) for pt in ["inexist", "contra", "unanswerable"] if e.get(pt) is not None]
            if vals:
                mean_score = sum(vals) / len(vals)
                scores_250.append(mean_score)
                if e["figure_id"] in sampled_set:
                    scores_100.append(mean_score)
        if scores_100 and scores_250:
            results["scale_validation"][model] = {
                "mean_100": round(sum(scores_100) / len(scores_100), 4),
                "mean_250": round(sum(scores_250) / len(scores_250), 4),
                "n_100": len(scores_100),
                "n_250": len(scores_250),
            }
    logger.info(f"  Scale validation: {len(results['scale_validation'])} models")

    return results


# ── Group 5: Ablation ──

def compute_ablation(collected, B):
    """Ablation study statistics (Mistral vs GPT-4o probes)."""
    logger.info("Group 5: Ablation")
    results = {}

    # Resistance ablation
    gpt4o = collected["ablation"].get("resistance_gpt4o_probes", [])
    mistral = collected["ablation"].get("resistance_mistral_probes", [])

    if gpt4o and mistral:
        gpt4o_by_fig = {e["figure_id"]: e for e in gpt4o}
        mistral_by_fig = {e["figure_id"]: e for e in mistral}
        common = sorted(set(gpt4o_by_fig) & set(mistral_by_fig))

        if common:
            scores_g = []
            scores_m = []
            for f in common:
                g = gpt4o_by_fig[f]
                m = mistral_by_fig[f]
                g_vals = [g.get(pt) for pt in ["inexist", "contra", "unanswerable"] if g.get(pt) is not None]
                m_vals = [m.get(pt) for pt in ["inexist", "contra", "unanswerable"] if m.get(pt) is not None]
                if g_vals and m_vals:
                    scores_g.append(sum(g_vals) / len(g_vals))
                    scores_m.append(sum(m_vals) / len(m_vals))

            results["resistance_probe_designer"] = {
                "gpt4o": bootstrap_ci(scores_g, B),
                "mistral": bootstrap_ci(scores_m, B),
                "paired_test": paired_bootstrap_test(scores_g, scores_m, B),
                "effect_size": cliffs_delta(scores_g, scores_m),
            }
            logger.info(f"  Resistance ablation: {len(common)} common figures")

    # Caption bias ablation
    gpt4o_cb = collected["ablation"].get("caption_bias_gpt4o_probes", [])
    mistral_cb = collected["ablation"].get("caption_bias_mistral_probes", [])

    if gpt4o_cb and mistral_cb:
        g_by_fig = {e["figure_id"]: e for e in gpt4o_cb}
        m_by_fig = {e["figure_id"]: e for e in mistral_cb}
        common = sorted(set(g_by_fig) & set(m_by_fig))

        if common:
            scores_g = []
            scores_m = []
            for f in common:
                g_r = g_by_fig[f].get("resistance")
                m_r = m_by_fig[f].get("resistance")
                if g_r is not None and m_r is not None:
                    scores_g.append(g_r)
                    scores_m.append(m_r)

            results["caption_bias_probe_designer"] = {
                "gpt4o": bootstrap_ci(scores_g, B),
                "mistral": bootstrap_ci(scores_m, B),
                "paired_test": paired_bootstrap_test(scores_g, scores_m, B),
                "effect_size": cliffs_delta(scores_g, scores_m),
            }
            logger.info(f"  Caption bias ablation: {len(common)} common figures")

    return results


# ── Main ──

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-n", type=int, default=10000, help="Number of bootstrap resamples")
    args = parser.parse_args()

    B = args.bootstrap_n
    logger.info(f"Bootstrap resamples: {B}")

    collected_path = STATS_DIR / "collected_results.json"
    if not collected_path.exists():
        print("Run collect_results.py first")
        return

    with open(collected_path) as f:
        collected = json.load(f)

    random.seed(42)

    all_stats = {
        "metadata": {
            "bootstrap_n": B,
            "seed": 42,
            "models": collected["metadata"]["models"],
        },
        "bootstrap_cis": compute_bootstrap_cis(collected, B),
        "significance": compute_significance(collected, B),
        "effect_sizes": compute_effect_sizes(collected),
        "stability": compute_stability(collected, B),
        "ablation": compute_ablation(collected, B),
    }

    out_path = STATS_DIR / "all_statistics.json"
    with open(out_path, "w") as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)

    logger.info(f"\nSaved to {out_path}")
    logger.info(f"File size: {out_path.stat().st_size / 1024:.1f} KB")

    # Print key results
    print("\n=== KEY STATISTICS ===")

    print("\nBaseline MQM (mean [95% CI]):")
    for model in collected["metadata"]["models"]:
        ci = all_stats["bootstrap_cis"]["baseline_mqm"].get(model, {})
        if ci.get("mean") is not None:
            print(f"  {model}: {ci['mean']:.1f} [{ci['ci_lower']:.1f}, {ci['ci_upper']:.1f}] (n={ci['n']})")

    print("\nResistance (mean [95% CI]):")
    for model in collected["metadata"]["models"]:
        ci = all_stats["bootstrap_cis"]["resistance"].get(model, {})
        if ci.get("mean") is not None:
            print(f"  {model}: {ci['mean']:.2f} [{ci['ci_lower']:.2f}, {ci['ci_upper']:.2f}] (n={ci['n']})")

    print("\nCaption Bias Resistance (mean [95% CI]):")
    for model in collected["metadata"]["models"]:
        ci = all_stats["bootstrap_cis"]["caption_bias"].get(model, {})
        if ci.get("mean") is not None:
            print(f"  {model}: {ci['mean']:.2f} [{ci['ci_lower']:.2f}, {ci['ci_upper']:.2f}] (n={ci['n']})")

    if "split_half_mqm" in all_stats["stability"]:
        sh = all_stats["stability"]["split_half_mqm"]
        print(f"\nSplit-half reliability (MQM): rho={sh['mean_rho']:.3f} [{sh['ci_lower']:.3f}, {sh['ci_upper']:.3f}]")

    if all_stats["ablation"]:
        print("\nAblation (probe designer):")
        for key in ["resistance_probe_designer", "caption_bias_probe_designer"]:
            if key in all_stats["ablation"]:
                pt = all_stats["ablation"][key]["paired_test"]
                es = all_stats["ablation"][key]["effect_size"]
                print(f"  {key}: diff={pt['diff']:.3f}, p={pt['p_value']:.3f}, delta={es['delta']:.3f} ({es['interpretation']})")


if __name__ == "__main__":
    main()
