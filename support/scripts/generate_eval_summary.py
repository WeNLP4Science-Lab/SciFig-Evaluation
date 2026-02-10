"""Generate evaluation summary with plots and markdown report.

Reads all MQM evaluation results from output/evaluation/ and
output/evaluation_structured/, computes statistics, generates plots,
and writes a summary markdown document.

Usage:
    python3 support/scripts/generate_eval_summary.py
"""

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_DIR = ROOT / "output" / "evaluation"
EVAL_STRUCT_DIR = ROOT / "output" / "evaluation_structured"
PLOTS_DIR = ROOT / "support" / "docs" / "eval_plots"
OUTPUT_MD = ROOT / "support" / "docs" / "sample_summary.md"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# MQM weights reference
MQM_WEIGHTS = {
    ("Accuracy", "Major"): 5.0, ("Accuracy", "Minor"): 2.0,
    ("Completeness", "Major"): 3.5, ("Completeness", "Minor"): 1.5,
    ("Clarity and Readability", "Major"): 2.0, ("Clarity and Readability", "Minor"): 1.0,
}

SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]
SUBFOLDER_LABELS = {
    "bulgarian_only": "Bulgarian",
    "chinese_only": "Chinese",
    "english_only": "English",
    "german_only": "German",
    "multi_language": "Multi-Lang",
}


# ── Data loading ──────────────────────────────────────────────────────

def load_eval_results(base_dir: Path, model: str = "gpt-4o-mini") -> list[dict]:
    """Load all evaluation JSON files, flattening multi-language into per-language entries."""
    results = []
    model_dir = base_dir / model
    for subfolder in SUBFOLDERS:
        folder = model_dir / subfolder
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.json")):
            with open(path) as f:
                data = json.load(f)
            data["subfolder"] = subfolder

            if "mqm_by_language" in data:
                # Multi-language: expand into per-language entries
                for lang, lang_result in data["mqm_by_language"].items():
                    entry = {
                        "figure_key": data["figure_key"],
                        "subfolder": subfolder,
                        "figure_type": data.get("figure_type", ""),
                        "evaluation_type": data.get("evaluation_type", ""),
                        "language": lang,
                        "is_multi": True,
                        **lang_result,
                    }
                    # Add breakdown if structured
                    bv = data.get("breakdown_verification_by_language", {}).get(lang)
                    if bv:
                        entry["breakdown_verification"] = bv
                    results.append(entry)
            else:
                entry = {
                    "figure_key": data["figure_key"],
                    "subfolder": subfolder,
                    "figure_type": data.get("figure_type", ""),
                    "evaluation_type": data.get("evaluation_type", ""),
                    "language": SUBFOLDER_LABELS.get(subfolder, subfolder).replace("-Lang", ""),
                    "is_multi": False,
                    "errors": data.get("errors", []),
                    "mqm_score": data.get("mqm_score", 0),
                    "total_penalty": data.get("total_penalty", 0),
                    "error_count": data.get("error_count", 0),
                }
                bv = data.get("breakdown_verification")
                if bv:
                    entry["breakdown_verification"] = bv
                results.append(entry)
    return results


# ── Statistics ────────────────────────────────────────────────────────

def compute_stats(results: list[dict]) -> dict:
    scores = [r["mqm_score"] for r in results]
    penalties = [r["total_penalty"] for r in results]
    error_counts = [r["error_count"] for r in results]

    # Error category breakdown
    cat_counter = Counter()
    sub_counter = Counter()
    sev_counter = Counter()
    cat_sev_counter = Counter()
    for r in results:
        for err in r.get("errors", []):
            cat = err.get("category", "Unknown")
            sub = err.get("sub_type", "Unknown")
            sev = err.get("severity", "Unknown")
            cat_counter[cat] += 1
            sub_counter[sub] += 1
            sev_counter[sev] += 1
            cat_sev_counter[(cat, sev)] += 1

    # By figure type
    by_type = defaultdict(list)
    for r in results:
        by_type[r["figure_type"]].append(r["mqm_score"])

    # By language
    by_lang = defaultdict(list)
    for r in results:
        by_lang[r["language"]].append(r["mqm_score"])

    # By subfolder
    by_sub = defaultdict(list)
    for r in results:
        by_sub[r["subfolder"]].append(r["mqm_score"])

    # Breakdown stats (structured only)
    bv_completeness = []
    bv_count_consistent = 0
    bv_total = 0
    for r in results:
        bv = r.get("breakdown_verification")
        if bv:
            bv_completeness.append(bv["field_completeness"])
            bv_total += 1
            if bv.get("count_consistent"):
                bv_count_consistent += 1

    return {
        "n": len(results),
        "mqm_mean": statistics.mean(scores) if scores else 0,
        "mqm_median": statistics.median(scores) if scores else 0,
        "mqm_stdev": statistics.stdev(scores) if len(scores) > 1 else 0,
        "mqm_min": min(scores) if scores else 0,
        "mqm_max": max(scores) if scores else 0,
        "penalty_mean": statistics.mean(penalties) if penalties else 0,
        "errors_mean": statistics.mean(error_counts) if error_counts else 0,
        "errors_total": sum(error_counts),
        "cat_counter": cat_counter,
        "sub_counter": sub_counter,
        "sev_counter": sev_counter,
        "cat_sev_counter": cat_sev_counter,
        "by_type": {k: statistics.mean(v) for k, v in by_type.items()},
        "by_lang": {k: statistics.mean(v) for k, v in by_lang.items()},
        "by_sub": {k: statistics.mean(v) for k, v in by_sub.items()},
        "bv_completeness_mean": statistics.mean(bv_completeness) if bv_completeness else None,
        "bv_count_consistent_pct": (bv_count_consistent / bv_total * 100) if bv_total else None,
        "scores": scores,
    }


