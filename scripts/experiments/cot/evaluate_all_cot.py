"""Evaluate all CoT experiment responses by temporarily patching the evaluator directories.

Runs hallucination, prompt reverse, caption bias, active admittance, and inductance
evaluations on CoT responses, outputting to cot/evaluation/.

Usage:
    python3 scripts/experiments/cot/evaluate_all_cot.py --model gpt-5.2 --judge gpt-4o
    python3 scripts/experiments/cot/evaluate_all_cot.py --model gpt-5.2 --judge mistral-large-3
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "experiments"))

COT_BASE = ROOT / "output" / "experiments" / "cot"


def run_hallucination(model, judge, workers):
    import evaluate_hallucination as eh
    eh.RESPONSES_DIR = COT_BASE / "questions"
    eh.OUTPUT_DIR = COT_BASE / "evaluation" / "hallucination"
    eh.run(model, judge, workers)


def run_prompt_reverse(model, judge, workers):
    import evaluate_prompt_reverse as ep
    ep.RESPONSES_DIR = COT_BASE / "questions"
    ep.OUTPUT_DIR = COT_BASE / "evaluation" / "prompt_reverse"
    ep.run(model, judge, workers)


def run_caption_bias(model, judge, workers):
    import evaluate_caption_bias as ec
    ec.RESPONSES_DIR = COT_BASE / "caption_bias" / "modified_caption"
    ec.OUTPUT_DIR = COT_BASE / "evaluation" / "caption_bias"
    ec.run(model, judge, workers)


def run_active_admittance(model, judge, workers):
    import evaluate_active_admittance as ea
    ea.RESPONSES_DIR = COT_BASE / "active_admittance"
    ea.OUTPUT_DIR = COT_BASE / "evaluation" / "active_admittance"
    ea.run(model, judge, workers)


def run_inductance(model, judge):
    import evaluate_inductance as ei
    ei.RESPONSES_DIR = COT_BASE / "inductance"
    ei.OUTPUT_DIR = COT_BASE / "evaluation" / "inductance"
    ei.run(model, judge)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate all CoT experiments")
    p.add_argument("--model", required=True)
    p.add_argument("--judge", default="gpt-4o")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--experiment", default="all",
                   choices=["all", "hallucination", "prompt_reverse", "caption_bias",
                            "active_admittance", "inductance"])
    a = p.parse_args()

    experiments = {
        "hallucination": lambda: run_hallucination(a.model, a.judge, a.workers),
        "prompt_reverse": lambda: run_prompt_reverse(a.model, a.judge, a.workers),
        "caption_bias": lambda: run_caption_bias(a.model, a.judge, a.workers),
        "active_admittance": lambda: run_active_admittance(a.model, a.judge, a.workers),
        "inductance": lambda: run_inductance(a.model, a.judge),
    }

    if a.experiment == "all":
        for name, fn in experiments.items():
            print(f"\n{'='*60}")
            print(f"CoT Evaluation: {name}")
            print(f"{'='*60}")
            try:
                fn()
            except Exception as e:
                print(f"ERROR in {name}: {e}")
    else:
        experiments[a.experiment]()
