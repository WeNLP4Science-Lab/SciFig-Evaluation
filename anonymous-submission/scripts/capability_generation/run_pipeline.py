"""
End-to-end capability question generation pipeline.

  Stage 1: Generate questions (GPT-4o) → results/generation/
  Stage 2: Validate (self-consistency + cross-model) → results/validation/
  Stage 3: Filter & finalize → dataset/capability_questions/ + results/report.json

Usage:
    python run_pipeline.py --limit 5          # pilot
    python run_pipeline.py                    # all 250
    python run_pipeline.py --skip-generate    # re-validate + filter only
    python run_pipeline.py --skip-validate    # generate only
    python run_pipeline.py --accept-all       # no cross-model filtering
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_stage(name: str, cmd: list[str]) -> bool:
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}\n")
    start = time.time()
    result = subprocess.run([sys.executable] + cmd, cwd=SCRIPT_DIR)
    elapsed = time.time() - start
    status = "OK" if result.returncode == 0 else "FAILED"
    print(f"\n  [{status}] {name} ({elapsed:.1f}s)")
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run full pipeline")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--skip-validate", action="store_true")
    parser.add_argument("--skip-self", action="store_true")
    parser.add_argument("--skip-cross", action="store_true")
    parser.add_argument("--accept-all", action="store_true")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    shared = []
    if args.limit:
        shared += ["--limit", str(args.limit)]
    if args.figures:
        shared += ["--figures"] + args.figures
    shared += ["--workers", str(args.workers)]

    start = time.time()
    print("=" * 60)
    print("  SciFig-Eval: Capability Question Generation Pipeline")
    print("=" * 60)

    # Stage 1
    if not args.skip_generate:
        if not run_stage("Stage 1: Generate Questions", ["generate.py"] + shared):
            print("\nAborted: generation failed.")
            sys.exit(1)

    # Stage 2
    if not args.skip_validate:
        val_args = shared.copy()
        if args.skip_self:
            val_args.append("--skip-self")
        if args.skip_cross:
            val_args.append("--skip-cross")
        run_stage("Stage 2: Validate Questions", ["validate.py"] + val_args)

        # Stage 3
        filter_args = []
        if args.accept_all:
            filter_args.append("--accept-all")
        run_stage("Stage 3: Filter & Finalize", ["filter.py"] + filter_args)

    print(f"\n{'=' * 60}")
    print(f"  Pipeline complete ({time.time() - start:.1f}s)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