# ── Plots ─────────────────────────────────────────────────────────────

def plot_mqm_comparison(unstruct: list[dict], struct: list[dict]):
    """Bar chart comparing MQM scores per figure (single-language only)."""
    # Get single-language figures only for clean comparison
    u_scores = {r["figure_key"]: r["mqm_score"] for r in unstruct if not r["is_multi"]}
    s_scores = {r["figure_key"]: r["mqm_score"] for r in struct if not r["is_multi"]}
    keys = sorted(set(u_scores) & set(s_scores))

    fig, ax = plt.subplots(figsize=(14, 5))
    x = range(len(keys))
    w = 0.35
    ax.bar([i - w/2 for i in x], [u_scores[k] for k in keys], w, label="Unstructured", color="#4C72B0")
    ax.bar([i + w/2 for i in x], [s_scores[k] for k in keys], w, label="Structured", color="#DD8452")
    ax.set_xticks(list(x))
    ax.set_xticklabels([k.replace("_fig_", "\n") for k in keys], fontsize=7, rotation=45, ha="right")
    ax.set_ylabel("MQM Score (100 = perfect)")
    ax.set_title("MQM Scores: Unstructured vs Structured (Single-Language Figures)")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "mqm_comparison_bar.png", dpi=150)
    plt.close(fig)


def plot_error_distribution(unstruct_stats: dict, struct_stats: dict):
    """Stacked bar chart of error categories for both approaches."""
    cats = ["Accuracy", "Completeness", "Clarity and Readability"]
    sevs = ["Major", "Minor"]
    colors = {"Major": "#C44E52", "Minor": "#CCB974"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, stats, title in [(axes[0], unstruct_stats, "Unstructured"), (axes[1], struct_stats, "Structured")]:
        bottoms = [0] * len(cats)
        for sev in sevs:
            vals = [stats["cat_sev_counter"].get((c, sev), 0) for c in cats]
            ax.bar(cats, vals, bottom=bottoms, label=sev, color=colors[sev])
            bottoms = [b + v for b, v in zip(bottoms, vals)]
        ax.set_title(title)
        ax.set_ylabel("Error Count")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        # Wrap long label
        ax.set_xticklabels(["Accuracy", "Completeness", "Clarity &\nReadability"], fontsize=9)

    fig.suptitle("Error Distribution by Category and Severity", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "error_distribution.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_error_subtypes(unstruct_stats: dict, struct_stats: dict):
    """Horizontal bar of error sub-types across both approaches."""
    all_subs = sorted(set(unstruct_stats["sub_counter"]) | set(struct_stats["sub_counter"]))
    u_vals = [unstruct_stats["sub_counter"].get(s, 0) for s in all_subs]
    s_vals = [struct_stats["sub_counter"].get(s, 0) for s in all_subs]

    fig, ax = plt.subplots(figsize=(10, 6))
    y = range(len(all_subs))
    h = 0.35
    ax.barh([i + h/2 for i in y], u_vals, h, label="Unstructured", color="#4C72B0")
    ax.barh([i - h/2 for i in y], s_vals, h, label="Structured", color="#DD8452")
    ax.set_yticks(list(y))
    ax.set_yticklabels(all_subs, fontsize=8)
    ax.set_xlabel("Count")
    ax.set_title("Error Sub-types: Unstructured vs Structured")
    ax.legend()
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "error_subtypes.png", dpi=150)
    plt.close(fig)


def plot_by_language(unstruct: list[dict], struct: list[dict]):
    """MQM scores by language for both approaches."""
    u_by_lang = defaultdict(list)
    s_by_lang = defaultdict(list)
    for r in unstruct:
        u_by_lang[r["language"]].append(r["mqm_score"])
    for r in struct:
        s_by_lang[r["language"]].append(r["mqm_score"])

    langs = sorted(set(u_by_lang) | set(s_by_lang))
    u_means = [statistics.mean(u_by_lang[l]) if l in u_by_lang else 0 for l in langs]
    s_means = [statistics.mean(s_by_lang[l]) if l in s_by_lang else 0 for l in langs]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(langs))
    w = 0.35
    ax.bar([i - w/2 for i in x], u_means, w, label="Unstructured", color="#4C72B0")
    ax.bar([i + w/2 for i in x], s_means, w, label="Structured", color="#DD8452")
    ax.set_xticks(list(x))
    ax.set_xticklabels(langs)
    ax.set_ylabel("Mean MQM Score")
    ax.set_title("Mean MQM Score by Language")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "mqm_by_language.png", dpi=150)
    plt.close(fig)


