#!/usr/bin/env python3
"""Export prompt_reverse and caption_bias experiment results to dashboard JSON."""

import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE / "output" / "experiments"
DASHBOARD_DATA = BASE / "dashboard" / "public" / "data"
BENCHMARKS_DIR = BASE / "adversarial_experiments" / "benchmarks"

MODELS = [
    "gpt-5.2",
    "gemini-3.1-pro",
    "qwen3-vl-235b-a22b",
    "qwen3-vl-32b",
    "qwen3-vl-30b-a3b",
    "qwen3-vl-8b",
    "llama4-maverick",
    "llama4-scout",
    "gemma3-27b-it",
    "gemma3-12b-it",
    "gemma3-4b-it",
    "phi-4-multimodal",
]

# Load adversarial manifest to get figure keys
manifest_path = DASHBOARD_DATA / "adversarial_experiments.json"
with open(manifest_path) as f:
    manifest = json.load(f)

figures_by_subfolder = manifest["figures_by_subfolder"]

# Load English translations for capability questions
cap_english = {}
for lang in ["bulgarian", "chinese", "german", "multi_language"]:
    en_path = BENCHMARKS_DIR / "capability" / "english" / f"{lang}.json"
    if en_path.exists():
        with open(en_path) as f:
            data = json.load(f)
        for fig_key, fig_data in data.items():
            for q in fig_data.get("questions", []):
                cap_english[(fig_key, q["id"])] = {
                    "question_english": q.get("question", ""),
                    "expected_answer_english": q.get("expected_answer", ""),
                }

results: dict = {}

for subfolder, fig_keys in figures_by_subfolder.items():
    for fig_key in fig_keys:
        entry: dict = {"models": {}}

        for model in MODELS:
            model_data: dict = {}

            # 1. Prompt reverse results
            pr_path = OUTPUT_DIR / "prompt_reverse" / model / subfolder / f"{fig_key}.json"
            if pr_path.exists():
                with open(pr_path) as f:
                    pr = json.load(f)
                model_data["prompt_reverse"] = {
                    "fact_description": pr.get("fact_description", ""),
                    "true_probe": {
                        "statement": pr.get("true_probe", {}).get("statement", ""),
                        "answer": pr.get("true_probe", {}).get("answer", ""),
                        "correct": pr.get("true_probe", {}).get("correct", False),
                    },
                    "false_probe": {
                        "statement": pr.get("false_probe", {}).get("statement", ""),
                        "answer": pr.get("false_probe", {}).get("answer", ""),
                        "correct": pr.get("false_probe", {}).get("correct", False),
                    },
                    "score": pr.get("score", 0),
                    "pattern": pr.get("pattern", "unknown"),
                }

            # 2. Caption bias - model description
            cb_desc_path = (
                OUTPUT_DIR / "caption_bias" / "modified_caption" / model / subfolder / f"{fig_key}.json"
            )
            description = ""
            if cb_desc_path.exists():
                with open(cb_desc_path) as f:
                    cb_desc = json.load(f)
                description = cb_desc.get("model_annotation", "")

            # 3. Caption bias evaluations from multiple judges
            judges_data = {}
            for judge in ["gpt-4o", "mistral-large-3"]:
                cb_eval_path = (
                    OUTPUT_DIR / "evaluation" / "caption_bias" / judge / model / subfolder / f"{fig_key}.json"
                )
                if cb_eval_path.exists():
                    with open(cb_eval_path) as f:
                        cb_eval = json.load(f)
                    judges_data[judge] = {
                        "resistance": cb_eval.get("resistance", 0),
                        "completeness": cb_eval.get("completeness", 0),
                        "evaluations": [
                            {
                                "claim": e.get("claim", ""),
                                "reality": e.get("reality", ""),
                                "mapped_to": e.get("mapped_to", ""),
                                "reason": e.get("reason", ""),
                            }
                            for e in cb_eval.get("evaluations", [])
                        ],
                    }

            if judges_data:
                model_data["caption_bias"] = {
                    "description": description,
                    "judges": judges_data,
                }

            # 4. Hallucination evaluations from multiple judges
            hallu_judges = {}
            for judge in ["gpt-4o", "mistral-large-3"]:
                hallu_eval_path = (
                    OUTPUT_DIR / "evaluation" / "hallucination" / judge / model / subfolder / f"{fig_key}.json"
                )
                if hallu_eval_path.exists():
                    with open(hallu_eval_path) as f:
                        hallu_eval = json.load(f)
                    hallu_judges[judge] = [
                        {
                            "probe_id": e.get("probe_id", ""),
                            "probe_type": e.get("probe_type", ""),
                            "question": e.get("question", ""),
                            "model_answer": e.get("model_answer", ""),
                            "judge_score": e.get("judge_score"),
                            "judge_reasoning": e.get("judge_reasoning", ""),
                        }
                        for e in hallu_eval.get("evaluations", [])
                    ]

            if hallu_judges:
                model_data["hallucination"] = {"judges": hallu_judges}

            # 5. Capability evaluations from multiple judges
            cap_judges = {}
            for judge in ["gpt-4o", "mistral-large-3"]:
                cap_eval_path = (
                    OUTPUT_DIR / "evaluation" / "capability" / judge / model / subfolder / f"{fig_key}.json"
                )
                if cap_eval_path.exists():
                    with open(cap_eval_path) as f:
                        cap_eval = json.load(f)
                    cap_judges[judge] = {
                        "average_score": cap_eval.get("average_score", 0),
                        "total_scored": cap_eval.get("total_scored", 0),
                        "total_excluded": cap_eval.get("total_excluded", 0),
                        "evaluations": [
                            {
                                "question_id": e.get("question_id", ""),
                                "question": e.get("question", ""),
                                "question_english": cap_english.get((fig_key, e.get("question_id", "")), {}).get("question_english", ""),
                                "expected_answer": e.get("expected_answer", ""),
                                "expected_answer_english": cap_english.get((fig_key, e.get("question_id", "")), {}).get("expected_answer_english", ""),
                                "model_answer": e.get("model_answer", ""),
                                "answer_type": e.get("answer_type", ""),
                                "score": e.get("score"),
                                "reason": e.get("reason", ""),
                                "excluded": e.get("excluded", False),
                            }
                            for e in cap_eval.get("evaluations", [])
                        ],
                    }

            if cap_judges:
                model_data["capability"] = {"judges": cap_judges}

            if model_data:
                entry["models"][model] = model_data

        if entry["models"]:
            results[fig_key] = entry

# Write output
out_path = DASHBOARD_DATA / "experiment_results.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

total_figures = len(results)
total_models = sum(len(v["models"]) for v in results.values())
pr_count = sum(
    1
    for v in results.values()
    for m in v["models"].values()
    if "prompt_reverse" in m
)
cb_count = sum(
    1
    for v in results.values()
    for m in v["models"].values()
    if "caption_bias" in m
)
cap_count = sum(
    1
    for v in results.values()
    for m in v["models"].values()
    if "capability" in m
)
print(f"Exported {total_figures} figures, {total_models} model entries")
print(f"  prompt_reverse: {pr_count}")
print(f"  caption_bias:   {cb_count}")
print(f"  capability:     {cap_count}")
print(f"  -> {out_path}")
