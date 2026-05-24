# SciFig-Eval Paper Framing

## Core Thesis

**"Description quality and behavioral reliability are orthogonal dimensions — current VLM benchmarks measure one while ignoring the other, creating a false sense of readiness for scientific deployment."**

---

## Title Candidates

1. **Measuring What Matters: Why Description Quality Alone Misjudges VLM Readiness for Scientific Use**
2. **SciFig-Eval: Revealing the Gap Between Quality and Reliability in Scientific Figure Understanding**
3. **Beyond Accuracy: A Multi-Dimensional Evaluation of Vision-Language Models on Scientific Figures**

---

## The Argument (4-step narrative)

### Step 1: The field evaluates VLMs on quality/accuracy
- ChartQA, FigureQA, PlotQA etc. measure "can the model answer correctly?"
- Leaderboards rank models by accuracy → highest scorer = "best model"
- Deployment decisions are made based on these rankings

### Step 2: Quality metrics miss critical failure modes
- A model scoring 91.6 on MQM (GPT-5.2) admits visual limitations only 6% of the time
- A model scoring 62.1 (Phi-4) has near-zero caption bias resistance (0.05) — it trusts text over its own eyes
- The "best" description writer confidently fabricates answers 98% of the time when it can't see something

### Step 3: We propose a multi-dimensional framework
Two evaluation axes:
- **Description** (open-ended): what does the model *say* about a figure?
- **Reasoning** (targeted): can the model *think* about a figure?

Two conditions per axis:
- **Standard**: clean images, fair questions
- **Adversarial**: transformations, misleading context, psychological probes

Plus a behavioral theory — the **A-R-I framework**:
- **Admittance**: does the model acknowledge when it can't see? (honesty under uncertainty)
- **Resistance**: does the model push back on false premises and non-existent elements? (robustness to deception)
- **Inductance**: can the model infer missing information from context? (reasoning under degradation)

### Step 4: These dimensions are orthogonal
Rankings on quality do NOT predict rankings on reliability:
- GPT-5.2: #1 quality, #2 resistance, #4 admittance
- Gemini: #2 quality, #1 resistance, #1 admittance
- Phi-4: #8 quality, #8 resistance, #8 admittance (consistent bottom, but still orthogonal for mid-tier models)
- Qwen-30B: #6 quality but #7 resistance (MoE architecture hurts behavioral reliability more than quality)

**Implication**: Deploying VLMs in scientific workflows based on quality benchmarks alone is dangerous.

---

## The 2×2 Matrix

|  | Standard (Baseline) | Adversarial (Behavioral) |
|---|---|---|
| **Description** (open-ended) | Baseline MQM (250 fig × 8 models) | Transforms, Caption Bias, Passive Admittance/Inductance |
| **Reasoning** (targeted Qs) | Capability Questions (100 fig × 8 models) | Hallucination Probes, Active Admittance/Inductance |

### Description axis breakdown:
- **Baseline**: clean image + caption → MQM score
- **Robustness transforms**: noise, rotation, low_contrast → MQM drop
- **In-paper**: figure in PDF page context → MQM (in-paper blur as sub-baseline)
- **Caption bias**: poisoned caption → MQM + specialized bias scoring (did model echo false claims?)
- **Passive admittance**: admittance-blurred image → MQM + specialized scoring (did model admit blur?)
- **Passive inductance**: inductance-blurred image → MQM + specialized scoring (did model infer missing element?)

### Reasoning axis breakdown:
- **Capability baseline**: counting, computation, comparison, pattern analysis
- **Hallucination probes**: inexist (presupposition embedding), contra (false premise anchoring), unanswerable (domain conventions)
- **Active admittance**: question about blurred element → admits/fabricates/correct
- **Active inductance**: question about inferable element → admits/fabricates/correct

---

## Key Findings That Drive the Narrative

