# Missing Evaluation Factors in MQM-Based VLM Chart Description Assessment

## Current Framework Summary

Our evaluation uses per-item checklists (14 bar, 15 line, 12 pie) scored on coverage and correctness, global constraints (hallucination, unwanted interpretation, clarity, verbosity), and MQM penalty weights across three dimensions: Accuracy (major 5 / minor 2), Completeness (major 3.5 / minor 1.5), and Clarity (major 2 / minor 1).

This document identifies evaluation dimensions present in other chart/figure benchmarks or accessibility literature that our framework does not currently capture.

---

## 1. Finer-Grained Error Sub-Typing Within Accuracy

### 1.1 The CHOCOLATE Error Taxonomy

Huang et al. (2024) introduce a fine-grained taxonomy of factual errors in chart captions (the CHOCOLATE dataset, ACL 2024 Findings) that distinguishes:

- **Value Error**: an incorrect quantitative data value
- **Label Error**: an incorrect non-quantitative value (e.g., wrong category name, axis label)
- **Trend Error**: the direction of a trend is wrong (e.g., "increasing" when decreasing)
- **Magnitude Error**: the magnitude or variance of a trend is wrong (e.g., "sharply increasing" when only modestly so)
- **Out-of-Context Error**: the caption introduces concepts not present in the chart
- **Nonsense Error**: the caption is incomplete or incoherent
- **Grammatical Error**: surface-level language errors

**Gap in our framework**: We collapse all of these into a single "Accuracy" dimension. Tracking sub-types (value vs. label vs. trend vs. magnitude vs. out-of-context) even under the same penalty weight would enable richer error analysis. In particular, *trend errors* and *magnitude errors* represent qualitatively different failure modes from *value errors*---the former reflect reasoning failures, while the latter reflect perceptual or OCR failures.

### 1.2 ChartHal Hallucination Scenarios

Cui et al. (2025) introduce ChartHal, a fine-grained hallucination benchmark with 12 hallucination-triggering scenarios organized into four categories:

- **Irrelevant**: questions that do not pertain to the chart (model should refuse)
- **Inexistent**: questions about elements not present in the chart
- **Contradictory**: questions that contain false premises about the chart
- **Normal**: standard answerable questions

**Gap**: Our "hallucination" flag is binary. ChartHal's taxonomy suggests distinguishing *fabricated entities* (describing data series that do not exist) from *fabricated values* (wrong numbers for real entities) from *fabricated relationships* (invented correlations or trends). These have different downstream consequences and different root causes.

---

## 2. Consistency (Internal Coherence)

No benchmark we surveyed uses an explicit "consistency" metric, but the problem surfaces repeatedly:

- ChartSumm (Rahman et al., 2023) reports that generated summaries often contain internally contradictory statements (e.g., "X increases steadily" followed by "X peaked in 2015 then declined").
- The MQM framework itself, as used in translation quality (Lommel et al., 2014), includes a top-level "Consistency" dimension for texts that contradict themselves, though it is rarely instantiated in chart evaluation.

**Gap**: Our framework does not penalize internal contradictions within a description. A model could state "the blue bar is the tallest" in one sentence and "the red bar exceeds all others" in the next, and each sentence would be scored independently. An explicit consistency check---flagging pairs of claims that cannot both be true---would catch this failure mode.

---

## 3. Specificity and Semantic Level Coverage

### 3.1 The Lundgard-Satyanarayan Four-Level Model

Lundgard and Satyanarayan (2022) propose a four-level model of semantic content for visualization descriptions (IEEE TVCG):

- **Level 1**: Chart construction (type, encodings, axis labels, title)
- **Level 2**: Statistical facts and individual data points (extremes, specific values)
- **Level 3**: Perceptual and cognitive patterns (trends, clusters, outliers, correlations)
- **Level 4**: Domain-specific and contextual interpretation (sociopolitical significance, causal claims)

Their user study found that blind participants rated Level 2 and Level 3 content as most useful. Sighted participants also preferred Level 3.

