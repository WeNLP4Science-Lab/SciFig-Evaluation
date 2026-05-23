# Severity Assignment for Bar Chart Description Checklist Items

## Overview

Each bar chart checklist item is assigned a severity level that caps the maximum error penalty when the item is wrong or missing. The severity reflects the impact on scientific usability of the generated description.

### Severity Levels

| Level | Meaning | Error Behaviour |
|-------|---------|-----------------|
| **Critical** | Essential for correct scientific interpretation; errors can mislead readers | Completely wrong/missing = Major error; partially wrong = Minor error |
| **Important** | Significant for completeness and usability; errors reduce description quality | Completely wrong/missing = Major error; partially wrong = Minor error |
| **Minor** | Supplementary detail; errors are noticeable but do not undermine core understanding | Any error = Minor error (capped) |

### Weight Matrix (for reference)

| Dimension | Major Weight | Minor Weight |
|-----------|-------------|-------------|
| Accuracy | 5.0 | 2.0 |
| Completeness | 3.5 | 1.5 |
| Clarity | 2.0 | 1.0 |

### Human Evaluation Error Frequencies (for reference)

| Error Type | Count | Rank |
|-----------|-------|------|
| acc_num_val (incorrect numerical values) | 265 | 1st |
| acc_visual_attb_mapping (wrong colour/label mapping) | 243 | 2nd |
| acc_structure_desc (wrong chart structure) | 86 | 3rd |
| comp_hallucination (fabricated content) | 46 | 4th |
| acc_axis_interpr (wrong axis info) | 26 | 5th |

---

## Item-by-Item Severity Assignments

### bar_01: Chart type correctly identified (bar chart)

**Severity: Critical**

Correctly identifying the chart type is the foundational premise for every subsequent element in the description. If a bar chart is described as a line plot or scatter plot, the entire description becomes structurally incoherent and scientifically unusable. CharXiv (Wang et al., 2024a) treats chart type identification as a prerequisite descriptive question, and ChartBench (Xu et al., 2024) separates evaluation by chart type precisely because misclassification invalidates all downstream reasoning. Our human evaluation data shows acc_structure_desc errors at 86 occurrences, confirming that structural misidentification is a real and consequential failure mode.

---

### bar_02: Bar orientation correctly stated (vertical/horizontal)

**Severity: Important**

Bar orientation determines how axes are interpreted: in a horizontal bar chart, the categorical axis is on the y-axis and the value axis is on the x-axis. Stating the wrong orientation causes axis label assignments to be swapped, which misleads readers about what is being measured versus what is being compared. However, if the rest of the description correctly maps axes and values, an isolated orientation error is less damaging than a full structural misidentification. ChartX (Xia et al., 2024) distinguishes horizontal and vertical bar subtypes, treating them as meaningfully different chart configurations.

---

### bar_03: Grouping/stacking structure correctly identified (simple/grouped/stacked)

**Severity: Critical**

Misidentifying grouped bars as stacked (or vice versa) fundamentally changes the semantics of the data representation. A stacked bar shows part-to-whole relationships, while a grouped bar shows side-by-side comparisons. Mukhopadhyay et al. (2024) in RobustCQA found that VLMs exhibit "significant performance variations" when the same data is rendered in different grouping formats, and our acc_structure_desc count of 86 errors confirms this is a frequent and impactful failure. The VisText L1 framework (Tang et al., 2023) considers encoding structure an elemental property that anchors all higher-level interpretation.

---

### bar_04: X-axis label and units correctly described

**Severity: Critical**

Axis labels define the semantic meaning of the data. Reporting the wrong x-axis label (e.g., saying "countries" when it shows "years") makes the entire description factually wrong in its core claim about what the chart measures. Our human evaluation found 26 acc_axis_interpr errors, but these carry disproportionate weight because an axis error propagates through every value statement in the description. ChartQA (Masry et al., 2022) treats axis understanding as foundational, and PlotQA (Methani et al., 2020) builds 80.76% of its questions on information not directly labeled, requiring correct axis interpretation as a prerequisite.

