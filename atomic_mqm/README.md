# Atomic MQM — Checklist-Based Figure Description Evaluation

## Problem
The current MQM evaluation asks a judge to "find errors" in an open-ended way. This leads to:
- Missed completeness errors (judge doesn't flag all missing elements)
- A completely wrong description (wrong figure) can score 61/100
- Inconsistent scoring across figures
- Judge's job is too open-ended — it catches what it notices, not what's actually missing

## Solution
Replace open-ended error finding with a **pre-defined checklist of atomic truths** per figure. The judge verifies each atom independently.

## What is an Atom?
The smallest verifiable claim about a figure. Examples:
- "The x-axis label is 'Number of completions (k)'"
- "The x-axis uses a logarithmic scale"
- "There are 4 lines in the plot"
- "The blue solid line starts at approximately 0.42"

Each atom is verified independently as: **Correct / Inaccurate / Missing / Hallucinated / N/A**

## Atom Categories

### 1. Identity Atoms (all figure types)
- Chart type (line plot, bar chart, pie chart, etc.)
- Chart purpose/title
- Number of subplots/panels

### 2. Axis Atoms (line plots, bar charts)
- Per axis: label, scale type, range, units, tick interval

### 3. Data Element Atoms (type-specific)
- **Line plots**: per line — name, color, style, marker, start value, end value, peaks/valleys
- **Bar charts**: per bar/group — label, color, value
- **Pie charts**: per slice — label, color, percentage/value

### 4. Structural Atoms (all types)
- Grouped vs stacked arrangement
- Sort order (descending, alphabetical, etc.)
- Legend presence and content

### 5. Annotation Atoms (all types)
- Data labels on elements
- Reference lines
- Visual emphasis (bold, exploded, highlighted)
- Text annotations

## Atom Severity Levels
- **Critical**: Chart purpose, axis labels, data series names — defines what the chart IS
- **Important**: Values, ranges, scale types — defines what the chart SHOWS
- **Minor**: Colors, styles, tick intervals — defines how the chart LOOKS

## Templates

### Base Template (shared by all figure types)
```
identity:
  chart_type: <line_plot | bar_chart | pie_chart | other>
  chart_purpose: <string>
  num_subplots: <int>
  title: <string or null>

legend:
  present: <bool>
  entries: [<list of legend items>]

annotations:
  data_labels: <bool>
  reference_lines: [<list>]
  visual_emphasis: [<list>]
```

### Line Plot Extension
```
x_axis:
  label: <string>
  scale_type: <linear | logarithmic | log2 | categorical>
  range: [<min>, <max>]
  units: <string or null>
  tick_interval: <string or null>

y_axis:
  <same structure as x_axis>

lines:
  - name: <string>
    color: <string>
    style: <solid | dashed | dotted | dash-dot>
    marker: <circle | square | triangle | diamond | none>
    start_value: <number>
    end_value: <number>
    key_points: [{ x: <val>, y: <val>, type: <peak | valley | inflection> }]
```

### Bar Chart Extension
```
category_axis:
  orientation: <horizontal | vertical>
  label: <string>
  categories: [<list of category names>]

value_axis:
  label: <string>
  scale_type: <linear | logarithmic>
  range: [<min>, <max>]
  units: <string or null>

structure: <single | grouped | stacked | 100_percent_stacked>
sort_order: <descending | ascending | custom | none>

bars:
  - label: <string>
    color: <string>
    value: <number>
    # For grouped/stacked: sub_bars with same structure
```

### Pie Chart Extension
```
total_slices: <int>

slices:
  - label: <string>
    color: <string>
    value: <number or percentage>
    exploded: <bool>

labels_position: <inside | outside | legend_only>
```

## Scoring

### Per-Atom Score
- **Correct (C)**: Model stated it accurately
- **Inaccurate (I)**: Model mentioned it but got it wrong
- **Missing (M)**: Model didn't mention it at all
- **Hallucinated (H)**: Model added something not in the checklist
- **N/A**: Atom doesn't apply to this figure

### Aggregated Scores
- **Accuracy** = C / (C + I)
- **Completeness** = C / (C + M)
- **Hallucination Rate** = H / total atoms mentioned by model
- **Overall** = weighted combination with severity

### Severity Weights (for penalty calculation)
| Severity | Inaccurate Penalty | Missing Penalty |
|----------|-------------------|-----------------|
| Critical | 5.0 | 5.0 |
| Important | 3.0 | 2.0 |
| Minor | 1.0 | 0.5 |

## Implementation Plan

### Phase 1: Build Templates
1. Define base template + 3 type-specific extensions
2. Validate template covers everything the generation prompts ask for

### Phase 2: Extract Atoms from Groundtruth (45 figures)
1. For each figure, determine type → select template
2. Parse groundtruth annotation into atom values
3. Use LLM to assist extraction, human-verify results
4. Expected: ~30-50 atoms per figure, ~1,500-2,000 total

### Phase 3: Build New Judge
1. Judge receives: image + atom checklist + model description
2. For each atom: classify as C/I/M/H/N/A
3. Compute scores from classifications
4. Compare with old MQM scores

### Phase 4: Re-evaluate
1. Re-score all 12 models on 45 adversarial figures
2. Compare old vs new MQM
3. Check: does a wrong-figure description now score near 0?

## File Structure
```
atomic_mqm/
├── README.md              (this file)
├── templates/
│   ├── base.json          (shared template)
│   ├── line_plot.json     (line plot extension)
│   ├── bar_chart.json     (bar chart extension)
│   └── pie_chart.json     (pie chart extension)
├── atoms/
│   ├── english_fig_002.json
│   ├── english_fig_005.json
│   └── ...                (one per figure, filled templates)
├── judge_prompt.txt       (new judge prompt)
└── evaluator.py           (new evaluation script)
```
