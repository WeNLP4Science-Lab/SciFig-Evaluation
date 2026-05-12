"""Run active admittance probes with Chain-of-Thought.

Same as run_active_admittance.py but adds CoT instruction.
Output: output/experiments/cot/active_admittance/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/cot/run_active_admittance_cot.py --model gpt-5.2 --workers 4
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator, _get_all_models

PROBES_FILE = ROOT / "adversarial_experiments" / "benchmarks" / "adversarial" / "admittance" / "active_selective_blur_probes.json"
FIGURES_DIR = ROOT / "adversarial_experiments" / "figures"
OUTPUT_DIR = ROOT / "output" / "experiments" / "cot" / "active_admittance"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

COT_PROMPT = """\
First, describe the visual structure of this figure: identify the chart type, axes, data series, labels, colors, and any notable patterns. Then, answer the following question based on your observations. Let's think step by step."""


def _process_figure(annotator, fig_key, probe):
    subfolder = probe["subfolder"]
    question = probe["question"]

    fig_dir = FIGURES_DIR / subfolder / fig_key / "transforms"
    fig_path = None
    for ext in [".png", ".jpeg", ".jpg"]:
        p = fig_dir / f"selective_blur{ext}"
        if p.exists():
            fig_path = p
            break

    if not fig_path:
        return True, fig_key, "skip"

    out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"
    if out_path.exists():
        return True, fig_key, "skip"

    try:
        raw_response = annotator.annotate_figure(
            prompt=COT_PROMPT,
            image_path=fig_path,
            caption=question,
            paper_title="",
        )

        result = {
            "figure_key": fig_key,
            "subfolder": subfolder,
            "model_name": annotator.model_name,
            "mode": "chain_of_thought",
            "question": question,
            "question_english": probe.get("question_english", ""),
            "expected_answer": probe.get("expected_answer", ""),
            "blurred_element": probe.get("blurred_element", ""),
            "model_answer": raw_response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {subfolder}/{fig_key}: {raw_response[:80]}...")
        return True, fig_key, "done"
    except Exception as e:
        logger.error(f"  FAIL {fig_key}: {e}")
        return False, fig_key, str(e)


def run(model_name, workers=4, subfolder_filter=None):
    with open(PROBES_FILE) as f:
        probes = json.load(f)["figures"]

    annotator = get_annotator(model_name)

    work_items = []
    skipped = 0
    for fig_key, probe in sorted(probes.items()):
        if subfolder_filter and probe["subfolder"] != subfolder_filter:
            continue
        out_path = OUTPUT_DIR / annotator.model_name / probe["subfolder"] / f"{fig_key}.json"
        if out_path.exists():
            skipped += 1
        else:
            work_items.append((fig_key, probe))

    logger.info(f"CoT Active admittance | model={annotator.model_name}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to run)")

    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_process_figure, annotator, fk, probe): fk for fk, probe in work_items}
        for f in as_completed(futs):
            try:
                ok, k, s = f.result()
                with lock:
                    if ok: success += 1
                    else: errors += 1
            except Exception as e:
                logger.error(f"  UNEXPECTED: {e}")
                with lock: errors += 1

    logger.info(f"Done. {success}/{len(work_items)+skipped} completed, {errors} errors.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="CoT active admittance probes")
    p.add_argument("--model", required=True)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.workers, a.subfolder)
