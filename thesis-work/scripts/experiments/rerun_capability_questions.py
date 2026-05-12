"""Rerun specific capability questions that changed after experiments.

Reads post_experiment_changes.json, filters by subfolder(s), sends only the
changed questions per figure to each model, and patches answers back into
existing response files.

Usage:
    # Rerun english_only for all models:
    python3 scripts/experiments/rerun_capability_questions.py --subfolder english_only

    # Rerun multiple subfolders:
    python3 scripts/experiments/rerun_capability_questions.py --subfolder english_only multi_language

    # Single model:
    python3 scripts/experiments/rerun_capability_questions.py --subfolder english_only --model gpt-5.2

    # Dry run (show what would be rerun without calling APIs):
    python3 scripts/experiments/rerun_capability_questions.py --subfolder english_only --dry-run
"""

import argparse
import json
import logging
import re
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from llm_generation.models import get_annotator, _get_all_models

BENCHMARKS_DIR = ROOT / "adversarial_experiments" / "benchmarks"
FIGURES_DIR = ROOT / "adversarial_experiments" / "figures"
OUTPUT_DIR = ROOT / "output" / "experiments" / "questions"
CHANGES_FILE = BENCHMARKS_DIR / "capability" / "post_experiment_changes.json"

SUBFOLDER_TO_LANG_KEY = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}

LANG_KEY_TO_SUBFOLDER = {v: k for k, v in SUBFOLDER_TO_LANG_KEY.items()}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _load_changes(subfolders):
    """Load question_text_changes filtered by subfolder(s).

    Returns: {fig_key: [question_id, ...]}
    """
    with open(CHANGES_FILE) as f:
        data = json.load(f)

    # Determine which figure prefixes map to which subfolders
    prefix_to_subfolder = {
        "english_fig_": "english_only",
        "german_fig_": "german_only",
        "bulgarian_fig_": "bulgarian_only",
        "chinese_fig_": "chinese_only",
        "multi_fig_": "multi_language",
    }

    by_fig = defaultdict(list)
    for change in data.get("question_text_changes", []):
        if not change.get("needs_rerun"):
            continue
        fig_key = change["figure_key"]
        # Determine subfolder from figure key prefix
        fig_subfolder = None
        for prefix, sub in prefix_to_subfolder.items():
            if fig_key.startswith(prefix):
                fig_subfolder = sub
                break
        if fig_subfolder and fig_subfolder in subfolders:
            by_fig[fig_key].append(change["question_id"])

    return by_fig


def _load_capability_questions(lang_key):
    """Load current capability questions for a language."""
    path = BENCHMARKS_DIR / "capability" / "native" / f"{lang_key}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def _get_subfolder_for_fig(fig_key):
    """Derive subfolder from figure key prefix."""
    for prefix, sub in {
        "english_fig_": "english_only",
        "german_fig_": "german_only",
        "bulgarian_fig_": "bulgarian_only",
        "chinese_fig_": "chinese_only",
        "multi_fig_": "multi_language",
    }.items():
        if fig_key.startswith(prefix):
            return sub
    return None


def _format_questions_prompt(questions):
    """Format questions into a prompt. Handles 1-N questions."""
    n = len(questions)
    if n == 1:
        return f"Please answer the following question about the figure. Keep your answer concise (1-3 sentences).\n\n1. {questions[0]['question']}"
    lines = [f"Please answer each of the following questions about the figure. IMPORTANT: Number your answers exactly as {' '.join(f'{i}.' for i in range(1, n+1))} with each answer on a new line. Keep each answer concise (1-3 sentences).\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q['question']}")
    return "\n".join(lines)


def _parse_answers(raw_response, questions):
    """Parse numbered answers from response."""
    n = len(questions)

    if n == 1:
        # Single question — entire response is the answer
        answer = raw_response.strip()
        # Strip leading "1. " if present
        answer = re.sub(r'^\*{0,2}\s*1\s*[.):\t]\s*', '', answer).strip()
        return [{"model_answer": answer}]

    sections = {}
    current_num = None
    current_lines = []

    for line in raw_response.strip().split("\n"):
        stripped = line.strip()
        stripped_clean = re.sub(r'^#{1,3}\s*', '', stripped)
        stripped_clean = re.sub(r'^\*{1,2}\s*', '', stripped_clean)

        m = re.match(r'^(\d+)\s*[.):\t]', stripped_clean)
        if not m:
            m2 = re.match(r'^(?:问题|Въпрос|Frage|Question)\s*(\d+)\s*[：:.)]', stripped_clean, re.IGNORECASE)
            if m2:
                m = m2

        if m:
            num = int(m.group(1))
            if 1 <= num <= n:
                if current_num is not None:
                    sections[current_num] = "\n".join(current_lines).strip()
                current_num = num
                rest = re.sub(r'^[#*\s]*(?:问题|Въпрос|Frage|Question)?\s*\d+\s*[.)：:\t\s]+', '', stripped, flags=re.IGNORECASE).strip()
                current_lines = [rest] if rest else []
                continue

        if current_num is not None:
            current_lines.append(stripped)

    if current_num is not None:
        sections[current_num] = "\n".join(current_lines).strip()

    result = []
    for i in range(n):
        answer = sections.get(i + 1, "")
        if answer.startswith("**"):
            bold_end = answer.find("**", 2)
            if bold_end > 0:
                after_bold = answer[bold_end + 2:].strip()
                after_bold = re.sub(r'^[*\-–]\s*', '', after_bold).strip()
                if after_bold:
                    answer = after_bold
        result.append({"model_answer": answer})

    return result


