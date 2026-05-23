"""MQM checklist items and global constraints per chart type.

The judge assesses each checklist item on two axes:
  coverage:    {status: complete|partial|missing, detail: "..."}
  correctness: {status: correct|partial|wrong|n/a, sub_type: "...", detail: "..."}

The judge also scans for global constraint violations.

A rule-based engine maps judge output to penalties using the PDF weight table:
  Accuracy:                Major=5.0, Minor=2.0
  Completeness:            Major=5.0, Minor=2.0
  Clarity and Readability: Major=2.5, Minor=1.0

Item severity (Major/Minor) caps the maximum error severity for that item.

MQM formula: max(0, 100 - total_penalty * (100 / (num_items * 5)))
  where num_items = len(checklist), global constraint penalties stack on top.

Accuracy sub-types (from PDF §2.1):
  - Incorrect Numerical Value
  - Incorrect Trend Interpretation
  - Incorrect Axis or Legend Interpretation
  - Incorrect Label Mapping

Completeness sub-type (from PDF §2.2):
  - Missing Key Information  (derived automatically from coverage status)
  - Hallucinated Content     (global constraint)

Clarity and Readability sub-types (from PDF §2.3):
  - Ambiguous Description
  - Missing Takeaway
  - Over-Generalization
  - Overly Verbose Description
  - Poor Sentence Structure
"""

WEIGHTS = {
    ("Accuracy", "Major"): 5.0,
    ("Accuracy", "Minor"): 2.0,
    ("Completeness", "Major"): 5.0,
    ("Completeness", "Minor"): 2.0,
    ("Clarity and Readability", "Major"): 2.5,
    ("Clarity and Readability", "Minor"): 1.0,
}

# ── Bar Chart Checklist (14 items) ──
BAR_CHART = [
    {"id": "bar_01", "item": "Chart type correctly identified (bar chart)", "severity": "Major"},
    {"id": "bar_02", "item": "Bar orientation correctly stated (vertical/horizontal)", "severity": "Major"},
    {"id": "bar_03", "item": "Grouping/stacking structure correctly identified (simple/grouped/stacked)", "severity": "Major"},
    {"id": "bar_04", "item": "X-axis label and units correctly described", "severity": "Major"},
    {"id": "bar_05", "item": "X-axis scale type and range correctly described", "severity": "Minor"},
    {"id": "bar_06", "item": "Y-axis label and units correctly described", "severity": "Major"},
    {"id": "bar_07", "item": "Y-axis scale type and range correctly described", "severity": "Minor"},
    {"id": "bar_08", "item": "All categories on the categorical axis mentioned", "severity": "Major"},
    {"id": "bar_09", "item": "All data series identified (for grouped/stacked)", "severity": "Major"},
    {"id": "bar_10", "item": "Legend correctly described (colour/pattern to series mapping)", "severity": "Major"},
    {"id": "bar_11", "item": "Numerical values accurate", "severity": "Major"},
    {"id": "bar_12", "item": "Colour descriptions accurate for bars/series", "severity": "Minor"},
    {"id": "bar_13", "item": "Annotations noted if present (error bars, reference lines, data labels)", "severity": "Minor"},
    {"id": "bar_14", "item": "Chart purpose or title described", "severity": "Minor"},
]

# ── Line Plot Checklist (15 items) ──
LINE_PLOT = [
    {"id": "line_01", "item": "Chart type correctly identified (line plot)", "severity": "Major"},
    {"id": "line_02", "item": "X-axis label and units correctly described", "severity": "Major"},
    {"id": "line_03", "item": "X-axis scale type and range correctly described", "severity": "Minor"},
    {"id": "line_04", "item": "Y-axis label and units correctly described", "severity": "Major"},
    {"id": "line_05", "item": "Y-axis scale type and range correctly described", "severity": "Minor"},
    {"id": "line_06", "item": "All lines/series mentioned", "severity": "Major"},
    {"id": "line_07", "item": "Legend correctly described (colour/style to series mapping)", "severity": "Major"},
    {"id": "line_08", "item": "Colour descriptions accurate for each line", "severity": "Minor"},
    {"id": "line_09", "item": "Line styles correctly described (solid, dashed, dotted)", "severity": "Minor"},
    {"id": "line_10", "item": "Marker shapes correctly described if present", "severity": "Minor"},
    {"id": "line_11", "item": "Numerical values accurate where stated (start/end, peaks, troughs)", "severity": "Major"},
    {"id": "line_12", "item": "Trends correctly described per line (increasing, decreasing, stable)", "severity": "Major"},
    {"id": "line_13", "item": "Crossover/intersection points mentioned if present", "severity": "Minor"},
    {"id": "line_14", "item": "Annotations noted if present (confidence intervals, shaded regions, reference lines)", "severity": "Minor"},
    {"id": "line_15", "item": "Dual y-axes described if present", "severity": "Minor"},
]

