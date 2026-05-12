"""Atomic MQM evaluation — checklist-based figure description scoring.

Uses atom checklists to guide systematic MQM evaluation. The judge receives
the image, atom checklist, reference description, and model description, then
produces standard MQM errors (category/sub_type/severity/text_span/evidence)
with atom_id linking errors to specific atoms.

Scoring follows the same MQM penalty framework:
  MQM = max(0, 100 - Σ penalties)
  Accuracy/Major=5.0, Accuracy/Minor=2.0, Completeness/Major=3.5,
  Completeness/Minor=1.5, Clarity/Major=2.0, Clarity/Minor=1.0

Additionally computes atom-level accuracy and completeness from atom_id links.

Output: output/evaluation/atomic_mqm/{judge}/{model}/{subfolder}/{fig_key}.json

Usage:
    python3 atomic_mqm/evaluator.py gpt-5.2 --judge azure/gpt-4o --workers 4
    python3 atomic_mqm/evaluator.py gpt-5.2 --judge azure/gpt-4o --subfolder english_only
    python3 atomic_mqm/evaluator.py --all --judge azure/gpt-4o --workers 4
"""

from __future__ import annotations

import argparse
import base64
import json
import logging
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "scripts"))

from evaluation.judge_backends import resolve_backend, get_openai_compat_client, get_vertex_client

ATOMS_DIR = ROOT / "atomic_mqm" / "atoms"
JUDGE_PROMPT_PATH = ROOT / "atomic_mqm" / "judge_prompt.txt"
TRANSFORMS_DIR = ROOT / "output" / "experiments" / "transforms"
GENERATION_DIR = ROOT / "output" / "generation"
FIGURES_DIR = ROOT / "Dataset" / "figures"
OUTPUT_DIR = ROOT / "output" / "evaluation" / "atomic_mqm"

SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "english_only": "English",
    "german_only": "German",
    "multi_language": "English",
}

# MQM weights — same as the main MQM evaluator
MQM_WEIGHTS = {
    ("Accuracy", "Major"): 5.0,
    ("Accuracy", "Minor"): 2.0,
    ("Completeness", "Major"): 3.5,
    ("Completeness", "Minor"): 1.5,
    ("Clarity and Readability", "Major"): 2.0,
    ("Clarity and Readability", "Minor"): 1.0,
}

VALID_CATEGORIES = {"Accuracy", "Completeness", "Clarity and Readability"}
VALID_SEVERITIES = {"Major", "Minor"}

# Accuracy sub_types — errors where the model mentioned an atom but got it wrong
ACCURACY_SUB_TYPES = {
    "Incorrect Numerical Value",
    "Incorrect Axis or Legend Interpretation",
    "Incorrect Visual Attribute Mapping",
    "Incorrect Structural Description",
}

# Completeness sub_types for missing content
MISSING_SUB_TYPES = {
    "Missing Chart Purpose",
    "Missing Axis Description",
    "Missing Visual Features",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

_judge_prompt = None


def _get_judge_prompt():
    global _judge_prompt
    if _judge_prompt is None:
        _judge_prompt = JUDGE_PROMPT_PATH.read_text()
    return _judge_prompt


def _encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from judge response: {text[:300]}...")


def _retry(func, max_retries: int = 3, backoff: float = 2.0):
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


def _build_user_text(atoms: list[dict], model_description: str,
                     reference_description: str) -> str:
    """Build the user message with atoms checklist, model description, and reference."""
    checklist_lines = []
    for atom in atoms:
        checklist_lines.append(
            f"  - ID: {atom['id']} | Severity: {atom['severity']} | "
            f"Value: {atom['value']}"
        )
    checklist = "\n".join(checklist_lines)

    return (
        f"## Atom Checklist ({len(atoms)} atoms)\n"
        f"{checklist}\n\n"
        f"## Reference Description (for clarity and readability comparison)\n"
        f"{reference_description}\n\n"
        f"## Machine-Generated Description (to evaluate)\n"
        f"{model_description}"
    )


def _call_judge_openai(client, judge_model: str, system_prompt: str,
                       user_content, max_tokens: int = 4096) -> dict:
    """Call OpenAI-compatible judge."""
    def _call():
        token_param = (
            "max_completion_tokens"
            if any(v in judge_model for v in ["gpt-5", "gpt-4.1"])
            else "max_tokens"
        )
        response = client.chat.completions.create(
            model=judge_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            **{token_param: max_tokens},
            temperature=0,
            response_format={"type": "json_object"},
        )
        return _extract_json(response.choices[0].message.content.strip())

    return _retry(_call)


def _call_judge_gemini(judge_model: str, system_prompt: str,
                       user_content_parts, backend_config: dict,
                       max_tokens: int = 8192) -> dict:
    """Call Gemini judge via Vertex AI."""
    from google.genai import types

    client = get_vertex_client(backend_config, judge_model)

    def _call():
        config_kwargs = {
            "system_instruction": system_prompt,
            "max_output_tokens": max_tokens,
            "response_mime_type": "application/json",
            "temperature": 0,
        }
        if "2.5" in judge_model or "2-5" in judge_model:
            config_kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_budget=4096,
            )
        response = client.models.generate_content(
            model=judge_model,
            contents=user_content_parts,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return _extract_json(response.text.strip())

    return _retry(_call)


def _run_judge(judge_model: str, image_path: Path, user_text: str) -> dict:
    """Dispatch judge call to correct backend."""
    system_prompt = _get_judge_prompt()
    backend_type, backend_config, model_id = resolve_backend(judge_model)

    if backend_type == "openai_compat":
        client = get_openai_compat_client(backend_config)
        b64 = _encode_image(image_path)
        user_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            },
            {"type": "text", "text": user_text},
        ]
        return _call_judge_openai(client, model_id, system_prompt,
                                  user_content, max_tokens=4096)

    elif backend_type == "vertex_ai":
        from google.genai import types
        parts = [
            types.Part.from_bytes(
                data=image_path.read_bytes(), mime_type="image/png",
            ),
            user_text,
        ]
        return _call_judge_gemini(model_id, system_prompt, parts,
                                 backend_config, max_tokens=8192)
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


