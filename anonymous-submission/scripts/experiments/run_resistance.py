"""Run resistance (hallucination) probes on original clean images.

Three probe types:
  - inexist:       asks about a non-existent element
  - contra:        states something contradicting the figure
  - unanswerable:  asks something that can't be determined from the figure

Each probe tests whether the model hallucinates or correctly pushes back.

Usage:
    python run_resistance.py gpt-5.2 --workers 4
    python run_resistance.py phi-5 --figures fig_001 fig_005
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

PROBES_DIR = DATASET_DIR / "resistance_probes"
OUTPUT_DIR = RESULTS_DIR / "generation" / "resistance"

SYSTEM_PROMPT = """Please answer the following questions about this figure. Number your answers exactly as 1. 2. 3. with each answer on a new line. Keep each answer concise (1-3 sentences). If a question asks about something not present in the figure, say so clearly."""


def process_figure(model_name, fig_id):
    out_dir = OUTPUT_DIR / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    img_path = FIGURES_DIR / f"{fig_id}.png"
    probe_path = PROBES_DIR / f"{fig_id}.json"

    if not img_path.exists() or not probe_path.exists():
        return False, "missing"

    with open(probe_path) as f:
        probe_data = json.load(f)

    probes = probe_data.get("probes", [])
    if not probes:
        return False, "no_probes"

    # Format all probes as numbered questions
    lines = []
    for i, p in enumerate(probes, 1):
        lines.append(f"{i}. {p['question']}")
    user_text = "\n".join(lines)

    try:
        answer = call_vlm(model_name, SYSTEM_PROMPT, img_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "probes": probes,
        "raw_response": answer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id} ({len(probes)} probes)")
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

    if not PROBES_DIR.exists():
        print(f"Resistance probes not yet generated. Create them in {PROBES_DIR}")
        return

    fig_ids = args.figures or sorted(p.stem for p in PROBES_DIR.glob("*.json"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (OUTPUT_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Resistance probes | model={args.model}")
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
