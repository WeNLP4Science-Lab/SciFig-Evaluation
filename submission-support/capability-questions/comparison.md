# Comparison Tasks in Scientific Figure Understanding: A Research Survey

## 1. What Are Comparison Tests in Scientific Figures?

### Definition

Comparison in chart understanding refers to determining **relative relationships** between visual elements: which value is larger or smaller, which comes first or last, how elements rank against each other, and identifying maxima and minima. Unlike value extraction (reading a single number) or trend detection (identifying a direction), comparison requires the model to hold multiple values in working memory and perform relational reasoning across them.

### Types of Comparison

1. **Pairwise comparison**: Determining whether element A is greater than, less than, or equal to element B. The simplest form---a binary judgment between two specific data points ("Is the bar for Category X taller than for Category Y?").

2. **Ordering / Ranking**: Sorting three or more elements by their values. Requires iterative pairwise comparisons and consistent transitivity ("Rank these five countries by GDP from highest to lowest").

3. **Extremum identification**: Finding the maximum or minimum element from a set. A special case of ranking where only the top/bottom element matters ("Which month had the highest sales?").

4. **Equality detection**: Determining whether two or more values are approximately equal, which is particularly hard when values are close but not identical ("Do Groups A and B have the same mean score?").

5. **Cross-category comparison**: Comparing the same measure across different groupings, often requiring integration of legends, colours, and spatial position ("Is the accuracy of Model X on Dataset A higher than Model Y on Dataset B?").

6. **Temporal comparison**: Comparing rates of change or relative magnitudes across time ("Did revenue grow faster in Q1 than in Q3?").

7. **Cross-subplot comparison**: Comparing values depicted in different panels of a multi-panel figure, requiring the model to reconcile potentially different axis scales.

### Why Comparison Is the Hardest Capability for VLMs

Multiple benchmarks consistently report comparison as the **lowest-accuracy task category** for vision-language models:

- **CharXiv** (Wang et al., NeurIPS 2024): The strongest proprietary model GPT-4o achieved only 47.1% on reasoning questions (many of which are comparative), versus human performance of 80.5%. Open-source models reached only 29.2%.

- **ChartMuseum** (Tang et al., NeurIPS 2025): Questions requiring complex visual reasoning---including comparisons---showed accuracy 35--55% lower than questions requiring only textual reasoning. The best model Gemini-2.5-Pro reached 63.0% overall vs. 93.0% human accuracy.

- **Visualization Literacy Tests** (Pandey et al., EuroVis 2025): On standardized VLAT and CALVI tests, "Make Comparisons" tasks were among the weakest categories, with VLMs showing consistent difficulties in comparing data-dense visualizations (bubble charts: 18.6--61.4% accuracy).

- **VLMs have Tunnel Vision** (Berman & Deng, NeurIPS 2025 Spotlight): Flagship models (GPT-5, Gemini 2.5 Pro, Claude Sonnet 4) barely exceeded random accuracy on comparative perception tasks requiring holding two images in working memory and comparing them.

The fundamental reason comparison is hardest is that it requires **multi-step visual reasoning**: (1) locate element A, (2) read its value, (3) locate element B, (4) read its value, (5) perform the relational judgment. Errors compound at each step, and the relational step introduces additional failure modes (proximity bias, scale confusion) not present in simple extraction.

---

## 2. Known Failure Modes of Best VLMs

### 2.1 Reading Values Correctly but Failing Relative Judgments

VLMs can often extract individual data points accurately but fail when asked to compare them. Huang & Qin (ACL Findings 2025) demonstrated in "Why Vision Language Models Struggle with Visual Arithmetic?" that even top-performing VLMs like GPT-4o and InternVL2.5-78B struggle with seemingly simple visual arithmetic tasks (object counting, length comparison), achieving less than 75% on challenging probing tasks. The root cause: while pre-trained vision encoders capture sufficient information, the **text decoder fails to decode it correctly** for arithmetic/relational reasoning.

### 2.2 Proximity Bias (Tunnel Vision)

