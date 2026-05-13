# Counting Tasks in Scientific Figure Understanding: A Comprehensive Research Survey

## 1. What Counting Tests in Scientific Figures

### 1.1 Definition and Scope

Counting in the context of scientific chart and figure understanding refers to the ability of a Vision-Language Model (VLM) to enumerate discrete visual elements within a chart, plot, graph, or diagram. Unlike object counting in natural images (e.g., counting cars in a street scene), counting in scientific figures requires parsing structured visual encodings where elements carry semantic meaning tied to underlying data.

Counting tasks in scientific figures encompass the following categories:

- **Structural element counting**: Counting bars in a bar chart, slices in a pie chart, lines in a line plot, or nodes in a network diagram.
- **Data point counting**: Counting individual data markers (dots, crosses, squares) in scatter plots or line charts.
- **Legend and label counting**: Counting the number of legend entries, axis tick marks, or category labels.
- **Conditional counting**: Counting elements that meet a specific criterion, e.g., "How many bars exceed a value of 50?" or "How many data points fall below the regression line?"
- **Cross-panel counting**: Counting elements across multiple subplots or panels in a composite figure.
- **Intersection and overlap counting**: Counting intersections between lines, overlapping regions in Venn diagrams, or shared categories across grouped bar charts.
- **Threshold-based counting**: Counting elements above, below, or between specified value thresholds.
- **Categorical counting**: Counting the number of distinct categories, groups, or clusters represented in a visualization.

### 1.2 Why Counting Matters for VLM Evaluation

Counting is a foundational perceptual capability that underpins higher-order chart reasoning. If a model cannot reliably count the bars in a bar chart, it cannot be trusted to perform comparative reasoning ("Which category has the most bars?"), aggregation ("What is the average across all groups?"), or compositional analysis ("How do the distributions differ between panels?").

Counting tasks serve as a diagnostic probe for several VLM capabilities simultaneously:

1. **Visual grounding**: The model must correctly segment and identify discrete visual elements.
2. **Spatial reasoning**: Elements must be distinguished from backgrounds, axes, labels, and other non-data visual components.
3. **Numerical precision**: The model must produce an exact integer, leaving no room for vague or hedged responses.
4. **Compositional understanding**: For conditional or cross-panel counting, the model must integrate visual perception with logical reasoning.

As Masry et al. (2022) noted in ChartQA, counting is among the core operation types that chart questions require, alongside lookup, comparison, and arithmetic operations.

---

## 2. Known Failure Modes of Best VLMs

### 2.1 Systematic Counting Failures Across Models

Recent research has comprehensively documented that counting remains one of the weakest capabilities of state-of-the-art VLMs, even for the most capable models.

**VLMCountBench (Guo et al., 2025)** demonstrated that even with minimalist geometric shapes (triangles, circles, squares), VLMs fail dramatically at compositional counting. Key results:

- **Single-shape counting (Level 1)**: Best model (Qwen2.5-72B) achieved only 0.60 accuracy.
- **Two-shape compositional counting (Level 2)**: Accuracy dropped to approximately 0.50.
- **Three-shape compositional counting (Level 3)**: Accuracy fell further to 0.45.
- Even for counts between 1 and 20 -- trivial for humans -- VLMs consistently erred.
- Performance degraded with random color and size perturbations, indicating reliance on superficial visual shortcuts rather than genuine counting.

**"Good at Captioning, Bad at Counting" (Zhang and Wang, 2024)** at the CVPR EarthVision Workshop (Best Paper, ICLR ML4RS Workshop) showed:

- GPT-4V excels at high-level scene understanding (image captioning, landmark recognition) but fails at object counting and localization.
- On RSICD captioning, GPT-4V achieved RefCLIPScore of 0.75 (surpassing human annotators), yet counting accuracy was unsatisfactory.
- The dichotomy between captioning success and counting failure reveals that VLMs rely on holistic scene understanding rather than precise spatial analysis.

**VLMs Are Biased (2024-2025)** research found:

- VLMs achieve 100% accuracy counting features on standard images of familiar objects but only approximately 17% accuracy on counterfactual images.
- Models default to memorized knowledge: they report "2 legs" for 3-legged birds and "4 legs" for 5-legged mammals, regardless of what the image actually shows.
- This confirms severe confirmation bias where training priors override visual evidence.

### 2.2 Model-Specific Failure Patterns

