"""RQ1: Process human evaluation results into structured output.

Reads from the Label Studio structured export, applies MQM scoring,
and produces per-model and per-annotator breakdowns.

Output: output/evaluation-results/rq1/human_eval.json
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
STRUCTURED_EXPORT = ROOT / "HumanEval" / "structuring_label_studio_export" / "structured_output" / "annotations_structured.json"
ATOMS_DIR = ROOT / "atomic_mqm" / "atoms"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq1"

CAT_MAP = {
    "cat_accuracy": "Accuracy",
    "cat_completeness": "Completeness",
    "cat_clarity": "Clarity and Readability",
}

MQM_WEIGHTS = {
    ("Accuracy", "Major"): 5.0,
    ("Accuracy", "Minor"): 2.0,
    ("Completeness", "Major"): 3.5,
    ("Completeness", "Minor"): 1.5,
    ("Clarity and Readability", "Major"): 2.0,
    ("Clarity and Readability", "Minor"): 1.0,
}

MODEL_NORM = {
    "gemma3-27b": "gemma3-27b-it",
    "qwen-vl-8b": "qwen3-vl-8b",
    "qwen-vl-30b": "qwen3-vl-30b-a3b",
    "gpt-5.2": "gpt-5.2",
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = json.load(open(STRUCTURED_EXPORT))

    # Load atom counts
    atom_counts = {}
    for f in ATOMS_DIR.glob("*.json"):
        ad = json.load(open(f))
        atom_counts[ad["figure_key"]] = len(ad["atoms"])

    # Process annotations
    all_results = []
    for task in data:
        fig_key = task["data"]["figure_key"]
        raw_model = task["data"]["model_name"]
        model = MODEL_NORM.get(raw_model, raw_model)
        num_atoms = atom_counts.get(fig_key, 20)

        for ann in task["annotations"]:
            annotator_id = ann["annotator_id"]
            spans = ann["spans"]

            errors = []
            for span in spans:
                cat = CAT_MAP.get(span["category"], span["category"])
                sev = span["severity"]
                weight = MQM_WEIGHTS.get((cat, sev), 0.0)
                errors.append({
                    "category": cat,
                    "sub_type": span["subtype"],
                    "severity": sev,
                    "weight": weight,
                    "text_span": span["text"],
                })

            total_penalty = sum(e["weight"] for e in errors)
            max_possible = num_atoms * 5.0
            mqm_score = max(0.0, 100.0 - (total_penalty / max_possible) * 100.0) if max_possible > 0 else 100.0

            all_results.append({
                "figure_key": fig_key,
                "model_name": model,
                "annotator_id": annotator_id,
                "num_atoms": num_atoms,
                "errors": errors,
                "error_count": len(errors),
                "total_penalty": round(total_penalty, 2),
                "mqm_score": round(mqm_score, 2),
            })

    # Model summary
    model_stats = defaultdict(lambda: {"mqm_scores": [], "error_counts": [], "figures": set()})
    for r in all_results:
        s = model_stats[r["model_name"]]
        s["mqm_scores"].append(r["mqm_score"])
        s["error_counts"].append(r["error_count"])
        s["figures"].add(r["figure_key"])

    model_summary = {}
    for model, s in sorted(model_stats.items(), key=lambda x: -np.mean(x[1]["mqm_scores"])):
        model_summary[model] = {
            "n": len(s["mqm_scores"]),
            "num_figures": len(s["figures"]),
            "avg_mqm": round(float(np.mean(s["mqm_scores"])), 2),
            "std_mqm": round(float(np.std(s["mqm_scores"])), 2),
            "avg_errors": round(float(np.mean(s["error_counts"])), 2),
        }

    # Per-annotator breakdown
    annotator_stats = defaultdict(lambda: defaultdict(list))
    for r in all_results:
        annotator_stats[r["annotator_id"]][r["model_name"]].append(r["mqm_score"])

    annotator_summary = {}
    for aid, models in annotator_stats.items():
        annotator_summary[str(aid)] = {
            model: {
                "n": len(scores),
                "avg_mqm": round(float(np.mean(scores)), 2),
            }
            for model, scores in models.items()
        }

    # Error type breakdown
    err_counts = defaultdict(int)
    sev_counts = defaultdict(int)
    for r in all_results:
        for e in r["errors"]:
            err_counts[e["sub_type"]] += 1
            sev_counts[(e["category"], e["severity"])] += 1

    error_subtypes = [
        {"sub_type": st, "count": cnt}
        for st, cnt in sorted(err_counts.items(), key=lambda x: -x[1])
    ]
    category_severity = [
        {"category": cat, "severity": sev, "count": cnt}
        for (cat, sev), cnt in sorted(sev_counts.items(), key=lambda x: -x[1])
    ]

    output = {
        "metadata": {
            "source": "Label Studio structured export",
            "num_figures": len(set(r["figure_key"] for r in all_results)),
            "num_annotations": len(all_results),
            "num_annotators": len(annotator_stats),
            "models": sorted(set(r["model_name"] for r in all_results)),
        },
        "model_summary": model_summary,
        "annotator_summary": annotator_summary,
        "error_subtypes": error_subtypes,
        "category_severity": category_severity,
        "results": all_results,
    }

    with open(OUTPUT_DIR / "human_eval.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print
    print(f"{'Model':25s} {'N':>4s} {'Avg MQM':>8s} {'Avg Errs':>9s}")
    print("-" * 50)
    for model, ms in model_summary.items():
        print(f"{model:25s} {ms['n']:4d} {ms['avg_mqm']:8.1f} {ms['avg_errors']:9.1f}")

    print(f"\nSaved to {OUTPUT_DIR / 'human_eval.json'}")


if __name__ == "__main__":
    main()
