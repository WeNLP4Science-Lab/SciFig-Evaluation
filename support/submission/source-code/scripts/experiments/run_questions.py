"""Run capability + hallucination + prompt reverse questions on adversarial figures.

Sends 5 questions per prompt, 2 prompts per figure:
  Prompt 1: 3 capability + 1 inexist + 1 prompt_reverse_true
  Prompt 2: 2 capability + 1 contra + 1 unanswerable + 1 prompt_reverse_false

Usage:
    python3 scripts/experiments/run_questions.py gpt-5.2 --prompt 1 --workers 4
    python3 scripts/experiments/run_questions.py llama4-maverick --prompt 2
    python3 scripts/experiments/run_questions.py --list-models
"""

import argparse
import json
import logging
import sys
import threading
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
SAMPLES_FILE = ROOT / "adversarial_experiments" / "samples.json"
OUTPUT_DIR = ROOT / "output" / "experiments" / "questions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

SUBFOLDER_TO_LANG_KEY = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}


def _load_capability_questions(lang_key):
    """Load capability questions for a language."""
    path = BENCHMARKS_DIR / "capability" / "native" / f"{lang_key}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def _load_hallucination_probes(lang_key):
    """Load hallucination probes for a language."""
    path = BENCHMARKS_DIR / "adversarial" / "hallucination" / "native" / f"{lang_key}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def _load_prompt_reverse(lang_key):
    """Load prompt reverse pairs for a language."""
    path = BENCHMARKS_DIR / "adversarial" / "prompt_reverse" / "native" / f"{lang_key}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def _build_prompt1_questions(fig_key, cap_data, hallu_data, pr_data):
    """Build 5 questions for prompt 1: 3 capability + 1 inexist + 1 reverse_true."""
    items = []

    # 3 capability questions (first 3)
    if fig_key in cap_data:
        for q in cap_data[fig_key].get("questions", [])[:3]:
            items.append({
                "id": q["id"],
                "type": "capability",
                "question": q["question"],
            })

    # 1 hallucination inexist
    if fig_key in hallu_data:
        for p in hallu_data[fig_key].get("probes", []):
            if p["type"] == "inexist":
                items.append({
                    "id": p["id"],
                    "type": "hallucination_inexist",
                    "question": p["question"],
                })
                break

    # 1 prompt reverse true
    if fig_key in pr_data:
        pair = pr_data[fig_key].get("pair", {})
        items.append({
            "id": pair.get("id", "") + "_true",
            "type": "prompt_reverse_true",
            "question": pair.get("true_statement", ""),
        })

    return items


def _build_prompt2_questions(fig_key, cap_data, hallu_data, pr_data):
    """Build 5 questions for prompt 2: 2 capability + 1 contra + 1 unanswerable + 1 reverse_false."""
    items = []

    # 2 capability questions (last 2)
    if fig_key in cap_data:
        for q in cap_data[fig_key].get("questions", [])[3:5]:
            items.append({
                "id": q["id"],
                "type": "capability",
                "question": q["question"],
            })

    # 1 hallucination contra
    if fig_key in hallu_data:
        for p in hallu_data[fig_key].get("probes", []):
            if p["type"] == "contra":
                items.append({
                    "id": p["id"],
                    "type": "hallucination_contra",
                    "question": p["question"],
                })
                break

    # 1 hallucination unanswerable
    if fig_key in hallu_data:
        for p in hallu_data[fig_key].get("probes", []):
            if p["type"] == "unanswerable":
                items.append({
                    "id": p["id"],
                    "type": "hallucination_unanswerable",
                    "question": p["question"],
                })
                break

    # 1 prompt reverse false
    if fig_key in pr_data:
        pair = pr_data[fig_key].get("pair", {})
        items.append({
            "id": pair.get("id", "") + "_false",
            "type": "prompt_reverse_false",
            "question": pair.get("false_statement", ""),
        })

    return items


def _format_questions_prompt(questions):
    """Format questions into a single prompt string."""
    lines = ["Please answer each of the following questions about the figure. IMPORTANT: Number your answers exactly as 1. 2. 3. 4. 5. with each answer on a new line. Keep each answer concise (1-3 sentences).\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q['question']}")
    return "\n".join(lines)