#### GPT-4V / GPT-4o
- Excels at captioning and qualitative description but struggles with precise counting (Zhang and Wang, 2024).
- On ChartQA augmented questions, GPT-4o achieves 88% baseline accuracy on clean charts but drops to below 60% under blur or occlusion corruptions (Losing the Plot, 2025).
- Exhibits value fabrication: generating plausible but incorrect numerical values when chart elements are degraded.
- Remains overconfident, producing plausible explanations even when charts are visually indecipherable.

#### Claude Sonnet
- Achieves 76% baseline accuracy on clean charts (Losing the Plot, 2025).
- Under major motion blur, accuracy drops to 45%.
- Contrast corruption reduces accuracy from 76% to 57%.
- Tends toward entity confusion: misidentifying which chart element corresponds to which category.

#### Gemini Pro / Flash
- Gemini 2.5 Pro achieves highest baseline chart accuracy at 88% (Losing the Plot, 2025).
- Still exhibits sharp performance drops under corruption and occlusion.
- On counting and spatial reasoning tasks, results are mixed; Gemini Flash generally leads on raw count QA but remains unreliable for compositional counting.

#### LLaVA / Open-Source Models
- LLaVA-v1.5 faces significant challenges in accurately identifying and counting objects, particularly in complex scenes with overlapping or small elements (Visual Haystacks, 2024).
- Performance degrades significantly as visual complexity increases (more distractors, more objects).
- Open-source models generally perform worse than proprietary models on counting tasks.

### 2.3 Specific Failure Patterns

1. **Overcounting**: Models hallucinate additional elements, particularly when chart elements are densely packed or overlap. This is related to the multi-object hallucination phenomenon documented by Chen et al. (NeurIPS 2024), where models invent nonexistent objects.

2. **Undercounting**: Models miss elements that are small, partially occluded, or share similar colors with backgrounds. In scientific charts, thin lines, small markers, and low-contrast elements are frequently missed.

3. **Boundary miscounting**: When elements are near visual boundaries (edges of axes, overlapping bar edges), models struggle to determine whether adjacent elements are one or two distinct items.

4. **Fabrication of elements**: VLMs generate plausible but entirely fabricated counts, particularly under degraded visual conditions. The "Losing the Plot" study found models remain overconfident, generating answers from incomplete data without acknowledging occlusions.

5. **Off-by-one errors on thresholds**: When counting elements above or below a threshold, models frequently err at boundary cases (elements exactly at the threshold value). This stems from imprecise value estimation from visual position.

6. **Confirmation bias / memorization**: Models default to statistically common counts from training data rather than performing visual analysis (VLMs Are Biased, 2024).

### 2.4 Root Causes

#### ViT Patch Embedding Compression
Vision Transformers divide images into patches (typically 16x16 or 32x32 pixels), converting spatial information into sequence tokens. This fundamentally changes how spatial information is processed: the image transforms from a spatial grid into a sequence of patch vectors, losing fine-grained positional relationships between visual elements. Smaller patches increase computational cost while larger patches lose detail -- a fundamental trade-off that directly impacts counting precision. Recent work on multi-resolution patch strategies (8x8, 16x16, 32x32) and ViT-CoMer (CVPR 2024) attempts to address this through convolutional multi-scale feature interaction.

#### CLIP Training Objective
Many VLMs use CLIP-based vision encoders trained on image-caption pairs through contrastive learning. This training objective incentivizes holistic scene understanding and semantic matching but does not reward precise counting, spatial localization, or fine-grained numerical reasoning. The internet-scale caption data used for CLIP training contains limited spatial and quantitative information, creating a fundamental dataset limitation.

#### The Binding Problem
Grounded in cognitive psychology, the binding problem (NeurIPS 2024) manifests in VLMs as failures in correctly associating visual features (shape, color) and spatial properties (location, size) with the right objects. Models may recognize individual elements correctly but confuse or conflate their attributes when multiple objects are present. This directly impacts compositional counting: the model can perceive "there are circles and triangles" but cannot maintain separate counts for each. Serial processing mechanisms that humans use for binding are poorly approximated by the parallel attention mechanisms in transformers.

#### Vision-Language Handoff
During the transition from visual features to language tokens, coordinate and spatial information is progressively abstracted away. By the time the language model generates a count, the precise spatial layout has been compressed into semantic representations that no longer distinguish individual elements reliably.

---

## 3. Best Question Design Strategies

### 3.1 Principles for Good Counting Questions

A well-designed counting question for scientific figures should:

