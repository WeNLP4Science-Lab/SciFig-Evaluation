# Severity Assignment for Pie Chart Description Checklist Items

Severity levels for the 17 atomic checklist items used in MQM-based evaluation of VLM-generated pie chart descriptions. Pie charts are the hardest chart type for VLMs in our evaluation (MQM 54.1 avg, 10.8 mean atoms, 10.2 errors/fig, delta_cap +11.0).

## Weight Matrix Reference

| Dimension    | Major | Minor |
|-------------|-------|-------|
| Accuracy    | 5.0   | 2.0   |
| Completeness| 3.5   | 1.5   |
| Clarity     | 2.0   | 1.0   |

## Severity Cap Mechanics

- **Critical / Important** item, completely wrong or missing: Major error (full dimension weight)
- **Critical / Important** item, partially wrong: Minor error (reduced weight)
- **Minor** item, any error: Minor error (capped, never escalates to Major)

---

## Item Severity Assignments

### pie_01: Chart type correctly identified (standard pie, donut, nested)

**Severity: Critical**

Misidentifying chart type (e.g., calling a donut chart a standard pie, or missing that a chart is nested/multi-ring) fundamentally misrepresents the data structure and invalidates downstream interpretation. ChartX (Xia et al., 2024) shows that VLM performance degrades substantially on compound chart types like nested and donut variants, making this a high-risk item. A wrong chart type signals that the model has misunderstood the visual encoding scheme entirely.

### pie_02: Chart purpose or title described

**Severity: Critical**

The title or stated purpose anchors the entire description in its scientific context. Omitting or misrepresenting the title (e.g., "Distribution of funding by discipline" vs. "Distribution of publications by discipline") renders the description scientifically misleading regardless of how accurate the slice-level details are. SciCap (Hsu et al., 2021) and ChartSumm (Rahman et al., 2023) both treat the chart's communicative purpose as a primary evaluation target.

### pie_03: Total number of slices correctly stated

**Severity: Critical**

Slice count is a structural fact that is objectively verifiable and has cascading effects: an incorrect count implies either hallucinated slices or missed slices, both of which are accuracy errors. BlindTest (Rahmanzadehgervi et al., 2024) demonstrated that VLMs fail at counting overlapping geometric shapes, and pie chart slices -- especially small ones subtending less than 4 degrees -- are routinely undercounted. An incorrect slice count is strong evidence of broader perceptual failure.

### pie_04: All slice labels mentioned

**Severity: Critical**

Omitting a slice label means an entire data category is absent from the description, which is a completeness failure with direct scientific impact. If a pie chart shows five funding sources and the description mentions only four, a reader relying on the description will draw incorrect conclusions. CHOCOLATE (Huang et al., 2024) classifies omission of chart elements as a factual error. ChartHal (Wang et al., 2025) shows that omission-type errors are among the most frequent VLM failures.

### pie_05: Slice colours correctly described

**Severity: Minor**

Colour descriptions support accessibility and cross-referencing with the original figure, but errors in colour naming (e.g., "blue" vs. "teal") do not directly corrupt the scientific interpretation if the label-to-value mapping is otherwise correct. Kim et al. (2024) document that VLMs lack reliable colour discrimination, making this a high-frequency but low-impact error. Capping at Minor prevents colour-naming noise from inflating MQM scores disproportionately.

### pie_06: Slice percentages/values accurate (exact when labeled, +/-5% when estimated for slices >=10%)

**Severity: Critical**

Percentage accuracy is the core quantitative claim in any pie chart description. CHOCOLATE (Huang et al., 2024) identifies percentage hallucination as the primary factual error type in VLM chart captions. ChartHal (Wang et al., 2025) found that even GPT-5 achieves only 34.46% on hallucination detection tasks. For scientific figures, wrong percentages directly mislead readers about data proportions. The +/-5% tolerance for estimated values already provides generous allowance; violations beyond this threshold represent genuine errors.

### pie_07: Colour-to-label mapping correct

**Severity: Important**

