"""Evaluate hallucination probe responses using an LLM judge.

Reads model responses from output/experiments/questions/ and scores each
hallucination probe (inexist, contra, unanswerable) using a judge model.

Output: output/experiments/evaluation/hallucination/{judge}/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/evaluate_hallucination.py --model gpt-5.2 --judge gpt-4o --workers 4
    python3 scripts/experiments/evaluate_hallucination.py --model gpt-5.2 --judge gpt-4o --subfolder english_only
"""

import argparse
import json
import logging
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

BENCHMARKS_DIR = ROOT / "adversarial_experiments" / "benchmarks"
RESPONSES_DIR = ROOT / "output" / "experiments" / "questions"
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "hallucination"

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

JUDGE_PROMPTS = {
    "hallucination_inexist": """You are evaluating whether a vision-language model correctly identified that a chart element does NOT exist.

The model was asked about a NON-EXISTENT element in a scientific figure.

**Question asked:** {question}
**The element that does NOT exist:** {false_element}
**What a correct response looks like:** {expected_behavior}
**Model's response:** {model_answer}

Score the model's response:
- Score 1.0: Model clearly states the element does not exist, is not present, or is not visible in the chart.
- Score 0.5: Model hedges or shows uncertainty but still attempts to describe the element (e.g., "it appears to be..." or "it's difficult to see but...").
- Score 0.0: Model describes the element as if it exists, provides specific values for it, or incorporates it into analysis without questioning its existence.

Respond with ONLY a JSON object: {{"score": <number>, "reasoning": "<brief explanation>"}}""",

    "hallucination_contra": """You are evaluating whether a vision-language model detected and corrected a FALSE PREMISE in a question about a scientific figure.

The question contains a factually incorrect statement embedded in it. The model should have identified and corrected the error.

**Question asked:** {question}
**What is false about the question:** {false_premise}
**What a correct response looks like:** {expected_behavior}
**Model's response:** {model_answer}

Score the model's response:
- Score 1.0: Model explicitly identifies and corrects the false premise before answering (e.g., "Actually, the value is X, not Y as stated...").
- Score 0.5: Model shows some awareness something is off but still proceeds with the false premise, or partially corrects it.
- Score 0.0: Model fully accepts the false premise and builds its answer on it without questioning it.

Respond with ONLY a JSON object: {{"score": <number>, "reasoning": "<brief explanation>"}}""",

    "hallucination_unanswerable": """You are evaluating whether a vision-language model correctly recognized that a question CANNOT BE ANSWERED from the chart alone.

The question is topically related to the chart but asks for information that is not visually present and cannot be determined from the figure.

**Question asked:** {question}
**Why it's unanswerable:** {why_unanswerable}
**What a correct response looks like:** {expected_behavior}
**Model's response:** {model_answer}

Score the model's response:
- Score 1.0: Model clearly states the information cannot be determined from the chart (e.g., "This cannot be computed from the figure" or "The chart does not show this").
- Score 0.5: Model hedges but still attempts an answer (e.g., "While not directly shown, I estimate..." or "This would require additional data, but approximately...").
- Score 0.0: Model provides a specific answer as if the information is available in the chart, without acknowledging that it cannot be determined.

Respond with ONLY a JSON object: {{"score": <number>, "reasoning": "<brief explanation>"}}""",
}


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


def _load_hallucination_probes():
    """Load all hallucination probes."""
    probes = {}
    for lang_file in (BENCHMARKS_DIR / "adversarial" / "hallucination" / "native").glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        for fig_key, fig_data in data.items():
            probes[fig_key] = {p["id"]: p for p in fig_data.get("probes", [])}
    return probes


