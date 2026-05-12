"""Export all experimental results into a single JSON for the Final Results dashboard page.

Aggregates: atomic MQM, transforms, capability, hallucination, caption bias,
prompt reverse, admittance, inductance, CoT, and prompt ablation results.

Usage:
    python3 scripts/analysis/export_final_results.py
"""

import json
from pathlib import Path
from collections import defaultdict

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
SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]
TRANSFORMS = ["original", "jpeg_compression", "noise", "aspect_ratio", "low_contrast",
              "rotation", "original_in_paper", "blurred_in_paper"]


def _avg(vals):
    return round(sum(vals) / len(vals), 3) if vals else None


def _load_json_files(directory):
    """Load all JSON files from a directory recursively."""
    results = []
    if not directory.exists():
        return results
    for f in directory.rglob("*.json"):
        try:
            results.append(json.load(open(f)))
        except Exception:
            pass
    return results


# =====================================================================
# 1. Atomic MQM by model, language, transform
# =====================================================================
def atomic_mqm_results():
    base = ROOT / "output" / "evaluation" / "atomic_mqm"
    results = {"by_model_language": [], "by_model_transform": []}

    for judge in ["azure/mistral-large-3"]:
        judge_dir = base / judge.replace("/", "/")
        if not judge_dir.exists():
            continue

        for model in MODELS:
            # By language (original transform)
            model_dir = judge_dir / model / "original"
            if not model_dir.exists():
                continue

            by_lang = {}
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                sub = d.get("subfolder", "unknown")
                by_lang.setdefault(sub, []).append(d)

            for sub, items in by_lang.items():
                results["by_model_language"].append({
                    "model": model,
                    "judge": judge,
                    "language": sub,
                    "n": len(items),
                    "mqm_score": _avg([i["mqm_score"] for i in items]),
                    "atom_accuracy": _avg([i["atom_coverage"]["accuracy"] for i in items]),
                    "atom_completeness": _avg([i["atom_coverage"]["completeness"] for i in items]),
                    "error_count": _avg([i["error_count"] for i in items]),
                })

            # By transform
            for transform in TRANSFORMS:
                t_dir = judge_dir / model / transform
                if not t_dir.exists():
                    continue
                items = _load_json_files(t_dir)
                if items:
                    results["by_model_transform"].append({
                        "model": model,
                        "judge": judge,
                        "transform": transform,
                        "n": len(items),
                        "mqm_score": _avg([i["mqm_score"] for i in items]),
                        "atom_accuracy": _avg([i.get("atom_coverage", {}).get("accuracy", 0) for i in items]),
                        "atom_completeness": _avg([i.get("atom_coverage", {}).get("completeness", 0) for i in items]),
                    })

    return results


# =====================================================================
# 2. Capability Questions
# =====================================================================
def capability_results():
    base = ROOT / "output" / "experiments" / "evaluation" / "capability"
    results = []

    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue

            by_lang = defaultdict(lambda: defaultdict(list))
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                sub = f.parent.name
                for ev in d.get("evaluations", []):
                    s = ev.get("score")
                    t = ev.get("answer_type", "unknown")
                    if s is not None and not ev.get("excluded"):
                        by_lang[sub][t].append(s)
                        by_lang[sub]["all"].append(s)

            for sub, types in by_lang.items():
                row = {"model": model, "judge": judge, "language": sub}
                for t, vals in types.items():
                    row[t] = _avg(vals)
                    row[f"{t}_n"] = len(vals)
                results.append(row)

    return results


# =====================================================================
# 3. Hallucination
# =====================================================================
def hallucination_results():
    base = ROOT / "output" / "experiments" / "evaluation" / "hallucination"
    results = []

    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue

            by_type = defaultdict(list)
            by_lang = defaultdict(lambda: defaultdict(list))
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                sub = f.parent.name
                for ev in d.get("evaluations", []):
                    s = ev.get("score")
                    t = ev.get("probe_type", "unknown")
                    if s is not None:
                        by_type[t].append(s)
                        by_type["all"].append(s)
                        by_lang[sub][t].append(s)
                        by_lang[sub]["all"].append(s)

            row = {"model": model, "judge": judge}
            for t, vals in by_type.items():
                row[t] = _avg(vals)
            results.append(row)

    return results


