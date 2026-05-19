# VLM Description Tasks for Line Plots in Scientific Figures: A Comprehensive Research Survey

---

## 1. What Makes Line Plot Description Challenging for VLMs

### 1.1 Overlapping and Dense Visual Elements

Line plots in scientific papers frequently contain multiple overlapping series, dense data points, small markers, and thin line segments that create severe visual ambiguity. The LineEX system (P. et al., 2023) identified that line charts with 2--6 lines present escalating difficulty for data extraction, as lines may cross, overlap, or run parallel with minimal separation. When lines share similar trajectories, even specialized line detection models using Siamese neural networks struggle with keypoint grouping (P. et al., 2023). For VLMs, this problem is compounded: the vision encoder must resolve fine-grained spatial relationships between pixel-level features that may differ by only a few pixels in the rasterized image.

The FUGU benchmark (Tartaglini et al., 2025) demonstrated through activation patching that even when a VLM's vision encoder correctly extracts data point coordinates into its latent representations, the vision-language handoff introduces errors. This architectural bottleneck means that correct visual perception does not guarantee correct textual description -- a fundamental challenge for line plot understanding.

### 1.2 Trajectory Reasoning: Trends, Inflection Points, and Convergence

Describing line plots requires trajectory reasoning -- identifying whether a line is increasing, decreasing, oscillating, converging with another line, or exhibiting inflection points. ChartMuseum (Li et al., 2025) revealed a 35--55% performance drop on visual reasoning questions compared to text-reasoning questions across all evaluated models, with trend identification being a core visual reasoning capability that VLMs systematically underperform on.

The ChartInsights benchmark (Wu et al., 2024) formally categorized trend-related tasks as "low-level" chart analysis tasks and found that the average accuracy across 19 advanced MLLMs was only 39.8% on such tasks, with even GPT-4o achieving only 69.17%. Identifying inflection points -- where a trend reverses direction -- requires the model to reason about second-order derivatives of visual curves, a capability that current VLMs largely lack.

### 1.3 Color Discrimination and Entity Confusion

Distinguishing between similarly colored lines is a persistent VLM weakness. Bendeck and Stasko (2024) found in their IEEE VIS evaluation that GPT-4V showed "a tendency to misread relatively unambiguous color legends on stacked bar charts," with the problem being even more acute for line plots where color is applied to thin 1--2 pixel strokes rather than filled regions. The "Losing the Plot" study (Kim et al., 2025) formally categorized "entity confusion" -- misidentifying which line corresponds to which legend entry -- as one of the primary hallucination modes in chart understanding, observing that it becomes more frequent under visual corruption or degradation.

The Perils of Chart Deception study (Mahbub et al., 2025) further showed that all 10 evaluated VLMs failed to identify axis inversion, and 9 out of 10 were affected by aspect ratio distortions. These spatial-structural failures directly impact line plot description, where the perceived slope of a line depends on the aspect ratio and axis configuration.

### 1.4 Precise Value Reading from Continuous Curves

Unlike bar charts where values correspond to discrete bar heights, line plots require interpolation between gridlines to read values at arbitrary x-coordinates. Bendeck and Stasko (2024) found that "GPT-4 struggles with simple value retrieval when not provided with the original dataset." The ChartInsights evaluation showed that even with the Chain-of-Charts prompting strategy that improved performance to 83.58%, precise numerical value extraction from continuous curves remains significantly harder than from discrete chart types.

The FUGU study (Tartaglini et al., 2025) provided a mechanistic explanation: while providing correct coordinates helps VLMs with tasks involving one or a small number of data points, it "generally worsens performance for tasks that require extracting statistical relationships across many data points." This suggests a fundamental capacity limitation in how VLMs process dense sequential visual information -- precisely the kind of information line plots contain.

### 1.5 Dual Y-Axes, Logarithmic Scales, and Confidence Intervals

Complex line plot features present additional challenges. The Perils of Chart Deception study (Mahbub et al., 2025) evaluated eight misleading chart designs including dual axes, truncated axes, and inverted axes, finding that "current VLMs are more prone to errors in interpreting spatial scale and structure than in detecting improper data encodings." Dual y-axes require the model to correctly associate each line series with its corresponding axis -- a task that introduces a second dimension of entity mapping beyond the legend.

