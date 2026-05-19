import json
import re
import os

GT_DIR = "/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation/anonymous-submission/dataset/groundtruth"
OUT_DIR = "/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation/submission-support/groundtruth-audit/line_plot"

fig_ids = [f"fig_{i}" for i in range(100, 199)]

def get_longest_english_annotation(annotations):
    english = [a for a in annotations if a.get("annotation_language", "").lower() == "english"]
    if not english:
        english = annotations
    if not english:
        return ""
    return max(english, key=lambda a: len(a.get("annotation", "")))["annotation"]

def has_subplot_indicators(text, gt_data):
    caption = gt_data.get("caption", "").lower()
    text_lower = text.lower()
    indicators = [
        "subplot", "sub-plot", "top plot", "bottom plot", "left plot", "right plot",
        "upper plot", "lower plot", "panel (a)", "panel (b)", "panel a", "panel b",
        "(a)", "(b)", "top panel", "bottom panel", "left panel", "right panel",
        "first plot", "second plot", "top figure", "bottom figure",
        "upper left", "upper right", "lower left", "lower right"
    ]
    for ind in indicators:
        if ind in text_lower or ind in caption:
            return True
    if text_lower.count("x-axis") > 1 or text_lower.count("y-axis") > 1:
        return True
    if text_lower.count("x axis") > 1 or text_lower.count("y axis") > 1:
        return True
    return False

def check_purpose(text):
    t = text.lower()
    purpose_words = ["illustrat", "show", "depict", "present", "display", "compar",
                     "demonstrate", "represent", "plot", "visualiz", "chart"]
    if any(w in t for w in purpose_words):
        if len(text) > 50:
            return "present"
    if len(text) > 100:
        return "partial"
    return "missing"

def check_x_axis(text):
    t = text.lower()
    has_label = any(p in t for p in ["x-axis", "x axis", "horizontal axis", "x label"])
    has_scale = any(p in t for p in ["linear scale", "logarithmic", "log scale", "log-scale"])
    has_tick = any(p in t for p in ["tick", "interval", "increment", "step"])

    x_patterns = [
        r'x[- ]?axis\b.*?(label|rang|from|to|scale|unit|tick|interval|increment)',
        r'horizontal axis\b.*?(label|rang|from|to|scale|unit|tick)',
    ]
    detailed = any(re.search(p, t) for p in x_patterns)

    if has_label and detailed:
        score = 0
        if has_label: score += 1
        if has_scale: score += 1
        if has_tick: score += 1
        if re.search(r'rang|from\s+\d', t): score += 1
        if score >= 3:
            return "present"
        return "partial"
    elif has_label:
        return "partial"
    return "missing"

def check_y_axis(text):
    t = text.lower()
    has_label = any(p in t for p in ["y-axis", "y axis", "vertical axis", "y label"])
    has_scale = any(p in t for p in ["linear scale", "logarithmic", "log scale", "log-scale"])
    has_tick = any(p in t for p in ["tick", "interval", "increment"])

    y_patterns = [
        r'y[- ]?axis\b.*?(label|rang|from|to|scale|unit|tick|interval|increment)',
        r'vertical axis\b.*?(label|rang|from|to|scale|unit|tick)',
    ]
    detailed = any(re.search(p, t) for p in y_patterns)

    if has_label and detailed:
        score = 0
        if has_label: score += 1
        if has_scale: score += 1
        if has_tick: score += 1
        if re.search(r'rang|from\s+\d', t): score += 1
        if score >= 3:
            return "present"
        return "partial"
    elif has_label:
        return "partial"
    return "missing"

def check_line_descriptions(text):
    t = text.lower()
    colors = ["red", "blue", "green", "orange", "purple", "black", "gray", "grey",
              "teal", "cyan", "magenta", "yellow", "pink", "brown", "violet",
              "dark", "light"]
    color_count = sum(1 for c in colors if c in t)
    has_color = color_count >= 1
    has_style = any(s in t for s in ["solid", "dashed", "dotted", "dash-dot", "line style"])
    has_marker = any(m in t for m in ["marker", "circle", "triangle", "square", "diamond", "star", "dot marker", "cross"])

    if has_color and has_style and has_marker:
        return "present"
    elif has_color and (has_style or has_marker):
        return "partial"
    elif has_color:
        return "partial"
    return "missing"

