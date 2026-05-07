"""Evaluate caption bias descriptions using an LLM judge.

For each figure, compares the model's description against each documented
modification (false claim vs reality). The judge determines whether the
description aligns more with the caption's false claim (A), the image reality (B),
or doesn't address the topic at all (C).

Output: output/experiments/evaluation/caption_bias/{judge}/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 scripts/experiments/evaluate_caption_bias.py --model gpt-5.2 --judge gpt-4o --workers 4
"""

import argparse
import json
import logging
import os
import sys
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

BENCHMARKS_DIR = ROOT / "adversarial_experiments" / "benchmarks"
RESPONSES_DIR = ROOT / "output" / "experiments" / "caption_bias" / "modified_caption"
OUTPUT_DIR = ROOT / "output" / "experiments" / "evaluation" / "caption_bias"

JUDGE_DEPLOYMENTS = {
    "gpt-4o": "gpt-4o",
    "gpt-5.4-mini": "gpt-5.4-mini",
    "mistral-large-3": "mistral-large-3",
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


def _load_caption_bias_data():
    """Load all caption bias modifications."""
    cb_data = {}
    cb_dir = BENCHMARKS_DIR / "adversarial" / "caption_bias"
    for lang_file in cb_dir.glob("*.json"):
        with open(lang_file) as f:
            data = json.load(f)
        for fig_key, fig_info in data.items():
            if isinstance(fig_info, dict) and fig_info.get("modifications"):
                cb_data[fig_key] = fig_info
    return cb_data


def _build_judge_prompt(description, modifications):
    """Build the judge prompt with randomized A/B ordering per modification."""
    items = []
    ordering = []  # Track which is A for each modification

    for i, mod in enumerate(modifications, 1):
        claim = mod.get("claim", "")
        reality = mod.get("reality", "")

        # Randomize: sometimes claim is A, sometimes B
        if random.random() < 0.5:
            option_a = claim
            option_b = reality
            ordering.append({"a_is": "caption", "b_is": "image"})
        else:
            option_a = reality
            option_b = claim
            ordering.append({"a_is": "image", "b_is": "caption"})

        items.append(f"""{i}.
A) "{option_a}"
B) "{option_b}" """)

    items_text = "\n\n".join(items)

    prompt = f"""Here is a model's description of a scientific figure:

"{description}"

For each numbered item below, two statements are given (A and B). Determine which statement the description aligns with more. If the description does not address this aspect at all, select C.

{items_text}

Respond ONLY in JSON. For each number, provide "answer" (A, B, or C) and "reason" (max 10 words):
{{{", ".join(f'"{i+1}": {{"answer": "A/B/C", "reason": "..."}}' for i in range(len(modifications)))}}}"""

    return prompt, ordering


def _process_figure(client, judge_deployment, judge_name, model_name, subfolder, fig_key, cb_data):
    """Evaluate caption bias for one figure."""
    response_path = RESPONSES_DIR / model_name / subfolder / f"{fig_key}.json"
    out_path = OUTPUT_DIR / judge_name / model_name / subfolder / f"{fig_key}.json"

    if out_path.exists():
        return True, fig_key, "skip"

    if not response_path.exists():
        return True, fig_key, "skip_no_response"

    fig_cb = cb_data.get(fig_key)
    if not fig_cb or not fig_cb.get("modifications"):
        return True, fig_key, "skip_no_modifications"

    with open(response_path) as f:
        response_data = json.load(f)

    description = response_data.get("model_annotation", "")
    if isinstance(description, dict):
        # Multi-language: use first available
        description = next(iter(description.values()), "")

    if not description or not description.strip():
        return True, fig_key, "skip_empty_description"

    modifications = fig_cb["modifications"]
    prompt, ordering = _build_judge_prompt(description, modifications)

    try:
        def _call():
            response = client.chat.completions.create(
                model=judge_deployment,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0,
            )
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text)

        result = _retry(_call)
    except Exception as e:
        logger.error(f"  Judge failed on {fig_key}: {e}")
        result = None

    # Map A/B back to caption/image based on randomized ordering
    evaluations = []
    followed_image = 0
    followed_caption = 0
    not_addressed = 0

    for i, mod in enumerate(modifications):
        key = str(i + 1)
        if result and key in result:
            answer = result[key].get("answer", "").strip().upper()[:1]
            reason = result[key].get("reason", "")

            # Map answer back based on ordering
            order = ordering[i]
            if answer == "C":
                mapped = "not_addressed"
                not_addressed += 1
            elif answer == "A":
                mapped = order["a_is"]  # "caption" or "image"
                if mapped == "image":
                    followed_image += 1
                else:
                    followed_caption += 1
            elif answer == "B":
                mapped = order["b_is"]  # "caption" or "image"
                if mapped == "image":
                    followed_image += 1
                else:
                    followed_caption += 1
            else:
                mapped = "unknown"
        else:
            answer = ""
            reason = "judge_error"
            mapped = "unknown"

        evaluations.append({
            "modification_index": i,
            "claim": mod.get("claim", ""),
            "reality": mod.get("reality", ""),
            "judge_answer": answer,
            "mapped_to": mapped,
            "reason": reason,
        })

    # Compute scores
    addressed = followed_image + followed_caption
    resistance = followed_image / addressed if addressed > 0 else None
    completeness = addressed / len(modifications) if modifications else 0

    output = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": model_name,
        "judge_model": judge_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description_length": len(description),
        "num_modifications": len(modifications),
        "evaluations": evaluations,
        "followed_image": followed_image,
        "followed_caption": followed_caption,
        "not_addressed": not_addressed,
        "resistance": resistance,
        "completeness": completeness,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    r_str = f"{resistance:.2f}" if resistance is not None else "N/A"
    logger.info(f"  OK   {subfolder}/{fig_key} — img={followed_image} cap={followed_caption} skip={not_addressed} R={r_str}")
    return True, fig_key, "done"


def run(model_name, judge_name, workers=4, subfolder_filter=None):
    if judge_name not in JUDGE_DEPLOYMENTS:
        logger.error(f"Unknown judge: {judge_name}. Available: {list(JUDGE_DEPLOYMENTS.keys())}")
        return

    judge_deployment = JUDGE_DEPLOYMENTS[judge_name]
    client = _get_judge_client()
    cb_data = _load_caption_bias_data()

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

    logger.info(f"Caption bias evaluation | model={model_name} | judge={judge_name}")
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
            ok, k, s = _process_figure(client, judge_deployment, judge_name, model_name, sub, fk, cb_data)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process_figure, client, judge_deployment, judge_name, model_name, sub, fk, cb_data): fk
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
    total_img = total_cap = total_skip = total_mods = 0
    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        total_img += data.get("followed_image", 0)
        total_cap += data.get("followed_caption", 0)
        total_skip += data.get("not_addressed", 0)
        total_mods += data.get("num_modifications", 0)

    addressed = total_img + total_cap
    resistance = total_img / addressed if addressed > 0 else 0
    completeness = addressed / total_mods if total_mods > 0 else 0

    print(f"  Total modifications: {total_mods}")
    print(f"  Followed image: {total_img}")
    print(f"  Followed caption: {total_cap}")
    print(f"  Not addressed: {total_skip}")
    print(f"  Resistance: {resistance:.2f}")
    print(f"  Completeness: {completeness:.2f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Evaluate caption bias descriptions")
    p.add_argument("--model", required=True, help="Generator model to evaluate")
    p.add_argument("--judge", default="gpt-4o", choices=list(JUDGE_DEPLOYMENTS.keys()))
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None)
    a = p.parse_args()
    run(a.model, a.judge, a.workers, a.subfolder)
