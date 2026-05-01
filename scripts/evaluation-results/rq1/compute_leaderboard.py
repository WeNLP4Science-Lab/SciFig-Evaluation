"""RQ1: Compute main leaderboard with bootstrap 95% CIs.

Produces the hero table: 13 models x (Overall, EN, BG, CN, DE) with CIs.
Also computes pairwise significance tests and Cliff's delta.

Output: output/evaluation-results/rq1/leaderboard.json
        output/evaluation-results/rq1/pairwise_significance.json
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
EVAL_DIR = ROOT / "output" / "evaluation" / "atomic_mqm_v2"
ATOMS_DIR = ROOT / "atomic_mqm" / "atoms"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq1"


LANG_MAP = {
    "english_only": "EN",
    "bulgarian_only": "BG",
    "chinese_only": "CN",
    "german_only": "DE",
    "multi_language": "Multi",
}


def bootstrap_ci(scores, n_resamples=10000, ci=0.95):
    """Compute BCa-style bootstrap confidence interval."""
    scores = np.array(scores)
    n = len(scores)
    if n < 2:
        m = float(np.mean(scores))
        return m, m, m

    rng = np.random.default_rng(42)
    boot_means = np.array([
        np.mean(rng.choice(scores, size=n, replace=True))
        for _ in range(n_resamples)
    ])

    alpha = (1 - ci) / 2
    lo = float(np.percentile(boot_means, alpha * 100))
    hi = float(np.percentile(boot_means, (1 - alpha) * 100))
    return float(np.mean(scores)), lo, hi


def paired_bootstrap_test(scores_a, scores_b, n_resamples=10000):
    """Test if model A is significantly better than model B."""
    diffs = np.array(scores_a) - np.array(scores_b)
    n = len(diffs)
    observed_diff = np.mean(diffs)

    rng = np.random.default_rng(42)
    count = 0
    for _ in range(n_resamples):
        sample = rng.choice(diffs, size=n, replace=True)
        if sample.mean() <= 0:
            count += 1

    p_value = count / n_resamples
    return float(observed_diff), p_value


def cliffs_delta(x, y):
    """Non-parametric effect size."""
    x, y = np.array(x), np.array(y)
    n_x, n_y = len(x), len(y)
    more = sum(1 for xi in x for yi in y if xi > yi)
    less = sum(1 for xi in x for yi in y if xi < yi)
    return float((more - less) / (n_x * n_y))


def load_all_results():
    """Load all v2 evaluation results."""
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    # results[judge][model][lang] = [scores]

    for judge_dir in sorted(EVAL_DIR.glob("azure/*")):
        judge = judge_dir.name
        for model_dir in judge_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model = model_dir.name
            for f in model_dir.rglob("*.json"):
                try:
                    d = json.load(open(f))
                    sub = d.get("subfolder", "")
                    lang = LANG_MAP.get(sub, "Other")
                    score = d["mqm_score"]
                    results[judge][model][lang].append(score)
                    results[judge][model]["Overall"].append(score)
                except Exception:
                    pass
    return results


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = load_all_results()
    judges = sorted(results.keys())
    languages = ["Overall", "EN", "BG", "CN", "DE", "Multi"]

    # Build leaderboard
    leaderboard = []
    for model in sorted(set(m for j in judges for m in results[j])):
        row = {"model": model}
        for judge in judges:
            for lang in languages:
                scores = results[judge][model].get(lang, [])
                if scores:
                    mean, ci_lo, ci_hi = bootstrap_ci(scores)
                    row[f"{judge}_{lang}"] = {
                        "mean": round(mean, 2),
                        "ci_lo": round(ci_lo, 2),
                        "ci_hi": round(ci_hi, 2),
                        "n": len(scores),
                        "std": round(float(np.std(scores)), 2),
                    }
        # Compute average across judges
        for lang in languages:
            all_judge_scores = []
            for judge in judges:
                all_judge_scores.extend(results[judge][model].get(lang, []))
            if all_judge_scores:
                mean, ci_lo, ci_hi = bootstrap_ci(all_judge_scores)
                row[f"avg_{lang}"] = {
                    "mean": round(mean, 2),
                    "ci_lo": round(ci_lo, 2),
                    "ci_hi": round(ci_hi, 2),
                    "n": len(all_judge_scores),
                }
        leaderboard.append(row)

    # Sort by average overall
    leaderboard.sort(key=lambda r: -r.get("avg_Overall", {}).get("mean", 0))

    # Add rank
    for i, row in enumerate(leaderboard, 1):
        row["rank"] = i

    # Save leaderboard
    with open(OUTPUT_DIR / "leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)

    # Print per-judge leaderboards
    for judge in judges:
        print(f"\n{'='*80}")
        print(f"Judge: {judge}")
        print(f"{'='*80}")
        print(f"{'Rank':>4s} {'Model':25s}", end="")
        for lang in languages:
            print(f" {lang:>12s}", end="")
        print()
        print("-" * (30 + 13 * len(languages)))

        judge_rows = sorted(leaderboard, key=lambda r: -r.get(f"{judge}_Overall", {}).get("mean", 0))
        for i, row in enumerate(judge_rows, 1):
            print(f"{i:4d} {row['model']:25s}", end="")
            for lang in languages:
                v = row.get(f"{judge}_{lang}", {})
                if v:
                    print(f" {v['mean']:5.1f}({v['ci_lo']:.0f}-{v['ci_hi']:.0f})", end="")
                else:
                    print(f" {'—':>12s}", end="")
            print()

    # Print average summary
    print(f"\n{'='*80}")
    print(f"Average across judges")
    print(f"{'='*80}")
    print(f"{'Rank':>4s} {'Model':25s}", end="")
    for lang in languages:
        print(f" {lang:>12s}", end="")
    print()
    print("-" * (30 + 13 * len(languages)))
    for row in leaderboard:
        print(f"{row['rank']:4d} {row['model']:25s}", end="")
        for lang in languages:
            v = row.get(f"avg_{lang}", {})
            if v:
                print(f" {v['mean']:5.1f}({v['ci_lo']:.0f}-{v['ci_hi']:.0f})", end="")
            else:
                print(f" {'—':>12s}", end="")
        print()

    # Pairwise significance tests (adjacent ranks)
    pairwise = []
    for i in range(len(leaderboard) - 1):
        a = leaderboard[i]
        b = leaderboard[i + 1]
        model_a, model_b = a["model"], b["model"]

        # Pool scores across judges for overall
        scores_a, scores_b = [], []
        for judge in judges:
            scores_a.extend(results[judge][model_a].get("Overall", []))
            scores_b.extend(results[judge][model_b].get("Overall", []))

        # Align to same figures (use min length)
        n = min(len(scores_a), len(scores_b))
        if n == 0:
            continue
        scores_a, scores_b = scores_a[:n], scores_b[:n]

        diff, p_val = paired_bootstrap_test(scores_a, scores_b)
        cd = cliffs_delta(scores_a, scores_b)

        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"

        pairwise.append({
            "rank_a": a["rank"],
            "model_a": model_a,
            "rank_b": b["rank"],
            "model_b": model_b,
            "mean_diff": round(diff, 2),
            "p_value": round(p_val, 4),
            "cliffs_delta": round(cd, 3),
            "significance": sig,
        })

    with open(OUTPUT_DIR / "pairwise_significance.json", "w") as f:
        json.dump(pairwise, f, indent=2)

    print(f"\n{'Model A':25s} vs {'Model B':25s} {'Diff':>6s} {'p':>7s} {'Cliff':>7s} {'Sig':>4s}")
    print("-" * 80)
    for p in pairwise:
        print(f"{p['model_a']:25s} vs {p['model_b']:25s} {p['mean_diff']:6.1f} {p['p_value']:7.4f} {p['cliffs_delta']:7.3f} {p['significance']:>4s}")

    print(f"\nSaved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
