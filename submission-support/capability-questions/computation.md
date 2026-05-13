# Computation in Scientific Figure Understanding: Research Review and Testing Strategies

## 1. What Computation Tests in Scientific Figures

### 1.1 Definition

Computation in chart understanding refers to the ability to perform **arithmetic operations on values that must first be visually extracted** from a scientific figure. This includes:

- **Differences**: "How much greater is the value of A than B?" (requires reading two values and subtracting)
- **Ratios**: "What is the ratio of X to Y?" (requires reading two values and dividing)
- **Sums and aggregations**: "What is the total across all categories?" (requires reading multiple values and summing)
- **Percentages**: "What percentage of the total does category X represent?" (requires reading one value and the total, then dividing and multiplying by 100)
- **Averages**: "What is the average value across the five years shown?" (requires reading all values and computing mean)
- **Rates of change**: "By what percentage did the value increase from 2018 to 2020?" (requires reading two values, computing difference, dividing by base, multiplying by 100)
- **Comparisons with derived quantities**: "Which category has the largest year-over-year growth?"

### 1.2 Why Computation Is a Compound Skill

Computation in chart understanding is fundamentally a **two-stage pipeline**:

1. **Stage 1 -- Visual Value Extraction**: The model must accurately read numerical values from the chart's visual encoding (bar heights, line positions, pie slice angles, scatter point coordinates). This requires interpreting axes, gridlines, scales, and visual marks.

2. **Stage 2 -- Arithmetic Reasoning**: Given the extracted values, the model must perform correct mathematical operations.

This compound nature means computation questions test both **perceptual fidelity** and **numerical reasoning** simultaneously, making them among the most demanding tasks in chart understanding benchmarks (Masry et al., 2022; Methani et al., 2020).

### 1.3 The Two-Stage Failure Mode

Errors in computation tasks arise from two distinct sources, and diagnosing which stage failed is critical for evaluation:

- **Failure Mode A -- Wrong Value Read, Wrong Computation**: The model misreads a value from the chart (e.g., reads "27" instead of "27.3") and then performs correct arithmetic on the wrong input. The final answer is wrong, but the arithmetic reasoning was sound.

- **Failure Mode B -- Correct Values, Wrong Arithmetic**: The model correctly extracts all values but makes a computational error (e.g., correctly reads 45 and 30 but reports their difference as 20 instead of 15). Research shows this is surprisingly common in LLMs, which generate answers via token prediction rather than formal computation (GitHub Next, 2023).

- **Failure Mode C -- Compound Errors**: Both value extraction and arithmetic fail, compounding the error magnitude.

Research by Huang et al. (2025) demonstrates that pre-trained vision encoders coupled with simple classifiers perform poorly on visual arithmetic, but fine-tuning the text decoder significantly improves performance, suggesting the bottleneck often lies in the decoder's processing capabilities rather than visual encoding alone. However, the FUGU study (2025) found through causal interventions and linear probes that the primary bottleneck lies in the **hand-off between vision and language components** -- the vision encoder successfully represents coordinates and spatial information, but the language model struggles to access and use this information effectively.

---

## 2. Known Failure Modes of Best VLMs

### 2.1 Systematic Arithmetic Errors in GPT-4V/4o

GPT-4V and GPT-4o demonstrate multiple categories of arithmetic failure on chart-extracted values:

- **Decimal and large-number errors**: Multi-step arithmetic leads to cumulative errors because intermediate values are not reliably tracked via token prediction (GitHub Next, 2023).
- **Basic comparison failures**: GPT-4 occasionally makes elementary comparison mistakes, such as judging $1,449.46 to be larger than $1,823.26 (OpenAI Community, 2024).
- **Prompting has limited effect**: Differences between prompting conditions (zero-shot, few-shot, chain-of-thought) were found to be "relatively small" compared to improvements from using a more capable model. GPT-5 outperforms GPT-4o by 20-40 percentage points on chart tasks, and this gap cannot be closed by prompt engineering alone (Shin et al., 2025).

### 2.2 Performance Across Leading VLMs

From the DynaMath benchmark (Zou et al., 2024) and CharXiv (NeurIPS 2024):

