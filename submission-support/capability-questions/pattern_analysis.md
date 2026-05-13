# Pattern Analysis in Scientific Figures: Strategies for Testing Vision-Language Models

> **Note:** This category was originally named "Trend Analysis" but was renamed to "Pattern Analysis" to accurately reflect its scope across all chart types. Trend analysis is a subset of pattern analysis that applies specifically to charts with ordered dimensions (time-series). The broader "Pattern Analysis" category follows the precedent set by CharXiv (Wang et al., NeurIPS 2024), which uses "PATT (Pattern Recognition)" as a chart-type-agnostic category.

## 1. What Pattern Analysis Tests in Scientific Figures

### 1.1 Definition

Pattern analysis in chart understanding refers to a model's ability to identify, characterize, and reason about structural patterns, distributions, and relationships across visual elements. It encompasses:

- **For line charts (trend analysis):** Directional patterns, trajectory reasoning across multiple data points, inflection points, convergence/divergence of series
- **For bar charts (distribution analysis):** Distribution shape (uniform, skewed, bimodal), ordering patterns across groups, symmetry/asymmetry, group-level consistency
- **For pie charts (proportion analysis):** Dominance patterns, concentration vs uniformity, segment relationships, threshold-based grouping

Unlike value reading (extracting a single data point), pattern analysis requires **reasoning across multiple elements** to infer higher-order properties of the data.

Core sub-capabilities tested by trend analysis include:

- **Direction identification**: Determining whether a data series is increasing, decreasing, or flat over a given interval.
- **Shape characterization**: Recognizing whether a trend is linear, exponential, logarithmic, polynomial, oscillating, U-shaped, inverted-U, sigmoidal, or step-wise.
- **Inflection point detection**: Identifying where a trend reverses direction or changes curvature (e.g., from concave-up to concave-down).
- **Convergence and divergence**: Assessing whether two or more data series are approaching each other (converging) or moving apart (diverging) over time.
- **Plateau detection**: Recognizing intervals where a series remains approximately constant despite changes elsewhere.
- **Rate of change comparison**: Determining which series increases or decreases faster, or whether a single series accelerates or decelerates.
- **Periodicity and oscillation**: Detecting cyclic patterns, their amplitude, and frequency.

### 1.2 Why Trend Analysis Requires Trajectory Reasoning

Value reading is a **local** task: it requires the model to locate a specific point on the chart and read its coordinate. Trend analysis is a **global** or **semi-global** task: it requires integrating information across multiple data points, often spanning the entire x-axis range or a specified sub-interval. This distinction is critical because:

1. **Perceptual integration**: The model must trace a visual path (a line, a sequence of bars, or scattered points) and extract its overall behavior, not just individual positions.
2. **Noise tolerance**: Real scientific data contains local fluctuations. The model must distinguish signal (the underlying trend) from noise (random variation around the trend).
3. **Multi-series reasoning**: In multi-line or grouped charts, the model must track each series independently and then compare or contrast their trends, requiring attentional separation of overlapping visual elements.
4. **Scale awareness**: The perceived steepness of a trend depends on axis scaling (linear vs. logarithmic, truncated vs. full-range). The model must account for axis properties when characterizing trends.
5. **Temporal reasoning**: Many scientific figures plot data over time, requiring the model to understand temporal ordering and causal implications of trend changes.

### 1.3 Taxonomy of Trend-Related Tasks

| Task Type | Cognitive Demand | Example |
|-----------|-----------------|---------|
| Direction (binary) | Low | "Is the accuracy increasing or decreasing between epoch 5 and epoch 20?" |
| Direction (ternary) | Low-Medium | "Is the loss increasing, decreasing, or stable after epoch 50?" |
| Shape identification | Medium | "Describe the overall pattern of the learning curve." |
| Inflection detection | Medium-High | "At approximately what x-value does the trend reverse?" |
| Rate comparison | High | "Which model's F1 score improves faster in the first 10 epochs?" |
| Convergence/divergence | High | "Do the two methods converge to similar performance by the end of training?" |
| Multi-panel consistency | High | "Is the upward trend in Panel A also present in Panel B?" |
| Complex pattern | Very High | "Describe the non-monotonic relationship between learning rate and accuracy." |

---

## 2. Known Failure Modes of Best VLMs

