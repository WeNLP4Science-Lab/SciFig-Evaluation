import json
import re
import os
from collections import Counter

MANIFEST_PATH = "/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation/anonymous-submission/dashboard/public/manifest.json"
GT_DIR = "/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation/anonymous-submission/dataset/groundtruth"
OUT_DIR = "/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation/submission-support/groundtruth-audit/bar_chart"

with open(MANIFEST_PATH) as f:
    manifest = json.load(f)

bar_ids = [fig['id'] for fig in manifest if fig.get('figure_type') == 'Bar Chart']
print(f"Found {len(bar_ids)} bar charts")

def get_longest_english_annotation(gt):
    english_anns = [a for a in gt.get('annotations', []) if a.get('annotation_language', '').lower() == 'english']
    if not english_anns:
        english_anns = gt.get('annotations', [])
    if not english_anns:
        return ""
    return max(english_anns, key=lambda a: len(a.get('annotation', '')))['annotation']

def check_purpose(text):
    keywords = r'(compar|present|show|illustrat|depict|display|demonstrat|evaluat|measur|assess|analyz|summariz|report|highlight)'
    if re.search(keywords, text, re.I):
        return "present"
    return "missing"

def check_category_axis(text):
    has_axis_label = bool(re.search(r'(x[- ]?axis|horizontal axis|category axis|categories)', text, re.I))
    has_categories = bool(re.search(r'(categor|label|group|named|x[- ]?axis\s+(show|label|display|represent|is))', text, re.I))
    has_specific = bool(re.search(r'(labeled|labelled|categories\s+(are|include|such as))', text, re.I))
    if has_axis_label or has_categories or has_specific:
        if re.search(r'"[^"]+"|\'[^\']+\'|\b(labeled|labelled)\b.{0,50}("|\'|\w{3,})', text, re.I):
            return "present"
        return "partial"
    return "missing"

def check_value_axis(text):
    has_axis = bool(re.search(r'(y[- ]?axis|vertical axis|value axis)', text, re.I))
    has_scale = bool(re.search(r'(scale|linear|logarithmic|log scale)', text, re.I))
    has_range = bool(re.search(r'(rang|from\s+\d|0\s+to\s+\d|\d+\s+to\s+\d)', text, re.I))
    has_units = bool(re.search(r'(percent|%|\$|dollar|unit|count|number|frequency|score|accuracy|ratio)', text, re.I))
    has_ticks = bool(re.search(r'(tick|interval|increment|step|marks?\s+at)', text, re.I))
    score = sum([has_axis, has_scale, has_range, has_units, has_ticks])
    if score >= 3:
        return "present"
    elif score >= 1:
        return "partial"
    return "missing"

def check_bar_descriptions(text):
    has_values = bool(re.search(r'(approx|approximately|about|roughly|around|~)?\s*\d+(\.\d+)?(%|\s*percent)?', text, re.I))
    has_colors = bool(re.search(r'(red|blue|green|yellow|orange|purple|pink|brown|gray|grey|black|white|cyan|magenta|teal|violet|dark|light)', text, re.I))
    has_labels = bool(re.search(r'"[^"]+"|\'[^\']+\'', text))
    value_mentions = len(re.findall(r'\d+(\.\d+)?(%|\s*percent)', text))
    if has_values and has_colors and has_labels and value_mentions >= 2:
        return "present"
    elif has_values and (has_colors or has_labels):
        return "partial"
    elif has_values:
        return "partial"
    return "missing"

def check_grouped_stacked(text, caption=""):
    is_grouped = bool(re.search(r'(group|clustered|side[- ]?by[- ]?side|adjacent)', text, re.I))
    is_stacked = bool(re.search(r'(stack|cumulative|layered)', text, re.I))
    caption_grouped = bool(re.search(r'(group|clustered)', caption, re.I))
    caption_stacked = bool(re.search(r'(stack)', caption, re.I))
    has_multiple_series = bool(re.search(r'(each (group|category|cluster)|per (group|category)|multiple (bar|color)|different color)', text, re.I))
    has_legend_multiple = len(re.findall(r'(represented by|denoted by|shown in|colored|colour)', text, re.I)) >= 2
    if is_grouped or is_stacked:
        return "present"
    elif has_multiple_series or has_legend_multiple or caption_grouped or caption_stacked:
        return "partial"
    return "not_applicable"

