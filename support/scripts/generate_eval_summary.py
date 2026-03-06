"""Generate evaluation summary with plots and markdown report.

Auto-discovers all model subdirectories under output/evaluation/ and
output/evaluation_structured/, computes statistics, generates plots
(including cross-model comparisons), and writes a summary markdown document.

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
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_DIR = ROOT / "output" / "evaluation"
EVAL_STRUCT_DIR = ROOT / "output" / "evaluation_structured"
PLOTS_DIR = ROOT / "support" / "docs" / "eval_plots"
OUTPUT_MD = ROOT / "support" / "docs" / "sample_summary.md"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)

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

# Consistent colors for models
MODEL_COLORS = {
    "gpt-4o-mini": "#4C72B0",
    "gpt-5.2": "#55A868",
    "opus-4.6": "#C44E52",
}

def _model_color(model: str) -> str:
    return MODEL_COLORS.get(model, "#8C8C8C")


# ── Data loading ──────────────────────────────────────────────────────

def discover_models(base_dir: Path) -> list[str]:
    """Auto-discover model subdirectories."""
    if not base_dir.exists():
        return []
    return sorted(
        d.name for d in base_dir.iterdir()
        if d.is_dir() and any((d / sf).exists() for sf in SUBFOLDERS)
    )


def load_eval_results(base_dir: Path, model: str) -> list[dict]:
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

    by_type = defaultdict(list)
    for r in results:
        by_type[r["figure_type"]].append(r["mqm_score"])

    by_lang = defaultdict(list)
    for r in results:
        by_lang[r["language"]].append(r["mqm_score"])

    by_sub = defaultdict(list)
    for r in results:
        by_sub[r["subfolder"]].append(r["mqm_score"])

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

def plot_cross_model_overview(all_data: dict[str, dict]):
    """Grouped bar chart: mean MQM per model, unstructured vs structured."""
    models = sorted(all_data.keys())
    approaches = ["unstructured", "structured"]
    approach_labels = {"unstructured": "Unstructured", "structured": "Structured"}

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(models))
    w = 0.35

    for i, approach in enumerate(approaches):
        means = []
        for m in models:
            stats = all_data[m].get(f"{approach}_stats")
            means.append(stats["mqm_mean"] if stats and stats["n"] > 0 else 0)
        offset = (i - 0.5) * w
        bars = ax.bar(x + offset, means, w, label=approach_labels[approach],
                      color=[_model_color(m) for m in models], alpha=0.6 + 0.3 * i,
                      edgecolor="white", linewidth=0.5)
        for bar, val in zip(bars, means):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylabel("Mean MQM Score")
    ax.set_title("Cross-Model MQM Comparison")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "cross_model_overview.png", dpi=150)
    plt.close(fig)


def plot_cross_model_by_language(all_data: dict[str, dict]):
    """MQM by language across all models (unstructured only for clarity)."""
    models = sorted(all_data.keys())
    all_langs = set()
    for m in models:
        stats = all_data[m].get("unstructured_stats")
        if stats:
            all_langs |= set(stats["by_lang"].keys())
    langs = sorted(all_langs)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(langs))
    n = len(models)
    w = 0.8 / n

    for i, m in enumerate(models):
        stats = all_data[m].get("unstructured_stats")
        means = [stats["by_lang"].get(l, 0) if stats else 0 for l in langs]
        offset = (i - (n - 1) / 2) * w
        ax.bar(x + offset, means, w, label=m, color=_model_color(m))

    ax.set_xticks(x)
    ax.set_xticklabels(langs)
    ax.set_ylabel("Mean MQM Score")
    ax.set_title("MQM by Language (Unstructured) — All Models")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "cross_model_by_language.png", dpi=150)
    plt.close(fig)


def plot_cross_model_by_figure_type(all_data: dict[str, dict]):
    """MQM by figure type across all models (unstructured)."""
    models = sorted(all_data.keys())
    all_types = set()
    for m in models:
        stats = all_data[m].get("unstructured_stats")
        if stats:
            all_types |= set(stats["by_type"].keys())
    types = sorted(all_types)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(types))
    n = len(models)
    w = 0.8 / n

    for i, m in enumerate(models):
        stats = all_data[m].get("unstructured_stats")
        means = [stats["by_type"].get(t, 0) if stats else 0 for t in types]
        offset = (i - (n - 1) / 2) * w
        ax.bar(x + offset, means, w, label=m, color=_model_color(m))

    ax.set_xticks(x)
    ax.set_xticklabels(types, fontsize=9)
    ax.set_ylabel("Mean MQM Score")
    ax.set_title("MQM by Figure Type (Unstructured) — All Models")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "cross_model_by_figure_type.png", dpi=150)
    plt.close(fig)


def plot_score_distribution_all(all_data: dict[str, dict]):
    """Overlayed histogram of MQM scores for all models (unstructured)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    bins = range(40, 101, 5)
    for m in sorted(all_data.keys()):
        results = all_data[m].get("unstructured", [])
        scores = [r["mqm_score"] for r in results]
        if scores:
            ax.hist(scores, bins=bins, alpha=0.5, label=m, color=_model_color(m), edgecolor="white")
    ax.set_xlabel("MQM Score")
    ax.set_ylabel("Count")
    ax.set_title("MQM Score Distribution (Unstructured) — All Models")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "cross_model_score_distribution.png", dpi=150)
    plt.close(fig)