### 2.1 Systematic Hallucinations in Chart Understanding

The paper **"Losing the Plot: How VLM Responses Degrade on Imperfect Charts"** (arXiv:2509.18425, 2025) evaluated ChatGPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro, identifying several hallucination categories specific to chart interpretation:

- **Value fabrication**: Producing incorrect numerical values when reading from charts.
- **Trend misinterpretation**: Misreading upward or downward patterns, especially under visual corruption or occlusion.
- **Entity confusion**: Misidentifying which series or data element a trend belongs to in multi-series charts.
- **Reasoning hallucination**: Introducing unsupported logical steps when explaining chart patterns.
- **Table/translation drift**: Errors during chart-to-table conversion that compound when the extracted table is used for trend reasoning.

A key finding was **prompt reverse inconsistency**: models contradict themselves when asked to confirm versus deny the same trend statement, revealing shallow pattern matching rather than genuine understanding. Models also remain **overconfident in degraded settings**, generating plausible but unsupported trend explanations.

### 2.2 Consistency and Robustness Failures

**"Unraveling the Truth: Do VLMs Really Understand Charts?"** (Mukhopadhyay et al., EMNLP 2024 Findings) introduced two diagnostic datasets:

- **ChartQA-Split**: Tests consistency across varying levels of chart and question complexity.
- **RobustCQA**: Tests robustness to visual perturbations (e.g., changing chart type while keeping data identical).

Key findings:
- Significant **performance variations based on question type and chart format**, suggesting models rely on surface-level visual cues rather than data understanding.
- When the same data is presented in different chart types (e.g., line chart vs. bar chart), models give **inconsistent trend descriptions**, indicating lack of genuine data comprehension.
- Performance degrades with chart complexity, particularly with overlapping series and dense data.

### 2.3 Specific Trend-Related Failure Modes

Based on the literature, the following failure modes are documented or well-attested:

**a) Confusing local fluctuations with overall trend**
- Models often describe a generally increasing series as "fluctuating" or "unstable" because of minor local dips, missing the dominant upward pattern.
- Conversely, models may describe a noisy flat series as "slightly increasing" due to the last few data points trending upward.

**b) Missing inflection points**
- Models frequently fail to identify where a trend reverses, particularly in U-shaped or inverted-U curves.
- When asked "at what point does the trend change direction?", models may report the wrong x-value or deny the existence of an inflection point.

**c) Series confusion in multi-line charts**
- In charts with multiple overlapping lines (common in ML training curves, ablation studies), models confuse which line exhibits which trend.
- Color-legend mapping errors are a primary cause: models misattribute a trend from one series to another.

**d) Non-monotonic trend failures**
- U-shaped relationships (e.g., optimal hyperparameter tuning) are described as "decreasing" (attending only to the first half) or "increasing" (attending only to the second half).
- Oscillating patterns are often summarized as a single directional trend.

**e) Scale misinterpretation**
- Models misinterpret the steepness of trends when axes use logarithmic scales, often describing exponential growth as "linear" or "gradual" because the log scale compresses the visual.
- Truncated y-axes (not starting from zero) cause models to overstate the magnitude of trends.

**f) Temporal window blindness**
- When asked about a specific sub-interval (e.g., "between epoch 10 and 20"), models often describe the entire series trend instead, ignoring the specified temporal window.

### 2.4 Performance Gaps by Model

From CharXiv (NeurIPS 2024) and EvoChart (AAAI 2025):

| Model | CharXiv Accuracy | EvoChart-QA Accuracy | Notes |
|-------|-----------------|---------------------|-------|
| GPT-4o | 47.1% | 49.8% | Best proprietary in 2024 |
| InternVL Chat V1.5 | 29.2% | -- | Best open-source in 2024 |
| Human experts | 80.5% | -- | CharXiv baseline |

The **33+ percentage point gap** between GPT-4o and human performance on CharXiv underscores that even frontier models have substantial deficits in chart understanding, with trend-related reasoning questions being among the hardest categories.

From MathVista (ICLR 2024), the best model (GPT-4V) achieved 49.9% overall accuracy on mathematical reasoning in visual contexts, with figure question answering being a particularly challenging subtask.

---

## 3. Best Question Design Strategies

### 3.1 Direction Questions

These test the most fundamental trend capability: identifying whether a series goes up, down, or stays flat.

