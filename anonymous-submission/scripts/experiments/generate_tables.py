"""Generate LaTeX tables from computed statistics.

Reads all_statistics.json and collected_results.json, produces .tex files
for all main paper and appendix tables.

Output: paper/tables/*.tex

Usage:
    python generate_tables.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import RESULTS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

STATS_DIR = RESULTS_DIR / "statistics"
TABLES_DIR = Path(__file__).resolve().parents[2] / "paper" / "tables"

MODEL_SHORT = {
    "gpt-5.2": "GPT-5.2",
    "gemini-3.1-pro": "Gemini",
    "llama4-maverick": "Llama 4",
    "qwen3-vl-235b-a22b": "Qwen-235B",
    "qwen3-vl-30b-a3b": "Qwen-30B",
    "qwen3-vl-8b": "Qwen-8B",
    "gemma3-27b-it": "Gemma",
    "phi-4-multimodal": "Phi-4",
}

MODEL_ORDER = [
    "gpt-5.2", "gemini-3.1-pro", "llama4-maverick",
    "qwen3-vl-235b-a22b", "qwen3-vl-8b", "qwen3-vl-30b-a3b",
    "gemma3-27b-it", "phi-4-multimodal",
]


def fmt_ci(stat, decimals=1, pct=False):
    """Format a bootstrap CI stat as 'mean_{lo}^{hi}'."""
    if not stat or stat.get("mean") is None:
        return "--"
    m = stat["mean"]
    lo = stat["ci_lower"]
    hi = stat["ci_upper"]
    if pct:
        m, lo, hi = m * 100, lo * 100, hi * 100
    if decimals == 0:
        return f"{m:.0f}$_{{\\scriptstyle {lo:.0f}}}^{{\\scriptstyle {hi:.0f}}}$"
    elif decimals == 1:
        return f"{m:.1f}$_{{\\scriptstyle {lo:.1f}}}^{{\\scriptstyle {hi:.1f}}}$"
    else:
        return f"{m:.2f}$_{{\\scriptstyle {lo:.2f}}}^{{\\scriptstyle {hi:.2f}}}$"


def fmt_mean(stat, decimals=1, pct=False):
    """Format just the mean."""
    if not stat or stat.get("mean") is None:
        return "--"
    m = stat["mean"]
    if pct:
        m = m * 100
    if decimals == 0:
        return f"{m:.0f}"
    elif decimals == 1:
        return f"{m:.1f}"
    else:
        return f"{m:.2f}"


def bold_best(values, model_keys, higher_better=True):
    """Return dict mapping model -> formatted value with bold for best, underline for 2nd."""
    means = {}
    for m in model_keys:
        v = values.get(m)
        if v and v.get("mean") is not None:
            means[m] = v["mean"]

    if not means:
        return {m: "--" for m in model_keys}

    sorted_models = sorted(means, key=means.get, reverse=higher_better)
    best = sorted_models[0] if sorted_models else None
    second = sorted_models[1] if len(sorted_models) > 1 else None

    result = {}
    for m in model_keys:
        val = values.get(m)
        formatted = fmt_ci(val)
        if m == best:
            formatted = f"\\textbf{{{formatted}}}"
        elif m == second:
            formatted = f"\\underline{{{formatted}}}"
        result[m] = formatted
    return result


def generate_table3(stats, collected):
    """Table 3: Description Quality (MQM scores across conditions)."""
    logger.info("Generating Table 3: Description Quality")

    cis = stats["bootstrap_cis"]
    transforms = ["original", "noise", "rotation", "low_contrast", "in_paper", "in_paper_blur", "caption_bias", "admittance_blur", "inductance_blur"]
    transform_labels = {
        "original": "Orig.",
        "noise": "Noise",
        "rotation": "Rot.",
        "low_contrast": "LowC",
        "in_paper": "InPap",
        "in_paper_blur": "IPBlr",
        "caption_bias": "CapB",
        "admittance_blur": "AdmB",
        "inductance_blur": "IndB",
    }

    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}l" + "r" * (1 + len(transforms)) + "@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Base} & " + " & ".join(f"\\textbf{{{transform_labels[t]}}}" for t in transforms) + " \\\\",
        "\\midrule",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]
        base = cis["baseline_mqm"].get(model, {})
        base_str = fmt_ci(base)

        cells = [base_str]
        for t in transforms:
            t_stat = cis["transform_mqm"].get(t, {}).get(model, {})
            cells.append(fmt_ci(t_stat))

        lines.append(f"{short} & " + " & ".join(cells) + " \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Description quality (MQM scores, 0--100) across conditions. Base = baseline with caption (250 figures). "
        "Transforms evaluated on 100-figure subset. Values show mean with 95\\% bootstrap CI (subscript/superscript). "
        "Higher is better.}",
        "\\label{tab:mqm-results}",
        "\\end{table*}",
    ]

    return "\n".join(lines)


def generate_table4(stats):
    """Table 4: Behavioral Evaluation."""
    logger.info("Generating Table 4: Behavioral Evaluation")

    cis = stats["bootstrap_cis"]

    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}l rrr r rr rr@{}}",
        "\\toprule",
        "& \\multicolumn{3}{c}{\\textbf{Resistance}} & \\textbf{Cap.} & \\multicolumn{2}{c}{\\textbf{Active}} & \\multicolumn{2}{c}{\\textbf{Passive}} \\\\",
        "\\cmidrule(lr){2-4} \\cmidrule(lr){5-5} \\cmidrule(lr){6-7} \\cmidrule(lr){8-9}",
        "\\textbf{Model} & \\textbf{Inex.} & \\textbf{Cont.} & \\textbf{Unans.} & \\textbf{Bias R} & \\textbf{Adm.} & \\textbf{Ind.\\textsuperscript{C}} & \\textbf{Adm.} & \\textbf{Ind.\\textsuperscript{C}} \\\\",
        "\\midrule",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]

        # Resistance by type
        r_by_type = cis.get("resistance_by_type", {}).get(model, {})
        inexist = fmt_ci(r_by_type.get("inexist", {}), 2)
        contra = fmt_ci(r_by_type.get("contra", {}), 2)
        unanswerable = fmt_ci(r_by_type.get("unanswerable", {}), 2)

        # Caption bias
        cb = fmt_ci(cis.get("caption_bias", {}).get(model, {}), 2)

        # Active probes
        act_adm = cis.get("active_probes", {}).get("admittance", {}).get(model, {})
        act_adm_str = fmt_ci(act_adm.get("admits", {}), 0, pct=True) if act_adm else "--"

        act_ind = cis.get("active_probes", {}).get("inductance", {}).get(model, {})
        act_ind_str = fmt_ci(act_ind.get("correct_given_fab", {}), 0, pct=True) if act_ind else "--"

        # Passive probes
        pas_adm = cis.get("passive_probes", {}).get("admittance", {}).get(model, {})
        pas_adm_str = fmt_ci(pas_adm.get("admits", {}), 0, pct=True) if pas_adm else "--"

        pas_ind = cis.get("passive_probes", {}).get("inductance", {}).get(model, {})
        pas_ind_str = fmt_ci(pas_ind.get("correct_given_fab", {}), 0, pct=True) if pas_ind else "--"

        lines.append(f"{short} & {inexist} & {contra} & {unanswerable} & {cb} & {act_adm_str} & {act_ind_str} & {pas_adm_str} & {pas_ind_str} \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Behavioral evaluation across A-R-I dimensions. Resistance scores (0--1, higher = more resistant) broken down by probe type. "
        "Cap. Bias R = caption bias resistance. Active/Passive Adm. = admittance rate (\\% admitting visual limitation). "
        "Ind.\\textsuperscript{C} = inductance correctness (\\% of fabricated answers that are correct). "
        "Values show mean with 95\\% bootstrap CI.}",
        "\\label{tab:behavioral}",
        "\\end{table*}",
    ]

    return "\n".join(lines)


def generate_table_a1(stats):
    """Appendix A1: Per chart type MQM breakdown."""
    logger.info("Generating Table A1: Per Chart Type MQM")

    cis = stats["bootstrap_cis"]
    chart_types = ["Bar Chart", "Line Plot", "Pie Chart"]
    ct_short = {"Bar Chart": "Bar", "Line Plot": "Line", "Pie Chart": "Pie"}

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrr@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Bar} & \\textbf{Line} & \\textbf{Pie} \\\\",
        "\\midrule",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]
        by_ct = cis.get("baseline_mqm_by_chart", {}).get(model, {})
        cells = []
        for ct in chart_types:
            cells.append(fmt_ci(by_ct.get(ct, {})))
        lines.append(f"{short} & " + " & ".join(cells) + " \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Baseline MQM scores by chart type with 95\\% bootstrap CI.}",
        "\\label{tab:mqm-chart-type}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a2(stats, collected):
    """Appendix A2: Per MQM dimension penalty breakdown."""
    logger.info("Generating Table A2: Per MQM Dimension")

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrr@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Accuracy} & \\textbf{Compl.} & \\textbf{Clarity} \\\\",
        "\\midrule",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]
        dims = stats["bootstrap_cis"].get("baseline_mqm_dimensions", {}).get(model, {})
        acc = fmt_ci(dims.get("penalty_accuracy", {}), 2)
        comp = fmt_ci(dims.get("penalty_completeness", {}), 2)
        clar = fmt_ci(dims.get("penalty_clarity", {}), 2)
        lines.append(f"{short} & {acc} & {comp} & {clar} \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Mean penalty per MQM dimension (lower = fewer errors). "
        "Accuracy and Completeness weighted equally (Major=5.0, Minor=2.0). "
        "Clarity weighted lower (Major=2.5, Minor=1.0).}",
        "\\label{tab:mqm-dimensions}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a3(collected):
    """Appendix A3: Most common error sub-types."""
    logger.info("Generating Table A3: Error Sub-Types")

    from collections import Counter
    error_counts = Counter()
    model_errors = {}

    for model, entries in collected["baseline_mqm"].items():
        model_counter = Counter()
        for e in entries:
            # Need to re-read full files for penalty details
            pass
        model_errors[model] = model_counter

    # For now generate a placeholder since collected_results may not have sub_type detail
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lr@{}}",
        "\\toprule",
        "\\textbf{Error Sub-Type} & \\textbf{Count} \\\\",
        "\\midrule",
        "% TODO: Populate from detailed penalty analysis \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Most common MQM error sub-types across all models and figures.}",
        "\\label{tab:error-subtypes}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a4(stats):
    """Appendix A4: Caption bias by modification type."""
    logger.info("Generating Table A4: Caption Bias by Type")

    cb_by_type = stats["bootstrap_cis"].get("caption_bias_by_type", {})

    # Get all modification types
    all_types = set()
    for model_data in cb_by_type.values():
        all_types.update(model_data.keys())
    all_types = sorted(all_types)

    if not all_types:
        return "% Table A4: No caption bias type data available"

    type_short = {
        "value_anchor": "Val. Anch.",
        "trend_characterization": "Trend",
        "comparison_swap": "Comp. Swap",
        "ranking_inversion": "Rank Inv.",
        "rate_mischaracterization": "Rate Mis.",
    }

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}l" + "r" * len(all_types) + "@{}}",
        "\\toprule",
        "\\textbf{Model} & " + " & ".join(f"\\textbf{{{type_short.get(t, t[:8])}}}" for t in all_types) + " \\\\",
        "\\midrule",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]
        model_data = cb_by_type.get(model, {})
        cells = []
        for t in all_types:
            cells.append(fmt_ci(model_data.get(t, {}), 2))
        lines.append(f"{short} & " + " & ".join(cells) + " \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Caption bias resistance by modification type. Higher = model resisted the false claim.}",
        "\\label{tab:caption-bias-type}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a5(stats):
    """Appendix A5: Pairwise significance tests."""
    logger.info("Generating Table A5: Significance Tests")

    sig = stats["significance"]

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrr@{}}",
        "\\toprule",
        "\\textbf{Comparison} & \\textbf{Diff} & \\textbf{$p$} & \\textbf{Sig.} \\\\",
        "\\midrule",
        "\\multicolumn{4}{@{}l}{\\emph{Baseline MQM (vs best)}} \\\\",
    ]

    for pair, result in sorted(sig.get("baseline_mqm", {}).items()):
        marker = "***" if result["significant_001"] else "**" if result["significant_01"] else "*" if result["significant_05"] else "n.s."
        lines.append(f"\\quad {pair.replace('_', ' ')} & {result['diff']:.1f} & {result['p_value']:.3f} & {marker} \\\\")

    lines.append("\\midrule")
    lines.append("\\multicolumn{4}{@{}l}{\\emph{Resistance (vs best)}} \\\\")

    for pair, result in sorted(sig.get("resistance", {}).items()):
        marker = "***" if result["significant_001"] else "**" if result["significant_01"] else "*" if result["significant_05"] else "n.s."
        lines.append(f"\\quad {pair.replace('_', ' ')} & {result['diff']:.2f} & {result['p_value']:.3f} & {marker} \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Paired bootstrap significance tests ($B$=10,000). Each model compared against the best. "
        "* $p<.05$, ** $p<.01$, *** $p<.001$.}",
        "\\label{tab:significance}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a6(stats):
    """Appendix A6: Ablation results."""
    logger.info("Generating Table A6: Ablation")

    abl = stats.get("ablation", {})

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrrr@{}}",
        "\\toprule",
        "\\textbf{Metric} & \\textbf{GPT-4o} & \\textbf{Mistral} & \\textbf{$\\Delta$} & \\textbf{$p$} \\\\",
        "\\midrule",
    ]

    for key, label in [("resistance_probe_designer", "Resistance"), ("caption_bias_probe_designer", "Caption Bias")]:
        if key in abl:
            d = abl[key]
            g = fmt_ci(d.get("gpt4o", {}), 2)
            m = fmt_ci(d.get("mistral", {}), 2)
            pt = d.get("paired_test", {})
            diff = f"{pt.get('diff', 0):.3f}" if pt.get("diff") is not None else "--"
            p_val = f"{pt.get('p_value', 1):.3f}" if pt.get("p_value") is not None else "--"
            lines.append(f"{label} & {g} & {m} & {diff} & {p_val} \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Probe designer ablation. GPT-4o vs Mistral Large 3 as probe generators, "
        "GPT-5.2 as test model, GPT-4o as judge. Values show mean with 95\\% bootstrap CI.}",
        "\\label{tab:ablation}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a7(stats):
    """Appendix A7: Stability analysis."""
    logger.info("Generating Table A7: Stability")

    stab = stats.get("stability", {})

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lr@{}}",
        "\\toprule",
        "\\textbf{Stability Measure} & \\textbf{Value} \\\\",
        "\\midrule",
    ]

    sh = stab.get("split_half_mqm", {})
    if sh:
        lines.append(f"Split-half reliability ($\\rho$) & {sh['mean_rho']:.3f} [{sh['ci_lower']:.3f}, {sh['ci_upper']:.3f}] \\\\")

    strat = stab.get("stratified_rho", {})
    for pair, rho in sorted(strat.items()):
        lines.append(f"Stratified $\\rho$ ({pair.replace('_vs_', ' vs ')}) & {rho:.3f} \\\\")

    sv = stab.get("scale_validation", {})
    if sv:
        lines.append("\\midrule")
        lines.append("\\multicolumn{2}{@{}l}{\\emph{Scale validation (100 vs 250 figures)}} \\\\")
        for model in MODEL_ORDER:
            if model in sv:
                d = sv[model]
                lines.append(f"\\quad {MODEL_SHORT[model]} & {d['mean_100']:.2f} $\\rightarrow$ {d['mean_250']:.2f} \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Stability analysis. Split-half reliability computed over 100 random splits. "
        "Stratified $\\rho$ shows rank correlation between chart types. "
        "Scale validation compares resistance scores on 100 vs 250 figures.}",
        "\\label{tab:stability}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a8(stats):
    """Appendix A8: Resistance by chart type."""
    logger.info("Generating Table A8: Resistance by Chart Type")

    # Need per-chart-type resistance from collected data
    # For now placeholder
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrr@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Bar} & \\textbf{Line} & \\textbf{Pie} \\\\",
        "\\midrule",
        "% TODO: Compute per-chart-type resistance scores \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Hallucination resistance scores by chart type.}",
        "\\label{tab:resistance-chart-type}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_a9(stats):
    """Appendix A9: Cross-dimensional correlations."""
    logger.info("Generating Table A9: Cross-Dimensional Correlations")

    cis = stats["bootstrap_cis"]

    # Compute rank correlations between dimensions
    dims = {
        "MQM": {},
        "Resistance": {},
        "Caption Bias": {},
        "Admittance (Active)": {},
        "Inductance (Active)": {},
    }

    for model in MODEL_ORDER:
        mqm = cis.get("baseline_mqm", {}).get(model, {})
        if mqm.get("mean") is not None:
            dims["MQM"][model] = mqm["mean"]

        res = cis.get("resistance", {}).get(model, {})
        if res.get("mean") is not None:
            dims["Resistance"][model] = res["mean"]

        cb = cis.get("caption_bias", {}).get(model, {})
        if cb.get("mean") is not None:
            dims["Caption Bias"][model] = cb["mean"]

        act_adm = cis.get("active_probes", {}).get("admittance", {}).get(model, {})
        if act_adm:
            admits = act_adm.get("admits", {})
            if admits.get("mean") is not None:
                dims["Admittance (Active)"][model] = admits["mean"]

        act_ind = cis.get("active_probes", {}).get("inductance", {}).get(model, {})
        if act_ind:
            correct = act_ind.get("correct_given_fab", {})
            if correct.get("mean") is not None:
                dims["Inductance (Active)"][model] = correct["mean"]

    dim_names = list(dims.keys())

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}l" + "r" * len(dim_names) + "@{}}",
        "\\toprule",
        "& " + " & ".join(f"\\textbf{{{n[:6]}}}" for n in dim_names) + " \\\\",
        "\\midrule",
    ]

    for i, d1_name in enumerate(dim_names):
        cells = []
        for j, d2_name in enumerate(dim_names):
            if i == j:
                cells.append("--")
            elif i < j:
                common = sorted(set(dims[d1_name]) & set(dims[d2_name]))
                if len(common) >= 4:
                    from itertools import combinations as _c
                    vals1 = [dims[d1_name][m] for m in common]
                    vals2 = [dims[d2_name][m] for m in common]
                    ranks1 = sorted(range(len(common)), key=lambda k: vals1[k], reverse=True)
                    ranks2 = sorted(range(len(common)), key=lambda k: vals2[k], reverse=True)
                    r1 = [0] * len(common)
                    r2 = [0] * len(common)
                    for rank, idx in enumerate(ranks1):
                        r1[idx] = rank + 1
                    for rank, idx in enumerate(ranks2):
                        r2[idx] = rank + 1
                    n = len(common)
                    d_sq = sum((a - b) ** 2 for a, b in zip(r1, r2))
                    rho = 1 - (6 * d_sq) / (n * (n ** 2 - 1))
                    cells.append(f"{rho:.2f}")
                else:
                    cells.append("--")
            else:
                cells.append("")
        lines.append(f"{d1_name} & " + " & ".join(cells) + " \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Spearman rank correlations between evaluation dimensions ($n$=8 models). "
        "Values below 0.70 suggest the dimensions capture distinct aspects of model competence.}",
        "\\label{tab:cross-dim}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def generate_table_capability():
    """Placeholder table for capability questions."""
    logger.info("Generating Table: Capability Questions (placeholder)")

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{@{}lrrrr@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Count} & \\textbf{Comp.} & \\textbf{Compar.} & \\textbf{Pattern} \\\\",
        "\\midrule",
        "% TODO: Fill with capability question results \\\\",
    ]

    for model in MODEL_ORDER:
        short = MODEL_SHORT[model]
        lines.append(f"{short} & -- & -- & -- & -- \\\\")

    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Capability question accuracy by category (counting, computation, comparison, pattern analysis). "
        "250 figures, 4 questions each.}",
        "\\label{tab:capability}",
        "\\end{table}",
    ]

    return "\n".join(lines)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    with open(STATS_DIR / "all_statistics.json") as f:
        stats = json.load(f)
    with open(STATS_DIR / "collected_results.json") as f:
        collected = json.load(f)

    tables = {
        "table3_description_quality.tex": generate_table3(stats, collected),
        "table4_behavioral.tex": generate_table4(stats),
        "table_a1_chart_type_mqm.tex": generate_table_a1(stats),
        "table_a2_mqm_dimensions.tex": generate_table_a2(stats, collected),
        "table_a3_error_subtypes.tex": generate_table_a3(collected),
        "table_a4_caption_bias_type.tex": generate_table_a4(stats),
        "table_a5_significance.tex": generate_table_a5(stats),
        "table_a6_ablation.tex": generate_table_a6(stats),
        "table_a7_stability.tex": generate_table_a7(stats),
        "table_a8_resistance_chart_type.tex": generate_table_a8(stats),
        "table_a9_cross_dimensional.tex": generate_table_a9(stats),
        "table_capability_placeholder.tex": generate_capability_placeholder(),
    }

    for filename, content in tables.items():
        path = TABLES_DIR / filename
        with open(path, "w") as f:
            f.write(content)
        logger.info(f"  Written: {path}")

    logger.info(f"\n{len(tables)} tables generated in {TABLES_DIR}")


def generate_capability_placeholder():
    return generate_table_capability()


if __name__ == "__main__":
    main()
