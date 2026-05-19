# VLM Description Tasks for Pie Charts in Scientific Figures

A comprehensive survey of challenges, evaluation strategies, and best practices for Vision-Language Model (VLM) description of pie charts, with emphasis on scientific figure contexts.

---

## 1. What Makes Pie Chart Description Challenging for VLMs

### 1.1 Angle and Area Estimation

Pie charts encode data as angular sectors whose areas are proportional to underlying values. This representation is notoriously difficult for VLMs. Rahmanzadehgervi et al. (2024) demonstrated in their BlindTest benchmark that state-of-the-art VLMs, including GPT-4o and Gemini 1.5 Pro, achieve only 58.07% average accuracy on elementary geometric tasks -- tasks that require spatial reasoning fundamentally similar to pie chart interpretation. Claude 3.5 Sonnet performed best at 77.84%, still far below human-level performance. Their linear probing experiments revealed that vision encoders contain sufficient visual information to solve such tasks, but the language decoder fails to translate fine-grained geometric features into correct textual descriptions. This encoder-decoder gap is central to pie chart description failures: the visual signal for a 23% slice versus a 27% slice may be adequately captured by the vision encoder, but the language model cannot reliably decode the distinction.

The fundamental problem is that VLMs lack explicit mechanisms for angular measurement. Unlike bar charts (where heights map to a linear scale with gridlines) or line charts (where values can be read from axis intersections), pie charts require estimating angles or areas relative to a full circle -- a task with no discrete visual anchors. Xia et al. (2024) showed in StructChart that converting chart perception to structured triplet representations (e.g., slice-label, slice-percentage pairs) significantly improves downstream reasoning, suggesting that the unstructured nature of pie chart visual encoding is itself a core bottleneck.

Wu et al. (2024) found in ChartInsights that across 19 multimodal LLMs evaluated on low-level chart analysis tasks spanning 7 chart types, average accuracy was only 39.8%, with pie charts consistently among the hardest chart types. GPT-4o, the top performer, reached only 69.17% overall, and accuracy dropped further on tasks requiring precise value extraction from proportional representations.

### 1.2 Small Slices That Are Hard to Distinguish

Scientific pie charts frequently contain slices representing small percentages (1-5%), which occupy minimal angular extent. At 1%, a slice subtends only 3.6 degrees of arc. VLMs struggle to detect, count, and label such slices. The ChartHal benchmark (Wang et al., 2025) found that questions involving information absent from or contradictory to charts are especially likely to trigger hallucinations -- and small slices that are nearly invisible are a prime source of such failures. Models either omit small slices entirely or hallucinate their presence when they do not exist.

The CHART NOISe benchmark (Shin et al., 2025) demonstrated that even minor visual degradation (corruption or occlusion) causes sharp performance drops in GPT-4o, Claude Sonnet, and Gemini 2.5 Pro, with models inventing values and misreading data. Small pie slices are functionally similar to partially occluded data: the visual signal is weak, and models default to confabulation.

### 1.3 Similar Colors for Adjacent Slices

Color discrimination is a persistent weakness of VLMs. When adjacent slices in a pie chart use similar hues (e.g., light blue vs. medium blue, or two shades of green), models frequently misattribute labels to the wrong slices. Huang et al. (2024) documented in their CHOCOLATE dataset that color-to-label mapping errors are a major category of factual inaccuracy in VLM-generated chart captions, even for GPT-4V. The problem is compounded in scientific figures, which often use colorblind-friendly palettes with limited hue variation, or institutional color schemes with subtle distinctions.

ChartGaze (Salamatian et al., 2025) showed that LVLMs frequently diverge from human gaze patterns when processing charts, attending to irrelevant regions rather than discriminating between visually similar elements. Their gaze-guided attention refinement improved accuracy by up to 2.56 percentage points, suggesting that attentional misallocation contributes to color confusion errors.

### 1.4 Nested and Donut Charts

Donut charts (pie charts with a hollow center) and nested/multi-ring charts add complexity by introducing concentric rings of data. VLMs must distinguish which ring a slice belongs to, track labels across rings, and understand the hierarchical relationship between inner and outer rings. The ChartX benchmark (Xia et al., 2024b) covers 18 chart types including donut and nested variants, and found that model performance degrades substantially on compound chart types compared to simple single-ring pie charts. The visual complexity of multi-ring encodings exceeds what current VLM architectures handle reliably, as there are no explicit visual separators between data series beyond ring boundaries.