**Design principles:**
- Specify the series explicitly (by name, color, or label).
- Specify the interval of interest (avoid ambiguity about which part of the x-axis).
- Use forced-choice format for reliability: "increasing", "decreasing", or "approximately constant".
- Include distractor conditions where a sub-interval contradicts the overall trend.

**Example:**
> "Between x=10 and x=50, is the blue line (Model A) generally increasing, decreasing, or approximately constant?"

### 3.2 Shape Questions

These test the ability to characterize the overall functional form of a series.

**Design principles:**
- Provide a vocabulary of shapes to choose from (linear, exponential, logarithmic, sigmoidal, U-shaped, oscillating) to avoid open-ended ambiguity.
- Alternatively, ask for open-ended descriptions and evaluate with a rubric.
- Include charts with genuinely different shapes to test discrimination.

**Example:**
> "Which best describes the overall shape of the training loss curve: (a) linear decrease, (b) exponential decay, (c) step-wise decrease, (d) oscillating decrease?"

### 3.3 Inflection Point Questions

These test whether the model can identify where a trend changes direction or curvature.

**Design principles:**
- Use charts with clear, unambiguous inflection points.
- Accept a range of answers (e.g., "between x=15 and x=20") rather than exact values.
- Include negative controls: charts with no inflection point where the correct answer is "none".

**Example:**
> "At approximately what value of the learning rate does the validation accuracy stop increasing and begin to decrease?"

### 3.4 Convergence Questions

These test multi-series comparative reasoning.

**Design principles:**
- Require the model to track two or more series simultaneously.
- Distinguish convergence (gap narrows) from crossing (lines intersect) from parallel movement.
- Specify the region of interest.

**Example:**
> "Do the performance curves of Model A and Model B converge by epoch 100, or does a gap remain?"

### 3.5 Rate Comparison Questions

These test relative slope reasoning.

**Design principles:**
- Compare slopes of two series in the same chart or the same series in two intervals.
- Use both same-scale and different-scale scenarios.
- Include cases where visual steepness is misleading due to axis scaling.

**Example:**
> "In the first 20 epochs, which model shows a faster decrease in training loss: ResNet-50 or VGG-16?"

### 3.6 Multi-Panel Trend Consistency Questions

These test the ability to compare trends across separate subplots.

**Design principles:**
- Use figures with multiple panels sharing the same data variable but different conditions.
- Ask whether a trend observed in one panel is consistent, reversed, or absent in another.
- This tests both trend identification and cross-panel visual integration.

**Example:**
> "The left panel shows results on CIFAR-10 and the right panel shows results on ImageNet. Does the same ranking of models (by final accuracy) hold in both panels?"

### 3.7 Temporal Window Questions

These test the ability to focus on a specified sub-interval.

**Design principles:**
- Explicitly state the start and end of the interval.
- Choose intervals where the local trend differs from the global trend.
- This is a strong test because models must override their tendency to describe the overall pattern.

**Example:**
> "Looking only at the region between temperature 0.5 and 1.0, what happens to the BLEU score?"

### 3.8 Plateau Detection Questions

**Design principles:**
- Ask whether and where a series levels off.
- Include both true plateaus and slow-growth regions that may appear plateau-like.
- Specify a tolerance criterion if needed (e.g., "approximately constant, varying by less than 2%").

**Example:**
> "After approximately how many training steps does the perplexity appear to plateau?"

---

## 4. Evaluation Strategies

### 4.1 Categorical Scoring for Direction and Shape

For forced-choice questions (direction, shape classification, yes/no convergence), use **exact match** or **categorical accuracy**:

- **Direction questions**: Correct if the model selects the right category (increasing/decreasing/constant). Score: 1 (correct) or 0 (incorrect).
- **Shape questions**: Correct if the model selects the right functional form. Score: 1 or 0.
- **Yes/No questions** (e.g., "Do the lines converge?"): Exact match. Score: 1 or 0.

Following ChartBench's **Acc++ metric**, avoid simple string matching in favor of semantic matching that accounts for paraphrases (e.g., "goes up" = "increases" = "rises").

### 4.2 Numerical Tolerance for Inflection Points

