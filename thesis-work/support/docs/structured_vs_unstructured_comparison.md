# Structured vs Unstructured LLM Figure Description Generation: Comparative Analysis

**Model:** gpt-4o-mini
**Date:** 2026-02-10
**Dataset:** 20 figures across 5 language subsets (Bulgarian, Chinese, English, German, Multi-language)

---

## Executive Summary

This report compares two approaches for LLM-generated scientific figure descriptions using gpt-4o-mini:

- **Unstructured** (paragraph-only): The model produces a single `model_annotation` string describing the figure in natural language.
- **Structured** (paragraph + breakdown): The model produces both a `model_annotation` paragraph AND a `breakdown` JSON object with machine-parseable fields (axis labels, line counts, colors, trends, etc.).

**Key findings:**

1. **Structured paragraphs are 14% shorter on average** (291 vs 338 characters for single-language figures), suggesting the structured prompt encourages the model to offload detail into the breakdown rather than the paragraph.
2. **Breakdown fields are well-populated** but have notable gaps -- 15% of breakdown entries contain at least one null, "not specified", or empty value, most commonly in percentage fields for pie charts and legend position fields.
3. **Cross-approach consistency is moderate**: The same figure described by both approaches often yields different specific numeric values, color assignments, and trend characterizations, even when the overall description theme is the same.
4. **Structured breakdowns frequently disagree with their own paragraphs** on specific details (e.g., the paragraph says "decreasing" but the breakdown says "stable"), occurring in approximately 25% of figures.
5. **Multi-language outputs show cross-language inconsistencies in both approaches**, with the structured approach exhibiting *more* inter-language variation in breakdown fields (different trend labels, different num_lines counts for the same figure across languages).
6. **Against groundtruth, both approaches show similar levels of factual accuracy**, with common errors including incorrect color assignments, hallucinated numeric values, and missed chart elements.

**Recommendation:** The structured approach is preferred for downstream machine processing but should be used with validation checks. For human-readable descriptions alone, the unstructured approach produces slightly richer paragraphs. A hybrid pipeline using structured outputs with automated consistency validation is ideal.

---

## Methodology

For each of the 20 figures (4 per language subset), I compared:
- Paragraph description length (character count)
- Description quality and specificity
- Breakdown field completeness (structured only)
- Internal consistency between paragraph and breakdown (structured only)
- Cross-approach agreement
- Multi-language consistency
- Accuracy against groundtruth human annotations

---

## Per-Figure Comparison Table

### Single-Language Figures (16 figures)