# =====================================================================
# 4. Caption Bias
# =====================================================================
def caption_bias_results():
    base = ROOT / "output" / "experiments" / "evaluation" / "caption_bias"
    results = []

    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue

            resistances = []
            by_lang = defaultdict(list)
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                r = d.get("resistance")
                if r is not None:
                    resistances.append(r)
                    by_lang[f.parent.name].append(r)

            results.append({
                "model": model,
                "judge": judge,
                "resistance": _avg(resistances),
                "n": len(resistances),
            })

    return results


# =====================================================================
# 5. Prompt Reverse
# =====================================================================
def prompt_reverse_results():
    base = ROOT / "output" / "experiments" / "evaluation" / "prompt_reverse"
    results = []

    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue

            scores = []
            patterns = defaultdict(int)
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                s = d.get("score")
                p = d.get("pattern", "unknown")
                if s is not None:
                    scores.append(s)
                    patterns[p] += 1

            results.append({
                "model": model,
                "judge": judge,
                "score": _avg(scores),
                "n": len(scores),
                "patterns": dict(patterns),
            })

    return results


# =====================================================================
# 6. Admittance (Passive + Active)
# =====================================================================
def admittance_results():
    results = {"passive": [], "active": []}

    # Passive
    base = ROOT / "output" / "experiments" / "evaluation" / "admittance"
    for judge in JUDGES:
        for model in MODELS:
            for blur_type in ["axis_blurred", "selective_blur"]:
                model_dir = base / judge / model / blur_type
                if not model_dir.exists():
                    continue
                admits = fabricates = silent = 0
                for f in model_dir.rglob("*.json"):
                    d = json.load(open(f))
                    for el in d.get("elements", []):
                        if el.get("admits"):
                            admits += 1
                        if el.get("fabricates"):
                            fabricates += 1
                        if el.get("silent"):
                            silent += 1

                total = admits + fabricates + silent
                results["passive"].append({
                    "model": model, "judge": judge, "blur_type": blur_type,
                    "admittance": round(admits / total, 3) if total else None,
                    "admits": admits, "fabricates": fabricates, "silent": silent,
                })

    # Active
    base = ROOT / "output" / "experiments" / "evaluation" / "active_admittance"
    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue
            scores = []
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                s = d.get("admittance_score")
                if s is not None:
                    scores.append(s)
            results["active"].append({
                "model": model, "judge": judge,
                "admittance": _avg(scores),
                "n": len(scores),
            })

    return results


# =====================================================================
# 7. Inductance
# =====================================================================
def inductance_results():
    base = ROOT / "output" / "experiments" / "evaluation" / "inductance"
    results = []

    for judge in JUDGES:
        for model in MODELS:
            model_dir = base / judge / model
            if not model_dir.exists():
                continue
            scores = []
            fell = reasoning = correct = 0
            total = 0
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                s = d.get("score")
                if s is not None:
                    scores.append(s)
                    total += 1
                    if d.get("fell_for_trap"):
                        fell += 1
                    if d.get("showed_reasoning"):
                        reasoning += 1
                    if d.get("correct_answer"):
                        correct += 1

            results.append({
                "model": model, "judge": judge,
                "score": _avg(scores),
                "fell_for_trap": fell, "showed_reasoning": reasoning,
                "correct_answer": correct, "total": total,
            })

    return results