For questions asking "at what x-value does the trend change?":
- Allow a **tolerance window** (e.g., +/- 5% of the x-axis range, or +/- 1 tick mark).
- Following ChartQA's convention, a **5% relative error margin** is standard for numerical answers.
- Score: 1 if within tolerance, 0 otherwise.

### 4.3 Open-Ended Evaluation for Pattern Descriptions

For open-ended trend descriptions ("Describe the overall pattern of..."), use a **rubric-based scoring system**:

**Rubric dimensions (adapted from Chart-to-Text evaluation and GPT-score frameworks):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Factual accuracy** | 40% | Does the description correctly identify the direction, shape, and key features of the trend? |
| **Completeness** | 25% | Does the description mention all salient trend features (e.g., inflection points, plateaus, rate changes)? |
| **Specificity** | 20% | Does the description reference specific data points, intervals, or values rather than vague generalities? |
| **Absence of hallucination** | 15% | Does the description avoid fabricating trends, values, or features not present in the chart? |

**Scoring scale**: 0-5 (following ChartX's GPT-score convention):
- 5: Complete, accurate, specific, no hallucination
- 4: Mostly complete and accurate, minor omissions
- 3: Captures the main trend but misses secondary features
- 2: Partially correct but contains errors or significant omissions
- 1: Mostly incorrect or highly incomplete
- 0: Completely wrong or describes a different chart

### 4.4 LLM-as-Judge for Trend Descriptions

Following the evaluation paradigm used in ChartQA-X (WACV 2026) and ChartX:

- Use a reference answer (ground truth trend description) and have an LLM judge score the model's response.
- **GPT-acc**: For unambiguous answers, binary scoring with 5% numerical tolerance.
- **GPT-score**: For open-ended responses, 0-5 scale scoring based on completeness, relevance, accuracy, and absence of fabrication.
- Use **ROSCOE scores** (from ChartQA-X) for evaluating explanation quality and reasoning chain validity.

### 4.5 Consistency-Based Evaluation

Following Mukhopadhyay et al. (EMNLP 2024):

- **Paraphrase consistency**: Ask the same trend question in different phrasings and measure agreement.
- **Visual perturbation consistency**: Present the same data in different chart types (line vs. bar) and check if trend answers remain consistent.
- **Prompt reverse consistency**: Ask the model to both confirm and deny a trend statement; inconsistency reveals shallow reasoning.

### 4.6 Handling Subjective Trend Descriptions

Some trend characterizations are inherently subjective (e.g., is a curve "rapidly increasing" or "moderately increasing"?). Strategies to handle this:

1. **Anchor to relative comparisons**: Instead of asking "is the increase rapid?", ask "which series increases more rapidly?"
2. **Provide reference points**: "Compared to a linear increase from 0 to 100, does this curve increase faster or slower in the first half?"
3. **Use ordinal rather than cardinal descriptors**: Instead of expecting specific growth rate numbers, accept ordinal rankings (fastest, second-fastest, slowest).
4. **Multiple annotator agreement**: For ground truth, use majority vote from 3+ human annotators on trend characterization.

---

## 5. References

### 5.1 Chart Understanding Benchmarks

1. **ChartQA**: Masry, A., Long, D., Tan, J. Q., Joty, S., & Hoque, E. (2022). "ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning." ACL 2022. -- Introduced 9,608 human-written and 23,111 machine-generated QA pairs over 4,804 charts; established the 5% tolerance convention for numerical answers.

2. **PlotQA**: Methani, N., Ganguly, P., Khapra, M. M., & Kumar, P. (2020). "PlotQA: Reasoning over Scientific Plots." WACV 2020. -- 28.9 million QA pairs over 224,377 plots from real-world sources; questions categorized into structural understanding, data retrieval, and reasoning; 80.76% of answers require out-of-vocabulary reasoning.

3. **CharXiv**: Wang, Z., Xia, M., et al. (2024). "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs." NeurIPS 2024 Datasets & Benchmarks Track. -- 2,323 charts from arXiv papers with descriptive and reasoning questions; GPT-4o achieves 47.1% vs. human 80.5%; adopted into evaluations for GPT-4.1, Qwen2.5-VL, InternVL2.5.

4. **ChartBench**: Xu, Z., et al. (2024). "ChartBench: A Benchmark for Complex Visual Reasoning in Charts." arXiv:2312.15915. -- 42 chart categories, 66.6k charts, 600k QA pairs; introduced Acc++ metric; emphasizes visual rather than textual reasoning.

5. **ChartX & ChartVLM**: Xia, R., Zhang, B., et al. (2024). "ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning." IEEE Transactions on Signal Processing. -- 48K multi-modal chart data covering 18 chart types, 22 topics, 7 tasks (including chart description and summarization); introduced GPT-score (0-5) for open-ended evaluation.

6. **EvoChart**: (2025). "EvoChart: A Benchmark and a Self-Training Approach Towards Real-World Chart Understanding." AAAI 2025, 39(4):3680-3688. -- 650 real-world charts, 1,250 expert-curated questions; GPT-4o achieves only 49.8%; tests direct retrieval and complex multi-step retrieval.

7. **ChartQA-X**: Hegde, S., et al. (2025/2026). "ChartQA-X: Generating Explanations for Visual Chart Reasoning." WACV 2026. -- 30,299 chart samples with detailed explanations; uses ROSCOE scores for explanation quality; fine-tuned models achieve +14.75% improvement.

8. **FigureQA**: Kahou, S. E., et al. (2018). "FigureQA: An Annotated Figure Dataset for Visual Reasoning." ICLR 2018 Workshop. -- Synthetic figure dataset with yes/no questions about visual properties and relationships.

9. **DVQA**: Kafle, K., Price, B., Cohen, S., & Kanan, C. (2018). "DVQA: Understanding Data Visualizations via Question Answering." CVPR 2018. -- Bar chart QA requiring structural, data, and reasoning-level understanding.

10. **MathVista**: Lu, P., et al. (2024). "MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts." ICLR 2024. -- 6,141 examples from 31 datasets; includes FunctionQA (algebraic reasoning over functional plots) and PaperQA (scientific reasoning with paper figures); GPT-4V achieves 49.9%.

### 5.2 Chart Summarization and Description

11. **Chart-to-Text**: Obeid, J., & Hoque, E. (2022). "Chart-to-Text: A Large-Scale Benchmark for Chart Summarization." ACL 2022. -- 44,096 charts with summaries; found that models suffer from hallucinations and factual errors in trend descriptions.

12. **ChartSumm**: Rahman, M., et al. (2023). "ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization of Long and Short Summaries." arXiv:2304.13620. -- 84,363 charts; documents issues with hallucination, missing important data points, and incorrect explanation of complex trends.

### 5.3 Robustness and Failure Analysis

13. **"Losing the Plot"**: (2025). "Losing the Plot: How VLM Responses Degrade on Imperfect Charts." arXiv:2509.18425. -- Introduces CHART NOISe dataset; evaluates GPT-4o, Claude Sonnet 4, Gemini 2.5 Pro under corruption/occlusion; documents value fabrication, trend misinterpretation, entity confusion; introduces prompt reverse inconsistency test.

14. **"Do VLMs Really Understand Charts?"**: Mukhopadhyay, S., Qidwai, A., Garimella, A., Ramu, P., Gupta, V., & Roth, D. (2024). "Unraveling the Truth: Do VLMs Really Understand Charts? A Deep Dive into Consistency and Robustness." Findings of EMNLP 2024. -- Introduces ChartQA-Split and RobustCQA datasets; tests consistency across chart types and visual perturbations.

15. **"GPT-5 Model Corrected GPT-4V's Chart Reading Errors"**: (2025). arXiv:2510.06782. -- Demonstrates that model scaling (GPT-5 vs. GPT-4o) yields larger improvements than prompt engineering for chart reading tasks.

### 5.4 Time Series and Temporal Reasoning

16. **MTBench**: (2025). "MTBench: A Multimodal Time Series Benchmark for Temporal Reasoning and Question Answering." arXiv:2503.16858. -- Evaluates LLMs on time series and text understanding in financial and weather domains.

17. **TRQA**: (2025). "TRQA: Time Series Reasoning Question and Answering Benchmark." OpenReview. -- Unifies six temporal reasoning tasks including anomaly detection, characterization, comparison, and temporal relationship reasoning.

18. **TimeSeriesExamAgent**: (2026). "TimeSeriesExamAgent: Creating Time Series Reasoning Benchmarks at Scale." arXiv:2604.10291. -- All models achieve less than 55% mean accuracy on time series reasoning, underscoring the difficulty for current VLMs.

### 5.5 Surveys

19. **"From Pixels to Insights"**: Huang, K.-H., Chan, H. P., Fung, Y., Qiu, H., Zhou, M., Joty, S., Chang, S.-F., & Ji, H. (2024). "From Pixels to Insights: A Survey on Automatic Chart Understanding in the Era of Large Foundation Models." IEEE TKDE. -- Comprehensive survey covering chart understanding tasks, datasets, models, and evaluation approaches.

20. **VLM Survey (26K Papers)**: (2025). "Vision Language Models: A Survey of 26K Papers." arXiv:2510.09586. -- Meta-analysis of VLM research trends across CVPR, ICLR, NeurIPS 2023-2025.

### 5.6 Related Evaluation Frameworks

21. **ChartAssistant**: Meng, F., et al. (2023). "ChartAssistant: A Universal Chart Multimodal Language Model via Chart-to-Table Pre-training and Multitask Instruction Tuning." ACL 2024 Findings. -- Specializes in chart comprehension including trend description generation.

22. **VProChart**: (2025). "VProChart: Answering Chart Questions Through Visual Perception Alignment Agent and Programmatic Solution Reasoning." AAAI 2025. -- Combines visual perception with programmatic reasoning for chart QA.

23. **Chart-CoCa**: (2025). "Chart-CoCa: Self-Improving Chart Understanding of Vision LMs via Code-Driven Synthesis and Candidate-Conditioned Answering." arXiv:2508.11975.

24. **AltChart**: (2024). "AltChart: Enhancing VLM-Based Chart Summarization Through Multi-Pretext Tasks." ECAI 2024.

25. **mChartQA**: (2024). "mChartQA: A Universal Benchmark for Multimodal Chart Question Answering." arXiv:2404.01548. -- Multilingual chart QA evaluation.

---

## 6. Recommended Question Templates

### Template 1: Simple Direction (Binary)
**Question**: "Between [x1] and [x2], is the [series_name] line increasing or decreasing?"
**Expected answer type**: Categorical (increasing / decreasing)
**Difficulty**: Easy
**Capability tested**: Basic direction identification

### Template 2: Direction with Stability Option (Ternary)
**Question**: "After [x_value], does the [series_name] series increase, decrease, or remain approximately constant?"
**Expected answer type**: Categorical (increasing / decreasing / approximately constant)
**Difficulty**: Easy-Medium
**Capability tested**: Direction identification with plateau detection

### Template 3: Overall Shape Classification
**Question**: "Which of the following best describes the overall shape of the [series_name] curve: (a) linear, (b) exponential growth, (c) logarithmic (fast then slow), (d) sigmoidal (S-shaped), (e) U-shaped, (f) inverted U-shaped?"
**Expected answer type**: Multiple choice
**Difficulty**: Medium
**Capability tested**: Shape characterization

### Template 4: Inflection Point Detection
**Question**: "At approximately what value of [x_variable] does the [series_name] curve change from increasing to decreasing (or vice versa)? If no such change occurs, answer 'none'."
**Expected answer type**: Numerical with tolerance, or "none"
**Difficulty**: Medium-Hard
**Capability tested**: Inflection point detection

### Template 5: Rate Comparison Between Series
**Question**: "In the interval from [x1] to [x2], which series shows a faster rate of increase: [series_A] or [series_B]?"
**Expected answer type**: Categorical (series name)
**Difficulty**: Medium-Hard
**Capability tested**: Relative rate comparison

### Template 6: Convergence/Divergence
**Question**: "Do the [series_A] and [series_B] curves converge (get closer together), diverge (move farther apart), or maintain approximately the same gap between [x1] and [x2]?"
**Expected answer type**: Categorical (converge / diverge / maintain gap)
**Difficulty**: Hard
**Capability tested**: Multi-series comparative trend reasoning

### Template 7: Temporal Window Focus
**Question**: "Looking only at the region between [x1] and [x2], describe what happens to the [metric_name]. Ignore the behavior outside this range."
**Expected answer type**: Open-ended (scored with rubric)
**Difficulty**: Medium
**Capability tested**: Interval-specific trend analysis, resistance to global-trend bias

### Template 8: Plateau Identification
**Question**: "Does the [series_name] curve appear to plateau (level off) at any point? If so, at approximately what [x_variable] value does the plateau begin, and what is the approximate [y_variable] value at the plateau?"
**Expected answer type**: Yes/No + Numerical (with tolerance)
**Difficulty**: Medium-Hard
**Capability tested**: Plateau detection with localization

### Template 9: Multi-Panel Trend Consistency
**Question**: "Panel (a) shows results for [condition_A] and Panel (b) shows results for [condition_B]. Does the [series_name] show the same directional trend (increasing/decreasing) in both panels?"
**Expected answer type**: Categorical (yes, same trend / no, different trends)
**Difficulty**: Hard
**Capability tested**: Cross-panel comparison, multi-figure reasoning

### Template 10: Complex Non-Monotonic Pattern Description
**Question**: "Describe the complete behavior of the [series_name] curve from left to right, noting any changes in direction, rate, or pattern. Mention specific [x_variable] values where notable changes occur."
**Expected answer type**: Open-ended (scored with rubric)
**Difficulty**: Hard
**Capability tested**: Comprehensive trend characterization

### Template 11: Series Crossing Detection
**Question**: "Do the [series_A] and [series_B] lines cross at any point in this chart? If so, at approximately what [x_variable] value, and which series is higher before vs. after the crossing?"
**Expected answer type**: Yes/No + Numerical + Categorical
**Difficulty**: Medium-Hard
**Capability tested**: Intersection detection, pre/post-crossing reasoning

### Template 12: Acceleration/Deceleration
**Question**: "Does the rate of increase of [series_name] appear to accelerate (get steeper over time), decelerate (flatten out over time), or remain constant between [x1] and [x2]?"
**Expected answer type**: Categorical (accelerate / decelerate / constant rate)
**Difficulty**: Hard
**Capability tested**: Second-order trend reasoning (rate of rate)

### Template 13: Scale-Aware Trend Question
**Question**: "This chart uses a logarithmic y-axis. Given this scaling, is the actual (non-log) growth of [series_name] between [x1] and [x2] best described as: (a) linear, (b) polynomial, (c) exponential?"
**Expected answer type**: Multiple choice
**Difficulty**: Very Hard
**Capability tested**: Scale interpretation + trend reasoning

### Template 14: Outlier vs. Trend Discrimination
**Question**: "The [series_name] shows a sharp spike at [x_value]. Ignoring this spike, what is the overall trend of the series?"
**Expected answer type**: Categorical direction + open-ended description
**Difficulty**: Medium
**Capability tested**: Noise/outlier tolerance in trend identification

### Template 15: Comparative Trend Across Metrics
**Question**: "As [metric_A] increases from [x1] to [x2] (shown in the top subplot), what happens to [metric_B] (shown in the bottom subplot) over the same [x_variable] range? Are they positively correlated, negatively correlated, or uncorrelated?"
**Expected answer type**: Categorical (positive / negative / uncorrelated)
**Difficulty**: Very Hard
**Capability tested**: Cross-subplot correlation reasoning

---

## 7. Summary of Recommendations for SciFig-Evaluation

### Question Design Priorities
1. **Start with forced-choice direction questions** as a baseline capability test (Templates 1-2).
2. **Add shape classification** to test pattern recognition beyond simple direction (Template 3).
3. **Include inflection and plateau detection** for medium-difficulty probes (Templates 4, 8).
4. **Test multi-series reasoning** with convergence, rate comparison, and crossing questions (Templates 5, 6, 11).
5. **Challenge with scale-awareness and non-monotonic patterns** for hard probes (Templates 10, 13, 14).

### Evaluation Protocol
- Use **exact match** for categorical questions.
- Use **5% tolerance** for numerical answers (following ChartQA convention).
- Use **rubric-based GPT-score (0-5)** for open-ended descriptions.
- Add **consistency checks** (paraphrase, visual perturbation, prompt reversal) to detect shallow reasoning.
- Report results **stratified by difficulty level and trend type** to enable fine-grained analysis.

### Known Gaps to Exploit
- Non-monotonic trends (U-shaped, oscillating) are the weakest area for all current VLMs.
- Multi-series charts with overlapping or crossing lines cause entity confusion.
- Logarithmic scales are consistently misinterpreted.
- Temporal window questions expose models' tendency to describe global rather than local trends.
- Corrupted or occluded charts cause disproportionate hallucination in trend descriptions.
