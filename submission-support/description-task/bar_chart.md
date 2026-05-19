# VLM Description Tasks for Bar Charts in Scientific Figures: A Comprehensive Research Survey

## 1. What Makes Bar Chart Description Challenging for VLMs

### 1.1 Fundamental Visual Perception Gaps

Vision-Language Models exhibit noticeable deficiencies in performing fundamental visual arithmetic tasks---accurately counting objects, comparing lengths, assessing angles, and evaluating relative sizes or areas---with these shortcomings being particularly evident in chart understanding tasks (Huang et al., 2024; Masry et al., 2025). Charts encode precise and structured information such as bar heights, line trajectories, and spatial dependencies, where even minor perceptual errors can cascade into significant descriptive inaccuracies.

The CharXiv benchmark (Wang et al., 2024a) demonstrated that even the strongest proprietary model (GPT-4o) achieves only 47.1% accuracy on reasoning questions about real scientific charts, while the strongest open-source model (InternVL Chat V1.5) achieves just 29.2%---both lagging far behind human performance of 80.5%. This gap is especially pronounced for bar charts requiring numerical comparison and value extraction.

### 1.2 Grouped and Stacked Bar Charts

Grouped bar charts require VLMs to simultaneously track multiple visual channels: bar position within a group, color-to-legend mapping, and relative heights across groups. Stacked bar charts add the challenge of segment boundary identification, where the model must decompose a single bar into its constituent parts and correctly attribute values to each segment. Current VLMs often confuse grouped bars with stacked bars or fail to correctly identify which color corresponds to which data series (Mukhopadhyay et al., 2024).

The ChartBench benchmark (Xu et al., 2024) specifically targets charts without data point annotations, requiring models to derive values by leveraging inherent chart elements such as color, legends, and coordinate systems. Across 42 subcategories of chart types, models consistently struggle with multi-series bar charts where visual disambiguation is required.

### 1.3 Error Bars and Small Value Differences

Error bars present a dual challenge: the model must (a) recognize that error bars exist as a distinct visual element and (b) correctly interpret their meaning (confidence intervals, standard deviations, standard errors). Many VLMs either ignore error bars entirely or misinterpret them as part of the bar itself. Small value differences between adjacent bars are particularly problematic because they require fine-grained pixel-level reasoning that exceeds the spatial resolution at which most VLMs operate (Kim et al., 2024).

### 1.4 OCR Challenges

Reading axis labels, tick marks, and data annotations from chart images remains a significant bottleneck. While VLMs have increasingly replaced traditional OCR pipelines for document understanding, chart-specific text poses unique challenges:

- **Rotated text**: Y-axis labels are typically rotated 90 degrees, and x-axis labels for bar charts with many categories are often rotated 45 or 90 degrees.
- **Small font sizes**: Tick mark labels and data annotations can be extremely small relative to the overall figure size.
- **Overlapping text**: Dense bar charts with many categories produce overlapping labels that confuse both OCR and VLM text recognition.
- **Scientific notation and special characters**: Axis labels in scientific figures often contain subscripts, superscripts, Greek letters, and mathematical notation.

Huang et al. (2024) found that GPT-4V often cannot understand charts without value labeling---i.e., cannot reliably align data points to axes when explicit numerical annotations are absent, necessitating the model to read and interpolate from axis scales.

### 1.5 Spatial Reasoning Challenges

Comparing bar heights requires implicit understanding of the coordinate system, including:

- **Scale reading**: Mapping pixel heights to numerical values using the y-axis scale, which may have non-uniform spacing (e.g., logarithmic scales).
- **Baseline alignment**: For horizontal bar charts, reading bar lengths from a common baseline.
- **Relative comparison**: Determining which of two bars with similar heights is taller, especially when they are not adjacent.
- **Logarithmic vs. linear scales**: VLMs frequently misinterpret logarithmic scales as linear, leading to order-of-magnitude errors in reported values (Wang et al., 2024a).