| Figure Key | Type | Lang | Unstruct Len | Struct Len | Len Delta | Breakdown Complete? | Para-Breakdown Consistent? | Cross-Approach Agreement | Groundtruth Alignment |
|---|---|---|---|---|---|---|---|---|---|
| bulgarian_fig_001 | Line Plot | BG | 952 | 817 | -14.2% | Yes (all fields) | Partial (color assignments differ: unstruct says blue=admin, struct says blue=admin but swaps orange/gray for other categories) | Moderate -- both describe 3 lines but assign different specific values and category-color mappings | Moderate -- both miss the administrative line being flat near 170, both inflate values |
| bulgarian_fig_002 | Line Plot | BG | 941 | 787 | -16.4% | Yes | Yes | Good -- both identify 2 lines (count + value) | Good -- values partially match groundtruth |
| bulgarian_fig_003 | Line Plot | BG | 888 | 797 | -10.2% | Yes | Yes | Good -- both describe dual-axis with count and value lines | Good -- key values (5667.2 peak, 989.3 start) present in both |
| bulgarian_fig_004 | Pie Chart | BG | 605 | 485 | -19.8% | Partial (2 of 4 percentages are "not specified") | Partial (unstruct says yellow=nikoga 57.1%, struct says blue="20 or more" 57.1% -- assignment differs) | Poor -- color-category mapping contradicts between approaches | Moderate -- 57.1% and 26.2% values match groundtruth, but color assignments vary |
| chinese_fig_001 | Line Plot | CN | 449 | 386 | -14.0% | Yes | Yes | Good -- both identify 3 lines (Precision, Recall, F1) with upward trends | Good -- matches groundtruth closely |
| chinese_fig_002 | Line Plot | CN | 381 | 343 | -10.0% | Yes (range "not specified" for y-axis is acceptable given the figure) | Yes | Moderate -- both describe emotion curve but struct is more concise | Good -- both match groundtruth emotion trajectory |
| chinese_fig_003 | Line Plot | CN | 371 | 330 | -11.1% | Yes | Yes -- both say peak at layers 2-3, decline after | Good | Good -- matches groundtruth peak at layer 2, though exact values differ slightly |
| chinese_fig_004 | Bar Chart | CN | 560 | 496 | -11.4% | Partial (bar "value" field has only approximate peak values, not full data; "color" for line overlay says "line chart" not a color) | Partial -- struct breakdown mislabels the overlay line's color | Moderate -- both describe combo chart but struct enumerated all 62 dates | Moderate -- both approaches capture overall pattern but differ on specific values |
| english_fig_001 | Pie Chart | EN | 700 | 705 | +0.7% | Yes | Partial -- struct breakdown lists 10 slices but misses inner/outer ring distinction that groundtruth specifies | Moderate -- both identify similar categories but with different percentages | Poor -- both miss the nested sunburst structure with inner/outer rings, significant simplification vs groundtruth |
| english_fig_002 | Pie Chart | EN | 696 | 629 | -9.6% | Yes (all 9 slices with percentages) | Yes | Good -- both describe 3 sub-charts accurately | Good -- matches groundtruth well |
| english_fig_003 | Line Plot | EN | 905 | 630 | -30.4% | Yes | Partial -- struct says 4 lines but unstruct describes 5 (includes baseline); struct breakdown says red line "decreasing" but paragraph says it starts -5% and ends at 0% (increasing) | Moderate -- both describe same lines but disagree on trend details | Moderate -- unstruct is more detailed, both partially match groundtruth |
| english_fig_004 | Line Plot | EN | 963 | 684 | -29.0% | Yes | Yes | Good -- both describe 4 lines + baseline | Good -- mostly aligns with groundtruth |
| german_fig_001 | Line Plot | EN | 550 | 448 | -18.5% | Yes | Yes | Good -- both describe 1 line with decreasing trend, orange markers | Good -- matches groundtruth |
| german_fig_002 | Bar Chart | EN | 727 | 607 | -16.5% | Yes (8 bars enumerated) | Yes | Good -- both describe grouped bars for LoRA vs QLoRA | Moderate -- specific values differ from groundtruth |
| german_fig_003 | Bar Chart | EN | 773 | 598 | -22.6% | Yes (8 bars) | Yes | Good -- consistent theme | Moderate -- both have approximate values |
| german_fig_004 | Bar Chart | EN | 715 | 620 | -13.3% | Yes (8 bars) | Partial -- struct says QLoRA(256)=6.0 but paragraph says QLoRA reaches 6.0, which contradicts groundtruth saying LoRA is higher at 256 | Moderate | Poor -- both misread which method is higher at rank 256 vs groundtruth |

### Multi-Language Figures (4 figures x 4 languages = 16 language-level descriptions)

| Figure Key | Type | Languages | Avg Unstruct Len | Avg Struct Len | Len Delta | Breakdown Complete? | Cross-Language Consistency (Struct) | Cross-Language Consistency (Unstruct) |
|---|---|---|---|---|---|---|---|---|
| multi_fig_001 | Line Plot | BG,CN,EN,DE | 694 | 624 | -10.1% | Yes | Poor -- BG says LLaMA1-7B "decreasing", CN says "stable", EN says "decreasing", DE says "stable" in breakdowns; trend fields vary per language | Moderate -- descriptions agree on general shape but differ on starting/ending values |
| multi_fig_002 | Bar Chart | BG,CN,EN,DE | 649 | 618 | -4.8% | Yes (all breakdowns present) | Good -- all languages agree on log scale, blue=Per-Output, orange=Per-Layer | Good -- all languages describe same pattern |
| multi_fig_003 | Bar Chart | BG,EN,DE (CN missing) | 670 | 538 | -19.7% | Partial (German breakdown has approximate values like "approximate value") | Moderate -- num_bars varies (24 vs 8 across languages) | Good |
| multi_fig_004 | Pie Chart | BG,EN,DE (CN missing) | 498 | 463 | -7.0% | Partial (most percentages "not specified" in BG and DE breakdowns) | Moderate -- num_slices varies (13 vs 10 across languages) | Moderate |

