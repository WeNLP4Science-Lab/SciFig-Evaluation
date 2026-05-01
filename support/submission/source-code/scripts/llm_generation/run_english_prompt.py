"""Runner script for cross-language figure description generation.

Uses English prompts with a strict language enforcement instruction,
telling the model to respond in the target language (determined by subfolder).

Skips english_only subfolder (already covered by run.py).
For multi_language, skips English annotations (already covered).

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/llm_generation/run_english_prompt.py <model_name> [--workers N]
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
OUTPUT_DIR = ROOT / "output" / "generation_english_prompt"
CROSS_LANG_PROMPTS_DIR = ROOT / "scripts" / "llm_generation" / "prompts" / "cross_language"

sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Skip english_only — already covered by native-prompt runs
SUBFOLDERS = [
    "bulgarian_only",
    "chinese_only",
    "german_only",
    "multi_language",
]

# Map subfolder to target language
SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "german_only": "German",
}

# Map figure_type to prompt file
FIGURE_TYPE_TO_FILE = {
    "Line Plot": "line_plot.txt",
    "Bar Chart": "bar_chart.txt",
    "Pie Chart": "pie_chart.txt",
}
DEFAULT_PROMPT_FILE = "default.txt"


def _load_cross_language_prompts() -> dict[str, str]:
    """Load cross-language prompt templates (with {language} placeholder)."""
    templates = {}
    for figure_type, filename in FIGURE_TYPE_TO_FILE.items():
        path = CROSS_LANG_PROMPTS_DIR / filename
        if path.exists():
            templates[figure_type] = path.read_text(encoding="utf-8")
    default_path = CROSS_LANG_PROMPTS_DIR / DEFAULT_PROMPT_FILE
    if default_path.exists():
        templates["Default"] = default_path.read_text(encoding="utf-8")
    return templates


def _get_cross_language_prompt(templates: dict[str, str], language: str, figure_type: str) -> str:
    """Get a cross-language prompt with {language} replaced."""
    template = templates.get(figure_type, templates.get("Default"))
    if not template:
        raise ValueError(f"No cross-language prompt for figure_type={figure_type!r}")
    return template.replace("{language}", language)


def _discover_figures(subfolder: str) -> list[str]:
    """Discover all figure keys in a groundtruth subfolder."""
    gt_folder = GROUNDTRUTH_DIR / subfolder
    keys = sorted(p.stem for p in gt_folder.glob("*.json"))
    return keys


def _process_figure(annotator, templates, subfolder, fig_key, model_output_dir):
    """Process a single figure using cross-language English prompts."""
    gt_folder = GROUNDTRUTH_DIR / subfolder
    fig_folder = FIGURES_DIR / subfolder
    out_folder = model_output_dir / subfolder

    gt_path = gt_folder / f"{fig_key}.json"
    fig_path = fig_folder / f"{fig_key}.png"
    out_path = out_folder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    with open(gt_path) as f:
        gt = json.load(f)

    if subfolder == "multi_language":
        languages = sorted(set(
            a["annotation_language"] for a in gt["annotations"]
            if a["annotation_language"] != "English"
        ))
        if not languages:
            return True, fig_key, "skip"
    else:
        # Target language from subfolder, not paper_language
        target_lang = SUBFOLDER_TO_LANGUAGE[subfolder]
        languages = [target_lang]

    logger.info(f"  [{subfolder}] {fig_key} ({gt['figure_type']}) — target: {languages}")

    if len(languages) == 1:
        prompt_text = _get_cross_language_prompt(templates, languages[0], gt["figure_type"])
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
            "prompt_language": "English",
            "target_language": languages[0],
            "model_annotation": description,
        }
        logger.info(f"  OK   {fig_key} ({len(description)} chars)")

    else:
        annotations_by_lang = {}
        for lang in languages:
            prompt_text = _get_cross_language_prompt(templates, lang, gt["figure_type"])
            logger.info(f"         generating {lang} (English prompt → {lang})...")
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
            "prompt_language": "English",
            "target_languages": languages,
            "model_annotations": annotations_by_lang,
        }
        logger.info(f"  OK   {fig_key} ({len(annotations_by_lang)} languages)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return True, fig_key, "done"


def run(model_name: str = "gpt-5.2", workers: int = 1, subfolder_filter: str | None = None):
    annotator = get_annotator(model_name)
    templates = _load_cross_language_prompts()
    model_output_dir = OUTPUT_DIR / annotator.model_name

    subfolders = [subfolder_filter] if subfolder_filter else SUBFOLDERS

    logger.info(f"Model: {annotator.model_name}")
    logger.info(f"Output: {model_output_dir}")
    logger.info(f"Subfolders: {subfolders}")
    logger.info(f"Workers: {workers}")
    logger.info(f"Mode: Cross-language (English prompt → target language)")
    logger.info(f"Loaded {len(templates)} prompt templates")
    print()

    work_items = []
    skipped = 0
    for subfolder in subfolders:
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
                annotator, templates, subfolder, fig_key, model_output_dir
            )
            _on_complete(ok, key, status)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _process_figure, annotator, templates, subfolder, fig_key, model_output_dir
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
    parser = argparse.ArgumentParser(
        description="Cross-language generation: English prompts with target language enforcement"
    )
    parser.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--subfolder", type=str, default=None, help="Process only this subfolder")
    args = parser.parse_args()
    run(args.model, args.workers, args.subfolder)
