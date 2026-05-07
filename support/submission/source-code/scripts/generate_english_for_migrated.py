"""Generate English annotations for migrated multi_language figures.

For each multi_fig_112..177, checks if "English" key exists in model_annotations.
If not, generates it using the English prompt and merges it into the existing JSON.

Works for both output/generation/ and output/generation_english_prompt/.
For generation_english_prompt, English is NOT generated (it's a cross-language dir
that only handles non-English languages).

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/generate_english_for_migrated.py <model_name> [--workers N]
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth" / "multi_language"
FIGURES_DIR = ROOT / "Dataset" / "figures" / "multi_language"
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

# Only process the migrated figures
MIGRATED_RANGE = range(112, 178)  # multi_fig_112 through multi_fig_177


def _process_figure(annotator, prompts, fig_key, model_output_dir):
    """Generate English annotation for a single figure if missing."""
    gt_path = GROUNDTRUTH_DIR / f"{fig_key}.json"
    fig_path = FIGURES_DIR / f"{fig_key}.png"
    out_path = model_output_dir / "multi_language" / f"{fig_key}.json"

    if not out_path.exists():
        logger.warning(f"  SKIP {fig_key} — output file doesn't exist")
        return True, fig_key, "skip"

    with open(out_path) as f:
        data = json.load(f)

    annotations = data.get("model_annotations", {})
    if "English" in annotations:
        return True, fig_key, "skip"

    with open(gt_path) as f:
        gt = json.load(f)

    prompt_text = get_prompt(prompts, "English", gt["figure_type"])

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

    annotations["English"] = description
    data["model_annotations"] = dict(sorted(annotations.items()))

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK   {fig_key} — English added ({len(description)} chars)")
    return True, fig_key, "done"


def run(model_name: str = "gpt-5.2", workers: int = 1, output_as: str | None = None):
    annotator = get_annotator(model_name)
    prompts = load_prompts()
    output_name = output_as or annotator.model_name
    model_output_dir = OUTPUT_DIR / output_name

    logger.info(f"Model: {annotator.model_name}")
    logger.info(f"Output dir: {model_output_dir}" + (f" (output-as={output_name})" if output_as else ""))
    logger.info(f"Workers: {workers}")
    logger.info(f"Task: Add English annotations to migrated figures (multi_fig_112..177)")
    print()

    # Collect work items
    work_items = []
    skipped = 0
    for i in MIGRATED_RANGE:
        fig_key = f"multi_fig_{i:03d}"
        out_path = model_output_dir / "multi_language" / f"{fig_key}.json"
        if not out_path.exists():
            logger.warning(f"  SKIP {fig_key} — no output file")
            skipped += 1
            continue
        with open(out_path) as f:
            data = json.load(f)
        if "English" in data.get("model_annotations", {}):
            skipped += 1
            continue
        work_items.append(fig_key)

    total = len(work_items) + skipped
    logger.info(f"Total: {total} ({skipped} already have English, {len(work_items)} to generate)")
    print()

    if not work_items:
        logger.info("Nothing to do — all figures already have English annotations.")
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
            done = success + errors - skipped
            if done % 5 == 0 or not ok:
                logger.info(f"  Progress: {done}/{len(work_items)} "
                            f"(success={success - skipped}, errors={errors})")

    if workers == 1:
        for fig_key in work_items:
            ok, key, status = _process_figure(annotator, prompts, fig_key, model_output_dir)
            _on_complete(ok, key, status)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _process_figure, annotator, prompts, fig_key, model_output_dir
                ): fig_key
                for fig_key in work_items
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
    parser = argparse.ArgumentParser(
        description="Generate English annotations for migrated multi_language figures"
    )
    parser.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--output-as", type=str, default=None,
                        help="Write output to this model's directory (e.g. use qwen3-vl-32b-or but save as qwen3-vl-32b)")
    args = parser.parse_args()
    run(args.model, args.workers, args.output_as)
