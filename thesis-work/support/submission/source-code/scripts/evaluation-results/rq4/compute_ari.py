"""RQ4: Compute A-R-I behavioural dynamics scores.

Extracts Admittance, Resistance, and Inductance per model.

Output: output/evaluation-results/rq4/ari.json
"""

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ADV_RESULTS = ROOT / "dashboard" / "public" / "data" / "adversarial_results.json"
OUTPUT_DIR = ROOT / "output" / "evaluation-results" / "rq4"

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2", "gemini-3.1-pro": "Gemini 3.1P",
    "claude-opus-4.6": "Claude 4.6", "qwen3-vl-235b-a22b": "Qwen 235B",
    "qwen3-vl-32b": "Qwen 32B", "qwen3-vl-30b-a3b": "Qwen 30B",
    "qwen3-vl-8b": "Qwen 8B", "llama4-maverick": "LLaMA Mav.",
    "llama4-scout": "LLaMA Scout", "gemma3-27b-it": "Gemma 27B",
    "phi-4-multimodal": "Phi-4", "gemma3-12b-it": "Gemma 12B",
    "gemma3-4b-it": "Gemma 4B",
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    adv = json.load(open(ADV_RESULTS))

    pa = {r["model"]: r for r in adv["passive_admittance"]}
    aa = {r["model"]: r for r in adv["active_admittance"]}
    hal = {r["model"]: r for r in adv["hallucination"]}
    ind = {r["model"]: r for r in adv["inductance"]}

    results = []
    for model in sorted(pa.keys()):
        p = pa[model]
        a = aa[model]
        h = hal[model]
        i = ind[model]

        # Admittance: average passive (axis + selective) and active
        passive_axis = np.mean([p.get("gpt-4o_axis_blurred", 0), p.get("mistral-large-3_axis_blurred", 0)])
        passive_sel = np.mean([p.get("gpt-4o_selective_blur", 0), p.get("mistral-large-3_selective_blur", 0)])
        active = a.get("avg", np.mean([a.get("gpt-4o_admittance", 0), a.get("mistral-large-3_admittance", 0)]))
        admittance = np.mean([passive_axis, passive_sel, active])

        # Fabrication counts (judge-averaged)
        fab_axis = np.mean([p.get("gpt-4o_axis_blurred_fabricates", 0), p.get("mistral-large-3_axis_blurred_fabricates", 0)])
        fab_sel = np.mean([p.get("gpt-4o_selective_blur_fabricates", 0), p.get("mistral-large-3_selective_blur_fabricates", 0)])

        # Resistance: hallucination probe resistance (judge-averaged)
        resistance = np.mean([h.get("gpt-4o_overall", 0), h.get("mistral-large-3_overall", 0)])
        contra = np.mean([h.get("gpt-4o_contra", 0), h.get("mistral-large-3_contra", 0)])
        inexist = np.mean([h.get("gpt-4o_inexist", 0), h.get("mistral-large-3_inexist", 0)])
        unans = np.mean([h.get("gpt-4o_unanswerable", 0), h.get("mistral-large-3_unanswerable", 0)])

        # Inductance
        inductance = i.get("avg", 0)

        results.append({
            "model": model,
            "model_short": MODEL_SHORT.get(model, model),
            "admittance": round(admittance, 3),
            "passive_axis": round(passive_axis, 3),
            "passive_selective": round(passive_sel, 3),
            "active": round(active, 3),
            "fab_axis": round(fab_axis, 1),
            "fab_selective": round(fab_sel, 1),
            "resistance": round(resistance, 3),
            "resist_contra": round(contra, 3),
            "resist_inexist": round(inexist, 3),
            "resist_unanswerable": round(unans, 3),
            "inductance": round(inductance, 3),
        })

    results.sort(key=lambda r: -(r["admittance"] + r["resistance"] + r["inductance"]))

    output = {"models": results}
    with open(OUTPUT_DIR / "ari.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print
    print(f"{'Model':22s} {'A':>6s} {'  Pa':>6s} {'  Ps':>6s} {'  Ac':>6s} {'R':>6s} {'  Ct':>6s} {'  In':>6s} {'  Un':>6s} {'I':>6s}")
    print("-" * 80)
    for r in results:
        print(f"{r['model_short']:22s} {r['admittance']:6.2f} {r['passive_axis']:6.2f} {r['passive_selective']:6.2f} {r['active']:6.2f} {r['resistance']:6.2f} {r['resist_contra']:6.2f} {r['resist_inexist']:6.2f} {r['resist_unanswerable']:6.2f} {r['inductance']:6.2f}")

    print(f"\nSaved to {OUTPUT_DIR / 'ari.json'}")


if __name__ == "__main__":
    main()