# ── Pie Chart Checklist (11 items) ──
PIE_CHART = [
    {"id": "pie_01", "item": "Chart type correctly identified (standard pie, donut, nested)", "severity": "Major"},
    {"id": "pie_02", "item": "Chart purpose or title described", "severity": "Major"},
    {"id": "pie_03", "item": "Total number of slices correctly stated", "severity": "Major"},
    {"id": "pie_04", "item": "All slice labels mentioned", "severity": "Major"},
    {"id": "pie_05", "item": "Slice colours correctly described", "severity": "Minor"},
    {"id": "pie_06", "item": "Slice percentages/values accurate (exact when labeled, +/-5% when estimated for slices >=10%)", "severity": "Major"},
    {"id": "pie_07", "item": "Ordering of slices described (clockwise, by size)", "severity": "Minor"},
    {"id": "pie_08", "item": "Legend correctly described if present (position, mappings)", "severity": "Minor"},
    {"id": "pie_09", "item": "Visual emphasis noted if present (exploded slices, bold labels)", "severity": "Minor"},
    {"id": "pie_10", "item": "Labels-on-slices vs external labels noted", "severity": "Minor"},
    {"id": "pie_11", "item": "Largest and smallest slices identified", "severity": "Minor"},
]

CHECKLISTS = {
    "Bar Chart": BAR_CHART,
    "Line Plot": LINE_PLOT,
    "Pie Chart": PIE_CHART,
}

# ── Binding Definitions ──
# For element-based checklist items, bindings verify per-element correctness.
# If ANY binding mismatch is found, the checklist item becomes a Major error,
# overriding Step 1's result. Bindings do NOT produce separate penalties.

BINDINGS = {
    "Pie Chart": [
        {
            "checklist_id": "pie_06",
            "attribute": "value",
            "instruction": "For each slice label in the reference, extract its percentage/value. Then find the same label in the model description and extract its stated percentage/value. Compare them. List each slice with its reference value and model value.",
        },
        {
            "checklist_id": "pie_05",
            "attribute": "colour",
            "instruction": "For each slice label in the reference, extract its colour. Then find the same label in the model description and extract its stated colour. Apply the colour family mapping rule before comparing. List each slice with its reference colour and model colour.",
        },
    ],
    "Bar Chart": [],   # TODO: define when we work on bar charts
    "Line Plot": [],   # TODO: define when we work on line plots
}


# ── Global Constraints ──
# Mapped to PDF error categories and sub-types.
# Category and severity are fixed. Each violation = one penalty.

GLOBAL_CONSTRAINTS = [
    # Completeness (§2.2)
    {"id": "global_hallucination", "constraint": "No hallucinated elements — fabricated categories, values, data points, or visual elements not present in the figure", "category": "Completeness", "severity": "Major", "sub_type": "Hallucinated Content"},
    {"id": "global_interpretation", "constraint": "No unwanted interpretation — no subjective claims, causal inference, or evaluative language beyond what is shown", "category": "Completeness", "severity": "Minor", "sub_type": "Unwanted Interpretation"},
    # Clarity and Readability (§2.3)
    {"id": "global_ambiguity", "constraint": "No ambiguous descriptions — no vague or unclear references (e.g., 'this increases significantly' without specifying the subject)", "category": "Clarity and Readability", "severity": "Minor", "sub_type": "Ambiguous Description"},
    {"id": "global_overgeneralization", "constraint": "No over-generalization — does not oversimplify or exaggerate visual information (e.g., 'all methods perform similarly' despite visible variation)", "category": "Clarity and Readability", "severity": "Minor", "sub_type": "Over-Generalization"},
    {"id": "global_verbose", "constraint": "Not overly verbose — no unnecessary repetition or excessive detail that does not add informational value", "category": "Clarity and Readability", "severity": "Minor", "sub_type": "Overly Verbose Description"},
    {"id": "global_poor_structure", "constraint": "No poor sentence structure — no grammatical errors or awkward phrasing that reduces readability", "category": "Clarity and Readability", "severity": "Minor", "sub_type": "Poor Sentence Structure"},
    {"id": "global_missing_takeaway", "constraint": "Includes a meaningful takeaway — does not merely list values without describing the overall trend, pattern, or comparison", "category": "Clarity and Readability", "severity": "Minor", "sub_type": "Missing Takeaway"},
]