1. **Have an unambiguous ground truth**: The correct count must be deterministic from the image alone, with no dependence on interpretation.
2. **Target a specific visual element type**: Avoid questions that conflate different element types (e.g., "How many elements are in the chart?" is too vague).
3. **Specify the counting scope clearly**: Indicate whether to count across all panels, within a specific region, or under specific conditions.
4. **Vary in difficulty systematically**: Include questions ranging from trivial to challenging to create a discriminative evaluation.
5. **Control for confounds**: Ensure that color, size, label presence, and visual clutter are deliberately varied to test robustness.

### 3.2 Difficulty Calibration

#### Easy (Level 1): Direct Structural Counting
- Count all bars in a simple bar chart (typically 3-8 bars).
- Count all slices in a pie chart.
- Count the number of lines in a line plot.
- Count legend entries.
- These test basic visual segmentation with minimal reasoning.

#### Medium (Level 2): Conditional Counting
- Count bars above/below a specific y-axis value.
- Count data points in a specific quadrant of a scatter plot.
- Count categories with values exceeding a threshold.
- Count the number of colors used in the chart.
- These require integrating visual perception with value estimation.

#### Hard (Level 3): Cross-Panel and Compositional Counting
- Count total bars across all subplots in a multi-panel figure.
- Count the number of panels where a specific trend appears.
- Count intersections between two plotted lines.
- Count elements meeting compound conditions (e.g., "bars that are both above 50 and belong to Category A").
- These require sustained attention across complex visual layouts.

#### Expert (Level 4): Edge Cases and Adversarial
- Count elements in densely packed visualizations (>20 elements).
- Count overlapping data points in scatter plots.
- Count zero-count categories (categories present in the legend but with zero-height bars).
- Count elements in charts with deliberately misleading visual features (dual axes, broken axes, non-zero baselines).

### 3.3 Cross-Panel Counting

Multi-panel figures are common in scientific literature and present unique counting challenges:

- **Aggregation across panels**: "How many total bars appear across all four subplots?"
- **Comparative panel counting**: "In how many panels does the blue line exceed the red line?"
- **Panel identification**: "How many subplots contain more than 5 data points?"

These questions test whether models can maintain consistent counting across spatially separated visual regions.

### 3.4 Conditional Counting

Conditional counting questions are particularly diagnostic because they require both:
1. Accurate value estimation (reading the y-axis position of each bar)
2. Correct application of a logical condition (above/below/between threshold)

Design considerations:
- Place the threshold at a visually unambiguous position (not between grid lines).
- Include elements near the boundary to test precision.
- Vary threshold positions: some conditions should yield zero counts, some should yield all-element counts, and most should yield partial counts.
- Use both explicit thresholds ("above 50") and relative thresholds ("above the mean").

### 3.5 Edge Cases

- **Overlapping elements**: Scatter plots with coincident data points; stacked bar charts where segment boundaries are unclear.
- **Very small counts (0-2)**: Zero counts are important -- models should be able to report "0" when no elements meet a condition.
- **Very large counts (15+)**: VLMCountBench showed accuracy degrades significantly beyond counts of ~10.
- **Ambiguous elements**: Error bars, confidence intervals, and annotations that might be confused with data elements.
- **Grouped/stacked bars**: Counting "bars" in a grouped bar chart is ambiguous -- specify whether to count individual bars or groups.

---

## 4. Evaluation Strategies

### 4.1 Exact Match vs. Tolerance-Based Scoring

**Exact Match** is the gold standard for counting tasks:
- Counting produces integer values; there is no legitimate reason for approximate answers.
- A count of 7 when the answer is 8 represents a genuine perceptual or reasoning failure.
- Exact match scoring (EM) provides the clearest signal about model capability.

**Tolerance-Based Scoring** (as used in ChartQA for numerical answers):
- ChartQA and PlotQA allow up to 5% tolerance for numeric answers, but this is designed for value extraction (reading axis values), not counting.
- For counting tasks specifically, tolerance should be minimal or zero.
- If tolerance is applied, use absolute tolerance (plus or minus 1) rather than relative tolerance, since a 5% tolerance on a count of 2 rounds to 0 (meaningless), while 5% on a count of 100 allows plus or minus 5 (too generous).

**Recommended approach for counting evaluation**:
- **Primary metric**: Exact match accuracy.
- **Secondary metric**: Mean absolute error (MAE) to capture severity of errors.
- **Diagnostic metric**: Directional bias (mean signed error) to detect systematic overcounting or undercounting.

