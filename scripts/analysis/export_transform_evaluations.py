"""Export per-figure transform MQM evaluations for dashboard viewing.

Output: dashboard/public/data/transform_evaluations.json

Usage:
    python3 scripts/analysis/export_transform_evaluations.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DASHBOARD_DATA = ROOT / "dashboard" / "public" / "data"
TRANSFORMS_DIR = ROOT / "output" / "experiments" / "transforms"
EVAL_DIR = ROOT / "output" / "evaluation" / "transforms" / "azure"
SAMPLES_FILE = ROOT / "adversarial_experiments" / "samples.json"

MODELS = [
    "gemini-3.1-pro", "gpt-5.2",
    "qwen3-vl-235b-a22b", "qwen3-vl-32b", "qwen3-vl-30b-a3b", "qwen3-vl-8b",
    "llama4-maverick", "llama4-scout",
    "gemma3-27b-it", "gemma3-12b-it", "gemma3-4b-it",
    "phi-4-multimodal",
]
TRANSFORMS = ["original", "jpeg_compression", "noise", "aspect_ratio", "low_contrast", "rotation", "original_in_paper", "blurred_in_paper"]
JUDGES = ["gpt-4o", "mistral-large-3"]

with open(SAMPLES_FILE) as f:
    samples = json.load(f)

results = {}

for subfolder, fig_keys in samples["samples"].items():
    for fig_key in fig_keys:
        fig_entry = {}
        for model in MODELS:
            model_entry = {}
            for transform in TRANSFORMS:
                transform_entry = {}
                # Load model description
                desc_path = TRANSFORMS_DIR / model / transform / subfolder / f"{fig_key}.json"
                if desc_path.exists():
                    desc_data = json.load(open(desc_path))
                    transform_entry["description"] = desc_data.get("model_annotation", "")
                    if not transform_entry["description"]:
                        descs = desc_data.get("model_annotations", {})
                        if descs:
                            transform_entry["descriptions_by_lang"] = descs

                # Load evaluations per judge
                for judge in JUDGES:
                    eval_path = EVAL_DIR / judge / model / transform / subfolder / f"{fig_key}.json"
                    if eval_path.exists():
                        eval_data = json.load(open(eval_path))
                        transform_entry[f"{judge}_score"] = eval_data.get("mqm_score", eval_data.get("mqm_score_avg"))
                        transform_entry[f"{judge}_errors"] = eval_data.get("errors", [])
                        transform_entry[f"{judge}_error_count"] = eval_data.get("error_count", len(eval_data.get("errors", [])))
                        # Multi-language
                        if "mqm_by_language" in eval_data:
                            transform_entry[f"{judge}_by_lang"] = {
                                lang: {"score": v.get("mqm_score"), "errors": v.get("errors", []), "error_count": v.get("error_count", 0)}
                                for lang, v in eval_data["mqm_by_language"].items()
                            }

                if transform_entry:
                    model_entry[transform] = transform_entry

            if model_entry:
                fig_entry[model] = model_entry

        if fig_entry:
            results[fig_key] = {"subfolder": subfolder, "models": fig_entry}

out_path = DASHBOARD_DATA / "transform_evaluations.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

total = len(results)
print(f"Exported {total} figures to {out_path}")