**Gap**: Our checklist conflates Levels 1--3 into a single item list without tracking which semantic level each item belongs to. We have no explicit mechanism for evaluating whether a description covers an appropriate *range* of semantic levels. A description that perfectly covers Level 1 (chart construction) but omits all Level 2/3 content (trends, extremes) would not be distinguishable from one that does the opposite---yet they serve very different user needs.

### 3.2 VisText L1/L2/L3 Separation

Tang, Boggust, and Satyanarayan (2023) operationalize this in VisText (ACL 2023): each chart has a synthetic L1 caption (construction) and a crowdsourced L2/L3 caption (statistics and trends). Evaluation metrics are applied separately to each level.

**Gap**: We do not separate our checklist items by semantic level, making it impossible to diagnose whether a model fails at perception (Level 1), data extraction (Level 2), or pattern recognition (Level 3).

---

## 4. Visual Grounding

### 4.1 ChartAnchor

Masry et al. (2024) introduce ChartAnchor, a benchmark for "chart grounding"---the bidirectional alignment between a chart's visual appearance and its structured semantics. Their multi-level evaluation integrates semantic validation, stylistic analysis, and perceptual metrics.

**Gap**: Our evaluation cannot distinguish whether a model's correct claim (e.g., "revenue peaked at $4.2M in 2019") was derived from actually reading the chart image vs. from caption text, OCR leakage, or training data memorization. A grounding dimension would evaluate whether claims are *visually verifiable* from the chart---i.e., whether a human could confirm the claim by looking at the figure alone. This is especially important for our adversarial blur experiments, where selectively blurred elements should *not* be described with high confidence.

### 4.2 Confidence Calibration

CHART NOISe / CHAOS (Bendeck et al., 2025) found that models remain "overconfident in degraded settings, generating plausible but unsupported explanations." Models rarely hedge or express uncertainty even when chart elements are occluded or corrupted.

**Gap**: We do not evaluate whether models appropriately hedge when visual evidence is ambiguous. A description that says "the value appears to be approximately 40" when a bar is partially occluded is more honest than one that says "the value is 42.3"---but our framework would score the hedged version lower on specificity.

---

## 5. Numerical Precision vs. Numerical Accuracy

### 5.1 Relaxed Accuracy in QA Benchmarks

ChartQA (Masry et al., 2022) uses "relaxed accuracy"---exact match with 5% numerical tolerance. PlotQA (Methani et al., 2020) uses a similar threshold. This reflects a practical reality: reading exact values from chart images is often impossible even for humans.

**Gap**: Our framework does not distinguish between:
- **Precision errors**: saying "about 40%" when the chart shows 40% (appropriate hedging)
- **Accuracy errors**: saying "60%" when the chart shows 40% (wrong value)
- **False precision**: saying "39.7%" when the chart shows a bar that could be anywhere from 38--42% (unjustified specificity)

False precision is arguably a *worse* failure than honest approximation, because it conveys unwarranted certainty. Yet our Accuracy dimension would score "approximately 40%" and "39.7%" identically if the true value is 40%.

### 5.2 ChartAnchor's Numerical Precision Findings

ChartAnchor (Masry et al., 2024) found "critical limitations in numerical precision" across all tested MLLMs, with models frequently producing values that are close but not exact. Separating precision from accuracy would let us analyze whether models are *systematically* over-precise or appropriately uncertain.

---

## 6. Spatial Reasoning Quality

### 6.1 Benchmarks That Test Spatial Understanding

- **ChartInsights** (Wang et al., 2024b, EMNLP 2024) defines 10 low-level analysis tasks derived from Amar et al.'s taxonomy: retrieve value, filter, compute derived value, find extremum, sort/order, determine range, characterize distribution, find anomalies, cluster, and correlate. Several of these (sort/order, find extremum, determine range) inherently require spatial reasoning about chart elements.
- **CharXiv** (Wang et al., 2024a, NeurIPS 2024) includes "descriptive questions" that require examining spatial relationships among chart elements.
- **ChartBench** (Xu et al., 2024) specifically tests unlabeled charts where models must derive values purely from spatial position relative to axes.