### 4.2 Handling Ambiguous Visual Elements

Strategies for reducing ambiguity:

1. **Explicit element specification**: "How many blue bars are in the chart?" rather than "How many bars?"
2. **Ground truth validation**: Have multiple human annotators independently count; use only questions with unanimous agreement.
3. **Element-type disambiguation**: For grouped bar charts, specify "How many individual bar segments?" vs. "How many bar groups?"
4. **Exclusion criteria**: Clearly define what counts as a "bar" (do error bar caps count? do axis ticks count?).
5. **Visual clarity requirements**: Exclude charts where elements are genuinely ambiguous even to expert human viewers.

### 4.3 Answer Format Considerations

**Numeric-only format**:
- Preferred for automated evaluation.
- Prompt: "Answer with only a single integer."
- Reduces parsing complexity and eliminates evaluation noise from free-text interpretation.
- Risk: Models may refuse or add hedging language.

**Explanation-required format**:
- Prompt: "Count the [elements] and explain your reasoning step by step. End with 'Final answer: [number]'."
- Enables error analysis: Was the error in perception (misidentifying elements) or reasoning (miscounting identified elements)?
- Aligns with Chain-of-Chart-Reasoning (CCR) prompting strategies that have shown improved accuracy (up to 78.2% with few-shot CoT).
- Useful for understanding failure modes but harder to evaluate automatically.

**Recommended approach**: Use numeric-only format for scoring, but collect explanation traces for a subset of questions to support qualitative error analysis.

### 4.4 Prompt Engineering for Counting Evaluation

Based on research from PromptChart and related work:

- **Chain-of-thought prompting** consistently yields higher accuracy on counting questions (up to 78.2% vs. lower baselines with direct prompting).
- **Few-shot examples** improve format adherence and reduce refusal rates.
- **Task-specific prompt categorization**: Separate counting from other chart QA tasks, using dedicated prompt templates for counting operations.
- **Consistency testing**: Ask the same counting question with varied phrasing to assess robustness.

---

## 5. References

### Core Counting and VLM Evaluation Papers

1. **Guo, X., Huang, Z., Shi, Z., Song, Z., and Zhang, J.** (2025). "Your Vision-Language Model Can't Even Count to 20: Exposing the Failures of VLMs in Compositional Counting." arXiv:2510.04401. Submitted October 2025. *Introduces VLMCountBench; demonstrates compositional counting failures across VLMs with accuracy dropping from 0.60 (single shape) to 0.45 (three shapes) for the best model (Qwen2.5-72B).*

2. **Zhang, C. and Wang, Z.** (2024). "Good at Captioning, Bad at Counting: Benchmarking GPT-4V on Earth Observation Data." CVPR 2024 EarthVision Workshop; Best Paper at ICLR ML4RS Workshop. arXiv:2401.17600. *Demonstrates GPT-4V's strong captioning but poor counting and localization on Earth observation imagery.*

3. **Gupta, T., Vahdat, A., Chechik, G., Yang, X., Kautz, J., and Hoiem, D.** (2024). "Understanding the Limits of Vision Language Models Through the Lens of the Binding Problem." NeurIPS 2024. arXiv:2411.00238. *Frames VLM multi-object reasoning failures (counting, localization, analogy) through the cognitive science binding problem.*

4. **Chen, X. et al.** (2024). "Multi-Object Hallucination in Vision Language Models." NeurIPS 2024. *Examines how VLMs hallucinate, invent, or miss objects in multi-object settings using the ROPE benchmark.*

### Chart Understanding Benchmarks

5. **Masry, A., Long, D., Tan, J.Q., Joty, S., and Hoque, E.** (2022). "ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning." Findings of ACL 2022. arXiv:2203.10244. *9.6K human-written questions and 23.1K generated questions; introduces evaluation with 5% tolerance for numeric answers.*

6. **Methani, N., Ganguly, P., Khapra, M.M., and Kumar, P.** (2020). "PlotQA: Reasoning over Scientific Plots." WACV 2020. arXiv:1909.00997. *28.9M question-answer pairs over 224K plots from real-world data; 74 crowd-sourced question templates including counting operations.*

7. **Kafle, K. and Kanan, C.** (2018). "DVQA: Understanding Data Visualizations via Question Answering." CVPR 2018. *Fully synthetic dataset focused on chart-specific questions including counting.*