| Model | DynaMath Avg Accuracy | DynaMath Worst-Case | Notes |
|-------|----------------------|--------------------|----|
| Claude 3.5 Sonnet | 64.8% | Significantly lower | Highest zero-shot average |
| GPT-4o | ~62% | Significantly lower | Strong on arithmetic/algebra subtypes |
| Gemini 1.5 Pro | ~60% | Significantly lower | Lower robustness than GPT-4o |
| Qwen2-VL-72B | ~61% | -- | Particularly robust on arithmetic |
| InternVL2-76B | ~59% | -- | Outperformed Gemini on robustness |

Key finding: **Worst-case accuracy (all 10 variants correct) is dramatically lower than average-case accuracy** for all models, revealing that VLMs cannot reliably apply solution steps to minor problem variations -- unlike humans.

From ChartQAPro (Masry et al., 2025):
- Claude Sonnet 3.5 scores **90.5% on ChartQA** but only **55.81% on ChartQAPro**, a drop of nearly 35 points on more diverse, realistic charts.
- This demonstrates that high benchmark scores do not translate to robust real-world chart reasoning.

### 2.3 Precision Loss in Value Reading

VLMs routinely exhibit precision loss when extracting values from charts:

- **Rounding to nearest integer**: A value of 27.3 may be read as "27" or "~28"
- **Approximation bias**: Models tend to report round numbers, introducing systematic bias in subsequent computations
- **OCR fragility**: Text recognition accuracy degrades severely under common visual corruptions (blur, noise, compression), with models misreading axis labels and tick marks (Shin et al., 2025)

The ORCA benchmark (2025) evaluated state-of-the-art LLMs on real-world calculation tasks across 500 problems and found only **45-63% accuracy**, with errors attributable to:
- Rounding errors: **35%** of all errors
- Calculation mistakes: **33%** of all errors
- Wrong method/formula selection: **13.4%**
- Wrong assumptions: **11.8%**

### 2.4 Multi-Step Computation Breakdowns

Multi-step computation compounds errors at each stage:

- Each intermediate step introduces potential for both value-extraction error and arithmetic error
- Models lack reliable mechanisms for tracking intermediate results across reasoning steps
- Chain-of-thought prompting helps marginally but cannot overcome fundamental architectural limitations (Shin et al., 2025)

### 2.5 Unit Confusion and Scale Misinterpretation

- **Log vs. linear scale**: VLMs frequently fail to recognize logarithmic scales, reading values as if the axis were linear. This leads to order-of-magnitude errors in extracted values.
- **Axis manipulation sensitivity**: Research on misleading visualizations found that inverted axes affect all 10 tested models, followed by aspect ratio and truncated axis distortions.
- **Unit conversion**: When charts display values in thousands, millions, or with unit prefixes (k, M, B), models may fail to apply the correct multiplier.

### 2.6 Chart Corruption and Degradation

The CHART NOISe study (Shin et al., 2025) -- "Losing the Plot: How VLM responses degrade on imperfect charts" -- evaluated ChatGPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro and documented:

- **Value fabrication**: Models produce incorrect numerical values with high confidence
- **Trend misinterpretation**: Models misread upward/downward patterns
- **Entity confusion**: Models misidentify which data series a value belongs to
- **Overconfidence**: Models generate plausible but unsupported explanations even when chart quality is degraded
- **Table/translation drift**: Errors during implicit chart-to-table conversion

---

## 3. Best Question Design Strategies

### 3.1 Single-Step Computation Questions

These are the simplest computation tasks, requiring one arithmetic operation on two extracted values:

- **Difference**: "What is the difference in value between Category A and Category B?"
- **Ratio**: "What is the ratio of the 2020 value to the 2019 value?"
- **Simple percentage**: "What percentage of the total does the largest segment represent?"

Design principle: Use these as baseline probes. If a model fails single-step computation, multi-step questions are uninformative.

### 3.2 Multi-Step Computation Questions

These require chaining two or more operations:

- **Percentage change**: "By what percentage did revenue increase from 2018 to 2022?" (requires: read two values, subtract, divide by base, multiply by 100)
- **Weighted average**: "What is the average value across all five categories shown?"
- **Compound ratio**: "The ratio of A to B is X. The ratio of B to C is Y. What is the ratio of A to C?"

### 3.3 Ratio Questions

Ratios are particularly diagnostic because they require:
1. Accurate extraction of two values
2. Division (which amplifies small extraction errors)
3. Appropriate precision in the answer

Example: "What is the ratio of the highest bar to the lowest bar in the chart?" -- If the highest bar is 85 and the lowest is 17, the answer is 5.0. If the model reads 84 and 18, it gets 4.67 -- a 6.6% error from small misreads.

### 3.4 Difference Questions