**Gap**: Our checklist includes items like "identifies the highest/lowest bar" but does not separately evaluate *spatial reasoning quality*---whether the model correctly describes left-to-right ordering, relative positions of bars/lines, which line is above/below another at a given point, or the spatial layout of legend placement. These are distinct from value accuracy; a model could report the correct maximum value but incorrectly describe *where* in the chart it appears.

### 6.2 Spatial Errors as a Distinct Category

The CALVI benchmark (Pandey et al., 2025, EuroVis) tests critical thinking about misleading visualizations, including spatial distortions (truncated axes, area-proportional misrepresentations). VLMs scored 21.8--30.0% accuracy on CALVI, far below their performance on basic chart literacy tasks.

**Recommendation**: Add spatial reasoning as either a separate checklist dimension or an error sub-type under Accuracy, covering: ordering claims, relative position claims, and layout descriptions.

---

## 7. Multi-Panel and Compound Figure Handling

### 7.1 Current Benchmark Landscape

- **MultiChartQA** (Zhu et al., 2025, NAACL 2025) explicitly benchmarks multi-chart reasoning across four task types: direct QA, parallel QA, comparative reasoning, and sequential reasoning. Significant performance gaps exist between single-chart and multi-chart tasks.
- **MultiChartQA-R** (2025) extends this with cross-chart trend comparison, complementary data integration, anomaly/causal analysis, and strategy recommendation tasks in three languages.
- **SciFIBench** (Roberts et al., 2024, NeurIPS 2024) includes multi-image tasks for scientific figure interpretation with 2,000 questions across 8 categories.
- **FigEx2** (2025) specifically addresses panel detection and captioning for scientific compound figures.

**Gap**: Our checklist assumes single-panel figures. For multi-panel figures, additional evaluation dimensions are needed:
- **Panel identification**: Does the description correctly identify and enumerate sub-panels?
- **Cross-panel reference**: Does the description correctly relate information across panels (e.g., "Panel A shows the training loss while Panel B shows the corresponding accuracy")?
- **Panel-claim attribution**: Are claims correctly attributed to the right panel?
- **Inter-panel consistency**: Are claims about shared axes or variables consistent across panel descriptions?

---

## 8. Analytical Task Coverage

### 8.1 ChartInsights' 10-Task Taxonomy

ChartInsights (Wang et al., 2024b) operationalizes Amar, Eagan, and Stasko's (2005) taxonomy of low-level analysis tasks:

| Task | Description | In our checklist? |
|------|-------------|-------------------|
| Retrieve Value | Find a specific data point | Yes (value items) |
| Find Extremum | Identify min/max | Yes (highest/lowest items) |
| Determine Range | Find value span | No |
| Characterize Distribution | Describe value distribution shape | No |
| Find Anomalies | Identify outliers | No |
| Cluster | Group similar points | No |
| Correlate | Identify relationships between variables | No (line only, partially) |
| Sort/Order | Rank data points | No |
| Filter | Identify data meeting conditions | No |
| Compute Derived Value | Calculate from data | No |

**Gap**: Our checklist covers value retrieval and extremum identification well but does not explicitly evaluate whether descriptions identify outliers, characterize distributions, or note clusters. For scientific chart descriptions, anomaly detection and distribution characterization are arguably among the most important analytical observations.

### 8.2 ChartX's Task Hierarchy

Xia et al. (2024) define seven tasks in ChartX: title perception, chart type recognition, structural extraction, QA, description, summarization, and redrawing. Their separation of "description" (detailed element-by-element) from "summarization" (high-level takeaway) maps to an important distinction.

**Gap**: We evaluate description quality but do not separately assess whether the model produces appropriate *summarization*---the high-level "so what" of the chart. A model could correctly describe every bar height but miss that the overall story is "consistent year-over-year growth."

---

