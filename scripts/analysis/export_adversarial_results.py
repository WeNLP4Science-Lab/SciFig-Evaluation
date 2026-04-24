"""Export aggregated adversarial experiment results for dashboard.

Generates a single JSON with leaderboard tables for each experiment.

Usage:
    python3 scripts/analysis/export_adversarial_results.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DASHBOARD_DATA = ROOT / "dashboard" / "public" / "data"

MODELS = [
    "gemini-3.1-pro", "gpt-5.2", "claude-opus-4.6",
    "qwen3-vl-235b-a22b", "qwen3-vl-32b", "qwen3-vl-30b-a3b", "qwen3-vl-8b",
    "llama4-maverick", "llama4-scout",
    "gemma3-27b-it", "gemma3-12b-it", "gemma3-4b-it",
    "phi-4-multimodal",
]
JUDGES = ["gpt-4o", "mistral-large-3"]


def _avg(vals):
    return round(sum(vals) / len(vals), 3) if vals else None


def capability_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "capability" / judge / model
            if not eval_dir.exists():
                row[judge] = None
                continue
            scores = []
            for f in eval_dir.rglob("*.json"):
                data = json.load(open(f))
                for ev in data.get("evaluations", []):
                    if ev.get("score") is not None and not ev.get("excluded"):
                        scores.append(ev["score"])
            row[judge] = _avg(scores)
        valid = [row[j] for j in JUDGES if row.get(j) is not None]
        row["avg"] = _avg(valid) if valid else None
        rows.append(row)
    return sorted(rows, key=lambda r: r.get("avg") or 0, reverse=True)


def caption_bias_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "caption_bias" / judge / model
            if not eval_dir.exists():
                row[judge] = None
                continue
            a_count = b_count = 0
            for f in eval_dir.rglob("*.json"):
                data = json.load(open(f))
                for ev in data.get("evaluations", []):
                    mapped = ev.get("mapped_to", "")
                    if mapped == "caption":
                        a_count += 1
                    elif mapped == "image":
                        b_count += 1
            total = a_count + b_count
            row[judge] = round(b_count / total, 3) if total > 0 else None
        valid = [row[j] for j in JUDGES if row.get(j) is not None]
        row["avg"] = _avg(valid) if valid else None
        rows.append(row)
    return sorted(rows, key=lambda r: r.get("avg") or 0, reverse=True)


def prompt_reverse_table():
    rows = []
    for model in MODELS:
        pr_dir = ROOT / "output" / "experiments" / "prompt_reverse" / model
        if not pr_dir.exists():
            rows.append({"model": model, "score": None, "correct_consistent": 0, "reversed": 0, "agrees_both": 0})
            continue
        scores = []
        patterns = {"correct_consistent": 0, "reversed": 0, "agrees_both": 0, "disagrees_both": 0}
        for f in pr_dir.rglob("*.json"):
            data = json.load(open(f))
            scores.append(data.get("score", 0))
            p = data.get("pattern", "unknown")
            if p in patterns:
                patterns[p] += 1
        rows.append({
            "model": model,
            "score": _avg(scores),
            "correct_consistent": patterns["correct_consistent"],
            "reversed": patterns["reversed"],
            "agrees_both": patterns["agrees_both"],
        })
    return sorted(rows, key=lambda r: r.get("score") or 0, reverse=True)


def hallucination_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            hallu_dir = ROOT / "output" / "experiments" / "evaluation" / "hallucination" / judge / model
            if not hallu_dir.exists():
                row[f"{judge}_contra"] = None
                row[f"{judge}_inexist"] = None
                row[f"{judge}_unanswerable"] = None
                row[f"{judge}_overall"] = None
                continue
            by_type = {"contra": [], "inexist": [], "unanswerable": []}
            for f in hallu_dir.rglob("*.json"):
                data = json.load(open(f))
                for ev in data.get("evaluations", []):
                    pt = ev.get("probe_type", "")
                    score = ev.get("judge_score")
                    if pt in by_type and score is not None:
                        by_type[pt].append(score)
            row[f"{judge}_contra"] = _avg(by_type["contra"])
            row[f"{judge}_inexist"] = _avg(by_type["inexist"])
            row[f"{judge}_unanswerable"] = _avg(by_type["unanswerable"])
            all_scores = by_type["contra"] + by_type["inexist"] + by_type["unanswerable"]
            row[f"{judge}_overall"] = _avg(all_scores)
        # Compute avg across judges
        for pt in ["contra", "inexist", "unanswerable", "overall"]:
            vals = [row.get(f"{j}_{pt}") for j in JUDGES if row.get(f"{j}_{pt}") is not None]
            row[f"avg_{pt}"] = _avg(vals) if vals else None
        rows.append(row)
    return sorted(rows, key=lambda r: r.get("avg_overall") or 0, reverse=True)


def passive_admittance_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            for blur_type in ["axis_blurred", "selective_blur"]:
                eval_dir = ROOT / "output" / "experiments" / "evaluation" / "admittance" / judge / model / blur_type
                key = f"{judge}_{blur_type}"
                if not eval_dir.exists():
                    row[key] = None
                    row[f"{key}_admits"] = 0
                    row[f"{key}_fabricates"] = 0
                    row[f"{key}_silent"] = 0
                    continue
                scores = []
                admits = fab = silent = fab_correct = fab_incorrect = 0
                for f in eval_dir.rglob("*.json"):
                    data = json.load(open(f))
                    scores.append(data.get("admittance_score", 0))
                    els = data.get("elements", [])
                    if not els:
                        els = [el for lang_els in data.get("elements_by_language", {}).values() for el in lang_els]
                    for el in els:
                        if el.get("admits"): admits += 1
                        if el.get("fabricates"):
                            fab += 1
                            if el.get("correct"): fab_correct += 1
                            else: fab_incorrect += 1
                        if not el.get("mentioned", True): silent += 1
                row[key] = _avg(scores)
                row[f"{key}_admits"] = admits
                row[f"{key}_fabricates"] = fab
                row[f"{key}_silent"] = silent
        rows.append(row)
    return sorted(rows, key=lambda r: (r.get("gpt-4o_selective_blur") or 0), reverse=True)


def active_admittance_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "active_admittance" / judge / model
            if not eval_dir.exists():
                row[f"{judge}_admittance"] = None
                row[f"{judge}_admits"] = 0
                row[f"{judge}_fab_correct"] = 0
                row[f"{judge}_fab_incorrect"] = 0
                continue
            admits = fab_correct = fab_incorrect = total = 0
            for f in eval_dir.rglob("*.json"):
                data = json.load(open(f))
                total += 1
                if data.get("admits"): admits += 1
                if data.get("fabricates"):
                    if data.get("correct"): fab_correct += 1
                    else: fab_incorrect += 1
            row[f"{judge}_admittance"] = round(admits / total, 3) if total > 0 else None
            row[f"{judge}_admits"] = admits
            row[f"{judge}_fab_correct"] = fab_correct
            row[f"{judge}_fab_incorrect"] = fab_incorrect
        valid = [row.get(f"{j}_admittance") for j in JUDGES if row.get(f"{j}_admittance") is not None]
        row["avg"] = _avg(valid) if valid else None
        rows.append(row)
    return sorted(rows, key=lambda r: r.get("avg") or 0, reverse=True)


def transform_mqm_table():
    rows = []
    transforms = ["original", "jpeg_compression", "noise", "aspect_ratio", "low_contrast", "rotation", "original_in_paper", "blurred_in_paper"]
    judge_slugs = {"gpt-4o": "gpt-4o", "mistral-large-3": "mistral-large-3"}
    for model in MODELS:
        row = {"model": model}
        for judge_name, judge_slug in judge_slugs.items():
            eval_dir = ROOT / "output" / "evaluation" / "transforms" / "azure" / judge_slug / model
            if not eval_dir.exists():
                for t in transforms:
                    row[f"{judge_name}_{t}"] = None
                continue
            for t in transforms:
                t_dir = eval_dir / t
                if not t_dir.exists():
                    row[f"{judge_name}_{t}"] = None
                    continue
                scores = []
                for f in t_dir.rglob("*.json"):
                    data = json.load(open(f))
                    s = data.get("mqm_score_avg") or data.get("mqm_score")
                    if s is not None:
                        scores.append(s)
                row[f"{judge_name}_{t}"] = _avg(scores)
        # Compute averages across judges per transform
        for t in transforms:
            vals = [row.get(f"{j}_{t}") for j in judge_slugs if row.get(f"{j}_{t}") is not None]
            row[t] = _avg(vals) if vals else None
        rows.append(row)
    return rows


results = {
    "capability": capability_table(),
    "caption_bias": caption_bias_table(),
    "prompt_reverse": prompt_reverse_table(),
    "hallucination": hallucination_table(),
    "passive_admittance": passive_admittance_table(),
    "active_admittance": active_admittance_table(),
    "transform_mqm": transform_mqm_table(),
    "models": MODELS,
    "judges": JUDGES,
}

out_path = DASHBOARD_DATA / "adversarial_results.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Exported to {out_path}")
for k, v in results.items():
    if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
        print(f"  {k}: {len(v)} rows")


def inductance_table():
    rows = []
    for model in MODELS:
        row = {"model": model}
        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "inductance" / judge / model
            if not eval_dir.exists():
                row[f"{judge}_score"] = None
                row[f"{judge}_trapped"] = None
                row[f"{judge}_correct"] = None
                continue
            scores = []
            trapped = correct = total = 0
            for f in eval_dir.glob("*.json"):
                data = json.load(open(f))
                total += 1
                scores.append(data.get("score", 0))
                if data.get("fell_for_trap"): trapped += 1
                if data.get("correct_answer"): correct += 1
            row[f"{judge}_score"] = _avg(scores)
            row[f"{judge}_trapped"] = trapped
            row[f"{judge}_correct"] = correct
        valid = [row.get(f"{j}_score") for j in JUDGES if row.get(f"{j}_score") is not None]
        row["avg"] = _avg(valid) if valid else None
        rows.append(row)
    return sorted(rows, key=lambda r: r.get("avg") or 0, reverse=True)

results["inductance"] = inductance_table()

# Re-write
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"  inductance: {len(results['inductance'])} rows")