def plot_by_figure_type(unstruct: list[dict], struct: list[dict]):
    """MQM scores by figure type."""
    u_by_type = defaultdict(list)
    s_by_type = defaultdict(list)
    for r in unstruct:
        u_by_type[r["figure_type"]].append(r["mqm_score"])
    for r in struct:
        s_by_type[r["figure_type"]].append(r["mqm_score"])

    types = sorted(set(u_by_type) | set(s_by_type))
    u_means = [statistics.mean(u_by_type[t]) if t in u_by_type else 0 for t in types]
    s_means = [statistics.mean(s_by_type[t]) if t in s_by_type else 0 for t in types]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(types))
    w = 0.35
    ax.bar([i - w/2 for i in x], u_means, w, label="Unstructured", color="#4C72B0")
    ax.bar([i + w/2 for i in x], s_means, w, label="Structured", color="#DD8452")
    ax.set_xticks(list(x))
    ax.set_xticklabels(types)
    ax.set_ylabel("Mean MQM Score")
    ax.set_title("Mean MQM Score by Figure Type")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "mqm_by_figure_type.png", dpi=150)
    plt.close(fig)


def plot_score_distribution(unstruct: list[dict], struct: list[dict]):
    """Histogram of MQM score distributions."""
    u_scores = [r["mqm_score"] for r in unstruct]
    s_scores = [r["mqm_score"] for r in struct]

    fig, ax = plt.subplots(figsize=(8, 5))
    bins = range(55, 101, 5)
    ax.hist(u_scores, bins=bins, alpha=0.6, label="Unstructured", color="#4C72B0", edgecolor="white")
    ax.hist(s_scores, bins=bins, alpha=0.6, label="Structured", color="#DD8452", edgecolor="white")
    ax.set_xlabel("MQM Score")
    ax.set_ylabel("Count")
    ax.set_title("MQM Score Distribution")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "score_distribution.png", dpi=150)
    plt.close(fig)


# ── Markdown ──────────────────────────────────────────────────────────