8. **Kahou, S.E., Michalski, V., Atkinson, A., Kadar, A., Trischler, A., and Bengio, Y.** (2018). "FigureQA: An Annotated Figure Dataset for Visual Reasoning." ICLR 2018 Workshop. *Synthetic figure QA dataset with binary yes/no questions about figure properties.*

9. **Xu, Z. et al.** (2023). "ChartBench: A Benchmark for Complex Visual Reasoning in Charts." arXiv:2312.15915, ICLR 2025. *42 categories, 66.6K charts, 600K QA pairs; introduces Acc+ metric for evaluation without costly manual assessment.*

10. **Wang, Z., Xia, R., et al.** (2024). "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs." NeurIPS 2024 Datasets and Benchmarks Track. arXiv:2406.18521. *2,323 charts from arXiv papers; descriptive questions include counting, enumeration, and pattern recognition. GPT-4o achieved 47.1%, humans 80.5%.*

11. **Xia, R., Zhang, L., et al.** (2024). "ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning." arXiv:2402.12185. *48,000 multi-modal chart samples across 18 chart types and 7 tasks.*

12. **Shen, L., Qigqi, Ding, K., Meng, G., and Xiang, S.** (2024). "Rethinking Comprehensive Benchmark for Chart Understanding: A Perspective from Scientific Literature." arXiv:2412.12150. *Introduces SCI-CQA from 15 top-tier CS conferences; models score 41/100 vs. human 90/100, with consistent undercounting in flowchart layer enumeration.*

### Chart-Specific Models and Methods

13. **Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Choi, Y., Cho, K., and Eisenschlos, J.** (2023). "MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering." ACL 2023. *Chart de-rendering pre-training for improved numerical reasoning.*

14. **Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Choi, Y., Cho, K., and Eisenschlos, J.** (2023). "DePlot: One-shot Visual Language Reasoning by Plot-to-Table Translation." Findings of ACL 2023. *Converts chart images to tables for downstream LLM reasoning.*

15. **Masry, A., Kavehzadeh, P., Do, X.L., Hoque, E., and Joty, S.** (2023). "UniChart: A Universal Vision-language Pretrained Model for Chart Comprehension and Reasoning." EMNLP 2023. *Achieves 88.56 RA on ChartQA, surpassing MatCha (81.6) and VL-T5 (30.5).*

### VLM Robustness and Hallucination

16. **Anonymous authors.** (2025). "Losing the Plot: How VLM Responses Degrade on Imperfect Charts." arXiv:2509.18425. *Tests Gemini 2.5 Pro (88% baseline), Claude Sonnet 4 (76%), ChatGPT-4o (70%) under 10 corruption types; identifies five hallucination categories including value fabrication and entity confusion.*

17. **Huang, Y. et al.** (2024). "A Survey on Hallucination in Large Vision-Language Models." arXiv:2402.00253. *Comprehensive survey of VLM hallucination types and mitigation strategies.*

### Spatial Reasoning and Visual Grounding

18. **Chen, B., Xu, Z., Koltun, V., Kolve, E., Ehsani, K., and Gordon, D.** (2024). "SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities." CVPR 2024. arXiv:2401.12168. *Creates internet-scale 3D spatial reasoning dataset; shows VLMs trained on image-caption pairs lack spatial/quantitative reasoning.*

19. **VLMs Are Biased (2024-2025).** Web resource at vlmsarebiased.github.io. *Documents 100% accuracy on standard images vs. 17% on counterfactual images, demonstrating confirmation bias in counting.*

### Prompting and Evaluation Strategies

20. **Do, X.L., Masry, A., Hoque, E., and Joty, S.** (2023). "Do LLMs Work on Charts? Designing Few-Shot Prompts for Chart Question Answering and Summarization." arXiv:2312.10610. *PromptChart framework; few-shot CoT prompting achieves up to 78.2% accuracy on chart QA.*

21. **Anonymous authors.** (2025). "Evaluating Prompting Strategies for Chart Reasoning with Large Language Models." arXiv:2603.22288. *Chain of Chart Reasoning (CCR) prompt strategy with task-specific subcategorization for chart QA.*

22. **Zheng, Y. et al.** (2025). "Advancing Chart Question Answering with Robust Chart Component Recognition." WACV 2025. *Improves chart QA through better component recognition including element counting.*

23. **mChartQA (2024).** "mChartQA: A Universal Benchmark for Multimodal Chart Question Answer based on Vision-Language Alignment and Reasoning." arXiv:2404.01548. *Extends chart QA evaluation across multiple modalities and chart types.*