def _parse_answers(raw_response, questions):
    """Parse numbered answers from the response.

    Handles various formats:
    - "1. answer" / "2. answer" (standard)
    - "**1. question text**" / "1. **question**" (Gemini bold)
    - "## 1. question" / "## 问题1：question" (LLaMA-Scout headers)
    - "3.\tanswer" (Phi with tabs)
    - "1) answer" / "1: answer"
    """
    import re

    n = len(questions)

    sections = {}
    current_num = None
    current_lines = []

    for line in raw_response.strip().split("\n"):
        stripped = line.strip()
        # Strip leading markdown: ##, **, *, etc.
        stripped_clean = re.sub(r'^#{1,3}\s*', '', stripped)
        stripped_clean = re.sub(r'^\*{1,2}\s*', '', stripped_clean)

        # Try standard pattern: "1. " or "1) " or "1: " or "1.\t"
        m = re.match(r'^(\d+)\s*[.):\t]', stripped_clean)

        # Also try localized patterns: "问题1：" "Въпрос 1:" "Frage 1:"
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
                # Remove everything up to and including the number prefix
                rest = re.sub(r'^[#*\s]*(?:问题|Въпрос|Frage|Question)?\s*\d+\s*[.)：:\t\s]+', '', stripped, flags=re.IGNORECASE).strip()
                current_lines = [rest] if rest else []
                continue

        if current_num is not None:
            current_lines.append(stripped)

    # Save last section
    if current_num is not None:
        sections[current_num] = "\n".join(current_lines).strip()

    # Map back to question items
    result = []
    for i, q in enumerate(questions):
        answer = sections.get(i + 1, "")
        # If answer starts with the question text (bold), strip it
        # Gemini often repeats: "**question text here?**\n* actual answer"
        if answer.startswith("**"):
            # Find end of bold question
            bold_end = answer.find("**", 2)
            if bold_end > 0:
                after_bold = answer[bold_end + 2:].strip()
                # Remove leading bullet/dash
                after_bold = re.sub(r'^[*\-–]\s*', '', after_bold).strip()
                if after_bold:
                    answer = after_bold

        result.append({
            **q,
            "model_answer": answer,
        })
    return result


def _process_figure(annotator, prompt_id, questions, subfolder, fig_key):
    """Process a single figure with the given questions."""
    fig_path = FIGURES_DIR / subfolder / fig_key / "original.png"
    out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"

    if not fig_path.exists():
        return False, fig_key, f"no image: {fig_path}"

    # Check if this prompt already ran
    existing = None
    if out_path.exists():
        with open(out_path) as f:
            existing = json.load(f)
        for resp in existing.get("responses", []):
            if resp.get("prompt_id") == prompt_id:
                return True, fig_key, "skip"

    if not questions:
        return True, fig_key, "skip_no_questions"

    prompt_text = _format_questions_prompt(questions)

    try:
        raw_response = annotator.annotate_figure(
            prompt=prompt_text,
            image_path=fig_path,
            caption="",
            paper_title="",
        )

        parsed_items = _parse_answers(raw_response, questions)

        response_entry = {
            "prompt_id": prompt_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "raw_response": raw_response,
            "items": parsed_items,
        }

        if existing:
            existing["responses"].append(response_entry)
            result = existing
        else:
            result = {
                "figure_key": fig_key,
                "subfolder": subfolder,
                "model_name": annotator.model_name,
                "responses": [response_entry],
            }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  OK   {subfolder}/{fig_key} [{prompt_id}] ({len(parsed_items)} answers)")
        return True, fig_key, "done"

    except Exception as e:
        logger.error(f"  FAIL {subfolder}/{fig_key} [{prompt_id}]: {e}")
        return False, fig_key, str(e)


def run(model_name, prompt_num, workers=4, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        samples = json.load(f)["samples"]

    annotator = get_annotator(model_name)
    prompt_id = f"prompt{prompt_num}"

    # Load all question data
    all_cap = {}
    all_hallu = {}
    all_pr = {}
    for subfolder in samples:
        lang_key = SUBFOLDER_TO_LANG_KEY[subfolder]
        all_cap.update(_load_capability_questions(lang_key))
        all_hallu.update(_load_hallucination_probes(lang_key))
        all_pr.update(_load_prompt_reverse(lang_key))

    # Build work items
    work_items = []
    skipped = 0
    for subfolder, fig_keys in samples.items():
        for fig_key in fig_keys:
            # Check skip
            out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"
            if out_path.exists():
                with open(out_path) as f:
                    existing = json.load(f)
                if any(r.get("prompt_id") == prompt_id for r in existing.get("responses", [])):
                    skipped += 1
                    continue

            if subfolder_filter and subfolder != subfolder_filter:
                continue

            if prompt_num == 1:
                questions = _build_prompt1_questions(fig_key, all_cap, all_hallu, all_pr)
            else:
                questions = _build_prompt2_questions(fig_key, all_cap, all_hallu, all_pr)

            if questions:
                work_items.append((subfolder, fig_key, questions))

    logger.info(f"Questions runner | model={annotator.model_name} | {prompt_id}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to run)")

    if not work_items:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok:
                success += 1
            else:
                errors += 1
            d = success + errors - skipped
            if d % 10 == 0 or not ok:
                logger.info(f"  Progress: {d}/{len(work_items)} (errors={errors})")

    if workers == 1:
        for sub, fk, qs in work_items:
            ok, k, s = _process_figure(annotator, prompt_id, qs, sub, fk)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, annotator, prompt_id, qs, sub, fk): fk
                for sub, fk, qs in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock:
                        errors += 1

    logger.info(f"Done. {success}/{len(work_items) + skipped} completed, {errors} errors.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Run questions on adversarial figures")
    p.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
    p.add_argument("--prompt", type=int, required=True, choices=[1, 2], help="Prompt number (1 or 2)")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    p.add_argument("--list-models", action="store_true")
    a = p.parse_args()

    if a.list_models:
        models = sorted(_get_all_models().keys())
        print(f"Available models ({len(models)}):")
        for m in models:
            print(f"  {m}")
        sys.exit(0)

    run(a.model, a.prompt, a.workers, a.subfolder)
