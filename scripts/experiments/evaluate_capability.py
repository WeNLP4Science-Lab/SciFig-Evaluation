"""Evaluate capability question responses.

For exact/approximate answers: rule-based scoring.
For open_ended answers: LLM judge.

Output: output/experiments/evaluation/capability/{judge}/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/evaluate_capability.py --model gemini-3.1-pro --judge gpt-4o --subfolder multi_language
"""

import argparse
import json
import logging
import os
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

BENCHMARKS_DIR = ROOT / "adversarial_experiments" / "benchmarks"
RESPONSES_DIR = ROOT / "output" / "experiments" / "questions"
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "capability"

JUDGE_DEPLOYMENTS = {
    "gpt-4o": "gpt-4o",
    "mistral-large-3": "mistral-large-3",
}

SUBFOLDER_TO_LANG_KEY = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def _get_judge_client():
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-12-01-preview",
    )


def _retry(func, max_retries=3, backoff=2.0):
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= backoff


def _load_capability_questions():
    """Load all capability questions with their expected answers and ranges.

    Only loads the main language file per subfolder, not translated variants
    (e.g., loads multi_language.json but skips multi_language_bg.json).
    """
    questions = {}
    main_files = ["bulgarian.json", "chinese.json", "english.json", "german.json", "multi_language.json"]
    for fname in main_files:
        lang_file = BENCHMARKS_DIR / "capability" / "native" / fname
        if not lang_file.exists():
            continue
        try:
            with open(lang_file) as f:
                data = json.load(f)
            for fig_key, fig_data in data.items():
                questions[fig_key] = {q["id"]: q for q in fig_data.get("questions", [])}
        except json.JSONDecodeError:
            continue
    return questions


def _load_excluded():
    """Load excluded questions."""
    exc_path = BENCHMARKS_DIR / "capability" / "excluded_questions.json"
    if exc_path.exists():
        data = json.load(open(exc_path))
        return {(e["figure_key"], e["question_id"]) for e in data.get("excluded", [])}
    return set()


def _score_with_judge(client, judge_deployment, question, model_answer, expected_answer, answer_type, acceptable_range=None):
    """Score any answer type using LLM judge."""
    if not model_answer:
        return 0.0, "Empty answer"

    range_info = ""
    if acceptable_range and len(acceptable_range) == 2:
        range_info = f"\nAcceptable range: [{acceptable_range[0]}, {acceptable_range[1]}]"

    prompt = f"""A model was asked a question about a scientific figure. Evaluate if the model's answer is correct.

Question: {question}
Expected answer: {expected_answer}{range_info}
Answer type: {answer_type}
Model's answer: {model_answer}

Scoring rules:
- For "exact" answers: the model must provide the correct value or information. Minor formatting differences are OK (e.g., "52%" vs "52 percent").
- For "approximate" answers: if an acceptable range is given, the model's value must fall within it. If no range, within 30% of expected is acceptable.
- For "open_ended" answers: judge if the model's reasoning and conclusion align with the expected answer.

Score:
- 1.0 = Correct answer
- 0.5 = Partially correct (right direction but wrong specifics)
- 0.0 = Incorrect answer

Respond ONLY in JSON: {{"score": <number>, "reason": "max 15 words"}}"""

    def _call():
        response = client.chat.completions.create(
            model=judge_deployment,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)

    result = _retry(_call)
    return result.get("score", 0), result.get("reason", "")