Logarithmic scales present a distinct challenge because the visual distance between values is non-linear. A line that appears to flatten on a log-scale plot may actually represent exponential growth, and VLMs frequently fail to account for scale type when describing trends. Confidence intervals and shaded regions add uncertainty information that requires the model to distinguish between the central tendency line and its bounds -- a capability that current VLMs handle poorly, as demonstrated by the systematic performance gaps documented in the "Unraveling the Truth" study (Akhtar et al., 2024).

### 1.6 Multi-Panel and Subplot Coordination

Scientific papers frequently present related line plots as multi-panel figures (e.g., subplots labeled a, b, c, d) that share axes, legends, or experimental conditions. SciFIBench (Roberts et al., 2024) evaluated VLMs on scientific figure interpretation from arXiv papers and found significant gaps between model and human performance, with humans achieving 86.4% accuracy on figure-to-caption matching while the best models lagged substantially. Cross-panel reasoning -- such as noting that a trend visible in panel (a) reverses in panel (b) under different conditions -- requires compositional visual reasoning that current VLMs do not reliably perform.

---

## 2. What Should a Complete Line Plot Description Contain

### 2.1 The Four-Level Semantic Content Model

Lundgard and Satyanarayan (2022) established the foundational framework for chart description content through their four-level model of semantic content, developed from a grounded theory analysis of 2,147 descriptive sentences:

- **Level 1 (Construction):** Chart type identification, axis labels, units, scale types (linear/log), ranges, tick mark intervals, title, legend entries, color/style mappings.
- **Level 2 (Statistics):** Specific numerical values, extrema (maxima, minima), means, ranges, differences between data points, correlations between series.
- **Level 3 (Perceptual/Cognitive):** Trends (increasing, decreasing, stable), patterns (cyclical, oscillatory), inflection points, convergence/divergence of lines, anomalies, comparative relationships ("Line A consistently outperforms Line B").
- **Level 4 (Domain-Specific):** Contextual interpretation of patterns, causal explanations, implications for the field, connections to hypotheses.

Their user study found that both blind and sighted participants rated Level 3 content as most useful, while blind participants found Level 2 content more useful than sighted participants. This hierarchy directly informs what a complete line plot description should prioritize.

### 2.2 What Benchmarks Expect

The VisText benchmark (Tang et al., 2023) operationalized the Lundgard-Satyanarayan model by pairing 12,441 charts with both synthetic L1 captions (construction details) and human-authored L2/L3 captions (trends and statistics). This established a concrete standard: a complete description should cover both structural elements and semantic interpretation.

ChartQA (Masry et al., 2022) expects models to answer questions requiring both visual and logical reasoning about charts, implying that descriptions should contain sufficient detail to support downstream reasoning. PlotQA (Methani et al., 2020) specifically addresses scientific plots with open-vocabulary questions requiring mathematical operations, setting the expectation that descriptions should include precise numerical information where readable.

The Chart-to-Text benchmark (Kantharaj et al., 2022) expects natural language summaries that explain data patterns and trends -- not merely enumerate values. Their analysis showed that human-written chart summaries typically combine factual reporting with trend interpretation.

### 2.3 Essential Content Elements for Line Plots

Based on the synthesis of benchmark expectations and the semantic content model, a complete line plot description should contain:

**Structural Elements (L1):**
- Chart type and title
- X-axis: label, units, range, scale type, direction
- Y-axis: label, units, range, scale type; if dual y-axes, both described
- Number of lines/series and their legend mappings
- Visual encoding: color, line style (solid, dashed, dotted), marker type for each series
- Presence of annotations, reference lines, confidence intervals, or shaded regions

**Statistical Elements (L2):**
- Starting and ending values for each line (where readable)
- Maximum and minimum values with their x-coordinates
- Notable specific data points (peaks, troughs, crossover points)
- Approximate magnitude of changes

