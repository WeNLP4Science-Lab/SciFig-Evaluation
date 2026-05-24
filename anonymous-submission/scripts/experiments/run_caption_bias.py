"""Generate descriptions under caption bias condition (poisoned caption).

Passes the modified_caption from caption bias probes instead of the real caption.
The no-caption baseline already exists as the 'original' transform.

Input:  dataset/caption_bias/{fig_id}.json (modified captions)
        dataset/figures/{fig_id}.png
Output: results/generation/caption_bias/{model}/{fig_id}.json

Usage:
    python run_caption_bias.py gpt-5.2 --workers 4
    python run_caption_bias.py gemma3-27b-it
"""

from __future__ import annotations

import json
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import MODELS, FIGURES_DIR, GROUNDTRUTH_DIR, RESULTS_DIR, PROMPTS_DIR, DATASET_DIR
from models import call_vlm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

CAPTION_BIAS_DIR = DATASET_DIR / "caption_bias"
OUTPUT_DIR = RESULTS_DIR / "generation" / "caption_bias"

# ── Prompts ──
PROMPTS = {}

def load_prompts():
    global PROMPTS
    for pfile in PROMPTS_DIR.glob("*.txt"):
        PROMPTS[pfile.stem] = pfile.read_text().strip()

def get_prompt(figure_type: str) -> str:
    type_map = {"Bar Chart": "bar_chart", "Line Plot": "line_plot", "Pie Chart": "pie_chart"}
    return PROMPTS.get(type_map.get(figure_type, "default"), PROMPTS.get("default", ""))


def process_figure(model_name, fig_id):
    out_dir = OUTPUT_DIR / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    fig_path = FIGURES_DIR / f"{fig_id}.png"
    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    bias_path = CAPTION_BIAS_DIR / f"{fig_id}.json"

    if not fig_path.exists():
        return False, "missing_image"
    if not gt_path.exists():
        return False, "missing_gt"
    if not bias_path.exists():
        return False, "missing_bias_probe"

    with open(gt_path) as f:
        gt = json.load(f)
    with open(bias_path) as f:
        bias = json.load(f)

    modified_caption = bias.get("modified_caption", "")
    if not modified_caption:
        return False, "empty_modified_caption"

    prompt = get_prompt(gt["figure_type"])

    # Pass poisoned caption + paper title (same as baseline but with wrong caption)
    user_text = f"Paper: {gt.get('paper_title', '')}\nCaption: {modified_caption}"

    try:
        description = call_vlm(model_name, prompt, fig_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "figure_type": gt["figure_type"],
        "description": description,
        "caption_used": modified_caption,
        "condition": "modified_caption",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id} ({len(description)} chars)")
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

    load_prompts()

    # Default to figures that have caption bias probes
    if args.figures:
        fig_ids = args.figures
    else:
        fig_ids = sorted(p.stem for p in CAPTION_BIAS_DIR.glob("*.json"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (OUTPUT_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Caption bias | model={args.model}")
    logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to process)")

    if not work:
        logger.info("Nothing to do.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    if args.workers == 1:
        for fid in work:
            ok, status = process_figure(args.model, fid)
            if ok: success += 1
            else: errors += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(process_figure, args.model, fid): fid for fid in work}
            for f in as_completed(futs):
                ok, status = f.result()
                with lock:
                    if ok: success += 1
                    else: errors += 1

    logger.info(f"Done. {success} ok, {errors} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
