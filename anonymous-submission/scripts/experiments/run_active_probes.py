"""Run active admittance and inductance probes on selectively blurred images.

Sends the blurred image + a question whose answer depends on the blurred element.
No hint that anything is blurred — the model should answer naturally.

For admittance: answer is unrecoverable (model should admit uncertainty)
For inductance: answer is inferable from context (model should still get it right)

Input:  dataset/adversarial/{admittance,inductance}/{fig_id}.png
        dataset/adversarial/probes/{fig_id}.json (confirmed questions)
Output: results/generation/active_probes/{model}/{probe_type}/{fig_id}.json

Usage:
    python run_active_probes.py gpt-5.2 --type admittance --workers 4
    python run_active_probes.py gpt-5.2 --type inductance --workers 4
    python run_active_probes.py gpt-5.2 --type all --workers 4
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
from config import MODELS, DATASET_DIR, RESULTS_DIR
from models import call_vlm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

ADVERSARIAL_DIR = DATASET_DIR / "adversarial"
PROBES_DIR = ADVERSARIAL_DIR / "probes"
OUTPUT_DIR = RESULTS_DIR / "generation" / "active_probes"

SYSTEM_PROMPT = "Please answer the following question about this figure. Keep your answer concise (1-3 sentences)."


def process_figure(model_name, fig_id, probe_type):
    out_dir = OUTPUT_DIR / model_name / probe_type
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    # Get blurred image
    img_path = ADVERSARIAL_DIR / probe_type / f"{fig_id}.png"
    probe_path = PROBES_DIR / f"{fig_id}.json"

    if not img_path.exists():
        return False, "missing_image"
    if not probe_path.exists():
        return False, "missing_probe"

    with open(probe_path) as f:
        probe = json.load(f)

    sb = probe.get("selective_blur", {}).get(probe_type, {})
    if not sb or sb.get("status") != "confirmed":
        return False, "not_confirmed"

    question = sb.get("question", "")
    if not question:
        return False, "no_question"

    try:
        raw_response = call_vlm(model_name, SYSTEM_PROMPT, img_path, question)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}/{probe_type}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "probe_type": probe_type,
        "question": question,
        "blurred_element": sb.get("blurred_text", ""),
        "expected_answer": sb.get("blurred_text", ""),
        "reviewer_notes": sb.get("reviewer_notes", ""),
        "model_answer": raw_response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}/{probe_type}: {raw_response[:80]}...")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--type", default="all", choices=["admittance", "inductance", "all"])
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.model not in MODELS:
        print(f"Unknown model. Available: {', '.join(sorted(MODELS.keys()))}")
        return

    probe_types = ["admittance", "inductance"] if args.type == "all" else [args.type]

    for probe_type in probe_types:
        # Get confirmed figures
        confirmed_path = DATASET_DIR / f"{probe_type}_confirmed.json"
        if confirmed_path.exists():
            with open(confirmed_path) as f:
                fig_ids = json.load(f)["figures"]
        else:
            # Fallback: find figures with confirmed probes
            fig_ids = []
            for p in PROBES_DIR.glob("*.json"):
                with open(p) as f:
                    probe = json.load(f)
                sb = probe.get("selective_blur", {}).get(probe_type, {})
                if sb.get("status") == "confirmed":
                    fig_ids.append(p.stem)
            fig_ids.sort()

        if args.figures:
            fig_ids = [f for f in args.figures if f in set(fig_ids)]

        work, skipped = [], 0
        for fid in fig_ids:
            if (OUTPUT_DIR / args.model / probe_type / f"{fid}.json").exists():
                skipped += 1
            else:
                work.append(fid)

        logger.info(f"Active {probe_type} | model={args.model}")
        logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to process)")

        if not work:
            logger.info("Nothing to do.")
            continue

        success, errors = 0, 0
        lock = threading.Lock()

        if args.workers == 1:
            for fid in work:
                ok, status = process_figure(args.model, fid, probe_type)
                if ok: success += 1
                else: errors += 1
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = {ex.submit(process_figure, args.model, fid, probe_type): fid for fid in work}
                for f in as_completed(futs):
                    ok, status = f.result()
                    with lock:
                        if ok: success += 1
                        else: errors += 1

        logger.info(f"  {args.model}/{probe_type}: {success} ok, {errors} errors, {skipped} skipped.")

    logger.info("Done.")


if __name__ == "__main__":
    main()
