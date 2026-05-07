# SciFig-Evaluation: Research Plan

## Main Research Question

**"How well do large language models truly understand scientific figures, and where do their capabilities break down?"**

Beyond surface-level description, do multimodal LLMs genuinely comprehend scientific visualizations, or do they rely on text shortcuts, parametric memory, and pattern matching?

---

## Contributions (What We Propose)

### Contribution 1: SciFig Benchmark
A multilingual scientific figure description benchmark.

| Aspect | Detail |
|--------|--------|
| Figures | 1,005 from real academic papers |
| Languages | 4 (English, Chinese, Bulgarian, German) |
| Annotations | 1,411 from 8 human annotators |
| Figure types | Line plots, bar charts, pie charts |
| Generator models | 11 across 5 families |
| Judge models | 4 from 2 families |
| Evaluation | MQM framework adapted from translation quality metrics |

No existing benchmark covers multilingual scientific figure description at this scale with open-ended generation and multi-judge evaluation.

### Contribution 2: Adversarial Probing Framework
A systematic framework of five adversarial strategies to probe figure understanding beyond standard accuracy:

| Strategy | What it probes |
|----------|---------------|
| A1. Hallucination probing | Fabrication about absent, incorrect, irrelevant, or unanswerable content |
| A2. Caption & context bias | Reliance on text shortcuts vs genuine visual reading |
| A3. Visual degradation & text manipulation | Robustness to image quality and text obfuscation |
| A4. Prompt reverse inconsistency | Stability of understanding under contradictory framing |
| A5. Misleading chart detection | False alarm rate — inventing problems on correct charts |

### Contribution 3: Capability Benchmark Suite
Structured capability tests at varying difficulty levels:

| Category | Subtypes |
|----------|----------|
| Descriptive (reading) | Numerical value reading, chart element identification |
| Reasoning (thinking) | Computation, visual counting, open-ended reasoning, cross-panel integration |
| In-paper context | Figure understanding on real paper pages |

### Contribution 4: Admittance & Resistance Metrics
Two new metrics for evaluating model behavior under adversarial conditions, capturing aspects that existing metrics (accuracy, MQM) miss.

**Admittance** — measures the degree to which a model acknowledges its limitations when information is missing or unreadable.

| Scenario | High admittance | Low admittance |
|----------|----------------|----------------|
| Blurred axis | "The axis labels are not legible" | Fabricates "Patient Visits 0-100" |
| Absent element | "There are no error bars in this figure" | Describes fictional error bars |
| Wrong premise | "Actually, Frustration is 25.1%, not 15.1%" | Accepts and builds on false premise |
| Unanswerable | "The p-value cannot be determined from this chart" | Fabricates "p < 0.05" |

Applies when: information is missing, degraded, absent, or beyond what the chart can convey.

**Resistance** — measures the degree to which a model maintains accuracy despite misleading or adversarial input.

| Scenario | High resistance | Low resistance |
|----------|----------------|----------------|
| Wrong caption | Ignores wrong caption, describes what it sees | Description follows wrong caption |
| Misplaced figure | Focuses on the figure, ignores surrounding page text | Injects page text into description |
| Image transforms | Description quality maintained | Quality collapses |
| Prompt reverse | Consistent answers to contradictory framings | Agrees with both true and false statements |

Applies when: misleading context, conflicting information, or adversarial framing is present.

**Why both are needed:**
- A model can have high resistance but low admittance (stays accurate but never says "I don't know")
- A model can have high admittance but low resistance (admits uncertainty when probed but gets influenced by wrong context)
- Existing metrics (MQM, accuracy) don't distinguish between these behaviors

**Measurement approach:**
| Probe type | Scoring method |
|------------|---------------|
| Inexist / unanswerable | Rule-based keyword matching for refusal |
| Contra | LLM judge — did model correct the premise? |
| Irrel | Rule-based — did model refuse the unrelated question? |
| Prompt reverse | Rule-based — yes/no consistency across pairs |
| Caption/context resistance | MQM delta: 1 - (MQM_drop / MQM_normal) |
| Visual degradation resistance | MQM delta under transforms |