- **Absolute difference**: "How much more is X than Y?"
- **Relative difference**: "By what factor does X exceed Y?"
- **Cross-category difference**: "What is the difference between the maximum and minimum values across all categories?"

### 3.5 Percentage Computation

- **Part-to-whole**: "What percentage of total sales does Region A represent?"
- **Percentage change**: "What is the percentage decrease from Q1 to Q4?"
- **Percentage point difference**: "How many percentage points higher is Method A's accuracy compared to Method B?"

### 3.6 Aggregate Computation

These are the most challenging because they require extracting many values:

- **Sum**: "What is the total value across all bars in the chart?"
- **Average**: "What is the mean value of the five data points shown?"
- **Range**: "What is the range (max minus min) of the dataset?"
- **Weighted aggregation**: "What is the weighted average, given the frequencies shown?"

### 3.7 Cross-Subplot Computation

For multi-panel figures, questions that require values from different subplots test both spatial reasoning and computation:

- "How much higher is the peak value in subplot (a) compared to subplot (b)?"
- "What is the ratio of the average values shown in the left panel vs. the right panel?"

### 3.8 Difficulty Calibration

Design questions along a difficulty gradient:

| Level | Description | Example | Operations |
|-------|------------|---------|-----------|
| L1 | Single value extraction + one operation | "What is the difference between bars A and B?" | 1 subtraction |
| L2 | Two extractions + one operation | "What is the ratio of the max to the min?" | 1 division, but requires identifying max/min |
| L3 | Multiple extractions + one operation | "What is the average of all five values?" | 5 extractions + 1 mean |
| L4 | Multiple extractions + chained operations | "What is the percentage change from the minimum to the maximum?" | Identify min/max + subtract + divide + multiply |
| L5 | Cross-subplot + multiple operations | "Compare the average growth rate between panel A and panel B" | Multiple extractions across panels + multiple operations |

---

## 4. Evaluation Strategies

### 4.1 Exact Match vs. Acceptable Range

For computed numerical answers, **exact match is almost always too strict** because:

- Chart values are inherently approximate (determined by visual resolution, not exact data)
- Human performance itself has inherent imprecision when reading charts
- Minor rounding differences should not penalize correct reasoning

### 4.2 Relaxed Accuracy (ChartQA Standard)

The ChartQA benchmark established the standard **relaxed accuracy** metric:

- For numerical answers: a tolerance of up to **5% relative error** is allowed
- For textual answers: exact matching after normalization (lowercase, remove punctuation, standardize number formats like "5 thousand" to "5000")
- This 5% tolerance has become the de facto standard in chart QA evaluation

Formula: A numerical answer `pred` is correct if `|pred - gold| / |gold| <= 0.05`

### 4.3 Handling Floating-Point Precision

Strategies for evaluating floating-point computed answers:

1. **Relative tolerance**: Accept answers within X% of ground truth (standard: 5%)
2. **Absolute tolerance**: For values near zero, use absolute tolerance (e.g., +/- 0.5)
3. **Significant figures**: Compare to N significant figures (typically 2-3 for chart-derived values)
4. **Format normalization**: Accept "25%", "0.25", "25 percent", "one quarter" as equivalent

### 4.4 Partial Credit for Correct Method

A more nuanced evaluation scheme awards partial credit:

- **Full credit**: Correct final answer within tolerance
- **Partial credit (method correct, values wrong)**: Model describes the correct computational approach but extracts wrong values. This can be assessed via chain-of-thought analysis.
- **Partial credit (values correct, arithmetic wrong)**: Model extracts correct values but makes a computational error. Diagnosable when the model shows its work.
- **No credit**: Wrong approach and wrong answer

This requires structured output (e.g., "I read value A = X and value B = Y, so the difference is Z") to enable diagnosis.

### 4.5 Setting Acceptable Ranges Based on Visual Precision

The acceptable error range should be calibrated to the **visual precision** of the chart:

- **Charts with gridlines and labeled ticks**: Tighter tolerance (2-5%), as values can be read more precisely
- **Charts without gridlines**: Wider tolerance (5-10%), as interpolation between tick marks introduces error
- **Small charts or low resolution**: Even wider tolerance (10-15%)
- **Pie charts**: Wider tolerance for angular estimation (5-10% for segments, higher for small slices)
- **Log-scale charts**: Tolerance should be in log-space, not linear

Rule of thumb: If a human panel cannot agree on a value within X%, the tolerance should be at least X%.