---

## 6. Recommended Question Templates

### Level 1: Easy -- Direct Structural Counting

**Template 1: Total Bar Count**
> "How many bars are shown in this bar chart?"
> Expected answer type: Exact integer (e.g., 6)
> Difficulty: Easy

**Template 2: Pie Slice Count**
> "How many slices are present in this pie chart?"
> Expected answer type: Exact integer (e.g., 5)
> Difficulty: Easy

**Template 3: Line Count**
> "How many distinct lines are plotted in this line chart?"
> Expected answer type: Exact integer (e.g., 3)
> Difficulty: Easy

**Template 4: Legend Entry Count**
> "How many entries are listed in the legend of this chart?"
> Expected answer type: Exact integer (e.g., 4)
> Difficulty: Easy

### Level 2: Medium -- Conditional Counting

**Template 5: Threshold-Based Bar Count**
> "How many bars in this chart have a value greater than [X]?"
> Expected answer type: Exact integer
> Difficulty: Medium
> Note: Choose X so that the answer is neither 0 nor all bars; include at least one bar near the threshold.

**Template 6: Category-Specific Count**
> "How many data points belong to the [color/category] series in this chart?"
> Expected answer type: Exact integer
> Difficulty: Medium

**Template 7: Axis Tick Count**
> "How many tick marks are labeled on the x-axis of this chart?"
> Expected answer type: Exact integer
> Difficulty: Medium

**Template 8: Color-Based Element Count**
> "How many [blue/red/green] bars appear in this grouped bar chart?"
> Expected answer type: Exact integer
> Difficulty: Medium

### Level 3: Hard -- Cross-Panel and Compositional

**Template 9: Cross-Panel Total Count**
> "Across all subplots in this figure, how many total bars are displayed?"
> Expected answer type: Exact integer
> Difficulty: Hard

**Template 10: Multi-Condition Count**
> "How many bars in this chart are both above [X] in value and belong to the [category] group?"
> Expected answer type: Exact integer
> Difficulty: Hard

**Template 11: Panel Comparison Count**
> "In how many of the subplots does the [blue] line exceed the [red] line at any point?"
> Expected answer type: Exact integer
> Difficulty: Hard

**Template 12: Intersection Count**
> "How many times do the two plotted lines intersect in this chart?"
> Expected answer type: Exact integer
> Difficulty: Hard

### Level 4: Expert -- Edge Cases and Zero Counts

**Template 13: Zero-Count Probe**
> "How many bars in this chart have a value of exactly zero?"
> Expected answer type: Exact integer (may be 0)
> Difficulty: Expert
> Note: Tests whether the model can correctly report 0 and distinguish zero-height bars from absent bars.

**Template 14: Dense Element Count**
> "How many individual data points are plotted in this scatter plot?"
> Expected answer type: Exact integer (typically 15-50)
> Difficulty: Expert
> Note: Tests counting under visual density; expect significant VLM degradation above ~15 elements.

**Template 15: Stacked Bar Segment Count**
> "How many individual colored segments are shown across all bars in this stacked bar chart?"
> Expected answer type: Exact integer
> Difficulty: Expert

**Template 16: Negative Value Count**
> "How many bars extend below the zero line (have negative values) in this chart?"
> Expected answer type: Exact integer
> Difficulty: Expert

**Template 17: Grouped Distinction Count**
> "This grouped bar chart shows [N] groups. How many individual bars are there in total across all groups?"
> Expected answer type: Exact integer
> Difficulty: Expert
> Note: Tests whether model distinguishes groups from individual bars.

### Bonus: Robustness Probes

**Template 18: Consistency Check (Rephrased)**
> Version A: "Count the number of bars in this chart."
> Version B: "What is the total number of bars displayed?"
> Version C: "How many rectangular bars can you see in this bar chart?"
> Purpose: Same question, three phrasings. Consistent answers indicate robust counting.

**Template 19: Negation Probe**
> "How many bars in this chart do NOT exceed a value of [X]?"
> Expected answer type: Exact integer
> Difficulty: Hard
> Note: Tests logical negation combined with counting; models frequently fail on negated conditions.

**Template 20: Exhaustive Enumeration Request**
> "List each bar in this chart by its category label and height. Then state the total count."
> Expected answer type: Enumeration + integer
> Difficulty: Expert
> Note: Forces element-by-element processing rather than gestalt estimation; useful for diagnostic analysis.
