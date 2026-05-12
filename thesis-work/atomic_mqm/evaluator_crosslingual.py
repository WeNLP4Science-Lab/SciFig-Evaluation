"""Cross-lingual atomic MQM evaluator.

Evaluates model descriptions against language-specific atom checklists
for the 13 parallel multi-language figures (same figure, 4 languages).

Output: output/evaluation/crosslingual/{judge}/{model}/{language}/{fig_key}.json

Usage:
    python3 atomic_mqm/evaluator_crosslingual.py --model gemini-3.1-pro --language Bulgarian --judge azure/mistral-large-3
    python3 atomic_mqm/evaluator_crosslingual.py --model gemini-3.1-pro --language all --judge azure/mistral-large-3
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

# Reuse the v2 evaluator internals
from atomic_mqm.evaluator_v2 import (
    _get_judge_prompt, _run_judge, _build_user_text,
    validate_errors, compute_mqm_score, compute_atom_coverage,
)

ATOMS_DIR = ROOT / "atomic_mqm" / "atoms_crosslingual"
TRANSFORMS_DIR = ROOT / "output" / "experiments" / "transforms"
GENERATION_DIR = ROOT / "output" / "generation"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "evaluation" / "crosslingual"

LANG_SHORT = {"Bulgarian": "bg", "Chinese": "cn", "German": "de", "English": "en"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_model_description(fig_key, model_name, language):
    """Get model description for a specific language."""
    # Try transforms first
    gen_path = TRANSFORMS_DIR / model_name / "original" / "multi_language" / f"{fig_key}.json"
    if not gen_path.exists():
        gen_path = GENERATION_DIR / model_name / "multi_language" / f"{fig_key}.json"
    if not gen_path.exists():
        return None

    data = json.load(open(gen_path))
    if "model_annotations" in data:
        return data["model_annotations"].get(language, "")
    return data.get("model_annotation", "")


def run(model_name, language, judge_model, workers=4):
    lang_short = LANG_SHORT.get(language)
    if not lang_short:
        logger.error(f"Unknown language: {language}")
        return

    # Load atom files for this language
    atom_files = sorted(ATOMS_DIR.glob(f"*_{lang_short}.json"))
    if not atom_files:
        logger.error(f"No atom files for {language}")
        return

    # Build work items
    work_items = []
    skipped = 0
    for atom_file in atom_files:
        atom_data = json.load(open(atom_file))
        fig_key = atom_data["figure_key"]
        out_path = OUTPUT_DIR / judge_model.replace("/", "/") / model_name / language / f"{fig_key}.json"
        if out_path.exists():
            skipped += 1
            continue
        fig_path = FIGURES_DIR / "multi_language" / f"{fig_key}.png"
        if not fig_path.exists():
            continue
        model_desc = _get_model_description(fig_key, model_name, language)
        if not model_desc:
            continue
        work_items.append((atom_data, fig_path, model_desc))

    logger.info(f"Cross-lingual eval | model={model_name} | lang={language} | judge={judge_model} | {len(work_items)} to eval, {skipped} done")

    if not work_items:
        logger.info("Nothing to do.")
        _print_summary(judge_model, model_name, language)
        return

    success = skipped
    errors = 0
    lock = threading.Lock()

    def _process(atom_data, fig_path, model_desc):
        nonlocal success, errors
        fig_key = atom_data["figure_key"]
        atoms = atom_data["atoms"]
        reference = atom_data.get("reference_description", "")
        out_path = OUTPUT_DIR / judge_model.replace("/", "/") / model_name / language / f"{fig_key}.json"

        user_text = _build_user_text(atoms, model_desc, reference)
        try:
            result = _run_judge(judge_model, fig_path, user_text)
        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")
            with lock:
                errors += 1
            return

        errs = validate_errors(result.get("errors", []))
        mqm_score, total_penalty = compute_mqm_score(errs, len(atoms))
        atom_coverage = compute_atom_coverage(errs, atoms)

        eval_result = {
            "figure_key": fig_key,
            "subfolder": "multi_language",
            "model_name": model_name,
            "judge_model": judge_model,
            "judge_type": "crosslingual_atomic_mqm",
            "language": language,
            "num_atoms": len(atoms),
            "errors": errs,
            "error_count": len(errs),
            "mqm_score": round(mqm_score, 2),
            "total_penalty": round(total_penalty, 2),
            "atom_coverage": atom_coverage,
        }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(eval_result, f, indent=2, ensure_ascii=False)

        ac = atom_coverage
        logger.info(
            f"  OK   {fig_key} [{language}]: MQM={mqm_score:.1f} "
            f"({len(errs)} errors) acc={ac['accuracy']:.2f} comp={ac['completeness']:.2f}"
        )
        with lock:
            success += 1

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_process, ad, fp, md): ad["figure_key"] for ad, fp, md in work_items}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                with lock:
                    errors += 1

    _print_summary(judge_model, model_name, language)
    logger.info(f"Done. {success}/{len(work_items)+skipped} evaluated, {errors} failures.")


def _print_summary(judge_model, model_name, language):
    eval_dir = OUTPUT_DIR / judge_model.replace("/", "/") / model_name / language
    if eval_dir.exists():
        scores = []
        for f in eval_dir.glob("*.json"):
            scores.append(json.load(open(f))["mqm_score"])
        if scores:
            print(f"\n  {language}: MQM={sum(scores)/len(scores):.2f} ({len(scores)} figures)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cross-lingual atomic MQM evaluation")
    p.add_argument("--model", required=True)
    p.add_argument("--language", required=True, help="Bulgarian, Chinese, German, English, or 'all'")
    p.add_argument("--judge", default="azure/mistral-large-3")
    p.add_argument("--workers", type=int, default=4)
    a = p.parse_args()

    if a.language == "all":
        for lang in ["Bulgarian", "Chinese", "German", "English"]:
            run(a.model, lang, a.judge, a.workers)
    else:
        run(a.model, a.language, a.judge, a.workers)