Berman & Deng (NeurIPS 2025) formally established that VLMs suffer from **tunnel vision**: they process local regions well but fail at **nonlocal visual reasoning**---comparing elements that are spatially distant in the image. Their benchmark isolated three forms of nonlocal vision:
- **Comparative perception**: holding two spatially separated visual elements in working memory and comparing them
- **Saccadic search**: making evidence-driven jumps to locate successive targets
- **Smooth visual search**: following a continuous contour across the image

Flagship models failed all three, suggesting a fundamental architectural limitation in integrating information across distant image regions---exactly what chart comparison requires.

### 2.3 Scale Confusion

When charts use different y-axis ranges, logarithmic scales, or dual axes, VLMs frequently misinterpret relative magnitudes. CharXiv (Wang et al., 2024) showed that charts with compositional complexity---multiple subplots with different scales---caused performance drops of up to 34.5% even on models that performed well on simpler charts. Cross-subplot comparisons are particularly vulnerable because the model must understand that the same visual height can represent different numerical values in different panels.

### 2.4 Visual Illusions and Near-Equal Values

Bar heights that appear similar but differ by 5--10% are a consistent failure case. The "Benchmarking Visual Language Models on Standardized Visualization Literacy Tests" study (Pandey et al., 2025) found that all four tested VLMs (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.2-Vision) struggled with anomaly detection (25--30% accuracy) and tasks requiring fine-grained visual discrimination. When values are close, models default to reporting equality or guess randomly.

### 2.5 Stacked and Grouped Bar Comparison Failures

Stacked bars require the model to visually decompose segments and compare individual segment heights rather than total bar heights. Grouped bars require matching colours/patterns to legends and comparing across non-adjacent elements. ChartX (Xia et al., 2024) showed markedly inferior performance on less common chart types including 3D-bar, multi-axes, and area charts, all of which compound comparison difficulty.

### 2.6 Confirmation Bias and Hallucination

Research on VLM bias (VLMs Are Biased, 2024) demonstrated that models suffer from **severe confirmation bias**: when they see familiar objects or chart patterns, they default to memorized knowledge instead of performing actual visual analysis. In chart comparison, this manifests as:
- Fabricating values that "make sense" rather than reading actual data
- Asserting trends consistent with domain expectations regardless of visual evidence
- Generating plausible but unsupported explanations for comparisons

### 2.7 Overconfidence Under Degradation

"Losing the Plot" (2025) evaluated ChatGPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro on charts with corruptions and occlusions. Models showed sharp performance drops but remained **overconfident**, exhibiting:
- **Value fabrication**: inventing specific numbers for occluded bars
- **Trend misinterpretation**: claiming upward trends in declining data
- **Entity confusion**: misattributing values to wrong categories
- **Prompt reverse inconsistency**: contradicting themselves when asked to confirm vs. deny the same comparison statement

### 2.8 Model-Specific Weaknesses

| Model | Key Weakness on Comparison | Source |
|-------|---------------------------|--------|
| GPT-4o/4V | Over-reliance on textual reasoning; fabricates values under occlusion; requires multi-step manual guidance for ChartBench | ChartBench (2024), Losing the Plot (2025) |
| Gemini | Heightened caution leading to 22.5% question omission; struggles with bubble charts and multi-encoding visualizations | Pandey et al. (2025) |
| Claude | Slightly less numerically precise on scaling calculations; 67.9% VLAT accuracy (best among tested but still far from human) | Pandey et al. (2025) |
| Open-source (LLaVA, Qwen-VL) | Chart recognition relies on OCR rather than visual logical reasoning; performance drops up to 34.5% on stress tests | CharXiv (2024), ChartBench (2024) |
| Specialized (MatCha, UniChart) | High accuracy (87--91%) on simple questions but degrade sharply on complex/augmented comparison tasks | Masry et al. (2024) |

---

## 3. Best Question Design Strategies

### 3.1 Binary Comparison (Is A > B?)

The simplest and most unambiguous comparison question format. FigureQA (Kahou et al., 2018) pioneered this approach with 15 question templates, all requiring yes/no answers.

**Strengths**: Clear ground truth, easy to evaluate, isolates comparison from other skills.
**Weaknesses**: 50% random baseline for yes/no; can be answered by guessing.
**Mitigation**: Use balanced datasets with equal yes/no distribution; pair with confidence scoring.

