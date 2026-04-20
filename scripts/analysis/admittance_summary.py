"""Extract and display all Admittance metrics across models and judges.

Tables:
1. Hallucination Unanswerable — does model admit it can't answer?
2. Passive Admittance (axis blur + selective blur) — does model admit blur in descriptions?
3. Active Admittance — does model admit when directly asked about blurred element?

Usage:
    python3 scripts/analysis/admittance_summary.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

MODELS = [
    "gemini-3.1-pro", "gpt-5.2",
    "qwen3-vl-235b-a22b", "qwen3-vl-32b", "qwen3-vl-30b-a3b", "qwen3-vl-8b",
    "llama4-maverick", "llama4-scout",
    "gemma3-27b-it", "gemma3-12b-it", "gemma3-4b-it",
    "phi-4-multimodal",
]
JUDGES = ["gpt-4o", "mistral-large-3"]


def unanswerable_admittance():
    """Table 1: Unanswerable hallucination probes — does model admit it can't answer?"""
    print("=" * 80)
    print("TABLE 1: UNANSWERABLE PROBE ADMITTANCE")
    print("  (Score = model correctly says 'cannot determine from chart')")
    print("=" * 80)
    print(f"{'Model':<25} {'gpt-4o':>10} {'mistral':>10} {'Avg':>10}")
    print("-" * 55)

    for model in MODELS:
        scores = {}
        for judge in JUDGES:
            hallu_dir = ROOT / "output" / "experiments" / "evaluation" / "hallucination" / judge / model
            if not hallu_dir.exists():
                scores[judge] = None
                continue
            vals = []
            for f in sorted(hallu_dir.rglob("*.json")):
                data = json.load(open(f))
                for ev in data.get("evaluations", []):
                    if ev.get("probe_type") == "unanswerable":
                        s = ev.get("judge_score")
                        if s is not None:
                            vals.append(s)
            scores[judge] = sum(vals) / len(vals) if vals else None

        g = scores.get("gpt-4o")
        m = scores.get("mistral-large-3")
        g_str = f"{g:.2f}" if g is not None else "—"
        m_str = f"{m:.2f}" if m is not None else "—"
        valid = [v for v in [g, m] if v is not None]
        avg = sum(valid) / len(valid) if valid else None
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        print(f"{model:<25} {g_str:>10} {m_str:>10} {avg_str:>10}")
    print()


def passive_admittance():
    """Table 2: Passive admittance — axis blur and selective blur descriptions."""
    print("=" * 80)
    print("TABLE 2: PASSIVE ADMITTANCE (from descriptions of blurred images)")
    print("=" * 80)
    print(f"{'Model':<25} {'Axis Blur':>10} {'Sel Blur':>10} {'Admits':>8} {'Fabr':>8} {'Silent':>8} {'Fab✓':>8} {'Fab✗':>8}")
    print("-" * 90)

    for model in MODELS:
        judge = "gpt-4o"
        axis_scores = []
        sel_scores = []
        total_admits = total_fab = total_silent = total_correct = total_incorrect = 0

        for blur_type in ["axis_blurred", "selective_blur"]:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "admittance" / judge / model / blur_type
            if not eval_dir.exists():
                continue
            for f in sorted(eval_dir.rglob("*.json")):
                data = json.load(open(f))
                score = data.get("admittance_score", 0)
                if blur_type == "axis_blurred":
                    axis_scores.append(score)
                else:
                    sel_scores.append(score)

                if "elements" in data:
                    els = data["elements"]
                else:
                    els = [el for lang_els in data.get("elements_by_language", {}).values() for el in lang_els]

                for el in els:
                    if el.get("admits"):
                        total_admits += 1
                    if el.get("fabricates"):
                        total_fab += 1
                        if el.get("correct"):
                            total_correct += 1
                        else:
                            total_incorrect += 1
                    if not el.get("mentioned", True):
                        total_silent += 1

        axis_avg = sum(axis_scores) / len(axis_scores) if axis_scores else None
        sel_avg = sum(sel_scores) / len(sel_scores) if sel_scores else None

        a_str = f"{axis_avg:.2f}" if axis_avg is not None else "—"
        s_str = f"{sel_avg:.2f}" if sel_avg is not None else "—"
        print(f"{model:<25} {a_str:>10} {s_str:>10} {total_admits:>8} {total_fab:>8} {total_silent:>8} {total_correct:>8} {total_incorrect:>8}")
    print()


def active_admittance():
    """Table 3: Active admittance — direct questions about blurred elements."""
    print("=" * 80)
    print("TABLE 3: ACTIVE ADMITTANCE (direct questions about blurred elements)")
    print("=" * 80)
    print(f"{'Model':<25} {'gpt-4o':>8} {'mistral':>8} {'Avg':>8} {'Admits':>8} {'Fab✓':>8} {'Fab✗':>8}")
    print("-" * 75)

    for model in MODELS:
        judge_scores = {}
        total_admits = total_correct = total_incorrect = 0

        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "active_admittance" / judge / model
            if not eval_dir.exists():
                judge_scores[judge] = None
                continue
            admits = fabricates = correct = incorrect = total = 0
            for f in sorted(eval_dir.rglob("*.json")):
                data = json.load(open(f))
                total += 1
                if data.get("admits"):
                    admits += 1
                if data.get("fabricates"):
                    fabricates += 1
                    if data.get("correct"):
                        correct += 1
                    else:
                        incorrect += 1
            judge_scores[judge] = admits / total if total > 0 else None
            if judge == "gpt-4o":
                total_admits = admits
                total_correct = correct
                total_incorrect = incorrect

        g = judge_scores.get("gpt-4o")
        m = judge_scores.get("mistral-large-3")
        g_str = f"{g:.2f}" if g is not None else "—"
        m_str = f"{m:.2f}" if m is not None else "—"
        valid = [v for v in [g, m] if v is not None]
        avg = sum(valid) / len(valid) if valid else None
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        print(f"{model:<25} {g_str:>8} {m_str:>8} {avg_str:>8} {total_admits:>8} {total_correct:>8} {total_incorrect:>8}")
    print()


if __name__ == "__main__":
    unanswerable_admittance()
    passive_admittance()
    active_admittance()
