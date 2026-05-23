# Severity Assignment for Line Plot Description Checklist Items

MQM-based evaluation of VLM-generated scientific figure descriptions.

## Weight Matrix

| Category     | Major | Minor |
|-------------|-------|-------|
| Accuracy     | 5.0   | 2.0   |
| Completeness | 3.5   | 1.5   |
| Clarity      | 2.0   | 1.0   |

## Severity Cap Rules

| Item Severity | Error Degree | Capped Error Level |
|--------------|-------------|-------------------|
| Critical     | Completely wrong/missing | Major |
| Critical     | Partially wrong | Minor |
| Important    | Completely wrong/missing | Major |
| Important    | Partially wrong | Minor |
| Minor        | Any error | Minor (capped) |

---

## Item-Level Severity Assignments

### line_01: Chart type correctly identified (line plot)

**Severity: Critical** | Category: Accuracy

Misidentifying the chart type (e.g., calling a line plot a bar chart or scatter plot) renders the entire downstream description structurally incoherent. ChartBench (Xu et al., 2024) treats chart type recognition as a prerequisite gating task; if the type is wrong, all subsequent structural expectations are misaligned. Our human eval data confirms that chart type errors cascade into trend, axis, and legend errors because the judge applies the wrong evaluation schema.

---

### line_02: X-axis label and units correctly described

**Severity: Critical** | Category: Accuracy

The x-axis defines the independent variable in most scientific line plots; misidentifying it fundamentally changes what the chart communicates. CharXiv (Wang et al., 2024) showed that axis label errors are among the most consequential for downstream reasoning tasks, as they corrupt the semantic frame for interpreting all data points and trends. In scientific contexts, wrong units (e.g., "seconds" vs. "milliseconds") introduce order-of-magnitude interpretation errors.

---

### line_03: X-axis scale type and range correctly described

**Severity: Important** | Category: Accuracy

Scale type (linear vs. logarithmic) and range determine how trends are interpreted; a line that appears linear on a log scale represents exponential growth. Mahbub et al. (2025) found that all 10 evaluated VLMs failed to detect axis inversion, and 9/10 were affected by aspect ratio distortions. However, partial errors (e.g., correct scale type but slightly off range endpoints) have bounded impact, placing this below Critical.

---

### line_04: Y-axis label and units correctly described

**Severity: Critical** | Category: Accuracy

The y-axis label identifies the measured quantity, which is the core scientific content of the figure. Misidentifying it (e.g., "accuracy" vs. "loss") inverts the meaning of every trend described. ChartInsights (Wu et al., 2024) and CharXiv both weight axis identification as foundational to all higher-level tasks. Our human evaluations consistently rank axis label errors among the highest-impact Accuracy errors.

---

### line_05: Y-axis scale type and range correctly described

**Severity: Important** | Category: Accuracy

Same reasoning as line_03: scale type errors (log vs. linear) can cause magnitude misinterpretation, and range errors affect whether reported values seem plausible. The Perils of Chart Deception study (Mahbub et al., 2025) documented systematic VLM failures on non-standard scales. Ranked Important rather than Critical because the y-axis label (line_04) already anchors the semantic identity of the measured variable.

---

### line_06: All lines/series mentioned

**Severity: Critical** | Category: Completeness

Missing an entire data series is a completeness failure that renders the description scientifically incomplete. In multi-method comparison plots common in ML papers, omitting a series means omitting a competing approach entirely. CHOCOLATE (Huang et al., 2024) identified entity omission as a primary factual error mode, and VisText (Tang et al., 2023) treats series enumeration as a Level 1 (Construction) requirement that gates all higher-level analysis.

---

### line_07: Legend correctly described (colour/style to series mapping)

**Severity: Critical** | Category: Accuracy

Legend mapping errors are a form of entity confusion, which Kim et al. (2025) identified as one of the primary hallucination modes in chart understanding. If "Method A" is attributed the color and trajectory of "Method B," every claim about both methods becomes wrong. Our human eval data identified acc_visual_attb_mapping as one of the two most frequent error types, directly implicating legend-to-series correspondence as a top failure mode.