---

### bar_05: X-axis scale type and range correctly described

**Severity: Important**

The scale type (linear, logarithmic, categorical) and range affect how values are read and compared. Pandey et al. (2025) found that VLMs perform at only 8-18% accuracy on detecting unconventional scale directions, and Wang et al. (2024a) documented order-of-magnitude errors when logarithmic scales are misread as linear. However, for bar charts, the x-axis is typically categorical, making scale errors less common than for the y-axis. The impact is significant when it occurs but the frequency is lower, warranting Important rather than Critical.

---

### bar_06: Y-axis label and units correctly described

**Severity: Critical**

The y-axis label defines what quantity the bar heights represent. Misidentifying it (e.g., "percentage" instead of "count," or wrong units) renders every numerical statement in the description semantically incorrect. This is arguably the single most consequential axis error for bar charts because it determines the interpretation of every bar value. Huang et al. (2024) found that GPT-4V cannot reliably align data points to axes when explicit annotations are absent, and the CHOCOLATE dataset taxonomy treats axis misinterpretation as a factual error category.

---

### bar_07: Y-axis scale type and range correctly described

**Severity: Important**

The y-axis scale type directly affects numerical accuracy. Wang et al. (2024a) demonstrated that misreading logarithmic scales as linear leads to order-of-magnitude value errors, and truncated axes (not starting at zero) distort comparative descriptions. Our acc_num_val error count of 265 is partly attributable to scale misreading. However, the scale type is secondary to the axis label itself; if the label and values are correct, a missing or incorrect scale description is a lesser error. The impact is significant enough for Important but does not reach Critical because the label (bar_06) captures the primary semantic content.

---

### bar_08: All categories on the categorical axis mentioned

**Severity: Critical**

Omitting categories means the description gives an incomplete picture of the data, which in a scientific context can hide important results. If a bar chart compares five treatments and the description mentions only three, readers may draw incorrect conclusions about which treatments were studied. ChartSumm (Rahman et al., 2023) distinguishes short and long summaries, but even short summaries are expected to reference all major data points. ChartBench (Xu et al., 2024) specifically tests whether models can enumerate all categories, and omissions are treated as completeness failures.

---

### bar_09: All data series identified (for grouped/stacked)

**Severity: Critical**

In grouped and stacked bar charts, each data series represents a distinct experimental condition, demographic group, or variable. Missing a series is equivalent to omitting an entire dimension of the data. ChartX (Xia et al., 2024) found that multi-series bar charts consistently receive lower accuracy scores, and our acc_visual_attb_mapping count of 243 errors shows that series identification is the second most common error category. Failing to identify a series makes the description structurally incomplete and potentially misleading about the scope of the data.

---

### bar_10: Legend correctly described (colour/pattern to series mapping)

**Severity: Critical**

The legend is the key that maps visual encodings to data semantics. Kim et al. (2024) documented GPT-4's "tendency to misread color legends and inability to consistently interpret multiple colors in charts," and our acc_visual_attb_mapping count of 243 is the second highest error frequency. A swapped legend mapping (attributing Series A's values to Series B) produces a description that is internally consistent but factually wrong, which is the most dangerous type of error for scientific usability. Pandey et al. (2025) confirmed that all tested VLMs (GPT-4o, Claude, Gemini, Llama) struggle with "data-dense visualizations involving multiple encodings."

---

### bar_11: Numerical values accurate

**Severity: Critical**

Numerical accuracy is the most fundamental requirement for scientific chart descriptions. Our human evaluation data shows acc_num_val at 265 occurrences, the single most common error type. Huang et al. (2024) found that even the most capable LVLMs produce chart captions with a non-factual rate of 81.27%, with value fabrication being the primary contributor. ChartQA (Masry et al., 2022) uses a relaxed 5% tolerance for numerical answers, implicitly acknowledging that exact value extraction is difficult but that approximately correct values are still scientifically useful. Completely wrong values directly mislead scientific interpretation.

