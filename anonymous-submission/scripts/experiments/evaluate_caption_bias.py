"""Evaluate caption bias descriptions using an LLM judge.

For each modification (false claim vs reality), the judge determines whether
the model's description aligns with the caption's false claim, the image
reality, or doesn't address the topic. A/B ordering is randomized per
modification to prevent position bias.

Metrics:
  resistance   = followed_image / (followed_image + followed_caption)
  completeness = (followed_image + followed_caption) / num_modifications

Input:  results/generation/caption_bias/{model}/{fig_id}.json
        dataset/caption_bias/{fig_id}.json (modifications)
Output: results/evaluation/caption_bias/{model}/{fig_id}.json

Usage:
    python evaluate_caption_bias.py gpt-5.2 --workers 4
    python evaluate_caption_bias.py gemma3-27b-it --workers 8
"""

from __future__ import annotations

import json
import argparse
import logging
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import MODELS, RESULTS_DIR, DATASET_DIR, AZURE_API_VERSION, get_azure_endpoint, get_azure_api_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

CAPTION_BIAS_DIR = DATASET_DIR / "caption_bias"
GEN_DIR = RESULTS_DIR / "generation" / "caption_bias"
EVAL_DIR = RESULTS_DIR / "evaluation" / "caption_bias"

JUDGE_MODEL = "gpt-4o"


def _get_judge_client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        azure_endpoint=get_azure_endpoint(),
        api_key=get_azure_api_key(),
        api_version=AZURE_API_VERSION,
    )


def _build_judge_prompt(description, modifications):
    """Build judge prompt with randomized A/B ordering per modification."""
    items = []
    ordering = []

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


def evaluate_figure(client, model_name, fig_id):
    out_path = EVAL_DIR / model_name / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    gen_path = GEN_DIR / model_name / f"{fig_id}.json"
    bias_path = CAPTION_BIAS_DIR / f"{fig_id}.json"

    if not gen_path.exists():
        return False, "missing_description"
    if not bias_path.exists():
        return False, "missing_bias_probe"

    with open(gen_path) as f:
        gen = json.load(f)
    with open(bias_path) as f:
        bias = json.load(f)

    description = gen.get("description", "")
    modifications = bias.get("modifications", [])

    if not description.strip():
        return False, "empty_description"
    if not modifications:
        return False, "no_modifications"

    # Set seed per figure for reproducible A/B ordering
    random.seed(f"caption_bias_{fig_id}")
    prompt, ordering = _build_judge_prompt(description, modifications)

    try:
        response = client.chat.completions.create(
            model=JUDGE_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    # Map A/B back to caption/image
    evaluations = []
    followed_image = 0
    followed_caption = 0
    not_addressed = 0

    for i, mod in enumerate(modifications):
        key = str(i + 1)
        if key in result:
            answer = result[key].get("answer", "").strip().upper()[:1]
            reason = result[key].get("reason", "")

            order = ordering[i]
            if answer == "C":
                mapped = "not_addressed"
                not_addressed += 1
            elif answer == "A":
                mapped = order["a_is"]
                if mapped == "image": followed_image += 1
                else: followed_caption += 1
            elif answer == "B":
                mapped = order["b_is"]
                if mapped == "image": followed_image += 1
                else: followed_caption += 1
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
            "type": mod.get("type", ""),
            "principle": mod.get("principle", ""),
            "judge_answer": answer,
            "mapped_to": mapped,
            "reason": reason,
        })

    addressed = followed_image + followed_caption
    resistance = followed_image / addressed if addressed > 0 else None
    completeness = addressed / len(modifications) if modifications else 0

    output = {
        "figure_id": fig_id,
        "model_name": model_name,
        "judge_model": JUDGE_MODEL,
        "figure_type": gen.get("figure_type", ""),
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
    logger.info(f"  OK {fig_id} — img={followed_image} cap={followed_caption} skip={not_addressed} R={r_str}")
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

    # Default to figures that have both generation and bias probes
    if args.figures:
        fig_ids = args.figures
    else:
        gen_dir = GEN_DIR / args.model
        if not gen_dir.exists():
            print(f"No caption bias descriptions for {args.model}. Run run_caption_bias.py first.")
            return
        fig_ids = sorted(p.stem for p in gen_dir.glob("*.json"))

    work, skipped = [], 0
    for fid in fig_ids:
        if (EVAL_DIR / args.model / f"{fid}.json").exists():
            skipped += 1
        else:
            work.append(fid)

    logger.info(f"Caption bias eval | model={args.model} | judge={JUDGE_MODEL}")
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
    total_img = total_cap = total_skip = total_mods = 0
    for ef in eval_dir.glob("*.json"):
        data = json.load(open(ef))
        total_img += data.get("followed_image", 0)
        total_cap += data.get("followed_caption", 0)
        total_skip += data.get("not_addressed", 0)
        total_mods += data.get("num_modifications", 0)

    addressed = total_img + total_cap
    resistance = total_img / addressed if addressed > 0 else 0
    completeness = addressed / total_mods if total_mods > 0 else 0

    print(f"\n=== SUMMARY ({args.model} judged by {JUDGE_MODEL}) ===")
    print(f"  Total modifications: {total_mods}")
    print(f"  Followed image: {total_img}")
    print(f"  Followed caption: {total_cap}")
    print(f"  Not addressed: {total_skip}")
    print(f"  Resistance: {resistance:.2f}")
    print(f"  Completeness: {completeness:.2f}")

    logger.info(f"Done. {success} ok, {errors} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
