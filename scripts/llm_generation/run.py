"""Runner script for LLM figure description generation.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/llm_generation/run.py <model_name> [--workers N]
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "generation"

sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator
from llm_generation.prompts import load_prompts, get_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SUBFOLDERS = [
    "bulgarian_only",
    "chinese_only",
    "english_only",
    "german_only",
    "multi_language",
]


def _discover_figures(subfolder: str) -> list[str]:
    """Discover all figure keys in a groundtruth subfolder."""
    gt_folder = GROUNDTRUTH_DIR / subfolder
    keys = sorted(p.stem for p in gt_folder.glob("*.json"))
    return keys


def _process_figure(annotator, prompts, subfolder, fig_key, model_output_dir):
    """Process a single figure. Returns (success: bool, fig_key: str)."""
    gt_folder = GROUNDTRUTH_DIR / subfolder
    fig_folder = FIGURES_DIR / subfolder
    out_folder = model_output_dir / subfolder

    gt_path = gt_folder / f"{fig_key}.json"
    fig_path = fig_folder / f"{fig_key}.png"
    out_path = out_folder / f"{fig_key}.json"

    # Re-check skip (race-safe: unique file per figure)
    if out_path.exists():
        return True, fig_key, "skip"

    with open(gt_path) as f:
        gt = json.load(f)

    if subfolder == "multi_language":
        languages = sorted(set(
            a["annotation_language"] for a in gt["annotations"]
        ))
    else:
        languages = [gt["paper_language"]]

    logger.info(f"  [{subfolder}] {fig_key} ({gt['figure_type']}) — languages: {languages}")

    if len(languages) == 1:
        prompt_text = get_prompt(prompts, languages[0], gt["figure_type"])
        try:
            description = annotator.annotate_figure(
                prompt=prompt_text,
                image_path=fig_path,
                caption=gt["caption"],
                paper_title=gt.get("paper_title", ""),
            )
        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")
            return False, fig_key, str(e)

        result = {
            "figure_key": fig_key,
            "task_id": gt["task_id"],
            "arxiv_id": gt.get("arxiv_id"),
            "paper_title": gt.get("paper_title", ""),
            "paper_language": gt["paper_language"],
            "figure_type": gt["figure_type"],
            "caption": gt["caption"],
            "model_name": annotator.model_name,
            "model_annotation": description,
        }
        logger.info(f"  OK   {fig_key} ({len(description)} chars)")

    else:
        annotations_by_lang = {}
        for lang in languages:
            prompt_text = get_prompt(prompts, lang, gt["figure_type"])
            logger.info(f"         generating {lang}...")
            try:
                desc = annotator.annotate_figure(
                    prompt=prompt_text,
                    image_path=fig_path,
                    caption=gt["caption"],
                    paper_title=gt.get("paper_title", ""),
                )
                annotations_by_lang[lang] = desc
                logger.info(f"         {lang}: {len(desc)} chars")
            except Exception as e:
                logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                return False, fig_key, str(e)

        result = {
            "figure_key": fig_key,
            "task_id": gt["task_id"],
            "arxiv_id": gt.get("arxiv_id"),
            "paper_title": gt.get("paper_title", ""),
            "paper_language": gt["paper_language"],
            "figure_type": gt["figure_type"],
            "caption": gt["caption"],
            "model_name": annotator.model_name,
            "model_annotations": annotations_by_lang,
        }
        logger.info(f"  OK   {fig_key} ({len(annotations_by_lang)} languages)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return True, fig_key, "done"


def run(model_name: str = "gpt-5.2", workers: int = 1):
    annotator = get_annotator(model_name)
    prompts = load_prompts()
    model_output_dir = OUTPUT_DIR / annotator.model_name

    logger.info(f"Model: {annotator.model_name}")
    logger.info(f"Output: {model_output_dir}")
    logger.info(f"Workers: {workers}")
    logger.info(f"Loaded {len(prompts)} prompts")
    print()

    # Collect all work items, filtering out already-done and missing files
    work_items = []
    skipped = 0
    for subfolder in SUBFOLDERS:
        gt_folder = GROUNDTRUTH_DIR / subfolder
        fig_folder = FIGURES_DIR / subfolder
        out_folder = model_output_dir / subfolder
        out_folder.mkdir(parents=True, exist_ok=True)

        for fig_key in _discover_figures(subfolder):
            gt_path = gt_folder / f"{fig_key}.json"
            fig_path = fig_folder / f"{fig_key}.png"
            out_path = out_folder / f"{fig_key}.json"

            if not gt_path.exists() or not fig_path.exists():
                logger.warning(f"  SKIP {fig_key} — missing groundtruth or image")
                continue
            if out_path.exists():
                skipped += 1
                continue

            work_items.append((subfolder, fig_key))

    total = len(work_items) + skipped
    logger.info(f"Total figures: {total} ({skipped} already done, {len(work_items)} to process)")
    print()

    if not work_items:
        logger.info("Nothing to do — all figures already generated.")
        return

    success = skipped
    errors = 0
    lock = threading.Lock()

    def _on_complete(ok, fig_key, status):
        nonlocal success, errors
        with lock:
            if ok:
                success += 1
            else:
                errors += 1
            done = success + errors
            if done % 10 == 0 or not ok:
                logger.info(f"  Progress: {done - skipped}/{len(work_items)} "
                            f"(success={success}, errors={errors})")

    if workers == 1:
        for subfolder, fig_key in work_items:
            ok, key, status = _process_figure(
                annotator, prompts, subfolder, fig_key, model_output_dir
            )
            _on_complete(ok, key, status)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _process_figure, annotator, prompts, subfolder, fig_key, model_output_dir
                ): fig_key
                for subfolder, fig_key in work_items
            }
            for future in as_completed(futures):
                try:
                    ok, key, status = future.result()
                    _on_complete(ok, key, status)
                except Exception as e:
                    fig_key = futures[future]
                    logger.error(f"  UNEXPECTED {fig_key}: {e}")
                    with lock:
                        errors += 1

    print()
    logger.info(f"Done. {success}/{total} succeeded, {errors} errors.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate figure descriptions with LLMs")
    parser.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    args = parser.parse_args()
    run(args.model, args.workers)
