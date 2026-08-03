"""RQ1: Item-level error-type agreement between GPT-4o judge and humans.

Defends the GPT-4o judge against No6d W4: even though absolute MQM scores diverge
(item-level Spearman rho = 0.58, mean bias -15), the *taxonomy* of errors flagged
by GPT-4o overlaps substantially with human annotations. Computes:

  - Category-level (Accuracy / Clarity / Completeness) precision/recall/F1/Jaccard
  - Sub-type-level (after mapping) precision/recall/F1/Jaccard
  - Error-count rank correlation (Spearman on error volume per pair)
  - Per-error-type confusion (which types align best, which are LLM-judge false alarms)

Output: output/evaluation-results/rq1/error_type_agreement.json
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent.parent
HUMAN_RESULTS = ROOT / "HumanEval" / "human_eval_results.json"
JUDGE_DIR = ROOT / "output" / "evaluation" / "atomic_mqm_v2" / "azure" / "gpt-4o"
OUTPUT = ROOT / "output" / "evaluation-results" / "rq1" / "error_type_agreement.json"

MODEL_NORM = {
    "gemma3-27b": "gemma3-27b-it",
    "qwen-vl-8b": "qwen3-vl-8b",
    "qwen-vl-30b": "qwen3-vl-30b-a3b",
    "gpt-5.2": "gpt-5.2",
}
HUMAN_MODELS = {"gemma3-27b-it", "gpt-5.2", "qwen3-vl-30b-a3b", "qwen3-vl-8b"}

# Map human short codes to canonical labels (matching GPT-4o judge vocabulary).
# Two human codes (acc_axis_interpr, acc_legend_interpr) collapse to one judge label.
HUMAN_TO_CANONICAL = {
    "acc_axis_interpr": "Incorrect Axis or Legend Interpretation",
    "acc_legend_interpr": "Incorrect Axis or Legend Interpretation",
    "acc_num_val": "Incorrect Numerical Value",
    "acc_structure_desc": "Incorrect Structural Description",
    "acc_visual_attb_mapping": "Incorrect Visual Attribute Mapping",
    "clar_ambig": "Ambiguity",  # no direct judge equivalent
    "clar_overgeneral": "Over-Generalization",
    "clar_sentence_struct": "Poor Sentence Structure",
    "comp_hallucination": "Hallucinated Content",
    "comp_missing_axis": "Missing Axis Description",
    "comp_missing_purpose": "Missing Chart Purpose",
    "comp_unwanted_interp": "Unwanted Interpretation",
    "comp_visual_feat_missing": "Missing Visual Features",
}

# Judge writes minor variants of the same labels; normalise to canonical.
JUDGE_ALIASES = {
    "Incorrect Axis Interpretation": "Incorrect Axis or Legend Interpretation",
    "Incorrect Legend Interpretation": "Incorrect Axis or Legend Interpretation",
    "Missing Structural Description": "Missing Visual Features",
    "Incomplete": "Missing Visual Features",
    "Overly Verbose Description": "Poor Sentence Structure",
}


def canonicalise_judge(sub_type: str) -> str:
    if sub_type is None:
        return ""
    return JUDGE_ALIASES.get(sub_type, sub_type).strip()


def norm_model(m: str) -> str:
    return MODEL_NORM.get(m, m)


def load_human_pairs():
    """Return {(figure_key, model): {"categories": set, "sub_types": set, "count": int}}.

    Union errors across annotators for each pair; each annotator's errors are
    accepted (any error either flagged by any human is considered 'human-flagged').
    """
    data = json.load(open(HUMAN_RESULTS))
    per_pair = defaultdict(lambda: {"categories": set(), "sub_types": set(), "counts": []})
    for r in data["results"]:
        key = (r["figure_key"], norm_model(r["model_name"]))
        cnt = 0
        for e in r.get("errors", []):
            cat = (e.get("category") or "").strip()
            sub = HUMAN_TO_CANONICAL.get(e.get("sub_type"), e.get("sub_type") or "")
            if cat:
                per_pair[key]["categories"].add(cat)
            if sub:
                per_pair[key]["sub_types"].add(sub)
            cnt += 1
        per_pair[key]["counts"].append(cnt)
    # Average error count across annotators for this pair.
    for k, v in per_pair.items():
        v["count"] = float(np.mean(v["counts"]))
        del v["counts"]
    return per_pair


def load_judge_pairs():
    per_pair = {}
    for model in HUMAN_MODELS:
        model_dir = JUDGE_DIR / model / "original" / "english_only"
        if not model_dir.exists():
            continue
        for path in model_dir.glob("english_fig_*.json"):
            try:
                d = json.load(open(path))
            except Exception:
                continue
            key = (d["figure_key"], model)
            cats, subs = set(), set()
            for e in d.get("errors", []):
                cat = (e.get("category") or "").strip()
                sub = canonicalise_judge((e.get("sub_type") or "").strip())
                if cat:
                    cats.add(cat)
                if sub:
                    subs.add(sub)
            per_pair[key] = {
                "categories": cats,
                "sub_types": subs,
                "count": float(d.get("error_count", len(d.get("errors", [])))),
            }
    return per_pair


def prf1(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


def jaccard(a, b):
    if not a and not b:
        return 1.0
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def per_pair_metrics(hp, jp, field):
    """Aggregate P/R/F1/Jaccard across pairs at the given field level."""
    tp = fp = fn = 0
    jaccards = []
    for key, h in hp.items():
        j = jp.get(key)
        if j is None:
            continue
        h_set, j_set = h[field], j[field]
        tp += len(h_set & j_set)
        fp += len(j_set - h_set)
        fn += len(h_set - j_set)
        jaccards.append(jaccard(h_set, j_set))
    p, r, f = prf1(tp, fp, fn)
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1": round(f, 4),
        "mean_jaccard": round(float(np.mean(jaccards)), 4) if jaccards else 0.0,
        "median_jaccard": round(float(np.median(jaccards)), 4) if jaccards else 0.0,
        "n_pairs": len(jaccards),
    }


def per_type_breakdown(hp, jp, field):
    """For each label, count how many pairs humans flagged it, judge flagged it,
    and both flagged it. Report per-label precision/recall/F1."""
    all_labels = set()
    for v in hp.values():
        all_labels |= v[field]
    for v in jp.values():
        all_labels |= v[field]

    out = {}
    for label in sorted(all_labels):
        tp = fp = fn = tn = 0
        for key in hp:
            if key not in jp:
                continue
            h_has = label in hp[key][field]
            j_has = label in jp[key][field]
            if h_has and j_has:
                tp += 1
            elif h_has and not j_has:
                fn += 1
            elif not h_has and j_has:
                fp += 1
            else:
                tn += 1
        p, r, f = prf1(tp, fp, fn)
        out[label] = {
            "human_flagged_pairs": tp + fn,
            "judge_flagged_pairs": tp + fp,
            "both_flagged": tp,
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1": round(f, 4),
        }
    return out


def volume_correlation(hp, jp):
    keys = sorted(set(hp) & set(jp))
    h_counts = np.array([hp[k]["count"] for k in keys])
    j_counts = np.array([jp[k]["count"] for k in keys])
    return {
        "n_pairs": len(keys),
        "spearman_rho": round(float(stats.spearmanr(h_counts, j_counts).statistic), 4),
        "spearman_p": float(stats.spearmanr(h_counts, j_counts).pvalue),
        "pearson_r": round(float(stats.pearsonr(h_counts, j_counts).statistic), 4),
        "pearson_p": float(stats.pearsonr(h_counts, j_counts).pvalue),
        "mean_human_errors": round(float(h_counts.mean()), 3),
        "mean_judge_errors": round(float(j_counts.mean()), 3),
    }


def main():
    hp = load_human_pairs()
    jp = load_judge_pairs()

    common = set(hp) & set(jp)
    result = {
        "metadata": {
            "human_source": str(HUMAN_RESULTS.relative_to(ROOT)),
            "judge_source": str(JUDGE_DIR.relative_to(ROOT)),
            "n_human_pairs": len(hp),
            "n_judge_pairs": len(jp),
            "n_common_pairs": len(common),
            "models": sorted(HUMAN_MODELS),
        },
        "category_level_agreement": per_pair_metrics(hp, jp, "categories"),
        "sub_type_level_agreement": per_pair_metrics(hp, jp, "sub_types"),
        "error_volume_correlation": volume_correlation(hp, jp),
        "per_category_breakdown": per_type_breakdown(hp, jp, "categories"),
        "per_sub_type_breakdown": per_type_breakdown(hp, jp, "sub_types"),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2))
    print(f"wrote {OUTPUT}")

    # Console summary
    print("\n== Category-level agreement ==")
    for k, v in result["category_level_agreement"].items():
        print(f"  {k}: {v}")
    print("\n== Sub-type-level agreement ==")
    for k, v in result["sub_type_level_agreement"].items():
        print(f"  {k}: {v}")
    print("\n== Error-volume correlation ==")
    for k, v in result["error_volume_correlation"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