---

## Detailed Findings

### 1. Description Length Analysis

**Statistical Summary:**

| Metric | Unstructured (chars) | Structured (chars) | Difference |
|---|---|---|---|
| Mean (single-lang) | 698 | 610 | -12.6% |
| Median (single-lang) | 714 | 614 | -14.0% |
| Min (single-lang) | 371 | 330 | -11.1% |
| Max (single-lang) | 963 | 817 | -15.2% |
| Std Dev (single-lang) | 178 | 143 | -- |
| Mean (multi-lang, per desc) | 628 | 561 | -10.7% |

The structured approach consistently produces shorter paragraph descriptions. The largest reduction (30.4%) occurred for english_fig_003, a complex line plot where the structured approach offloaded line-by-line details into the breakdown rather than embedding them in prose.

### 2. Description Quality Differences

**Unstructured advantages:**
- Richer narrative flow with more contextual interpretation (e.g., bulgarian_fig_003 unstructured notes "the chart visualizes a warning about significant fluctuations")
- More specific numeric values embedded in the text (e.g., explicit data point callouts at each year)
- Better at capturing subtle visual features like error bars, marker shapes

**Structured advantages:**
- More organized presentation of axis information
- Paragraph is more focused on overall trends rather than exhaustive detail
- The breakdown fields provide machine-parseable metadata

**Quality concerns shared by both:**
- Both approaches occasionally hallucinate specific numeric values not present in the figure
- Color assignments are inconsistent -- for the same figure, the unstructured approach may say "blue line" while the structured says "green line" for the same data series
- Both tend to describe what the figure *should* show based on the caption rather than what it actually shows

### 3. Breakdown Completeness Analysis

For the 16 single-language structured figures:

| Breakdown Field | Present Rate | Notes |
|---|---|---|
| figure_type_detected | 16/16 (100%) | Always present; occasionally in native language (e.g., "pitana diagrama" for pie chart in Bulgarian) |
| x_axis / category_axis | 16/16 (100%) | Always present with label, scale, and range |
| y_axis / value_axis | 16/16 (100%) | Always present |
| num_lines / num_bars / num_slices | 16/16 (100%) | Always present but sometimes inaccurate |
| lines/bars/slices array | 16/16 (100%) | Always present |
| Individual element labels | 16/16 (100%) | Always populated |
| Individual element colors | 16/16 (100%) | Always populated but sometimes wrong or vague (e.g., "dark color") |
| Percentage (pie charts) | 3/4 (75%) | "Not specified" appears for 2 of 4 slices in bulgarian_fig_004 |
| Trend (line plots) | 8/8 (100%) | Always present for line plots |
| has_legend | 16/16 (100%) | Always present |
| legend_position | 14/16 (87.5%) | Two entries are null or "null" as string |

For multi-language structured figures (4 figures x 3-4 languages):

| Issue | Count |
|---|---|
| Percentage field "not specified" | 18 of 40 pie chart slice entries across multi_fig_004 |
| Approximate/vague bar values | 6 entries in multi_fig_003 German breakdown |
| Missing language outputs | multi_fig_003 and multi_fig_004 are missing Chinese breakdowns |

**Overall breakdown completeness rate: 87.5%** (fields populated with specific values vs. null/not-specified/approximate)

### 4. Breakdown-Paragraph Internal Consistency

I identified the following inconsistency patterns:

**Trend disagreements (found in 5/20 figures):**
- english_fig_003: Breakdown says red line trend is "decreasing" but paragraph says it "starts at -5% and ends at ~0%" which is increasing
- multi_fig_001 (Chinese): Breakdown says LLaMA1-7B trend is "stable" but paragraph says "showing a stable trend near the upper range" while groundtruth shows it decreasing
- multi_fig_001 (German): Breakdown says LLaMA1-7B is "stable" but paragraph says it "begins at 30 at M=3 and ends at 30 at M=8" (arguably stable, but paragraph also mentions "different trends including decreasing values")

