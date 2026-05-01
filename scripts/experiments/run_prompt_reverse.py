"""Run prompt reverse experiment with forced A/B JSON responses.

For each figure, sends two separate prompts (true statement and false statement)
with the image. Model must respond in JSON with answer A (True) or B (False).

Output: output/experiments/prompt_reverse/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/run_prompt_reverse.py gpt-5.2 --workers 4
    python3 scripts/experiments/run_prompt_reverse.py --list-models
"""

import argparse
import json
import logging
import sys
import threading
import time
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
OUTPUT_DIR = ROOT / "output" / "experiments" / "prompt_reverse"

SUBFOLDER_TO_LANG_KEY = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}

PROMPT_TEMPLATE = """Statement: {statement}

Is this statement true or false based on the figure?

Respond ONLY in JSON: {{"answer": "A", "explanation": "max 10 words"}}
A = True, B = False"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _load_prompt_reverse_probes():
    """Load all prompt reverse pairs."""
    probes = {}
    pr_dir = BENCHMARKS_DIR / "adversarial" / "prompt_reverse" / "native"
    for lang_file in pr_dir.glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        for fig_key, fig_data in data.items():
            probes[fig_key] = fig_data.get("pair", {})
    return probes


def _parse_ab_response(raw_response):
    """Parse A or B from JSON response."""
    text = raw_response.strip()
    # Try JSON parse
    try:
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)
        return data.get("answer", "").strip().upper()[:1], data.get("explanation", "")
    except (json.JSONDecodeError, AttributeError):
        pass
    # Fallback: look for A or B in first few chars
    first = text[:10].strip().upper()
    if first.startswith("A"):
        return "A", text
    if first.startswith("B"):
        return "B", text
    return "", text


def _process_figure(annotator, subfolder, fig_key, pair):
    """Run both true and false prompts for one figure."""
    fig_path = FIGURES_DIR / subfolder / fig_key / "original.png"
    out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not fig_path.exists():
        return False, fig_key, f"no image: {fig_path}"

    true_stmt = pair.get("true_statement", "")
    false_stmt = pair.get("false_statement", "")

    if not true_stmt or not false_stmt:
        return True, fig_key, "skip_no_pair"

    results = {}
    for label, statement, expected in [("true", true_stmt, "A"), ("false", false_stmt, "B")]:
        prompt = PROMPT_TEMPLATE.format(statement=statement)
        try:
            raw = annotator.annotate_figure(
                prompt=prompt,
                image_path=fig_path,
                caption="",
                paper_title="",
            )
            answer, explanation = _parse_ab_response(raw)
            results[label] = {
                "statement": statement,
                "expected": expected,
                "raw_response": raw,
                "answer": answer,
                "explanation": explanation,
                "correct": answer == expected,
            }
        except Exception as e:
            logger.error(f"  FAIL {fig_key} [{label}]: {e}")
            results[label] = {
                "statement": statement,
                "expected": expected,
                "raw_response": "",
                "answer": "",
                "explanation": str(e),
                "correct": False,
            }

    # Compute consistency score
    true_correct = results.get("true", {}).get("correct", False)
    false_correct = results.get("false", {}).get("correct", False)
    true_answer = results.get("true", {}).get("answer", "")
    false_answer = results.get("false", {}).get("answer", "")

    if true_correct and false_correct:
        score = 1.0
        pattern = "correct"
    elif true_answer == false_answer:
        score = 0.0
        pattern = "agrees_both" if true_answer == "A" else "disagrees_both"
    elif not true_correct and not false_correct:
        score = 0.5
        pattern = "reversed"
    else:
        score = 0.0
        pattern = "mixed"

    output = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": annotator.model_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact_description": pair.get("fact_description", ""),
        "true_probe": results.get("true", {}),
        "false_probe": results.get("false", {}),
        "score": score,
        "pattern": pattern,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK   {subfolder}/{fig_key} — T={true_answer} F={false_answer} score={score} ({pattern})")
    return True, fig_key, "done"


def run(model_name="gpt-5.2", workers=4, subfolder_filter=None):
    with open(SAMPLES_FILE) as f:
        samples = json.load(f)["samples"]

    annotator = get_annotator(model_name)
    probes = _load_prompt_reverse_probes()

    work_items = []
    skipped = 0
    for subfolder, fig_keys in samples.items():
        if subfolder_filter and subfolder != subfolder_filter:
            continue
        for fig_key in fig_keys:
            out_path = OUTPUT_DIR / annotator.model_name / subfolder / f"{fig_key}.json"
            if out_path.exists():
                skipped += 1
            elif fig_key in probes:
                work_items.append((subfolder, fig_key, probes[fig_key]))

    logger.info(f"Prompt reverse | model={annotator.model_name}")
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

    if workers == 1:
        for sub, fk, pair in work_items:
            ok, k, s = _process_figure(annotator, sub, fk, pair)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, annotator, sub, fk, pair): fk
                for sub, fk, pair in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED: {e}")
                    with lock:
                        errors += 1

    # Summary
    print(f"\n=== SUMMARY ({annotator.model_name}) ===")
    eval_dir = OUTPUT_DIR / annotator.model_name
    scores = []
    patterns = {}
    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        s = data.get("score")
        p = data.get("pattern", "unknown")
        if s is not None:
            scores.append(s)
            patterns[p] = patterns.get(p, 0) + 1

    if scores:
        print(f"  Score: {sum(scores)/len(scores):.2f} ({len(scores)} pairs)")
        print(f"  Patterns: {patterns}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Run prompt reverse with A/B forced format")
    p.add_argument("model", nargs="?", default="gpt-5.2", help="Model name")
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

    run(a.model, a.workers, a.subfolder)