---

### line_08: Colour descriptions accurate for each line

**Severity: Minor** | Category: Accuracy

Colour naming errors (e.g., "blue" vs. "teal") are common due to VLM colour perception limitations documented by Bendeck and Stasko (2024), but they are less consequential than legend mapping errors (line_07) because the description may still correctly associate the right trend with the right series name. Our evaluation system already applies a colour family tolerance (11 basic families). Standalone colour inaccuracy that does not break legend mapping is a stylistic rather than scientific error.

---

### line_09: Line styles correctly described (solid, dashed, dotted)

**Severity: Minor** | Category: Completeness

Line style is a secondary visual encoding that supplements colour for series discrimination. While useful for accessibility and greyscale printing, incorrect line style descriptions rarely affect scientific interpretation if the legend mapping (line_07) and series identification (line_06) are correct. VisText treats visual encoding details as Level 1 content that is informative but not essential for understanding the chart's message.

---

### line_10: Marker shapes correctly described if present

**Severity: Minor** | Category: Completeness

Marker shapes are a tertiary visual encoding. Many scientific line plots do not use markers at all, making this conditionally applicable. When present, marker errors (e.g., "circles" vs. "triangles") do not affect trend interpretation or numerical accuracy. ChartMuseum (Li et al., 2025) found that fine-grained visual attribute discrimination is a known VLM weakness, but the scientific impact of marker errors is low.

---

### line_11: Numerical values accurate where stated (start/end, peaks, troughs)

**Severity: Critical** | Category: Accuracy

Numerical accuracy is the most directly verifiable aspect of a chart description and the most consequential for scientific use. Our human eval data identified acc_num_val as the top error type across all models. ChartQA uses a 5% tolerance precisely because numerical errors are high-impact. CHOCOLATE (Huang et al., 2024) found an 81.27% non-factual rate in chart captions, with value fabrication as a primary contributor. Stating "accuracy reaches 95%" when it reaches 75% is a critical scientific misrepresentation.

---

### line_12: Trends correctly described per line (increasing, decreasing, stable)

**Severity: Critical** | Category: Accuracy

Trend description is the core analytical content of a line plot description. Kim et al. (2025) documented that all three frontier models exhibited trend misinterpretation, with the problem becoming more frequent under visual corruption. ChartInsights (Wu et al., 2024) found only 39.8% average accuracy on trend-related tasks across 19 models. Describing an increasing trend as decreasing inverts the scientific conclusion (e.g., "performance improves" becomes "performance degrades").

---

### line_13: Crossover/intersection points mentioned if present

**Severity: Important** | Category: Completeness

Crossover points often represent the most scientifically significant features of a multi-series line plot (e.g., "Method A surpasses Method B at epoch 50"). Missing them omits key comparative findings. However, this is conditionally applicable (only relevant when crossovers exist) and is a completeness rather than accuracy concern, placing it at Important rather than Critical. ChartInsights categorises intersection detection as a distinct low-level task where VLMs underperform.

---

### line_14: Annotations noted if present (confidence intervals, shaded regions, reference lines)

**Severity: Important** | Category: Completeness

Annotations convey uncertainty quantification and contextual baselines that are essential in scientific reporting. Omitting confidence intervals removes information about statistical reliability; omitting reference lines removes performance baselines. Akhtar et al. (2024) documented that VLMs handle annotation-related information poorly. Ranked Important because annotations are conditionally present and their omission, while significant, does not corrupt the core data description.

---

### line_15: Dual y-axes described if present

**Severity: Important** | Category: Accuracy

Dual y-axes require the reader to associate each series with its correct scale; failure to note dual axes means the reader may compare values across incompatible scales. Mahbub et al. (2025) found that dual axes are among the misleading chart features VLMs handle worst. Ranked Important rather than Critical because dual y-axes are conditionally present (most line plots have a single y-axis), but when present and missed, the error is Major.

---

### line_16: Chart purpose or title described

**Severity: Important** | Category: Completeness