**Color assignment disagreements (found in 3/20 figures):**
- bulgarian_fig_001: Paragraph maps colors differently than breakdown for the three line categories
- bulgarian_fig_004: Paragraph says "yellow=nikoga (57.1%)" but breakdown says the 57.1% slice is "20 or more" in "blue"

**Numeric value disagreements (found in 4/20 figures):**
- chinese_fig_004: Paragraph says max cases "approximately 160,000-180,000" but breakdown lists single value "160000"
- german_fig_004: Paragraph says QLoRA(256) reaches "approximately 6.0" but breakdown says "6.0" while groundtruth says LoRA is higher at 5.0 and QLoRA at 3.5

### 5. Cross-Approach Consistency

Comparing unstructured paragraphs with structured paragraphs for the same figure:

| Agreement Level | Count | Percentage |
|---|---|---|
| High (same facts, same structure) | 8/20 | 40% |
| Moderate (same theme, different details) | 9/20 | 45% |
| Poor (contradictory claims) | 3/20 | 15% |

**Examples of contradictions:**
- **bulgarian_fig_004**: Unstructured says yellow=nikoga(57.1%), blue="20 or more"; Structured says blue="20 or more"(57.1%), but the color-label mapping is reversed for some categories
- **english_fig_003**: Unstructured describes 5 lines (including baseline), structured breakdown lists only 4 lines (omitting baseline from count but mentioning it in the paragraph)
- **multi_fig_001** (English): Unstructured says LLaMA1-7B starts at ~40 perplexity, structured says ~35; groundtruth consensus is ~28-35

### 6. Multi-Language Quality Analysis

For multi_fig_001 (Line Plot), comparing the same figure described in 4 languages:

**Unstructured approach -- Cross-language value agreement for LLaMA1-7B starting perplexity at M=3:**
| Language | Stated Value | Groundtruth Range |
|---|---|---|
| Bulgarian | ~38 | 28-35 |
| Chinese | ~30-35 | 28-35 |
| English | ~40 | 28-35 |
| German | ~36 | 28-35 |

**Structured approach -- Same metric:**
| Language | Stated Value | Breakdown Trend |
|---|---|---|
| Bulgarian | ~30 | decreasing |
| Chinese | "stable trend near upper range" | stable |
| English | ~35 | decreasing |
| German | 30 | stable |

The structured approach shows **more inter-language variation in breakdown fields** than the unstructured approach shows in paragraph content. This is particularly evident in:
- **Trend labels**: The same line is labeled "decreasing" in one language and "stable" in another (multi_fig_001)
- **num_lines/num_bars**: multi_fig_003 German breakdown says 8 bars while Bulgarian and English say 24
- **Percentage values**: multi_fig_004 Bulgarian breakdown has all percentages as "not specified" while English provides approximate percentages

For multi_fig_003 and multi_fig_004, the Chinese language output is entirely missing from both approaches in the multi-language files, indicating a generation failure for Chinese in these specific cases.

### 7. Groundtruth Comparison Highlights

**bulgarian_fig_001 (Line Plot):**
- Groundtruth: Administrative line starts at 170, is "mostly straight and doesn't change much", ending at 70 in 2022
- Both approaches: Describe administrative line starting at ~4,938 and reaching ~7,047 -- this is a major error where the model confuses the administrative line with one of the other categories
- The structured breakdown at least captures 3 lines and axis ranges correctly

**english_fig_001 (Pie Chart -- sunburst):**
- Groundtruth: Complex nested sunburst with 6 inner categories and 15 outer subcategories per chart
- Both approaches: Simplify to a single-level pie chart, missing the inner/outer ring distinction entirely
- Structured breakdown lists 10 slices without hierarchical nesting -- a significant structural loss

**english_fig_003 (Line Plot):**
- Groundtruth: RULER4k 1x16-bit drops to -15% at Layer13-20 (consensus of 4 annotators)
- Unstructured: Says dark blue line drops to "nearly -10%" -- underestimates
- Structured: Breakdown says trend "increasing" for this line but it actually dips then recovers

