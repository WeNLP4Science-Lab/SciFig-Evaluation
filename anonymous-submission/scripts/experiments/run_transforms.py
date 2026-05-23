"""Generate descriptions for transformed images (degradation robustness).

All transforms are run WITHOUT caption — including 'original' which serves
as the caption-free baseline for fair comparison across conditions.

Transforms:
  original          clean image, no caption (baseline)
  noise             Gaussian noise added
  low_contrast      reduced contrast
  rotation          15° rotation
  in_paper          figure embedded in its PDF page
  in_paper_blur     figure blurred within its PDF page
  admittance_blur   selective blur on unrecoverable element
  inductance_blur   selective blur on inferable element

Usage:
    python run_transforms.py gpt-5.2 --transform original --workers 4
    python run_transforms.py phi-5 --transform all --workers 2
    python run_transforms.py gemma3-27b-it --transform noise
"""

from __future__ import annotations

import json
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import cv2
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import MODELS, FIGURES_DIR, GROUNDTRUTH_DIR, RESULTS_DIR, PROMPTS_DIR, ADVERSARIAL_DIR
from models import call_vlm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

TRANSFORMS_DIR = RESULTS_DIR / "generation" / "description_tasks" / "transforms"
ADMITTANCE_DIR = ADVERSARIAL_DIR / "admittance"
INDUCTANCE_DIR = ADVERSARIAL_DIR / "inductance"
IN_PAPER_DIR = DATASET_DIR / "in_paper"
IN_PAPER_BLUR_DIR = DATASET_DIR / "in_paper_blur"

ALL_TRANSFORMS = [
    "original",
    "noise",
    "low_contrast",
    "rotation",
    "in_paper",
    "in_paper_blur",
    "admittance_blur",
    "inductance_blur",
]

# ── Prompts ──
PROMPTS = {}

def load_prompts():
    global PROMPTS
    for pfile in PROMPTS_DIR.glob("*.txt"):
        PROMPTS[pfile.stem] = pfile.read_text().strip()

def get_prompt(figure_type: str) -> str:
    type_map = {"Bar Chart": "bar_chart", "Line Plot": "line_plot", "Pie Chart": "pie_chart"}
    return PROMPTS.get(type_map.get(figure_type, "default"), PROMPTS.get("default", ""))


# ── Image transforms (applied on-the-fly for noise/contrast/rotation) ──

def apply_transform(img_path: str, transform: str, out_path: str) -> bool:
    img = cv2.imread(img_path)
    if img is None:
        return False

    if transform == "noise":
        noise = np.random.normal(0, 25, img.shape).astype(np.int16)
        noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        cv2.imwrite(out_path, noisy)
    elif transform == "rotation":
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 15, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))
        cv2.imwrite(out_path, rotated)
    elif transform == "low_contrast":
        low = cv2.convertScaleAbs(img, alpha=0.3, beta=50)
        cv2.imwrite(out_path, low)
    else:
        return False
    return True


def get_image_path(fig_id: str, transform: str, tmp_dir: Path):
    """Return the image path for a given transform. Creates temp files for on-the-fly transforms."""
    if transform == "original":
        return FIGURES_DIR / f"{fig_id}.png", False
    elif transform == "admittance_blur":
        return ADMITTANCE_DIR / f"{fig_id}.png", False
    elif transform == "inductance_blur":
        return INDUCTANCE_DIR / f"{fig_id}.png", False
    elif transform == "in_paper":
        return IN_PAPER_DIR / f"{fig_id}.png", False
    elif transform == "in_paper_blur":
        return IN_PAPER_BLUR_DIR / f"{fig_id}.png", False
    elif transform in ("noise", "low_contrast", "rotation"):
        src = FIGURES_DIR / f"{fig_id}.png"
        tmp_path = tmp_dir / f"{fig_id}_{transform}.png"
        if apply_transform(str(src), transform, str(tmp_path)):
            return tmp_path, True
        return None, False
    return None, False


def process_figure(model_name, fig_id, transform, tmp_dir):
    out_dir = TRANSFORMS_DIR / model_name / transform
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    if not gt_path.exists():
        return False, "missing_gt"

    img_path, is_temp = get_image_path(fig_id, transform, tmp_dir)
    if img_path is None or not img_path.exists():
        return False, "missing_image"

    with open(gt_path) as f:
        gt = json.load(f)

    prompt = get_prompt(gt["figure_type"])

    # NO caption — image only with paper title for context
    user_text = f"Paper: {gt.get('paper_title', '')}" if gt.get("paper_title") else ""

    try:
        description = call_vlm(model_name, prompt, img_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}/{transform}: {e}")
        return False, str(e)
    finally:
        if is_temp:
            img_path.unlink(missing_ok=True)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "transform": transform,
        "description": description,
        "figure_type": gt["figure_type"],
        "caption_included": False,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}/{transform} ({len(description)} chars)")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--transform", default="all", help="Transform name or 'all'")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.model not in MODELS:
        print(f"Unknown model. Available: {', '.join(sorted(MODELS.keys()))}")
        return

    load_prompts()

    transforms = ALL_TRANSFORMS if args.transform == "all" else [args.transform]
    fig_ids = args.figures or sorted(p.stem for p in FIGURES_DIR.glob("*.png"))

    tmp_dir = RESULTS_DIR / "_tmp_transforms"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Build work items
    work = []
    skipped = 0
    for t in transforms:
        for fid in fig_ids:
            out = TRANSFORMS_DIR / args.model / t / f"{fid}.json"
            if out.exists():
                skipped += 1
            else:
                work.append((fid, t))

    logger.info(f"Transforms (no caption) | model={args.model} | transforms={transforms}")
    logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to process)")

    if not work:
        logger.info("Nothing to do.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    if args.workers == 1:
        for fid, t in work:
            ok, status = process_figure(args.model, fid, t, tmp_dir)
            if ok: success += 1
            else: errors += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(process_figure, args.model, fid, t, tmp_dir): (fid, t) for fid, t in work}
            for f in as_completed(futs):
                try:
                    ok, status = f.result()
                    with lock:
                        if ok: success += 1
                        else: errors += 1
                except Exception as e:
                    logger.error(f"  UNEXPECTED: {e}")
                    with lock: errors += 1

    tmp_dir.rmdir()  # only removes if empty
    logger.info(f"Done. {success} ok, {errors} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
