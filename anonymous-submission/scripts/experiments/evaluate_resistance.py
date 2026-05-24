"""Evaluate resistance (hallucination) probe responses using an LLM judge.

For each probe, the judge scores whether the model:
  - inexist:       recognized the element doesn't exist (1.0/0.5/0.0)
  - contra:        detected and corrected the false premise (1.0/0.5/0.0)
  - unanswerable:  stated info can't be determined from chart (1.0/0.5/0.0)

Input:  results/generation/resistance/{model}/{fig_id}.json
        dataset/resistance_probes/{fig_id}.json
Output: results/evaluation/resistance/{model}/{fig_id}.json

Usage:
    python evaluate_resistance.py gpt-5.2 --workers 4
    python evaluate_resistance.py gemma3-27b-it --figures fig_002 fig_009
"""

from __future__ import annotations

import re
import json
import argparse
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import MODELS, RESULTS_DIR, DATASET_DIR, AZURE_API_VERSION, get_azure_endpoint, get_azure_api_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

PROBES_DIR = DATASET_DIR / "resistance_probes"
GEN_DIR = RESULTS_DIR / "generation" / "resistance"
EVAL_DIR = RESULTS_DIR / "evaluation" / "resistance"

JUDGE_MODEL = "gpt-4o"

JUDGE_PROMPTS = {
    "inexist": """You are evaluating whether a vision-language model correctly identified that a chart element does NOT exist.

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

    "contra": """You are evaluating whether a vision-language model detected and corrected a FALSE PREMISE in a question about a scientific figure.

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

    "unanswerable": """You are evaluating whether a vision-language model correctly recognized that a question CANNOT BE ANSWERED from the chart alone.

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
    from openai import AzureOpenAI
    return AzureOpenAI(
        azure_endpoint=get_azure_endpoint(),
        api_key=get_azure_api_key(),
        api_version=AZURE_API_VERSION,
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


def _parse_answers(raw_response, n=3):
    """Parse numbered answers from the raw response."""
    sections = {}
    current_num = None
    current_lines = []

    for line in raw_response.strip().split("\n"):
        stripped = line.strip()
        stripped_clean = re.sub(r'^#{1,3}\s*', '', stripped)
        stripped_clean = re.sub(r'^\*{1,2}\s*', '', stripped_clean)

        m = re.match(r'^(\d+)\s*[.):\t]', stripped_clean)
        if m:
            num = int(m.group(1))
            if 1 <= num <= n:
                if current_num is not None:
                    sections[current_num] = "\n".join(current_lines).strip()
                current_num = num
                rest = re.sub(r'^[#*\s]*\d+\s*[.):\t\s]+', '', stripped).strip()
                current_lines = [rest] if rest else []
                continue

        if current_num is not None:
            current_lines.append(stripped)

    if current_num is not None:
        sections[current_num] = "\n".join(current_lines).strip()

    return sections


def evaluate_figure(client, model_name, fig_id):
    out_path = EVAL_DIR / model_name / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    gen_path = GEN_DIR / model_name / f"{fig_id}.json"
    probe_path = PROBES_DIR / f"{fig_id}.json"

    if not gen_path.exists():
        return False, "missing_response"
    if not probe_path.exists():
        return False, "missing_probes"

    with open(gen_path) as f:
        gen = json.load(f)
    with open(probe_path) as f:
        probe_data = json.load(f)

    raw_response = gen.get("raw_response", "")
    probes = probe_data.get("probes", [])

    if not raw_response.strip():
        return False, "empty_response"

    # Parse numbered answers
    answers = _parse_answers(raw_response, len(probes))

    evaluations = []
    for i, probe in enumerate(probes):
        model_answer = answers.get(i + 1, "")
        probe_type = probe["type"]

        template = JUDGE_PROMPTS.get(probe_type)
        if not template:
            continue

        format_args = {
            "question": probe.get("question", ""),
            "expected_behavior": probe.get("expected_behavior", ""),
            "model_answer": model_answer if model_answer else "(no answer parsed)",
            "false_element": probe.get("false_element", ""),
            "false_premise": probe.get("false_premise", ""),
            "why_unanswerable": probe.get("why_unanswerable", ""),
        }

        judge_prompt = template.format(**format_args)

        try:
            def _call():
                response = client.chat.completions.create(
                    model=JUDGE_MODEL,
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

            result = _retry(_call)
            evaluations.append({
                "probe_type": probe_type,
                "question": probe["question"],
                "model_answer": model_answer,
                "judge_score": result.get("score"),
                "judge_reasoning": result.get("reasoning", ""),
            })
        except Exception as e:
            logger.error(f"  Judge failed on {fig_id}/{probe_type}: {e}")
            evaluations.append({
                "probe_type": probe_type,
                "question": probe["question"],
                "model_answer": model_answer,
                "judge_score": None,
                "judge_reasoning": f"Judge error: {e}",
            })

    # Compute per-type scores
    type_scores = {}
    for ev in evaluations:
        if ev["judge_score"] is not None:
            type_scores.setdefault(ev["probe_type"], []).append(ev["judge_score"])

    output = {
        "figure_id": fig_id,
        "model_name": model_name,
        "judge_model": JUDGE_MODEL,
        "figure_type": probe_data.get("figure_type", ""),
        "evaluations": evaluations,
        "scores": {t: sum(s) / len(s) for t, s in type_scores.items()},
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    scores_str = " ".join(f"{t}={sum(s)/len(s):.1f}" for t, s in type_scores.items())
    logger.info(f"  OK {fig_id} — {scores_str}")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.model not in MODELS:
        print(f"Unknown model. Available: {', '.join(sorted(MODELS.keys()))}")
        return

    client = _get_judge_client()

    if args.figures:
        fig_ids = args.figures
    else:
        gen_dir = GEN_DIR / args.model
        if not gen_dir.exists():
            print(f"No resistance responses for {args.model}. Run run_resistance.py first.")
            return
        fig_ids = sorted(p.stem for p in gen_dir.glob("*.json"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (EVAL_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Resistance eval | model={args.model} | judge={JUDGE_MODEL}")
    logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to evaluate)")

    if not work:
        logger.info("Nothing to do.")
        return

    success, errors = 0, 0
    lock = threading.Lock()

    if args.workers == 1:
        for fid in work:
            ok, status = evaluate_figure(client, args.model, fid)
            if ok: success += 1
            else: errors += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(evaluate_figure, client, args.model, fid): fid for fid in work}
            for f in as_completed(futs):
                ok, status = f.result()
                with lock:
                    if ok: success += 1
                    else: errors += 1

    # Summary
    eval_dir = EVAL_DIR / args.model
    type_scores = {}
    for ef in eval_dir.glob("*.json"):
        data = json.load(open(ef))
        for ev in data.get("evaluations", []):
            t = ev["probe_type"]
            s = ev.get("judge_score")
            if s is not None:
                type_scores.setdefault(t, []).append(s)

    print(f"\n=== SUMMARY ({args.model} judged by {JUDGE_MODEL}) ===")
    for t, scores in sorted(type_scores.items()):
        avg = sum(scores) / len(scores)
        print(f"  {t:15s}: {avg:.2f} ({len(scores)} probes)")

    all_scores = [s for ss in type_scores.values() for s in ss]
    if all_scores:
        print(f"  {'OVERALL':15s}: {sum(all_scores)/len(all_scores):.2f} ({len(all_scores)} probes)")

    logger.info(f"Done. {success} ok, {errors} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
