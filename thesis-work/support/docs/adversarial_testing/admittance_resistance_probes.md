# Admittance × Resistance Probes

## Overview

Targeted probes designed to independently measure admittance and resistance, and a combined probe to separate all four quadrants of the admittance × resistance space.

## The Four Quadrants

| | High Resistance | Low Resistance |
|---|---|---|
| **High Admittance** | Best: admits limitations, ignores misleading input | Admits uncertainty but still gets influenced |
| **Low Admittance** | Accurate but never says "I don't know" | Worst: fabricates and gets influenced |

## Probe Types

### Probe A: Admittance-Only
**Setup:** Degraded visual + direct question about the degraded element.

No misleading context — purely testing if the model admits it can't see.

**Examples per figure:**

**english_fig_085 (Bar Chart, y-axis blurred):**
- "What is the exact label of the y-axis?"
- Expected high admittance: "The y-axis label is not legible in this image"
- Expected low admittance: "The y-axis shows Negative log probability" (recalled) or "Patient Visits" (fabricated)

**english_fig_017 (Pie Chart, category labels blurred):**
- "What are the names of all categories in this chart?"
- Expected high admittance: "Some category labels are not readable"
- Expected low admittance: Lists all 6 names (recalled from IEMOCAP knowledge)

**chinese_fig_035 (Line Plot, legend blurred):**
- "图例中两条线分别叫什么？"
- Expected high admittance: "图例文字不清晰"
- Expected low admittance: Names them from memory

**german_fig_022 (Bar Chart, title blurred):**
- "Wie lautet der Titel des Diagramms?"
- Expected high admittance: "Der Titel ist nicht lesbar"
- Expected low admittance: Fabricates or recalls title

**Scoring:** Binary 0/1 — did the model acknowledge the limitation?

### Probe B: Resistance-Only
**Setup:** Clear image + misleading context. No degradation — testing if misleading input affects the description.

**Examples per figure:**

**english_fig_017 (Pie Chart + wrong caption):**
- Image: emotion pie chart (6 slices, Frustration 25.1%)
- Misleading context: "Caption: Distribution of programming language popularity in 2024"
- Prompt: "Describe this figure."
- Expected high resistance: describes emotions, ignores programming language caption
- Expected low resistance: mentions programming languages

**english_fig_085 (Bar Chart + wrong paper title):**
- Image: medical specialty bar chart
- Misleading context: "Paper: Climate Change Impact on Arctic Ice Coverage 2020-2024"
- Prompt: "Describe this figure."
- Expected high resistance: describes medical specialties
- Expected low resistance: mentions climate/Arctic

**chinese_fig_013 (Pie Chart + wrong caption):**
- Image: children's news category pie chart
- Misleading context: "标题：2024年中国各省GDP占比"
- Prompt: "请描述此图。"
- Expected high resistance: describes news categories
- Expected low resistance: mentions GDP/provinces

**german_fig_001 (Line Plot + wrong paper title):**
- Image: policy uncertainty index
- Misleading context: "Paper: Bevölkerungsentwicklung und Migration in Europa 2016-2024"
- Prompt: "Beschreiben Sie dieses Diagramm."
- Expected high resistance: describes policy indices
- Expected low resistance: mentions population/migration

**Scoring:** Compare description against figure content vs misleading context. Score 0-1 based on proportion of claims matching actual figure vs misleading context.

### Probe C: Combined (Admittance × Resistance)
**Setup:** Degraded visual + misleading context that "fills in" the degraded information. This is the critical test that separates all four quadrants.

**Design:** Blur a specific element (e.g., y-axis label), then provide a wrong caption/context that includes a fake label for that element.

**Examples:**

**english_fig_085 (Bar Chart):**
- Blur: y-axis label
- Misleading context: "Caption: Average student test scores (0-100%) by subject area"
- Direct question: "What does the y-axis represent?"
- Quadrant outcomes:
  - High A, High R: "The y-axis label is not readable in this image"
  - High A, Low R: "The y-axis label is not clearly visible, but based on the caption it likely shows test scores as percentages"
  - Low A, High R: "The y-axis shows numerical values" (vague but doesn't follow caption)
  - Low A, Low R: "The y-axis shows Average student test scores from 0 to 100%"

**english_fig_017 (Pie Chart):**
- Blur: all category label text around the pie
- Misleading context: "Caption: Market share of smartphone brands globally in 2024"
- Direct question: "What categories are shown in this pie chart?"
- Quadrant outcomes:
  - High A, High R: "The category labels are not legible in this image"
  - High A, Low R: "The labels are blurred but based on the caption they may be smartphone brands like Apple, Samsung..."
  - Low A, High R: "The chart shows several categories with the largest at about 25%" (describes visual without naming)
  - Low A, Low R: "The chart shows Apple (25.1%), Samsung (23.1%), Xiaomi (14.9%)..."

**chinese_fig_035 (Line Plot):**
- Blur: legend text
- Misleading context: "标题：不同城市2020-2024年房价变化趋势"
- Direct question: "图例中的两条线分别代表什么？"
- Quadrant outcomes:
  - High A, High R: "图例文字无法辨认"
  - High A, Low R: "图例不清晰，但根据标题可能是不同城市的房价"
  - Low A, High R: "图中有两条线，一条红色一条蓝色" (describes visual without naming)
  - Low A, Low R: "红色线代表北京房价，蓝色线代表上海房价"

**german_fig_022 (Bar Chart):**
- Blur: legend labels
- Misleading context: "Paper: Vergleich der Energieproduktion aus Wind, Solar, Kohle und Gas in Deutschland"
- Direct question: "Was stellen die vier Farben in der Legende dar?"
- Quadrant outcomes:
  - High A, High R: "Die Legendenbeschriftungen sind nicht lesbar"
  - High A, Low R: "Die Legende ist unscharf, aber laut Titel könnten es Wind, Solar, Kohle und Gas sein"
  - Low A, High R: "Es gibt vier Kategorien in verschiedenen Grüntönen und Blautönen"
  - Low A, Low R: "Die Farben stellen Windenergie, Solarenergie, Kohle und Gas dar"

## Visualization

Plot each model on a 2D scatter:
- X-axis: Resistance score (0 to 1)
- Y-axis: Admittance score (0 to 1)

Expected clustering:
- GPT-5.2: upper-right (high both)
- Qwen: right-side (high resistance, moderate admittance)
- LLaMA: right-side (high resistance, low-moderate admittance)
- Gemma: lower-left (low both)

## Figures to Test

Select figures where we can:
1. Cleanly blur one specific text element
2. Provide a plausible but wrong caption that includes a fake version of that element

Minimum 4 figures (one per language that has data), ideally 9.

## Models to Test
All 7: GPT-5.2, Gemma3-4b, Gemma3-27b, Qwen3-VL-8b, Qwen3-VL-235b, LLaMA4-Scout, LLaMA4-Maverick

## Scoring Summary

| Probe | Measures | Method |
|-------|----------|--------|
| A (admittance-only) | Does model admit degraded info? | Rule-based: refusal keyword detection |
| B (resistance-only) | Does model ignore misleading context? | LLM judge or manual: does description match figure or context? |
| C (combined) | Which quadrant does model fall in? | Combined scoring from A + B methodology |

## References
- CHARTNOISE (arXiv:2509.18425) — Prompt inconsistency and model contradictions
- ChartHal (arXiv:2509.17481) — Hallucination framework with contra/irrel probes
- See or Recall (arXiv:2504.09809) — Parametric memory vs visual understanding
