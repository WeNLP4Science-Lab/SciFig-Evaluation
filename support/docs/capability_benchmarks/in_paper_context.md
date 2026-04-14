# In-Paper Page Context Benchmark

## Overview

Tests whether models can describe a figure when it appears on a real paper page with surrounding text, tables, and other visual elements. This is a legitimate real-world scenario — users often send full pages rather than cropped figures.

## Setup

Extracted PDF pages containing target figures from source papers. Verified matches manually (33 out of 88 confirmed correct page-figure matches across English, Chinese, German, and Multilingual papers).

## Experiments

### Clean Image vs In-Paper Page (GPT-5.2)
**5 English figures tested:**

| Figure | Clean MQM | In-Paper MQM | Diff |
|--------|-----------|-------------|------|
| english_fig_017 | 90.0 | 87.0 | -3.0 |
| english_fig_033 | 91.5 | 88.0 (approx) | -3.5 |
| english_fig_085 | 68.5 | ~66.5 | -2.0 |
| english_fig_038 | — | Good | — |
| english_fig_057 | — | Good | — |

**GPT-5.2 finding:** Minimal performance drop. Correctly identifies target figure, uses surrounding text to enrich description (e.g., reads dataset name "IEMOCAP" from page context).

### Multi-Model In-Paper Page Comparison
**2 figures × 7 models:**

| Model | english_fig_017 (Pie) | chinese_fig_014 (Line) |
|-------|----------------------|----------------------|
| GPT-5.2 | ✓ Perfect — 6 slices, all correct | ✓ Perfect — 2 subplots, correct values |
| Qwen3-VL-235b | ✓ Perfect | ✓ Perfect |
| LLaMA4-Maverick | ✓ Perfect | ✓ Good, accurate values |
| LLaMA4-Scout | ✓ Perfect | ✓ Good |
| Qwen3-VL-8b | 5 slices (minor) | ✓ Correct |
| Gemma3-27b | ✓ Correct | ✗ Wrong topic, single chart |
| Gemma3-4b | ✗ 11 slices (mixed table data) | ✗ Fabricated topic, wrong values |

### Gemma3-4b In-Paper Page Comparison (5 figures)
| Figure | Clean | In-Paper | Diff |
|--------|-------|----------|------|
| english_fig_033 | 55.0 | 57.0 | +2.0 |
| english_fig_017 | 91.5 | 74.5 | -17.0 |
| german_fig_009 | 51.5 | 70.0 | +18.5 |
| german_fig_033 | 53.5 | 74.0 | +20.5 |
| chinese_fig_014 | 83.0 | 66.5 | -16.5 |

**Small model finding:** Volatile — sometimes page context helps (German), sometimes it hurts (English pie chart, Chinese line plot). Large models are more consistent.

## Key Findings

1. **Figure localization is a capability gap** — small models (Gemma3-4b) cannot isolate the target figure from page clutter even when told "describe Figure 2"
2. **Page context can help large models** — GPT-5.2 uses surrounding text to add context (dataset names, methodology details)
3. **Page context confuses small models** — Gemma3-4b counted 11 slices by mixing Table 1 data into pie chart description
4. **IEMOCAP "5 slices" bias confirmed** — multiple models say 5 instead of 6, suggesting training data overrides visual evidence

## Stored Results
- `adversarial_dataset/matched.json` — Verified page-figure matches
- `new_adversarial_strategies/gemma_transforms/page_results.json` — Gemma in-paper results
- `new_adversarial_strategies/multi_model_comparison/results.json` — Multi-model results
- `new_adversarial_strategies/multi_model_comparison/llama_results.json` — LLaMA results