A wrong colour-to-label mapping (e.g., saying "the blue slice represents Category A" when it actually represents Category B) swaps the identity of data categories, which is a factual error that corrupts interpretation. CHOCOLATE (Huang et al., 2024) documents this as a major error category. However, this item is rated Important rather than Critical because the error is detectable by a reader who cross-references with the original figure, and it often co-occurs with pie_04 or pie_06 errors that already carry Critical severity.

### pie_08: Ordering of slices described (clockwise, by size)

**Severity: Minor**

Slice ordering is a layout detail that aids spatial navigation but does not affect the factual content of the description. A description that accurately lists all slices with correct labels and values but describes them in an arbitrary order rather than clockwise is less organised but not scientifically wrong. Rahmanzadehgervi et al. (2024) show that spatial reasoning is a broad VLM weakness, but ordering errors have low downstream impact compared to value or label errors.

### pie_09: Legend correctly described if present (position, mappings)

**Severity: Important**

The legend is the key that connects visual encodings to data categories. If the legend description is wrong, colour-to-label mappings become unreliable. ChartGaze (Salamatian et al., 2025) found that VLMs often attend to irrelevant regions rather than the legend, leading to systematic mapping errors. Rated Important because legend errors typically cascade into pie_07 (colour-to-label mapping) errors, but the legend itself is a secondary element -- the slice-level data is primary.

### pie_10: Legend position correctly stated if present

**Severity: Minor**

Legend position (e.g., "top-right" vs. "bottom-left") is a layout detail with no bearing on data interpretation. Errors here are purely descriptive inaccuracies about spatial arrangement. Capping at Minor ensures this low-impact item does not contribute disproportionately to score inflation, consistent with the delta_cap finding that multi-error atoms on minor items inflate pie chart scores.

### pie_11: Visual emphasis noted if present (exploded slices, bold labels)

**Severity: Minor**

Visual emphasis is an authorial design choice that signals importance but does not alter the underlying data. Missing a note about an exploded slice means the description fails to convey the author's intent, but the data itself can still be correctly interpreted. Current benchmarks under-represent exploded pie charts (Kahou et al., 2018), meaning this item has limited evaluation precedent. Minor severity prevents over-penalising omissions of a feature that many charts lack entirely.

### pie_12: Labels-on-slices vs external labels noted

**Severity: Minor**

The labelling strategy (internal vs. external with leader lines) is a visual design characteristic. Noting it adds useful context for understanding how the VLM derived its data, but errors or omissions here do not corrupt the described data values. Masry et al. (2024) found that VLMs perform differently depending on label placement, but this difference affects extraction accuracy (captured by pie_04 and pie_06), not the correctness of describing the placement itself.

### pie_13: Largest and smallest slices identified

**Severity: Important**

Identifying extremes is a core analytical task that readers expect from a chart description. ChartInsights (Wu et al., 2024) found that comparison tasks ("which is larger?") are among the most error-prone for VLMs, particularly on pie charts where angular comparison is unreliable. Getting the largest/smallest wrong reverses the chart's key message. Rated Important rather than Critical because the individual slice values (pie_06) already carry Critical severity, and extreme identification is derivable from correct values.

### pie_14: No hallucinated elements (fabricated slices, percentages)

**Severity: Critical**

Hallucination is the most damaging error class for scientific figure descriptions. A fabricated slice or invented percentage introduces false information that has no basis in the source figure. CHOCOLATE (Huang et al., 2024) found non-factual rates of 81.27% in VLM chart captions. ChartHal (Wang et al., 2025) and CHART NOISe (Shin et al., 2025) both document that VLMs invent values under uncertainty. Any hallucinated element warrants the maximum penalty because it fundamentally undermines trust in the description.

### pie_15: No unwanted interpretation

**Severity: Important**

Adding causal claims, predictions, or domain interpretations beyond what the chart shows ("this indicates a declining trend in funding") introduces unsupported inference. For scientific figures, unsupported interpretation can mislead readers about the authors' conclusions. However, this is rated Important rather than Critical because mild interpretation (e.g., "Category A dominates") is often expected in chart descriptions (VisText L3 captions), and the boundary between description and interpretation is context-dependent. Partial violations (slight over-interpretation) should incur only Minor penalties.

