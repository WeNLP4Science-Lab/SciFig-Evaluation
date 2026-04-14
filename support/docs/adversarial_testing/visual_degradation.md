# Visual Degradation & Text Manipulation

## Overview

Tests model robustness through deliberate image degradation, text obfuscation, and visual manipulation. These are adversarial because we intentionally modify images to challenge the model.

## Experiments

### 1. Image Degradation Transforms
**30 adversarial samples × 5 transforms**

| Transform | What it does | GPT-5.2 Impact | Gemma3-4b Impact |
|-----------|-------------|----------------|------------------|
| JPEG compression (q=15) | Block artifacts | Minimal (-9.4% length) | Paradoxically helped (+352 chars) |
| Noise (sigma=30) | Gaussian noise overlay | Moderate (-6.2% length) | Content loss, structural errors |
| Grayscale | Remove all color | Mild (-3.3% length) | Devastating (-17 MQM points) |
| Aspect ratio (1.2x stretch) | Horizontal distortion | Minimal | Moderate confusion |
| Low contrast (50%) | Faded appearance | Minimal | Moderate |

**Key finding:** GPT-5.2 is resilient to all transforms. Small models (Gemma3-4b) are fragile, especially to grayscale (color-dependent understanding).

### 2. Axis Blur (Margin Text Removal)
**9 samples × 7 models**

Blur bottom 15% (x-axis), left 15% (y-axis), top 12% (title/legend) of the image.

**Honesty rate (admitting text is unreadable):**
| Model | Rate |
|-------|------|
| GPT-5.2 | 67% (2/3) |
| Qwen3-VL-235b | 11% (1/9) |
| Qwen3-VL-8b | 11% (1/9) |
| LLaMA4-Scout | 11% (1/9) |
| LLaMA4-Maverick | 0% (0/9) |
| Gemma3-27b | 0% (0/9) |
| Gemma3-4b | 0% (0/9) |

**Key finding:** Only GPT-5.2 consistently admits when text is unreadable. All other models fabricate axis labels. Gemma3-4b invented "Patient Visits 0-100" for a negative log probability chart.

### 3. Single-Label Blur (Memorization Test)
**multi_fig_002, 3 tests — blur one x-axis label at a time**

Blurred 10%, 50%, or 80% label individually. GPT-5.2 still mentioned the blurred value — but this is logical inference from the pattern (10% increments), not memorization.

### 4. Legend/Title Blur (Genuine Reading Test)
**multi_fig_002, 4 tests — blur legend, y-axis title, x-axis title, all three**

| What was blurred | Per-Output | Per-Layer | Perplexity | Sparsity |
|------------------|-----------|-----------|------------|----------|
| Legend | **NO** | YES* | YES | YES |
| Y-axis title | YES | YES | **NO** | YES |
| X-axis title | YES | YES | YES | **NO** |
| All three | **NO** | YES* | **NO** | **NO** |

**Key finding:** GPT-5.2 is genuinely reading, not memorizing. When text is unreadable, it doesn't fill in from training knowledge — it describes what's visible and omits what's not. This proves genuine visual reading capability.

### 5. Figure-Blurred Page (Honesty Test)
**2 figures × 7 models — figure unreadable on paper page, surrounding text visible**

| Model | Behavior when figure is blurred |
|-------|-------------------------------|
| GPT-5.2 | Says "obscured" / "不清晰" — admits it can't see |
| Gemma3-4b | Describes Table 1 data AS the pie chart |
| Gemma3-27b | Also hallucinates — same pattern as 4b |
| Qwen3-VL-8b | Infers from caption text |
| Qwen3-VL-235b | Mostly cautious |
| LLaMA4-Scout | Fabricates values |
| LLaMA4-Maverick | Fabricates values |

### 6. Misplaced Figure (Text Influence Test)
**2 figures × 7 models — figure placed on wrong page of same paper**

| Model | Influenced by surrounding text? |
|-------|-------------------------------|
| GPT-5.2 | No — focused on actual figure |
| Qwen3-VL-235b | No |
| Qwen3-VL-8b | No |
| LLaMA4-Maverick | No |
| LLaMA4-Scout | No |
| Gemma3-27b | **Yes** — "speaker anonymization performance", "CemuSTC" |
| Gemma3-4b | **Yes** — mixed page text into figure description |

**Key finding:** Only Gemma models get influenced by surrounding text on the page. All other model families focus on the actual figure regardless of page context.

## Stored Results
- `new_adversarial_strategies/axis_blurred/results/` — Axis blur MQM results
- `new_adversarial_strategies/multi_model_comparison/axis_blurred_all_models.json` — All models axis blur
- `new_adversarial_strategies/gemma_transforms/` — Gemma transform results
- `new_adversarial_strategies/figure_blurred_pages/` — Figure-blurred page images
- `new_adversarial_strategies/misplaced_figure/results.json` — Misplaced figure results