### Contribution 5: Cross-Model Architecture Analysis
Systematic comparison across 7 models from 5 families to determine whether model family or parameter count better predicts adversarial robustness, admittance, and resistance.

---

## Expected Findings (What We Investigate)

These are hypotheses to test, not confirmed results.

### F1: Caption Bias
- Does removing caption improve or hurt description quality?
- Can models produce plausible descriptions without seeing the figure?
- Do existing benchmarks measure text comprehension rather than visual understanding?

### F2: Parametric Memory Overrides Visual When Visual Is Weak
- When visual signal is degraded (blurred, small, low quality), do models fall back to training data?
- Do models reproduce known dataset characteristics (e.g., IEMOCAP has 5 emotions) even when the image shows otherwise?
- What conditions trigger the switch from genuine visual reading to parametric recall?

### F3: The Counting-Reasoning Gap
- Do models show a gap between open-ended reasoning and precise counting?
- Is the gap format-dependent — does binary scoring reveal weaknesses that open-ended questioning hides?
- Does the gap extend to cross-panel scenarios?

### F4: Architecture vs Size
- Does model family predict robustness better than parameter count?
- Do smaller models from better architectures outperform larger models from weaker architectures?
- Is the honesty gap (admittance) architecture-dependent or size-dependent?

### F5: Genuine Visual Reading
- Can we prove models genuinely read figures through selective text manipulation?
- What happens when we blur specific labels — does the model fabricate or omit?
- How do responses differ between "can't see" and "won't admit"?

---

## Positioning Against Existing Work

| Paper | What they do | What we add |
|-------|-------------|-------------|
| CharXiv (NeurIPS 2024) | English charts, MC questions, desc vs reasoning gap | Multilingual, open-ended, format-dependent gap analysis |
| ChartHal (2025) | Hallucination on chart QA | Extended hallucination taxonomy (5 types) + admittance metric |
| ChartMuseum (NeurIPS 2025) | Visual vs textual reasoning gap | Caption bias investigation |
| See or Recall (2025) | No-image baseline for VQA | No-image baseline for description + parametric memory analysis |
| FUGU (2025) | Vision-language bottleneck diagnosis | Empirical confirmation via selective blur methodology |
| CALVI (EuroVis 2025) | Misleading chart detection | Misleading detection on scientific figures |
| CHARTNOISE (2025) | Prompt reverse inconsistency | Confirm/deny probes on multilingual scientific figures |
| ChartQAPro (2025) | Unanswerable questions | Unanswerable probes for figure description |

---

## Target Venue

**Primary:** ACL / EMNLP 2026
**Alternative:** NeurIPS 2026 Datasets & Benchmarks Track

**Strengths:**
1. Multilingual — underserved area
2. New metrics (admittance, resistance) — methodological contribution
3. Comprehensive framework — adversarial + capability in one
4. Cross-model architecture analysis — actionable for practitioners
5. Reproducible — open-source

---

## Evaluation Tiers

### Tier 1: Full Dataset (1,005 figures)
- 11 generator models × 4 judges
- Standard MQM evaluation
- Cross-judge agreement analysis

### Tier 2: Sample Analysis (120 figures)
- Caption ablation (image+caption vs image-only vs no-image)
- Validates Tier 1 baseline
- Human evaluation comparison subset

### Tier 3: Deep Probing (to be determined — balanced across languages and figure types)
- All adversarial strategies
- All capability benchmarks
- Cross-model comparison (7 models)
- Admittance and resistance measurement

---

## What's Needed

| Task | Priority |
|------|----------|
| Finalize adversarial sample selection and data preparation | High |
| Define formal admittance and resistance scoring formulas | High |
| Run all hallucination probes (5 types) across models | High |
| Run prompt reverse across models | High |
| Run misleading detection across models | High |
| Run caption ablation on 120 samples | High |
| Run all capability probes across models | High |
| Cross-model comparison and analysis | High |
| Dashboard updates | Medium |
| Write paper | High |