### pie_16: Description is clear and unambiguous

**Severity: Important**

Clarity falls under the Clarity dimension (Major=2.0, Minor=1.0), which already carries lower weights than Accuracy. An unclear description that uses ambiguous pronoun references or confusing sentence structure can cause misinterpretation even when the underlying facts are correct. Rated Important because ambiguity in scientific communication can lead to misunderstanding of data relationships, but the lower Clarity weights naturally limit the score impact.

### pie_17: Description is not overly verbose or repetitive

**Severity: Minor**

Verbosity and repetition are stylistic issues that reduce readability but do not introduce factual errors. A description that states the same percentage twice or uses unnecessarily wordy phrasing is annoying but not scientifically harmful. This aligns with the Clarity dimension's lower weight structure. Capping at Minor ensures that verbosity never receives a Major penalty, consistent with MQM conventions where fluency/style issues are typically minor.

---

## Summary Table

| Item   | Description                                      | Severity   | Dimension     | Max Penalty |
|--------|--------------------------------------------------|------------|---------------|-------------|
| pie_01 | Chart type correctly identified                  | Critical   | Accuracy      | 5.0         |
| pie_02 | Chart purpose or title described                 | Critical   | Completeness  | 3.5         |
| pie_03 | Total number of slices correctly stated          | Critical   | Accuracy      | 5.0         |
| pie_04 | All slice labels mentioned                       | Critical   | Completeness  | 3.5         |
| pie_05 | Slice colours correctly described                | Minor      | Accuracy      | 2.0         |
| pie_06 | Slice percentages/values accurate                | Critical   | Accuracy      | 5.0         |
| pie_07 | Colour-to-label mapping correct                  | Important  | Accuracy      | 5.0         |
| pie_08 | Ordering of slices described                     | Minor      | Completeness  | 1.5         |
| pie_09 | Legend correctly described if present             | Important  | Completeness  | 3.5         |
| pie_10 | Legend position correctly stated if present       | Minor      | Completeness  | 1.5         |
| pie_11 | Visual emphasis noted if present                 | Minor      | Completeness  | 1.5         |
| pie_12 | Labels-on-slices vs external labels noted        | Minor      | Completeness  | 1.5         |
| pie_13 | Largest and smallest slices identified            | Important  | Accuracy      | 5.0         |
| pie_14 | No hallucinated elements                         | Critical   | Accuracy      | 5.0         |
| pie_15 | No unwanted interpretation                       | Important  | Accuracy      | 5.0         |
| pie_16 | Description is clear and unambiguous             | Important  | Clarity       | 2.0         |
| pie_17 | Description is not overly verbose or repetitive  | Minor      | Clarity       | 1.0         |

## Distribution

- **Critical**: 6 items (pie_01, pie_02, pie_03, pie_04, pie_06, pie_14)
- **Important**: 5 items (pie_07, pie_09, pie_13, pie_15, pie_16)
- **Minor**: 6 items (pie_05, pie_08, pie_10, pie_11, pie_12, pie_17)

## Design Rationale

The severity distribution is shaped by two key findings:

1. **Pie charts have the highest error density** (10.2 errors/fig on 10.8 atoms). With nearly one error per atom, capping Minor items prevents score collapse. If all 17 items were Critical, a typical pie chart description would accumulate catastrophic penalties that fail to differentiate between slightly-wrong and completely-wrong descriptions.

2. **The delta_cap of +11.0 points** shows that multi-error atoms on pie charts inflate scores under uncapped scoring. The 6 Critical / 5 Important / 6 Minor split ensures that the most consequential errors (wrong values, hallucinations, missing categories) receive full Major penalties, while layout and style details (ordering, legend position, verbosity) are capped at Minor. This concentrates scoring power on items that matter for scientific interpretation while dampening the noise from high-frequency low-impact errors.