def check_legend(text):
    if re.search(r'(legend|color[- ]?(to[- ]?label|mapping|code|key)|key\s+(show|describ|indicat|map))', text, re.I):
        return "present"
    if re.search(r'(represented by|denoted by|indicated by|correspond)', text, re.I):
        return "present"
    color_label_pairs = re.findall(r'(red|blue|green|yellow|orange|purple|pink|brown|gray|grey|black|white|cyan|magenta|teal|violet)\s*[,)]\s*[\w\d]', text, re.I)
    if len(color_label_pairs) >= 2:
        return "present"
    if len(re.findall(r'"[^"]+"[^"]*\(([^)]*(?:red|blue|green|yellow|orange|purple|pink|brown|gray|grey|black|white|cyan|teal|violet)[^)]*)\)', text, re.I)) >= 2:
        return "present"
    return "missing"

def check_sorting(text):
    if re.search(r'(sort|order|descending|ascending|ranked|highest.{0,20}lowest|lowest.{0,20}highest|left.{0,20}right|alphabetic|neither.{0,30}sort|not.{0,30}sort|no.{0,20}(particular|specific).{0,10}order)', text, re.I):
        return "present"
    return "missing"

def check_visual_emphasis(text):
    if re.search(r'(emphasis|bold|highlight|annotat|outline|arrow|callout|mark|underline|border|pattern|stripe|hatch|dashed|dotted|no.{0,20}(additional|special).{0,20}(visual|emphasis|annotation))', text, re.I):
        return "present"
    return "missing"

def check_values_correct(text):
    values = re.findall(r'\d+(\.\d+)?', text)
    if len(values) >= 3:
        return "present"
    elif len(values) >= 1:
        return "partial"
    return "missing"

def check_clarity(text):
    if len(text) < 50:
        return "missing"
    sentences = text.split('.')
    if len(sentences) >= 3 and len(text) > 150:
        return "present"
    return "partial"

def find_issues(text, checklist, fig_id):
    issues = []
    if checklist['purpose'] == 'missing':
        issues.append("No clear statement of chart purpose or what is being compared")
    if checklist['category_axis'] == 'missing':
        issues.append("X-axis / category axis not described")
    elif checklist['category_axis'] == 'partial':
        issues.append("Category axis mentioned but specific category names may be incomplete")
    if checklist['value_axis'] == 'missing':
        issues.append("Y-axis / value axis not described (label, scale, range, units, ticks)")
    elif checklist['value_axis'] == 'partial':
        issues.append("Value axis partially described - missing some of: label, scale type, range, units, tick interval")
    if checklist['bar_descriptions'] == 'missing':
        issues.append("Individual bars not described with labels, colors, and values")
    elif checklist['bar_descriptions'] == 'partial':
        issues.append("Bar descriptions incomplete - missing some of: labels, colors, approximate values")
    if checklist['grouped_stacked'] == 'partial':
        issues.append("Chart appears grouped/stacked but structure not explicitly described")
    if checklist['legend'] == 'missing':
        issues.append("No legend or color-to-label mapping described")
    if checklist['sorting'] == 'missing':
        issues.append("Sorting order of bars not mentioned")
    if checklist['visual_emphasis'] == 'missing':
        issues.append("No mention of visual emphasis (annotations, bold, outlines, patterns) or lack thereof")
    if checklist['values_correct'] == 'missing':
        issues.append("No specific numeric values provided for bars")
    elif checklist['values_correct'] == 'partial':
        issues.append("Very few numeric values provided")
    if checklist['clarity'] == 'missing':
        issues.append("Description too short or unclear")
    elif checklist['clarity'] == 'partial':
        issues.append("Description could be more detailed for full clarity")
    return issues