### 3.2 Ranking Questions (Order From Highest to Lowest)

Require the model to produce a full ordering of N elements. PlotQA (Methani et al., WACV 2020) includes ordering tasks over real-world data.

**Strengths**: Rich signal (many possible wrong orderings); tests transitivity.
**Weaknesses**: Partial errors hard to score; sensitive to ties.
**Best practice**: Limit to 3--7 elements; use rank correlation metrics for evaluation.

### 3.3 Superlative Questions (Which Has the Highest/Lowest?)

Extremum identification is the most common comparison question in existing benchmarks (ChartQA, PlotQA, DVQA).

**Strengths**: Single correct answer; natural question format.
**Weaknesses**: Can sometimes be answered from text alone (e.g., if labels contain numerical hints); doesn't test fine-grained discrimination.
**Best practice**: Ensure the answer requires visual inspection, not just legend/label reading.

### 3.4 Cross-Category Comparison

Comparing the same metric across different categorical groupings (e.g., "Is Model A's accuracy on Task 1 higher than Model B's accuracy on Task 2?").

**Strengths**: Tests integration of multiple visual channels (colour, position, legend).
**Weaknesses**: Requires unambiguous categorical encoding in the chart.

### 3.5 Cross-Subplot Comparison

Comparing values across different panels in a multi-panel figure. CharXiv (2024) found this to be a major failure mode.

**Strengths**: Tests scale awareness and spatial reasoning across discontinuous regions.
**Weaknesses**: Requires careful ground-truth annotation accounting for different scales.
**Best practice**: Include questions where subplots share the same scale AND where they differ.

### 3.6 Near-Miss Comparisons

Values that are very close together (within 5--10%), testing precision of visual reading. CogAlign (Huang & Qin, 2025) specifically designed probing tasks for this.

**Strengths**: Highest discriminative power---separates genuine understanding from approximate guessing.
**Weaknesses**: Sensitive to image resolution and rendering artifacts.
**Best practice**: Specify tolerance thresholds; include both "very close but A > B" and "approximately equal" cases.

### 3.7 Temporal Comparisons

Comparing rates of change, growth, or trends over time periods ("Did metric X increase more than metric Y between 2020 and 2023?").

**Strengths**: Tests integration of trend detection with comparison.
**Weaknesses**: Requires clear temporal axis; ambiguous for non-monotonic trends.

### 3.8 Negation and Reversal Questions

Testing consistency by asking the same comparison in positive and negative forms. "Losing the Plot" (2025) introduced **prompt reverse inconsistency** as a diagnostic.

**Strengths**: Detects models that guess or rely on surface patterns.
**Best practice**: Include matched pairs: "Is A > B?" and "Is B > A?" for the same data.

### 3.9 Graduated Difficulty Design

Following the cognitive development framework from CogAlign (Huang & Qin, 2025), design comparison questions at increasing difficulty levels:
1. **Level 1**: Compare two clearly different values (>20% difference)
2. **Level 2**: Compare two moderately different values (5--20% difference)
3. **Level 3**: Compare two very close values (<5% difference)
4. **Level 4**: Rank 3--5 elements with clear separation
5. **Level 5**: Rank 3--5 elements with some close values
6. **Level 6**: Cross-subplot or cross-scale comparison
7. **Level 7**: Compound comparison with temporal/categorical integration

---

## 4. Evaluation Strategies

### 4.1 Binary Accuracy for Yes/No Comparisons

Standard accuracy metric for pairwise comparison questions. Report alongside:
- **Balanced accuracy**: average of true-positive and true-negative rates, to account for class imbalance
- **Acc+** (ChartBench metric): accuracy corrected for random guessing bias in binary QA

### 4.2 Rank Correlation Metrics for Ordering Tasks

- **Kendall's Tau (tau-b)**: Measures the ordinal association between two rankings based on concordant and discordant pairs. Ranges from -1 (perfect disagreement) to +1 (perfect agreement). Preferred when there are ties. Directly interpretable as the difference between the probability that two observations are in the same order versus different order.

- **Spearman's Rho**: Measures the strength of monotonic relationships between rankings. Generally yields larger absolute values than Kendall's tau. More sensitive to large rank displacements.

