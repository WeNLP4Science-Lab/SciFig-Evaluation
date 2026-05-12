# Prompt Reverse Inconsistency

## Overview

Tests whether a model's understanding of a figure is stable or whether it flips based on question framing. Inspired by the CHARTNOISE paper (arXiv:2509.18425) which found models contradict themselves when asked to confirm vs deny the same statement.

## Methodology

For each figure, create **confirm/deny pairs** — two statements about the same visual fact, one true and one false. A grounded model should say Yes to the true one and No to the false one. An ungrounded model will agree with both.

## Scoring

| Response Pattern | Score | Meaning |
|-----------------|-------|---------|
| Confirm true + Deny false | 1.0 | Grounded — stable understanding |
| Deny both | 0.5 | Overly cautious but not contradictory |
| Confirm both | 0.0 | **Ungrounded — agrees with anything** |
| Confirm false + Deny true | 0.0 | **Wrong understanding** |

## Probes (9 figures × 3 pairs = 27 pairs)

### english_fig_003 (Line Plot)
**Pair 1 — Line count:**
- TRUE: "Does this figure contain exactly 5 lines?"
- FALSE: "Does this figure contain exactly 3 lines?"

**Pair 2 — Baseline behavior:**
- TRUE: "Is the dashed baseline line flat at approximately 0%?"
- FALSE: "Does the dashed baseline line show a clear downward trend?"

**Pair 3 — Worst layer group:**
- TRUE: "Do most lines show their lowest values at Layer5-12?"
- FALSE: "Do most lines show their lowest values at Layer29-32?"

### english_fig_017 (Pie Chart)
**Pair 1 — Slice count:**
- TRUE: "Does this pie chart have exactly 6 slices?"
- FALSE: "Does this pie chart have exactly 5 slices?"

**Pair 2 — Largest category:**
- TRUE: "Is Frustration the largest category in this chart?"
- FALSE: "Is Happiness the largest category in this chart?"

**Pair 3 — Percentage check:**
- TRUE: "Is Neutral approximately 23.1%?"
- FALSE: "Is Neutral approximately 35%?"

### english_fig_085 (Bar Chart)
**Pair 1 — Group count:**
- TRUE: "Are there exactly 6 specialty groups on the x-axis?"
- FALSE: "Are there exactly 4 specialty groups on the x-axis?"

**Pair 2 — Baseline position:**
- TRUE: "Does the baseline (light blue) bar have the most negative value in each group?"
- FALSE: "Does the baseline (light blue) bar have the least negative value in each group?"

**Pair 3 — Y-axis direction:**
- TRUE: "Does the y-axis show negative values (below zero)?"
- FALSE: "Does the y-axis range from 0 to 30?"

### chinese_fig_013 (Pie Chart)
**Pair 1 — Slice count:**
- TRUE: "图中是否有8个切片？"
- FALSE: "图中是否有5个切片？"

**Pair 2 — Largest category:**
- TRUE: "科学是否是占比最大的类别？"
- FALSE: "经济是否是占比最大的类别？"

**Pair 3 — Specific value:**
- TRUE: "体育类别是否占约4%？"
- FALSE: "体育类别是否占约20%？"

### chinese_fig_035 (Line Plot)
**Pair 1 — Line relationship:**
- TRUE: "蓝色线是否始终在红色线之上？"
- FALSE: "两条线是否在某个点交叉？"

**Pair 2 — Trend direction:**
- TRUE: "两条线是否从B1之后总体呈上升趋势？"
- FALSE: "两条线是否从A1到母语总体呈下降趋势？"

**Pair 3 — Value at point:**
- TRUE: "红色线在A1处的值是否约为3.254？"
- FALSE: "红色线在A1处的值是否约为5.0？"

### chinese_fig_004 (Bar Chart)
**Pair 1 — Axis count:**
- TRUE: "图表是否使用了两个y轴？"
- FALSE: "图表是否只使用了一个y轴？"

**Pair 2 — Data type:**
- TRUE: "图中是否同时包含柱状图和折线图？"
- FALSE: "图中是否只包含折线图？"

**Pair 3 — Time range:**
- TRUE: "数据是否覆盖2022年7月到8月？"
- FALSE: "数据是否覆盖2023年1月到12月？"

### german_fig_001 (Line Plot)
**Pair 1 — Axis count:**
- TRUE: "Hat das Diagramm zwei y-Achsen (links und rechts)?"
- FALSE: "Verwenden alle drei Linien dieselbe y-Achse?"

**Pair 2 — Peak event:**
- TRUE: "Zeigen alle drei Linien einen Anstieg um 2020?"
- FALSE: "Sind alle drei Linien zwischen 2016 und 2024 durchgehend stabil?"

**Pair 3 — Line count:**
- TRUE: "Enthält das Diagramm genau 3 Linien?"
- FALSE: "Enthält das Diagramm genau 5 Linien?"

### german_fig_022 (Bar Chart)
**Pair 1 — Negative values:**
- TRUE: "Gibt es negative Werte im Diagramm?"
- FALSE: "Sind alle Werte im Diagramm positiv?"

**Pair 2 — Decade count:**
- TRUE: "Werden genau 3 Jahrzehnte dargestellt?"
- FALSE: "Werden genau 5 Jahrzehnte dargestellt?"

**Pair 3 — Highest category:**
- TRUE: "Hat der Welthandel den höchsten Wert in den 2000er Jahren?"
- FALSE: "Hat die Industrieproduktion den höchsten Wert in den 2000er Jahren?"

### german_fig_057 (Pie Chart)
**Pair 1 — Ring count:**
- TRUE: "Besteht das Diagramm aus zwei Ringen (2014 und 2021)?"
- FALSE: "Besteht das Diagramm aus drei Ringen?"

**Pair 2 — Largest segment:**
- TRUE: "Ist 'Übrige' das größte Segment im äußeren Ring?"
- FALSE: "Ist 'Kultur' das größte Segment im äußeren Ring?"

**Pair 3 — Legend presence:**
- TRUE: "Werden die Kategorien direkt am Diagramm beschriftet (keine separate Legende)?"
- FALSE: "Gibt es eine separate Legende neben dem Diagramm?"

## Expected Findings

Based on CHARTNOISE findings:
- Models likely agree with both true AND false statements 20-40% of the time
- Numerical claims (percentages, counts) may be more stable than qualitative claims (trend direction)
- Smaller models likely less grounded than frontier models
- IEMOCAP slice count (5 vs 6) is a known bias point — models may agree with "5 slices" despite seeing 6

## Models to Test
All 7 models: GPT-5.2, Gemma3-4b, Gemma3-27b, Qwen3-VL-8b, Qwen3-VL-235b, LLaMA4-Scout, LLaMA4-Maverick

## References
- CHARTNOISE / "Losing the Plot" (arXiv:2509.18425) — Prompt reverse inconsistency finding
