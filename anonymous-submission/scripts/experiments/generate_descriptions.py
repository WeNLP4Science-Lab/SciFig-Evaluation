"""Generate figure descriptions using VLMs.

For models without thesis outputs (e.g., Phi-5) or for regeneration.
Uses the same prompts as the thesis for consistency.

Usage:
    python generate_descriptions.py phi-5
    python generate_descriptions.py phi-5 --workers 4
    python generate_descriptions.py phi-5 --figures fig_001 fig_005
    python generate_descriptions.py gpt-5.2 --figures fig_001  # regenerate one
"""

from __future__ import annotations

import json
import base64
import time
import logging
import argparse
import threading
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    MODELS, FIGURES_DIR, GROUNDTRUTH_DIR, DESCRIPTIONS_DIR,
    PROMPTS_DIR, TEMPERATURE, MAX_TOKENS, AZURE_API_VERSION,
    OPENROUTER_BASE_URL,
    get_azure_endpoint, get_azure_api_key, get_openrouter_api_key,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Prompts ──

PROMPTS = {}

def load_prompts():
    global PROMPTS
    for pfile in PROMPTS_DIR.glob("*.txt"):
        PROMPTS[pfile.stem] = pfile.read_text().strip()
    return PROMPTS


def get_prompt(figure_type: str) -> str:
    type_map = {
        "Bar Chart": "bar_chart",
        "Line Plot": "line_plot",
        "Pie Chart": "pie_chart",
    }
    key = type_map.get(figure_type, "default")
    return PROMPTS.get(key, PROMPTS.get("default", "Describe this scientific figure."))


# ── API clients ──

def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_model(model_name: str, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
    cfg = MODELS[model_name]
    b64 = encode_image(image_path)

    user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"
    user_content = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
        {"type": "text", "text": user_text},
    ]
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content},
    ]

    max_tok = cfg.get("max_tokens", MAX_TOKENS)

    if cfg["backend"] == "azure":
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=get_azure_endpoint(),
            api_key=get_azure_api_key(),
            api_version=AZURE_API_VERSION,
        )
        token_param = "max_completion_tokens" if any(v in cfg["model_id"] for v in ["gpt-5", "gpt-4.1"]) else "max_tokens"
        response = client.chat.completions.create(
            model=cfg["model_id"],
            messages=messages,
            temperature=TEMPERATURE,
            **{token_param: max_tok},
        )
    else:
        from openai import OpenAI
        client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=get_openrouter_api_key())
        response = client.chat.completions.create(
            model=cfg["model_id"],
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=max_tok,
        )

    return response.choices[0].message.content.strip()


def retry_call(func, max_retries=3, backoff=2.0):
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


def process_figure(model_name: str, fig_id: str, out_dir: Path) -> tuple[bool, str]:
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not gt_path.exists() or not fig_path.exists():
        return False, "missing"

    with open(gt_path) as f:
        gt = json.load(f)

    prompt = get_prompt(gt["figure_type"])

    try:
        description = retry_call(
            lambda: call_model(
                model_name, prompt, fig_path,
                gt.get("caption", ""), gt.get("paper_title", ""),
            )
        )
    except Exception as e:
        logger.error(f"  FAIL {fig_id}: {e}")
        return False, str(e)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "description": description,
        "figure_type": gt["figure_type"],
    }

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id} ({len(description)} chars)")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name from config")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+", help="Specific figures to generate")
    args = parser.parse_args()

    if args.model not in MODELS:
        available = ", ".join(sorted(MODELS.keys()))
        print(f"Unknown model: {args.model}. Available: {available}")
        return

    load_prompts()
    logger.info(f"Loaded {len(PROMPTS)} prompts")

    out_dir = DESCRIPTIONS_DIR / args.model
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.figures:
        fig_ids = args.figures
    else:
        fig_ids = sorted(p.stem for p in FIGURES_DIR.glob("*.png"))

    # Filter already done
    todo = [f for f in fig_ids if not (out_dir / f"{f}.json").exists()]
    skipped = len(fig_ids) - len(todo)

    logger.info(f"Model: {args.model}")
    logger.info(f"Total: {len(fig_ids)} ({skipped} done, {len(todo)} to process)")
    print()

    if not todo:
        logger.info("Nothing to do.")
        return

    success, errors = skipped, 0
    lock = threading.Lock()

    def on_complete(ok, status):
        nonlocal success, errors
        with lock:
            if ok and status != "skip":
                success += 1
            elif not ok:
                errors += 1
            done = success + errors - skipped
            if done % 10 == 0 or not ok:
                logger.info(f"  Progress: {done}/{len(todo)} (success={success}, errors={errors})")

    if args.workers == 1:
        for fig_id in todo:
            ok, status = process_figure(args.model, fig_id, out_dir)
            on_complete(ok, status)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(process_figure, args.model, fig_id, out_dir): fig_id
                for fig_id in todo
            }
            for future in as_completed(futures):
                try:
                    ok, status = future.result()
                    on_complete(ok, status)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futures[future]}: {e}")
                    with lock:
                        errors += 1

    print()
    logger.info(f"Done. {success}/{len(fig_ids)} succeeded, {errors} errors.")
    logger.info(f"Output: {out_dir}")


if __name__ == "__main__":
    main()