SpatialVLM (Chen et al., 2024) demonstrated that limited spatial reasoning in VLMs is not a fundamental architectural limitation but rather a training data limitation. However, chart-specific spatial reasoning (e.g., reading values from gridlines, interpolating between tick marks) remains undertrained in general-purpose VLMs.

### 1.6 Color Perception and Legend Mapping

An empirical evaluation of GPT-4's multimodal capabilities on visualization literacy tasks (Kim et al., 2024) revealed that the model "lacks the ability to reliably distinguish between colors in charts." This is a critical failure mode for bar charts where color is the primary encoding for distinguishing data series in grouped and stacked configurations. The VLAT/CALVI benchmark study (Pandey et al., 2025) found that all four tested VLMs (GPT-4o, Claude, Gemini, Llama) exhibited "consistent difficulties with data-dense visualizations involving multiple encodings" such as those found in complex grouped bar charts.

### 1.7 Robustness to Imperfect Charts

Real-world scientific figures are not pristine---they may have compression artifacts, low resolution, color printing artifacts, or unusual styling. The CHART NOISe dataset (Bendeck et al., 2025) systematically evaluated VLM robustness under chart corruption and occlusion, finding that ChatGPT-4o, Claude Sonnet, and Gemini 2.5 Pro all showed "sharp performance drops under corruption or occlusion, with hallucinations such as value fabrication, trend misinterpretation, and entity confusion becoming more frequent." Models remained overconfident in degraded settings, generating plausible but unsupported explanations.


## 2. What Should a Complete Bar Chart Description Contain

### 2.1 Survey of Benchmark Expectations

Different benchmarks define chart description completeness at varying levels of granularity:

**ChartQA** (Masry et al., 2022): Focuses on question answering rather than full descriptions, but its 9.6K human-written questions and 23.1K machine-generated questions reveal what humans consider important about charts: specific values, comparisons between categories, trends, extremes (maximum/minimum), and compositional reasoning (e.g., "What is the difference between X and Y?").

**PlotQA** (Methani et al., 2020): Contains 28.9 million question-answer pairs over 224,377 scientific plots. Its question templates (74 unique templates from 7,000 crowd-sourced questions) cover structural understanding (chart type, number of categories), data retrieval (specific values), and reasoning (comparisons, arithmetic operations). Notably, 80.76% of answers are not directly present in the plot, requiring inference.

**Chart-to-Text** (Kantharaj et al., 2022): A large-scale benchmark with 44,096 charts, introducing two task variants: (a) description with access to the underlying data table, and (b) description from the chart image alone. Expected descriptions include chart type identification, key trends, notable data points, and summary statistics.

**ChartSumm** (Rahman et al., 2023): Comprising 84,363 chart images with metadata and summaries, ChartSumm distinguishes between short summaries (1-2 sentences capturing the main takeaway) and long summaries (detailed paragraph covering all major aspects). This distinction highlights that description completeness is context-dependent.

**SciCap** (Hsu et al., 2021): Focused on scientific figure captioning, SciCap contains chart images paired with their original paper captions. These captions tend to be more interpretive, connecting chart content to scientific findings rather than purely describing visual elements.

**VisText** (Tang et al., 2023): Winner of the ACL 2023 Outstanding Paper Award, VisText provides 12,441 chart-caption pairs with a crucial three-level semantic framework:
- **Level 1 (L1)**: Elemental and encoded properties---chart type, axis labels, scales, color encodings.
- **Level 2 (L2)**: Statistical and relational properties---trends, extremes, comparisons, clusters.
- **Level 3 (L3)**: Perceptual and cognitive phenomena---insights, implications, patterns that require domain knowledge.

### 2.2 Content Elements for Complete Bar Chart Description

Based on the synthesis of benchmark expectations and accessibility guidelines (W3C WAI), a complete bar chart description should include:

1. **Chart type and orientation**: "Vertical bar chart" or "Horizontal grouped bar chart"
2. **Title and caption**: If present in the figure
3. **Axes**: What each axis represents, units, and scale type (linear/logarithmic)
4. **Categories**: All category labels on the categorical axis
5. **Data series**: For grouped/stacked bars, identification of all series with their legend labels and visual encodings (colors/patterns)
6. **Values**: Numerical values or ranges for each bar/segment
7. **Notable features**: Maximum, minimum, outliers, trends, groupings
8. **Annotations**: Error bars, significance markers, reference lines, data labels
9. **Visual properties**: Color scheme, sorting order, baseline

