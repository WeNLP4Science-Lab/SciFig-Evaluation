"""Collect all experiment results into a single structured JSON.

Walks result directories, extracts key metrics from each JSON file,
and outputs a unified results file for downstream statistics and tables.

Output: results/statistics/collected_results.json

Usage:
    python collect_results.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import DATASET_DIR, RESULTS_DIR, GROUNDTRUTH_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

MODELS = [
    "gpt-5.2", "gemini-3.1-pro", "llama4-maverick",
    "qwen3-vl-235b-a22b", "qwen3-vl-30b-a3b", "qwen3-vl-8b",
    "gemma3-27b-it", "phi-4-multimodal",
]

TRANSFORMS = [
    "original", "noise", "low_contrast", "rotation",
    "in_paper", "in_paper_blur",
    "admittance_blur", "inductance_blur",
    "caption_bias",
]

PROBE_TYPES = ["admittance", "inductance"]
RESISTANCE_TYPES = ["inexist", "contra", "unanswerable"]

OUTPUT_DIR = RESULTS_DIR / "statistics"


def load_chart_types():
    """Load figure_id -> chart_type mapping from groundtruth."""
    mapping = {}
    for f in GROUNDTRUTH_DIR.glob("*.json"):
        with open(f) as fh:
            gt = json.load(fh)
        mapping[f.stem] = gt.get("figure_type", "Unknown")
    return mapping


def collect_baseline_mqm(chart_types):
    """Collect baseline MQM scores."""
    base_dir = RESULTS_DIR / "evaluation" / "description_tasks" / "baseline_descriptions"
    results = {}

    for model in MODELS:
        model_dir = base_dir / model
        if not model_dir.exists():
            continue

        scores = []
        for f in sorted(model_dir.glob("*.json")):
            with open(f) as fh:
                d = json.load(fh)
            fig_id = f.stem
            entry = {
                "figure_id": fig_id,
                "chart_type": chart_types.get(fig_id, "Unknown"),
                "mqm": d.get("mqm_deduped", d.get("mqm_raw")),
            }
            # Extract per-dimension penalties if available
            penalties = d.get("penalties_deduped", d.get("penalties", []))
            dims = {"Accuracy": 0, "Completeness": 0, "Clarity and Readability": 0}
            for p in penalties:
                dim = p.get("dimension", p.get("category", ""))
                if dim in dims:
                    dims[dim] += p.get("weight", p.get("penalty", 0))
            entry["penalty_accuracy"] = dims["Accuracy"]
            entry["penalty_completeness"] = dims["Completeness"]
            entry["penalty_clarity"] = dims["Clarity and Readability"]

            # Extract severity counts
            majors = sum(1 for p in penalties if p.get("severity") == "Major")
            minors = sum(1 for p in penalties if p.get("severity") == "Minor")
            entry["n_major"] = majors
            entry["n_minor"] = minors
            entry["n_penalties"] = len(penalties)

            scores.append(entry)

        results[model] = scores
        logger.info(f"  Baseline MQM {model}: {len(scores)} figures")

    return results


def collect_transform_mqm(chart_types):
    """Collect transform MQM scores."""
    base_dir = RESULTS_DIR / "evaluation" / "description_tasks" / "transforms"
    results = {}

    for transform in TRANSFORMS:
        results[transform] = {}
        for model in MODELS:
            model_dir = base_dir / transform / model
            if not model_dir.exists():
                continue

            scores = []
            for f in sorted(model_dir.glob("*.json")):
                with open(f) as fh:
                    d = json.load(fh)
                fig_id = f.stem
                scores.append({
                    "figure_id": fig_id,
                    "chart_type": chart_types.get(fig_id, "Unknown"),
                    "mqm": d.get("mqm_deduped", d.get("mqm_raw")),
                })
            results[transform][model] = scores

        total = sum(len(v) for v in results[transform].values())
        if total > 0:
            logger.info(f"  Transform MQM {transform}: {total} total across models")

    return results


def collect_caption_bias():
    """Collect caption bias behavioral evaluation."""
    base_dir = RESULTS_DIR / "evaluation" / "caption_bias"
    results = {}

    for model in MODELS:
        model_dir = base_dir / model
        if not model_dir.exists():
            continue

        entries = []
        for f in sorted(model_dir.glob("*.json")):
            with open(f) as fh:
                d = json.load(fh)
            entry = {
                "figure_id": f.stem,
                "followed_image": d.get("followed_image", 0),
                "followed_caption": d.get("followed_caption", 0),
                "not_addressed": d.get("not_addressed", 0),
                "resistance": d.get("resistance"),
                "completeness": d.get("completeness"),
                "num_modifications": d.get("num_modifications", 0),
            }
            # Per-modification details
            per_mod = []
            for ev in d.get("evaluations", []):
                per_mod.append({
                    "type": ev.get("type", ""),
                    "principle": ev.get("principle", ""),
                    "mapped_to": ev.get("mapped_to", ""),
                })
            entry["evaluations"] = per_mod
            entries.append(entry)

        results[model] = entries
        logger.info(f"  Caption bias {model}: {len(entries)} figures")

    return results


def collect_resistance(chart_types):
    """Collect hallucination resistance evaluation."""
    base_dir = RESULTS_DIR / "evaluation" / "resistance"
    results = {}

    for model in MODELS:
        model_dir = base_dir / model
        if not model_dir.exists():
            continue

        entries = []
        for f in sorted(model_dir.glob("*.json")):
            with open(f) as fh:
                d = json.load(fh)
            fig_id = f.stem
            per_probe = {}
            for ev in d.get("evaluations", []):
                pt = ev.get("probe_type", "")
                per_probe[pt] = ev.get("judge_score")

            entries.append({
                "figure_id": fig_id,
                "chart_type": chart_types.get(fig_id, "Unknown"),
                "inexist": per_probe.get("inexist"),
                "contra": per_probe.get("contra"),
                "unanswerable": per_probe.get("unanswerable"),
            })

        results[model] = entries
        logger.info(f"  Resistance {model}: {len(entries)} figures")

    return results


def collect_active_probes(chart_types):
    """Collect active admittance/inductance probe results."""
    base_dir = RESULTS_DIR / "evaluation" / "active_probes"
    results = {}

    for probe_type in PROBE_TYPES:
        results[probe_type] = {}
        for model in MODELS:
            model_dir = base_dir / model / probe_type
            if not model_dir.exists():
                continue

            entries = []
            for f in sorted(model_dir.glob("*.json")):
                with open(f) as fh:
                    d = json.load(fh)
                entries.append({
                    "figure_id": f.stem,
                    "chart_type": chart_types.get(f.stem, "Unknown"),
                    "admits": d.get("admits", False),
                    "fabricates": d.get("fabricates", False),
                    "correct": d.get("correct", False),
                })

            results[probe_type][model] = entries

        total = sum(len(v) for v in results[probe_type].values())
        if total > 0:
            logger.info(f"  Active {probe_type}: {total} total across models")

    return results


def collect_passive_probes(chart_types):
    """Collect passive admittance/inductance probe results."""
    base_dir = RESULTS_DIR / "evaluation" / "passive_probes"
    results = {}

    for probe_type in PROBE_TYPES:
        results[probe_type] = {}
        for model in MODELS:
            model_dir = base_dir / model / probe_type
            if not model_dir.exists():
                continue

            entries = []
            for f in sorted(model_dir.glob("*.json")):
                with open(f) as fh:
                    d = json.load(fh)
                entries.append({
                    "figure_id": f.stem,
                    "chart_type": chart_types.get(f.stem, "Unknown"),
                    "mentioned": d.get("mentioned", False),
                    "admits": d.get("admits", False),
                    "fabricates": d.get("fabricates", False),
                    "correct": d.get("correct", False),
                })

            results[probe_type][model] = entries

        total = sum(len(v) for v in results[probe_type].values())
        if total > 0:
            logger.info(f"  Passive {probe_type}: {total} total across models")

    return results


def collect_capability(chart_types):
    """Collect capability question evaluation results."""
    base_dir = RESULTS_DIR / "evaluation" / "capability"
    results = {}

    for model in MODELS:
        model_dir = base_dir / model
        if not model_dir.exists():
            continue

        entries = []
        for f in sorted(model_dir.glob("*.json")):
            with open(f) as fh:
                d = json.load(fh)
            fig_id = f.stem
            entries.append({
                "figure_id": fig_id,
                "chart_type": chart_types.get(fig_id, "Unknown"),
                **{k: v for k, v in d.items() if k not in ("figure_id",)},
            })

        results[model] = entries
        logger.info(f"  Capability {model}: {len(entries)} figures")

    if not results:
        logger.info("  Capability: no evaluation results found (0 for all models)")

    return results


def collect_ablation():
    """Collect ablation study results (Mistral vs GPT-4o probes)."""
    results = {}

    # Load ablation figure IDs
    abl_path = DATASET_DIR / "ablation_50.json"
    if abl_path.exists():
        with open(abl_path) as f:
            abl_figs = set(json.load(f)["figures"])
    else:
        abl_figs = set()

    # Resistance ablation
    for label, eval_dir in [
        ("gpt4o_probes", RESULTS_DIR / "evaluation" / "resistance" / "gpt-5.2"),
        ("mistral_probes", RESULTS_DIR / "evaluation" / "resistance_mistral" / "gpt-5.2"),
    ]:
        scores = []
        if eval_dir.exists():
            for f in eval_dir.glob("*.json"):
                if f.stem not in abl_figs:
                    continue
                with open(f) as fh:
                    d = json.load(fh)
                per_probe = {}
                for ev in d.get("evaluations", []):
                    per_probe[ev.get("probe_type", "")] = ev.get("judge_score")
                scores.append({
                    "figure_id": f.stem,
                    "inexist": per_probe.get("inexist"),
                    "contra": per_probe.get("contra"),
                    "unanswerable": per_probe.get("unanswerable"),
                })
        results[f"resistance_{label}"] = scores

    # Caption bias ablation
    for label, eval_dir in [
        ("gpt4o_probes", RESULTS_DIR / "evaluation" / "caption_bias" / "gpt-5.2"),
        ("mistral_probes", RESULTS_DIR / "evaluation" / "caption_bias_mistral" / "gpt-5.2"),
    ]:
        scores = []
        if eval_dir.exists():
            for f in eval_dir.glob("*.json"):
                if f.stem not in abl_figs:
                    continue
                with open(f) as fh:
                    d = json.load(fh)
                scores.append({
                    "figure_id": f.stem,
                    "followed_image": d.get("followed_image", 0),
                    "followed_caption": d.get("followed_caption", 0),
                    "resistance": d.get("resistance"),
                })
        results[f"caption_bias_{label}"] = scores

    for k, v in results.items():
        if v:
            logger.info(f"  Ablation {k}: {len(v)} figures")

    return results


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chart_types = load_chart_types()
    logger.info(f"Loaded {len(chart_types)} chart type mappings")

    collected = {
        "metadata": {
            "models": MODELS,
            "transforms": TRANSFORMS,
            "probe_types": PROBE_TYPES,
            "resistance_types": RESISTANCE_TYPES,
            "n_figures": len(chart_types),
            "chart_type_distribution": {},
        },
        "baseline_mqm": collect_baseline_mqm(chart_types),
        "transform_mqm": collect_transform_mqm(chart_types),
        "caption_bias": collect_caption_bias(),
        "resistance": collect_resistance(chart_types),
        "active_probes": collect_active_probes(chart_types),
        "passive_probes": collect_passive_probes(chart_types),
        "capability": collect_capability(chart_types),
        "ablation": collect_ablation(),
    }

    # Chart type distribution
    from collections import Counter
    ct_counts = Counter(chart_types.values())
    collected["metadata"]["chart_type_distribution"] = dict(ct_counts)

    # Summary counts
    summary = {}
    for model in MODELS:
        s = {"model": model}
        s["baseline_n"] = len(collected["baseline_mqm"].get(model, []))
        s["resistance_n"] = len(collected["resistance"].get(model, []))
        s["caption_bias_n"] = len(collected["caption_bias"].get(model, []))
        s["capability_n"] = len(collected["capability"].get(model, []))
        for pt in PROBE_TYPES:
            s[f"active_{pt}_n"] = len(collected["active_probes"].get(pt, {}).get(model, []))
            s[f"passive_{pt}_n"] = len(collected["passive_probes"].get(pt, {}).get(model, []))
        for t in TRANSFORMS:
            s[f"transform_{t}_n"] = len(collected["transform_mqm"].get(t, {}).get(model, []))
        summary[model] = s
    collected["summary"] = summary

    out_path = OUTPUT_DIR / "collected_results.json"
    with open(out_path, "w") as f:
        json.dump(collected, f, indent=2, ensure_ascii=False)

    logger.info(f"\nSaved to {out_path}")
    logger.info(f"File size: {out_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Print summary
    print("\n=== COLLECTION SUMMARY ===")
    for model, s in summary.items():
        print(f"  {model}: baseline={s['baseline_n']}, resistance={s['resistance_n']}, "
              f"caption_bias={s['caption_bias_n']}, capability={s['capability_n']}, "
              f"active_adm={s['active_admittance_n']}, active_ind={s['active_inductance_n']}")


if __name__ == "__main__":
    main()
