"""Run admittance probes — send blurred (admittance) images + questions to models.

The admittance blurred image has an element that is unrecoverable from context.
We ask the model a question whose answer is the blurred element, testing whether
the model hallucinates or honestly reports inability.

Usage:
    python run_admittance.py gpt-5.2 --workers 4
    python run_admittance.py phi-5 --figures fig_001 fig_005
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
from config import MODELS, ADVERSARIAL_DIR, RESULTS_DIR
from models import call_vlm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

ADMITTANCE_DIR = ADVERSARIAL_DIR / "admittance"
PROBES_DIR = ADVERSARIAL_DIR / "probes"
OUTPUT_DIR = RESULTS_DIR / "generation" / "admittance"

SYSTEM_PROMPT = "Please answer the following question about this figure. Keep your answer concise (1-3 sentences)."


def process_figure(model_name, fig_id):
    out_dir = OUTPUT_DIR / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    img_path = ADMITTANCE_DIR / f"{fig_id}.png"
    probe_path = PROBES_DIR / f"{fig_id}.json"

    if not img_path.exists() or not probe_path.exists():
        return False, "missing"

    with open(probe_path) as f:
        probe = json.load(f)

    adm = probe.get("selective_blur", {}).get("admittance", {})
    if not adm:
        return False, "no_admittance_probe"

    question = adm.get("question", "")
    if not question:
        return False, "no_question"

    try:
        answer = call_vlm(model_name, SYSTEM_PROMPT, img_path, question)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "probe_type": "admittance",
        "question": question,
        "expected_answer": adm.get("blurred_text", ""),
        "blurred_element": adm.get("blurred_text", ""),
        "model_answer": answer,
        "expected_behavior": adm.get("expected_behavior", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}: {answer[:80]}...")
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

    fig_ids = args.figures or sorted(p.stem for p in ADMITTANCE_DIR.glob("*.png"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (OUTPUT_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Admittance probes | model={args.model}")
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