The title provides the semantic frame for interpreting the chart. Omitting it forces the reader to infer purpose from axis labels alone. SciFIBench (Roberts et al., 2024) found significant gaps in VLM figure-caption matching, partly because models fail to connect chart content to its stated purpose. Ranked Important because while the title aids interpretation, the data content (axes, values, trends) can stand alone for scientific assessment.

---

### line_17: No hallucinated elements (fabricated lines, data points, or trends)

**Severity: Critical** | Category: Accuracy

Hallucination is the most dangerous error mode because it introduces false information that a reader has no way to detect without the original figure. CHOCOLATE (Huang et al., 2024) documented an 81.27% non-factual rate, and Kim et al. (2025) showed that models generate "plausible but unsupported explanations" even when chart content is occluded. Fabricating a data series or trend that does not exist is worse than omitting a real one because it actively misleads.

---

### line_18: No unwanted interpretation (no subjective claims or causal inference)

**Severity: Important** | Category: Clarity

Subjective or causal claims (e.g., "Method A is better because of its architecture") go beyond description into interpretation, which is inappropriate for a factual chart description task. Lundgard and Satyanarayan (2022) classified causal claims as Level 4 content that is domain-specific and should be distinguished from Level 1-3 factual content. Ranked Important because while such claims are methodologically inappropriate, they do not corrupt the factual data content of the description.

---

### line_19: Description is clear and unambiguous

**Severity: Minor** | Category: Clarity

Clarity issues (ambiguous phrasing, poor sentence structure, vague references) affect readability but not factual content. Under MQM, Clarity errors carry the lowest weights (Major=2.0, Minor=1.0), reflecting that a poorly written but factually correct description is far preferable to a well-written but inaccurate one. ChaTS-Pi (Krichene et al., 2024) demonstrated that faithfulness and clarity are separable quality dimensions.

---

## Summary Table

| ID | Item (short) | Severity | Category | Max Penalty (wrong/missing) |
|----|-------------|----------|----------|-----------------------------|
| line_01 | Chart type identified | Critical | Accuracy | 5.0 |
| line_02 | X-axis label and units | Critical | Accuracy | 5.0 |
| line_03 | X-axis scale and range | Important | Accuracy | 5.0 |
| line_04 | Y-axis label and units | Critical | Accuracy | 5.0 |
| line_05 | Y-axis scale and range | Important | Accuracy | 5.0 |
| line_06 | All lines/series mentioned | Critical | Completeness | 3.5 |
| line_07 | Legend mapping | Critical | Accuracy | 5.0 |
| line_08 | Colour descriptions | Minor | Accuracy | 2.0 |
| line_09 | Line styles | Minor | Completeness | 1.5 |
| line_10 | Marker shapes | Minor | Completeness | 1.5 |
| line_11 | Numerical values | Critical | Accuracy | 5.0 |
| line_12 | Trends per line | Critical | Accuracy | 5.0 |
| line_13 | Crossover points | Important | Completeness | 3.5 |
| line_14 | Annotations | Important | Completeness | 3.5 |
| line_15 | Dual y-axes | Important | Accuracy | 5.0 |
| line_16 | Chart purpose/title | Important | Completeness | 3.5 |
| line_17 | No hallucinations | Critical | Accuracy | 5.0 |
| line_18 | No unwanted interpretation | Important | Clarity | 2.0 |
| line_19 | Clear and unambiguous | Minor | Clarity | 1.0 |

**Distribution:** 8 Critical, 7 Important, 4 Minor

**Critical items** (8): chart type, x-axis label, y-axis label, all series mentioned, legend mapping, numerical values, trends, no hallucinations. These represent the irreducible core: if any is completely wrong, the description is scientifically misleading.

**Important items** (7): x-axis scale/range, y-axis scale/range, crossover points, annotations, dual y-axes, chart purpose, no unwanted interpretation. These matter for completeness and precision but have bounded impact when partially wrong.

**Minor items** (4): colour names, line styles, marker shapes, clarity. These are informative but not load-bearing for scientific interpretation.