results = []

for fig_id in bar_ids:
    gt_path = os.path.join(GT_DIR, f"{fig_id}.json")
    if not os.path.exists(gt_path):
        print(f"WARNING: {gt_path} not found")
        results.append({
            "figure_id": fig_id,
            "figure_type": "Bar Chart",
            "checklist": {k: "missing" for k in ["purpose","category_axis","value_axis","bar_descriptions","grouped_stacked","legend","sorting","visual_emphasis","values_correct","clarity"]},
            "issues": ["Ground truth file not found"]
        })
        continue

    with open(gt_path) as f:
        gt = json.load(f)

    text = get_longest_english_annotation(gt)
    caption = gt.get('caption', '')

    if not text:
        results.append({
            "figure_id": fig_id,
            "figure_type": "Bar Chart",
            "checklist": {k: "missing" for k in ["purpose","category_axis","value_axis","bar_descriptions","grouped_stacked","legend","sorting","visual_emphasis","values_correct","clarity"]},
            "issues": ["No English annotation found"]
        })
        continue

    checklist = {
        "purpose": check_purpose(text),
        "category_axis": check_category_axis(text),
        "value_axis": check_value_axis(text),
        "bar_descriptions": check_bar_descriptions(text),
        "grouped_stacked": check_grouped_stacked(text, caption),
        "legend": check_legend(text),
        "sorting": check_sorting(text),
        "visual_emphasis": check_visual_emphasis(text),
        "values_correct": check_values_correct(text),
        "clarity": check_clarity(text),
    }

    issues = find_issues(text, checklist, fig_id)

    results.append({
        "figure_id": fig_id,
        "figure_type": "Bar Chart",
        "checklist": checklist,
        "issues": issues
    })

# Save audit results
with open(os.path.join(OUT_DIR, "audit.json"), 'w') as f:
    json.dump(results, f, indent=2)

# Generate summary
summary_keys = ["purpose","category_axis","value_axis","bar_descriptions","grouped_stacked","legend","sorting","visual_emphasis","values_correct","clarity"]
summary = {"total_figures": len(results), "checklist_summary": {}}

for key in summary_keys:
    counts = {}
    for r in results:
        val = r["checklist"][key]
        counts[val] = counts.get(val, 0) + 1
    summary["checklist_summary"][key] = counts

total_checks = len(results) * len(summary_keys)
present_count = sum(1 for r in results for k in summary_keys if r["checklist"][k] == "present")
missing_count = sum(1 for r in results for k in summary_keys if r["checklist"][k] == "missing")
partial_count = sum(1 for r in results for k in summary_keys if r["checklist"][k] == "partial")
na_count = sum(1 for r in results for k in summary_keys if r["checklist"][k] == "not_applicable")

summary["overall"] = {
    "total_checks": total_checks,
    "present": present_count,
    "missing": missing_count,
    "partial": partial_count,
    "not_applicable": na_count,
    "present_rate": round(present_count / total_checks * 100, 1),
    "missing_rate": round(missing_count / total_checks * 100, 1),
}

issue_counts = [(r["figure_id"], len(r["issues"])) for r in results]
issue_counts.sort(key=lambda x: -x[1])
summary["most_issues"] = issue_counts[:10]

all_issues = [issue for r in results for issue in r["issues"]]
summary["common_issues"] = Counter(all_issues).most_common()

with open(os.path.join(OUT_DIR, "summary.json"), 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Audit complete: {len(results)} figures processed")
print(f"Present: {present_count}/{total_checks} ({round(present_count/total_checks*100,1)}%)")
print(f"Missing: {missing_count}/{total_checks} ({round(missing_count/total_checks*100,1)}%)")
print(f"Partial: {partial_count}/{total_checks} ({round(partial_count/total_checks*100,1)}%)")
print(f"N/A: {na_count}/{total_checks}")
print(f"\nTop issues:")
for issue, count in Counter(all_issues).most_common():
    print(f"  {count}: {issue}")