**Recommendation**: Report both Kendall's tau-b (for robustness to ties) and Spearman's rho (for comparability with prior work). Use Kendall's tau as the primary metric for ranking questions.

### 4.3 Partial Credit for Nearly-Correct Orderings

- **Normalized Kendall Tau Distance**: Number of pairwise disagreements normalized by total pairs. A ranking that swaps only adjacent elements scores high.
- **Rank-Biased Overlap (RBO)**: Weights top-ranked elements more heavily than lower-ranked ones, appropriate when the top of the ranking matters more.
- **Mean Average Precision (MAP)**: If treating ordering as a retrieval problem.
- **Edit Distance on Rankings**: Minimum number of adjacent transpositions to convert predicted ranking to ground truth.

### 4.4 Handling Ties and Near-Equal Values

When ground-truth values are within a tolerance threshold (e.g., <2% relative difference):
1. **Accept either ordering** for tied elements
2. **Define explicit tolerance bands**: values within epsilon of each other are treated as ties
3. **Use soft accuracy**: give full credit for correct ordering, partial credit when swapped elements are within tolerance
4. **Report separate accuracy** for "clear comparison" (>10% difference) vs. "near-miss comparison" (<10% difference)

### 4.5 Multi-Dimensional Evaluation Framework

Following the structure of CharXiv and ChartMuseum, evaluate comparison along:
- **Chart complexity**: simple (single series) vs. complex (multi-series, multi-panel)
- **Question complexity**: binary vs. ranking vs. compound
- **Visual difficulty**: clear separation vs. near-miss vs. cross-scale
- **Reasoning type**: purely visual vs. requiring textual context (legends, labels)

### 4.6 Consistency Metrics

From "Do VLMs Really Understand Charts?" (Masry et al., EMNLP Findings 2024):
- **Augmentation robustness**: Does the model give the same comparison answer when the chart is slightly perturbed (colour change, font change, axis format change)?
- **Bidirectional consistency**: If model says A > B, does it also say B < A?
- **Transitivity consistency**: If model says A > B and B > C, does it say A > C?

---

## 5. References

### Core Chart QA Benchmarks

1. **Kahou, S.E., Michalski, V., Atkinson, A., et al.** (2018). "FigureQA: An Annotated Figure Dataset for Visual Reasoning." *ICLR 2018 Workshop*. Over 1 million yes/no question-answer pairs on 100K+ synthetic figures; 15 comparison-focused question templates.

2. **Kafle, K., Price, B., Cohen, S., & Kanan, C.** (2018). "DVQA: Understanding Data Visualizations via Question Answering." *CVPR 2018*. Synthetic bar chart QA with fixed vocabulary answers; introduced structure, data, and reasoning question types.

3. **Methani, N., Ganguly, P., Khapra, M.M., & Kumar, P.** (2020). "PlotQA: Reasoning over Scientific Plots." *WACV 2020*. 28.9M question-answer pairs over 224K plots from real-world data; open-vocabulary with complex reasoning including comparison and ordering.

4. **Masry, A., Long, D., Tan, J.Q., Joty, S., & Hoque, E.** (2022). "ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning." *ACL Findings 2022*. Human-written and machine-generated questions on real charts; distinguishes visual vs. logical reasoning.

5. **Xu, Z., et al.** (2024). "ChartBench: A Benchmark for Complex Visual Reasoning in Charts." *arXiv:2312.15915*. 42 categories, 66.6K charts, 600K QA pairs; introduced Acc+ metric to correct binary QA bias; showed most models rely on OCR rather than visual reasoning.

6. **Xia, R., Zhang, B., et al.** (2024). "ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning." *arXiv:2402.12185*. 48K charts, 22 topics, 18 chart types, 7 tasks; introduced SCRM metric for structural evaluation; showed inferior performance on rose, area, 3D-bar, bubble, multi-axes, and radar charts.

7. **Wang, Z., Xia, M., et al.** (2024). "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs." *NeurIPS 2024 Datasets & Benchmarks*. 2,323 real scientific charts; descriptive and reasoning questions; GPT-4o achieved only 47.1% vs. 80.5% human; stress tests showed up to 34.5% performance degradation.

