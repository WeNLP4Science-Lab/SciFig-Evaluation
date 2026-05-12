"""Generate figure descriptions for the 120-sample evaluation set.

Only generates for figures that have atom checklists (atomic_mqm/atoms/).
Skips figures that already have descriptions in transforms/ or generation/.

Usage:
    python3 scripts/llm_generation/run_120_sample.py claude-opus-4.6 --workers 4
    python3 scripts/llm_generation/run_120_sample.py claude-opus-4.6 --workers 4 --limit 55
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator
from llm_generation.prompts import load_prompts, get_prompt

ATOMS_DIR = ROOT / "atomic_mqm" / "atoms"
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
TRANSFORMS_DIR = ROOT / "output" / "experiments" / "transforms"
OUTPUT_DIR = ROOT / "output" / "generation"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_120_sample():
    """Get the 120 figures from atom checklists."""
    figs = []
    for f in sorted(ATOMS_DIR.glob("*.json")):
        ad = json.load(open(f))
        figs.append((ad["figure_key"], ad.get("subfolder", "")))
    return figs


def _has_description(fig_key, subfolder, model_name):
    """Check if description already exists in transforms or generation."""
    t = TRANSFORMS_DIR / model_name / "original" / subfolder / f"{fig_key}.json"
    g = OUTPUT_DIR / model_name / subfolder / f"{fig_key}.json"
    return t.exists() or g.exists()


def _process_figure(annotator, prompts, subfolder, fig_key):
    """Generate description for one figure."""
    gt_path = GROUNDTRUTH_DIR / subfolder / f"{fig_key}.json"
    fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
    out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    with open(gt_path) as f:
        gt = json.load(f)

    if subfolder == "multi_language":
        languages = sorted(set(a["annotation_language"] for a in gt["annotations"]))
    else:
        languages = [gt["paper_language"]]

    if len(languages) == 1:
        prompt_text = get_prompt(prompts, languages[0], gt["figure_type"])
        description = annotator.annotate_figure(
            prompt=prompt_text,
            image_path=fig_path,
            caption=gt["caption"],
            paper_title=gt.get("paper_title", ""),
        )
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
    else:
        annotations_by_lang = {}
        for lang in languages:
            prompt_text = get_prompt(prompts, lang, gt["figure_type"])
            desc = annotator.annotate_figure(
                prompt=prompt_text,
                image_path=fig_path,
                caption=gt["caption"],
                paper_title=gt.get("paper_title", ""),
            )
            annotations_by_lang[lang] = desc
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

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK   {subfolder}/{fig_key}")
    return True, fig_key, "done"


def run(model_name, workers=4, limit=None):
    annotator = get_annotator(model_name)
    prompts = load_prompts()

    all_figs = _get_120_sample()
    existing = 0
    work = []
    for fig_key, subfolder in all_figs:
        if _has_description(fig_key, subfolder, model_name):
            existing += 1
        else:
            work.append((fig_key, subfolder))

    if limit and len(work) > limit:
        work = work[:limit]

    logger.info(f"120-sample generation | model={model_name} | {existing} exist, {len(work)} to generate")

    if not work:
        logger.info("Nothing to do.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    def _do(fig_key, subfolder):
        nonlocal success, errors
        try:
            ok, key, status = _process_figure(annotator, prompts, subfolder, fig_key)
            with lock:
                if ok:
                    success += 1
                else:
                    errors += 1
        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")
            with lock:
                errors += 1

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_do, fk, sub): fk for fk, sub in work}
        for f in as_completed(futs):
            f.result()

    logger.info(f"Done. {success}/{len(work)} generated, {errors} failures. Total: {existing + success}/120")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate descriptions for 120-sample evaluation set")
    p.add_argument("model", help="Model name (e.g. claude-opus-4.6)")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--limit", type=int, default=None, help="Max figures to generate (e.g. 55)")
    a = p.parse_args()
    run(a.model, a.workers, a.limit)