def _rerun_figure(annotator, fig_key, question_ids, all_cap):
    """Rerun specific capability questions for one figure across one model."""
    subfolder = _get_subfolder_for_fig(fig_key)
    fig_path = FIGURES_DIR / subfolder / fig_key / "original.png"
    out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"

    if not fig_path.exists():
        return False, fig_key, f"no image: {fig_path}"

    if not out_path.exists():
        return False, fig_key, f"no existing response file"

    # Get current question texts from benchmark
    fig_questions = all_cap.get(fig_key, {}).get("questions", [])
    questions_to_run = [q for q in fig_questions if q["id"] in question_ids]

    if not questions_to_run:
        return False, fig_key, f"questions {question_ids} not found in benchmark"

    prompt_text = _format_questions_prompt(questions_to_run)

    try:
        raw_response = annotator.annotate_figure(
            prompt=prompt_text,
            image_path=fig_path,
            caption="",
            paper_title="",
        )

        parsed = _parse_answers(raw_response, questions_to_run)

        # Load existing response file and patch answers
        with open(out_path) as f:
            existing = json.load(f)

        # Build id->answer map from parsed results
        rerun_answers = {}
        for q, p in zip(questions_to_run, parsed):
            rerun_answers[q["id"]] = p["model_answer"]

        # Patch into existing responses
        patched_count = 0
        for resp in existing.get("responses", []):
            for item in resp.get("items", []):
                if item["id"] in rerun_answers:
                    item["model_answer"] = rerun_answers[item["id"]]
                    item["question"] = next(q["question"] for q in questions_to_run if q["id"] == item["id"])
                    item["rerun_timestamp"] = datetime.now(timezone.utc).isoformat()
                    patched_count += 1

        # Also add a rerun log entry
        if "reruns" not in existing:
            existing["reruns"] = []
        existing["reruns"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question_ids": question_ids,
            "raw_response": raw_response,
            "parsed": [{
                "id": q["id"],
                "question": q["question"],
                "model_answer": rerun_answers[q["id"]],
            } for q in questions_to_run],
        })

        with open(out_path, "w") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        answers_preview = " | ".join(f"{qid}: {rerun_answers[qid][:40]}" for qid in question_ids)
        logger.info(f"  OK   {annotator.model_name}/{subfolder}/{fig_key} — patched {patched_count} answers")
        logger.info(f"       {answers_preview}")
        return True, fig_key, "done"

    except Exception as e:
        logger.error(f"  FAIL {annotator.model_name}/{subfolder}/{fig_key}: {e}")
        return False, fig_key, str(e)


def run(subfolders, model_filter=None, workers=4, dry_run=False):
    changes = _load_changes(subfolders)
    if not changes:
        logger.info("No questions to rerun for the specified subfolder(s).")
        return

    # Load capability questions for relevant languages
    all_cap = {}
    for subfolder in subfolders:
        lang_key = SUBFOLDER_TO_LANG_KEY[subfolder]
        all_cap.update(_load_capability_questions(lang_key))

    # Determine models
    if model_filter:
        model_names = model_filter
    else:
        # All models that have response files
        model_names = sorted(d.name for d in OUTPUT_DIR.iterdir() if d.is_dir())

    logger.info(f"=== Capability Question Rerun ===")
    logger.info(f"Subfolders: {', '.join(subfolders)}")
    logger.info(f"Figures: {len(changes)}")
    for fig_key, qids in sorted(changes.items()):
        logger.info(f"  {fig_key}: {qids}")
    logger.info(f"Models: {', '.join(model_names)}")
    logger.info(f"Total API calls: {len(changes) * len(model_names)}")

    if dry_run:
        logger.info("DRY RUN — no API calls made.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    work_items = []
    for model_name in model_names:
        for fig_key, qids in changes.items():
            subfolder = _get_subfolder_for_fig(fig_key)
            resp_path = OUTPUT_DIR / model_name / subfolder / f"{fig_key}.json"
            if not resp_path.exists():
                logger.warning(f"  SKIP {model_name}/{fig_key} — no response file")
                continue
            work_items.append((model_name, fig_key, qids))

    def _do_work(model_name, fig_key, qids):
        annotator = get_annotator(model_name)
        return _rerun_figure(annotator, fig_key, qids, all_cap)

    if workers == 1:
        for model_name, fig_key, qids in work_items:
            ok, k, s = _do_work(model_name, fig_key, qids)
            with lock:
                if ok:
                    success += 1
                else:
                    errors += 1
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_do_work, mn, fk, qi): (mn, fk)
                for mn, fk, qi in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    with lock:
                        if ok:
                            success += 1
                        else:
                            errors += 1
                except Exception as e:
                    mn, fk = futs[f]
                    logger.error(f"  UNEXPECTED {mn}/{fk}: {e}")
                    with lock:
                        errors += 1

    logger.info(f"\n=== DONE === {success} succeeded, {errors} failed out of {len(work_items)} total")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Rerun changed capability questions")
    p.add_argument("--subfolder", nargs="+", required=True,
                   choices=list(SUBFOLDER_TO_LANG_KEY.keys()),
                   help="Subfolder(s) to rerun")
    p.add_argument("--model", nargs="+", default=None, help="Specific model(s). Default: all.")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--dry-run", action="store_true", help="Show what would be rerun without calling APIs")
    a = p.parse_args()
    run(a.subfolder, a.model, a.workers, a.dry_run)