def generate_markdown(
    unstruct: list[dict], struct: list[dict],
    u_stats: dict, s_stats: dict,
) -> str:
    lines = []
    lines.append("# Sample Evaluation Summary")
    lines.append("")
    lines.append("> MQM-based evaluation of GPT-4o-mini figure annotations (20 sample figures)")
    lines.append("> ")
    lines.append("> - **Unstructured**: paragraph-only descriptions")
    lines.append("> - **Structured**: paragraph + component breakdown (Option C: paragraph MQM for fair comparison)")
    lines.append("")

    # ── Overview
    lines.append("## Overview")
    lines.append("")
    lines.append("| Metric | Unstructured | Structured |")
    lines.append("|---|---|---|")
    lines.append(f"| Evaluations | {u_stats['n']} | {s_stats['n']} |")
    lines.append(f"| MQM Mean | {u_stats['mqm_mean']:.1f} | {s_stats['mqm_mean']:.1f} |")
    lines.append(f"| MQM Median | {u_stats['mqm_median']:.1f} | {s_stats['mqm_median']:.1f} |")
    lines.append(f"| MQM Std Dev | {u_stats['mqm_stdev']:.1f} | {s_stats['mqm_stdev']:.1f} |")
    lines.append(f"| MQM Min | {u_stats['mqm_min']:.1f} | {s_stats['mqm_min']:.1f} |")
    lines.append(f"| MQM Max | {u_stats['mqm_max']:.1f} | {s_stats['mqm_max']:.1f} |")
    lines.append(f"| Avg Errors/Figure | {u_stats['errors_mean']:.1f} | {s_stats['errors_mean']:.1f} |")
    lines.append(f"| Total Errors | {u_stats['errors_total']} | {s_stats['errors_total']} |")
    lines.append(f"| Avg Penalty | {u_stats['penalty_mean']:.1f} | {s_stats['penalty_mean']:.1f} |")
    if s_stats["bv_completeness_mean"] is not None:
        lines.append(f"| Breakdown Field Completeness | — | {s_stats['bv_completeness_mean']*100:.0f}% |")
    if s_stats["bv_count_consistent_pct"] is not None:
        lines.append(f"| Breakdown Count Consistency | — | {s_stats['bv_count_consistent_pct']:.0f}% |")
    lines.append("")

    # ── Score comparison plot
    lines.append("## MQM Score Comparison")
    lines.append("")
    lines.append("![MQM Comparison](eval_plots/mqm_comparison_bar.png)")
    lines.append("")

    # ── Per-figure table
    lines.append("## Per-Figure Results")
    lines.append("")
    lines.append("### Single-Language Figures")
    lines.append("")
    lines.append("| Figure | Type | Unstruct MQM | Unstruct Errors | Struct MQM | Struct Errors | Breakdown |")
    lines.append("|---|---|---|---|---|---|---|")

    u_by_key = {}
    s_by_key = {}
    for r in unstruct:
        if not r["is_multi"]:
            u_by_key[r["figure_key"]] = r
    for r in struct:
        if not r["is_multi"]:
            s_by_key[r["figure_key"]] = r

    for key in sorted(set(u_by_key) | set(s_by_key)):
        u = u_by_key.get(key, {})
        s = s_by_key.get(key, {})
        ft = u.get("figure_type", s.get("figure_type", ""))
        u_mqm = f"{u['mqm_score']:.1f}" if u else "—"
        u_err = str(u.get("error_count", "—")) if u else "—"
        s_mqm = f"{s['mqm_score']:.1f}" if s else "—"
        s_err = str(s.get("error_count", "—")) if s else "—"
        bv = s.get("breakdown_verification", {})
        bv_str = f"{bv['field_completeness']*100:.0f}%" if bv else "—"
        lines.append(f"| {key} | {ft} | {u_mqm} | {u_err} | {s_mqm} | {s_err} | {bv_str} |")
    lines.append("")

    # Multi-language table
    lines.append("### Multi-Language Figures")
    lines.append("")
    lines.append("| Figure | Language | Unstruct MQM | Unstruct Errors | Struct MQM | Struct Errors |")
    lines.append("|---|---|---|---|---|---|")

    u_multi = defaultdict(dict)
    s_multi = defaultdict(dict)
    for r in unstruct:
        if r["is_multi"]:
            u_multi[r["figure_key"]][r["language"]] = r
    for r in struct:
        if r["is_multi"]:
            s_multi[r["figure_key"]][r["language"]] = r

    for key in sorted(set(u_multi) | set(s_multi)):
        langs = sorted(set(list(u_multi.get(key, {}).keys()) + list(s_multi.get(key, {}).keys())))
        for lang in langs:
            u = u_multi.get(key, {}).get(lang, {})
            s = s_multi.get(key, {}).get(lang, {})
            u_mqm = f"{u['mqm_score']:.1f}" if u else "—"
            u_err = str(u.get("error_count", "—")) if u else "—"
            s_mqm = f"{s['mqm_score']:.1f}" if s else "—"
            s_err = str(s.get("error_count", "—")) if s else "—"
            lines.append(f"| {key} | {lang} | {u_mqm} | {u_err} | {s_mqm} | {s_err} |")
    lines.append("")

    # ── Score distribution
    lines.append("## Score Distribution")
    lines.append("")
    lines.append("![Score Distribution](eval_plots/score_distribution.png)")
    lines.append("")

    # ── By language
    lines.append("## MQM by Language")
    lines.append("")
    lines.append("![MQM by Language](eval_plots/mqm_by_language.png)")
    lines.append("")
    lines.append("| Language | Unstruct Mean | Struct Mean |")
    lines.append("|---|---|---|")
    all_langs = sorted(set(u_stats["by_lang"]) | set(s_stats["by_lang"]))
    for lang in all_langs:
        u_val = f"{u_stats['by_lang'][lang]:.1f}" if lang in u_stats["by_lang"] else "—"
        s_val = f"{s_stats['by_lang'][lang]:.1f}" if lang in s_stats["by_lang"] else "—"
        lines.append(f"| {lang} | {u_val} | {s_val} |")
    lines.append("")

    # ── By figure type
    lines.append("## MQM by Figure Type")
    lines.append("")
    lines.append("![MQM by Figure Type](eval_plots/mqm_by_figure_type.png)")
    lines.append("")
    lines.append("| Figure Type | Unstruct Mean | Struct Mean |")
    lines.append("|---|---|---|")
    all_types = sorted(set(u_stats["by_type"]) | set(s_stats["by_type"]))
    for ft in all_types:
        u_val = f"{u_stats['by_type'][ft]:.1f}" if ft in u_stats["by_type"] else "—"
        s_val = f"{s_stats['by_type'][ft]:.1f}" if ft in s_stats["by_type"] else "—"
        lines.append(f"| {ft} | {u_val} | {s_val} |")
    lines.append("")

    # ── Error analysis
    lines.append("## Error Analysis")
    lines.append("")
    lines.append("![Error Distribution](eval_plots/error_distribution.png)")
    lines.append("")
    lines.append("### Error Counts by Category and Severity")
    lines.append("")
    lines.append("| Category | Severity | Unstructured | Structured |")
    lines.append("|---|---|---|---|")
    for cat in ["Accuracy", "Completeness", "Clarity and Readability"]:
        for sev in ["Major", "Minor"]:
            u_val = u_stats["cat_sev_counter"].get((cat, sev), 0)
            s_val = s_stats["cat_sev_counter"].get((cat, sev), 0)
            lines.append(f"| {cat} | {sev} | {u_val} | {s_val} |")
    lines.append("")

    # ── Error sub-types
    lines.append("### Error Sub-types")
    lines.append("")
    lines.append("![Error Sub-types](eval_plots/error_subtypes.png)")
    lines.append("")
    lines.append("| Sub-type | Unstructured | Structured |")
    lines.append("|---|---|---|")
    all_subs = sorted(set(u_stats["sub_counter"]) | set(s_stats["sub_counter"]),
                      key=lambda s: -(u_stats["sub_counter"].get(s, 0) + s_stats["sub_counter"].get(s, 0)))
    for sub in all_subs:
        u_val = u_stats["sub_counter"].get(sub, 0)
        s_val = s_stats["sub_counter"].get(sub, 0)
        lines.append(f"| {sub} | {u_val} | {s_val} |")
    lines.append("")

    # ── MQM formula reminder
    lines.append("## Scoring Methodology")
    lines.append("")
    lines.append("MQM Score = max(0, 100 - total_penalty)")
    lines.append("")
    lines.append("| Error Category | Major Weight | Minor Weight |")
    lines.append("|---|---|---|")
    lines.append("| Accuracy | 5.0 | 2.0 |")
    lines.append("| Completeness | 3.5 | 1.5 |")
    lines.append("| Clarity and Readability | 2.0 | 1.0 |")
    lines.append("")
    lines.append("- **100** = error-free description")
    lines.append("- **0** = penalties exceed 100 points")
    lines.append("- Judge model: `gpt-4o-mini` via OpenRouter")
    lines.append("- Sample: 20 figures (4 per language folder), 20 single-language + multi-language per-language evaluations")
    lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────