### 2.3 Precision Requirements

The appropriate level of numerical precision depends on context:

- **When data labels are present**: Exact values should be reported (e.g., "79.3%").
- **When reading from axes**: Approximate values with appropriate hedging (e.g., "approximately 80%") are acceptable and often preferable to false precision.
- **For comparisons**: Relative descriptions ("Bar A is roughly twice Bar B") may be more informative than absolute values when the exact numbers cannot be reliably determined.

ChartQA uses relaxed accuracy metrics that consider an answer correct if it is within 5% of the ground truth for numerical questions, acknowledging the inherent imprecision of reading values from chart images.

### 2.4 Grouped and Stacked Bar Handling

Benchmarks handle these differently:

- **Grouped bars**: Descriptions should explicitly state the grouping variable (x-axis categories), the series variable (legend), and enable comparison both within groups (across series) and across groups (across categories for the same series).
- **Stacked bars**: Descriptions should report both individual segment values (or proportions) and total bar heights. The order of stacking (bottom-to-top) and whether the chart uses absolute values or percentages should be noted.

ChartX (Xia et al., 2024) covers 18 chart types including both grouped and stacked variants, and their evaluation reveals that multi-series bar charts consistently receive lower accuracy scores than simple single-series bars.


## 3. Common VLM Errors on Bar Charts

### 3.1 Value Hallucination

The most pervasive error category. Huang et al. (2024) found that even for the most capable LVLMs, the non-factual rate in chart captions reaches 81.27%. Value hallucination manifests as:

- **Fabricated numbers**: The model generates plausible but incorrect numerical values, particularly when no data labels are present and values must be read from axes.
- **Precision inflation**: Reporting values like "73.4%" when the chart resolution only supports reading "approximately 70-75%."
- **Systematic bias**: Models tend to round to convenient numbers or anchor to values mentioned in nearby text.

The CHOCOLATE dataset (Huang et al., 2024) provides large-scale human annotations of factual errors in chart captions generated by various VLMs, establishing a taxonomy of error types and their frequencies.

### 3.2 Category Confusion

Models frequently swap labels between bars, particularly when:
- Many categories are present (>10 bars)
- Category labels are long or visually similar
- Bars are closely spaced
- The categorical axis uses rotated text

This error is especially problematic in grouped bar charts where the model must simultaneously track both the group label and the series label for each bar.

### 3.3 Grouping Errors

Misidentifying chart structure is a fundamental error:
- Describing a grouped bar chart as multiple separate bar charts
- Confusing grouped bars with stacked bars
- Failing to recognize that bars of different colors within a group represent different data series
- Incorrectly identifying the grouping variable

Mukhopadhyay et al. (2024) introduced RobustCQA specifically to test model consistency when the same data is rendered in different visual formats, finding "significant performance variations based on question and chart types."

### 3.4 Scale Misreading

- **Linear vs. logarithmic**: Treating a logarithmic scale as linear, leading to order-of-magnitude errors
- **Axis origin**: Assuming the y-axis starts at zero when it does not (truncated axis), which distorts comparative descriptions
- **Scale direction**: Pandey et al. (2025) found that VLMs perform poorly (8-18% accuracy) on detecting unconventional scale directions, compared to approximately 50% for humans

### 3.5 Color Description Errors

Kim et al. (2024) documented GPT-4's "tendency to misread color legends and inability to consistently interpret multiple colors in charts." This leads to:
- Swapping which data series is described as which color
- Using generic color terms ("blue") when the actual color is a specific shade that maps to a particular legend entry
- Failing to distinguish between visually similar colors (e.g., light blue vs. teal)

### 3.6 Missing Elements

Models frequently omit:
- Some bars in charts with many categories
- Error bars or confidence intervals
- Annotations and reference lines
- Secondary y-axes in dual-axis charts
- One or more series in grouped/stacked bars