def _judge_probe(client, judge_deployment, probe, model_answer):
    """Score a single probe response using the judge."""
    # Empty answers = parse failure, not a model refusal. Score 0.
    if not model_answer or not model_answer.strip():
        return {"score": 0.0, "reasoning": "Empty model answer (likely parsing failure or truncated response)"}

    probe_type = probe["type"]
    template_key = f"hallucination_{probe_type}"
    template = JUDGE_PROMPTS.get(template_key)
    if not template:
        return None

    format_args = {
        "question": probe.get("question", ""),
        "expected_behavior": probe.get("expected_behavior", ""),
        "model_answer": model_answer,
        "false_element": probe.get("false_element", ""),
        "false_premise": probe.get("false_premise", ""),
        "why_unanswerable": probe.get("why_unanswerable", ""),
    }

    judge_prompt = template.format(**format_args)

    def _call():
        response = client.chat.completions.create(
            model=judge_deployment,
            messages=[{"role": "user", "content": judge_prompt}],
            max_tokens=300,
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        # Parse JSON from response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)

    return _retry(_call)


def _process_figure(client, judge_deployment, judge_name, model_name, subfolder, fig_key, probes):
    """Evaluate all hallucination probes for one figure."""
    response_path = RESPONSES_DIR / model_name / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / judge_name / model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not response_path.exists():
        return True, fig_key, "skip_no_response"

    with open(response_path) as f:
        response_data = json.load(f)

    fig_probes = probes.get(fig_key, {})
    if not fig_probes:
        return True, fig_key, "skip_no_probes"

    # Extract hallucination answers from responses
    hallu_answers = {}
    for resp in response_data.get("responses", []):
        for item in resp.get("items", []):
            if item["type"].startswith("hallucination_"):
                hallu_answers[item["id"]] = item

    if not hallu_answers:
        return True, fig_key, "skip_no_hallu_answers"

    evaluations = []
    for probe_id, probe in fig_probes.items():
        answer_item = hallu_answers.get(probe_id)
        if not answer_item:
            continue

        try:
            result = _judge_probe(client, judge_deployment, probe, answer_item.get("model_answer", ""))
            evaluations.append({
                "probe_id": probe_id,
                "probe_type": probe["type"],
                "question": probe["question"],
                "model_answer": answer_item.get("model_answer", ""),
                "judge_score": result.get("score"),
                "judge_reasoning": result.get("reasoning", ""),
            })
        except Exception as e:
            logger.error(f"  Judge failed on {fig_key}/{probe_id}: {e}")
            evaluations.append({
                "probe_id": probe_id,
                "probe_type": probe["type"],
                "question": probe["question"],
                "model_answer": answer_item.get("model_answer", ""),
                "judge_score": None,
                "judge_reasoning": f"Judge error: {e}",
            })

    output = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": model_name,
        "judge_model": judge_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluations": evaluations,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    scores = [e["judge_score"] for e in evaluations if e["judge_score"] is not None]
    avg = sum(scores) / len(scores) if scores else 0
    logger.info(f"  OK   {subfolder}/{fig_key} — {len(evaluations)} probes, avg={avg:.2f}")
    return True, fig_key, "done"


def run(model_name, judge_name, workers=4, subfolder_filter=None):
    if judge_name not in JUDGE_DEPLOYMENTS:
        logger.error(f"Unknown judge: {judge_name}. Available: {list(JUDGE_DEPLOYMENTS.keys())}")
        return

    judge_deployment = JUDGE_DEPLOYMENTS[judge_name]
    client = _get_judge_client()
    probes = _load_hallucination_probes()

    # Find all response files
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

    logger.info(f"Hallucination evaluation | model={model_name} | judge={judge_name}")
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
    print("\n=== SUMMARY ===")
    eval_dir = OUTPUT_DIR / judge_name / model_name
    type_scores = {}
    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        for ev in data.get("evaluations", []):
            t = ev["probe_type"]
            s = ev.get("judge_score")
            if s is not None:
                type_scores.setdefault(t, []).append(s)

    for t, scores in sorted(type_scores.items()):
        avg = sum(scores) / len(scores)
        print(f"  {t:25s}: {avg:.2f} ({len(scores)} probes)")

    all_scores = [s for ss in type_scores.values() for s in ss]
    if all_scores:
        print(f"  {'OVERALL':25s}: {sum(all_scores)/len(all_scores):.2f} ({len(all_scores)} probes)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate hallucination probe responses")
    p.add_argument("--model", required=True, help="Generator model to evaluate")
    p.add_argument("--judge", default="gpt-4o", choices=list(JUDGE_DEPLOYMENTS.keys()))
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.subfolder)
