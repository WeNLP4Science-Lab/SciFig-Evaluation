# Inductance Probe Design — References & Strategies

## Key References

### Chart Reasoning Benchmarks
- **ChartQA** (Masry et al., ACL Findings 2022) — "visual" vs "logical" questions; logical = multi-step arithmetic/comparison
- **PlotQA** (Methani et al., AAAI 2020) — "Is the sum of X greater than Y?" cross-element derived comparison
- **Chart-HQA** (ACM MM 2025) — Hypothetical "what if" counterfactual questions on charts
- **Misleading ChartQA** (arXiv 2503.18172, 2025) — 21 misleader types, 3,026 examples; deception detection
- **MultiChartQA** (NAACL 2025) — Cross-chart reasoning requiring multi-image inference
- **ChartBench** (Xu et al., 2024) — Open-ended + binary across 42 chart types

### Perceptual Science
- **Cleveland & McGill** (JASA, 1984) — Perceptual accuracy ranking: position > length > angle > area > volume
- **Heer & Bostock** (CHI 2010) — Crowdsourced replication confirming perceptual biases

### Reasoning & Paradoxes
- **Kievit et al.** (Frontiers in Psychology, 2013) — Simpson's Paradox practical guide with detection markers
- **Survey of Inductive Reasoning for LLMs** (arXiv 2510.10182, 2025) — Rule induction, hypothesis testing, analogical transfer

### VLM Failures
- **"VLMs Need Words"** (arXiv 2604.02486, 2025) — Models anchor on semantic labels over visual evidence
- **"Unmasking Deceptive Visuals"** (EMNLP 2025) — No open-source model detects axis inversion
- **Pandey et al.** (CGF 2025) — VLMs fail on standardized visualization literacy tests

## Actionable Question Design Strategies

### 1. Contradiction Probes (our en213 pattern)
Chart shows X but surface interpretation suggests not-X. Model must compute to discover the truth.
- Example: "Correct % drops" but precision improves

### 2. Simpson's Paradox Probes (NEW — to find)
Aggregate trend contradicts subgroup trends. Ask about the overall trend, correct answer requires checking subgroups.
- Need: charts where overall average moves one way but subgroups move the other

### 3. Counterfactual Probes (from Chart-HQA)
"If this value were 20% higher, would the conclusion change?"
- Forces computation rather than pattern matching

### 4. Cross-Element Derived Comparison (from PlotQA)
"Is the sum of X greater than Y?" — requires reading multiple values and computing
- Our bg095 is this pattern

### 5. Hypothesis Testing (from reasoning taxonomy)
Present a claim about the chart. Model must evaluate with evidence.
- Our en166 and en213 use this pattern (student vs professor, defend vs disagree)

### 6. Deception Detection (from Misleading ChartQA)
"Is this chart misleading? If so, how?"
- Tests meta-reasoning about chart design itself

### 7. Text-Visual Conflict (from "VLMs Need Words")
Caption says one thing, chart shows another. Which does the model follow?
- Related to our Resistance metric (caption bias)

## Priority for New Probes
1. Find Simpson's Paradox examples in our dataset
2. Design counterfactual questions on existing figures
3. Create hypothesis-testing questions with competing claims (like en166/en213)