def get_checklist(figure_type: str) -> list[dict]:
    return CHECKLISTS.get(figure_type, BAR_CHART)


def get_global_constraints() -> list[dict]:
    return GLOBAL_CONSTRAINTS


def get_bindings(figure_type: str) -> list[dict]:
    return BINDINGS.get(figure_type, [])


def compute_penalties(judge_output: dict, checklist: list[dict]) -> list[dict]:
    """Map judge output to penalty list using the PDF weight table.

    Three-step evaluation:
      Step 1 - Checklist: coverage + correctness per item
      Step 2 - Bindings: per-element verification for element-based items
               (overrides Step 1 correctness if mismatches found)
      Step 3 - Global constraints: hallucination, clarity, etc.

    Judge output format:
      checklist: [{id, reasoning, coverage: {status, detail}, correctness: {status, sub_type, detail, text_span}}]
      bindings: [{checklist_id, comparisons: [{label, reference_value, model_value, match: true/false}]}]
      global: [{id, violations: [{text_span, explanation}]}]

    Returns list of penalty dicts.
    """
    penalties = []

    # Build severity cap lookup
    item_severity = {item["id"]: item["severity"] for item in checklist}

    # ── Step 2: Binding overrides ──
    # Check which checklist items have binding mismatches
    binding_overrides = {}  # checklist_id -> {has_mismatch, details}
    for binding in judge_output.get("bindings", []):
        cid = binding.get("checklist_id", "")
        comparisons = binding.get("comparisons", [])
        mismatches = [c for c in comparisons if not c.get("match", True)]
        if mismatches:
            details = "; ".join(
                f"{m['label']}: model={m.get('model_value','')} ref={m.get('reference_value','')}"
                for m in mismatches
            )
            binding_overrides[cid] = {
                "has_mismatch": True,
                "num_mismatches": len(mismatches),
                "num_total": len(comparisons),
                "detail": details,
            }

    # ── Step 1: Checklist item penalties (with binding overrides) ──
    for item in judge_output.get("checklist", []):
        item_id = item["id"]
        cap = item_severity.get(item_id, "Major")

        coverage = item.get("coverage", {})
        correctness = item.get("correctness", {})
        cov_status = coverage.get("status", "complete")
        cor_status = correctness.get("status", "correct")

        # Check if bindings override this item's correctness
        if item_id in binding_overrides:
            override = binding_overrides[item_id]
            # Bindings found mismatches → force Major error on this item
            cor_status = "wrong"
            correctness = {
                "status": "wrong",
                "sub_type": "Incorrect Label Mapping",
                "detail": f"Binding verification: {override['num_mismatches']}/{override['num_total']} elements mismatched. {override['detail']}",
                "text_span": "",
            }

        # Coverage → Completeness errors
        if cov_status == "missing":
            sev = "Major" if cap == "Major" else "Minor"
            penalties.append({
                "id": item_id, "category": "Completeness", "severity": sev,
                "sub_type": "Missing Key Information",
                "weight": WEIGHTS[("Completeness", sev)],
                "source": "checklist_coverage",
                "detail": coverage.get("detail", ""),
            })
        elif cov_status == "partial":
            penalties.append({
                "id": item_id, "category": "Completeness", "severity": "Minor",
                "sub_type": "Missing Key Information",
                "weight": WEIGHTS[("Completeness", "Minor")],
                "source": "checklist_coverage",
                "detail": coverage.get("detail", ""),
            })

        # Correctness → Accuracy errors (only if something is present)
        if cov_status != "missing":
            if cor_status == "wrong":
                sev = "Major" if cap == "Major" else "Minor"
                penalties.append({
                    "id": item_id, "category": "Accuracy", "severity": sev,
                    "sub_type": correctness.get("sub_type", ""),
                    "weight": WEIGHTS[("Accuracy", sev)],
                    "source": "checklist_correctness",
                    "detail": correctness.get("detail", ""),
                    "text_span": correctness.get("text_span", ""),
                })
            elif cor_status == "partial":
                penalties.append({
                    "id": item_id, "category": "Accuracy", "severity": "Minor",
                    "sub_type": correctness.get("sub_type", ""),
                    "weight": WEIGHTS[("Accuracy", "Minor")],
                    "source": "checklist_correctness",
                    "detail": correctness.get("detail", ""),
                    "text_span": correctness.get("text_span", ""),
                })

    # ── Global constraint penalties ──
    constraint_lookup = {c["id"]: c for c in GLOBAL_CONSTRAINTS}
    for gc in judge_output.get("global", []):
        cid = gc.get("id", gc.get("constraint_id", ""))
        constraint = constraint_lookup.get(cid)
        if not constraint:
            continue
        for violation in gc.get("violations", []):
            penalties.append({
                "id": cid, "category": constraint["category"],
                "severity": constraint["severity"],
                "sub_type": constraint["sub_type"],
                "weight": WEIGHTS[(constraint["category"], constraint["severity"])],
                "source": "global",
                "detail": violation.get("explanation", ""),
                "text_span": violation.get("text_span", ""),
            })

    return penalties


