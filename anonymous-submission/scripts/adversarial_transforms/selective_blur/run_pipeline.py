"""
End-to-end selective blur pipeline (OCR-based).

  Stage 1: EasyOCR extracts text + bounding boxes
  Stage 2: GPT-4o selects admittance + inductance targets
  Stage 3: Apply blur to selected regions

Usage:
    python run_pipeline.py --limit 5
    python run_pipeline.py --workers 8
    python run_pipeline.py --skip-ocr       # re-identify + blur only
    python run_pipeline.py --skip-identify   # blur from existing identifications
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--skip-ocr", action="store_true")
    parser.add_argument("--skip-identify", action="store_true")
    args = parser.parse_args()

    shared = []
    if args.limit:
        shared += ["--limit", str(args.limit)]
    if args.figures:
        shared += ["--figures"] + args.figures

    start = time.time()
    print("=" * 60)
    print("  SciFig-Eval: Selective Blur Pipeline (OCR-based)")
    print("=" * 60)

    # Stage 1: OCR
    if not args.skip_ocr:
        if not run_stage("Stage 1: OCR Text Extraction", ["ocr_extract.py"] + shared):
            print("\nAborted: OCR extraction failed.")
            sys.exit(1)

    # Stage 2: Identify
    if not args.skip_identify:
        identify_args = shared + ["--workers", str(args.workers)]
        if not run_stage("Stage 2: Identify Blur Targets (GPT-4o)", ["identify.py"] + identify_args):
            print("\nAborted: identification failed.")
            sys.exit(1)

    # Stage 3: Blur
    run_stage("Stage 3: Apply Selective Blur", ["blur.py"] + shared)

    print(f"\n{'=' * 60}")
    print(f"  Pipeline complete ({time.time() - start:.1f}s)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