### 3.7 Model-Specific Weaknesses

**GPT-4V / GPT-4o**: Strong on descriptive questions (84.5% on CharXiv descriptive tasks) but weak on reasoning (47.1%). Tends to misread color legends. Cannot reliably read values from axes without explicit data labels. Moderately robust to chart corruptions but often produces confident answers despite reduced accuracy (Bendeck et al., 2025). A study found that GPT-5 outperformed GPT-4o by 20-40 percentage points on chart reading, suggesting model capability matters more than prompting (Pandey et al., 2025b).

**Claude**: Achieved 67.9% on the VLAT visualization literacy assessment (Pandey et al., 2025), but dropped sharply under motion and defocus blur in chart images. Tends to be more cautious than GPT-4o in making numerical claims.

**Gemini**: Maintained the highest baseline accuracy (88%) in clean conditions in the CHART NOISe evaluation (Bendeck et al., 2025), but displayed heightened caution with 22.5% question omission versus 7-8% for other models (Pandey et al., 2025).

**LLaVA**: LLaVA-V1.6-13B achieved only 25.08% on open-ended chart tasks and 70.63% on multiple-choice in comprehensive benchmarks. Struggles significantly with numerical value extraction and multi-step reasoning over charts.

**InternVL**: InternVL2 demonstrates strong performance on ChartQA and related benchmarks, achieving state-of-the-art among open-source models. However, InternVL Chat V1.5 answered only 29.2% of CharXiv reasoning questions correctly, highlighting the gap between benchmark performance and real-world chart understanding.

**Llama**: Open-source Llama models generally underperform on chart understanding tasks compared to proprietary models, particularly on tasks requiring precise numerical extraction from bar charts.


## 4. Evaluation Strategies for Bar Chart Descriptions

### 4.1 MQM-Based Evaluation

The Multidimensional Quality Metrics (MQM) framework, originally developed for machine translation evaluation, provides a structured error taxonomy applicable to chart descriptions. Adapted for chart captioning, an MQM-style evaluation would annotate errors across dimensions including:

- **Accuracy**: Factual correctness of stated values, comparisons, and trends
- **Completeness**: Whether all chart elements are described
- **Fluency**: Grammatical and stylistic quality of the description
- **Terminology**: Correct use of chart-related vocabulary

MQM's primary limitation is its demand for expert annotation---an expensive, time-consuming resource (Kocmi et al., 2024). Genre-specific MQM variants have been proposed for specialized contexts (Li et al., 2024), and similar adaptations could be developed for chart description evaluation.

### 4.2 Checklist-Based Evaluation

ChartBench (Xu et al., 2024) uses a simplified binary evaluation (Acc+) where each question receives a yes/no judgment, reducing reliance on expensive LLM-based or manual evaluation. A more detailed checklist approach for bar chart descriptions would verify:

- [ ] Chart type correctly identified
- [ ] All axes correctly described (labels, units, scale)
- [ ] All categories/bars mentioned
- [ ] Values accurate within tolerance (e.g., +/- 5%)
- [ ] Grouping/stacking correctly identified
- [ ] Legend correctly mapped to visual elements
- [ ] Error bars noted if present
- [ ] Key trends/comparisons identified
- [ ] No hallucinated information

ChartInsights (Wu et al., 2024) evaluates 19 MLLMs across 10 data analysis tasks, finding an average accuracy of only 39.8%, with GPT-4o achieving the highest at 69.17%.

### 4.3 Reference-Based Metrics and Their Limitations

Traditional NLG metrics have well-documented shortcomings for chart description evaluation:

**BLEU** (Papineni et al., 2002): Measures n-gram overlap with reference descriptions. For chart descriptions, BLEU penalizes valid paraphrases (e.g., "the tallest bar" vs. "the maximum value") and fails to detect factual errors when the generated text has high lexical overlap but incorrect numbers.

**ROUGE**: Similar limitations to BLEU. Cannot distinguish between "Bar A is 80%" (correct) and "Bar A is 60%" (incorrect) if the rest of the description matches.