def check_trajectory(text):
    t = text.lower()
    trajectory_words = ["start", "begin", "increas", "decreas", "peak", "decline",
                        "rise", "drop", "fall", "grow", "upward", "downward",
                        "trend", "fluctuat", "stable", "plateau", "converge",
                        "ascend", "descend", "spike", "dip", "climb", "reach"]
    has_trajectory = sum(1 for w in trajectory_words if w in t) >= 2
    has_values = bool(re.search(r'\d+\.?\d*', t))
    has_start_end = ("start" in t or "begin" in t) and ("end" in t or "reach" in t or "final" in t)

    if has_trajectory and has_values and has_start_end:
        return "present"
    elif has_trajectory and has_values:
        return "partial"
    elif has_trajectory:
        return "partial"
    return "missing"

def check_data_points(text):
    t = text.lower()
    value_patterns = [
        r'approximately\s+\d',
        r'about\s+\d',
        r'around\s+\d',
        r'reaching\s+\d',
        r'value\s+of\s+\d',
        r'at\s+\d+\.?\d*\s*(percent|%)?',
        r'\d+\.?\d*\s*(at|for|when)',
    ]
    matches = sum(1 for p in value_patterns if re.search(p, t))
    numbers = re.findall(r'\d+\.?\d*', t)

    if matches >= 2 and len(numbers) >= 4:
        return "present"
    elif matches >= 1 or len(numbers) >= 3:
        return "partial"
    return "missing"

def check_legend(text):
    t = text.lower()
    if any(w in t for w in ["legend", "label", "labeled", "labelled", "color-to-label", "color coding"]):
        return "present"
    if re.search(r'"[^"]+"|\'[^\']+\'', text):
        return "present"
    return "missing"

def check_subplots(text, gt_data):
    if not has_subplot_indicators(text, gt_data):
        return "not_applicable"
    t = text.lower()
    subplot_desc = any(p in t for p in [
        "top plot", "bottom plot", "left plot", "right plot",
        "first plot", "second plot", "panel (a)", "panel (b)",
        "panel a", "panel b", "upper", "lower",
        "top panel", "bottom panel", "subplot"
    ])
    shared_axes = any(p in t for p in ["shared", "same axis", "same x", "same y", "both plot", "both panel"])
    if subplot_desc and shared_axes:
        return "present"
    elif subplot_desc:
        return "partial"
    return "missing"

def check_values_correct(text):
    numbers = re.findall(r'\d+\.?\d*', text)
    if len(numbers) >= 3:
        return "present"
    return "missing"

def check_clarity(text):
    if len(text) < 50:
        return "missing"
    sentences = text.split('.')
    if len(sentences) >= 3 and len(text) > 200:
        return "present"
    return "missing"