## 9. Robustness and Degradation Awareness

### 9.1 CHAOS Benchmark

The CHAOS benchmark (2025) evaluates MLLMs against 5 textual and 10 visual perturbation types at three severity levels, including label removal, color shifts, noise injection, and occlusion. Models show 40--60% drops in accuracy on corrupted charts.

### 9.2 CHART NOISe

Bendeck et al. (2025) evaluate VLM robustness under chart corruption and occlusion, finding that models fabricate values, misinterpret trends, and confuse entities under degradation---while remaining overconfident.

**Gap**: Our adversarial blur experiments partially address this, but we do not systematically evaluate whether models *acknowledge* degraded or missing information. A model that says "the y-axis label is not visible" when it has been blurred out is behaving correctly, but our current framework has no mechanism to reward such epistemic honesty.

---

## 10. Additional MQM Dimensions From Translation Quality

The full MQM framework (Lommel et al., 2014) includes eight top-level dimensions. We use three. The remaining five are:

| MQM Dimension | Relevance to Chart Description |
|---------------|-------------------------------|
| **Terminology** | Using correct domain-specific terms (e.g., "median" vs. "mean", "bar" vs. "column") |
| **Locale Convention** | Formatting numbers, dates, and units correctly for the target locale (e.g., comma vs. period as decimal separator) |
| **Style** | Register appropriateness, consistent tone, audience-appropriate language |
| **Verity** | Whether claims can be verified against the source (closely related to grounding) |
| **Design** | Structural and formatting quality of the output text |

**Gap**: Of these, **Terminology** and **Verity** are most relevant:
- *Terminology*: Models frequently confuse chart-type terminology (calling a grouped bar chart a "stacked bar chart"), statistical terms ("average" vs. "median"), and visual encoding terms. These errors are qualitatively different from factual inaccuracies.
- *Verity*: Whether each claim in the description can be independently verified by examining the chart. This is the MQM analog of the "grounding" dimension discussed in Section 4.

---

## 11. Accessibility-Specific Dimensions

### 11.1 W3C WAI Guidelines

W3C WAI (WCAG 2.1, Guideline 1.1.1) requires that complex images like charts have both a short text alternative and a detailed description. Evaluation criteria include:
- **Conciseness**: The alt text should be the most concise description possible of the image's purpose.
- **Information priority**: Most important information first.
- **Functional purpose**: The description must serve the user's task, not merely catalog visual elements.

**Gap**: We do not evaluate *information ordering*---whether the most important findings appear first. For accessibility, front-loading key takeaways is critical because screen reader users process text sequentially.

### 11.2 Audience Adaptation

Lundgard and Satyanarayan (2022) found that blind and sighted readers have different preferences: blind readers valued Level 2 (statistical) content more highly, while sighted readers preferred Level 3 (trends/patterns). Both groups found Level 4 (contextual interpretation) less useful.

**Gap**: Our evaluation is audience-agnostic. Depending on whether the description is for a sighted reader (who can see the chart and wants a textual summary) or a blind reader (for whom the description *is* the chart), different content priorities apply.

---

## 12. Summary of Recommended Additions

Ranked by estimated impact on evaluation discriminativeness and analytical value:

