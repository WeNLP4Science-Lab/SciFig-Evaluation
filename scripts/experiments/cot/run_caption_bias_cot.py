"""Generate figure descriptions under caption bias conditions with Chain-of-Thought.

Same as run_caption_bias.py but prepends a CoT instruction to the generation prompt.
Output: output/experiments/cot/caption_bias/<condition>/<model>/<subfolder>/<fig_key>.json

Usage:
    python3 scripts/experiments/cot/run_caption_bias_cot.py gpt-5.2 --condition modified_caption --workers 4
    python3 scripts/experiments/cot/run_caption_bias_cot.py gpt-5.2 --condition image_only --workers 4
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator, _get_all_models
from llm_generation.prompts import load_prompts, get_prompt

ADVERSARIAL_DIR = ROOT / "adversarial_experiments"
SAMPLES_FILE = ADVERSARIAL_DIR / "samples.json"
FIGURES_DIR = ADVERSARIAL_DIR / "figures"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
CAPTION_BIAS_DIR = ADVERSARIAL_DIR / "benchmarks" / "adversarial" / "caption_bias"
OUTPUT_DIR = ROOT / "output" / "experiments" / "cot" / "caption_bias"

CONDITIONS = ["modified_caption", "image_only"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

COT_PREFIX = """\
First, describe the visual structure of this figure: identify the chart type, axes, data series, labels, colors, and any notable patterns. Let's think step by step.

After your reasoning, write your final description on a new line starting with "DESCRIPTION:" — only the text after DESCRIPTION: will be used.

"""


def _extract_description(raw_response: str) -> str:
    """Extract the final description after the DESCRIPTION: marker."""
    import re
    match = re.search(r'DESCRIPTION:\s*(.*)', raw_response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: return the whole response if no marker found
    return raw_response.strip()



def _load_modified_captions():
    captions = {}
    for lang_file in CAPTION_BIAS_DIR.glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        captions.update(data)
    return captions


def _process_figure(annotator, prompts, condition, subfolder, fig_key, modified_captions):
    fig_path = FIGURES_DIR / subfolder / fig_key / "original.png"
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / condition / annotator.model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"
    if not fig_path.exists():
        return False, fig_key, f"no image: {fig_path}"
    if not gt_path.exists():
        return False, fig_key, f"no groundtruth: {gt_path}"

    with open(gt_path) as f:
        gt = json.load(f)

    figure_type = gt["figure_type"]

    if subfolder == "multi_language":
        languages = sorted(set(a["annotation_language"] for a in gt["annotations"]))
    else:
        languages = [gt["paper_language"]]

    if condition == "modified_caption":
        caption_data = modified_captions.get(fig_key, {})
        caption = caption_data.get("modified_caption", gt["caption"])
        paper_title = gt.get("paper_title", "")
    elif condition == "image_only":
        caption = ""
        paper_title = ""

    try:
        if len(languages) == 1:
            prompt_text = COT_PREFIX + get_prompt(prompts, languages[0], figure_type)
            raw_response = annotator.annotate_figure(
                prompt=prompt_text, image_path=fig_path,
                caption=caption, paper_title=paper_title,
            )
            result = {
                "figure_key": fig_key, "figure_type": figure_type,
                "condition": condition, "mode": "chain_of_thought",
                "caption_used": caption, "model_name": annotator.model_name,
                "raw_response": raw_response,
                "model_annotation": _extract_description(raw_response),
            }
        else:
            annotations_by_lang = {}
            raw_responses_by_lang = {}
            for lang in languages:
                prompt_text = COT_PREFIX + get_prompt(prompts, lang, figure_type)
                raw_response = annotator.annotate_figure(
                    prompt=prompt_text, image_path=fig_path,
                    caption=caption, paper_title=paper_title,
                )
                raw_responses_by_lang[lang] = raw_response
                annotations_by_lang[lang] = _extract_description(raw_response)
            result = {
                "figure_key": fig_key, "figure_type": figure_type,
                "condition": condition, "mode": "chain_of_thought",
                "caption_used": caption, "model_name": annotator.model_name,
                "raw_responses": raw_responses_by_lang,
                "model_annotations": annotations_by_lang,
            }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {condition}/{subfolder}/{fig_key}")
        return True, fig_key, "done"
    except Exception as e:
        logger.error(f"  FAIL {condition}/{subfolder}/{fig_key}: {e}")
        return False, fig_key, str(e)


def run(model_name="gpt-5.2", condition="modified_caption", workers=4, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        samples = json.load(f)["samples"]

    annotator = get_annotator(model_name)
    prompts = load_prompts()
    modified_captions = _load_modified_captions() if condition == "modified_caption" else {}

    work_items = []
    skipped = 0
    for subfolder, fig_keys in samples.items():
        if subfolder_filter and subfolder != subfolder_filter:
            continue
        for fig_key in fig_keys:
            out_path = OUTPUT_DIR / condition / annotator.model_name / subfolder / f"{fig_key}.json"
            if out_path.exists():
                skipped += 1
            else:
                work_items.append((subfolder, fig_key))

    logger.info(f"CoT Caption bias | model={annotator.model_name} | condition={condition}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to run)")

    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok: success += 1
            else: errors += 1

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_process_figure, annotator, prompts, condition, sub, fk, modified_captions): fk for sub, fk in work_items}
        for f in as_completed(futs):
            try:
                ok, k, s = f.result()
                _on_done(ok, k, s)
            except Exception as e:
                logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                with lock: errors += 1

    logger.info(f"Done. {success}/{len(work_items)+skipped} completed, {errors} errors.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="CoT caption bias descriptions")
    p.add_argument("model", nargs="?", default="gpt-5.2")
    p.add_argument("--condition", required=True, choices=CONDITIONS)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.condition, a.workers, a.subfolder)
