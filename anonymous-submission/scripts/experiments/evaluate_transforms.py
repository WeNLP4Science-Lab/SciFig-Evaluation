"""MQM evaluation of transform descriptions.

Same judge as evaluate_mqm.py but reads from transforms directory
and writes output grouped by transform/model.

Input:  results/generation/description_tasks/transforms/{model}/{transform}/{fig_id}.json
Output: results/evaluation/description_tasks/transforms/{transform}/{model}/{fig_id}.json

Usage:
    python evaluate_transforms.py gpt-5.2 --transform low_contrast --workers 4
    python evaluate_transforms.py gemma3-27b-it --transform all --workers 4
    python evaluate_transforms.py --all-models --transform noise
"""

from __future__ import annotations

import json
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    MODELS, FIGURES_DIR, GROUNDTRUTH_DIR, RESULTS_DIR, DATASET_DIR,
    AZURE_API_VERSION,
    get_azure_endpoint, get_azure_api_key,
)
from models import encode_image
from checklists import (
    get_checklist, get_global_constraints, get_bindings,
    compute_penalties, deduplicate_penalties, compute_mqm,
)

# Import the prompts from evaluate_mqm
from evaluate_mqm import SYSTEM_PROMPT, USER_PROMPT, _format_checklist, _format_constraints, _format_bindings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

GEN_TRANSFORMS_DIR = RESULTS_DIR / "generation" / "description_tasks" / "transforms"
EVAL_TRANSFORMS_DIR = RESULTS_DIR / "evaluation" / "description_tasks" / "transforms"

JUDGE_MODEL = "gpt-4o"

ALL_TRANSFORMS = ["original", "noise", "low_contrast", "rotation"]


def evaluate_figure(model_name: str, transform: str, fig_id: str) -> tuple[bool, str]:
    out_dir = EVAL_TRANSFORMS_DIR / transform / model_name
    out_path = out_dir / f"{fig_id}.json"
    if out_path.exists():
        return True, "skip"

    desc_path = GEN_TRANSFORMS_DIR / model_name / transform / f"{fig_id}.json"
    gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not desc_path.exists() or not gt_path.exists() or not fig_path.exists():
        return False, "missing"

    with open(desc_path) as f:
        desc_data = json.load(f)
    with open(gt_path) as f:
        gt_data = json.load(f)

    description = desc_data.get("description", "")
    figure_type = gt_data.get("figure_type", "Bar Chart")

    # Get ground-truth human annotation
    anns = gt_data.get("annotations", [])
    eng = [a["annotation"] for a in anns if a.get("annotation_language") == "English"]
    if not eng:
        eng = [a["annotation"] for a in anns if "annotation" in a]
    groundtruth = max(eng, key=len) if eng else ""

    if not description or not groundtruth:
        return False, "empty"

    checklist = get_checklist(figure_type)
    constraints = get_global_constraints()
    bindings = get_bindings(figure_type)

    user_prompt = USER_PROMPT.format(
        figure_type=figure_type,
        checklist_text=_format_checklist(checklist),
        constraints_text=_format_constraints(constraints),
        binding_instructions=_format_bindings(bindings),
        groundtruth=groundtruth,
        description=description,
    )

    from openai import AzureOpenAI
    client = AzureOpenAI(
        azure_endpoint=get_azure_endpoint(),
        api_key=get_azure_api_key(),
        api_version=AZURE_API_VERSION,
    )

    b64 = encode_image(fig_path)
    try:
        response = client.chat.completions.create(
            model=JUDGE_MODEL,
            temperature=0,
            max_tokens=4000,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
                    {"type": "text", "text": user_prompt},
                ]},
            ],
        )
        judge_output = json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"  FAIL {fig_id}/{transform}: {e}")
        return False, str(e)

    penalties = compute_penalties(judge_output, checklist)
    mqm_raw = compute_mqm(penalties, checklist)

    deduped = deduplicate_penalties(penalties)
    mqm_deduped = compute_mqm(deduped, checklist)

    result = {
        "figure_id": fig_id,
        "model_name": model_name,
        "transform": transform,
        "figure_type": figure_type,
        "judge_model": JUDGE_MODEL,
        "num_items": len(checklist),
        "num_penalties_raw": len(penalties),
        "num_penalties_deduped": len(deduped),
        "total_penalty_raw": sum(p["weight"] for p in penalties),
        "total_penalty_deduped": sum(p["weight"] for p in deduped),
        "mqm_raw": round(mqm_raw, 2),
        "mqm_deduped": round(mqm_deduped, 2),
        "penalties_raw": penalties,
        "penalties_deduped": deduped,
        "judge_output": judge_output,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"  OK {fig_id}/{transform}: MQM={mqm_deduped:.1f}")
    return True, "done"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", nargs="?", help="Model name")
    parser.add_argument("--all-models", action="store_true")
    parser.add_argument("--transform", default="all", help="Transform name or 'all'")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--figures", nargs="+")
    args = parser.parse_args()

    if args.all_models:
        model_names = sorted(MODELS.keys())
    elif args.model:
        model_names = [args.model]
    else:
        print("Specify a model name or --all-models")
        return

    transforms = ALL_TRANSFORMS if args.transform == "all" else [args.transform]

    for model_name in model_names:
        for transform in transforms:
            gen_dir = GEN_TRANSFORMS_DIR / model_name / transform
            if not gen_dir.exists():
                logger.info(f"{model_name}/{transform}: no descriptions, skipping")
                continue

            fig_ids = args.figures or sorted(p.stem for p in gen_dir.glob("*.json"))

            eval_dir = EVAL_TRANSFORMS_DIR / transform / model_name
            work, skipped = [], 0
            for fid in fig_ids:
                if (eval_dir / f"{fid}.json").exists():
                    skipped += 1
                else:
                    work.append(fid)

            logger.info(f"MQM eval [{transform}] | model={model_name}")
            logger.info(f"Total: {len(work) + skipped} ({skipped} done, {len(work)} to evaluate)")

            if not work:
                logger.info("Nothing to do.")
                continue

            success, errors = 0, 0
            lock = threading.Lock()

            if args.workers == 1:
                for fid in work:
                    ok, s = evaluate_figure(model_name, transform, fid)
                    if ok: success += 1
                    else: errors += 1
            else:
                with ThreadPoolExecutor(max_workers=args.workers) as ex:
                    futs = {ex.submit(evaluate_figure, model_name, transform, fid): fid for fid in work}
                    for f in as_completed(futs):
                        ok, s = f.result()
                        with lock:
                            if ok: success += 1
                            else: errors += 1

            logger.info(f"  {model_name}/{transform}: {success} ok, {errors} errors, {skipped} skipped.")

    logger.info("All done.")


if __name__ == "__main__":
    main()