**Trend and Pattern Elements (L3):**
- Overall trajectory of each line (increasing, decreasing, stable, non-monotonic)
- Rate of change descriptions (steep, gradual, exponential)
- Inflection points where trends reverse
- Convergence or divergence between series
- Crossover points where lines intersect
- Relative ordering of lines across the x-axis range

### 2.4 Handling Dense Multi-Line Plots

For plots with many lines (5+), attempting to describe every line individually produces unwieldy descriptions. The VisText approach suggests a prioritization strategy: describe the overall pattern first, then highlight notable outliers or exceptional series. The ChaTS-Pi approach (Krichene et al., 2024) demonstrates that faithful summarization need not be exhaustive -- summaries that capture key patterns while omitting minor details can be both more readable and more accurate than attempts at comprehensive enumeration.

For scientific line plots specifically, the recommended approach from the accessibility literature (Lundgard and Satyanarayan, 2022) is:
1. Describe the general pattern shared by most lines
2. Identify and describe the best-performing and worst-performing series
3. Note any series that deviate significantly from the general pattern
4. Describe crossover points and rank changes

---

## 3. Common VLM Errors on Line Plots

### 3.1 Taxonomy of Errors

The CHOCOLATE dataset (Huang et al., 2024a) established a systematic error taxonomy through large-scale human annotation of chart captions generated by LVLMs. Their analysis found that LVLMs have a non-factual rate of 81.27% in chart captioning. The primary error categories relevant to line plots include:

1. **Value fabrication:** Generating specific numerical values that do not appear in the chart
2. **Trend misinterpretation:** Describing an increasing trend as decreasing, or vice versa
3. **Entity confusion:** Attributing properties of one line series to another
4. **Reasoning hallucination:** Introducing unsupported logical relationships between data elements
5. **Table/translation drift:** Errors in intermediate chart-to-table conversion that propagate to descriptions

### 3.2 Trend Misidentification

Trend misidentification is among the most consequential errors for line plot descriptions. The "Losing the Plot" study (Kim et al., 2025) documented that all three frontier models (GPT-4o, Claude Sonnet 4, and Gemini 2.5 Pro) exhibited trend misinterpretation, with the problem becoming "more frequent and severe" under visual corruptions. The "Unraveling the Truth" study (Akhtar et al., 2024) specifically investigated consistency, finding that VLMs may correctly identify a trend when asked directly but contradict themselves when the same information is queried from a different angle.

The Perils of Chart Deception study (Mahbub et al., 2025) showed that inverted axes affect all 10 evaluated models, meaning a model may report an "increasing" trend because the visual line goes upward, even when the y-axis is inverted and the actual values are decreasing.

### 3.3 Entity Confusion and Legend Misreading

Entity confusion -- attributing data or trends from one line to another -- is particularly prevalent in multi-series line plots. Bendeck and Stasko (2024) documented GPT-4V's tendency to misread color legends. This error is compounded when lines are similarly colored, when the legend placement is far from the lines, or when line styles (solid vs. dashed) carry the distinguishing information rather than color.

### 3.4 Precise Value Errors and Scale Misinterpretation

ChartInsights (Wu et al., 2024) demonstrated that models achieve significantly lower accuracy on value retrieval tasks compared to pattern recognition tasks. The "Diagnosing Bottlenecks" study (Tartaglini et al., 2025) showed that even when vision encoders correctly represent coordinate information, the language generation stage introduces numerical errors.

Scale misinterpretation -- confusing logarithmic and linear scales -- leads to systematic magnitude errors. A value of 100 on a log scale occupies the same visual space as dramatically different values on a linear scale, and VLMs frequently fail to adjust their numerical descriptions for the scale type.

### 3.5 Data Point Fabrication

The CHOCOLATE analysis (Huang et al., 2024a) found that VLMs frequently generate plausible-sounding but fabricated specific values, especially when the chart does not contain data labels. For line plots without data point markers, models may report values at x-coordinates where no data point exists, or assign precise numbers to points that can only be approximately read from the chart.

### 3.6 Missing Structural Elements

