"""Run capability questions on original figure images.

Sends the 4 capability questions (counting, computation, comparison, pattern_analysis)
per figure to each model, collects answers.

Reads:  dataset/capability_questions/{fig_id}.json
        dataset/figures/{fig_id}.png

Writes: results/capability/{model}/{fig_id}.json

Usage:
    python run_capability.py gpt-5.2 --workers 4
    python run_capability.py phi-5 --figures fig_001 fig_005
"""

from __future__ import annotations

import json
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import MODELS, FIGURES_DIR, DATASET_DIR, RESULTS_DIR
from models import call_vlm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

QUESTIONS_DIR = DATASET_DIR / "capability_questions"
OUTPUT_DIR = RESULTS_DIR / "generation" / "capability"

SYSTEM_PROMPT = """Please answer each of the following questions about this figure. Number your answers exactly as 1. 2. 3. 4. with each answer on a new line. Keep each answer concise (1-3 sentences)."""


def process_figure(model_name, fig_id):
    out_dir = OUTPUT_DIR / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    img_path = FIGURES_DIR / f"{fig_id}.png"
    q_path = QUESTIONS_DIR / f"{fig_id}.json"

    if not img_path.exists() or not q_path.exists():
        return False, "missing"

    with open(q_path) as f:
        q_data = json.load(f)

    questions = q_data.get("questions", [])
    if not questions:
        return False, "no_questions"

    # Format questions
    lines = []
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q['question']}")
    user_text = "\n".join(lines)

    try:
        raw_response = call_vlm(model_name, SYSTEM_PROMPT, img_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "questions": questions,
        "raw_response": raw_response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id} ({len(questions)} questions)")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.model not in MODELS:
        print(f"Unknown model. Available: {', '.join(sorted(MODELS.keys()))}")
        return

    fig_ids = args.figures or sorted(p.stem for p in QUESTIONS_DIR.glob("*.json"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (OUTPUT_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Capability questions | model={args.model}")
    logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to process)")

    if not work:
        logger.info("Nothing to do.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    if args.workers == 1:
        for fid in work:
            ok, s = process_figure(args.model, fid)
            if ok: success += 1
            else: errors += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(process_figure, args.model, fid): fid for fid in work}
            for f in as_completed(futs):
                ok, s = f.result()
                with lock:
                    if ok: success += 1
                    else: errors += 1

    logger.info(f"Done. {success} ok, {errors} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