---

### bar_12: Colour descriptions accurate for bars/series

**Severity: Important**

Accurate colour descriptions matter for reproducibility and accessibility (readers may need to reference specific bars in follow-up work), and colour is the primary visual channel for distinguishing series in grouped and stacked charts. Kim et al. (2024) found that GPT-4 "lacks the ability to reliably distinguish between colors in charts." However, colour description is downstream of legend mapping (bar_10): if the legend mapping is correct, a colour naming error (e.g., "blue" vs. "teal") is less consequential than a mapping error. The impact is significant but not as severe as getting the mapping itself wrong.

---

### bar_13: Annotations noted if present (error bars, reference lines, data labels)

**Severity: Important**

Error bars convey statistical uncertainty, reference lines indicate thresholds or baselines, and data labels provide exact values. These elements are scientifically meaningful: error bars can change conclusions about statistical significance, and reference lines often represent critical thresholds (e.g., p=0.05 lines, performance baselines). Bendeck et al. (2025) in CHART NOISe found that VLMs frequently miss these elements, and Huang et al. (2024) noted that VLMs "either ignore error bars entirely or misinterpret them." However, annotations are not universally present on all bar charts, and their absence does not invalidate the core description, so Important is appropriate.

---

### bar_14: Sorting order described

**Severity: Minor**

Sorting order (alphabetical, ascending by value, custom) is a presentation choice rather than a data property. While noting that bars are sorted by descending value can aid comprehension, omitting or misidentifying the sort order does not change the factual content of the description. No major benchmark (ChartQA, CharXiv, CHOCOLATE) includes sorting order as an evaluation criterion. It is a useful detail for completeness but errors here have minimal impact on scientific interpretation.

---

### bar_15: Visual emphasis noted if present (highlighted, bolded bars)

**Severity: Minor**

Visual emphasis (e.g., a highlighted bar, a different colour for a specific category, bolding) is an authorial choice to draw attention. While noting it adds completeness, missing it does not introduce factual errors or omit data. The VisText L1 framework covers encoded properties but does not specifically flag emphasis as a required element. Emphasis is context-dependent and its significance varies; treating it as Minor ensures it is checked without over-penalizing its omission.

---

### bar_16: Chart purpose or title described

**Severity: Important**

The chart title or stated purpose provides the interpretive frame for the data. Omitting it forces readers to infer purpose from axes and data alone, which is possible but reduces usability. SciCap (Hsu et al., 2021) found that scientific figure captions connect chart content to scientific findings, and the title is often the primary mechanism for this connection. However, not all charts have explicit titles, and even without stating the title, a description that correctly covers all data elements remains scientifically usable. Important captures its value without treating it as indispensable.

---

### bar_17: No hallucinated elements

**Severity: Critical**

Hallucination is the most dangerous error type because it introduces fabricated information that readers have no way to detect from the description alone. Our human evaluation found 46 comp_hallucination occurrences, and Huang et al. (2024) showed non-factual rates of 81.27% in VLM chart captions. The CHOCOLATE dataset specifically taxonomises hallucination types (fabricated values, invented trends, phantom data series), and Bendeck et al. (2025) found that hallucinations become more frequent under chart corruption, with models remaining "overconfident" and generating "plausible but unsupported explanations." Any hallucinated element directly undermines the trustworthiness of the entire description.

---

### bar_18: No unwanted interpretation

**Severity: Important**

Unwanted interpretation occurs when the description includes causal claims, speculative explanations, or subjective judgments not supported by the chart data alone. While less dangerous than outright hallucination (bar_17), interpretation can bias readers toward conclusions the data does not support. The VisText framework (Tang et al., 2023) explicitly separates L1/L2 (descriptive) from L3 (interpretive) content, recognising that interpretation should be clearly distinguished from description. In a scientific context, unsolicited interpretation can be misleading, but it is typically recognisable as opinion rather than fabricated fact, making it less severe than hallucination. Important reflects the real risk while distinguishing it from the Critical severity of hallucinated content.

