import json
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple


"""
Process a Label Studio *project JSON export* into a structured, task-centric JSON.

How to use:
  - Edit the CONFIG section below (paths + mode).
  - Run: python scripts/structuring_label_studio_export/process_label_studio_export.py
"""

# =========================
# CONFIG (edit these)
# =========================

# Paths are resolved relative to this script's directory, so running the script from
# any working directory will still work.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(SCRIPT_DIR)

# Path to the Label Studio project export JSON (as downloaded from Label Studio).
INPUT_JSON_PATH = os.path.join(
    SCRIPT_DIR,
    "label_studio_export",
    "project-15-at-2026-04-27-01-32-eea32bfb.json",
)

# Output JSON path. If None, derived from INPUT_JSON_PATH.
# Default: write into scripts/structuring_label_studio_export/structured_output/
OUTPUT_JSON_PATH: Optional[str] = os.path.join(
    SCRIPT_DIR,
    "structured_output",
    "annotations_structured.json",
)

# Path to the alias pools used when masking model names on upload.
ALIAS_POOLS_PATH = os.path.join(SCRIPT_DIR, "model_alias_pools.json")

# Label Studio uses label aliases when present. These are the category aliases you configured.
KNOWN_CATEGORY_ALIASES = {"cat_accuracy", "cat_completeness", "cat_clarity"}

# Map category alias -> the per-region Choices control name that stores the subtype.
SUBTYPE_GROUP_FROM_CATEGORY_ALIAS = {
    "cat_accuracy": "accuracy_subtypes",
    "cat_completeness": "completeness_subtypes",
    "cat_clarity": "clarity_subtypes",
}


def _load_alias_to_true_model(alias_pools_path: str) -> Dict[str, str]:
    """
    Invert scripts/model_alias_pools.json into alias -> true model name.

    Input example:
      { "gpt-5.2": ["Cumulus-02", ...], ... }
    Output example:
      { "Cumulus-02": "gpt-5.2", ... }
    """
    with open(alias_pools_path, "r", encoding="utf-8") as f:
        pools = json.load(f)

    if not isinstance(pools, dict):
        raise ValueError(f"Alias pools must be a JSON object, got {type(pools).__name__}")

    alias_to_true: Dict[str, str] = {}
    for true_model_name, aliases in pools.items():
        if not isinstance(true_model_name, str):
            raise ValueError(f"Alias pools keys must be strings; got {type(true_model_name).__name__}")
        if not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases):
            raise ValueError(f"Pool for {true_model_name!r} must be a list of strings")
        for a in aliases:
            if a in alias_to_true and alias_to_true[a] != true_model_name:
                raise ValueError(
                    f"Alias {a!r} is duplicated across models: {alias_to_true[a]!r} and {true_model_name!r}"
                )
            alias_to_true[a] = true_model_name

    return alias_to_true


