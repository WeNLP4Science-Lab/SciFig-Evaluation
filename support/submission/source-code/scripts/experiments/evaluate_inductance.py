"""Evaluate inductance probe responses.

For each probe, the judge checks if the model:
1. Fell for the trap (naive answer) — score 0
2. Showed partial reasoning — score 0.5
3. Reasoned correctly (correct answer with working) — score 1

Output: output/experiments/evaluation/inductance/{judge}/{model}/{fig_key}.json

Usage:
    python3 scripts/experiments/evaluate_inductance.py --model gemini-3.1-pro --judge gpt-4o
    python3 scripts/experiments/evaluate_inductance.py --model gpt-5.2 --judge mistral-large-3
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

RESPONSES_DIR = ROOT / "output" / "experiments" / "inductance"
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "inductance"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

JUDGE_PROMPT = """\
You are evaluating whether a model demonstrated genuine deep reasoning when answering a question about a scientific figure.

You are given:
1. The question that was asked
2. The expected correct answer (with reasoning)
3. The naive/wrong answer that a surface-level reading would produce
4. What the trap is (what makes this question hard)
5. The model's actual answer

Evaluate the model's response:

**Score 1.0 — Correct reasoning:**
- Model arrived at the correct answer AND showed the reasoning steps
- The working/computation must be present, not just the final answer
- Model explicitly addressed or avoided the trap

**Score 0.5 — Partial reasoning:**
- Model showed some awareness of the trap but didn't fully resolve it
- OR model got the right answer but without clear reasoning
- OR model identified the issue but made computational errors

**Score 0.0 — Fell for the trap:**
- Model gave the naive/wrong answer
- OR model showed no awareness of the trap
- OR model's reasoning was fundamentally flawed

Respond ONLY in JSON:
{
  "score": 0.0 | 0.5 | 1.0,
  "fell_for_trap": true | false,
  "showed_reasoning": true | false,
  "correct_answer": true | false,
  "reason": "<brief explanation, max 30 words>"
}"""


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


def _evaluate(client, judge_deployment, response_data):
    user_msg = f"""## Question
{response_data['question']}

## Expected Correct Answer
{response_data['expected_answer']}

## Naive/Wrong Answer (trap)
{response_data.get('naive_answer', 'N/A')}

## What Makes This Hard
{response_data.get('trap', 'N/A')}

## Model's Answer
{response_data['model_answer']}"""

    def _call():
        response = client.chat.completions.create(
            model=judge_deployment,
            messages=[
                {"role": "system", "content": JUDGE_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=200,
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)

    return _retry(_call)


def run(model_name, judge_name="gpt-4o", workers=1):
    client = _get_judge_client()

    resp_dir = RESPONSES_DIR / model_name
    if not resp_dir.exists():
        logger.error(f"No inductance responses for {model_name}")
        return

    work_items = []
    skipped = 0
    for resp_file in sorted(resp_dir.glob("*.json")):
        fig_key = resp_file.stem
        out_path = OUTPUT_DIR / judge_name / model_name / f"{fig_key}.json"
        if out_path.exists():
            skipped += 1
        else:
            work_items.append((fig_key, resp_file))

    logger.info(f"Inductance evaluation | model={model_name} | judge={judge_name}")
    logger.info(f"Total: {len(work_items) + skipped} ({skipped} done, {len(work_items)} to evaluate)")

    if not work_items:
        logger.info("Nothing to do.")
        _print_summary(model_name, judge_name)
        return

    for fig_key, resp_file in work_items:
        with open(resp_file) as f:
            resp_data = json.load(f)

        try:
            result = _evaluate(client, judge_name, resp_data)

            output = {
                "figure_key": fig_key,
                "model_name": model_name,
                "judge_model": judge_name,
                "question": resp_data["question"],
                "expected_answer": resp_data["expected_answer"],
                "naive_answer": resp_data.get("naive_answer", ""),
                "trap": resp_data.get("trap", ""),
                "model_answer": resp_data["model_answer"],
                "score": result.get("score", 0),
                "fell_for_trap": result.get("fell_for_trap", True),
                "showed_reasoning": result.get("showed_reasoning", False),
                "correct_answer": result.get("correct_answer", False),
                "reason": result.get("reason", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            out_path = OUTPUT_DIR / judge_name / model_name / f"{fig_key}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            score_tag = "✅" if output["score"] == 1.0 else "⚠️" if output["score"] == 0.5 else "❌"
            trap_tag = "TRAPPED" if output["fell_for_trap"] else "AVOIDED"
            logger.info(f"  {score_tag} {fig_key}: {output['score']} ({trap_tag}) — {output['reason']}")

        except Exception as e:
            logger.error(f"  FAIL {fig_key}: {e}")

    _print_summary(model_name, judge_name)


def _print_summary(model_name, judge_name):
    eval_dir = OUTPUT_DIR / judge_name / model_name
    if not eval_dir.exists():
        return

    scores = []
    trapped = 0
    reasoned = 0
    correct = 0
    total = 0

    for f in sorted(eval_dir.glob("*.json")):
        data = json.load(open(f))
        total += 1
        scores.append(data.get("score", 0))
        if data.get("fell_for_trap"):
            trapped += 1
        if data.get("showed_reasoning"):
            reasoned += 1
        if data.get("correct_answer"):
            correct += 1

    if total:
        avg = sum(scores) / len(scores)
        print(f"\n=== SUMMARY ({model_name} judged by {judge_name}) ===")
        print(f"  Score: {avg:.2f} ({total} probes)")
        print(f"  Fell for trap: {trapped}/{total}")
        print(f"  Showed reasoning: {reasoned}/{total}")
        print(f"  Correct answer: {correct}/{total}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate inductance probe responses")
    p.add_argument("--model", required=True)
    p.add_argument("--judge", default="gpt-4o")
    a = p.parse_args()
    run(a.model, a.judge)
