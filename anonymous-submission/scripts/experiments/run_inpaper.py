"""Generate descriptions for in-paper and in-paper-blur transforms.

Unlike other transforms, in-paper images show the full PDF page which may
contain multiple figures. The model needs figure number, caption, and
position hints to identify which figure to describe.

No caption is included in the description prompt (same as other transforms),
but figure identification context IS provided to locate the correct figure.

Input:  dataset/transforms/in_paper/{fig_id}.png
        dataset/transforms/in_paper_blur/{fig_id}.png
Output: results/generation/description_tasks/transforms/{model}/{transform}/{fig_id}.json

Usage:
    python run_inpaper.py gpt-5.2 --transform in_paper --workers 4
    python run_inpaper.py gemma3-27b-it --transform in_paper_blur
    python run_inpaper.py gpt-5.2 --transform all --workers 4
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

TRANSFORMS_DIR = RESULTS_DIR / "generation" / "description_tasks" / "transforms"
IN_PAPER_DIR = DATASET_DIR / "transforms" / "in_paper"
IN_PAPER_BLUR_DIR = DATASET_DIR / "transforms" / "in_paper_blur"

ALL_TRANSFORMS = ["in_paper", "in_paper_blur"]

# ── Prompts ──
PROMPTS = {}

def load_prompts():
    global PROMPTS
    for pfile in PROMPTS_DIR.glob("*.txt"):
        PROMPTS[pfile.stem] = pfile.read_text().strip()

def get_prompt(figure_type: str) -> str:
    type_map = {"Bar Chart": "bar_chart", "Line Plot": "line_plot", "Pie Chart": "pie_chart"}
    return PROMPTS.get(type_map.get(figure_type, "default"), PROMPTS.get("default", ""))


# ── Position hints from Admin reviews ──

def load_position_hints() -> dict:
    """Load Admin position hints from reviews."""
    reviews_path = DATASET_DIR / "capability_answers" / "reviews.json"
    hints = {}
    if not reviews_path.exists():
        return hints

    with open(reviews_path) as f:
        reviews = json.load(f)

    for r in reviews:
        if r.get("annotator") == "Admin" and r.get("notes"):
            notes = r["notes"]
            if any(w in notes.lower() for w in [
                "left", "right", "top", "bottom", "first", "second",
                "1 of", "one of", "plot", "chart", "quadrant", "grid",
                "pair", "middle", "row",
            ]):
                hints[r["figure_id"]] = notes

    return hints


def build_user_text(fig_id: str, gt: dict, position_hints: dict) -> str:
    """Build the user text with figure identification context."""
    fig_num = gt.get("figure_number", "")
    caption = gt.get("caption", "")

    parts = ["This is a full PDF page that may contain multiple figures."]

    # Figure identification
    if fig_id in position_hints:
        hint = position_hints[fig_id]
        parts.append(f"Please describe ONLY {fig_num}. Context: {hint}")
    elif fig_num:
        parts.append(f"Please describe ONLY {fig_num}.")

    # Caption for identification (not for content — model should describe from image)
    if caption:
        parts.append(f'This figure has the caption: "{caption[:200]}"')

    return " ".join(parts)


def process_figure(model_name, fig_id, transform, position_hints):
    out_dir = TRANSFORMS_DIR / model_name / transform
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    # Get image path
    if transform == "in_paper":
        img_path = IN_PAPER_DIR / f"{fig_id}.png"
    elif transform == "in_paper_blur":
        img_path = IN_PAPER_BLUR_DIR / f"{fig_id}.png"
    else:
        return False, "unknown_transform"

    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"

    if not img_path.exists():
        return False, "missing_image"
    if not gt_path.exists():
        return False, "missing_gt"

    with open(gt_path) as f:
        gt = json.load(f)

    prompt = get_prompt(gt["figure_type"])
    user_text = build_user_text(fig_id, gt, position_hints)

    try:
        description = call_vlm(model_name, prompt, img_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}/{transform}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "transform": transform,
        "description": description,
        "figure_type": gt["figure_type"],
        "caption_included": False,
        "figure_context": user_text,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}/{transform} ({len(description)} chars)")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--transform", default="all", help="in_paper, in_paper_blur, or all")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.model not in MODELS:
        print(f"Unknown model. Available: {', '.join(sorted(MODELS.keys()))}")
        return

    load_prompts()
    position_hints = load_position_hints()
    logger.info(f"Loaded {len(position_hints)} position hints")

    transforms = ALL_TRANSFORMS if args.transform == "all" else [args.transform]

    # Default to sampled 100
    if args.figures:
        fig_ids = args.figures
    else:
        sample_path = DATASET_DIR / "sampled_100.json"
        if sample_path.exists():
            with open(sample_path) as f:
                fig_ids = json.load(f)["figures"]
        else:
            fig_ids = sorted(p.stem for p in FIGURES_DIR.glob("*.png"))

    for transform in transforms:
        # Filter to figures that have the transform image
        if transform == "in_paper":
            img_dir = IN_PAPER_DIR
        else:
            img_dir = IN_PAPER_BLUR_DIR

        available = [f for f in fig_ids if (img_dir / f"{f}.png").exists()]

        work, skipped = [], 0
        for fid in available:
            if (TRANSFORMS_DIR / args.model / transform / f"{fid}.json").exists():
                skipped += 1
            else:
                work.append(fid)

        logger.info(f"In-paper [{transform}] | model={args.model}")
        logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to process, {len(fig_ids) - len(available)} missing images)")

        if not work:
            logger.info("Nothing to do.")
            continue

        success, errors = 0, 0
        lock = threading.Lock()

        if args.workers == 1:
            for fid in work:
                ok, status = process_figure(args.model, fid, transform, position_hints)
                if ok: success += 1
                else: errors += 1
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = {ex.submit(process_figure, args.model, fid, transform, position_hints): fid for fid in work}
                for f in as_completed(futs):
                    ok, status = f.result()
                    with lock:
                        if ok: success += 1
                        else: errors += 1

        logger.info(f"  {args.model}/{transform}: {success} ok, {errors} errors, {skipped} skipped.")

    logger.info("Done.")


if __name__ == "__main__":
    main()