8. **Tang, L., et al.** (2025). "ChartMuseum: Testing Visual Reasoning Capabilities of Large Vision-Language Models." *NeurIPS 2025*. 1,162 expert-annotated questions from 184 real-world sources; showed visual reasoning 35--55% worse than textual reasoning; best model 63.0% vs. 93.0% human.

9. **Zhou, Y., et al.** (2024). "Rethinking Comprehensive Benchmark for Chart Understanding: A Perspective from Scientific Literature (SCI-CQA)." *arXiv:2412.12150*. 37,607 charts from top CS conferences; 5,629 questions including scientific reasoning type; exposed inflated scores from template-based questions.

10. **Li, K., et al.** (2025). "ChartQAPro: A More Diverse and Challenging Benchmark for Chart Question Answering." *arXiv:2504.05506*. Extended benchmark addressing limitations of prior ChartQA datasets.

### VLM Failure Analysis and Visual Reasoning

11. **Masry, A., Gupta, R., et al.** (2024). "Unraveling the Truth: Do VLMs Really Understand Charts? A Deep Dive into Consistency and Robustness." *EMNLP Findings 2024*. Showed VLMs achieve as low as 25% accuracy on complex chart + complex question pairs; demonstrated robustness failures under perturbation.

12. **Huang, L. & Qin, Z.** (2025). "Why Vision Language Models Struggle with Visual Arithmetic? Towards Enhanced Chart and Geometry Understanding." *ACL Findings 2025*. Identified that text decoders fail to decode visual arithmetic correctly; proposed CogAlign post-training strategy based on Piaget's cognitive development theory; improved chart understanding by 4.6%.

13. **Berman, S. & Deng, J.** (2025). "VLMs Have Tunnel Vision: Evaluating Nonlocal Visual Reasoning in Leading VLMs." *NeurIPS 2025 Spotlight*. Demonstrated flagship models (GPT-5, Gemini 2.5 Pro, Claude Sonnet 4) barely exceed random accuracy on comparative perception tasks requiring nonlocal reasoning.

14. **Kim, J., et al.** (2025). "Losing the Plot: How VLM Responses Degrade on Imperfect Charts." *arXiv:2509.18425*. Introduced CHART NOISe dataset; showed value fabrication, trend misinterpretation, entity confusion, and prompt reverse inconsistency in GPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro.

15. **VLMs Are Biased** (2024). Demonstrated confirmation bias in VLMs: models default to memorized knowledge rather than performing actual visual analysis, failing to detect subtle changes in counterfactual visual inputs.

### Visualization Literacy and Standardized Tests

16. **Pandey, A., et al.** (2025). "Benchmarking Visual Language Models on Standardized Visualization Literacy Tests." *Computer Graphics Forum / EuroVis 2025*. Tested GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.2-Vision on VLAT and CALVI; Claude achieved 67.9% on VLAT; all models showed 25--30% accuracy on anomaly/misleading visualization detection.

17. **Lee, S., Kim, S.H., & Kwon, B.C.** (2017). "VLAT: Development of a Visualization Literacy Assessment Test." *IEEE VIS 2017*. Foundational standardized test measuring human visualization literacy across task types including "Retrieve Value," "Find Extremum," "Make Comparisons," and others.

### Multi-Modal Evaluation and General Benchmarks

18. **Chen, L., et al.** (2024). "Are We on the Right Way for Evaluating Large Vision-Language Models? (MMStar)." *NeurIPS 2024*. 1,500 vision-indispensable samples evaluating 6 core capabilities and 18 axes; introduced Multi-modal Gain (MG) and Multi-modal Leakage (ML) metrics.

19. **Masry, A., et al.** (2024). "SciFIBench: Benchmarking Large Multimodal Models for Scientific Figure Interpretation." *arXiv:2405.08807*. 2,000 questions across 8 categories on arXiv paper figures; adversarial filtering for hard negatives.

20. **Xu, G., et al.** (2025). "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step." *ICCV 2025*. Chain-of-thought reasoning for visual tasks; showed step-by-step reasoning can improve comparison accuracy.

---

## 6. Recommended Question Templates