---

## Summary Table

| Item | Description | Severity | Dimension |
|------|-------------|----------|-----------|
| bar_01 | Chart type identified | Critical | Accuracy |
| bar_02 | Bar orientation stated | Important | Accuracy |
| bar_03 | Grouping/stacking structure | Critical | Accuracy |
| bar_04 | X-axis label and units | Critical | Accuracy |
| bar_05 | X-axis scale type and range | Important | Accuracy |
| bar_06 | Y-axis label and units | Critical | Accuracy |
| bar_07 | Y-axis scale type and range | Important | Accuracy |
| bar_08 | All categories mentioned | Critical | Completeness |
| bar_09 | All data series identified | Critical | Completeness |
| bar_10 | Legend correctly described | Critical | Accuracy |
| bar_11 | Numerical values accurate | Critical | Accuracy |
| bar_12 | Colour descriptions accurate | Important | Accuracy |
| bar_13 | Annotations noted | Important | Completeness |
| bar_14 | Sorting order described | Minor | Completeness |
| bar_15 | Visual emphasis noted | Minor | Completeness |
| bar_16 | Chart purpose/title described | Important | Completeness |
| bar_17 | No hallucinated elements | Critical | Accuracy |
| bar_18 | No unwanted interpretation | Important | Clarity |

### Distribution

- **Critical**: 9 items (bar_01, bar_03, bar_04, bar_06, bar_08, bar_09, bar_10, bar_11, bar_17)
- **Important**: 7 items (bar_02, bar_05, bar_07, bar_12, bar_13, bar_16, bar_18)
- **Minor**: 2 items (bar_14, bar_15)

### Design Rationale

The severity distribution reflects the principle that errors in core data semantics (what is measured, what values are reported, what series exist) should be penalised most heavily because they directly affect scientific conclusions. Presentation details (sorting, emphasis) are penalised least because they affect readability but not correctness. The large number of Critical items (9/18) is intentional: bar charts in scientific figures carry quantitative claims, and most checklist items test aspects that, if wrong, would mislead a reader about those claims.

The assignment is corroborated by our human evaluation data, which shows the two most frequent error types (acc_num_val at 265, acc_visual_attb_mapping at 243) mapping to Critical items (bar_11 and bar_10 respectively), while the less frequent errors map to Important or Minor items. This alignment between observed error frequency and assigned severity ensures that the scoring system penalises the errors that matter most in practice.

## References

- Bendeck et al. (2025). Losing the Plot: How VLM Responses Degrade on Imperfect Charts.
- Huang et al. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. CHOCOLATE dataset.
- Hsu et al. (2021). SciCap: Generating Captions for Scientific Figures.
- Kim et al. (2024). An Empirical Evaluation of the GPT-4 Multimodal Language Model on Visualization Literacy Tasks.
- Masry et al. (2022). ChartQA: A Benchmark for Question Answering about Charts.
- Methani et al. (2020). PlotQA: Reasoning over Scientific Plots.
- Mukhopadhyay et al. (2024). Unraveling the Truth: Do VLMs Really Understand Charts? (RobustCQA).
- Pandey et al. (2025). Benchmarking Visual Language Models on Standardized Visualization Literacy Tests.
- Rahman et al. (2023). ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization.
- Tang et al. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. ACL Outstanding Paper.
- Wang et al. (2024a). CharXiv: Charting Gaps in Realistic Chart Understanding. NeurIPS 2024.
- Xia et al. (2024). ChartX & ChartVLM: A Versatile Benchmark and Foundation Model.
- Xu et al. (2024). ChartBench: A Benchmark for Complex Visual Reasoning in Charts.