| Priority | Dimension | Implementation Complexity | Rationale |
|----------|-----------|--------------------------|-----------|
| **High** | Error sub-typing (value/label/trend/magnitude/out-of-context) | Low: annotate within existing Accuracy items | Enables root-cause analysis of model failures (CHOCOLATE; Huang et al., 2024) |
| **High** | Consistency (internal contradictions) | Low: add as global constraint | Catches a common failure mode not currently penalized |
| **High** | Semantic level tagging (L1/L2/L3) | Low: tag existing checklist items | Enables level-specific analysis (Lundgard & Satyanarayan, 2022; VisText) |
| **Medium** | Spatial reasoning quality | Medium: add checklist items for ordering and relative position | Distinct failure mode from value accuracy (ChartInsights; CharXiv) |
| **Medium** | Numerical precision vs. accuracy | Medium: separate scoring criteria | Distinguishes honest hedging from false precision (ChartQA relaxed accuracy) |
| **Medium** | Multi-panel handling | Medium: extend checklist for compound figures | Our dataset likely contains multi-panel figures (MultiChartQA; SciFIBench) |
| **Medium** | Grounding / verifiability | High: requires tracing claims to visual evidence | Important for adversarial experiments (ChartAnchor; Masry et al., 2024) |
| **Low** | Analytical task coverage (outliers, distribution, clusters) | Low: add checklist items | Currently implicit; making explicit improves coverage (ChartInsights) |
| **Low** | Information ordering | Low: add global constraint | Accessibility best practice (W3C WAI) |
| **Low** | Terminology correctness | Low: add as error sub-type | Distinct from factual errors (MQM Terminology dimension) |

---

## References

- Amar, R., Eagan, J., and Stasko, J. (2005). Low-Level Components of Analytic Activity in Information Visualization. *IEEE Symposium on Information Visualization (InfoVis)*.
- Bendeck, A., et al. (2025). CHART NOISe: Evaluating VLM Robustness Under Chart Corruption and Occlusion. *Preprint*.
- CHAOS Authors (2025). CHAOS: Chart Analysis with Outlier Samples. *arXiv:2505.17235*.
- Cui, Y., et al. (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. *arXiv:2509.17481*.
- Huang, K.-H., Zhou, M., Chan, H. P., Fung, Y., Wang, Z., Zhang, L., Chang, S.-F., and Ji, H. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. *Findings of ACL 2024*.
- Lommel, A., Uszkoreit, H., and Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics. *Language Resources and Evaluation*.
- Lundgard, A. and Satyanarayan, A. (2022). Accessible Visualization via Natural Language Descriptions: A Four-Level Model of Semantic Content. *IEEE Transactions on Visualization and Computer Graphics*, 28(1).
- Masry, A., Long, D., Tan, J. Q., Joty, S., and Hoque, E. (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. *Findings of ACL 2022*.
- Masry, A., et al. (2024). ChartAnchor: Chart Grounding with Structural-Semantic Fidelity. *arXiv:2512.01017*.
- Methani, N., Ganguly, P., Khapra, M. M., and Kumar, P. (2020). PlotQA: Reasoning over Scientific Plots. *WACV 2020*.
- Pandey, A. V., et al. (2025). Benchmarking Visual Language Models on Standardized Visualization Literacy Tests. *Computer Graphics Forum (EuroVis 2025)*.
- Rahman, M., et al. (2023). ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization of Long and Short Summaries. *Canadian Conference on Artificial Intelligence (Canadian AI 2023)*.
- Roberts, J., et al. (2024). SciFIBench: Benchmarking Large Multimodal Models for Scientific Figure Interpretation. *NeurIPS 2024 Datasets and Benchmarks Track*.
- Tang, B., Boggust, A., and Satyanarayan, A. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. *ACL 2023*.
- Wang, Z., et al. (2024a). CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs. *NeurIPS 2024 Datasets and Benchmarks Track*.
- Wang, Z., et al. (2024b). ChartInsights: Evaluating Multimodal Large Language Models for Low-Level Chart Question Answering. *Findings of EMNLP 2024*.
- Xia, R., et al. (2024). ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning. *IEEE Transactions on Pattern Analysis and Machine Intelligence*.
- Xu, Z., et al. (2024). ChartBench: A Benchmark for Complex Visual Reasoning in Charts. *arXiv:2312.15915*.
- Zhu, Y., et al. (2025). MultiChartQA: Benchmarking Vision-Language Models on Multi-Chart Problems. *NAACL 2025*.
- W3C. (2018). Web Content Accessibility Guidelines (WCAG) 2.1. *W3C Recommendation*.
- W3C MQM Community Group. (2018). Multidimensional Quality Metrics (MQM) Issue Types. *W3C Community Group Draft*.