The "Are LVLMs Up to the Challenge" study (Islam et al., 2024) found that models frequently omit critical structural information such as axis labels, units, and scale types when generating descriptions. For line plots, omitting the y-axis scale type (log vs. linear) or failing to note dual y-axes fundamentally undermines the description's utility.

### 3.7 Overconfidence in Degraded Conditions

The "Losing the Plot" study (Kim et al., 2025) introduced the concept of "prompt reverse inconsistency" -- models contradict themselves when asked to confirm versus deny the same statement about a chart. Critically, they found that "when essential information is occluded, models often fail to acknowledge the occlusion and instead generate answers based solely on remaining unoccluded data," demonstrating a systematic overconfidence that is particularly problematic for partially visible line plots.

---

## 4. Evaluation Strategies for Line Plot Descriptions

### 4.1 MQM-Based Evaluation

The Multidimensional Quality Metrics (MQM) framework (Lommel et al., 2014; updated 2024), originally developed for translation quality evaluation, provides a systematic error annotation methodology applicable to chart descriptions. MQM uses a hierarchical error typology with seven top-level dimensions and associated severity levels (Critical, Major, Minor). For chart description evaluation, the MQM framework can be adapted to assess:

- **Accuracy errors:** Factual mistakes about chart content (values, trends, entities)
- **Fluency errors:** Grammatical or stylistic issues in the description
- **Completeness errors:** Missing required content elements
- **Terminology errors:** Incorrect use of chart or domain terminology

The 2024 Linear Calibrated Scoring Model (Lommel et al., 2024) provides a principled method for aggregating error annotations into quality scores, incorporating Statistical Quality Control tools for confidence interval calculation around quality scores. This is particularly relevant for line plot description evaluation where severity of errors varies dramatically -- misidentifying a trend direction is far more consequential than omitting a minor data point.

### 4.2 Trend Accuracy Evaluation

Evaluating whether a model correctly identified trends requires decomposing descriptions into directional claims and verifying each against ground truth. The approach used by ChartInsights (Wu et al., 2024) categorizes tasks including "Determine Range," "Find Extremum," "Retrieve Value," and "Find Correlations/Trends" -- each evaluated with task-specific metrics.

For trend descriptions specifically, evaluation can be binary (correct direction or not) or graded (accounting for partial correctness, e.g., correctly identifying an overall upward trend but missing a local dip). The Chain-of-Charts prompting strategy (Wu et al., 2024) improved trend identification accuracy by 14.41%, suggesting that evaluation should account for the prompting methodology used.

### 4.3 Value Accuracy with Tolerance Bands

ChartQA (Masry et al., 2022) introduced relaxed accuracy with a 5% tolerance for numerical answers. ChartQAPro extended this with differentiated tolerances: 5% error margin for numeric answers, exact match for years, and ANLS scores for textual responses. For line plot value descriptions, tolerance bands should account for the inherent imprecision of reading values from continuous curves without data labels.

### 4.4 Completeness Metrics

Completeness evaluation assesses whether the description covers all required content elements. Building on the VisText framework (Tang et al., 2023), completeness for line plots can be assessed at each semantic level:

- **L1 completeness:** Are all axes, lines, and legend entries mentioned?
- **L2 completeness:** Are key numerical values (extrema, start/end points) reported?
- **L3 completeness:** Are the major trends and patterns identified?

The ChaTS-Pi approach (Krichene et al., 2024) operationalized a form of completeness evaluation by scoring summaries sentence-by-sentence against the source chart, providing a granular assessment of what information is faithfully conveyed.

### 4.5 LLM-as-Judge Approaches

Using LLMs to evaluate chart descriptions has gained significant traction. Hsu et al. (2023) demonstrated that GPT-4 used as a zero-shot evaluator for scientific figure captions "outperformed all other models and even surpassed assessments made by computer science undergraduates," achieving a Kendall correlation of 0.401 with PhD student rankings on the SCICAP-EVAL benchmark.