def audit_figure(fig_id):
    gt_path = os.path.join(GT_DIR, f"{fig_id}.json")
    if not os.path.exists(gt_path):
        return {
            "figure_id": fig_id,
            "figure_type": "Line Plot",
            "checklist": {k: "missing" for k in ["purpose","x_axis","y_axis","line_descriptions","trajectory","data_points","legend","subplots","values_correct","clarity"]},
            "issues": [f"Groundtruth file not found: {gt_path}"]
        }

    with open(gt_path) as f:
        gt_data = json.load(f)

    annotation = get_longest_english_annotation(gt_data.get("annotations", []))
    if not annotation:
        return {
            "figure_id": fig_id,
            "figure_type": "Line Plot",
            "checklist": {k: "missing" for k in ["purpose","x_axis","y_axis","line_descriptions","trajectory","data_points","legend","subplots","values_correct","clarity"]},
            "issues": ["No English annotation found"]
        }

    subplots_result = check_subplots(annotation, gt_data)

    checklist = {
        "purpose": check_purpose(annotation),
        "x_axis": check_x_axis(annotation),
        "y_axis": check_y_axis(annotation),
        "line_descriptions": check_line_descriptions(annotation),
        "trajectory": check_trajectory(annotation),
        "data_points": check_data_points(annotation),
        "legend": check_legend(annotation),
        "subplots": subplots_result,
        "values_correct": check_values_correct(annotation),
        "clarity": check_clarity(annotation),
    }

    issues = []
    t = annotation.lower()

    if checklist["x_axis"] == "missing":
        issues.append("X-axis label/description not mentioned")
    elif checklist["x_axis"] == "partial":
        missing_parts = []
        if "scale" not in t and "linear" not in t and "log" not in t:
            missing_parts.append("scale type")
        if not re.search(r'rang|from\s+\d', t):
            missing_parts.append("range")
        if "unit" not in t:
            missing_parts.append("units")
        if "tick" not in t and "interval" not in t and "increment" not in t:
            missing_parts.append("tick interval")
        if missing_parts:
            issues.append(f"X-axis missing: {', '.join(missing_parts)}")

    if checklist["y_axis"] == "missing":
        issues.append("Y-axis label/description not mentioned")
    elif checklist["y_axis"] == "partial":
        missing_parts = []
        if "scale" not in t and "linear" not in t and "log" not in t:
            missing_parts.append("scale type")
        if not re.search(r'rang|from\s+\d', t):
            missing_parts.append("range")
        if "unit" not in t:
            missing_parts.append("units")
        if "tick" not in t and "interval" not in t and "increment" not in t:
            missing_parts.append("tick interval")
        if missing_parts:
            issues.append(f"Y-axis missing: {', '.join(missing_parts)}")

    if checklist["line_descriptions"] == "missing":
        issues.append("No line color/style/marker descriptions")
    elif checklist["line_descriptions"] == "partial":
        if "marker" not in t and "circle" not in t and "triangle" not in t and "square" not in t:
            issues.append("Line marker shapes not described")
        if not any(s in t for s in ["solid", "dashed", "dotted"]):
            issues.append("Line styles not described")

    if checklist["trajectory"] == "missing":
        issues.append("No trajectory description (start/end values, peaks, trends)")
    elif checklist["trajectory"] == "partial":
        if "start" not in t and "begin" not in t:
            issues.append("Trajectory missing start value")
        if "end" not in t and "reach" not in t and "final" not in t:
            issues.append("Trajectory missing end value")
        if "peak" not in t and "maximum" not in t:
            issues.append("No peak/maximum mentioned")

    if checklist["data_points"] == "missing":
        issues.append("No specific data point values mentioned")
    elif checklist["data_points"] == "partial":
        issues.append("Few specific data points; more exact values would improve annotation")

    if checklist["legend"] == "missing":
        issues.append("Legend/color-to-label mapping not described")

    if checklist["subplots"] == "missing":
        issues.append("Figure appears to have subplots but they are not described")
    elif checklist["subplots"] == "partial":
        issues.append("Subplots described but shared axes not explicitly noted")

    if checklist["values_correct"] == "missing":
        issues.append("Insufficient numeric values to verify plausibility")

    if checklist["clarity"] == "missing":
        issues.append("Annotation too short or lacks coherent structure")

    if checklist["purpose"] == "missing":
        issues.append("Chart purpose not stated")
    elif checklist["purpose"] == "partial":
        issues.append("Chart purpose vaguely stated")

    return {
        "figure_id": fig_id,
        "figure_type": "Line Plot",
        "checklist": checklist,
        "issues": issues
    }

# Run audit
results = []
for fig_id in fig_ids:
    result = audit_figure(fig_id)
    results.append(result)

# Save audit results
with open(os.path.join(OUT_DIR, "audit.json"), "w") as f:
    json.dump(results, f, indent=2)

# Compute summary
summary = {
    "total_figures": len(results),
    "checklist_counts": {},
    "figures_with_no_issues": 0,
    "figures_with_issues": 0,
    "common_issues": {}
}

checklist_keys = ["purpose", "x_axis", "y_axis", "line_descriptions", "trajectory",
                  "data_points", "legend", "subplots", "values_correct", "clarity"]

for key in checklist_keys:
    counts = {"present": 0, "partial": 0, "missing": 0, "not_applicable": 0}
    for r in results:
        val = r["checklist"][key]
        counts[val] = counts.get(val, 0) + 1
    summary["checklist_counts"][key] = {k: v for k, v in counts.items() if v > 0}

issue_counter = {}
for r in results:
    if len(r["issues"]) == 0:
        summary["figures_with_no_issues"] += 1
    else:
        summary["figures_with_issues"] += 1
    for issue in r["issues"]:
        issue_counter[issue] = issue_counter.get(issue, 0) + 1

summary["common_issues"] = dict(sorted(issue_counter.items(), key=lambda x: -x[1]))

with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("Audit complete!")
print(f"Total figures: {len(results)}")
print(f"Figures with no issues: {summary['figures_with_no_issues']}")
print(f"Figures with issues: {summary['figures_with_issues']}")
print("\nChecklist summary:")
for key in checklist_keys:
    print(f"  {key}: {summary['checklist_counts'][key]}")
print("\nTop issues:")
for issue, count in list(summary['common_issues'].items())[:15]:
    print(f"  [{count}] {issue}")