def main():
    print("Loading evaluation results...")
    unstruct = load_eval_results(EVAL_DIR)
    struct = load_eval_results(EVAL_STRUCT_DIR)
    print(f"  Unstructured: {len(unstruct)} evaluations")
    print(f"  Structured:   {len(struct)} evaluations")

    print("Computing statistics...")
    u_stats = compute_stats(unstruct)
    s_stats = compute_stats(struct)

    print("Generating plots...")
    plot_mqm_comparison(unstruct, struct)
    print("  ✓ mqm_comparison_bar.png")
    plot_error_distribution(u_stats, s_stats)
    print("  ✓ error_distribution.png")
    plot_error_subtypes(u_stats, s_stats)
    print("  ✓ error_subtypes.png")
    plot_by_language(unstruct, struct)
    print("  ✓ mqm_by_language.png")
    plot_by_figure_type(unstruct, struct)
    print("  ✓ mqm_by_figure_type.png")
    plot_score_distribution(unstruct, struct)
    print("  ✓ score_distribution.png")

    print("Writing summary markdown...")
    md = generate_markdown(unstruct, struct, u_stats, s_stats)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"  ✓ {OUTPUT_MD}")

    print()
    print(f"Summary: Unstructured MQM={u_stats['mqm_mean']:.1f} vs Structured MQM={s_stats['mqm_mean']:.1f}")
    print("Done.")


if __name__ == "__main__":
    main()
