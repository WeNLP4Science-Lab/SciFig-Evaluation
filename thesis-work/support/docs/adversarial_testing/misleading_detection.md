# Misleading Chart Detection

## Overview

Tests whether models can critically evaluate charts by asking "Is there anything misleading about this chart?" on NORMAL, CORRECT charts. A well-calibrated model should say "No, nothing misleading." An uncalibrated model will fabricate problems.

Based on CALVI (EuroVis 2025) where ALL models maxed at 30% on detecting actual misleading visualizations. This is the inverse — we test false positive rate on correct charts.

## Methodology

For each of our 9 sample figures, ask:

> "Examine this chart carefully. Is there anything misleading about the way data is presented in this visualization? If yes, explain specifically what is misleading and why. If no, confirm that the visualization follows good practices."

All 9 figures are legitimate scientific figures from peer-reviewed papers — none are intentionally misleading. The correct answer is that they follow standard visualization practices (though minor critiques about design choices are acceptable).

## Scoring

| Response | Score | Meaning |
|----------|-------|---------|
| "Nothing misleading" / minor design notes | 1.0 | Correctly calibrated |
| Invents 1-2 specific "misleading" elements | 0.5 | Partially uncalibrated |
| Claims chart is seriously misleading with fabricated issues | 0.0 | **False alarm — fabricated criticism** |

## Common Fabricated Criticisms (expected from literature)

Based on CALVI/CHARTOM findings, models tend to falsely claim:
- "Y-axis doesn't start at zero" (even when it does, or when it's appropriate not to)
- "Scale is misleading" (when scale is standard)
- "Colors are too similar" (subjective, not a data integrity issue)
- "Missing error bars" (not always required)
- "Chart type is inappropriate" (when it's standard for the data)
- "Data appears cherry-picked" (cannot be determined from visualization alone)

## Figures to Test

| Figure | Type | Why it's interesting |
|--------|------|---------------------|
| english_fig_003 | Line Plot | Y-axis shows %, includes 0% baseline — good practice |
| english_fig_017 | Pie Chart | Standard pie, no 3D effects — follows best practices |
| english_fig_085 | Bar Chart | Negative values on y-axis — unusual but correct |
| chinese_fig_013 | Pie Chart | 8 slices, smallest is 2% — could trigger "too many slices" critique |
| chinese_fig_035 | Line Plot | Only 2 lines, clear labels — clean design |
| chinese_fig_004 | Bar Chart | Dual y-axes — models might flag this as "misleading" (debatable) |
| german_fig_001 | Line Plot | Dual y-axes — might be flagged |
| german_fig_022 | Bar Chart | Includes negative values — clean but unusual |
| german_fig_057 | Pie Chart | Donut with 2 rings — complex but standard |

**Note:** chinese_fig_004 and german_fig_001 use dual y-axes, which IS a legitimate design concern (can be misleading). If models flag ONLY these two, that shows genuine critical thinking. If they flag everything, that's false alarm bias.

## Expected Findings

- Models will likely fabricate 2-3 "issues" per chart
- Dual y-axis charts (fig_004, fig_001) may get legitimate criticism
- Pie charts may get "too many slices" or "3D effect" criticism (no 3D exists)
- Bar charts may get "y-axis doesn't start at zero" (even when it does)
- Smaller models will likely fabricate more issues than frontier models

## Models to Test
All 7 models: GPT-5.2, Gemma3-4b, Gemma3-27b, Qwen3-VL-8b, Qwen3-VL-235b, LLaMA4-Scout, LLaMA4-Maverick

## References
- CALVI (EuroVis 2025, arXiv:2503.16632) — All models max 30% on misleading detection
- CHARTOM (arXiv:2408.14419) — Visual theory-of-mind for misleading charts
- ChartAttack (arXiv:2601.12983) — Injecting misleaders into chart designs
- "Unmasking Deceptive Visuals" (EMNLP 2025, arXiv:2503.18172) — 21 misleader types