def validate_errors(errors: list[dict]) -> list[dict]:
    """Normalize and validate error entries from the judge."""
    validated = []
    for err in errors:
        cat = err.get("category", "")
        sub = err.get("sub_type", "")
        sev = err.get("severity", "")

        # Normalize category
        if cat not in VALID_CATEGORIES:
            for valid_cat in VALID_CATEGORIES:
                if valid_cat.lower() in cat.lower():
                    cat = valid_cat
                    break

        # Normalize severity
        if sev not in VALID_SEVERITIES:
            sev = "Minor"

        # Handle text_span
        text_span = err.get("text_span")
        if text_span is not None:
            text_span = str(text_span).strip() if text_span else None
        if sub in MISSING_SUB_TYPES:
            text_span = None

        validated.append({
            "category": cat,
            "sub_type": sub,
            "severity": sev,
            "weight": MQM_WEIGHTS.get((cat, sev), 0.0),
            "text_span": text_span,
            "evidence": err.get("evidence", ""),
            "atom_id": err.get("atom_id"),
        })
    return validated


def compute_mqm_score(errors: list[dict], num_atoms: int) -> tuple[float, float]:
    """Compute normalized MQM score from errors.

    Formula: MQM = max(0, 100 - (Σ penalties / max_possible_penalty) × 100)
    Where max_possible_penalty = num_atoms × 5.0 (worst case: every atom Accuracy/Major).

    Hallucination and clarity penalties can push the sum above max_possible_penalty,
    but the score is clamped at 0.

    Returns (mqm_score, total_penalty).
    """
    total_penalty = sum(e.get("weight", 0.0) for e in errors)
    max_possible = num_atoms * 5.0  # worst case: every atom Accuracy/Major
    if max_possible == 0:
        return 100.0, 0.0
    normalized = (total_penalty / max_possible) * 100.0
    return max(0.0, 100.0 - normalized), total_penalty


def compute_atom_coverage(errors: list[dict], atoms: list[dict]) -> dict:
    """Compute atom-level accuracy and completeness from error atom_ids.

    Atoms that have NO error linked to them are considered Correct.
    Atoms linked to an Accuracy error are Inaccurate.
    Atoms linked to a Missing* Completeness error are Missing.
    """
    atom_ids = {a["id"] for a in atoms}

    # Collect atoms with errors
    inaccurate_atoms = set()
    missing_atoms = set()
    for err in errors:
        aid = err.get("atom_id")
        if not aid or aid not in atom_ids:
            continue
        if err["category"] == "Accuracy":
            inaccurate_atoms.add(aid)
        elif err["sub_type"] in MISSING_SUB_TYPES:
            missing_atoms.add(aid)

    # Atoms with no errors are correct
    correct_atoms = atom_ids - inaccurate_atoms - missing_atoms

    c = len(correct_atoms)
    i = len(inaccurate_atoms)
    m = len(missing_atoms)

    accuracy = c / (c + i) if (c + i) > 0 else 1.0
    completeness = c / (c + m) if (c + m) > 0 else 1.0

    return {
        "correct": c,
        "inaccurate": i,
        "missing": m,
        "total": len(atom_ids),
        "accuracy": round(accuracy, 4),
        "completeness": round(completeness, 4),
    }