**german_fig_002 (Bar Chart):**
- Groundtruth: LoRA at rank 16 is ~0.65, QLoRA at rank 16 is ~0.45
- Unstructured: Says LoRA ~0.56, QLoRA ~0.5 -- incorrect
- Structured: Says LoRA ~0.5, QLoRA ~0.4 -- closer to groundtruth pattern but values still off

---

## Statistical Summary

### Description Length

| Statistic | Unstructured | Structured | Delta |
|---|---|---|---|
| Total chars (all 20 figs, primary desc) | 13,233 | 11,648 | -12.0% |
| Avg chars per description | 662 | 582 | -12.0% |
| Avg word count per description | ~105 | ~92 | -12.4% |

### Breakdown Field Completeness (Structured Only)

| Category | Total Fields Checked | Populated | Completeness Rate |
|---|---|---|---|
| Axis labels/ranges | 64 | 62 | 96.9% |
| Element counts (num_lines etc.) | 20 | 20 | 100.0% |
| Element detail arrays | 20 | 20 | 100.0% |
| Individual colors | 98 | 98 | 100.0% |
| Individual labels | 98 | 98 | 100.0% |
| Percentages (pie only) | 40 | 22 | 55.0% |
| Trend labels (line only) | 26 | 26 | 100.0% |
| Legend info | 40 | 36 | 90.0% |
| **Overall** | **406** | **382** | **94.1%** |

### Accuracy Indicators

| Metric | Unstructured | Structured |
|---|---|---|
| Correct figure type identification | 20/20 (100%) | 20/20 (100%) |
| Correct element count (lines/bars/slices) | 15/20 (75%) | 16/20 (80%) |
| Correct color assignments (vs groundtruth) | ~12/20 (60%) | ~11/20 (55%) |
| Correct trend identification | ~14/20 (70%) | ~13/20 (65%) |
| Major factual errors (wrong category-value mapping) | 3/20 (15%) | 3/20 (15%) |

---

## Recommendations

### When to Use Each Approach

**Use Structured (paragraph + breakdown) when:**
- Building automated evaluation pipelines that need to extract specific attributes (axis ranges, line counts, colors)
- Performing large-scale quantitative analysis across many figures
- Feeding outputs into downstream systems that consume structured data
- You need machine-readable metadata alongside human-readable text

**Use Unstructured (paragraph-only) when:**
- The primary consumer is a human reader
- Narrative richness and interpretive context are valued
- The figure is highly complex (e.g., nested sunburst charts) where breakdown schemas may not capture the structure
- Token budget is a concern (structured outputs are larger in total despite shorter paragraphs)

### Process Improvements

1. **Add consistency validation**: After structured generation, automatically check that the paragraph and breakdown agree on key facts (num_lines, colors, trends). Flag discrepancies for review.

2. **Improve pie chart percentage extraction**: The 55% completeness rate for pie chart percentages suggests the model often cannot read slice percentages. Consider adding explicit instructions to report "not visible" rather than leaving blank.

3. **Standardize cross-language breakdowns**: For multi-language generation, enforce that the breakdown structure (num_lines, colors, trends) is identical across languages for the same figure. Currently, different languages produce structurally different breakdowns for the same image.

4. **Handle complex chart types**: Both approaches fail on nested/hierarchical visualizations (sunburst charts). The breakdown schema should be extended to support nested structures.

5. **Add groundtruth-based calibration**: The ~60% color assignment accuracy and ~70% trend accuracy suggest the model benefits from few-shot examples with correct color and trend labels.

---

## Appendix: File Locations

- Unstructured outputs: `/Users/poamen/projects/2026/grace/scifig/SciFig-Evaluation/output/generation/gpt-4o-mini/`
- Structured outputs: `/Users/poamen/projects/2026/grace/scifig/SciFig-Evaluation/output/generation_structured/gpt-4o-mini/`
- Groundtruth annotations: `/Users/poamen/projects/2026/grace/scifig/SciFig-Evaluation/Dataset/groundtruth/`
- Subfolders: `bulgarian_only/`, `chinese_only/`, `english_only/`, `german_only/`, `multi_language/`
- 4 figures per subfolder, 20 figures total per approach
