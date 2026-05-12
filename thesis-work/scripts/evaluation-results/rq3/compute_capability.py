"""RQ3: Compute capability question results per model, per category, per judge.

Also includes caption bias and prompt reversal scores.

Output: output/evaluation-results/rq3/capability.json
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
EVAL_DIR = ROOT / "output" / "experiments" / "evaluation" / "capability"
QUESTIONS_DIR = ROOT / "adversarial_experiments" / "benchmarks" / "capability"
ADV_RESULTS = ROOT / "dashboard" / "public" / "data" / "adversarial_results.json"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq3"

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2", "gemini-3.1-pro": "Gemini 3.1P",
    "claude-opus-4.6": "Claude 4.6", "qwen3-vl-235b-a22b": "Qwen 235B",
    "qwen3-vl-32b": "Qwen 32B", "qwen3-vl-30b-a3b": "Qwen 30B",
    "qwen3-vl-8b": "Qwen 8B", "llama4-maverick": "LLaMA Mav.",
    "llama4-scout": "LLaMA Scout", "gemma3-27b-it": "Gemma 27B",
    "phi-4-multimodal": "Phi-4", "gemma3-12b-it": "Gemma 12B",
    "gemma3-4b-it": "Gemma 4B",
}

CATEGORIES = ["computation", "value_reading", "comparison", "trend_analysis", "counting"]
CAT_SHORT = {
    "computation": "Comp.", "value_reading": "Value",
    "comparison": "Compar.", "trend_analysis": "Trend", "counting": "Count",
}


def load_question_categories():
    """Map question_id -> category from benchmark files."""
    q_cat = {}
    for f in QUESTIONS_DIR.rglob("*.json"):
        if f.name in ("answer_corrections_log.json", "excluded_questions.json", "post_experiment_changes.json"):
            continue
        try:
            d = json.load(open(f))
            for fig_key, fig_data in d.items():
                if not isinstance(fig_data, dict):
                    continue
                for q in fig_data.get("questions", []):
                    q_cat[q["id"]] = q.get("category", "unknown")
        except Exception:
            pass
    return q_cat


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    q_cat = load_question_categories()

    # Per-model per-judge per-category accuracy
    # results[model][judge][category] = [0/1 list]
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for judge_dir in sorted(EVAL_DIR.iterdir()):
        if not judge_dir.is_dir():
            continue
        judge = judge_dir.name
        for model_dir in sorted(judge_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            model = model_dir.name
            for f in model_dir.rglob("*.json"):
                try:
                    d = json.load(open(f))
                    for ev in d.get("evaluations", []):
                        qid = ev.get("question_id", "")
                        if ev.get("excluded", False):
                            continue
                        score = ev.get("score", 0)
                        correct = 1 if score == 1 else 0
                        cat = q_cat.get(qid, "unknown")
                        results[model][judge][cat].append(correct)
                        results[model][judge]["overall"].append(correct)
                except Exception:
                    pass

    # Load caption bias and prompt reversal from adversarial_results
    adv = json.load(open(ADV_RESULTS))
    cb_data = {r["model"]: r for r in adv["caption_bias"]}
    pr_data = {r["model"]: r for r in adv["prompt_reverse"]}

    # Build output
    model_results = []
    for model in sorted(results.keys()):
        entry = {"model": model, "model_short": MODEL_SHORT.get(model, model)}

        for judge in ["gpt-4o", "mistral-large-3"]:
            for cat in CATEGORIES + ["overall"]:
                scores = results[model][judge].get(cat, [])
                if scores:
                    entry[f"{judge}_{cat}"] = round(np.mean(scores), 3)
                    entry[f"{judge}_{cat}_n"] = len(scores)

        # Judge-averaged per category
        for cat in CATEGORIES + ["overall"]:
            vals = []
            for judge in ["gpt-4o", "mistral-large-3"]:
                v = entry.get(f"{judge}_{cat}")
                if v is not None:
                    vals.append(v)
            if vals:
                entry[f"avg_{cat}"] = round(np.mean(vals), 3)

        # Caption bias
        cb = cb_data.get(model, {})
        entry["caption_bias"] = cb.get("avg")

        # Prompt reversal
        pr = pr_data.get(model, {})
        entry["prompt_reversal"] = pr.get("score")

        model_results.append(entry)

    model_results.sort(key=lambda r: -r.get("avg_overall", 0))

    # Category difficulty
    cat_summary = {}
    for cat in CATEGORIES:
        vals = [r.get(f"avg_{cat}", 0) for r in model_results if r.get(f"avg_{cat}") is not None]
        cat_summary[cat] = {
            "mean": round(np.mean(vals), 3),
            "best_model": max(model_results, key=lambda r: r.get(f"avg_{cat}", 0))["model"],
        }

    output = {
        "description": "RQ3: Capability question accuracy per model, category, judge.",
        "categories": CATEGORIES,
        "models": model_results,
        "category_summary": cat_summary,
    }

    with open(OUTPUT_DIR / "capability.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print
    print(f"{'Model':22s} {'Overall':>7s} {'Comp.':>6s} {'Value':>6s} {'Comp.':>6s} {'Trend':>6s} {'Count':>6s} {'CapBi':>6s} {'PrRev':>6s}")
    print("-" * 75)
    for r in model_results:
        def fmt(k):
            v = r.get(k)
            return f"{v:.2f}" if v is not None else "  --"
        print(f"{r['model_short']:22s} {fmt('avg_overall'):>7s} {fmt('avg_computation'):>6s} {fmt('avg_value_reading'):>6s} {fmt('avg_comparison'):>6s} {fmt('avg_trend_analysis'):>6s} {fmt('avg_counting'):>6s} {fmt('caption_bias'):>6s} {fmt('prompt_reversal'):>6s}")

    print(f"\nCategory difficulty (mean across models):")
    for cat in sorted(cat_summary, key=lambda c: cat_summary[c]["mean"]):
        cs = cat_summary[cat]
        print(f"  {CAT_SHORT[cat]:10s}: {cs['mean']:.3f} (best: {MODEL_SHORT.get(cs['best_model'], cs['best_model'])})")

    print(f"\nSaved to {OUTPUT_DIR / 'capability.json'}")


if __name__ == "__main__":
    main()
