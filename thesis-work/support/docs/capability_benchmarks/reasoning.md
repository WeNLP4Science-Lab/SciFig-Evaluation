# Reasoning Capability

## Overview

Tests the model's ability to THINK about chart data — requiring inference, computation, comparison, or judgment beyond what is directly readable. This is where models show the largest performance gaps.

---

## Subtypes

### R1. Numerical Computation
**Status:** ✅ Done

Arithmetic on values read from the figure.

**Medium (simple arithmetic on 2 values):**
- "Combined percentage of Anger and Sadness?" → 14.9 + 14.7 = 29.6%
- "How much did blue line rise from B1 to 母语?" → 5.204 - 4.030 = 1.174

**Hard (multi-step computation):**
- "Ratio of largest to smallest slice?" → 21% ÷ 2% = 10.5x
- "Smallest gap between two lines and where?" → B1, 4.030 - 3.179 = 0.851

**GPT-5.2 Results:**
| Difficulty | Score |
|------------|-------|
| Medium | 78% (7/9) |
| Hard | 78-89% (7-8/9) |

**Failures:** Dense overlapping line charts cause approximate reading errors that cascade into wrong computations.

### R2. Visual Counting
**Status:** ✅ Done

Scan visual elements and count those meeting a condition. The fundamental weakness of all VLMs.

**Single-panel counting (CharXiv Number-in-General style):**
- "How many lines have value below -5%?" → 2
- "How many individual bars total?" → 42
- "How many categories below 10%?" → 3

**Cross-panel counting:**
- "How many bars > 20% across both panels?" → 4
- "How many line crossings across both panels?" → 0
- "For how many metal-year combos does DE > EU?" → 3

**GPT-5.2 Results:**
| Experiment | Score |
|------------|-------|
| Single-panel counting | **44%** (8/18) |
| Cross-panel counting | **61%** (11/18) |

**Error patterns:**
| Type | Frequency | Example |
|------|-----------|---------|
| Overcounting | Most common | Expected 3, got 4 or 6 |
| Severe undercounting | Common | Expected ~10-15, got 2 |
| Boundary miscounting | Occasional | ">14%" — counted 14.1% as qualifying |
| Fabricated elements | Rare but severe | Said 2 line crossings when there are 0 |

**Root cause (architectural):**
1. ViT patch embeddings compress away spatial precision for individuation
2. CLIP contrastive training never incentivizes counting
3. Vision-language handoff loses coordinate information (FUGU paper)
4. Models use OCR text pathway, not geometric visual pathway
5. System 1 pattern matching replaces System 2 deliberate counting

### R3. Open-Ended Reasoning
**Status:** ✅ Done

Free-form questions requiring comparison, trend analysis, inference, or interpretation.

**Question types:**
| Type | Example |
|------|---------|
| Comparison | "Which specialty benefits most from fine-tuning?" |
| Arithmetic | "Do negative emotions outweigh positive? By how much?" |
| Trend analysis | "Do the two lines show similar trends?" |
| Inference | "Which emotion would have worst classification accuracy?" |
| Interpretation | "What event caused the 2020 spike?" |
| Cross-reference | "Does same-specialty fine-tuning always win?" |

**GPT-5.2 Result: 89% (~16/18)**

Failures were minor — misidentified most stable configuration, debatable claim about news leading cases.

### R4. Cross-Panel Reasoning
**Status:** ✅ Done

Questions requiring integration of information from multiple sub-plots.

**Open-ended cross-panel:** GPT-5.2 at **89-94%** (16-17/18)
- Correctly reads values from both panels
- Computes differences accurately
- Draws valid conclusions

**Binary-scored cross-panel counting:** GPT-5.2 at **61%** (11/18)
- Drops when precise counting is required across panels

### R5. Other Subtypes — PLANNED
Future reasoning subtypes to explore:
- Extrapolation ("Based on the trend, what would happen at x=10?")
- Counterfactual reasoning ("If the blue values were doubled...")
- Anomaly detection ("Is there anything unusual in this data?")
- Causal reasoning ("What might explain the dip at Layer5-12?")

---

## The Format Effect

The same model on the same charts shows dramatically different performance depending on response format:

```
Open-ended reasoning:       89%  ██████████████████████
Cross-panel open reasoning: 89%  ██████████████████████
Numerical computation:      78%  ████████████████████
Cross-panel counting:       61%  ███████████████
Single-panel counting:      44%  ███████████
```

**Key insight:** When models can reason freely in text, they perform well (89%). When forced to give a precise count or exact number, they collapse (44%). This suggests the reasoning capability exists but the precise visual extraction pipeline is broken.

---

## Cross-Model Comparison

| Model | Open Reasoning | Counting | Notes |
|-------|---------------|----------|-------|
| GPT-5.2 | 89% | 44% | Strong reasoning, weak counting |
| Others | — | — | Planned |

## The Gap

| Benchmark | Descriptive | Reasoning | Gap |
|-----------|------------|-----------|-----|
| CharXiv GPT-4o | 84.5% | 47.1% | 37pts |
| Our GPT-5.2 (open-ended) | ~100% | 89% | 11pts |
| Our GPT-5.2 (binary-scored) | 78% | 44% | 34pts |

The gap is **format-dependent**: open-ended questioning closes the gap to 11 points, but binary-scored exact-match restores the full 34-point gap seen in CharXiv.

## Stored Results
- `new_adversarial_strategies/numerical_precision/gpt52_results.json`
- `new_adversarial_strategies/charxiv_style/gpt52_results.json`
- `new_adversarial_strategies/reasoning_vs_descriptive/gpt52_results.json`
- `new_adversarial_strategies/cross_panel_reasoning/gpt52_results.json`
- `new_adversarial_strategies/cross_panel_counting/gpt52_results.json`

## References
- CharXiv (arXiv:2406.18521) — Descriptive vs reasoning gap benchmark
- ChartMuseum (arXiv:2505.13444) — Visual vs textual reasoning gap
- FUGU (arXiv:2510.21740) — Vision-language handoff bottleneck
- QVLM (arXiv:2601.13401) — Code generation approach to bypass counting
- Chart-HQA (arXiv:2503.04095) — Hypothetical/counterfactual reasoning
