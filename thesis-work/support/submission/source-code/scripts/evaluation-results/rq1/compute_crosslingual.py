"""RQ1: Compute cross-lingual controlled comparison results.

Uses 13 parallel figures evaluated in 4 languages with language-specific atoms.
Eliminates figure-difficulty confound.

Output: output/evaluation-results/rq1/crosslingual_controlled.json
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CROSS_DIR = ROOT / "output" / "evaluation" / "crosslingual"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq1"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    models_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for judge_dir in sorted(CROSS_DIR.iterdir()):
        if not judge_dir.is_dir():
            continue
        for sub in sorted(judge_dir.iterdir()):
            if not sub.is_dir():
                continue
            judge = f"{judge_dir.name}/{sub.name}"
            for model_dir in sorted(sub.iterdir()):
                if not model_dir.is_dir():
                    continue
                for lang_dir in sorted(model_dir.iterdir()):
                    if not lang_dir.is_dir():
                        continue
                    for f in lang_dir.glob("*.json"):
                        try:
                            d = json.load(open(f))
                            models_data[model_dir.name][judge][lang_dir.name].append(d["mqm_score"])
                        except Exception:
                            pass

    results = {}
    languages = ["English", "Bulgarian", "Chinese", "German"]

    for model in sorted(models_data.keys()):
        avgs = {}
        per_judge = {}
        for lang in languages:
            all_scores = []
            for judge in models_data[model]:
                scores = models_data[model][judge].get(lang, [])
                all_scores.extend(scores)
                if judge not in per_judge:
                    per_judge[judge] = {}
                if scores:
                    per_judge[judge][lang] = round(float(np.mean(scores)), 2)
            if all_scores:
                avgs[lang] = round(float(np.mean(all_scores)), 2)

        en = avgs.get("English", 0)
        gaps = {}
        for lang in ["Bulgarian", "Chinese", "German"]:
            if lang in avgs and en > 0:
                gaps[f"EN-{lang[:2].upper()}"] = round((en - avgs[lang]) / en * 100, 1)

        results[model] = {
            "avg_scores": avgs,
            "per_judge": per_judge,
            "en_x_gaps": gaps,
        }

    output = {
        "description": "Cross-lingual controlled comparison: 13 parallel figures x 4 languages",
        "models": results,
    }

    with open(OUTPUT_DIR / "crosslingual_controlled.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print
    print(f"{'Model':25s} {'EN':>7s} {'BG':>7s} {'CN':>7s} {'DE':>7s} {'EN-BG%':>7s} {'EN-CN%':>7s} {'EN-DE%':>7s}")
    print("-" * 80)
    for model in sorted(results.keys(), key=lambda m: -results[m]["avg_scores"].get("English", 0)):
        r = results[model]
        a = r["avg_scores"]
        g = r["en_x_gaps"]
        print(f"{model:25s} {a.get('English',0):7.1f} {a.get('Bulgarian',0):7.1f} {a.get('Chinese',0):7.1f} {a.get('German',0):7.1f} {g.get('EN-BG','—'):>7} {g.get('EN-CN','—'):>7} {g.get('EN-DE','—'):>7}")

    print(f"\nSaved to {OUTPUT_DIR / 'crosslingual_controlled.json'}")


if __name__ == "__main__":
    main()