def plot_per_model_comparison(model: str, unstruct: list[dict], struct: list[dict]):
    """Bar chart comparing MQM scores per figure for one model (single-language only)."""
    u_scores = {r["figure_key"]: r["mqm_score"] for r in unstruct if not r["is_multi"]}
    s_scores = {r["figure_key"]: r["mqm_score"] for r in struct if not r["is_multi"]}
    keys = sorted(set(u_scores) & set(s_scores))
    if not keys:
        return

    fig, ax = plt.subplots(figsize=(14, 5))
    x = range(len(keys))
    w = 0.35
    ax.bar([i - w/2 for i in x], [u_scores[k] for k in keys], w, label="Unstructured", color="#4C72B0")
    ax.bar([i + w/2 for i in x], [s_scores[k] for k in keys], w, label="Structured", color="#DD8452")
    ax.set_xticks(list(x))
    ax.set_xticklabels([k.replace("_fig_", "\n") for k in keys], fontsize=7, rotation=45, ha="right")
    ax.set_ylabel("MQM Score (100 = perfect)")
    ax.set_title(f"MQM Scores: {model} — Unstructured vs Structured")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / f"mqm_comparison_{model.replace('.', '_')}.png", dpi=150)
    plt.close(fig)


def plot_error_distribution(model: str, u_stats: dict, s_stats: dict):
    """Stacked bar chart of error categories for both approaches."""
    cats = ["Accuracy", "Completeness", "Clarity and Readability"]
    sevs = ["Major", "Minor"]
    colors = {"Major": "#C44E52", "Minor": "#CCB974"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, stats, title in [(axes[0], u_stats, "Unstructured"), (axes[1], s_stats, "Structured")]:
        bottoms = [0] * len(cats)
        for sev in sevs:
            vals = [stats["cat_sev_counter"].get((c, sev), 0) for c in cats]
            ax.bar(cats, vals, bottom=bottoms, label=sev, color=colors[sev])
            bottoms = [b + v for b, v in zip(bottoms, vals)]
        ax.set_title(title)
        ax.set_ylabel("Error Count")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        ax.set_xticklabels(["Accuracy", "Completeness", "Clarity &\nReadability"], fontsize=9)

    fig.suptitle(f"Error Distribution — {model}", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / f"error_distribution_{model.replace('.', '_')}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── Markdown ──────────────────────────────────────────────────────────

def generate_markdown(all_data: dict[str, dict]) -> str:
    models = sorted(all_data.keys())
    lines = []
    lines.append("# Evaluation Summary — Multi-Model Comparison")
    lines.append("")
    n_figs = 50  # 10 per folder × 5 folders
    lines.append(f"> MQM-based evaluation of {len(models)} models on {n_figs} sample figures")
    lines.append(f"> Models: {', '.join(f'**{m}**' for m in models)}")
    lines.append("> ")
    lines.append("> - **Unstructured**: paragraph-only descriptions")
    lines.append("> - **Structured**: paragraph + component breakdown (paragraph MQM for fair comparison)")
    lines.append("")

    # ── Cross-Model Overview
    lines.append("## Cross-Model Overview")
    lines.append("")
    lines.append("![Cross-Model Overview](eval_plots/cross_model_overview.png)")
    lines.append("")

    # Summary table
    header = "| Metric |" + " | ".join(f"{m} (U) | {m} (S)" for m in models) + " |"
    sep = "|---|" + " | ".join(["---", "---"] * len(models)) + " |"
    lines.append(header)
    lines.append(sep.replace(" | ", "---|").replace("|---|", "|---").rstrip(" |") + "|")

    # Build a cleaner separator
    cols = 1 + len(models) * 2
    lines[-1] = "|" + "---|" * cols

    metrics = [
        ("Evaluations", "n", "{}", False),
        ("MQM Mean", "mqm_mean", "{:.1f}", False),
        ("MQM Median", "mqm_median", "{:.1f}", False),
        ("MQM Std Dev", "mqm_stdev", "{:.1f}", False),
        ("MQM Min", "mqm_min", "{:.1f}", False),
        ("MQM Max", "mqm_max", "{:.1f}", False),
        ("Avg Errors/Fig", "errors_mean", "{:.1f}", False),
        ("Total Errors", "errors_total", "{}", False),
        ("Avg Penalty", "penalty_mean", "{:.1f}", False),
    ]

    for label, key, fmt, struct_only in metrics:
        row = f"| {label} |"
        for m in models:
            u_stats = all_data[m].get("unstructured_stats", {})
            s_stats = all_data[m].get("structured_stats", {})
            u_val = fmt.format(u_stats[key]) if u_stats and key in u_stats else "—"
            s_val = fmt.format(s_stats[key]) if s_stats and key in s_stats else "—"
            row += f" {u_val} | {s_val} |"
        lines.append(row)
    lines.append("")

    # ── Cross-model plots
    lines.append("## MQM by Language — All Models")
    lines.append("")
    lines.append("![Cross-Model by Language](eval_plots/cross_model_by_language.png)")
    lines.append("")

    # Language comparison table
    all_langs = set()
    for m in models:
        u_stats = all_data[m].get("unstructured_stats")
        if u_stats:
            all_langs |= set(u_stats["by_lang"].keys())
    langs = sorted(all_langs)

    header = "| Language |" + " | ".join(models) + " |"
    lines.append(header)
    lines.append("|---|" + "---|" * len(models))
    for lang in langs:
        row = f"| {lang} |"
        for m in models:
            u_stats = all_data[m].get("unstructured_stats")
            val = f"{u_stats['by_lang'][lang]:.1f}" if u_stats and lang in u_stats["by_lang"] else "—"
            row += f" {val} |"
        lines.append(row)
    lines.append("")

    lines.append("## MQM by Figure Type — All Models")
    lines.append("")
    lines.append("![Cross-Model by Figure Type](eval_plots/cross_model_by_figure_type.png)")
    lines.append("")

    # Figure type comparison table
    all_types = set()
    for m in models:
        u_stats = all_data[m].get("unstructured_stats")
        if u_stats:
            all_types |= set(u_stats["by_type"].keys())
    types = sorted(all_types)

    header = "| Figure Type |" + " | ".join(models) + " |"
    lines.append(header)
    lines.append("|---|" + "---|" * len(models))
    for ft in types:
        row = f"| {ft} |"
        for m in models:
            u_stats = all_data[m].get("unstructured_stats")
            val = f"{u_stats['by_type'][ft]:.1f}" if u_stats and ft in u_stats["by_type"] else "—"
            row += f" {val} |"
        lines.append(row)
    lines.append("")

    lines.append("## Score Distribution — All Models")
    lines.append("")
    lines.append("![Score Distribution](eval_plots/cross_model_score_distribution.png)")
    lines.append("")

    # ── Per-Model Detail Sections
    for m in models:
        lines.append(f"---")
        lines.append("")
        lines.append(f"## Model: {m}")
        lines.append("")

        u_stats = all_data[m].get("unstructured_stats")
        s_stats = all_data[m].get("structured_stats")
        unstruct = all_data[m].get("unstructured", [])
        struct = all_data[m].get("structured", [])

        if not u_stats or u_stats["n"] == 0:
            lines.append("*No unstructured evaluation results available.*")
            lines.append("")
            continue

        safe_name = m.replace(".", "_")

        # Per-figure comparison plot
        lines.append(f"### Unstructured vs Structured")
        lines.append("")
        lines.append(f"![{m} Comparison](eval_plots/mqm_comparison_{safe_name}.png)")
        lines.append("")

        # Overview table
        lines.append("| Metric | Unstructured | Structured |")
        lines.append("|---|---|---|")
        lines.append(f"| Evaluations | {u_stats['n']} | {s_stats['n'] if s_stats else '—'} |")
        def _sf(stats, key, fmt=".1f"):
            """Format a stat value or return '—' if stats is None."""
            if not stats:
                return "—"
            return f"{stats[key]:{fmt}}"

        lines.append(f"| MQM Mean | {u_stats['mqm_mean']:.1f} | {_sf(s_stats, 'mqm_mean')} |")
        lines.append(f"| MQM Median | {u_stats['mqm_median']:.1f} | {_sf(s_stats, 'mqm_median')} |")
        lines.append(f"| MQM Std Dev | {u_stats['mqm_stdev']:.1f} | {_sf(s_stats, 'mqm_stdev')} |")
        lines.append(f"| Avg Errors/Figure | {u_stats['errors_mean']:.1f} | {_sf(s_stats, 'errors_mean')} |")
        lines.append(f"| Total Errors | {u_stats['errors_total']} | {s_stats['errors_total'] if s_stats else '—'} |")
        if s_stats and s_stats.get("bv_completeness_mean") is not None:
            lines.append(f"| Breakdown Completeness | — | {s_stats['bv_completeness_mean']*100:.0f}% |")
        if s_stats and s_stats.get("bv_count_consistent_pct") is not None:
            lines.append(f"| Count Consistency | — | {s_stats['bv_count_consistent_pct']:.0f}% |")
        lines.append("")

        # Error distribution plot
        lines.append(f"### Error Distribution")
        lines.append("")
        lines.append(f"![{m} Errors](eval_plots/error_distribution_{safe_name}.png)")
        lines.append("")

        # Error table
        lines.append("| Category | Severity | Unstructured | Structured |")
        lines.append("|---|---|---|---|")
        for cat in ["Accuracy", "Completeness", "Clarity and Readability"]:
            for sev in ["Major", "Minor"]:
                u_val = u_stats["cat_sev_counter"].get((cat, sev), 0)
                s_val = s_stats["cat_sev_counter"].get((cat, sev), 0) if s_stats else "—"
                lines.append(f"| {cat} | {sev} | {u_val} | {s_val} |")
        lines.append("")

    # ── Scoring methodology
    lines.append("---")
    lines.append("")
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
    lines.append(f"- Sample: {n_figs} figures (10 per language folder), {len(models)} models")
    lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────

def main():
    # Auto-discover models
    u_models = discover_models(EVAL_DIR)
    s_models = discover_models(EVAL_STRUCT_DIR)
    all_models = sorted(set(u_models) | set(s_models))

    if not all_models:
        print("No evaluation results found.")
        return

    print(f"Discovered models: {', '.join(all_models)}")

    # Load all data
    all_data: dict[str, dict] = {}
    for model in all_models:
        print(f"\nLoading {model}...")
        unstruct = load_eval_results(EVAL_DIR, model) if model in u_models else []
        struct = load_eval_results(EVAL_STRUCT_DIR, model) if model in s_models else []
        u_stats = compute_stats(unstruct) if unstruct else None
        s_stats = compute_stats(struct) if struct else None
        all_data[model] = {
            "unstructured": unstruct,
            "structured": struct,
            "unstructured_stats": u_stats,
            "structured_stats": s_stats,
        }
        print(f"  Unstructured: {len(unstruct)} evaluations")
        print(f"  Structured:   {len(struct)} evaluations")

    # Generate cross-model plots
    print("\nGenerating cross-model plots...")
    plot_cross_model_overview(all_data)
    print("  + cross_model_overview.png")
    plot_cross_model_by_language(all_data)
    print("  + cross_model_by_language.png")
    plot_cross_model_by_figure_type(all_data)
    print("  + cross_model_by_figure_type.png")
    plot_score_distribution_all(all_data)
    print("  + cross_model_score_distribution.png")

    # Generate per-model plots
    for model in all_models:
        d = all_data[model]
        unstruct = d["unstructured"]
        struct = d["structured"]
        u_stats = d["unstructured_stats"]
        s_stats = d["structured_stats"]

        if unstruct and struct:
            plot_per_model_comparison(model, unstruct, struct)
            print(f"  + mqm_comparison_{model.replace('.', '_')}.png")
        if u_stats and s_stats:
            plot_error_distribution(model, u_stats, s_stats)
            print(f"  + error_distribution_{model.replace('.', '_')}.png")

    # Generate markdown
    print("\nWriting summary markdown...")
    md = generate_markdown(all_data)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"  + {OUTPUT_MD}")

    # Print quick summary
    print("\n=== Quick Summary ===")
    for model in all_models:
        u = all_data[model]["unstructured_stats"]
        s = all_data[model]["structured_stats"]
        u_mqm = f"{u['mqm_mean']:.1f}" if u else "N/A"
        s_mqm = f"{s['mqm_mean']:.1f}" if s else "N/A"
        print(f"  {model}: Unstructured={u_mqm}, Structured={s_mqm}")
    print("Done.")


if __name__ == "__main__":
    main()
