# Descriptive Capability

## Overview

Tests the model's ability to READ and extract information directly visible in the figure. No inference, computation, or reasoning required — just accurate visual reading.

---

## Subtypes

### D1. Numerical Value Reading
**Status:** ✅ Done

Read labeled/annotated values directly from the figure.

**Setup:** 9 figures × 1 easy question each = 9 questions.

**GPT-5.2 Result: 100% (9/9)**

| Figure | Question | Expected | Got |
|--------|----------|----------|-----|
| eng_017 | Frustration percentage? | 25.1% | 25.1% ✓ |
| chi_035 | Red line at A1? | 3.254 | 3.254 ✓ |
| chi_004 | Right y-axis max? | 6000 | 6000 ✓ |
| ger_022 | Welt-BIP 2000er? | 3.9% | 3.9% ✓ |
| ger_057 | Sport/Erholung 2021? | 3.6% | 3.6% ✓ |
| ... | ... | ... | All correct |

**Finding:** GPT-5.2 reads labeled values perfectly across all languages.

### D2. Chart Element Identification (CharXiv Templates)
**Status:** ✅ Done

Adapted from CharXiv's 19 descriptive question templates.

**Question types tested:**
| QID | Question | Type |
|-----|----------|------|
| 1 | What is the title? | title/ocr |
| 2-3 | Axis labels? | ocr |
| 4-7 | Tick values (leftmost, rightmost, lowest, highest)? | ocr |
| 8-9 | Tick interval? | quant |
| 10 | How many lines? | quant |
| 11 | Do lines intersect? | bool |
| 12-13 | Legend labels and count? | quant/ocr |
| 16 | General trend? | pattern |
| 17 | Total labeled ticks? | quant |
| 18-19 | Subplot layout and count? | quant |

**GPT-5.2 Result: 78% (22/28)**

**Failures:**
- Title: said "Frustration" instead of "Not Applicable" (pie chart has no title)
- X-axis label: said "Layer1-4" instead of "Not Applicable" (has tick labels but no axis title)
- Legend: said "6" instead of "Not Applicable" (labels on slices, not legend)
- Subplot layout: format mismatch ("1 row × 2 columns" vs "1 by 2")
- Chinese bool: said "没有" — correct meaning but didn't match "No" string

### D3. Other Subtypes — PLANNED
Future descriptive subtypes to explore:
- Color identification accuracy
- Spatial relationship reading (which element is above/below/left/right)
- Text extraction from annotations/callouts
- Scale type identification (linear vs log)

---

## Cross-Model Comparison (Descriptive)

Only GPT-5.2 tested so far on formal descriptive probes. From informal observations across experiments:

| Model | Value Reading | Element ID | Notes |
|-------|-------------|-----------|-------|
| GPT-5.2 | Excellent | Good (78%) | Occasionally confused by "Not Applicable" cases |
| Gemma3-4b | Poor | Poor | Fabricates axis labels when blurred |
| Qwen3-VL-235b | Good | — | Honest about unreadable text |

## Stored Results
- `new_adversarial_strategies/numerical_precision/gpt52_results.json` (easy questions)
- `new_adversarial_strategies/charxiv_style/gpt52_results.json` (descriptive subset)
- `new_adversarial_strategies/reasoning_vs_descriptive/gpt52_results.json` (descriptive subset)

## References
- CharXiv (arXiv:2406.18521) — 19 descriptive question templates, 84.5% GPT-4o baseline
