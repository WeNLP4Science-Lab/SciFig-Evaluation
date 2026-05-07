# State-of-the-Art: LLM Evaluation on Scientific Figure & Chart Understanding

> A comprehensive literature survey covering benchmarks, datasets, models, evaluation metrics, and emerging trends (2018–2026).

---

## Table of Contents

1. [Overview](#1-overview)
2. [Key Benchmark Papers](#2-key-benchmark-papers)
3. [Datasets](#3-datasets)
4. [Specialized Chart Models](#4-specialized-chart-models)
5. [General-Purpose MLLMs on Charts](#5-general-purpose-mllms-on-charts)
6. [Evaluation Metrics & Methodologies](#6-evaluation-metrics--methodologies)
7. [Novel Evaluation Approaches](#7-novel-evaluation-approaches)
8. [Error Analysis & Hallucination](#8-error-analysis--hallucination)
9. [Research Gaps](#9-research-gaps)
10. [Emerging Trends (2024–2026)](#10-emerging-trends-2024-2026)
11. [Key References](#11-key-references)
12. [Recent Papers (2025–2026)](#12-recent-papers-2025-2026)
13. [Detailed Paper Breakdown Table (2023–2026)](#13-detailed-paper-breakdown-table-2023-2026)

---

## 1. Overview

The evaluation of Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) on scientific figures — including bar charts, line plots, pie charts, scatter plots, heatmaps, and more — has become a rapidly growing research area. The field has evolved from simple synthetic QA benchmarks (2018) to complex real-world evaluation frameworks involving multi-step reasoning, structured error taxonomies, and multilingual assessment.

**Key insight**: Even frontier models like GPT-4o achieve only ~47% on reasoning questions over real scientific charts (CharXiv), revealing a substantial gap between current capabilities and human expert performance (~80%).

---

## 2. Key Benchmark Papers

### 2.1 FigureQA (2018)

- **Title**: FigureQA: An Annotated Figure Dataset for Visual Reasoning
- **Authors**: Kahou, Michalski, Atkinson, Kadar, Trischler, Bengio
- **Venue**: ICLR 2018 Workshop | **ArXiv**: 1710.07300
- **Contribution**: One of the earliest large-scale synthetic benchmarks for visual reasoning over figures.
- **Dataset**: ~100,000 figures, ~1.5M yes/no QA pairs. 5 chart types (line, dot-line, vertical/horizontal bar, pie). Fully synthetic.
- **Metrics**: Binary accuracy.
- **Key Finding**: Neural models at the time performed near random on many question types, exposing the difficulty of figure understanding.

### 2.2 DVQA (2018)

- **Title**: DVQA: Understanding Data Visualizations via Question Answering
- **Authors**: Kafle, Price, Cohen, Kanan
- **Venue**: CVPR 2018 | **ArXiv**: 1801.08163
- **Contribution**: Benchmark for bar chart understanding via QA with structural, data retrieval, and reasoning questions.
- **Dataset**: ~300,000 figures, ~3.4M QA pairs. Bar charts only (simple, grouped, stacked). Synthetic.
- **Metrics**: Accuracy by question type (structure, data, reasoning).
- **Key Finding**: Models showed strong structural understanding but weak data retrieval and reasoning.

### 2.3 PlotQA (2020)

- **Title**: PlotQA: Reasoning over Scientific Plots
- **Authors**: Methani, Ganguly, Khapra, Kumar
- **Venue**: WACV 2020 | **ArXiv**: 1909.00997
- **Contribution**: Large-scale benchmark with real-world data (World Bank) requiring numerical computation.
- **Dataset**: ~224,000 plots, 28.9M QA pairs. 3 types (line, bar, scatter). Semi-synthetic (real data, programmatic rendering).
- **Metrics**: Accuracy by difficulty level (structural, data retrieval, reasoning).
- **Key Finding**: Even strong VQA models achieved ~0–5% on reasoning questions vs. ~60–80% on structural ones.

### 2.4 ChartQA (2022)

- **Title**: ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning
- **Authors**: Masry, Long, Tan, Joty, Hoque
- **Venue**: ACL 2022 Findings | **ArXiv**: 2203.10244
- **Contribution**: The de facto standard benchmark combining human-written and machine-generated questions on real-world charts. Introduced the **Relaxed Accuracy** metric.
- **Dataset**: ~21,000 QA pairs over ~4,800 charts from Statista, Pew Research, OECD, Our World in Data. Two subsets: Human (~9,600 questions) and Augmented (~11,500 machine-generated).
- **Metrics**: Relaxed accuracy (5% tolerance for numerical answers), exact match.
- **Key Finding**: Significant gap between human-written (harder) and augmented (easier) subsets. Chart understanding requires both visual perception and logical reasoning.

### 2.5 CharXiv (2024)

- **Title**: CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs
- **Authors**: Wang, Xia, He, Chen, Liu, Zhu, Liang, Wu, Liu, Malladi, Chevalier, Arora, Chen
- **Venue**: NeurIPS 2024 Datasets & Benchmarks | **ArXiv**: 2406.18521
- **Contribution**: Rigorously curated benchmark using real charts from arXiv papers. Distinguishes descriptive vs. reasoning questions. Designed to be leak-resistant.
- **Dataset**: 2,323 charts from arXiv with ~9,600 questions. Descriptive (~1,000) and Reasoning (~1,300) splits. Expert-annotated with multi-round validation.
- **Metrics**: Accuracy (exact match + GPT-4 judge for open-ended answers), separate descriptive vs. reasoning scores.
- **Key Findings**:
  - GPT-4o: ~80% descriptive, ~47% reasoning
  - Human experts: ~80% on reasoning
  - Open-source models significantly trailed proprietary ones
  - Complex/multi-panel charts were especially difficult

### 2.6 ChartBench (2024)

- **Title**: ChartBench: A Benchmark for Complex Visual Reasoning in Charts
- **Authors**: Xu, Du, Qi, Xu, Yuan, Guo
- **Venue**: ACL 2024 Findings | **ArXiv**: 2312.15915
- **Contribution**: Introduced the **Acc+** metric addressing yes-bias in binary QA evaluation.
- **Dataset**: ~4,200 charts, ~16,800 QA pairs. 9 chart types. Two difficulty levels per question type.
- **Metrics**: Acc+ (balanced accuracy for yes/no bias), standard accuracy, breakdown by chart/question type.
- **Key Finding**: Many MLLMs exhibit strong "yes-bias" — Acc+ revealed actual performance was much lower than standard accuracy suggested.

### 2.7 ChartX (2024)

- **Title**: ChartX & ChartVLM: A Versatile Benchmark and Foundation Model for Complicated Chart Reasoning
- **Authors**: Xia, Zhang, Ye, Yan, Liu, Zhou, Chen, Dou, Shi, Yan, Qiao
- **Venue**: NeurIPS 2024 Datasets & Benchmarks | **ArXiv**: 2402.12185
- **Contribution**: Most comprehensive multi-task benchmark with **18 chart types** and **7 evaluation tasks**.
- **Dataset**: ~6,000 charts with multi-task annotations. Tasks: chart type classification, data table extraction, title extraction, description generation, QA, chart-to-code, chart redrawing.
- **Metrics**: Task-specific (accuracy, BLEU/ROUGE, structural similarity, GPT-based evaluation).
- **Key Finding**: GPT-4V struggled on complex chart types and data extraction. Performance varied dramatically across chart types.

### 2.8 MMC-Benchmark (2023/2024)

- **Title**: MMC: Advancing Multimodal Chart Understanding with Large-scale Instruction Tuning
- **Authors**: Liu, Wang, Yao, Chen, Song, Cho, Yacoob, Yu
- **Venue**: NAACL 2024 | **ArXiv**: 2311.10774
- **Contribution**: Large-scale instruction-tuning dataset + systematic evaluation benchmark.
- **Dataset**: ~600,000 chart-instruction pairs (training). MMC-Benchmark: ~2,400 charts with multi-choice and free-form questions (evaluation).
- **Metrics**: Accuracy (multiple-choice), GPT-4 scoring (open-ended).
- **Key Finding**: Even GPT-4V achieved only ~58% on multiple choice. Open-source models significantly underperformed proprietary ones.

### 2.9 ChartInsights (2024)

- **Title**: ChartInsights: Evaluating Multimodal Large Language Models for Low-Level Chart Question Answering
- **Authors**: Wu, Yan, Shen, Wang, Tang
- **Venue**: EMNLP 2024 Findings
- **Contribution**: Targets low-level chart understanding tasks (reading precise values rather than high-level reasoning).
- **Dataset**: ~8,900 charts, ~48,000 QA pairs. 10 chart types. 10 low-level analysis tasks (retrieve value, find extremum, determine range, characterize distribution, find anomalies, cluster, correlate, sort, filter, compute derived values).
- **Metrics**: Accuracy with numerical tolerance, breakdown by task/chart type.
- **Key Finding**: Models performed well on simple retrieval but poorly on precise numerical reading. Performance degraded with chart complexity.

### 2.10 ChartMimic (2024)

- **Title**: ChartMimic: Evaluating LMM's Cross-Modal Generation from Charts
- **Authors**: Shi, Yang, Liu, Shui, Wang, et al.
- **Venue**: NeurIPS 2024 | **ArXiv**: 2406.09961
- **Contribution**: Evaluates MLLMs' ability to generate code reproducing charts (chart-to-code).
- **Dataset**: 1,000 charts from scientific papers + matplotlib gallery. 18 types of matplotlib figures. Ground-truth Python/matplotlib code provided.
- **Metrics**: Code executability, visual similarity (pixel-level), chart element accuracy (type, layout, color, labels, data values).
- **Key Finding**: GPT-4V was the best performer but still struggled with complex multi-panel figures and precise data reproduction.

### 2.11 Additional Notable Benchmarks

| Benchmark | Year | Key Focus |
|-----------|------|-----------|
| **OpenCQA** | 2022 | Open-ended chart QA with free-form text answers (~7,700 QA pairs) |
| **Chart-to-Text** | 2022 | Chart summarization (~44,000 chart-summary pairs) |
| **SciGraphQA** | 2023 | Multi-turn QA over scientific figures from arXiv (~295,000 QA pairs) |
| **MathVista** | 2023 | Math-visual reasoning including chart subset (ICLR 2024) |
| **MMStar** | 2024 | Meta-benchmark including chart understanding with anti-leakage design |

---

## 3. Datasets

### Comprehensive Dataset Comparison

| Dataset | Year | Size (Images / QA) | Creation | Chart Types | Tasks | Reasoning? | Real/Synthetic |
|---------|------|---------------------|----------|-------------|-------|------------|----------------|
| FigureQA | 2018 | 100K / 1.5M | Synthetic | 5 | Binary QA | Limited | Synthetic |
| DVQA | 2018 | 300K / 3.4M | Synthetic | Bar only | Multi-type QA | Yes | Synthetic |
| PlotQA | 2020 | 224K / 28.9M | Semi-synthetic | 3 | Multi-type QA | Yes (arithmetic) | Semi-synthetic |
| ChartQA | 2022 | 4.8K / 21K | Human + Machine | Diverse real | Open QA | Yes | Mixed |
| OpenCQA | 2022 | 900 / 7.7K | Human annotated | Real-world | Open-ended QA | Yes | Real |
| Chart-to-Text | 2022 | 44K / 44K | Web-scraped | Diverse real | Summarization | Implicit | Real |
| SciGraphQA | 2023 | ~295K / 295K | LLM-generated on real | Scientific | Multi-turn QA | Yes | Real |
| MMC-Bench | 2023 | 2.4K eval / 600K train | Web + GPT-4 | Diverse | Multi-task | Yes | Mixed |
| StructChart | 2023 | 7K eval / 500K train | Synthetic + real | 7+ types | Table extraction + QA | Yes | Mixed |
| ChartBench | 2023 | 4.2K / 16.8K | Synthetic + curated | 9 types | Multi-level QA | Yes | Mixed |
| ChartX | 2024 | 6K / multi-task | Human-curated | **18 types** | 7 tasks | Yes | Mixed |
| CharXiv | 2024 | 2.3K / 9.6K | Expert-annotated | Scientific | Descriptive + Reasoning | **Yes (expert)** | Real |
| ChartLlama data | 2023 | 11K / 160K | GPT-4 generated | 7+ types | QA + Code gen | Yes | Synthetic |
| ChartAssistant data | 2024 | 4.2M / 1M instruct | Synthetic | 10+ types | Multi-task | Yes | Synthetic |
| UniChart data | 2023 | compiled / 611K | Compiled | Diverse | Multi-task | Yes | Mixed |

### Key Observations on Datasets

1. **Evolution from synthetic to real**: Early datasets (FigureQA, DVQA) were fully synthetic. Modern benchmarks (CharXiv, ChartQA-Human) use real scientific figures.
2. **The synthetic-real gap**: Models trained on synthetic benchmarks show 15–30% lower performance on real scientific charts.
3. **Scale vs. quality tradeoff**: PlotQA has 28.9M QA pairs but synthetic rendering; CharXiv has only 2.3K charts but expert annotations.
4. **Real scientific figures** present unique challenges: multi-panel layouts, LaTeX-rendered text, compression artifacts, domain-specific conventions, non-English text.

---

## 4. Specialized Chart Models

### 4.1 MatCha (2023)

- **Architecture**: Pix2Struct (image-to-text Transformer), ~282M params
- **Training**: (1) Math reasoning pre-training on MATH/DROP; (2) Chart derendering pre-training (recover tables from charts)
- **Novel**: First to incorporate mathematical reasoning pre-training for charts
- **Performance**: ChartQA ~51% avg. Significantly outperformed prior specialized models at release.
- **ArXiv**: 2212.09662 | **Venue**: ACL 2023

### 4.2 DePlot (2023)

- **Architecture**: Two-stage pipeline — Pix2Struct chart-to-table model + LLM reasoner (PaLM-2/Codex)
- **Training**: DePlot trained on chart-table pairs; LLM used frozen at inference
- **Novel**: Decouples visual perception from reasoning. Enables one-shot/few-shot chart QA with any LLM.
- **Performance**: ChartQA ~54% avg with PaLM-2
- **ArXiv**: 2212.10505 | **Venue**: ACL 2023 Findings

### 4.3 UniChart (2023)

- **Architecture**: Donut (Swin Transformer encoder + BART decoder), ~270M params
- **Training**: Three-stage: chart-specific pre-training, multi-task learning (ChartQA + PlotQA + Chart-to-Text + OpenCQA), fine-tuning
- **Novel**: First unified model jointly trained on multiple chart understanding tasks
- **Performance**: ChartQA Human 43.9%, Aug 88.6%. SOTA at release.
- **ArXiv**: 2305.14761 | **Venue**: EMNLP 2023

### 4.4 ChartLlama (2023)

- **Architecture**: LLaVA (CLIP ViT-L/14 + LLaMA-2 13B)
- **Training**: Instruction tuning on ~160K samples including chart understanding + generation tasks
- **Novel**: First to combine chart understanding with chart code generation (matplotlib)
- **Performance**: Competitive with GPT-4V on several chart tasks
- **ArXiv**: 2311.16483

### 4.5 TinyChart (2024)

- **Architecture**: SigLIP vision encoder + Phi-2 (2.7B), ~3B params total
- **Training**: Visual Token Merging + Program-of-Thoughts (PoT) learning — generates executable Python for numerical reasoning
- **Novel**: Achieves strong performance with only 3B parameters. PoT eliminates numerical reasoning errors via code execution.
- **Performance**: **ChartQA ~83.6% overall** — rivaling GPT-4V with 3B params
- **ArXiv**: 2404.16635

### 4.6 ChartInstruct (2024)

- **Architecture**: Two versions — UniChart-based (270M) and LLaVA-based (13B)
- **Training**: Instruction tuning on ~191K chart-specific instruction samples generated via GPT-4
- **Novel**: Systematic instruction tuning specifically for charts
- **Performance**: SOTA among open-source models at release
- **ArXiv**: 2403.09028

### 4.7 ChartAssistant (2024)

- **Architecture**: LLaVA-1.5 (CLIP ViT-L + Vicuna-7B/13B)
- **Training**: Two-stage: (1) Chart-to-table pre-training on 4.2M pairs; (2) Multi-task instruction tuning on 1M samples
- **Novel**: Largest-scale chart pre-training. Chart-to-table alignment as a foundation.
- **Performance**: Competitive with GPT-4V. Excels on data extraction.
- **ArXiv**: 2401.02384 | **Venue**: ACL 2024 Findings

### 4.8 StructChart (2024)

- **Architecture**: Three-stage pipeline: Perception → Structuring → Reasoning
- **Training**: ~500K synthetic chart-table pairs. Each stage uses different model backbones.
- **Novel**: Explicit perceive-structure-reason decomposition mirroring human chart interpretation.
- **ArXiv**: 2309.11268

### Model Comparison Table

| Model | Year | Params | Key Innovation | ChartQA Avg |
|-------|------|--------|----------------|-------------|
| MatCha | 2023 | ~282M | Math pre-training + derendering | ~51% |
| DePlot | 2023 | ~282M + LLM | Chart-to-table + LLM reasoning | ~54% |
| UniChart | 2023 | ~270M | Unified multi-task pre-training | ~66% |
| ChartLlama | 2023 | ~13B | Understanding + generation | ~GPT-4V level |
| ChartInstruct | 2024 | 270M–13B | Systematic instruction tuning | ~65–68% |
| ChartAssistant | 2024 | 7B/13B | 4.2M chart-table pre-training | ~70–72% |
| **TinyChart** | 2024 | **~3B** | Token merging + PoT | **~83.6%** |
| StructChart | 2024 | Variable | 3-stage perceive-structure-reason | Competitive |

---

## 5. General-Purpose MLLMs on Charts

### Performance Comparison (Approximate Across Multiple Benchmarks)

| Model | ChartQA (Human) | ChartQA (Aug) | CharXiv Descriptive | CharXiv Reasoning |
|-------|-----------------|---------------|---------------------|-------------------|
| **GPT-4o** | ~73–78% | ~90–93% | ~80% | ~48% |
| **GPT-4V** | ~67–70% | ~85–88% | ~72% | ~42% |
| **Gemini 1.5 Pro** | ~70–75% | ~88–90% | ~75% | ~45% |
| **Claude 3.5 Sonnet** | ~68–72% | ~86–89% | ~70% | ~40% |
| **InternVL2** | ~65–70% | ~83–86% | ~60% | ~35% |
| **LLaVA-NeXT** | ~55–60% | ~75–80% | ~50% | ~28% |
| **Qwen-VL-Plus** | ~60–65% | ~80–83% | ~55% | ~30% |

*Numbers are approximate ranges synthesized from multiple benchmark papers.*

### Specialized vs. General-Purpose: Key Findings

| Dimension | Specialized Models | General-Purpose MLLMs |
|-----------|-------------------|----------------------|
| **Numerical extraction** | Better (precise values) | Tend to hallucinate values |
| **Novel reasoning** | Weaker (distribution-dependent) | Stronger (broader training) |
| **Unusual chart types** | Fail on unseen types | Better generalization |
| **Open-ended analysis** | Limited | Superior |
| **Cost/speed** | Orders of magnitude cheaper | Expensive API calls |
| **Structured output** | Better (tables, data) | Less reliable |

---

## 6. Evaluation Metrics & Methodologies

### 6.1 Standard Metrics

| Metric | Used By | Description |
|--------|---------|-------------|
| **Exact Match Accuracy** | FigureQA, DVQA, ChartBench | Strict string/value matching |
| **Relaxed Accuracy (5%)** | ChartQA, PlotQA | Numerical answers within 5% tolerance |
| **Acc+** | ChartBench | Balanced accuracy addressing yes-bias |
| **BLEU (1–4)** | Chart-to-Text, ChartX, UniChart | N-gram overlap for text generation |
| **ROUGE (1, 2, L)** | Chart-to-Text, ChartX | Recall-oriented text evaluation |
| **BERTScore (F1)** | Multiple | Contextual embedding similarity |
| **SBERT Cosine Similarity** | Inter-annotator agreement | Sentence-level semantic similarity |
| **F1 Score** | ChartQA, UniChart | Token-level overlap |
| **RNSS** | DePlot, Chart-to-Table | Relative Number Set Similarity for data extraction |
| **RMS** | Chart-to-Table | Relative Mapping Similarity for key-value pairs |
| **GPT-4 Judge** | CharXiv, MMC, ChartX | LLM-as-judge for open-ended answers |
| **Human Evaluation** | CharXiv, Chart-to-Text | Expert Likert-scale or pairwise comparison |

### 6.2 Evaluation Tasks Across Benchmarks

| Task | Benchmarks |
|------|-----------|
| **Question Answering (QA)** | ChartQA, FigureQA, DVQA, PlotQA, CharXiv, ChartBench, ChartInsights, MMC |
| **Chart Summarization** | Chart-to-Text, ChartSumm, ChartX, UniChart |
| **Data Table Extraction** | ChartX, DePlot, StructChart, ChartAssistant, UniChart |
| **Chart Type Classification** | ChartX, ChartBench, MMC |
| **Code Generation (Chart-to-Code)** | ChartMimic, ChartX, ChartLlama |
| **Numerical Reasoning** | PlotQA, ChartQA, CharXiv, MathVista |
| **Trend/Pattern Analysis** | ChartBench, MMC, ChartInsights |
| **Figure Description** | FigureSense, SciGraphQA, Chart-to-Text |

### 6.3 Annotation Methodologies

| Method | Benchmarks | Pros | Cons |
|--------|-----------|------|------|
| **Fully Synthetic** | FigureQA, DVQA, PlotQA | Large scale, controlled | Limited visual diversity |
| **Real Charts + Human QA** | ChartQA (human), CharXiv | Realistic, high quality | Expensive, smaller scale |
| **Real Charts + Machine QA** | ChartQA (aug), MMC | Scalable | Potential quality issues |
| **Real Charts + Expert Annotation** | CharXiv, FigureSense | Highest quality | Very expensive |
| **Mixed Sources** | ChartX, ChartBench | Diverse | Consistency challenges |

---

## 7. Novel Evaluation Approaches

### 7.1 MQM-Style Quality Scoring (FigureSense Framework)

Adapted from the Multidimensional Quality Metrics (MQM) framework used in machine translation evaluation. Key components:

**Error Taxonomy (8 categories):**
1. **Hallucination** — Model describes something not present in the figure
2. **Omission** — Model fails to mention a detail from the gold annotation
3. **Misinterpretation** — Model describes a figure element incorrectly
4. **Inaccuracy** — Numerically or factually incorrect value
5. **Label Misalignment** — Incorrect label, legend reference, or variable name
6. **Overgeneralization** — Broader/stronger claim than supported
7. **Ambiguity** — Vague, underspecified language
8. **Stylistic/Fluency** — Awkward, ungrammatical, or redundant language

**Severity Levels:**
- **Critical** (weight=25): >20% error on linear scales, >0.3 log10 difference on log scales, axis scale type errors
- **Moderate** (weight=5): 5–20% error on linear scales, 0.1–0.3 log10 difference
- **Minor** (weight=1): <5% error on linear scales, <0.1 log10 difference

**Per-Figure TQ Score:**
```
TQ = 100 - sum(severity_weight × error_count / word_count)
```
Clamped to [0, 100]. Word count normalization accounts for annotation length differences.

**Component-Level Controlled Vocabulary:** Errors tagged to specific figure components (x_axis_label, y_axis_label, line_trend, bar_height, pie_slice_label, legend_position, chart_title, general_trend, etc. — 30+ components).

### 7.2 Automated Error Detection Pipeline

1. Model-generated annotation + human gold annotation compared by GPT-4o
2. Structured JSON output: error type, severity, component, target, model_said, human_said, span
3. Human validators review automated detections in Label Studio
4. Meta-evaluation: detection precision measured against human judgments

### 7.3 Reproducibility Testing for LLM-as-Judge

Multiple runs of error detection compared via:
- **Jaccard Similarity** between error type sets
- **Weighted Jaccard Similarity** using error count frequencies
- **L1 Distance** between error count vectors
- **Cosine Similarity** between error count vectors

### 7.4 ChartBench Acc+ Metric

Addresses the tendency of MLLMs to answer "Yes" to binary chart questions. Requires correct answers on both positive and negative versions of the same question:
```
Acc+ = (Accuracy_yes + Accuracy_no) / 2
```

### 7.5 Chart-to-Code Verification (ChartMimic)

Tests understanding by asking models to generate code that reproduces charts. Low-level metrics (executability, pixel similarity) and high-level metrics (element accuracy) combined.

---

## 8. Error Analysis & Hallucination

### 8.1 Common Error Patterns Across Studies

| Error Category | Frequency | Chart Types Most Affected |
|----------------|-----------|---------------------------|
| Numerical value misreading | Very High | Bar charts, line charts |
| Trend misinterpretation | High | Line charts, multi-series plots |
| Color/legend confusion | High | Multi-series, stacked charts |
| Scale type hallucination | Medium | Logarithmic plots, non-uniform axes |
| Data point fabrication | Medium | Scatter plots, dense line charts |
| Spatial relationship errors | Medium | Grouped bar charts, subplots |
| Statistical claim fabrication | Low–Medium | All types |
| Omission of complex elements | High | Error bars, confidence intervals, annotations |

### 8.2 Key Error Analysis Papers

- **ChartQA** (Masry et al., 2022): Visual grounding errors, numerical reasoning errors, compositional reasoning failures
- **ChartBench** (Xu et al., 2023): Identified "yes" bias. Categorized errors by chart type and question complexity.
- **"Do LVLMs Understand Charts?"** (Huang et al., 2024, arXiv:2312.10160): Analyzed perceptual errors, reasoning errors, knowledge errors. Found GPT-4V struggles with precise numerical extraction.
- **TinyChart** (Zhang et al., 2024): Low resolution → visual perception errors; High resolution → reasoning errors.
- **HallusionBench** (Guan et al., 2024, arXiv:2310.14566): Visual illusion vs. knowledge hallucination failures (includes chart examples).

### 8.3 Complexity-Performance Relationship

| Complexity Factor | Performance Impact | Evidence |
|-------------------|-------------------|----------|
| Number of data series | High negative | Strong (multiple studies) |
| Logarithmic/non-linear scales | High negative | Strong |
| Small text/dense labels | High negative | Strong |
| Number of subplots | Medium negative | Moderate |
| Overlapping elements | Medium negative | Moderate |
| Color-only encoding | Medium negative | Moderate |
| Error bars/confidence intervals | High negative (often ignored) | Moderate |
| Mathematical notation | Medium negative | Moderate |
| 3D effects/distortion | High negative | Limited |

---

## 9. Research Gaps

### 9.1 Critical Gaps

1. **Multi-panel figure reasoning**: Nearly zero benchmarks properly evaluate understanding of multi-panel scientific figures with cross-panel reasoning.
2. **Multilingual chart understanding**: Almost no benchmarks test chart understanding in non-English contexts despite global scientific publishing.
3. **Fine-grained standardized error taxonomy**: Most papers use coarse error categories. A community-adopted taxonomy (like MQM for translation) is needed.
4. **Confidence calibration**: Models never express "I'm not sure about this value." Calibrated uncertainty for chart-extracted data is unexplored.
5. **Long-form chart description evaluation**: Most benchmarks use short-answer QA. Evaluating paragraph-length descriptions remains methodologically challenging.
6. **Chart complexity as controlled variable**: No benchmark systematically varies complexity to study its isolated effect on performance.

### 9.2 Underexplored Areas

7. **Cross-paper figure reasoning**: Comparing figures across different papers
8. **Figure quality assessment**: Detecting misleading or poorly designed scientific visualizations
9. **Accessibility**: Generating detailed alt-text for scientific figures for visually impaired researchers
10. **Dynamic/interactive charts**: No evaluation for animated or interactive visualizations
11. **OCR integration quality**: Handling unusual fonts, rotated labels, mathematical notation
12. **Adversarial chart evaluation**: Testing with intentionally misleading charts (truncated y-axes, dual scales, cherry-picked ranges)

### 9.3 From Survey Papers

**"From Pixels to Insights" (Masry et al., 2024, arXiv:2403.12027)** — the most comprehensive survey — identified:
- Most benchmarks focus on simple bar/line/pie; scientific papers use complex visualizations
- No standard benchmark for multi-chart reasoning
- No evaluation of domain-specific chart understanding (medical, financial)
- Lack of robustness/adversarial testing

---

## 10. Emerging Trends (2024–2026)

### 10.1 Chain-of-Thought for Charts

Structured CoT for chart understanding:
1. Identify chart type → 2. Extract axis labels/ranges → 3. Enumerate data series → 4. Read values → 5. Reason over data

**Results**: CoT improves reasoning by 5–15% but can introduce more hallucinations in extraction steps.

### 10.2 Program-of-Thoughts (PoT)

Instead of natural language reasoning, models generate executable Python code. Code execution produces final numerical answers, eliminating arithmetic errors. Pioneered by TinyChart.

### 10.3 Tool-Augmented / Agentic Chart Understanding

Multi-agent systems with:
- OCR agent for text extraction
- Visual grounding agent for element identification
- Data extraction agent for table conversion
- Reasoning agent for analysis

Show 10–20% improvements over end-to-end approaches.

### 10.4 Chart-Specific Prompting Strategies

- **Structured prompting**: First describe structural elements, then answer questions
- **Visual scaffolding**: Building understanding in layers
- **Grounding prompts**: Cite specific visual evidence for each claim (reduces hallucination ~10–15%)

### 10.5 Chart-to-Table as Foundation

Multiple papers show learning to extract structured data tables from charts is a powerful pre-training objective (DePlot, StructChart, ChartAssistant, UniChart).

### 10.6 Efficient Specialized Models

TinyChart (3B) proved small, well-trained models can match GPT-4V on specific tasks — making deployment practical at scale.

### 10.7 General MLLMs Closing the Gap

Each generation (GPT-4V → GPT-4o, Gemini 1.0 → 1.5 → 2.0) shows dramatic chart understanding improvements without chart-specific training. The question: will specialized models remain necessary?

### 10.8 Emerging Applications

- **Chart-grounded claim verification**: Can models verify whether paper text claims match figures?
- **Automated figure quality assessment**: Flagging misleading/poorly designed charts
- **Cross-modal consistency checking**: Verifying consistency between text, tables, and figures
- **Figure accessibility generation**: Automatic detailed alt-text for scientific figures

---

## 11. Key References

### Benchmarks

1. Kahou et al. (2018). "FigureQA: An Annotated Figure Dataset for Visual Reasoning." ICLR Workshop. arXiv:1710.07300
2. Kafle et al. (2018). "DVQA: Understanding Data Visualizations via Question Answering." CVPR. arXiv:1801.08163
3. Methani et al. (2020). "PlotQA: Reasoning over Scientific Plots." WACV. arXiv:1909.00997
4. Masry et al. (2022). "ChartQA: A Benchmark for Question Answering about Charts." ACL Findings. arXiv:2203.10244
5. Kantharaj et al. (2022). "Chart-to-Text: A Large-Scale Benchmark for Chart Summarization." ACL. arXiv:2203.06486
6. Kantharaj et al. (2022). "OpenCQA: Open-ended Question Answering with Charts." EMNLP. arXiv:2210.06628
7. Li et al. (2023). "SciGraphQA: A Large-Scale Synthetic Multi-Turn QA Dataset for Scientific Graphs." arXiv:2308.03349
8. Liu et al. (2023). "MMC: Advancing Multimodal Chart Understanding with Large-scale Instruction Tuning." NAACL 2024. arXiv:2311.10774
9. Xu et al. (2023). "ChartBench: A Benchmark for Complex Visual Reasoning in Charts." ACL 2024 Findings. arXiv:2312.15915
10. Xia et al. (2024). "ChartX & ChartVLM: A Versatile Benchmark and Foundation Model." NeurIPS 2024. arXiv:2402.12185
11. Wang et al. (2024). "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs." NeurIPS 2024. arXiv:2406.18521
12. Shi et al. (2024). "ChartMimic: Evaluating LMM's Cross-Modal Generation from Charts." NeurIPS 2024. arXiv:2406.09961
13. Wu et al. (2024). "ChartInsights: Evaluating MLLMs for Low-Level Chart Question Answering." EMNLP 2024 Findings.
14. Lu et al. (2023). "MathVista: Evaluating Mathematical Reasoning in Visual Contexts." ICLR 2024. arXiv:2310.02255
15. Xia et al. (2023). "StructChart: Perception, Structuring, Reasoning for Visual Chart Understanding." arXiv:2309.11268

### Models

16. Liu et al. (2023). "MatCha: Enhancing Visual Language Pretraining with Math Reasoning and Chart Derendering." ACL. arXiv:2212.09662
17. Liu et al. (2023). "DePlot: One-shot Visual Language Reasoning by Plot-to-Table Translation." ACL Findings. arXiv:2212.10505
18. Masry et al. (2023). "UniChart: A Universal Vision-Language Pretrained Model for Chart Comprehension." EMNLP. arXiv:2305.14761
19. Han et al. (2023). "ChartLlama: A Multimodal LLM for Chart Understanding and Generation." arXiv:2311.16483
20. Zhang et al. (2024). "TinyChart: Efficient Chart Understanding with Visual Token Merging and PoT Learning." arXiv:2404.16635
21. Masry et al. (2024). "ChartInstruct: Instruction Tuning for Chart Comprehension and Reasoning." arXiv:2403.09028
22. Meng et al. (2024). "ChartAssistant: A Universal Chart Multimodal Language Model." ACL 2024 Findings. arXiv:2401.02384

### Surveys & Error Analysis

23. Masry et al. (2024). "From Pixels to Insights: A Survey on Automatic Chart Understanding." arXiv:2403.12027
24. Huang et al. (2024). "Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning." arXiv:2312.10160
25. Guan et al. (2024). "HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion." CVPR. arXiv:2310.14566

---

## 12. Recent Papers (2025–2026)

The field has seen an explosion of activity in 2025–2026 with increasingly challenging benchmarks, agentic approaches, and new evaluation dimensions.

### 12.1 New Benchmarks (Chart QA)

#### ChartQAPro (2025)
- **Authors**: Masry, Islam, Ahmed, Bajaj, Kabir, Kartha, Laskar, Rahman, Rahman, Shahmohammadi, Thakkar, Parvez, Hoque, Joty
- **ArXiv**: 2504.05506
- **Contribution**: More diverse and challenging CQA benchmark addressing saturation of existing benchmarks. Includes multiple-choice, conversational, hypothetical, and unanswerable questions.
- **Dataset**: 1,341 charts from 157 sources; 1,948 human-written, human-verified QA pairs.
- **Key Finding**: Claude Sonnet 3.5 drops from **90.50% (ChartQA) to 55.81% (ChartQAPro)**.

#### ChartMuseum (NeurIPS 2025)
- **Authors**: Tang et al.
- **ArXiv**: 2505.13444
- **Contribution**: Entirely human-curated (no LLM assistance) chart QA benchmark focused on visual reasoning. 184 chart sources.
- **Dataset**: 1,162 expert-annotated questions. 10 open-source + 11 proprietary models evaluated.
- **Key Finding**: Qwen2.5-VL-72B: 38.5%, Gemini-2.5-Pro: 63.0%, **Human: 93.0%**. Visual reasoning performance is 35–55% worse than textual reasoning.

#### ChartMind (2025)
- **ArXiv**: 2505.23242
- **Contribution**: First **dual-language (English/Chinese)** CQA benchmark supporting open-ended outputs. Proposes ChartLLM framework with structured semantic cues.
- **Dataset**: 7 task categories, 14 mainstream multimodal models evaluated.

#### Chart-HQA (2025)
- **Authors**: Chen, Fang, Xiao, Li, Lin, Tang, Yang, Zhuang
- **ArXiv**: 2503.04095
- **Contribution**: Novel **Chart Hypothetical QA** task requiring counterfactual reasoning. Uses HAI (human-AI interactive) data synthesis.
- **Dataset**: 2,172 hypothetical questions, 18 MLLMs evaluated.
- **Key Finding**: Models exhibit output biases using parametric memory rather than genuine chart understanding.

#### InfoChartQA (2025)
- **ArXiv**: 2505.19028
- **Contribution**: First benchmark for **infographic chart understanding** with paired infographic/plain chart comparisons.
- **Dataset**: 5,642 pairs from 11 platforms; 60,949 questions (55,091 text-based + 7,937 visual-element-based).
- **Key Finding**: Claude 3.5 Sonnet: 81.37% on plain charts vs. **62.80% on infographic charts**. Models score only 55.33% on metaphor-related questions.

#### MultiChartQA (NAACL 2025)
- **Authors**: Zhu, Jia et al.
- **ArXiv**: 2410.14179
- **Contribution**: First benchmark for **multi-chart reasoning** with four evaluation dimensions: direct QA, parallel QA, comparative reasoning, sequential reasoning.
- **Dataset**: 1,370 charts from arXiv, OECD, Our World in Data, Pew Research.
- **Key Finding**: MLLMs trail humans significantly, especially with color or spatial constraints.

#### PolyChartQA (2025/2026)
- **ArXiv**: 2507.11939
- **Contribution**: First large-scale **multilingual CQA benchmark** with scalable pipeline for multilingual chart generation.
- **Dataset**: 22,606 charts, 26,151 QA pairs across **10 languages**.
- **Key Finding**: Significant performance gap between English and other languages, particularly low-resource ones.

#### ChartQA-X (2025)
- **Authors**: Hegde, Fazli et al.
- **ArXiv**: 2504.13275
- **Contribution**: Dataset with **explanations** for chart QA, evaluating faithfulness, informativeness, coherence.
- **Dataset**: 30,799 chart samples with questions, answers, and explanations. 6 VLMs evaluated.
- **Key Finding**: Model-generated explanations surpass human-written ones. Fine-tuning gains: +24.57 pts in explanation quality, +18.96 pp in QA accuracy.

#### SCI-CQA (2024/2025)
- **ArXiv**: 2412.12150
- **Contribution**: Emphasizes flowcharts as overlooked category. Exam-inspired evaluation from 15 top-tier CS conferences.
- **Dataset**: 202,760 image-text pairs refined to 37,607 high-quality charts; 5,629 curated questions.
- **Key Finding**: Existing benchmarks produce inflated scores due to template-based questions and narrow chart types.

### 12.2 Chart Reasoning & Agentic Approaches

#### ChartAgent (2025)
- **ArXiv**: 2510.04514
- **Contribution**: **Agentic framework** with chart-specific vision tools (40+ chart types) for visual reasoning. Multi-turn interaction loop with drawing annotations, cropping regions, localizing axes.
- **Key Finding**: **SOTA on ChartBench and ChartX**: +16.07% overall, +17.31% on numerically intensive queries.

#### ChartReasoner (2025)
- **ArXiv**: 2506.10116
- **Contribution**: Two-stage framework: **Chart2Code** (translates charts to ECharts code) + ChartThink dataset (140K multi-step reasoning samples). Trained via SFT + RL.
- **Key Finding**: Comparable to SOTA open-source models, approaches GPT-4o in OOD settings with fewer parameters.

#### Chart-RVR (2025)
- **ArXiv**: 2510.10973
- **Contribution**: **RL framework (GRPO)** with three verifiable rewards: chart-type classification, table reconstruction, process conformity.
- **Key Finding**: Outperforms SFT on both in-distribution and OOD datasets across 6 benchmarks.

#### RefChartQA (2025)
- **Authors**: Moured et al.
- **ArXiv**: 2503.23131
- **Contribution**: Integrates CQA with **visual grounding** (bounding box annotations linking answers to chart elements).
- **Dataset**: 73,702 image-question-grounding pairs.
- **Key Finding**: Spatial grounding improves accuracy by **+15%** and reduces hallucinations. 93.45% grounding correctness.

### 12.3 Chart-to-Code and Chart Editing

#### Chart2Code (2025)
- **ArXiv**: 2510.17932
- **Contribution**: Three-level benchmark: reproduction, editing, long-table to chart. 2,023 tasks, 22 chart types, ~5,000 charts from arXiv. 25 LMMs tested including GPT-5.
- **Key Finding**: Even **GPT-5 averages only 0.57 on code-based evaluation** and 0.22 on chart editing quality.

#### ChartM3 (2025)
- **ArXiv**: 2507.21167
- **Contribution**: **Multimodal chart editing** with natural language + visual indicators. Four difficulty levels.
- **Dataset**: 1,000 evaluation + 24,000 training samples.

#### ChartE3 (2026)
- **ArXiv**: 2601.21694
- **Contribution**: **End-to-end chart editing** without intermediate code/programs. Local editing (font, color) + global editing (data filtering, trend lines).

#### FigEdit (2025)
- **Authors**: Li, Rossi, Kim, Choudhary, Dernoncourt, Mathur, Tu, Zhao
- **ArXiv**: 2512.00752
- **Contribution**: 30,000+ samples, 10 chart types, 5 progressively challenging editing tasks.
- **Key Finding**: Chart editing is a **structured transformation problem** on marks, scales, encodings — not pixel manipulation.

### 12.4 Scientific Figure Benchmarks

#### SciFig (2026)
- **ArXiv**: 2601.04390
- **Contribution**: End-to-end AI agent for generating publication-ready **pipeline figures** from research paper text. Rubric-based evaluation from 2,219 real scientific figures.
- **Metrics**: Visual clarity, structural organization, overall quality (70.1% dataset-level).

#### SciFIBench (NeurIPS 2024, widely adopted 2025)
- **Authors**: Roberts et al.
- **ArXiv**: 2405.08807
- **Contribution**: Two-task scientific figure interpretation benchmark (Figure→Caption, Caption→Figure) with adversarial filtering.
- **Dataset**: 2,000 questions across 8 categories from arXiv figures. 28 LMMs evaluated.

#### MAC (2025)
- **ArXiv**: 2508.15802
- **Contribution**: **Continuously evolving live benchmark** from journal cover images (Nature, Science, Cell). 25,000+ image-text pairs.
- **Key Finding**: Models show strong perception but limited cross-modal scientific reasoning.

### 12.5 Visualization Literacy & Understanding

#### VLM Visualization Literacy (EuroVis 2025)
- **Authors**: Pandey et al.
- **ArXiv**: 2503.16632
- **Contribution**: First systematic evaluation using standardized **VLAT** (53 questions, 12 visualization types) and **CALVI** (45 items for misleading visualizations).
- **Key Finding**: Claude: 67.9% on VLAT. All models max **30.0% on CALVI** (misleading charts). Strong on line charts (76–96%), poor on bubble charts (18.6–61.4%).

#### Charts-of-Thought (2025)
- **Authors**: Das, Tarun, Mueller
- **ArXiv**: 2508.04842
- **Contribution**: Novel **prompting technique** guiding systematic data extraction, verification, and analysis.
- **Key Finding**: Claude-3.7-sonnet: 50.17 vs. human baseline 28.82. +21.8% for GPT-4.5, +9.4% for Gemini-2.0.

#### EncQA (IEEE VIS 2025)
- **ArXiv**: 2508.04650 (Apple Research)
- **Contribution**: Systematic benchmark covering **6 visual encoding channels** and 8 analytic tasks. 2,076 synthetic QA pairs.
- **Key Finding**: Legend-dependent encodings harder than axis-based. Performance does not improve with model size for many tasks.

#### CHARTOM (2025)
- **ArXiv**: 2408.14419 (ETH Zurich)
- **Contribution**: Evaluates whether LLMs can judge if a chart will **mislead humans** (FACT + MIND questions). Uses Human Misleadingness Index.
- **Dataset**: 112 charts (56 original + 56 manipulated), 5 chart types.
- **Key Finding**: Challenging for all models on both factual accuracy and theory-of-mind about human perception.

#### See or Recall (2025)
- **ArXiv**: 2504.09809
- **Contribution**: **Sanity check** revealing MLLMs can answer substantial portions of visualization questions **without seeing the visualization**.
- **Key Finding**: MLLM perception fundamentally differs from human approaches to chart reading.

### 12.6 Large-Scale Datasets

#### ChartGalaxy (2025)
- **Authors**: Li, Li et al.
- **ArXiv**: 2505.18668
- **Contribution**: **Million-scale infographic chart dataset**. 75 chart types, 440 variations, 68 layout templates.
- **Dataset**: **1,763,189 infographic charts** (1,701,356 synthetic + 61,833 real) from 18 websites.

#### EvoChart (AAAI 2025)
- **ArXiv**: 2409.01577
- **Contribution**: Self-training method for synthetic chart generation + EvoChart-QA benchmark.
- **Dataset**: 650 real-world charts from 140 websites, 1,250 expert-curated questions.

### 12.7 Summary Table — Recent Papers (2025–2026)

| Paper | Year | ArXiv | Dataset Size | Top Model Score | Human Score |
|-------|------|-------|-------------|----------------|-------------|
| ChartQAPro | 2025 | 2504.05506 | 1,948 QA pairs | Claude 3.5: 55.81% | — |
| ChartMuseum | 2025 | 2505.13444 | 1,162 questions | Gemini-2.5-Pro: 63.0% | 93.0% |
| ChartMind | 2025 | 2505.23242 | 7 task categories | ChartLLM best | — |
| Chart-HQA | 2025 | 2503.04095 | 2,172 questions | 18 MLLMs tested | — |
| InfoChartQA | 2025 | 2505.19028 | 60,949 questions | Claude 3.5: 62.80% (infographic) | — |
| MultiChartQA | 2025 | 2410.14179 | 1,370 charts | Below human | Yes |
| PolyChartQA | 2025/26 | 2507.11939 | 26,151 QA, 10 langs | English best | — |
| ChartQA-X | 2025 | 2504.13275 | 30,799 samples | +24.57 pts fine-tuned | Yes |
| SCI-CQA | 2024/25 | 2412.12150 | 5,629 questions | — | — |
| ChartAgent | 2025 | 2510.04514 | Multi-benchmark | +16.07% SOTA | — |
| ChartReasoner | 2025 | 2506.10116 | 140K samples | Near GPT-4o | — |
| Chart-RVR | 2025 | 2510.10973 | 6 benchmarks | Outperforms SFT | — |
| RefChartQA | 2025 | 2503.23131 | 73,702 pairs | +15% with grounding | — |
| Chart2Code | 2025 | 2510.17932 | 2,023 tasks | GPT-5: 0.57/0.22 | — |
| ChartM3 | 2025 | 2507.21167 | 1,000 samples | GPT-4o limited | — |
| ChartE3 | 2026 | 2601.21694 | — | — | — |
| FigEdit | 2025 | 2512.00752 | 30,000+ samples | — | — |
| SciFig | 2026 | 2601.04390 | 2,219 figures | 70.1% quality | — |
| SciFIBench | 2024/25 | 2405.08807 | 2,000 questions | GPT-4o/Gemini best | Yes |
| MAC | 2025 | 2508.15802 | 25,000+ pairs | +11% with DAD | — |
| VLM Vis Literacy | 2025 | 2503.16632 | VLAT + CALVI | Claude: 67.9% | — |
| Charts-of-Thought | 2025 | 2508.04842 | VLAT | Claude-3.7: 50.17 | 28.82 |
| EncQA | 2025 | 2508.04650 | 2,076 QA pairs | 9 VLMs | — |
| CHARTOM | 2025 | 2408.14419 | 112 charts | All struggle | HMI |
| See or Recall | 2025 | 2504.09809 | VisQA tasks | — | — |
| ChartGalaxy | 2025 | 2505.18668 | 1,763,189 charts | — | — |
| EvoChart | 2025 | 2409.01577 | 650 + 1,250 QA | — | — |

### 12.8 Key Takeaways from 2025–2026

1. **Benchmark saturation exposed**: ChartQAPro showed Claude drops from 90.5% → 55.8% when benchmarks get harder. Existing numbers overstate capability.
2. **Multi-chart reasoning**: MultiChartQA is the first benchmark tackling reasoning across multiple charts — a critical real-world skill.
3. **Multilingual evaluation expanding**: PolyChartQA (10 languages), ChartMind (EN/CN) address the multilingual gap.
4. **Agentic approaches winning**: ChartAgent (+16% SOTA), ChartReasoner, Chart-RVR show tool-augmented and RL-based approaches outperform end-to-end models.
5. **Visual grounding matters**: RefChartQA shows grounding answers to chart elements improves accuracy +15% and reduces hallucination.
6. **Chart editing emerges**: Chart2Code, ChartM3, ChartE3, FigEdit establish chart editing as a new evaluation dimension — even GPT-5 struggles.
7. **Misleading chart detection**: CHARTOM and CALVI show models max ~30% on misleading chart identification — a major gap.
8. **Hypothesis/counterfactual reasoning**: Chart-HQA reveals models cannot handle "what if" questions about charts.
9. **Vision not always used**: "See or Recall" proves models often answer chart questions from parametric memory, not actual visual understanding.
10. **Million-scale datasets**: ChartGalaxy (1.7M charts) enables training at unprecedented scale.

---

---

## 13. Detailed Paper Breakdown Table (2023–2026)

The table below provides a fine-grained breakdown of each paper from 2023–2026, organized by year (most recent first). Columns: paper name, link, focus area, novel contribution, models evaluated, metrics used, and key performance results.

### 2026

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **ChartE3** | [arXiv:2601.21694](https://arxiv.org/abs/2601.21694) | Chart Editing | End-to-end chart editing without intermediate code/programs; local + global edits | Multiple MLLMs | End-to-end edit quality, structural fidelity | Pipeline approaches limited on complex edits |
| **SciFig** | [arXiv:2601.04390](https://arxiv.org/abs/2601.04390) | Figure Generation | AI agent for generating publication-ready pipeline figures from paper text; rubric-based evaluation | LLM-based agents | Visual clarity, structural organization, overall quality rubric | 70.1% dataset-level quality, 66.2% paper-specific |

### 2025 — Benchmarks

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **ChartQAPro** | [arXiv:2504.05506](https://arxiv.org/abs/2504.05506) | Benchmark / Evaluation | More challenging CQA with multiple-choice, conversational, hypothetical, and unanswerable questions | 21 models including GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Qwen-VL, InternVL, LLaVA | Accuracy across question types | Claude 3.5 Sonnet: 55.81% (vs. 90.50% on ChartQA); exposes benchmark saturation |
| **ChartMuseum** | [arXiv:2505.13444](https://arxiv.org/abs/2505.13444) | Benchmark / Evaluation | Entirely human-curated (no LLM assistance) benchmark; 184 chart sources; visual reasoning focus | 10 open-source + 11 proprietary: GPT-4o, Gemini-2.5-Pro, Claude 3.5, Qwen2.5-VL-72B, InternVL2 | Accuracy (visual vs. textual reasoning) | Gemini-2.5-Pro: 63.0%, Qwen2.5-VL-72B: 38.5%, Human: **93.0%**. Visual 35–55% worse than textual |
| **ChartMind** | [arXiv:2505.23242](https://arxiv.org/abs/2505.23242) | Benchmark / Evaluation | First dual-language (EN/CN) CQA with open-ended outputs (summarization, trend analysis); proposes ChartLLM framework | 14 mainstream multimodal models | Task-specific accuracy, open-ended evaluation | ChartLLM outperforms instruction-following, OCR-enhanced, and CoT paradigms |
| **Chart-HQA** | [arXiv:2503.04095](https://arxiv.org/abs/2503.04095) | Benchmark / Evaluation | Novel hypothetical/counterfactual QA task; HAI (human-AI interactive) data synthesis | 18 MLLMs of varying sizes | Accuracy on hypothetical questions | Models exhibit output biases using parametric memory; significant generalization challenges |
| **InfoChartQA** | [arXiv:2505.19028](https://arxiv.org/abs/2505.19028) | Benchmark / Evaluation | First infographic chart benchmark; paired infographic/plain chart comparisons | 20 MLLMs including Claude 3.5 Sonnet, GPT-4o | Accuracy (text-based + visual-element-based questions) | Claude 3.5: 81.37% plain → 62.80% infographic; 55.33% on metaphor questions |
| **MultiChartQA** | [arXiv:2410.14179](https://arxiv.org/abs/2410.14179) | Benchmark / Evaluation | First multi-chart reasoning benchmark; 4 evaluation dimensions (direct, parallel, comparative, sequential) | GPT-4o, Gemini, Claude, open-source VLMs | Accuracy across 4 reasoning types | MLLMs trail humans significantly; struggle with color/spatial constraints |
| **PolyChartQA** | [arXiv:2507.11939](https://arxiv.org/abs/2507.11939) | Benchmark / Evaluation | First large-scale multilingual CQA; scalable multilingual chart generation pipeline | Multiple MLLMs across 10 languages | Accuracy by language and chart type | Significant gap English vs. other languages; low-resource languages worst |
| **ChartQA-X** | [arXiv:2504.13275](https://arxiv.org/abs/2504.13275) | Benchmark / Evaluation | Explanations for chart QA; evaluates faithfulness, informativeness, coherence | LLaVA 1.6, Phi-3, CogVLM, Deepseek-VL, Qwen2-VL, GPT-4o | QA accuracy, explanation quality, perplexity | +24.57 pts explanation quality, +18.96 pp QA accuracy, +14.75 pp on unseen benchmarks |
| **SCI-CQA** | [arXiv:2412.12150](https://arxiv.org/abs/2412.12150) | Benchmark / Evaluation | Flowcharts as overlooked category; exam-inspired evaluation from 15 top CS conferences | Multiple MLLMs | Objective + open-ended accuracy | Existing benchmarks produce inflated scores |
| **Chart QA from Analytical Narratives** | [arXiv:2507.01627](https://arxiv.org/abs/2507.01627) | Benchmark / Evaluation | CQA from visualization notebooks with ecologically valid multi-view charts | GPT-4.1 and others | Accuracy | GPT-4.1: 69.3% — underscores challenges of authentic CQA |

### 2025 — Reasoning & Agentic Models

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **ChartAgent** | [arXiv:2510.04514](https://arxiv.org/abs/2510.04514) | Agentic Reasoning | Agentic framework with chart-specific vision tools (40+ chart types); multi-turn interaction with annotations, cropping, axis localization | Multiple MLLMs as backbone | Accuracy on ChartBench, ChartX | **+16.07% overall SOTA**, +17.31% on numerically intensive queries |
| **ChartReasoner** | [arXiv:2506.10116](https://arxiv.org/abs/2506.10116) | Reasoning Model | Chart2Code (chart → ECharts code) + ChartThink (140K reasoning samples); SFT + RL training | Open-source models, compared to GPT-4o | Accuracy on ChartQA, ChartBench, EvoChart-QA, ChartQAPro | Approaches GPT-4o in OOD settings with fewer parameters |
| **Chart-RVR** | [arXiv:2510.10973](https://arxiv.org/abs/2510.10973) | RL for Charts | RL framework (GRPO) with 3 verifiable rewards: chart-type classification, table reconstruction, process conformity | RL-trained models vs. SFT baselines | Accuracy across 6 chart benchmarks | Outperforms SFT on both in-distribution and OOD; largest gains on EvoChart, ChartQAPro, ChartBench |
| **RefChartQA** | [arXiv:2503.23131](https://arxiv.org/abs/2503.23131) | Visual Grounding | CQA with bounding box annotations linking answers to chart elements | Instruction-tuned VLMs | QA accuracy + grounding correctness | **+15% accuracy** with grounding; 93.45% grounding agreement |
| **Charts-of-Thought** | [arXiv:2508.04842](https://arxiv.org/abs/2508.04842) | Prompting Technique | Structured prompting for systematic data extraction, verification, and analysis | Claude-3.7-sonnet, GPT-4.5, Gemini-2.0-pro | VLAT score | Claude-3.7: 50.17 (human: 28.82). +21.8% GPT-4.5, +9.4% Gemini-2.0, +13.5% Claude |

### 2025 — Chart Editing & Generation

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **Chart2Code** | [arXiv:2510.17932](https://arxiv.org/abs/2510.17932) | Chart-to-Code / Editing | 3-level benchmark: reproduction, editing, long-table→chart; 22 chart types | 25 LMMs: GPT-5, Qwen2.5-VL, InternVL3/3.5, MiMo-VL, Seed-1.6-VL | Code-based evaluation + chart quality assessment | Even **GPT-5: 0.57 code-based, 0.22 chart editing quality** |
| **ChartM3** | [arXiv:2507.21167](https://arxiv.org/abs/2507.21167) | Chart Editing | Multimodal chart editing (NL + visual indicators); 4 difficulty levels | GPT-4o and other MLLMs | Visual + code metrics | GPT-4o shows significant limitations interpreting visual indicators |
| **FigEdit** | [arXiv:2512.00752](https://arxiv.org/abs/2512.00752) | Chart Editing | 30K+ samples, 10 chart types, 5 progressive tasks; chart editing as structured transformation (not pixel manipulation) | Multiple MLLMs | Structural transformation quality | Models incorrectly treat chart edits as visual rearrangements |
| **ChartGalaxy** | [arXiv:2505.18668](https://arxiv.org/abs/2505.18668) | Dataset / Generation | Million-scale infographic dataset; 75 chart types, 440 variations, 68 layout templates | Used for fine-tuning + benchmarking | Generation quality, understanding benchmarks | 1,763,189 charts enabling training at unprecedented scale |
| **EvoChart** | [arXiv:2409.01577](https://arxiv.org/abs/2409.01577) | Dataset / Self-Training | Self-training for synthetic chart generation + EvoChart-QA benchmark (real-world) | Multiple chart understanding models | QA accuracy on real-world charts | 650 real charts, 1,250 expert-curated questions |

### 2025 — Visualization Literacy & Understanding

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **VLM Vis Literacy** | [arXiv:2503.16632](https://arxiv.org/abs/2503.16632) | Evaluation / Vis Literacy | First standardized VLAT (53 Q, 12 vis types) + CALVI (45 items, misleading charts) evaluation | GPT-4, Claude, Gemini, Llama | VLAT accuracy, CALVI accuracy | Claude: 67.9% VLAT. All models max **30.0% CALVI**. Line charts 76–96%, bubble charts 18.6–61.4% |
| **Do LLMs Have Vis Literacy?** | [arXiv:2501.16277](https://arxiv.org/abs/2501.16277) | Evaluation / Vis Literacy | Modified VLAT with randomized values to prevent training data exposure bias | GPT-4, Gemini | Modified VLAT accuracy | LLMs fail to match general public visualization literacy; rely on pre-existing knowledge |
| **EncQA** | [arXiv:2508.04650](https://arxiv.org/abs/2508.04650) | Evaluation / Encoding | 6 visual encoding channels × 8 analytic tasks; systematic encoding evaluation | 9 SOTA VLMs | Per-encoding accuracy | Legend-dependent encodings harder; performance does not improve with model size |
| **CHARTOM** | [arXiv:2408.14419](https://arxiv.org/abs/2408.14419) | Evaluation / Misleading | Theory-of-mind for misleading charts; FACT + MIND questions; Human Misleadingness Index | GPT, Claude, Gemini, Qwen, Llama, LLaVA series | FACT accuracy, MIND accuracy, HMI | Challenging for all models on both FACT and MIND |
| **See or Recall** | [arXiv:2504.09809](https://arxiv.org/abs/2504.09809) | Evaluation / Sanity Check | Reveals MLLMs answer visualization questions without seeing the visualization | Multiple MLLMs | Accuracy with/without visual input | MLLM perception fundamentally differs from human chart reading |
| **SciFIBench** | [arXiv:2405.08807](https://arxiv.org/abs/2405.08807) | Benchmark / Scientific Figs | Figure↔Caption matching with adversarial filtering; 8 categories from arXiv | 28 LMMs including GPT-4o, Gemini 1.5 | Accuracy | GPT-4o and Gemini 1.5 best but still below human baseline |
| **MAC** | [arXiv:2508.15802](https://arxiv.org/abs/2508.15802) | Live Benchmark | Continuously evolving benchmark from journal covers (Nature, Science, Cell); proposes DAD method | Multiple MLLMs | Scientific reasoning accuracy | +11% improvement with DAD; models better on older content |

### 2024

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **CharXiv** | [arXiv:2406.18521](https://arxiv.org/abs/2406.18521) | Benchmark / Evaluation | Real arXiv charts; descriptive vs. reasoning split; leak-resistant; expert-annotated | GPT-4o, GPT-4V, Gemini 1.5 Pro, Claude 3.5 Sonnet, InternVL, LLaVA-NeXT, Qwen-VL | Accuracy (exact match + GPT-4 judge), descriptive/reasoning split | GPT-4o: 80% desc / **47% reasoning**. Human: ~80% reasoning |
| **ChartX** | [arXiv:2402.12185](https://arxiv.org/abs/2402.12185) | Benchmark / Multi-task | 18 chart types, 7 tasks; includes chart redrawing as understanding test | GPT-4V, Gemini Pro Vision, Claude 3, open-source VLMs | Accuracy, BLEU/ROUGE, structural similarity, GPT-based eval | GPT-4V struggled on complex types; performance varies dramatically by chart type |
| **ChartBench** | [arXiv:2312.15915](https://arxiv.org/abs/2312.15915) | Benchmark / Evaluation | Acc+ metric addressing yes-bias; 9 chart types, 2 difficulty levels | GPT-4V, Gemini Pro Vision, InternVL, LLaVA, Qwen-VL, CogVLM | Acc+, standard accuracy, per-type/question breakdown | Yes-bias inflated scores significantly; Acc+ reveals much lower real performance |
| **ChartInsights** | EMNLP 2024 Findings | Benchmark / Low-level | 10 low-level analysis tasks (retrieve, extremum, range, distribution, anomalies, cluster, correlate, sort, filter, derive) | Multiple MLLMs | Accuracy with numerical tolerance, per-task/chart breakdown | Good on simple retrieval, poor on precise numerical reading |
| **ChartMimic** | [arXiv:2406.09961](https://arxiv.org/abs/2406.09961) | Chart-to-Code | Chart reproduction via code generation; 18 matplotlib types; direct + customized mimic | GPT-4V, Gemini, Claude, open-source VLMs | Code executability, pixel similarity, element accuracy (type, layout, color, labels, data) | GPT-4V best but struggles with multi-panel; open-source models significant gaps |
| **TinyChart** | [arXiv:2404.16635](https://arxiv.org/abs/2404.16635) | Specialized Model | 3B params; Visual Token Merging + Program-of-Thoughts (PoT) — generates executable Python for reasoning | TinyChart vs. GPT-4V, UniChart, ChartLlama, MatCha, DePlot | ChartQA accuracy, PlotQA accuracy | **ChartQA ~83.6%** — rivals GPT-4V with only 3B params |
| **ChartInstruct** | [arXiv:2403.09028](https://arxiv.org/abs/2403.09028) | Specialized Model | Systematic instruction tuning for charts; 191K chart-specific instruction samples via GPT-4 | ChartInstruct-UniChart, ChartInstruct-LLaVA vs. baselines | ChartQA accuracy, PlotQA accuracy | SOTA among open-source at release; UniChart variant ~49.6%/73.6% (human/aug) |
| **ChartAssistant** | [arXiv:2401.02384](https://arxiv.org/abs/2401.02384) | Specialized Model | Largest chart pre-training (4.2M chart-table pairs); chart-to-table alignment as foundation | ChartAssistant-7B/13B vs. GPT-4V, UniChart, ChartLlama | ChartQA accuracy, chart-to-table metrics | Competitive with GPT-4V; excels on data extraction |
| **StructChart** | [arXiv:2309.11268](https://arxiv.org/abs/2309.11268) | Specialized Model | 3-stage pipeline: Perceive → Structure → Reason; explicit decomposition | Pipeline stages with different backbones + LLM reasoner | ChartQA, data extraction accuracy | Strong on data extraction; competitive with LLM reasoners |

### 2023

| Paper | Link | Focus | Novel Contribution | Models Evaluated | Metrics | Key Performance |
|-------|------|-------|-------------------|-----------------|---------|-----------------|
| **SciGraphQA** | [arXiv:2308.03349](https://arxiv.org/abs/2308.03349) | Dataset / QA | Large-scale multi-turn QA over real scientific figures from arXiv; 295K QA pairs | PaLM-2, GPT-4, LLaVA | Open-ended QA accuracy, BLEU, ROUGE | Models achieving >80% on synthetic benchmarks score <50% on real scientific figures |
| **MMC** | [arXiv:2311.10774](https://arxiv.org/abs/2311.10774) | Benchmark + Training | 600K instruction-tuning dataset + MMC-Benchmark (2,400 charts); multi-task evaluation | GPT-4V, open-source MLLMs | Accuracy (MC), GPT-4 scoring (open-ended) | GPT-4V: ~58% on MC. Open-source significantly underperformed |
| **UniChart** | [arXiv:2305.14761](https://arxiv.org/abs/2305.14761) | Specialized Model | First unified multi-task model for charts (QA + summarization + table extraction); 270M params | UniChart vs. MatCha, DePlot, Pix2Struct | ChartQA accuracy, Chart-to-Text BLEU/ROUGE, OpenCQA metrics | ChartQA Human 43.9%, Aug 88.6%. SOTA at release |
| **ChartLlama** | [arXiv:2311.16483](https://arxiv.org/abs/2311.16483) | Specialized Model | First to combine chart understanding + chart code generation (matplotlib); 13B params | ChartLlama vs. GPT-4V, LLaVA | ChartQA accuracy, code generation quality | Competitive with GPT-4V; novel chart generation capability |
| **MatCha** | [arXiv:2212.09662](https://arxiv.org/abs/2212.09662) | Specialized Model | Math reasoning pre-training + chart derendering; first to add math pre-training for charts | MatCha vs. Pix2Struct, prior VQA models | ChartQA relaxed accuracy, PlotQA accuracy | ChartQA ~51% avg; significantly beat prior models |
| **DePlot** | [arXiv:2212.10505](https://arxiv.org/abs/2212.10505) | Specialized Model | Decouples perception (chart-to-table) from reasoning (LLM); enables one-shot chart QA | DePlot + PaLM-2/Codex vs. MatCha, prior models | ChartQA relaxed accuracy | ChartQA ~54% with PaLM-2; flexible — any LLM as reasoner |
| **MathVista** | [arXiv:2310.02255](https://arxiv.org/abs/2310.02255) | Benchmark / Math-Visual | Math-visual reasoning including chart/figure subset; diverse visual contexts | GPT-4V, Gemini, Claude, Bard, LLaVA, InstructBLIP | Accuracy on math-visual tasks | GPT-4V: ~49.9% overall; chart questions especially challenging |

---

*Note: This survey draws from research published through early 2026. Performance numbers are approximate ranges synthesized from multiple reported results. ArXiv IDs are provided for verification. For the latest results, consult papers directly on arXiv and Semantic Scholar.*