Laskar et al. (2025) specifically evaluated LVLMs as judges for chart comprehension in their "Judging the Judges" study at ACL 2025, finding that "some open-source LVLMs (e.g., 7B models like LLaVA-Critic, Qwen2-VL, InternLM, and LLaVA-Next) can achieve judgment accuracy comparable to state-of-the-art closed-source models like GPT-4." However, they also documented persistent biases: positional preference (favoring options in certain positions) and length bias (preferring longer responses), both of which can distort evaluation of chart descriptions.

For line plot descriptions specifically, LLM-as-judge evaluation should decompose the assessment into:
1. Structural accuracy (are chart elements correctly identified?)
2. Trend accuracy (are trajectories correctly described?)
3. Numerical accuracy (are reported values within tolerance?)
4. Completeness (are all significant elements covered?)
5. Faithfulness (is every claim grounded in the chart?)

### 4.6 Reference-Free Evaluation

The ChaTS-Critic component of ChaTS-Pi (Krichene et al., 2024) introduced a reference-free evaluation approach that uses an image-to-text model to recover the data table from a chart, then applies tabular entailment to score descriptions sentence by sentence. This approach is particularly valuable for line plots because reference captions in datasets like Chart-to-Text (Kantharaj et al., 2022) are known to be noisy and sometimes hallucinated themselves.

---

## 5. Best Practices for Prompting VLMs on Line Plots

### 5.1 Structured Extraction Before Description

The Charts-of-Thought prompting technique (Mueller et al., 2025) demonstrated that guiding VLMs through systematic data extraction before answering questions significantly improves performance. Their approach, inspired by how humans interpret visualizations, follows a structured process:

1. Identify axes and their properties (labels, scales, ranges)
2. Extract data points or key values from each series
3. Verify extracted values against visual evidence
4. Perform analysis and generate the description

This approach improved performance by 21.8% for GPT-4.5, 9.4% for Gemini-2.0, and 13.5% for Claude-3.7 compared to standard prompting on the VLAT benchmark. For line plots specifically, the extraction step should enumerate each line series and its visual encoding before attempting trajectory description.

### 5.2 Chain-of-Charts for Low-Level Tasks

The Chain-of-Charts prompting strategy (Wu et al., 2024) tailored for chart QA tasks achieved 83.58% accuracy (a 14.41% improvement over baselines). This strategy decomposes chart reasoning into sequential steps:

1. Chart type recognition and structural parsing
2. Data extraction from relevant visual elements
3. Reasoning over extracted data
4. Answer generation with supporting evidence

Incorporating a visual prompt strategy that directs attention to relevant visual elements further improved accuracy to 84.32%.

### 5.3 Chart-to-Table as Intermediate Representation

The MatCha approach (Liu et al., 2023) and DePlot (Liu et al., 2023) demonstrated that converting charts to intermediate table representations before reasoning significantly improves downstream performance. For line plot descriptions, prompting the VLM to first extract a data table (x-values and corresponding y-values for each series) creates a structured intermediate representation that can then be used for more accurate trend description and value reporting.

The Chart Specification approach (2025) extends this by using structural intermediate representations that capture semantic intent and physical execution data, enabling more faithful chart-to-description generation.

### 5.4 Handling Multi-Series Plots in Prompts

For multi-series line plots, effective prompts should:

1. **Request legend enumeration first:** "List all series shown in the legend with their visual properties (color, line style, markers)."
2. **Request per-series description:** "For each series, describe its trajectory from left to right."
3. **Request comparative analysis:** "Describe how the series compare to each other. Where do they intersect? Which consistently leads?"
4. **Request structured output:** Using JSON or markdown table format for per-series information prevents the model from conflating series in free-text generation.

### 5.5 Structured Output for Trajectory Descriptions

Requesting structured output reduces entity confusion and improves completeness. An effective prompt template for line plot description:

```
Describe this line plot following this structure:
1. CHART OVERVIEW: Title, axes (labels, units, ranges, scale types)
2. SERIES INVENTORY: For each line series:
   - Legend label
   - Visual encoding (color, style, markers)
   - Starting value (leftmost point)
   - Ending value (rightmost point)
   - Overall trend (increasing/decreasing/stable/non-monotonic)
   - Notable features (peaks, troughs, inflection points)
3. COMPARATIVE ANALYSIS: Relationships between series
4. KEY OBSERVATIONS: Most important patterns and takeaways
```