### 4.6 Evaluation Protocol Recommendations

1. **Always report both strict and relaxed accuracy** to allow comparison across studies
2. **Separate value-extraction accuracy from computation accuracy** where possible (by providing ground-truth values in a control condition)
3. **Report per-operation-type accuracy** (addition, subtraction, division, etc.) to identify systematic weaknesses
4. **Use multiple paraphrases** of the same question to test robustness (as shown by DynaMath's variant-based evaluation)

---

## 5. References

### 5.1 Core Chart QA Benchmarks

1. **Masry, A., Do, X.L., Tan, J.Q., Joty, S., & Hoque, E.** (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. *Findings of ACL 2022*, pp. 2263-2279. -- Introduced 9.6K human-written + 23.1K generated questions over 18,317 chart images. Established relaxed accuracy with 5% tolerance for numerical answers. Key benchmark for chart computation evaluation.

2. **Masry, A. et al.** (2025). ChartQAPro: A More Diverse and Challenging Benchmark for Chart Question Answering. *Findings of ACL 2025*, pp. 19123-19151, Vienna, Austria. -- 1,341 charts from 99 sources, 1,948 questions including multiple-choice, conversational, hypothetical, and unanswerable. Claude Sonnet 3.5 drops from 90.5% (ChartQA) to 55.81% (ChartQAPro).

3. **Methani, N., Ganguly, P., Khapra, M.M., & Kumar, P.** (2020). PlotQA: Reasoning over Scientific Plots. *WACV 2020*. -- 28.9 million QA pairs over 224,377 plots from real-world data sources. 74 question templates from crowd-sourced questions. 80.76% of questions have out-of-vocabulary answers requiring computation.

4. **Kafle, K., Cohen, S., Price, B., & Kanan, C.** (2018). DVQA: Understanding Data Visualizations via Question Answering. *CVPR 2018*. -- Fully synthetic bar chart dataset with structure, data, and reasoning question types. Integer-only answers.

5. **Kahou, S.E., Atkinson, A., Michalski, V., Kadar, A., Trischler, A., & Bengio, Y.** (2018). FigureQA: An Annotated Figure Dataset for Visual Reasoning. *ICLR 2018 Workshop*. -- Over 1M QA pairs on 100K+ synthetic figures (line plots, bar graphs, pie charts). Binary yes/no questions from 15 templates.

### 5.2 Mathematical and Numerical Reasoning Benchmarks

6. **Lu, P., Bansal, H., Xia, T., Liu, J., Li, C., Hajishirzi, H., Cheng, H., Chang, K.-W., Galley, M., & Gao, J.** (2024). MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts. *ICLR 2024 (Oral)*. -- 6,141 examples from 31 datasets. GPT-4V achieves 49.9%, still 10.4% below human performance. Includes FunctionQA and PaperQA subsets relevant to scientific figure computation.

7. **Zou, G., Guo, Z., et al.** (2024). DynaMath: A Dynamic Visual Benchmark for Evaluating Mathematical Reasoning Robustness of Vision Language Models. *arXiv:2411.00836*. -- 501 seed questions with 10 variants each (5,010 total). Worst-case accuracy dramatically lower than average-case for all VLMs. GPT-4o and Claude-3.5 lead at ~62-65% average accuracy.

8. **Wang, K. et al.** (2024). Measuring Multimodal Mathematical Reasoning with the MATH-Vision Dataset. *NeurIPS 2024 Datasets and Benchmarks Track*. -- Focused on mathematical reasoning from visual inputs.

9. **ORCA Benchmark** (2025). The ORCA Benchmark: Evaluating Real-World Calculation Accuracy in Large Language Models. *arXiv:2511.02589*. -- 500 real-world calculation tasks across finance, physics, health, statistics. State-of-the-art LLMs achieve only 45-63% accuracy. Rounding errors (35%) and calculation mistakes (33%) dominate.

### 5.3 Chart-Specialized Models

10. **Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Choi, Y., Eisenschlos, J., & Altun, Y.** (2023). MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering. *ACL 2023*. -- Pre-training with chart derendering + math reasoning from MATH and DROP datasets. Outperforms prior SOTA by ~20% on PlotQA and ChartQA.

11. **Masry, A., Kavehzadeh, P., Do, X.L., Hoque, E., & Joty, S.** (2023). UniChart: A Universal Vision-Language Pretrained Model for Chart Comprehension and Reasoning. *EMNLP 2023*. -- Outperforms MatCha on ChartQA and Chart-to-Text, establishing new SOTA for chart comprehension.

12. **Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Choi, Y., Eisenschlos, J., & Altun, Y.** (2023). DePlot: One-shot Visual Language Reasoning by Plot-to-Table Translation. *Findings of ACL 2023*. -- Translates chart images to linearized tables, then uses LLM for reasoning. 24% improvement over finetuned SOTA with one-shot prompting.

13. **Masry, A., Shahmohammadi, M., et al.** (2024). ChartInstruct: Instruction Tuning for Chart Comprehension and Reasoning. *Findings of ACL 2024*. -- 191K instructions over 71K charts. End-to-end and pipeline models for chart reasoning.

14. **Kantharaj, S., Leong, C.T., Lin, X., Masry, A., Thakkar, M., Hoque, E., & Joty, S.** (2022). Chart-to-Text: A Large-Scale Benchmark for Chart Summarization. *ACL 2022*. -- 44,096 charts from Statista and Pew Research. Models suffer from hallucinations and factual errors in numerical summaries.

### 5.4 VLM Failure Mode Analysis

15. **Huang, Y., Qin, Y., et al.** (2025). Why Vision Language Models Struggle with Visual Arithmetic? Towards Enhanced Chart and Geometry Understanding. *Findings of ACL 2025*. -- Documents VLM failures on basic visual arithmetic (counting, length comparison, area estimation). Proposes CogAlign post-training strategy. GPT-4o and InternVL2.5-78B struggle with probing tasks even with in-domain training.

16. **Shin, P.W. et al.** (2025). Losing the Plot: How VLM responses degrade on imperfect charts. *arXiv:2509.18425*. -- Introduces CHART NOISe dataset. Documents value fabrication, trend misinterpretation, entity confusion, and overconfidence in ChatGPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro on corrupted charts.

17. **FUGU Study** (2025). Diagnosing Bottlenecks in Data Visualization Understanding by Vision-Language Models. *arXiv:2510.21740*. -- Uses behavioral evaluation, causal interventions, and linear probes on LLaMA-3.2B 11B, LLaVA-OneVision 7B, InternVL3 14B. Finds primary bottleneck in vision-to-language hand-off, not visual encoding or math reasoning individually.

18. **Stanford CS231N** (2024). Understanding How Vision-Language Models Reason When Solving Visual Questions. *Course project report*. -- Analyzed where VLM failures originate: visual encoding, language reasoning, or vision-language transfer.

19. **CharXiv** (2024). Charting Gaps in Realistic Chart Understanding in Multimodal LLMs. *NeurIPS 2024 Datasets and Benchmarks Track*. -- 2,323 real-world charts from arXiv papers across 8 subjects. Separates descriptive questions (chart elements) from reasoning questions (comparisons, approximations). All questions manually curated with validated ground truth.

20. **ChartBench** (2024). A Benchmark for Complex Visual Reasoning in Charts. *arXiv:2312.15915*. -- 42 categories, 66.6K charts, 600K QA pairs. Charts lack data point annotations, requiring models to derive values from visual encodings.

21. **The Perils of Chart Deception** (2025). How Misleading Visualizations Affect Vision-Language Models. *arXiv:2508.09716*. -- All 10 tested models affected by axis manipulation (inverted axes, truncated axes, aspect ratio distortions).

### 5.5 Programmatic and Chain-of-Thought Approaches

22. **VProChart** (2024). Answering Chart Question Through Visual Perception Alignment Agent and Programmatic Solution Reasoning. *arXiv:2409.01667*. -- Uses Qwen2-7B-Instruct with code-driven reasoning for chart QA.

23. **Chart-based Reasoning** (2024). Transferring Capabilities from LLMs to VLMs. *arXiv:2403.12596*. -- Synthesizes reasoning traces using table representations of charts to improve numerical operations.

24. **Shin, P.W. et al.** (2025). GPT-5 Model Corrected GPT-4V's Chart Reading Errors, Not Prompting. *arXiv:2510.06782*. -- Demonstrates that model capability, not prompting strategy, is the primary driver of chart reading accuracy. GPT-5 outperforms GPT-4o by 20-40 percentage points.

---

## 6. Recommended Question Templates

### 6.1 Single-Step Computation (Level 1)

**Template 1 -- Simple Difference**
> "What is the difference in [metric] between [Category A] and [Category B]?"
> Expected answer type: Exact numerical value (tolerance: 5%)
> Example: "What is the difference in accuracy between GPT-4 and LLaVA?" -> 12.3

**Template 2 -- Simple Ratio**
> "What is the ratio of [Category A]'s value to [Category B]'s value?"
> Expected answer type: Decimal (tolerance: 5%)
> Example: "What is the ratio of the tallest bar to the shortest bar?" -> 3.2

**Template 3 -- Direct Percentage Read + Computation**
> "What percentage of the total does [Category X] represent?"
> Expected answer type: Percentage (tolerance: 5%)
> Example: "What percentage of total revenue comes from Product A?" -> 34.5%

### 6.2 Two-Step Computation (Level 2)

**Template 4 -- Percentage Change**
> "By what percentage did [metric] change from [Time 1] to [Time 2]?"
> Expected answer type: Percentage with sign (tolerance: 5%)
> Example: "By what percentage did sales increase from 2019 to 2023?" -> +42.7%

**Template 5 -- Identify-then-Compute**
> "What is the difference between the highest and lowest values shown in the chart?"
> Expected answer type: Numerical value (tolerance: 5%)
> Note: Requires identifying extremes before computing

**Template 6 -- Normalized Comparison**
> "How many times larger is the maximum value compared to the minimum value?"
> Expected answer type: Multiplier (tolerance: 5%)
> Example: "How many times larger is the tallest bar than the shortest?" -> 4.2x

### 6.3 Multi-Step Computation (Level 3)

**Template 7 -- Average Across Categories**
> "What is the average [metric] across all [N] categories shown?"
> Expected answer type: Decimal (tolerance: 5%)
> Example: "What is the average F1 score across all five models?" -> 78.4

**Template 8 -- Sum with Condition**
> "What is the total [metric] for all categories that exceed [threshold]?"
> Expected answer type: Numerical value (tolerance: 5%)
> Example: "What is the total accuracy for all models scoring above 80%?" -> 267.3

**Template 9 -- Relative Share Computation**
> "What fraction of the total is accounted for by the top [N] categories?"
> Expected answer type: Fraction or percentage (tolerance: 5%)
> Example: "What percentage of total emissions is represented by the top 3 countries?" -> 61.2%

### 6.4 Complex Multi-Step Computation (Level 4-5)

**Template 10 -- Cross-Series Comparison with Aggregation**
> "What is the difference in the average value between [Series A] and [Series B] across all time points?"
> Expected answer type: Numerical value (tolerance: 5%)
> Requires: Reading all values for both series, computing two averages, subtracting

**Template 11 -- Growth Rate Comparison**
> "Which category shows the largest percentage increase from the first to the last time point?"
> Expected answer type: Category name + percentage (tolerance: 5% on the numerical component)
> Requires: Computing percentage change for each category, comparing

**Template 12 -- Cross-Subplot Computation**
> "What is the ratio of the peak value in panel (a) to the peak value in panel (b)?"
> Expected answer type: Decimal ratio (tolerance: 5%)
> Requires: Navigating multi-panel layout, identifying peaks, dividing

**Template 13 -- Cumulative Computation**
> "At what point does the cumulative sum of all bars first exceed [threshold]?"
> Expected answer type: Category or position identifier
> Requires: Sequential reading and running sum

**Template 14 -- Variance/Spread Estimation**
> "What is the range (maximum minus minimum) of values shown for [Series X]?"
> Expected answer type: Numerical value (tolerance: 5%)

**Template 15 -- Weighted Metric**
> "Given the sample sizes shown in the table/figure, what is the weighted average [metric] across all groups?"
> Expected answer type: Decimal (tolerance: 5%)
> Requires: Reading both metrics and weights, computing weighted sum, dividing by total weight

### 6.5 Template Design Principles

1. **Specify precision expectations**: State whether approximate or exact answers are expected
2. **Avoid ambiguity in referents**: Clearly identify which chart elements to use
3. **Scale difficulty incrementally**: Start with L1 questions before L4-5
4. **Include distractor-free and distractor-rich variants**: Some questions with clear visual separation of values, others with dense overlapping data
5. **Test each arithmetic operation independently**: Have separate templates for addition, subtraction, multiplication, division, and comparison to diagnose per-operation weaknesses
6. **Pair computation questions with extraction-only questions**: Ask "What is the value of X?" before "What is the difference between X and Y?" to separate extraction errors from computation errors
7. **Use known ground truth**: Only pose computation questions where the underlying data table is available for verification
