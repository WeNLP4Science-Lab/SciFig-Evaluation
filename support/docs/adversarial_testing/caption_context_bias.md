# Caption & Context Bias Testing

## Overview

Tests whether models rely on text context (paper title, caption) instead of actually reading the figure. Inspired by the "See or Recall" paper (arXiv:2504.09809).

## Key Discovery

Our generation pipeline was sending `Paper: {title}\nCaption: {caption}` alongside images to all 11 generator models. The system prompt never asks for this — it only says "describe what is visually shown." This means all existing generation outputs may be biased by caption text.

## Experiments

### 1. Caption Ablation (3 conditions)
**9 samples, GPT-5.2, judged by GPT-4o (Azure)**

| Condition | Avg MQM | What model receives |
|-----------|---------|---------------------|
| Original (image + caption) | 78.6 | Image + paper title + caption |
| Image only | **82.3** | Image only, no text |
| No image (caption only) | 78.0* | Caption + title, no image |

*No-image scores unreliable — includes refusals and fabrications scored by MQM

**Finding:** Image-only scored HIGHER. Captions can bias and hurt performance.

### 2. Caption Mismatch (wrong caption)
**9 samples, GPT-5.2**

Gave each figure a caption from a different figure of the same type.

**Avg MQM: 76.8** (vs 82.3 image-only)

GPT-5.2 mostly ignored wrong captions but some figures were affected. english_fig_085 dropped to 33.0 on first run (judge variance issue — reruns at temp=0 gave 63.0).

### 3. No-Image Content Analysis
Detailed review of what the model produces without seeing the figure:

- **english_fig_017** (pie chart): Fabricated wrong slice count (5 not 6), wrong percentages, wrong categories — but knew IEMOCAP is an emotion dataset from training data
- **english_fig_085** (bar chart): Paraphrased caption with zero specific visual details — scored 83.0 MQM because it made no falsifiable claims

**Key insight:** MQM has a precision-recall asymmetry — it penalizes errors but not vagueness. A description that says nothing specific scores higher than one that attempts specifics and gets some wrong.

## Stored Results
- `new_adversarial_strategies/image_only/results.json` — Image-only generation outputs
- `new_adversarial_strategies/image_only/mqm_comparison.json` — MQM scores for image-only vs original
- `new_adversarial_strategies/no_image/results.json` — No-image generation outputs
- `new_adversarial_strategies/caption_mismatch/results/mqm_results.json` — Wrong caption results