### 5.6 Scale and Axis Awareness

Given the documented VLM failures with non-standard scales (Mahbub et al., 2025), prompts should explicitly request scale identification: "First identify whether the y-axis uses a linear or logarithmic scale, and whether the x-axis is continuous or categorical." This priming helps the model attend to scale indicators before interpreting trends.

### 5.7 Uncertainty Acknowledgment

Following the findings of Kim et al. (2025) on VLM overconfidence, prompts should encourage uncertainty expression: "If any values cannot be precisely read from the chart, indicate this with approximate ranges rather than stating specific numbers." This reduces value fabrication hallucinations.

---

## 6. References

1. Akhtar, M. S., et al. (2024). Unraveling the Truth: Do VLMs Really Understand Charts? A Deep Dive into Consistency and Robustness. In *Findings of the Association for Computational Linguistics: EMNLP 2024*. https://aclanthology.org/2024.findings-emnlp.973/

2. Bendeck, A., & Stasko, J. (2024). An Empirical Evaluation of the GPT-4 Multimodal Language Model on Visualization Literacy Tasks. *IEEE Transactions on Visualization and Computer Graphics*, 31(1), 1105--1115. (Proc. IEEE VIS 2024). https://ieeexplore.ieee.org/document/10670574/

3. Cheng, Z., et al. (2023). ChartReader: A Unified Framework for Chart Derendering and Comprehension without Heuristic Rules. In *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV 2023)*. https://openaccess.thecvf.com/content/ICCV2023/papers/Cheng_ChartReader_A_Unified_Framework_for_Chart_Derendering_and_Comprehension_without_ICCV_2023_paper.pdf

4. Choi, V., et al. (2024). Chart-based Reasoning: Transferring Capabilities from LLMs to VLMs. In *Findings of the Association for Computational Linguistics: NAACL 2024*. https://aclanthology.org/2024.findings-naacl.62/

5. Hsu, T.-Y., Huang, C.-Y., Rossi, R., Kim, S., Giles, C. L., & Huang, T.-H. K. (2023). GPT-4 as an Effective Zero-Shot Evaluator for Scientific Figure Captions. In *Findings of the Association for Computational Linguistics: EMNLP 2023*. https://aclanthology.org/2023.findings-emnlp.363/

6. Huang, K.-H., et al. (2024a). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. In *Findings of the Association for Computational Linguistics: ACL 2024*. https://aclanthology.org/2024.findings-acl.41/

7. Huang, K.-H., et al. (2024b). From Pixels to Insights: A Survey on Automatic Chart Understanding in the Era of Large Foundation Models. *IEEE Transactions on Knowledge and Data Engineering*. https://ieeexplore.ieee.org/document/10787102/

8. Islam, M. M., et al. (2024). Are Large Vision Language Models Up to the Challenge of Chart Comprehension and Reasoning? In *Findings of the Association for Computational Linguistics: EMNLP 2024*. https://aclanthology.org/2024.findings-emnlp.191/

9. Kantharaj, S., et al. (2022). Chart-to-Text: A Large-Scale Benchmark for Chart Summarization. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022)*. https://aclanthology.org/2022.acl-long.277/

10. Kim, J., et al. (2025). Losing the Plot: How VLM Responses Degrade on Imperfect Charts. *arXiv preprint arXiv:2509.18425*. https://arxiv.org/abs/2509.18425

11. Krichene, S., et al. (2024). Faithful Chart Summarization with ChaTS-Pi. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024)*. https://aclanthology.org/2024.acl-long.472/

12. Laskar, M. T. R., et al. (2025). Judging the Judges: Can Large Vision-Language Models Fairly Evaluate Chart Comprehension and Reasoning? In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*. https://aclanthology.org/2025.acl-industry.83/

13. Li, L., et al. (2025). ChartMuseum: Testing Visual Reasoning Capabilities of Large Vision-Language Models. In *Advances in Neural Information Processing Systems 38 (NeurIPS 2025)*. https://arxiv.org/abs/2505.13444

