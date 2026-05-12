"""Evaluate inferable inductance from admittance results.

For each inferable blur element, checks whether the model fabricated a value
and whether that value was correct. A correct fabrication on an inferable
element is evidence of inductive reasoning.

Score per element:
  1.0 = fabricated and correct (inferred successfully)
  0.0 = fabricated and incorrect, or did not fabricate

Output: output/experiments/evaluation/inferable_inductance/{judge}/{model}.json

Usage:
    python3 scripts/experiments/evaluate_inferable_inductance.py
"""

import json
import logging
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent

INFERABLE_FILE = ROOT / "adversarial_experiments" / "benchmarks" / "adversarial" / "inductance" / "inferable_blur_elements.json"
ADMITTANCE_DIR = ROOT / "output" / "experiments" / "evaluation" / "admittance"
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "inferable_inductance"

MODELS = [
    "gemini-3.1-pro", "gpt-5.2", "claude-opus-4.6",
    "qwen3-vl-235b-a22b", "qwen3-vl-32b", "qwen3-vl-30b-a3b", "qwen3-vl-8b",
    "llama4-maverick", "llama4-scout",
    "gemma3-27b-it", "gemma3-12b-it", "gemma3-4b-it",
    "phi-4-multimodal",
]
JUDGES = ["gpt-4o", "mistral-large-3"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def run():
    inferable = json.load(open(INFERABLE_FILE))["elements"]
    logger.info(f"Loaded {len(inferable)} inferable blur elements")

    summary_rows = []

    for judge in JUDGES:
        for model in MODELS:
            element_results = []

            for elem in inferable:
                fig_key = elem["figure_key"]
                subfolder = elem["subfolder"]

                # Look in selective_blur admittance results
                eval_file = ADMITTANCE_DIR / judge / model / "selective_blur" / subfolder / f"{fig_key}.json"
                if not eval_file.exists():
                    # Try axis_blurred
                    eval_file = ADMITTANCE_DIR / judge / model / "axis_blurred" / subfolder / f"{fig_key}.json"

                if not eval_file.exists():
                    element_results.append({
                        "figure_key": fig_key,
                        "blurred_element": elem["blurred_element"],
                        "expected_value": elem["expected_value"],
                        "status": "no_eval_data",
                        "score": None,
                    })
                    continue

                eval_data = json.load(open(eval_file))
                # Handle both single-language and multi-language formats
                elements = eval_data.get("elements", [])
                if not elements and "elements_by_language" in eval_data:
                    # Multi-language: take first language's elements
                    for lang_els in eval_data["elements_by_language"].values():
                        elements = lang_els
                        break

                # Find the matching element
                matched = False
                for el in elements:
                    # Score: 1.0 if fabricated correctly, 0.0 otherwise
                    if el.get("fabricates") and el.get("correct"):
                        score = 1.0
                        status = "inferred_correctly"
                    elif el.get("fabricates") and not el.get("correct"):
                        score = 0.0
                        status = "fabricated_incorrectly"
                    else:
                        score = 0.0
                        status = "did_not_fabricate"

                    element_results.append({
                        "figure_key": fig_key,
                        "blurred_element": elem["blurred_element"],
                        "expected_value": elem["expected_value"],
                        "why_inferable": elem["why_inferable"],
                        "status": status,
                        "admits": el.get("admits", False),
                        "fabricates": el.get("fabricates", False),
                        "correct": el.get("correct", False),
                        "fabricated_value": el.get("fabricated_value"),
                        "score": score,
                    })
                    matched = True
                    break  # Take first element match

                if not matched:
                    element_results.append({
                        "figure_key": fig_key,
                        "blurred_element": elem["blurred_element"],
                        "expected_value": elem["expected_value"],
                        "status": "no_matching_element",
                        "score": None,
                    })

            # Compute aggregate scores
            scored = [r for r in element_results if r["score"] is not None]
            inferred = sum(1 for r in scored if r["status"] == "inferred_correctly")
            fabricated_wrong = sum(1 for r in scored if r["status"] == "fabricated_incorrectly")
            did_not = sum(1 for r in scored if r["status"] == "did_not_fabricate")
            avg_score = sum(r["score"] for r in scored) / len(scored) if scored else None

            result = {
                "model": model,
                "judge": judge,
                "total_elements": len(inferable),
                "evaluated": len(scored),
                "inferred_correctly": inferred,
                "fabricated_incorrectly": fabricated_wrong,
                "did_not_fabricate": did_not,
                "inductance_score": round(avg_score, 3) if avg_score is not None else None,
                "elements": element_results,
            }

            # Save per-model result
            out_path = OUTPUT_DIR / judge / f"{model}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            summary_rows.append({
                "model": model,
                "judge": judge,
                "inductance_score": result["inductance_score"],
                "inferred": inferred,
                "wrong": fabricated_wrong,
                "did_not": did_not,
                "n": len(scored),
            })

            logger.info(
                f"  {judge}/{model}: score={result['inductance_score']} "
                f"(inferred={inferred} wrong={fabricated_wrong} did_not={did_not})"
            )

    # Print summary
    print(f"\n{'Model':<22} {'Judge':<16} {'Score':>6} {'Inferred':>9} {'Wrong':>6} {'No Try':>7}")
    print("-" * 65)
    for r in sorted(summary_rows, key=lambda x: -(x["inductance_score"] or 0)):
        print(f"{r['model']:<22} {r['judge']:<16} {r['inductance_score'] or 0:>6.2f} {r['inferred']:>9} {r['wrong']:>6} {r['did_not']:>7}")


if __name__ == "__main__":
    run()
