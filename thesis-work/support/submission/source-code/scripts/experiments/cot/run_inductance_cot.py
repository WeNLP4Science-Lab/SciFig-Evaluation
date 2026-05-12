"""Run inductance probes with Chain-of-Thought.

Same as run_inductance.py but adds explicit CoT instruction.
Output: output/experiments/cot/inductance/{model}/{fig_key}.json

Usage:
    python3 scripts/experiments/cot/run_inductance_cot.py --model gpt-5.2
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator, _get_all_models

PROBES_FILE = ROOT / "adversarial_experiments" / "benchmarks" / "adversarial" / "inductance" / "active_inductance_probes.json"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "experiments" / "cot" / "inductance"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

COT_PROMPT = """\
First, describe the visual structure of this figure: identify the chart type, axes, data series, labels, colors, and any notable patterns. Then, answer the following question based on your observations. Let's think step by step."""


def run(model_name):
    with open(PROBES_FILE) as f:
        probes = json.load(f)["probes"]

    annotator = get_annotator(model_name)

    for probe in probes:
        fig_key = probe["figure_key"]
        subfolder = probe["subfolder"]
        question = probe["question"]

        fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
        out_path = OUTPUT_DIR / annotator.model_name / f"{fig_key}.json"

        if out_path.exists():
            logger.info(f"  SKIP {fig_key}")
            continue
        if not fig_path.exists():
            logger.warning(f"  SKIP {fig_key} — no image")
            continue

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
                "trap": probe.get("trap", ""),
                "naive_answer": probe.get("naive_answer", ""),
                "model_answer": raw_response,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"  OK   {fig_key}: {raw_response[:100]}...")

        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")

    logger.info("Done.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="CoT inductance probes")
    p.add_argument("--model", required=True)
    a = p.parse_args()
    run(a.model)
