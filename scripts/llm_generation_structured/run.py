"""Runner script for structured LLM figure description generation.

Generates both a paragraph description AND a structured component breakdown.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python3 scripts/llm_generation_structured/run.py
"""

import json
import logging
import sys
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent
GROUNDTRUTH_DIR = ROOT / "Dataset" / "groundtruth"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "generation_structured"

sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation_structured.models import get_annotator
from llm_generation_structured.prompts import load_prompts, get_prompt

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

# Figures to process: first 4 from each folder
SAMPLE_PREFIXES = {
    "bulgarian_only": [f"bulgarian_fig_{i:03d}" for i in range(1, 5)],
    "chinese_only": [f"chinese_fig_{i:03d}" for i in range(1, 5)],
    "english_only": [f"english_fig_{i:03d}" for i in range(1, 5)],
    "german_only": [f"german_fig_{i:03d}" for i in range(1, 5)],
    "multi_language": [f"multi_fig_{i:03d}" for i in range(1, 5)],
}


def run(model_name: str = "gpt-4o-mini"):
    annotator = get_annotator(model_name)
    prompts = load_prompts()
    model_output_dir = OUTPUT_DIR / annotator.model_name

    logger.info(f"Model: {annotator.model_name} (structured output)")
    logger.info(f"Output: {model_output_dir}")
    logger.info(f"Loaded {len(prompts)} prompts")
    print()

    total = 0
    success = 0
    errors = 0

    for subfolder in SUBFOLDERS:
        gt_folder = GROUNDTRUTH_DIR / subfolder
        fig_folder = FIGURES_DIR / subfolder
        out_folder = model_output_dir / subfolder
        out_folder.mkdir(parents=True, exist_ok=True)

        figures_to_process = SAMPLE_PREFIXES[subfolder]

        for fig_key in figures_to_process:
            total += 1
            gt_path = gt_folder / f"{fig_key}.json"
            fig_path = fig_folder / f"{fig_key}.png"
            out_path = out_folder / f"{fig_key}.json"

            if not gt_path.exists():
                logger.warning(f"  SKIP {fig_key} — groundtruth not found")
                continue
            if not fig_path.exists():
                logger.warning(f"  SKIP {fig_key} — figure image not found")
                continue
            if out_path.exists():
                logger.info(f"  SKIP {fig_key} — already generated")
                success += 1
                continue

            # Load groundtruth
            with open(gt_path) as f:
                gt = json.load(f)

            # Determine which languages to generate
            if subfolder == "multi_language":
                languages = sorted(set(
                    a["annotation_language"] for a in gt["annotations"]
                ))
            else:
                languages = [gt["paper_language"]]

            logger.info(f"  [{subfolder}] {fig_key} ({gt['figure_type']}) — languages: {languages}")

            if len(languages) == 1:
                # Single language — generate one structured description
                prompt_text = get_prompt(prompts, languages[0], gt["figure_type"])
                try:
                    structured = annotator.annotate_figure(
                        prompt=prompt_text,
                        image_path=fig_path,
                        caption=gt["caption"],
                        paper_title=gt.get("paper_title", ""),
                    )
                except Exception as e:
                    logger.error(f"  FAIL {fig_key}: {e}")
                    errors += 1
                    continue

                result = {
                    "figure_key": fig_key,
                    "task_id": gt["task_id"],
                    "arxiv_id": gt.get("arxiv_id"),
                    "paper_title": gt.get("paper_title", ""),
                    "paper_language": gt["paper_language"],
                    "figure_type": gt["figure_type"],
                    "caption": gt["caption"],
                    "model_name": annotator.model_name,
                    "model_annotation": structured.get("description", ""),
                    "breakdown": structured.get("breakdown", {}),
                }
                desc_len = len(result["model_annotation"])
                breakdown_keys = len(result["breakdown"])
                success += 1
                logger.info(f"  OK   {fig_key} ({desc_len} chars, {breakdown_keys} breakdown fields)")

            else:
                # Multi-language — generate one structured description per language
                annotations_by_lang = {}
                breakdowns_by_lang = {}
                failed = False
                for lang in languages:
                    prompt_text = get_prompt(prompts, lang, gt["figure_type"])
                    logger.info(f"         generating {lang}...")
                    try:
                        structured = annotator.annotate_figure(
                            prompt=prompt_text,
                            image_path=fig_path,
                            caption=gt["caption"],
                            paper_title=gt.get("paper_title", ""),
                        )
                        annotations_by_lang[lang] = structured.get("description", "")
                        breakdowns_by_lang[lang] = structured.get("breakdown", {})
                        logger.info(f"         {lang}: {len(annotations_by_lang[lang])} chars, {len(breakdowns_by_lang[lang])} breakdown fields")
                    except Exception as e:
                        logger.error(f"  FAIL {fig_key} ({lang}): {e}")
                        failed = True
                        break

                if failed:
                    errors += 1
                    continue

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
                    "breakdowns": breakdowns_by_lang,
                }
                success += 1
                logger.info(f"  OK   {fig_key} ({len(annotations_by_lang)} languages)")

            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

    print()
    logger.info(f"Done. {success}/{total} succeeded, {errors} errors.")


if __name__ == "__main__":
    run()
