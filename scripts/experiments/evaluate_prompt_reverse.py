"""Evaluate prompt reverse consistency using an LLM judge.

For each figure, sends both the true and false statement responses to the judge
in a single call. The judge determines if the model was consistent and correct.

Output: output/experiments/evaluation/prompt_reverse/{judge}/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/evaluate_prompt_reverse.py --model gemini-3.1-pro --judge gpt-4o
"""

import argparse
import json
import logging
import os
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
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "prompt_reverse"

JUDGE_DEPLOYMENTS = {
    "gpt-4o": "gpt-4o",
    "gpt-5.4-mini": "gpt-5.4-mini",
    "mistral-large-3": "mistral-large-3",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

SUBFOLDER_TO_LANG_KEY = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "multi_language",
}

JUDGE_PROMPT = """You are evaluating whether a vision-language model gave consistent and correct responses when asked about the same visual fact with opposite framing.

The model was shown a scientific figure and asked two separate yes/no questions about the same fact — one true, one false. The model answered each independently (it never saw both at once).

**The TRUE statement (this is factually correct based on the figure):**
{true_statement}

**Model's response to the TRUE statement:**
{true_response}

**The FALSE statement (this is factually incorrect based on the figure):**
{false_statement}

**Model's response to the FALSE statement:**
{false_response}

**Visual fact being tested:** {fact_description}

Evaluate the model's pair of responses:
- Score 1.0: Model AGREES with the true statement AND DISAGREES with the false statement. This is correct and consistent — the model is visually grounded.
- Score 0.5: Model agrees with one and disagrees with the other, but it agreed with the FALSE statement and disagreed with the TRUE statement. The model is consistent but has the wrong understanding.
- Score 0.0: Model agrees with BOTH statements or disagrees with BOTH statements. The model is inconsistent — it is not grounded in the visual evidence.

Respond with ONLY a JSON object: {{"score": <number>, "pattern": "<agrees_both|disagrees_both|correct|reversed>", "reasoning": "<brief explanation>"}}"""


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


def _load_prompt_reverse_probes():
    """Load all prompt reverse pairs."""
    probes = {}
    for lang_file in (BENCHMARKS_DIR / "adversarial" / "prompt_reverse" / "native").glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        for fig_key, fig_data in data.items():
            probes[fig_key] = fig_data.get("pair", {})
    return probes


def _process_figure(client, judge_deployment, judge_name, model_name, subfolder, fig_key, probes):
    """Evaluate prompt reverse for one figure."""
    response_path = RESPONSES_DIR / model_name / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / judge_name / model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not response_path.exists():
        return True, fig_key, "skip_no_response"

    pair = probes.get(fig_key)
    if not pair:
        return True, fig_key, "skip_no_pair"

    with open(response_path) as f:
        response_data = json.load(f)

    # Extract true and false responses
    true_response = ""
    false_response = ""
    for resp in response_data.get("responses", []):
        for item in resp.get("items", []):
            if item["type"] == "prompt_reverse_true":
                true_response = item.get("model_answer", "")
            elif item["type"] == "prompt_reverse_false":
                false_response = item.get("model_answer", "")

    if not true_response and not false_response:
        return True, fig_key, "skip_no_pr_answers"

    # Handle empty answers
    if not true_response.strip() or not false_response.strip():
        result = {
            "score": 0.0,
            "pattern": "missing_response",
            "reasoning": "One or both responses are empty (parsing failure or truncated)"
        }
    else:
        judge_prompt = JUDGE_PROMPT.format(
            true_statement=pair.get("true_statement", ""),
            true_response=true_response,
            false_statement=pair.get("false_statement", ""),
            false_response=false_response,
            fact_description=pair.get("fact_description", ""),
        )

        def _call():
            response = client.chat.completions.create(
                model=judge_deployment,
                messages=[{"role": "user", "content": judge_prompt}],
                max_tokens=300,
                temperature=0,
            )
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text)

        try:
            result = _retry(_call)
        except Exception as e:
            logger.error(f"  Judge failed on {fig_key}: {e}")
            result = {"score": None, "pattern": "judge_error", "reasoning": str(e)}

    output = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": model_name,
        "judge_model": judge_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "true_statement": pair.get("true_statement", ""),
        "false_statement": pair.get("false_statement", ""),
        "fact_description": pair.get("fact_description", ""),
        "true_response": true_response,
        "false_response": false_response,
        "evaluation": result,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    score = result.get("score", "?")
    pattern = result.get("pattern", "?")
    logger.info(f"  OK   {subfolder}/{fig_key} — score={score} pattern={pattern}")
    return True, fig_key, "done"


def run(model_name, judge_name, workers=4, subfolder_filter=None):
    if judge_name not in JUDGE_DEPLOYMENTS:
        logger.error(f"Unknown judge: {judge_name}. Available: {list(JUDGE_DEPLOYMENTS.keys())}")
        return

    judge_deployment = JUDGE_DEPLOYMENTS[judge_name]
    client = _get_judge_client()
    probes = _load_prompt_reverse_probes()

    response_dir = RESPONSES_DIR / model_name
    if not response_dir.exists():
        logger.error(f"No responses found for model {model_name}")
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

    logger.info(f"Prompt reverse evaluation | model={model_name} | judge={judge_name}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to evaluate)")

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
        for sub, fk in work_items:
            ok, k, s = _process_figure(client, judge_deployment, judge_name, model_name, sub, fk, probes)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, client, judge_deployment, judge_name, model_name, sub, fk, probes): fk
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

    # Print summary
    print(f"\n=== SUMMARY ({model_name} judged by {judge_name}) ===")
    eval_dir = OUTPUT_DIR / judge_name / model_name
    scores = []
    patterns = {}
    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        ev = data.get("evaluation", {})
        s = ev.get("score")
        p = ev.get("pattern", "unknown")
        if s is not None:
            scores.append(s)
            patterns[p] = patterns.get(p, 0) + 1

    if scores:
        print(f"  Score: {sum(scores)/len(scores):.2f} ({len(scores)} pairs)")
        print(f"  Patterns: {patterns}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate prompt reverse consistency")
    p.add_argument("--model", required=True, help="Generator model to evaluate")
    p.add_argument("--judge", default="gpt-4o", choices=list(JUDGE_DEPLOYMENTS.keys()))
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.subfolder)