### Simple Binary Comparison (Level 1--2)

**T1. Direct Pairwise Comparison**
> "Is the value for {Category A} greater than the value for {Category B}?"
> Expected answer: Yes / No

**T2. Pairwise with Specificity**
> "In {year/group}, does {Series A} have a higher value than {Series B}?"
> Expected answer: Yes / No

**T3. Approximate Equality Detection**
> "Are the values for {Category A} and {Category B} approximately equal (within 5%)?"
> Expected answer: Yes / No

### Superlative / Extremum (Level 2--3)

**T4. Maximum Identification**
> "Which {category/group/year} has the highest value of {metric}?"
> Expected answer: Category name (string)

**T5. Minimum Identification**
> "Which {series/line/bar} shows the lowest value at {time point / x-value}?"
> Expected answer: Series name (string)

**T6. Conditional Extremum**
> "Among {subset of categories}, which one has the highest {metric}?"
> Expected answer: Category name (string)

### Ranking / Ordering (Level 4--5)

**T7. Full Ranking**
> "Rank the following categories from highest to lowest based on their {metric} values: {A, B, C, D, E}."
> Expected answer: Ordered list (e.g., "C, A, E, B, D")

**T8. Partial Ranking (Top-K)**
> "What are the top 3 {categories/models/countries} by {metric}?"
> Expected answer: Ordered list of 3 items

**T9. Ranking with Ties**
> "Rank these items by {metric}. If any two values appear approximately equal, indicate a tie."
> Expected answer: Ordered list with tie notation (e.g., "A, B=C, D")

### Cross-Category and Cross-Subplot (Level 5--6)

**T10. Cross-Group Comparison**
> "Is {metric} for {Category A} in {Group 1} higher than {metric} for {Category B} in {Group 2}?"
> Expected answer: Yes / No

**T11. Cross-Subplot Comparison**
> "Comparing the left and right panels, which panel shows a higher peak value for {series}?"
> Expected answer: Left / Right (or Panel A / Panel B)

**T12. Ratio Comparison**
> "Which category's value is closest to being twice the value of {reference category}?"
> Expected answer: Category name (string)

### Temporal and Trend Comparison (Level 6--7)

**T13. Growth Rate Comparison**
> "Between {year1} and {year2}, did {Series A} increase more than {Series B}?"
> Expected answer: Yes / No

**T14. Relative Change**
> "Which series showed the largest percentage increase from {start} to {end}?"
> Expected answer: Series name (string)

### Compound and Adversarial (Level 7)

**T15. Multi-Step Comparison**
> "What is the difference between the highest and lowest values across all categories shown in the chart? Is this difference greater than {threshold}?"
> Expected answer: Numerical value + Yes/No

**T16. Consistency Check (Negation)**
> "Is {Category A}'s value less than or equal to {Category B}'s value?"
> Expected answer: Yes / No (paired with T1 using the same data for consistency testing)

**T17. Near-Miss Discrimination**
> "The values for {Category A} and {Category B} appear similar. Which one is actually higher, and by approximately how much?"
> Expected answer: Category name + approximate difference

**T18. Stacked Bar Segment Comparison**
> "In the stacked bar chart, is the {colour/segment} portion of {Bar A} larger than the {colour/segment} portion of {Bar B}?"
> Expected answer: Yes / No

---

## Summary of Design Recommendations

1. **Balance binary questions** with equal yes/no ground truth to avoid random-baseline inflation.
2. **Include near-miss pairs** (values within 5--10%) to test genuine visual reading vs. guessing.
3. **Test cross-subplot comparison** explicitly, as this is a documented severe failure mode.
4. **Use consistency checks**: ask the same comparison in forward and reverse form.
5. **Grade difficulty** from simple binary to compound multi-element ranking.
6. **Report separate accuracy** for clear-separation vs. near-miss comparisons.
7. **Use Kendall's tau-b** as the primary metric for ranking questions; Spearman's rho as secondary.
8. **Include robustness tests**: same question on perturbed versions of the chart (colour change, font change).
9. **Avoid questions answerable from text alone**: ensure the comparison genuinely requires visual inspection.
10. **Document tolerance thresholds** for near-equal values in the evaluation protocol.