14. Li, S., & Tajbakhsh, N. (2023). SciGraphQA: A Large-Scale Synthetic Multi-Turn Question-Answering Dataset for Scientific Graphs. *arXiv preprint arXiv:2308.03349*. https://arxiv.org/abs/2308.03349

15. Liu, F., et al. (2023). MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023)*. https://aclanthology.org/2023.acl-long.714/

16. Lommel, A., et al. (2024). The Multi-Range Theory of Translation Quality Measurement: MQM Scoring Models and Statistical Quality Control. In *Proceedings of AMTA 2024*. https://aclanthology.org/2024.amta-presentations.6.pdf

17. Lundgard, A., & Satyanarayan, A. (2022). Accessible Visualization via Natural Language Descriptions: A Four-Level Model of Semantic Content. *IEEE Transactions on Visualization and Computer Graphics*, 28(1), 521--531. https://arxiv.org/abs/2110.04406

18. Mahbub, R., et al. (2025). The Perils of Chart Deception: How Misleading Visualizations Affect Vision-Language Models. In *Proceedings of IEEE VIS 2025*. https://arxiv.org/abs/2508.09716

19. Masry, A., et al. (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. In *Findings of the Association for Computational Linguistics: ACL 2022*. https://aclanthology.org/2022.findings-acl.177/

20. Masry, A., et al. (2023). UniChart: A Universal Vision-language Pretrained Model for Chart Comprehension and Reasoning. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)*. https://aclanthology.org/2023.emnlp-main.906/

21. Methani, N., et al. (2020). PlotQA: Reasoning over Scientific Plots. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2020)*. https://openaccess.thecvf.com/content_WACV_2020/papers/Methani_PlotQA_Reasoning_over_Scientific_Plots_WACV_2020_paper.pdf

22. Mueller, K., et al. (2025). Charts-of-Thought: Enhancing LLM Visualization Literacy Through Structured Data Extraction. *IEEE Transactions on Visualization and Computer Graphics*. https://arxiv.org/abs/2508.04842

23. P., S., et al. (2023). LineEX: Data Extraction from Scientific Line Charts. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2023)*. https://openaccess.thecvf.com/content/WACV2023/papers/P._LineEX_Data_Extraction_From_Scientific_Line_Charts_WACV_2023_paper.pdf

24. Pandey, A. V., et al. (2025). Benchmarking Visual Language Models on Standardized Visualization Literacy Tests. *Computer Graphics Forum* (Proc. EuroVis 2025). https://onlinelibrary.wiley.com/doi/10.1111/cgf.70137

25. Roberts, J., et al. (2024). SciFIBench: Benchmarking Large Multimodal Models for Scientific Figure Interpretation. In *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*. https://proceedings.neurips.cc/paper_files/paper/2024/file/217bb44ab14621754db8a392163e6b07-Paper-Datasets_and_Benchmarks_Track.pdf

26. Tang, B. J., et al. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023)*. (Outstanding Paper Award). https://aclanthology.org/2023.acl-long.401/

27. Tartaglini, A. R., et al. (2025). Diagnosing Bottlenecks in Data Visualization Understanding by Vision-Language Models. *arXiv preprint arXiv:2510.21740*. https://arxiv.org/abs/2510.21740

28. Wu, C., et al. (2024). ChartInsights: Evaluating Multimodal Large Language Models for Low-Level Chart Question Answering. In *Findings of the Association for Computational Linguistics: EMNLP 2024*. https://aclanthology.org/2024.findings-emnlp.710/

29. Xia, R., et al. (2025). Time-VLM: Exploring Multimodal Vision-Language Models for Augmented Time Series Forecasting. In *Proceedings of the International Conference on Machine Learning (ICML 2025)*. https://arxiv.org/abs/2502.04395

30. Zheng, M., et al. (2025). Chart Specification: Structural Representations for Incentivizing VLM Reasoning in Chart-to-Code Generation. *arXiv preprint arXiv:2602.10880*. https://arxiv.org/abs/2602.10880