def deduplicate_penalties(penalties: list[dict]) -> list[dict]:
    """Remove double-counted penalties.

    Two deduplication rules:
    1. Global constraint violations that share the same text_span (or substantial
       substring overlap) with a checklist correctness penalty are removed — the
       checklist penalty already captures the error.
    2. Multiple checklist items penalised for the same root cause (same text_span)
       keep only the highest-weight penalty — the others are cascading symptoms.

    Returns the deduplicated penalty list.
    """
    # Collect checklist text_spans
    checklist_spans = set()
    for p in penalties:
        if p["source"].startswith("checklist") and p.get("text_span"):
            checklist_spans.add(p["text_span"].strip().lower())

    deduped = []
    seen_spans = {}  # text_span -> highest weight penalty

    for p in penalties:
        span = (p.get("text_span") or "").strip().lower()

        # Rule 1: drop global penalties that overlap with checklist spans
        if p["source"] == "global" and span:
            if span in checklist_spans:
                continue
            # Also check substring overlap
            overlap = False
            for cs in checklist_spans:
                if cs and (span in cs or cs in span):
                    overlap = True
                    break
            if overlap:
                continue

        # Rule 2: for checklist correctness with overlapping text_span, keep highest weight
        if p["source"] == "checklist_correctness" and span:
            # Check exact match or substring overlap with any seen span
            matched_key = None
            for seen_span in seen_spans:
                if seen_span and span and (span in seen_span or seen_span in span):
                    matched_key = seen_span
                    break

            if matched_key is not None:
                if p["weight"] > seen_spans[matched_key]["weight"]:
                    # Replace with higher weight
                    old_span = matched_key
                    deduped = [x for x in deduped if not (
                        x["source"] == "checklist_correctness"
                        and (x.get("text_span") or "").strip().lower() == old_span
                    )]
                    deduped.append(p)
                    seen_spans[span] = p
                    del seen_spans[matched_key]
                # else skip — lower weight duplicate
                continue
            seen_spans[span] = p

        deduped.append(p)

    return deduped


def compute_max_penalty(checklist: list[dict]) -> float:
    """Compute max possible penalty for a checklist.

    Each item can produce at most one penalty at its severity cap:
      Major item → max(Accuracy/Major, Completeness/Major) = 5.0
      Minor item → max(Accuracy/Minor, Completeness/Minor) = 2.0
    """
    total = 0.0
    for item in checklist:
        if item["severity"] == "Major":
            total += 5.0  # max of Accuracy/Major and Completeness/Major
        else:
            total += 2.0  # max of Accuracy/Minor and Completeness/Minor
    return total


def compute_mqm(penalties: list[dict], checklist: list[dict]) -> float:
    """Compute MQM score from penalty list.

    Formula: max(0, 100 - total_penalty * (100 / max_possible_penalty))
    where max_possible_penalty is derived from checklist item severities.
    Global constraint penalties stack on top and can push below 0 (clamped).
    """
    total_penalty = sum(p["weight"] for p in penalties)
    max_penalty = compute_max_penalty(checklist)
    if max_penalty == 0:
        return 100.0
    return max(0.0, 100.0 - total_penalty * (100.0 / max_penalty))
