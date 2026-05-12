"""Evaluate CoT capability question responses.

Patches the evaluator directories to read from CoT output.

Usage:
    python3 scripts/experiments/cot/evaluate_capability_cot.py --model gpt-5.2 --judge gpt-4o
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "experiments"))

COT_BASE = ROOT / "output" / "experiments" / "cot"

import evaluate_capability as ec
ec.RESPONSES_DIR = COT_BASE / "questions"
ec.OUTPUT_DIR = COT_BASE / "evaluation" / "capability"

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate CoT capability responses")
    p.add_argument("--model", required=True)
    p.add_argument("--judge", default="gpt-4o")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    ec.run(a.model, a.judge, a.workers, a.subfolder)