def _get_model_description(fig_key: str, subfolder: str,
                           model_name: str, language: str,
                           transform: str = "original") -> str | None:
    """Load model description for a figure.

    Looks in transforms/{transform}/ first, then falls back to
    generation/ for original descriptions.
    """
    gen_path = TRANSFORMS_DIR / model_name / transform / subfolder / f"{fig_key}.json"
    if not gen_path.exists() and transform == "original":
        gen_path = GENERATION_DIR / model_name / subfolder / f"{fig_key}.json"
    if not gen_path.exists():
        return None

    with open(gen_path) as f:
        gen = json.load(f)

    if "model_annotations" in gen:
        return gen["model_annotations"].get(language, "")
    return gen.get("model_annotation", "")


def _process(fig_key: str, subfolder: str, model_name: str,
             judge_model: str, atom_data: dict,
             transform: str = "original") -> tuple:
    """Process a single figure evaluation."""
    fig_path = FIGURES_DIR / subfolder / f"{fig_key}.png"
    transform_suffix = "" if transform == "original" else f"/{transform}"
    out_path = (OUTPUT_DIR / judge_model / model_name / (transform + "/" + subfolder)
                / f"{fig_key}.json")

    if out_path.exists():
        return True, fig_key, "skip"

    if not fig_path.exists():
        logger.warning(f"Image not found: {fig_path}")
        return True, fig_key, "skip"

    language = atom_data.get("language", SUBFOLDER_TO_LANGUAGE.get(subfolder, "English"))
    model_desc = _get_model_description(fig_key, subfolder, model_name,
                                        language, transform)
    if not model_desc:
        return True, fig_key, "skip"

    atoms = atom_data["atoms"]
    reference = atom_data.get("reference_description", "")

    user_text = _build_user_text(atoms, model_desc, reference)

    try:
        result = _run_judge(judge_model, fig_path, user_text)
    except Exception as e:
        logger.error(f"  FAIL {fig_key}: {e}")
        return False, fig_key, str(e)

    # Validate and score
    errors = validate_errors(result.get("errors", []))
    mqm_score, total_penalty = compute_mqm_score(errors, len(atoms))
    atom_coverage = compute_atom_coverage(errors, atoms)

    eval_result = {
        "figure_key": fig_key,
        "subfolder": subfolder,
        "model_name": model_name,
        "judge_model": judge_model,
        "judge_type": "atomic_mqm",
        "transform": transform,
        "figure_type": atom_data.get("figure_type", ""),
        "language": language,
        "num_atoms": len(atoms),
        "errors": errors,
        "error_count": len(errors),
        "mqm_score": round(mqm_score, 2),
        "total_penalty": round(total_penalty, 2),
        "atom_coverage": atom_coverage,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(eval_result, f, indent=2, ensure_ascii=False)

    ac = atom_coverage
    logger.info(
        f"  OK   {subfolder}/{fig_key}: MQM={mqm_score:.1f} "
        f"({len(errors)} errors, penalty={total_penalty:.1f}) "
        f"atoms: C={ac['correct']} I={ac['inaccurate']} M={ac['missing']} "
        f"acc={ac['accuracy']:.2f} comp={ac['completeness']:.2f}"
    )
    return True, fig_key, "done"


def _load_all_atoms() -> dict:
    """Load all atom files into a dict keyed by (fig_key, subfolder)."""
    atoms = {}
    for f in sorted(ATOMS_DIR.iterdir()):
        if not f.suffix == ".json":
            continue
        with open(f) as fh:
            data = json.load(fh)
        key = (data["figure_key"], data["subfolder"])
        atoms[key] = data
    return atoms


def run(model_name: str, judge_model: str = "azure/gpt-4o",
        workers: int = 4, subfolder_filter: str = None,
        transform: str = "original"):
    """Run atomic MQM evaluation for a model."""
    all_atoms = _load_all_atoms()

    work_items = []
    skipped = 0
    for (fig_key, subfolder), atom_data in all_atoms.items():
        if subfolder_filter and subfolder != subfolder_filter:
            continue
        out_path = (OUTPUT_DIR / judge_model / model_name
                    / transform / subfolder / f"{fig_key}.json")
        if out_path.exists():
            skipped += 1
            continue
        language = atom_data.get("language",
                                SUBFOLDER_TO_LANGUAGE.get(subfolder, "English"))
        if _get_model_description(fig_key, subfolder, model_name,
                                  language, transform) is None:
            continue
        work_items.append((fig_key, subfolder, atom_data))

    logger.info(
        f"Atomic MQM evaluation | model={model_name} | judge={judge_model} "
        f"| transform={transform} | workers={workers}"
    )
    logger.info(
        f"Total: {len(work_items) + skipped} figures "
        f"({skipped} done, {len(work_items)} to evaluate)"
    )
    if not work_items:
        logger.info("Nothing to do.")
        _print_summary(model_name, judge_model, subfolder_filter, transform)
        return

    success = skipped
    errors = 0
    lock = threading.Lock()

    def _on_done(ok, k, s):
        nonlocal success, errors
        with lock:
            if ok:
                success += 1
            else:
                errors += 1
            d = success + errors - skipped
            if d % 5 == 0 or not ok:
                logger.info(
                    f"  Progress: {d}/{len(work_items)} (errors={errors})"
                )

    if workers == 1:
        for fk, sub, ad in work_items:
            ok, k, s = _process(fk, sub, model_name, judge_model, ad, transform)
            _on_done(ok, k, s)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {
                ex.submit(_process, fk, sub, model_name, judge_model,
                          ad, transform): fk
                for fk, sub, ad in work_items
            }
            for f in as_completed(futs):
                try:
                    ok, k, s = f.result()
                    _on_done(ok, k, s)
                except Exception as e:
                    logger.error(f"  UNEXPECTED {futs[f]}: {e}")
                    with lock:
                        errors += 1

    _print_summary(model_name, judge_model, subfolder_filter, transform)
    logger.info(
        f"Done. {success}/{len(work_items) + skipped} evaluated, "
        f"{errors} failures."
    )


def _print_summary(model_name: str, judge_model: str,
                   subfolder_filter: str = None,
                   transform: str = "original"):
    """Print aggregate scores from completed evaluations."""
    eval_dir = OUTPUT_DIR / judge_model / model_name / transform
    if not eval_dir.exists():
        return

    all_results = []
    by_subfolder = {}

    for ef in eval_dir.rglob("*.json"):
        data = json.load(open(ef))
        sub = data.get("subfolder", "unknown")
        if subfolder_filter and sub != subfolder_filter:
            continue
        all_results.append(data)
        by_subfolder.setdefault(sub, []).append(data)

    if not all_results:
        return

    t_label = f" [{transform}]" if transform != "original" else ""
    print(f"\n=== ATOMIC MQM SUMMARY ({model_name}{t_label} judged by {judge_model}) ===")
    print(f"{'Subfolder':<20} {'N':>4} {'MQM':>7} {'Errs':>5} "
          f"{'AtomAcc':>8} {'AtomComp':>9}")
    print("-" * 60)

    for sub in sorted(by_subfolder):
        results = by_subfolder[sub]
        n = len(results)
        avg_mqm = sum(r["mqm_score"] for r in results) / n
        avg_errs = sum(r["error_count"] for r in results) / n
        avg_acc = sum(r["atom_coverage"]["accuracy"] for r in results) / n
        avg_comp = sum(r["atom_coverage"]["completeness"] for r in results) / n
        print(f"{sub:<20} {n:>4} {avg_mqm:>7.2f} {avg_errs:>5.1f} "
              f"{avg_acc:>8.2%} {avg_comp:>9.2%}")

    n = len(all_results)
    avg_mqm = sum(r["mqm_score"] for r in all_results) / n
    avg_errs = sum(r["error_count"] for r in all_results) / n
    avg_acc = sum(r["atom_coverage"]["accuracy"] for r in all_results) / n
    avg_comp = sum(r["atom_coverage"]["completeness"] for r in all_results) / n
    print("-" * 60)
    print(f"{'OVERALL':<20} {n:>4} {avg_mqm:>7.2f} {avg_errs:>5.1f} "
          f"{avg_acc:>8.2%} {avg_comp:>9.2%}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Atomic MQM evaluation for figure descriptions"
    )
    p.add_argument("model", help="Model name to evaluate")
    p.add_argument("--judge", default="azure/gpt-4o",
                   help="Judge model (e.g. azure/gpt-4o, mistral-large-3)")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--subfolder", default=None,
                   help="Filter to specific subfolder")
    p.add_argument("--transform", default="original",
                   help="Transform to evaluate (e.g. original, blurred_in_paper)")
    p.add_argument("--all", action="store_true",
                   help="Evaluate all models that have descriptions")
    a = p.parse_args()

    if a.all:
        models = sorted([
            d.name for d in TRANSFORMS_DIR.iterdir()
            if d.is_dir() and (d / a.transform).exists()
        ])
        logger.info(f"Evaluating all models: {models}")
        for model in models:
            run(model, a.judge, a.workers, a.subfolder, a.transform)
    else:
        run(a.model, a.judge, a.workers, a.subfolder, a.transform)
