"""Extract and display all three Resistance metrics across models and judges.

Tables:
1. Caption Bias Resistance — B/(A+B)
2. Prompt Reverse Resistance — correct+consistent score
3. Hallucination Resistance — contra + inexist probe scores

Usage:
    python3 scripts/analysis/resistance_summary.py
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


def caption_bias_resistance():
    """Table 1: Caption Bias Resistance."""
    print("=" * 80)
    print("TABLE 1: CAPTION BIAS RESISTANCE (B/(A+B))")
    print("=" * 80)
    print(f"{'Model':<25} {'gpt-4o':>10} {'mistral':>10} {'Avg':>10}")
    print("-" * 55)

    for model in MODELS:
        scores = {}
        for judge in JUDGES:
            eval_dir = ROOT / "output" / "experiments" / "evaluation" / "caption_bias" / judge / model
            if not eval_dir.exists():
                scores[judge] = None
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
            scores[judge] = b_count / total if total > 0 else None

        g = scores.get("gpt-4o")
        m = scores.get("mistral-large-3")
        g_str = f"{g:.2f}" if g is not None else "—"
        m_str = f"{m:.2f}" if m is not None else "—"
        avg = sum(v for v in [g, m] if v is not None) / sum(1 for v in [g, m] if v is not None) if any(v is not None for v in [g, m]) else None
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        print(f"{model:<25} {g_str:>10} {m_str:>10} {avg_str:>10}")
    print()


def prompt_reverse_resistance():
    """Table 2: Prompt Reverse Resistance."""
    print("=" * 80)
    print("TABLE 2: PROMPT REVERSE RESISTANCE (sycophancy test)")
    print("=" * 80)
    print(f"{'Model':<25} {'Score':>10} {'Correct':>10} {'Reversed':>10} {'Agrees Both':>10}")
    print("-" * 65)

    for model in MODELS:
        pr_dir = ROOT / "output" / "experiments" / "prompt_reverse" / model
        if not pr_dir.exists():
            print(f"{model:<25} {'—':>10} {'—':>10} {'—':>10} {'—':>10}")
            continue

        scores = []
        patterns = {"correct_consistent": 0, "reversed": 0, "agrees_both": 0, "disagrees_both": 0}
        for f in sorted(pr_dir.rglob("*.json")):
            data = json.load(open(f))
            s = data.get("score", 0)
            p = data.get("pattern", "unknown")
            scores.append(s)
            if p in patterns:
                patterns[p] += 1

        avg = sum(scores) / len(scores) if scores else 0
        total = len(scores)
        cc = patterns["correct_consistent"]
        rv = patterns["reversed"]
        ab = patterns["agrees_both"]
        print(f"{model:<25} {avg:>10.2f} {cc:>10} {rv:>10} {ab:>10}")
    print()


def hallucination_resistance():
    """Table 3: Hallucination Resistance — contra + inexist scores."""
    print("=" * 80)
    print("TABLE 3: HALLUCINATION RESISTANCE (contra + inexist probes)")
    print("=" * 80)
    print(f"{'Model':<25} {'Contra':>8} {'Inexist':>8} {'Unansw':>8} {'Overall':>8}  (gpt-4o judge)")
    print("-" * 65)

    for model in MODELS:
        for judge in ["gpt-4o"]:
            hallu_dir = ROOT / "output" / "experiments" / "evaluation" / "hallucination" / judge / model
            if not hallu_dir.exists():
                print(f"{model:<25} {'—':>8} {'—':>8} {'—':>8} {'—':>8}")
                continue

            by_type = {"contra": [], "inexist": [], "unanswerable": []}
            for f in sorted(hallu_dir.rglob("*.json")):
                data = json.load(open(f))
                for ev in data.get("evaluations", []):
                    pt = ev.get("probe_type", "")
                    score = ev.get("judge_score")
                    if pt in by_type and score is not None:
                        by_type[pt].append(score)

            contra = sum(by_type["contra"]) / len(by_type["contra"]) if by_type["contra"] else None
            inexist = sum(by_type["inexist"]) / len(by_type["inexist"]) if by_type["inexist"] else None
            unansw = sum(by_type["unanswerable"]) / len(by_type["unanswerable"]) if by_type["unanswerable"] else None

            all_scores = by_type["contra"] + by_type["inexist"] + by_type["unanswerable"]
            overall = sum(all_scores) / len(all_scores) if all_scores else None

            c_str = f"{contra:.2f}" if contra is not None else "—"
            i_str = f"{inexist:.2f}" if inexist is not None else "—"
            u_str = f"{unansw:.2f}" if unansw is not None else "—"
            o_str = f"{overall:.2f}" if overall is not None else "—"
            print(f"{model:<25} {c_str:>8} {i_str:>8} {u_str:>8} {o_str:>8}")
    print()


if __name__ == "__main__":
    caption_bias_resistance()
    prompt_reverse_resistance()
    hallucination_resistance()