def _group_results_by_region_id(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in results:
        region_id = r.get("id")
        if region_id is None:
            continue
        grouped[str(region_id)].append(r)
    return grouped


def _extract_span_fields(items: List[Dict[str, Any]]) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    """
    Returns (start, end, text). Prefer any item that has them.
    """
    start = end = None
    text = None

    for r in items:
        v = r.get("value") or {}
        if start is None and isinstance(v.get("start"), int):
            start = v["start"]
        if end is None and isinstance(v.get("end"), int):
            end = v["end"]
        if text is None and isinstance(v.get("text"), str):
            text = v["text"]

    return start, end, text


def _extract_category(items: List[Dict[str, Any]]) -> Optional[str]:
    """
    Returns the category alias from the Labels result (error_category).
    """
    for r in items:
        if r.get("from_name") == "error_category" and r.get("type") == "labels":
            labels = (r.get("value") or {}).get("labels") or []
            if labels:
                return str(labels[0])
    return None


def _extract_choices(items: List[Dict[str, Any]], from_name: str) -> List[str]:
    out: List[str] = []
    for r in items:
        if r.get("from_name") == from_name and r.get("type") == "choices":
            choices = (r.get("value") or {}).get("choices") or []
            out.extend([str(c) for c in choices])
    return out


def _log_skip_draft(task_id: Any, draft: Dict[str, Any]) -> None:
    draft_id = draft.get("id")
    user = draft.get("user")
    created_username = draft.get("created_username")
    created_at = draft.get("created_at") or draft.get("draft_created_at") or draft.get("createdDate")
    result_count = len(draft.get("result") or [])
    print(
        f"[skip draft] task_id={task_id} draft_id={draft_id} user={user!r} created_username={created_username!r} "
        f"created_at={created_at!r} result_items={result_count}"
    )


def _build_span(region_id: str, items: List[Dict[str, Any]], task_id: Any, annotation_id: Any) -> Optional[Dict[str, Any]]:
    start, end, text = _extract_span_fields(items)
    category = _extract_category(items)

    if category not in KNOWN_CATEGORY_ALIASES:
        print(
            f"[skip span incomplete/unknown category] task_id={task_id} annotation_id={annotation_id} "
            f"region_id={region_id} category={category!r} start={start} end={end} text={text!r}"
        )
        return None

    subtype_group = SUBTYPE_GROUP_FROM_CATEGORY_ALIAS.get(category)
    subtype_choices = _extract_choices(items, subtype_group) if subtype_group else []
    if len(subtype_choices) > 1:
        raise RuntimeError(
            "Multiple subtypes selected for a single span. "
            f"task_id={task_id} annotation_id={annotation_id} region_id={region_id} "
            f"category={category!r} subtype_group={subtype_group!r} subtype_choices={subtype_choices!r}"
        )
    if len(subtype_choices) == 0:
        print(
            f"[skip span missing subtype] task_id={task_id} annotation_id={annotation_id} region_id={region_id} "
            f"category={category!r} subtype_group={subtype_group!r} start={start} end={end} text={text!r}"
        )
        return None

    severity_choices = _extract_choices(items, "severity")
    if len(severity_choices) != 1:
        print(
            f"[skip span missing/ambiguous severity] task_id={task_id} annotation_id={annotation_id} region_id={region_id} "
            f"severity_choices={severity_choices!r} start={start} end={end} text={text!r}"
        )
        return None

    if start is None or end is None or text is None:
        print(
            f"[skip span missing offsets/text] task_id={task_id} annotation_id={annotation_id} region_id={region_id} "
            f"start={start} end={end} text={text!r}"
        )
        return None

    return {
        "region_id": region_id,
        "start": start,
        "end": end,
        "text": text,
        "category": category,
        "subtype": subtype_choices[0],
        "severity": severity_choices[0],
    }


def transform_export_to_task_records(export: List[Dict[str, Any]], alias_to_true_model: Dict[str, str]) -> List[Dict[str, Any]]:
    out_tasks: List[Dict[str, Any]] = []

    for task in export:
        task_id = task.get("id")
        task_data = dict(task.get("data") or {})

        # Unmask model_name (keep masked value for traceability).
        masked_model_name = task_data.get("model_name")
        if isinstance(masked_model_name, str):
            true_model_name = alias_to_true_model.get(masked_model_name)
            if true_model_name is not None:
                task_data["model_name_masked"] = masked_model_name
                task_data["model_name"] = true_model_name
            else:
                print(
                    f"[warn] model_name alias not found in pools: task_id={task_id} model_name={masked_model_name!r}"
                )

        # Log and skip drafts (requirement).
        for draft in task.get("drafts") or []:
            _log_skip_draft(task_id, draft)

        annotations_out: List[Dict[str, Any]] = []
        for ann in task.get("annotations") or []:
            annotation_id = ann.get("id")
            annotator_id = ann.get("completed_by")
            results = ann.get("result") or []

            if not results:
                # Meaning: annotator found no errors
                annotations_out.append({"annotator_id": annotator_id, "spans": []})
                continue

            spans_out: List[Dict[str, Any]] = []
            grouped = _group_results_by_region_id(results)
            for region_id, items in grouped.items():
                span = _build_span(region_id, items, task_id=task_id, annotation_id=annotation_id)
                if span is not None:
                    spans_out.append(span)

            annotations_out.append({"annotator_id": annotator_id, "spans": spans_out})

        out_tasks.append(
            {
                "task_id": task_id,
                "data": task_data,
                "annotations": annotations_out,
            }
        )

    return out_tasks


def _default_output_path(input_path: str) -> str:
    base, _ext = os.path.splitext(input_path)
    return f"{base}.tasks.json"


def main() -> None:
    if not os.path.exists(INPUT_JSON_PATH):
        raise FileNotFoundError(f"INPUT_JSON_PATH does not exist: {INPUT_JSON_PATH}")

    if not os.path.exists(ALIAS_POOLS_PATH):
        raise FileNotFoundError(f"ALIAS_POOLS_PATH does not exist: {ALIAS_POOLS_PATH}")

    out_json = OUTPUT_JSON_PATH or _default_output_path(INPUT_JSON_PATH)
    out_dir = os.path.dirname(out_json)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    alias_to_true_model = _load_alias_to_true_model(ALIAS_POOLS_PATH)

    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        export = json.load(f)

    if not isinstance(export, list):
        raise ValueError("Expected top-level JSON array (list of tasks).")

    tasks = transform_export_to_task_records(export, alias_to_true_model=alias_to_true_model)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(tasks)} task records.")
    print(f"- JSON: {out_json}")


if __name__ == "__main__":
    main()