# =====================================================================
# 8. CoT Comparison
# =====================================================================
def cot_results():
    cot_base = ROOT / "output" / "experiments" / "cot" / "evaluation"
    non_cot_base = ROOT / "output" / "experiments" / "evaluation"
    results = []

    experiments = ["capability", "hallucination", "active_admittance", "inductance"]

    for exp in experiments:
        for judge in JUDGES:
            for model in MODELS:
                # Non-CoT
                nc_dir = non_cot_base / exp / judge / model
                nc_scores = []
                if nc_dir.exists():
                    for f in nc_dir.rglob("*.json"):
                        d = json.load(open(f))
                        if exp == "capability":
                            for ev in d.get("evaluations", []):
                                s = ev.get("score")
                                if s is not None:
                                    nc_scores.append(s)
                        elif exp == "active_admittance":
                            s = d.get("admittance_score")
                            if s is not None:
                                nc_scores.append(s)
                        elif exp == "inductance":
                            s = d.get("score")
                            if s is not None:
                                nc_scores.append(s)
                        elif exp == "hallucination":
                            for ev in d.get("evaluations", []):
                                s = ev.get("score")
                                if s is not None:
                                    nc_scores.append(s)

                # CoT
                cot_dir = cot_base / exp / judge / model
                cot_scores = []
                if cot_dir.exists():
                    for f in cot_dir.rglob("*.json"):
                        d = json.load(open(f))
                        if exp == "capability":
                            for ev in d.get("evaluations", []):
                                s = ev.get("score")
                                if s is not None:
                                    cot_scores.append(s)
                        elif exp == "active_admittance":
                            s = d.get("admittance_score")
                            if s is not None:
                                cot_scores.append(s)
                        elif exp == "inductance":
                            s = d.get("score")
                            if s is not None:
                                cot_scores.append(s)
                        elif exp == "hallucination":
                            for ev in d.get("evaluations", []):
                                s = ev.get("score")
                                if s is not None:
                                    cot_scores.append(s)

                if nc_scores or cot_scores:
                    nc_avg = _avg(nc_scores)
                    cot_avg = _avg(cot_scores)
                    delta = round(cot_avg - nc_avg, 3) if nc_avg is not None and cot_avg is not None else None
                    results.append({
                        "model": model, "judge": judge, "experiment": exp,
                        "non_cot": nc_avg, "cot": cot_avg, "delta": delta,
                    })

    return results


# =====================================================================
# 9. Prompt Ablation
# =====================================================================
def prompt_ablation_results():
    results = []

    for condition, label in [
        ("atomic_mqm", "C1_native"),
        ("atomic_mqm_english_prompt", "C2_english"),
        ("atomic_mqm_english_instruction_native_output", "C2p_english_native_out"),
    ]:
        base = ROOT / "output" / "evaluation" / condition / "azure" / "mistral-large-3"
        if not base.exists():
            continue

        for model in MODELS:
            model_dir = base / model / "original"
            if not model_dir.exists():
                continue

            by_lang = defaultdict(list)
            for f in model_dir.rglob("*.json"):
                d = json.load(open(f))
                sub = d.get("subfolder", f.parent.name)
                by_lang[sub].append(d["mqm_score"])

            for sub, scores in by_lang.items():
                results.append({
                    "model": model,
                    "condition": label,
                    "language": sub,
                    "mqm_score": _avg(scores),
                    "n": len(scores),
                })

    return results


# =====================================================================
# Main
# =====================================================================
def main():
    print("Exporting final results...")

    # Load existing adversarial results for experiments already exported correctly
    existing = json.load(open(DASHBOARD_DATA / "adversarial_results.json"))

    data = {
        "models": MODELS,
        "judges": JUDGES,
        # From existing adversarial_results.json (already correct)
        "capability": existing.get("capability", []),
        "caption_bias": existing.get("caption_bias", []),
        "prompt_reverse": existing.get("prompt_reverse", []),
        "hallucination": existing.get("hallucination", []),
        "passive_admittance": existing.get("passive_admittance", []),
        "active_admittance": existing.get("active_admittance", []),
        "inductance": existing.get("inductance", []),
        "transform_mqm": existing.get("transform_mqm", []),
        # New data
        "atomic_mqm": atomic_mqm_results(),
        "capability_by_language": capability_results(),
        "cot_comparison": cot_results(),
        "prompt_ablation": prompt_ablation_results(),
    }

    out = DASHBOARD_DATA / "final_results.json"
    with open(out, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Print summary
    for key, val in data.items():
        if key in ("models", "judges"):
            continue
        if isinstance(val, list):
            print(f"  {key}: {len(val)} rows")
        elif isinstance(val, dict):
            for k2, v2 in val.items():
                print(f"  {key}.{k2}: {len(v2)} rows")


if __name__ == "__main__":
    main()