### Finding 1: Quality ≠ Reliability (the headline)
| Model | MQM (Quality) | Resistance | Caption Bias R | Admittance |
|---|---|---|---|---|
| GPT-5.2 | 91.6 (#1) | 0.81 (#2) | 0.89 (#2) | 0.06 (#4) |
| Gemini | 90.2 (#2) | 0.91 (#1) | 0.90 (#1) | 0.90 (#1) |
| Llama4 | 81.6 (#3) | 0.78 (#3) | 0.74 (#3) | 0.22 (#2) |
| Phi-4 | 62.1 (#8) | 0.21 (#8) | 0.05 (#8) | 0.02 (#8) |

Spearman correlation between MQM rank and Admittance rank would be interesting to compute.

### Finding 2: The Honesty Gap
- Gemini admits 90% of the time when it can't see → the only "honest" model
- GPT-5.2 admits 6% → confidently fabricates, but fabrications are often plausible
- Most models never admit → 98%+ fabrication rate across the board
- **Implication**: Current training (RLHF) may suppress uncertainty expression

### Finding 3: Caption Dependency Spectrum
- Gemini/GPT-5.2: trust image over caption (R=0.89-0.90)
- Mid-tier (Llama, Qwen-235B): partially influenced (R=0.56-0.74)
- Phi-4: almost entirely caption-dependent (R=0.05)
- **Implication**: Smaller/weaker models may use captions as a crutch, describing what the caption says rather than what the image shows

### Finding 4: Vulnerability profiles differ by probe type
- **Unanswerable**: easiest to resist (most models 0.73-0.95) — models CAN refuse
- **Inexist (presupposition)**: hardest (0.04-0.88) — definite articles trick models into accepting non-existent elements
- **Contra (false premise)**: middle difficulty — anchoring with plausible-but-wrong values
- **Implication**: Models struggle more with implicit assumptions than explicit false claims

### Finding 5: The Inductance Validation
- When elements ARE inferable: 21-81% correct fabrication (models can reason from context)
- When elements are NOT inferable: 0-14% correct fabrication (lucky guesses at best)
- **Implication**: The A-R-I framework captures real behavioral distinctions, not just noise

### Finding 6: Probe Designer Independence (Ablation)
- Mistral-designed vs GPT-4o-designed probes: resistance 0.86 vs 0.80, caption bias 0.87 vs 0.89
- **Implication**: Results are robust to the choice of probe generator — addresses circularity concern

---

## Psychology-Informed Evaluation as Methodological Contribution

This is what elevates the paper beyond "we tested models." The probes are grounded in cognitive science:

| Principle | Source | How We Use It |
|---|---|---|
| Presupposition embedding | Loftus & Zanni (1975) | Inexist probes use definite articles to presuppose element existence |
| Anchoring bias | Tversky & Kahneman (1974) | Contra probes embed plausible-but-wrong values (20-30% off) |
| Cooperative principle | Grice (1975) | Models assume questions are well-formed, don't challenge premises |
| Sycophantic agreement | Sharma et al. (2023) | Caption bias exploits models' tendency to agree with provided text |
| Co-occurrence priors | Li et al. (2023, POPE) | Inexist probes target elements commonly found in chart types |
| Peripheral misinformation | Loftus (2005) | Caption bias poisons secondary details, not primary features |

**Why this matters for NLP**: We're not just finding that models fail — we're showing *why* they fail by mapping failure modes to known cognitive biases. This connects VLM evaluation to decades of cognitive psychology research, offering a principled framework for designing harder, more targeted evaluations.

---

## A-R-I as Reusable Theoretical Contribution

The Admittance-Resistance-Inductance framework is analogous to electrical circuit properties:
- **Admittance** (honesty): Does current (information) flow freely, or does the model gate it? High admittance = model acknowledges what it can/can't see.
- **Resistance** (robustness): Does the model resist false currents (misleading inputs)? High resistance = model pushes back on deception.
- **Inductance** (inference): Can the model generate current (knowledge) from changing fields (context)? High inductance = model reasons from partial information.

**Why reviewers would care**: This isn't just a scoring rubric — it's a decomposition of model behavior into interpretable, independently measurable dimensions. Other researchers can apply A-R-I to their own evaluations, beyond scientific figures.

---

## Paper Structure (8 pages)

### 1. Introduction (1.5 pages)
- Para 1: VLMs deployed in science. Stakes are high.
- Para 2: Current benchmarks only measure quality/accuracy. Gap: no behavioral evaluation.
- Para 3: We introduce SciFig-Eval. Contributions (numbered):
  1. A 2×2 evaluation framework (description/reasoning × standard/adversarial)
  2. Psychology-informed probe design grounded in cognitive science
  3. The A-R-I behavioral framework for decomposing model honesty
  4. Empirical finding: quality and reliability are orthogonal
- Para 4: Hook — "The highest-scoring model on description quality admits visual limitations only 6% of the time, while confidently fabricating answers 98% of the time when shown blurred elements."
- Figure 1: Overview diagram showing the 2×2 matrix with example probes

### 2. Related Work (1 page)
- 2.1 Chart/Figure understanding benchmarks (ChartQA, FigureQA, PlotQA, ChartBench)
- 2.2 VLM hallucination and reliability (POPE, CHAIR, HallusionBench)
- 2.3 Evaluation methodology (MQM, human evaluation, LLM-as-judge)

### 3. SciFig-Eval Framework (2.5 pages)
- 3.1 Dataset: 250 English figures (bar/line/pie), sourcing, annotation
- 3.2 Description evaluation: Checklist-based MQM with binding verification
- 3.3 Reasoning evaluation: Capability questions (4 types)
- 3.4 Adversarial evaluation: Caption bias, hallucination probes, selective blur
- 3.5 A-R-I behavioral framework
- Table 1: Dataset statistics
- Table 2: Evaluation dimensions and metrics

### 4. Experiments (2 pages)
- 4.1 Models (8 VLMs, justify selection — commercial vs open, range of sizes)
- 4.2 Description results: MQM baseline → transforms → caption bias → passive blur
- 4.3 Reasoning results: Capability baseline → hallucination → active blur
- 4.4 Cross-dimensional analysis: quality vs reliability correlations
- Table 3: MQM leaderboard
- Table 4: Resistance/caption bias/admittance leaderboard
- Figure 2: Scatter plot quality vs reliability
- Figure 3: Radar chart per model across A-R-I dimensions

### 5. Analysis (0.5 pages)
- 5.1 Why quality ≠ reliability (training incentives, RLHF effects)
- 5.2 The psychology of model failure (which cognitive biases work and why)
- 5.3 Ablation: probe designer independence

### 6. Conclusion (0.5 pages)
- Summary of contributions
- Practical recommendations for VLM deployment in science
- Future work: more figure types, interactive evaluation, multilingual extension

### Limitations (not counted)
- English only (thesis had 4 languages, ACL subset is English)
- 3 figure types (bar, line, pie) — not tables, diagrams, etc.
- GPT-4o as primary judge — addressed by ablation but single judge still a limitation
- Dataset from arXiv — domain bias toward CS/ML papers

### Ethics (not counted)
- Figures from arXiv (open access)
- No personal data
- Benchmark designed to expose failures, not to game models

---

## Hook Sentences (for reviewer impact)

- "The model that writes the best scientific figure descriptions is also the one that most confidently fabricates information it cannot see."
- "When given a poisoned caption, Phi-4-multimodal follows the text over its own visual evidence 95% of the time."
- "Only one of eight evaluated VLMs acknowledges visual uncertainty — the rest fabricate with 98%+ confidence."
- "Presupposition embedding, a technique from eyewitness testimony research, reveals that VLMs are susceptible to the same cognitive traps as humans."