**BERTScore** (Zhang et al., 2020): Uses contextual embeddings and demonstrates superior correlation with human judgment in semantic tasks (59% vs. 47-50% for BLEU/ROUGE). However, it still cannot reliably detect numerical errors in chart descriptions, as the semantic embeddings treat different numbers as relatively similar.

**CIDEr**: Designed for image captioning, weighs informative n-grams higher. Better than BLEU/ROUGE for chart descriptions but still fundamentally limited by the reference-comparison paradigm.

Chart-to-Text (Kantharaj et al., 2022) and VisText (Tang et al., 2023) report these metrics but acknowledge their limitations, noting that high metric scores do not guarantee factual correctness.

### 4.4 LLM-as-Judge Approaches

Using a strong LLM (e.g., GPT-4o, Claude) to evaluate chart descriptions has become increasingly common. Research shows strong LLM judges achieve 80-90% agreement with human evaluators, comparable to inter-annotator agreement between humans. Key considerations:

- **Verbosity bias**: LLM judges tend to prefer more verbose descriptions, which may not reflect actual quality.
- **Position bias**: In pairwise comparisons, LLMs prefer the first response.
- **Reference requirement**: The judge needs either the original image, a data table, or a gold-standard description to assess factual accuracy.

CHARTVE (Huang et al., 2024) is a visual entailment model specifically designed for chart caption factuality evaluation, outperforming general-purpose LVLMs at this task. This represents a more targeted approach than using general LLM judges.

### 4.5 Human Evaluation Protocols

Gold-standard evaluation for chart descriptions typically involves:

1. **Expert annotators**: Domain experts who can verify numerical accuracy against the source data
2. **Error span annotation**: Marking specific text spans that contain errors, with severity ratings (critical/major/minor)
3. **Multi-annotator agreement**: Measuring inter-annotator reliability using Cohen's kappa or Krippendorff's alpha
4. **Stratified evaluation**: Separate assessment of different aspects (accuracy, completeness, fluency)

The CHOCOLATE dataset (Huang et al., 2024) employed large-scale human annotation to identify and categorize factual errors in chart captions, providing a template for rigorous human evaluation of chart descriptions.

### 4.6 Benchmark-Specific Evaluation

**ChartQA** (Masry et al., 2022): Relaxed accuracy allowing 5% numerical tolerance for extraction questions; exact match for categorical answers.

**Chart-to-Text** (Kantharaj et al., 2022): BLEU-4, METEOR, and human evaluation on informativeness, conciseness, and factual correctness.

**ChartInsights** (Wu et al., 2024): Task-specific accuracy across 10 data analysis tasks (value retrieval, comparison, trend identification, etc.).

**CharXiv** (Wang et al., 2024a): Separate evaluation of descriptive questions (basic chart elements) and reasoning questions (multi-step inference), with all questions handpicked and verified by human experts.

**CHARTOM** (Bendeck et al., 2024): Dual evaluation of factual comprehension (FACT) and assessment of misleading potential (MIND), calibrated against a Human Misleadingness Index derived from human study participants.


## 5. Best Practices for Prompting VLMs on Bar Charts

### 5.1 Structured Output Instructions

Prompting VLMs to produce structured descriptions significantly improves completeness and reduces omissions. Effective strategies include:

- **Template-based prompting**: Providing a structured template (chart type, axes, categories, values, trends) that the model fills in.
- **JSON output**: Requesting structured JSON output for value extraction tasks enables downstream verification.
- **Section-based descriptions**: Asking for descriptions organized by sections (Overview, Data, Comparisons, Insights) encourages systematic coverage.

For robust data extraction from charts, prompts must be specific, provide a clear output structure (like JSON), and include constraints to filter out noise.

### 5.2 Few-Shot vs. Zero-Shot

Research on prompting strategies for chart QA (Meng et al., 2024; Huang et al., 2024b) demonstrates that:

- **Few-Shot Chain-of-Thought** prompting consistently yields the highest accuracy (up to 78.2%), particularly on reasoning-intensive questions.
- Few-shot examples strongly influence VLM output style: "The captions in few-shot examples clearly influence the output by the VLM for new images, leading to more concise and shorter captions" (Subramanian, 2024).
- Carefully selecting few-shot examples that match the target chart type (e.g., using grouped bar chart examples for grouped bar chart tasks) improves performance more than using generic chart examples.

### 5.3 Chain-of-Thought for Chart Reading

The Chain-of-Charts strategy (Wu et al., 2024) orchestrates a sequence of sub-questions and answers that guide the model through systematic chart analysis, boosting performance by 14.41% and achieving 83.58% accuracy when combined with visual prompts.

Effective CoT for bar charts should decompose the task:
1. First identify the chart type and structure
2. Read and enumerate axis labels and scales
3. Identify all data series and their visual encodings
4. Extract values for each bar/segment
5. Identify trends and notable comparisons
6. Synthesize into a coherent description

### 5.4 Role Prompting Effects

Assigning the VLM a specific role (e.g., "You are a data visualization expert who describes charts precisely for scientific papers") can improve description quality by:
- Encouraging use of appropriate terminology
- Setting expectations for precision level
- Reducing tendency toward generic or vague descriptions

### 5.5 Visual Prompt Augmentation

ChartInsights (Wu et al., 2024) found that incorporating visual prompts---directing model attention to relevant visual elements through bounding boxes or highlights---further improved accuracy from 83.58% to 84.32%. This suggests that explicitly guiding the model's visual attention to specific bars or regions can reduce omission errors.

### 5.6 Chart Derendering as an Intermediate Step

DePlot (Liu et al., 2023a) demonstrated that translating a chart image to its underlying data table first, then using an LLM for reasoning and description, can dramatically improve accuracy. When combined with strong LLMs and self-consistency, DePlot+LLM achieved 29.4% improvement over prior state-of-the-art. This two-stage approach (image-to-table, table-to-description) may produce more accurate bar chart descriptions than direct image-to-text generation.

### 5.7 Multi-Level Description Generation

Following the VisText framework (Tang et al., 2023), prompting for descriptions at different semantic levels allows customization:
- **L1 prompt**: "Describe the chart structure: type, axes, categories, and visual encodings."
- **L2 prompt**: "Describe the data: values, trends, comparisons, and statistical properties."
- **L3 prompt**: "Interpret the chart: what insights, patterns, or implications does it convey?"

Generating descriptions at each level separately and combining them can produce more comprehensive outputs than a single monolithic prompt.


## 6. References

1. Bendeck, A., et al. (2025). Losing the Plot: How VLM Responses Degrade on Imperfect Charts. *arXiv preprint arXiv:2509.18425*.

2. Bendeck, A., et al. (2024). CHARTOM: A Visual Theory-of-Mind Benchmark for LLMs on Misleading Charts. *arXiv preprint arXiv:2408.14419*.

3. Chen, B., et al. (2024). SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2024)*.

4. Han, Y., et al. (2023). ChartLlama: A Multimodal LLM for Chart Understanding and Generation. *arXiv preprint arXiv:2311.16483*.

5. Hsu, T.-Y., et al. (2021). SciCap: Generating Captions for Scientific Figures. *Findings of the Association for Computational Linguistics: EMNLP 2021*.

6. Huang, K.-H., et al. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. *Findings of the Association for Computational Linguistics: ACL 2024*.

7. Huang, K.-H., Chan, H., Fung, Y., Qiu, H., Zhou, M., Joty, S., Chang, S.-F., & Ji, H. (2024). From Pixels to Insights: A Survey on Automatic Chart Understanding in the Era of Large Foundation Models. *IEEE Transactions on Knowledge and Data Engineering (TKDE 2024)*.

8. Kantharaj, S., Leong, R.T., et al. (2022). Chart-to-Text: A Large-Scale Benchmark for Chart Summarization. *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022)*.

9. Kim, D.H., et al. (2024). An Empirical Evaluation of the GPT-4 Multimodal Language Model on Visualization Literacy Tasks. *IEEE Transactions on Visualization and Computer Graphics (IEEE VIS 2024)*.