### 1.5 3D Pie Charts and Perspective Distortion

3D pie charts introduce perspective projection that systematically distorts area perception. Slices in the front of a 3D pie appear larger than equally-valued slices in the back. This is a well-documented problem in visualization research (see Cleveland and McGill's seminal work on graphical perception, extended in modern contexts by Heer and Bostock, 2010). For VLMs, 3D rendering adds foreshortening, shadow, and occlusion artifacts that further confuse proportional estimation. The DCQA benchmark (Wu et al., 2024b) includes varied chart style variations specifically to test robustness to such rendering differences, and found that 3D rendering consistently degrades QA accuracy.

Zhang et al. (2026) showed in their misleading chart QA work (ChartCynics) that deceptive visual encodings -- including 3D perspective distortion -- cause VLMs to produce answers that align with the visual distortion rather than the true data. Their dual-path framework, which separates visual anomaly detection from numerical grounding, improved robustness by approximately 29%, indicating that VLMs are as susceptible to 3D chart illusions as human viewers.

### 1.6 Label Placement Challenges

Pie charts use diverse labeling strategies: labels inside slices, labels outside with leader lines, legends with color keys, or combinations thereof. Each placement strategy creates different challenges:

- **Inside labels**: May be rotated, small, or occluded by the slice boundary. VLM OCR capabilities degrade for rotated or curved text.
- **Outside labels with leader lines**: Require the model to trace a thin line from the label to the correct slice -- a spatial reasoning task that VLMs handle poorly (Rahmanzadehgervi et al., 2024).
- **Legend-based labeling**: Requires matching colors between the legend and pie slices, compounding the color discrimination problem described above.

Masry et al. (2024) in ChartInstruct found that instruction-tuned models improve substantially on charts with explicit textual labels but still struggle when labels must be inferred from legends or spatial proximity.

### 1.7 Exploded and Offset Slices

Exploded pie charts separate one or more slices from the main circle for emphasis. This introduces spatial gaps that VLMs may misinterpret as additional chart elements, boundaries, or separate visual objects. The FigureQA dataset (Kahou et al., 2018) includes pie charts among its five figure types and tests relationships between plot elements, but does not specifically address exploded variants. Current benchmarks under-represent exploded pie charts, meaning VLMs have limited training signal for this configuration. In practice, exploded slices alter the visual centroid of the chart and can cause models to misjudge relative sizes, as the displaced slice loses its angular context.

---

## 2. What Should a Complete Pie Chart Description Contain

### 2.1 Survey of Benchmark Expectations

Existing benchmarks set varying standards for pie chart descriptions:

- **ChartQA** (Masry et al., 2022): Focuses on question-answering rather than full descriptions. Questions probe specific values, comparisons, and arithmetic reasoning about chart data. For pie charts, this means questions like "What percentage does category X represent?" or "Which category is the largest?"
- **ChartSumm** (Rahman et al., 2023): Requires both brief and extended summaries of chart content from 84,363 charts. Summaries should capture the overall message, key data points, and notable patterns.
- **Chart-to-Text** tasks evaluated in UniChart (Masry et al., 2023) and ChartLlama (Han et al., 2023): Expect natural language descriptions that enumerate key visual elements and their relationships.
- **SciCap** (Hsu et al., 2021): Targets scientific figure captioning from 2M+ figures, expecting captions that convey the figure's scientific purpose and key findings.
- **CHOCOLATE** (Huang et al., 2024): Evaluates factual consistency of chart captions, establishing that complete descriptions must be verifiably accurate with respect to the source chart.

The NLG for Visualizations survey (Hoque and Islam, 2024) categorizes text generation for visualizations along five dimensions (who, what, why, how, when), establishing that complete descriptions should address the visualization's purpose, content, and context.

### 2.2 Content Elements for a Complete Pie Chart Description

Based on the synthesis of benchmark requirements and evaluation frameworks, a complete pie chart description should include:

1. **Purpose/Title**: What the pie chart represents (e.g., "Distribution of research funding by discipline in 2023").

2. **Total number of slices**: The count of distinct categories represented.

3. **Per-slice information** (for each slice):
   - **Label**: The category name.
   - **Color**: The visual encoding used (critical for accessibility and verification).
   - **Value**: The percentage or absolute value, if displayed.
   - **Relative size**: Qualitative description if exact values are not labeled (e.g., "approximately one-quarter," "the largest slice").

4. **Ordering**: How slices are arranged (typically clockwise from 12 o'clock; the description should note the ordering convention and sequence).

5. **Legend**: Description of the legend if present, including position and mapping.

6. **Emphasis**: Any visual emphasis (exploded slices, bold labels, highlighting) and what it signifies.

7. **Source/annotation**: Any source attribution, footnotes, or annotations visible on the chart.

8. **Key takeaway**: The dominant pattern (e.g., "Category A dominates at 45%, while the remaining four categories each contribute between 10-15%").

### 2.3 Precision: Estimated vs. Exact Percentages

The question of acceptable precision depends on whether the pie chart displays explicit percentage labels:

- **Charts with explicit percentage labels**: The description must reproduce the exact values. Any deviation constitutes a factual error. The CHOCOLATE framework (Huang et al., 2024) and CHARTVE visual entailment model treat such deviations as hallucinations.

- **Charts without percentage labels**: Estimation is necessary. The StructChart metric (SCRM) by Xia et al. (2023) provides a framework for evaluating perception accuracy with tolerances. In visualization research, human estimation accuracy for pie chart angles is approximately +/-5% for slices above 10% and degrades to +/-10% or worse for smaller slices (as documented in Cleveland and McGill's graphical perception studies and their modern extensions).

- **Hybrid charts**: Some pie charts display percentages for large slices but not small ones. Descriptions should state exact values where available and clearly signal when values are estimated.

### 2.4 Handling Pie Charts Without Percentage Labels

When percentage labels are absent, VLMs must estimate proportions from visual angles. Best practice from evaluation benchmarks:

- State estimates explicitly as approximations (e.g., "approximately 30%").
- Round to the nearest 5% for slices above 10%; to the nearest 1-2% for slices below 10%.
- Ensure all stated percentages sum to approximately 100% (within a tolerance of +/-2-3%).
- Cross-reference with any gridlines, reference circles, or tick marks if present.

The DePlot approach (Liu et al., 2023) converts charts to linearized tables, effectively forcing explicit value extraction. When applied to pie charts, this two-stage approach (visual-to-table, then table-to-text) avoids the direct estimation problem but introduces its own errors at the conversion stage.

---

## 3. Common VLM Errors on Pie Charts

### 3.1 Percentage Hallucination

The most frequently documented error. VLMs state specific percentages that do not match the chart data. Huang et al. (2024) found in the CHOCOLATE study that GPT-4V "frequently produces captions laced with factual inaccuracies," with percentage hallucination being a primary error type. The ChartHal benchmark (Wang et al., 2025) quantified this systematically, finding that even GPT-5 achieved only 34.46% accuracy on their hallucination detection tasks, and o4-mini scored 22.79%.

Percentage hallucination is especially severe for pie charts because:
- There are no axis scales to anchor estimates.
- The model may rely on memorized statistical priors (e.g., defaulting to round numbers like 25%, 33%, 50%) rather than visual evidence.
- Similar-sized slices may be assigned identical percentages when they differ by small amounts.

The ChartSumm benchmark (Rahman et al., 2023) noted that baseline models generate "fabricated information" and overlook key data values, confirming that hallucination is a systemic problem across architectures.

### 3.2 Failing to Count All Slices

VLMs frequently undercount slices, particularly missing small slices or slices with similar colors to adjacent segments. This is consistent with the broader counting deficit documented in BlindTest (Rahmanzadehgervi et al., 2024), where VLMs failed at counting overlapping geometric shapes. For pie charts, the counting problem is exacerbated when slices are unlabeled or when multiple small slices cluster together.

### 3.3 Confusing Similar-Sized Slices

When two or more slices have similar proportions (e.g., 18% vs. 20%), VLMs may:
- Swap their labels.
- Report them as identical.
- Assign the wrong ranking (e.g., stating the smaller slice is larger).

ChartInsights (Wu et al., 2024) found that comparison tasks ("which is larger?") are among the most error-prone for multimodal LLMs across all chart types, with pie charts being particularly affected due to the difficulty of angular comparison.

### 3.4 Wrong Color-to-Label Mapping

As documented in CHOCOLATE (Huang et al., 2024), models frequently associate the wrong color with a category label, especially when:
- The legend is spatially separated from the chart.
- Multiple shades of the same hue are used.
- The chart uses a gradient color scheme.

### 3.5 Failing on Charts Without Explicit Percentage Labels

When charts lack numerical annotations, VLMs must estimate purely from visual proportions. Performance drops dramatically in this setting. The MatCha pretraining approach (Liu et al., 2023b) improved chart derendering capabilities, but the fundamental limitation remains: without explicit textual anchors, VLMs revert to rough estimation or memorized priors.

### 3.6 Ordering Errors

Pie charts typically present slices in a consistent order (largest to smallest, clockwise from 12 o'clock). VLMs frequently describe slices in an arbitrary order or misidentify which slice is positioned where. This is related to the spatial reasoning deficit identified by Rahmanzadehgervi et al. (2024) and the attention misallocation documented by ChartGaze (Salamatian et al., 2025).

### 3.7 Specific Model Weaknesses from Published Evaluations

| Model | Key Weakness on Charts | Source |
|-------|----------------------|--------|
| GPT-4V/4o | Factual inaccuracies in captions, overconfident incorrect percentages | Huang et al. (2024), Wang et al. (2025) |
| GPT-5 | 34.46% on hallucination detection | Wang et al. (2025) |
| Gemini 1.5 Pro | Poor geometric reasoning (BlindTest) | Rahmanzadehgervi et al. (2024) |
| Claude 3.5 Sonnet | Best on geometric reasoning (77.84%) but still below human level | Rahmanzadehgervi et al. (2024) |
| LLaVA (various) | Modest zero-shot chart performance; improves significantly with fine-tuning | Li and Tajbakhsh (2023) |
| All tested VLMs | Sharp degradation under chart corruption/occlusion; invent values, misread trends | Shin et al. (2025) |

---

## 4. Evaluation Strategies for Pie Chart Descriptions

### 4.1 MQM-Based Evaluation for Proportional Data

Multidimensional Quality Metrics (MQM) provide a structured error typology applicable to chart descriptions. For pie chart descriptions, an MQM-adapted framework should include:

- **Accuracy > Number**: Incorrect percentage or value stated for a slice.
- **Accuracy > Mistranslation**: Wrong label associated with a slice.
- **Accuracy > Addition**: Slice mentioned that does not exist in the chart.
- **Accuracy > Omission**: Slice present in the chart but not mentioned.
- **Accuracy > Ordering**: Slices described in wrong spatial or ranking order.
- **Fluency > Style**: Description is grammatical but uses misleading language (e.g., "dominates" for a 30% slice).
- **Terminology**: Incorrect use of chart-specific terms.

This framework aligns with the error typology in CHOCOLATE (Huang et al., 2024) and can be scored with severity weights (critical for factual errors like wrong percentages, minor for stylistic issues).

### 4.2 Tolerance for Percentage Estimation

Establishing appropriate tolerance thresholds is critical:

- **Charts with explicit labels**: Zero tolerance. Any deviation from the stated value is an error.
- **Charts without labels, slices >= 10%**: Tolerance of +/-3 percentage points, based on human perceptual accuracy benchmarks from visualization research.
- **Charts without labels, slices 5-10%**: Tolerance of +/-5 percentage points.
- **Charts without labels, slices < 5%**: Tolerance of +/-3 percentage points absolute (which represents a large relative error but reflects the inherent difficulty).
- **Sum constraint**: All estimated percentages should sum to 95-105%.

The SCRM metric from StructChart (Xia et al., 2023) provides a principled framework for evaluating chart perception accuracy with structured representations, and can be adapted for pie chart percentage estimation.

### 4.3 Completeness Evaluation

A completeness score for pie chart descriptions should measure:

- **Slice recall**: Fraction of true slices mentioned (target: 100%).
- **Label recall**: Fraction of true labels correctly stated.
- **Value recall**: Fraction of true values correctly stated (within tolerance).
- **Structural completeness**: Whether the description includes title, legend description, and ordering information.

The ChartVE visual entailment model (Huang et al., 2024) provides a learned approach to completeness evaluation by checking whether claims in a caption are entailed by the chart image.

### 4.4 Accuracy Evaluation

Accuracy evaluation for pie chart descriptions involves:

- **Value accuracy**: Mean absolute error (MAE) between stated and true percentages.
- **Ranking accuracy**: Whether the model correctly orders slices by size (Kendall's tau or Spearman correlation).
- **Label accuracy**: Exact match of label-to-value assignments.
- **Relational accuracy**: Correctness of comparative statements (e.g., "A is larger than B").

ChartInsights (Wu et al., 2024) uses task-specific accuracy metrics across 10 data analysis tasks, providing fine-grained evaluation that can be adapted for description tasks.

### 4.5 How Existing Benchmarks Handle Pie Chart Evaluation

- **ChartQA** (Masry et al., 2022): Uses relaxed accuracy with a 5% tolerance for numerical answers. For pie charts, a stated value of 23% when the true value is 25% would be considered correct.
- **FigureQA** (Kahou et al., 2018): Uses binary yes/no accuracy for relational questions about plots including pie charts.
- **ChartX** (Xia et al., 2024b): Evaluates across 7 chart tasks with multi-type coverage; pie charts are one of 18 chart types with per-type analysis.
- **CHOCOLATE** (Huang et al., 2024): Uses factual consistency scoring where each claim in a caption is verified against the source chart. Errors are classified by type and severity.
- **ChartHal** (Wang et al., 2025): Provides a fine-grained hallucination classification framework with 1,062 validated examples.
- **CHART NOISe** (Shin et al., 2025): Evaluates robustness under degraded conditions using exam-style multiple choice, including a "prompt reverse inconsistency" metric.

---

## 5. Best Practices for Prompting VLMs on Pie Charts

### 5.1 Prompt Strategies for Better Pie Chart Descriptions

Based on findings from ChartInsights (Wu et al., 2024), ChartInstruct (Masry et al., 2024), and the broader prompting literature:

1. **Enumerate explicitly**: Prompt the model to "List every slice in the pie chart, stating its label, color, and percentage." Explicit enumeration instructions reduce omission errors.

2. **Chain-of-Charts prompting**: Wu et al. (2024) introduced this strategy, which improved chart QA accuracy from ~40% to 83.58%. The approach guides the model through stepwise reasoning about chart elements before answering questions.

3. **Summation constraint**: Include in the prompt: "Ensure your stated percentages sum to 100%." This self-consistency check catches hallucinated values.

4. **Clockwise enumeration**: Instruct the model to "Describe slices in clockwise order starting from the 12 o'clock position." This imposes a spatial discipline that reduces ordering errors and helps ensure completeness.

5. **Separate perception from reasoning**: Following the VisDoT approach (Lee et al., 2026), first ask the model to describe what it sees (perception), then ask it to interpret the data (reasoning). This two-stage approach reduces hallucination.

6. **Visual prompting**: Wu et al. (2024) found that combining textual prompts with visual annotations (e.g., highlighted regions) improved accuracy to 84.32%. For pie charts, this could involve overlaying grid lines or angular reference marks.

### 5.2 How to Elicit Percentage Estimates When Labels Are Absent

When a pie chart lacks percentage annotations:

1. **Reference-point anchoring**: "The largest slice appears to be approximately what fraction of the whole circle? Is it closer to 1/4, 1/3, or 1/2?"

2. **Pairwise comparison first**: "Compare each pair of slices: which is larger? By how much?" This builds a relative ordering before absolute estimation.

3. **DePlot-style decomposition**: Use a two-stage approach where the first prompt asks the model to extract a data table from the chart, and the second prompt generates the description from the table. Liu et al. (2023) showed this dramatically improves accuracy on chart reasoning tasks.

4. **Explicit uncertainty marking**: "For each slice, state your estimated percentage and your confidence (high/medium/low)." This calibrates the model and signals to downstream consumers which values are reliable.

5. **Cross-validation prompt**: "After listing all percentages, verify that they sum to 100%. If they don't, adjust your estimates proportionally."

### 5.3 Structured Output for Slice Enumeration

Requesting structured output (JSON, markdown table) improves completeness and reduces hallucination:

```
Describe this pie chart in the following JSON format:
{
  "title": "...",
  "total_slices": N,
  "slices": [
    {
      "rank": 1,
      "label": "...",
      "color": "...",
      "percentage": ...,
      "is_estimated": true/false,
      "position": "clockwise position from 12 o'clock"
    }
  ],
  "legend_present": true/false,
  "source": "...",
  "key_finding": "..."
}
```

This approach aligns with the Structured Triplet Representation framework from StructChart (Xia et al., 2023) and the chart-to-table paradigm from DePlot (Liu et al., 2023) and ChartAssistant (Meng et al., 2024). Structured output forces the model to commit to specific claims for each slice, making omissions and inconsistencies immediately apparent.

The ChartCards framework (Wu et al., 2026) provides a metadata generation approach for charts that produces organized, structured descriptions supporting multiple downstream tasks, validating the utility of structured output for chart understanding.

---

## 6. References

### Core VLM Blindness and Limitations

1. Rahmanzadehgervi, P., Bolton, L., Taesiri, M. R., & Nguyen, A. T. (2024). Vision Language Models Are Blind. *arXiv:2407.06581*. Demonstrates VLMs achieve only 58% accuracy on elementary geometric tasks in the BlindTest benchmark.

### Chart Understanding Benchmarks

2. Masry, A., Long, D. X., Tan, J. Q., Joty, S., & Hoque, E. (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. *Findings of ACL 2022*. arXiv:2203.10244. Benchmark with 9.6K human-written and 23.1K machine-generated QA pairs.

3. Kahou, S. E., Michalski, V., Atkinson, A., Kadar, A., Trischler, A., & Bengio, Y. (2018). FigureQA: An Annotated Figure Dataset for Visual Reasoning. *arXiv:1710.07300*. Over 1M QA pairs on synthetic figures including pie charts.

4. Xia, R., Zhang, B., Ye, H., Yan, X., Liu, Q., Zhou, H., Chen, Z., Ye, P., Dou, M., Shi, B., Yan, J., & Qiao, Y. (2024b). ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning. *arXiv:2402.12185*. Multi-modal evaluation covering 18 chart types and 7 tasks.

5. Wu, Y., Yan, L., Shen, L., Wang, Y., Tang, N., & Luo, Y. (2024). ChartInsights: Evaluating Multimodal Large Language Models for Low-Level Chart Question Answering. *EMNLP 2024*. arXiv:2405.07001. 22,347 QA pairs across 10 tasks and 7 chart types.

6. Wu, A., Xiao, L., Wu, X., Yang, S., Xu, J., Zhuang, Z., Xie, N., Jin, C., & He, L. (2024b). DCQA: Document-Level Chart Question Answering towards Complex Reasoning and Common-Sense Understanding. *arXiv:2310.18983*. 50K documents with 699K questions.

7. Li, S. & Tajbakhsh, N. (2023). SciGraphQA: A Large-Scale Synthetic Multi-Turn Question-Answering Dataset for Scientific Graphs. *arXiv:2308.03349*. 295K multi-turn QA dialogues about academic graphs.

### Chart Hallucination and Factual Accuracy

8. Huang, K.-H., Zhou, M., Chan, H. P., Fung, Y. R., Wang, Z., Zhang, L., Chang, S.-F., & Ji, H. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. *Findings of ACL 2024*. arXiv:2312.10160. Introduces CHOCOLATE error typology and CHARTVE visual entailment.

9. Wang, X., Cui, Y., Yao, X., Wang, S., Hu, G., & Qin, X. (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. *arXiv:2509.17481*. GPT-5 achieves only 34.46% on hallucination detection.

10. Shin, P. W., Sampson, J., Narayanan, V., Marquez, A., & Halappanavar, M. (2025). CHART NOISe: Losing the Plot -- How VLM Responses Degrade on Imperfect Charts. *arXiv:2509.18425*. Benchmark for VLM robustness under chart corruption and occlusion.

### Chart-Specific Models and Pretraining

11. Liu, F., Eisenschlos, J. M., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Chen, W., Collier, N., & Altun, Y. (2023). DePlot: One-shot Visual Language Reasoning by Plot-to-Table Translation. *arXiv:2212.10505*. Two-stage chart-to-table-to-answer pipeline.

12. Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Altun, Y., Collier, N., & Eisenschlos, J. M. (2023b). MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering. *ACL 2023*. arXiv:2212.09662. Improves chart understanding by ~20% on PlotQA and ChartQA.

13. Lee, K., Joshi, M., Turc, I., Hu, H., Liu, F., Eisenschlos, J., Khandelwal, U., Shaw, P., Chang, M.-W., & Toutanova, K. (2023). Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding. *arXiv:2210.03347*. Foundation model for visually-situated language.

14. Masry, A., Kavehzadeh, P., Do, X. L., Hoque, E., & Joty, S. (2023). UniChart: A Universal Vision-language Pretrained Model for Chart Comprehension and Reasoning. *arXiv:2305.14761*. Chart-grounded pretraining for unified chart understanding.

15. Han, Y., Zhang, C., Chen, X., Yang, X., Wang, Z., Yu, G., Fu, B., & Zhang, H. (2023). ChartLlama: A Multimodal LLM for Chart Understanding and Generation. *arXiv:2311.16483*. Instruction-tuned LLM for chart comprehension.

16. Masry, A., Shahmohammadi, M., Parvez, M. R., Hoque, E., & Joty, S. (2024). ChartInstruct: Instruction Tuning for Chart Comprehension and Reasoning. *arXiv:2403.09028*. 191K chart instruction-following dataset.

17. Meng, F., Shao, W., Lu, Q., Gao, P., Zhang, K., Qiao, Y., & Luo, P. (2024). ChartAssistant: A Universal Chart Multimodal Language Model via Chart-to-Table Pre-training and Multitask Instruction Tuning. *arXiv:2401.02384*. Two-stage chart-to-table then instruction-following training.

### Chart Captioning and Summarization

18. Rahman, R., Hasan, R., Farhad, A. A., Laskar, M. T. R., Ashmafee, M. H., & Kamal, A. R. M. (2023). ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization of Long and Short Summaries. *Canadian AI 2023*. arXiv:2304.13620. 84,363 charts with metadata and descriptions.

19. Hsu, T.-Y., Giles, C. L., & Huang, T.-H. K. (2021). SciCap: Generating Captions for Scientific Figures. *Findings of EMNLP 2021*. arXiv:2110.11624. 2M+ scientific figures from 290K arXiv papers.

20. Hoque, E. & Islam, M. S. (2024). Natural Language Generation for Visualizations: State of the Art, Challenges and Future Directions. *arXiv:2409.19747*. Comprehensive survey of NLG for data visualizations.

### Chart Perception, Attention, and Evaluation Metrics

21. Xia, R., Peng, H., Ye, H., Li, M., Yan, X., Ye, P., Shi, B., Qiao, Y., Yan, J., & Zhang, B. (2023). StructChart: On the Schema, Metric, and Augmentation for Visual Chart Understanding. *arXiv:2309.11268*. Structured Triplet Representations and SCRM metric.

22. Salamatian, A., Abaskohi, A., Fan, W.-C., Hossain, M. R. I., Sigal, L., & Carenini, G. (2025). ChartGaze: Enhancing Chart Understanding in LVLMs with Eye-Tracking Guided Attention Refinement. *EMNLP 2025*. arXiv:2509.13282. Human gaze-guided attention for chart reasoning.

23. Baechler, G., Sunkara, S., Wang, M., Zubach, F., Mansoor, H., Etter, V., Carbune, V., Lin, J., Chen, J., & Sharma, A. (2024). ScreenAI: A Vision-Language Model for UI and Infographics Understanding. *arXiv:2402.04615*. 5B-parameter model achieving SOTA on infographic tasks.

### Misleading Charts and Robustness

24. Zhang, Y., Li, Y., Sheng, R., Chen, Z., Lin, Y., Qu, H., Chen, L., & Sun, Y. (2026). Navigating the Mirage: A Dual-Path Agentic Framework for Robust Misleading Chart Question Answering. *arXiv:2603.28583*. ~29% improvement on misleading chart robustness.

### Scientific Figure Understanding

25. Tao, H., Huang, C., Wang, N., Lyu, H., Zhang, L., Ke, G., & Fang, X. (2026). OmniScience: A Large-scale Multi-modal Dataset for Scientific Image Understanding. *arXiv:2602.13758*. 1.5M figure-caption-context triplets across 10+ disciplines.

26. Yang, Z., Li, L., Lin, K., Wang, J., Lin, C.-C., Liu, Z., & Wang, L. (2023). The Dawn of LMMs: Preliminary Explorations with GPT-4V(ision). *arXiv:2309.17421*. Early comprehensive evaluation of GPT-4V multimodal capabilities.

27. Yue, X., et al. (2023). MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI. *arXiv:2311.16502*. 11.5K multimodal questions including charts across 30 image types.

28. Rojas, M. A. & Carranza, R. (2024). Enhancing Scientific Figure Captioning Through Cross-modal Learning. *arXiv:2406.17047*. Cross-modal approach to scientific chart title generation.

---

*This survey was compiled in May 2026 to support the SciFig-Evaluation project's analysis of VLM description quality on scientific figures, with particular emphasis on pie chart challenges relevant to the MQM-based evaluation framework.*
