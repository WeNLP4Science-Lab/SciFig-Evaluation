"""RQ1: Compute error type breakdown across models, judges, and languages.

Produces per-model error counts by category/severity/sub-type,
hallucination rates, and judge severity comparison.

Output: output/evaluation-results/rq1/error_analysis.json
"""

import json
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


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load atom metadata
    atom_meta = {}
    for f in ATOMS_DIR.glob("*.json"):
        ad = json.load(open(f))
        atom_meta[ad["figure_key"]] = {
            "figure_type": ad.get("figure_type", "Unknown"),
            "num_atoms": len(ad["atoms"]),
        }

    # Collect all results
    all_data = []
    for judge_dir in sorted(EVAL_DIR.glob("azure/*")):
        judge = judge_dir.name
        for model_dir in judge_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model = model_dir.name
            for f in model_dir.rglob("*.json"):
                try:
                    d = json.load(open(f))
                    d["_judge"] = judge
                    d["_model"] = model
                    d["_fig_type"] = atom_meta.get(d["figure_key"], {}).get("figure_type", "Unknown")
                    d["_lang"] = LANG_MAP.get(d.get("subfolder", ""), "Other")
                    all_data.append(d)
                except Exception:
                    pass

    # 1. Error sub-type breakdown
    subtype_counts = defaultdict(int)
    cat_sev_counts = defaultdict(int)
    total_errors = 0

    for d in all_data:
        for e in d.get("errors", []):
            subtype_counts[e.get("sub_type", "Unknown")] += 1
            cat_sev_counts[(e.get("category", "?"), e.get("severity", "?"))] += 1
            total_errors += 1

    error_subtypes = [
        {"sub_type": st, "count": cnt, "pct": round(cnt / total_errors * 100, 1)}
        for st, cnt in sorted(subtype_counts.items(), key=lambda x: -x[1])
    ]

    category_severity = [
        {"category": cat, "severity": sev, "count": cnt, "pct": round(cnt / total_errors * 100, 1)}
        for (cat, sev), cnt in sorted(cat_sev_counts.items(), key=lambda x: -x[1])
    ]

    # 2. Per-model error profile
    model_profiles = {}
    for model in sorted(set(d["_model"] for d in all_data)):
        model_data = [d for d in all_data if d["_model"] == model]
        n = len(model_data)

        err_counts = defaultdict(int)
        halluc_count = 0
        total_model_errors = 0

        for d in model_data:
            for e in d.get("errors", []):
                key = f"{e.get('category', '?')}/{e.get('severity', '?')}"
                err_counts[key] += 1
                total_model_errors += 1
                if e.get("sub_type") == "Hallucinated Content":
                    halluc_count += 1

        avg_errors = total_model_errors / n if n > 0 else 0

        model_profiles[model] = {
            "n_evaluations": n,
            "total_errors": total_model_errors,
            "avg_errors_per_fig": round(avg_errors, 2),
            "error_breakdown": {k: round(v / n, 2) for k, v in sorted(err_counts.items())},
            "hallucination_count": halluc_count,
            "hallucination_rate": round(halluc_count / n, 3),
        }

    # 3. Judge severity comparison
    judge_profiles = {}
    for judge in sorted(set(d["_judge"] for d in all_data)):
        judge_data = [d for d in all_data if d["_judge"] == judge]
        judge_errors = defaultdict(int)
        judge_total = 0

        for d in judge_data:
            for e in d.get("errors", []):
                key = (e.get("category", "?"), e.get("severity", "?"))
                judge_errors[key] += 1
                judge_total += 1

        major = sum(v for (c, s), v in judge_errors.items() if s == "Major")
        minor = sum(v for (c, s), v in judge_errors.items() if s == "Minor")

        judge_profiles[judge] = {
            "total_errors": judge_total,
            "major_count": major,
            "minor_count": minor,
            "major_pct": round(major / judge_total * 100, 1) if judge_total > 0 else 0,
            "minor_pct": round(minor / judge_total * 100, 1) if judge_total > 0 else 0,
            "breakdown": {
                f"{c}/{s}": {"count": cnt, "pct": round(cnt / judge_total * 100, 1)}
                for (c, s), cnt in sorted(judge_errors.items(), key=lambda x: -x[1])
            },
        }

    # 4. Per figure type
    fig_type_stats = defaultdict(lambda: {"scores": [], "errors": [], "figs": set()})
    for d in all_data:
        ft = d["_fig_type"]
        fig_type_stats[ft]["scores"].append(d["mqm_score"])
        fig_type_stats[ft]["errors"].append(d.get("error_count", len(d.get("errors", []))))
        fig_type_stats[ft]["figs"].add(d["figure_key"])

    figure_types = {}
    for ft, stats_data in fig_type_stats.items():
        scores = stats_data["scores"]
        figure_types[ft] = {
            "n_figures": len(stats_data["figs"]),
            "n_evaluations": len(scores),
            "mean_mqm": round(float(np.mean(scores)), 2),
            "std_mqm": round(float(np.std(scores)), 2),
            "min_mqm": round(float(min(scores)), 2),
            "max_mqm": round(float(max(scores)), 2),
            "mean_errors": round(float(np.mean(stats_data["errors"])), 2),
        }

    # 5. Per language stats
    lang_stats = defaultdict(list)
    for d in all_data:
        lang_stats[d["_lang"]].append(d["mqm_score"])

    language_summary = {}
    for lang in ["EN", "BG", "CN", "DE", "Multi"]:
        scores = lang_stats[lang]
        if scores:
            language_summary[lang] = {
                "n": len(scores),
                "mean": round(float(np.mean(scores)), 2),
                "std": round(float(np.std(scores)), 2),
                "median": round(float(np.median(scores)), 2),
            }

    # Assemble output
    output = {
        "total_evaluations": len(all_data),
        "total_errors": total_errors,
        "mean_errors_per_eval": round(total_errors / len(all_data), 2),
        "error_subtypes": error_subtypes,
        "category_severity": category_severity,
        "model_profiles": model_profiles,
        "judge_severity": judge_profiles,
        "figure_types": figure_types,
        "language_summary": language_summary,
    }

    with open(OUTPUT_DIR / "error_analysis.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print summary
    print(f"Total evaluations: {len(all_data)}")
    print(f"Total errors: {total_errors}")
    print(f"Mean errors/eval: {total_errors / len(all_data):.1f}")

    print(f"\n--- Top Error Sub-types ---")
    for es in error_subtypes[:8]:
        print(f"  {es['sub_type']:45s}: {es['count']:6d} ({es['pct']}%)")

    print(f"\n--- Judge Severity ---")
    for judge, jp in judge_profiles.items():
        print(f"  {judge}: Major={jp['major_pct']}% Minor={jp['minor_pct']}%")

    print(f"\n--- Model Hallucination Rates ---")
    for model in sorted(model_profiles, key=lambda m: model_profiles[m]["hallucination_rate"]):
        mp = model_profiles[model]
        print(f"  {model:25s}: {mp['hallucination_rate']:.3f}/fig ({mp['hallucination_count']} total)")

    print(f"\n--- Figure Types ---")
    for ft in sorted(figure_types, key=lambda x: -figure_types[x]["mean_mqm"]):
        fts = figure_types[ft]
        print(f"  {ft:20s}: MQM={fts['mean_mqm']:.1f} (n={fts['n_figures']} figs)")

    print(f"\n--- Languages ---")
    for lang, ls in language_summary.items():
        print(f"  {lang:6s}: MQM={ls['mean']:.1f} +/- {ls['std']:.1f} (n={ls['n']})")

    print(f"\nSaved to {OUTPUT_DIR / 'error_analysis.json'}")


if __name__ == "__main__":
    main()