def _process_figure(client, judge_deployment, judge_name, model_name, subfolder, fig_key, all_questions, excluded):
    """Evaluate capability questions for one figure."""
    response_path = RESPONSES_DIR / model_name / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / judge_name / model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not response_path.exists():
        return True, fig_key, "skip_no_response"

    fig_questions = all_questions.get(fig_key, {})
    if not fig_questions:
        return True, fig_key, "skip_no_questions"

    with open(response_path) as f:
        response_data = json.load(f)

    # Extract capability answers
    cap_answers = {}
    for resp in response_data.get("responses", []):
        for item in resp.get("items", []):
            if item["type"] == "capability":
                cap_answers[item["id"]] = item.get("model_answer", "")

    evaluations = []
    for qid, q in fig_questions.items():
        if (fig_key, qid) in excluded:
            evaluations.append({
                "question_id": qid,
                "question": q.get("question", ""),
                "expected_answer": q.get("expected_answer", ""),
                "model_answer": cap_answers.get(qid, ""),
                "answer_type": q.get("answer_type", ""),
                "score": None,
                "reason": "Excluded from scoring",
                "excluded": True,
            })
            continue

        model_ans = cap_answers.get(qid, "")
        answer_type = q.get("answer_type", "exact")
        expected = q.get("expected_answer", "")
        acceptable_range = q.get("acceptable_range")

        try:
            score, reason = _score_with_judge(
                client, judge_deployment,
                q.get("question", ""), model_ans, expected,
                answer_type, acceptable_range
            )
        except Exception as e:
            score, reason = None, f"Error: {e}"

        evaluations.append({
            "question_id": qid,
            "question": q.get("question", ""),
            "expected_answer": expected,
            "model_answer": model_ans,
            "answer_type": answer_type,
            "acceptable_range": acceptable_range,
            "score": score,
            "reason": reason,
            "excluded": False,
        })

    scored = [e for e in evaluations if e["score"] is not None and not e.get("excluded")]
    avg = sum(e["score"] for e in scored) / len(scored) if scored else 0

    output = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": model_name,
        "judge_model": judge_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluations": evaluations,
        "average_score": avg,
        "total_scored": len(scored),
        "total_excluded": sum(1 for e in evaluations if e.get("excluded")),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK   {subfolder}/{fig_key} — {len(scored)} scored, avg={avg:.2f}")
    return True, fig_key, "done"


def run(model_name, judge_name, workers=4, subfolder_filter=None):
    if judge_name not in JUDGE_DEPLOYMENTS:
        logger.error(f"Unknown judge: {judge_name}")
        return

    judge_deployment = JUDGE_DEPLOYMENTS[judge_name]
    client = _get_judge_client()
    all_questions = _load_capability_questions()
    excluded = _load_excluded()

    response_dir = RESPONSES_DIR / model_name
    if not response_dir.exists():
        logger.error(f"No responses for {model_name}")
        return

    work_items = []
    skipped = 0
    for subfolder_dir in sorted(response_dir.iterdir()):
        if not subfolder_dir.is_dir():
            continue
        subfolder = subfolder_dir.name
        if subfolder_filter and subfolder != subfolder_filter:
            continue
        for resp_file in sorted(subfolder_dir.glob("*.json")):
            fig_key = resp_file.stem
            out_path = OUTPUT_DIR / judge_name / model_name / subfolder / f"{fig_key}.json"
            if out_path.exists():
                skipped += 1
            else:
                work_items.append((subfolder, fig_key))

    logger.info(f"Capability evaluation | model={model_name} | judge={judge_name}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to evaluate)")

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

    if workers == 1:
        for sub, fk in work_items:
            ok, k, s = _process_figure(client, judge_deployment, judge_name, model_name, sub, fk, all_questions, excluded)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, client, judge_deployment, judge_name, model_name, sub, fk, all_questions, excluded): fk
                for sub, fk in work_items
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
    print(f"\n=== SUMMARY ({model_name} judged by {judge_name}) ===")
    eval_dir = OUTPUT_DIR / judge_name / model_name
    all_scores = []
    by_type = {}
    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        for ev in data.get("evaluations", []):
            if ev.get("excluded") or ev.get("score") is None:
                continue
            all_scores.append(ev["score"])
            t = ev.get("answer_type", "unknown")
            by_type.setdefault(t, []).append(ev["score"])

    if all_scores:
        print(f"  Overall: {sum(all_scores)/len(all_scores):.2f} ({len(all_scores)} questions)")
        for t, scores in sorted(by_type.items()):
            print(f"  {t}: {sum(scores)/len(scores):.2f} ({len(scores)} questions)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate capability questions")
    p.add_argument("--model", required=True)
    p.add_argument("--judge", default="gpt-4o", choices=list(JUDGE_DEPLOYMENTS.keys()))
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.subfolder)