10. Lee, K., Joshi, M., et al. (2023). Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding. *Proceedings of the International Conference on Machine Learning (ICML 2023)*.

11. Li, A., et al. (2023). SciGraphQA: A Large-Scale Synthetic Multi-Turn Question-Answering Dataset for Scientific Graphs. *arXiv preprint arXiv:2308.03349*.

12. Liu, F., et al. (2023a). DePlot: One-Shot Visual Language Reasoning by Plot-to-Table Translation. *Findings of the Association for Computational Linguistics: ACL 2023*.

13. Liu, F., et al. (2023b). MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering. *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023)*.

14. Masry, A., Long, D.X., Tan, J.Q., Joty, S., & Hoque, E. (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. *Findings of the Association for Computational Linguistics: ACL 2022*.

15. Masry, A., et al. (2025). BigCharts-R1: Enhanced Chart Reasoning with Visual Reinforcement Finetuning. *Proceedings of the Conference on Language Modeling (COLM 2025)*.

16. Masry, A., et al. (2023). UniChart: A Universal Vision-Language Pretrained Model for Chart Comprehension and Reasoning. *Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)*.

17. Meng, F., et al. (2024). ChartAssistant: A Universal Chart Multimodal Language Model via Chart-to-Table Pre-training and Multitask Instruction Tuning. *arXiv preprint arXiv:2401.02384*.

18. Methani, N., Ganguly, P., Khapra, M.M., & Kumar, P. (2020). PlotQA: Reasoning over Scientific Plots. *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2020)*.

19. Mukhopadhyay, A., et al. (2024). Unraveling the Truth: Do VLMs Really Understand Charts? A Deep Dive into Consistency and Robustness. *Findings of the Association for Computational Linguistics: EMNLP 2024*.

20. Pandey, A.V., et al. (2025). Benchmarking Visual Language Models on Standardized Visualization Literacy Tests. *Computer Graphics Forum (Eurographics Conference on Visualization, EuroVis 2025)*.

21. Pandey, A.V., et al. (2025b). GPT-5 Model Corrected GPT-4V's Chart Reading Errors, Not Prompting. *arXiv preprint arXiv:2510.06782*.

22. Rahman, P., et al. (2023). ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization of Long and Short Summaries. *Proceedings of the Canadian Conference on Artificial Intelligence (Canadian AI 2023)*.

23. Tang, B.J., et al. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023)*. **Outstanding Paper Award**.

24. Wang, Z., et al. (2024a). CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs. *Advances in Neural Information Processing Systems (NeurIPS 2024), Datasets and Benchmarks Track*.

25. Wu, Y., et al. (2024). ChartInsights: Evaluating Multimodal Large Language Models for Low-Level Chart Question Answering. *Findings of the Association for Computational Linguistics: EMNLP 2024*.

26. Xia, R., et al. (2024). ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning. *arXiv preprint arXiv:2402.12185*.

27. Xu, Z., et al. (2024). ChartBench: A Benchmark for Complex Visual Reasoning in Charts. *Proceedings of the International Conference on Learning Representations (ICLR 2025)*.

28. Zhang, T., Kishore, V., Wu, F., Weinberger, K.Q., & Artzi, Y. (2020). BERTScore: Evaluating Text Generation with BERT. *Proceedings of the International Conference on Learning Representations (ICLR 2020)*.

29. Zhou, Y., et al. (2024). Representing Charts as Text for Language Models: An In-Depth Study of Question Answering for Bar Charts. *IEEE VIS 2024 Short Papers*.

30. Meng, X., et al. (2024). Do LLMs Work on Charts? Designing Few-Shot Prompts for Chart Question Answering and Summarization. *arXiv preprint arXiv:2312.10610*.

31. Chen, Z., et al. (2024). InternVL: Scaling Up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2024)*.

32. Liu, H., et al. (2024). LLaVA-NeXT: Improved Reasoning, OCR, and World Knowledge. *arXiv preprint*.

33. Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS 2022)*.

34. Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems (NeurIPS 2023)*.
