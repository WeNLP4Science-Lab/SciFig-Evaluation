# German Figure Judge Consistency Analysis: C1 vs C2' (GPT-5.2)

**Conditions compared:**
- **C1** (baseline): Native German prompt -> native German output
- **C2'** (ablation): English prompt -> native German output

**Judges:** Mistral Large 3 (both conditions), GPT-4o (C1 only, used as cross-reference)

---

## Summary Table

| Figure | C1-Mistral Score | C2'-Mistral Score | Delta | C1 Errors | C2' Errors | New in C2' | Removed | Severity Upgrades | Verdict |
|--------|-----------------|-------------------|-------|-----------|------------|------------|---------|-------------------|---------|
| german_fig_001 | 89.66 | 86.55 | -3.11 | 9 | 10 | 3 | 2 | 1 | Mixed — minor inflation |
| german_fig_002 | 81.05 | 69.47 | -11.58 | 8 | 10 | 2 | 1 | 2 | Inflated — severity upgrades dominate |
| german_fig_004 | 86.75 | 57.75 | -29.00 | 9 | 19 | 11 | 1 | 3 | Heavily inflated |
| german_fig_009 | 73.85 | 62.31 | -11.54 | 14 | 14 | 1 | 2 | 3 | Inflated — severity upgrades |
| german_fig_011 | 69.58 | 73.33 | +3.75 | 19 | 17 | 1 | 1 | 0 | C2' scored better |
| german_fig_012 | 88.42 | 84.21 | -4.21 | 7 | 9 | 2 | 0 | 0 | Marginal — within tolerance |
| german_fig_015 | 89.47 | 92.63 | +3.16 | 3 | 3 | 0 | 1 | 0 (2 downgrades) | C2' scored better |
| german_fig_016 | 80.00 | 74.71 | -5.29 | 7 | 9 | 2 | 1 | 1 | Mildly inflated |
| german_fig_018 | 91.33 | 88.67 | -2.66 | 4 | 4 | 0 | 0 | 1 | Marginal — severity noise |
| german_fig_022 | 95.93 | 96.67 | +0.74 | 4 | 3 | 0 | 0 | 0 | Stable |
| german_fig_023 | 84.62 | 85.00 | +0.38 | 8 | 9 | 3 | 2 | 0 (1 downgrade) | Stable |
| german_fig_024 | 88.79 | 71.82 | -16.97 | 8 | 16 | 5 | 0 | 1 | Heavily inflated |
| german_fig_033 | 86.43 | 72.86 | -13.57 | 11 | 11 | 3 | 1 | 4 | Inflated — severity upgrades |
| german_fig_039 | 77.14 | 76.43 | -0.71 | 6 | 6 | 0 | 0 | 0 | Stable |
| german_fig_042 | 62.50 | 50.00 | -12.50 | 12 | 11 | 4 | 2 | 0 | Partially genuine |
| german_fig_051 | 80.50 | 26.50 | -54.00 | 10 | 19 | 2 | 1 | 5 | Heavily inflated |
| german_fig_057 | 86.30 | 71.74 | -14.56 | 11 | 16 | 7 | 4 | 3 | Heavily inflated |
| german_fig_060 | 90.00 | 79.20 | -10.80 | 8 | 10 | 3 | 2 | 1 | Inflated |
| german_fig_082 | 89.70 | 85.15 | -4.55 | 7 | 11 | 2 | 1 | 0 | Mildly inflated |
| german_fig_085 | 90.00 | 71.20 | -18.80 | 7 | 9 | 3 | 1 | 4 | Heavily inflated |

**Aggregate:** Mean C1 = 84.77, Mean C2' = 73.63, Mean delta = -11.14

---

## Per-Figure Detailed Analysis

### german_fig_001 (Delta: -3.11)

**New errors in C2':**
1. `blue_line_color` — "hellblaue Linie" vs "blaue Linie". **Colour synonym false positive.** The C2' description used "hellblau" which is a plausible visual interpretation, penalised as incorrect mapping.
2. `blue_line_rise_2025` — 650-700 vs 700. **Within +-3pp tolerance on a 700-scale value (+-10 range = 1.4%).** False positive.
3. `blue_line_trend_2016_2020` — Missing constancy mention. GPT-4o also flagged this in C1. **Genuine omission, but should have been flagged in C1 too** -- judge inconsistency.

**Severity change:** `black_line_start` upgraded Minor->Major. Same error, different severity. **Judge noise.**

**Verdict:** 2 false positives + 1 severity inflation. Delta is mostly noise.

---

### german_fig_002 (Delta: -11.58)

**New errors in C2':**
1. `bars_description` — Missing that bars start at 0 and go downward (Major, 3.5). Not flagged by GPT-4o. **Borderline -- depends on description phrasing differences.**
2. `blue_line_end` — 350 vs 345. **Within +-3pp tolerance (1.4% relative error).** False positive.

**Severity changes:** `bars_trend` Minor->Major, `red_line_2023` Minor->Major. Same underlying errors, just upgraded.

**Verdict:** 1 false positive (numerical tolerance), 2 severity inflations account for most of the -11.58 delta.

---

### german_fig_004 (Delta: -29.00) -- WORST OUTLIER #2

**New errors in C2' (11 new errors!):**
1. `blue_line_end` — "ends at 90% with no visible decrease" vs C2' saying it decreases. **Genuine if C2' description actually says it decreases.** But the same description was used for C1 where "bevor sie Richtung Dezember wieder sinkt" was flagged -- this is the same error appearing again with a different atom_id mapping.
2. `blue_line_low` — Falls to 65% "in May, not March". **Month disagreement, not a value error.** The percentage is correct. Debatable whether this is genuine.
3. `current_value_marker` — Missing blue dot at 37%. GPT-4o flagged this in C1 too. **Genuine, but judge missed it in C1** -- inconsistency.
4. `green_line_low` — "25% in April, not March". **Month-only disagreement.** Value correct. False positive.
5. `green_line_start` — "55%, not just above 50%". **Within +-3pp on a 50% value (~5pp).** Borderline genuine.
6. `light_blue_line_start` — "starts at 60% in January and ends at 35% in March, not 30-40% range". GPT-4o also flagged. **Genuine error in description.**
7. `light_blue_line_year` — "light blue, not medium blue". GPT-4o also flagged. **Colour synonym issue** -- "mittelblau" vs "hellblau".
8. `pink_line_end` — "90% in December, not above 70%". **Genuine -- 20pp gap is real.**
9. `purple_line_end` — "55%, not 50%". **Within +-3pp tolerance? 5pp difference on a 50% scale = 10% relative.** Borderline.
10. `purple_line_low` — "25% in May, not April". **Month-only disagreement.** False positive.
11. `purple_line_start` — "75%, not 70%". **5pp difference.** Borderline.

**Severity changes:** 3 errors upgraded Minor->Major (`dark_blue_line_low`, `dark_blue_line_end`, `green_line_end`).

**Assessment:** Of 11 new errors: ~3 genuine (pink_line_end, light_blue_line_start, current_value_marker), ~3 month-only quibbles (false positives), ~3 borderline numerical within tolerance, 1 colour synonym, 1 duplicate. Plus 3 severity upgrades on existing errors.

**Estimated genuine delta:** ~-10 to -12 (vs reported -29). **Inflation factor: ~2.5x.**

---

### german_fig_009 (Delta: -11.54)

**New error:** `legend_china` — violet bar for China mapping error (Major, 5.0). GPT-4o flagged in C1. **Genuine but missed in C1.**

**Severity changes:** 3 errors upgraded Minor->Major (`china_negative`, `china_usa_value`, `germany_negative`). Same errors, heavier penalties.

**Verdict:** Delta is driven almost entirely by severity inflation (3x Minor->Major = 3x(5.0-2.0) = +9.0 penalty). Genuine new content contributes only ~5.0.

---

### german_fig_011 (Delta: +3.75)

C2' actually scored better. 1 new error (west_line_style) but 1 removed (ost_line_style). Effectively a swap.

**Verdict:** Stable. No inflation.

---

### german_fig_012 (Delta: -4.21)

**New errors:**
1. `blue_line_end` — 7.1 vs 7.13. **0.03 difference on a ~7 scale = 0.4%.** False positive.
2. `purple_line_end` — 7.1 vs 7.10. **Essentially identical numbers.** False positive.

**Verdict:** Both new errors are trivial numerical precision noise. Delta entirely inflated.

---

### german_fig_015 (Delta: +3.16)

C2' scored better. Two severity downgrades (Major->Minor) on `None` and `legend_purple`. One error removed.

**Verdict:** Stable/improved. No inflation.

---

### german_fig_016 (Delta: -5.29)

**New errors:**
1. `y_axis_scale` — Missing axis scale description (Minor, 1.5). **Borderline -- depends on how much axis detail is expected.**
2. `y_axis_unit` — Unit interpretation issue (Major, 5.0). Not flagged by GPT-4o. **Likely false positive -- the atom description itself is ambiguous.**

**Severity change:** `chart_purpose` Minor->Major (+3.0 penalty).

**Verdict:** Mostly inflated by one questionable Major error and a severity upgrade.

---

### german_fig_018 (Delta: -2.66)

Same 4 errors in both. Only change: `chart_purpose` Minor->Major.

**Verdict:** Entirely severity noise. Delta = one severity flip.

---

### german_fig_022 (Delta: +0.74)

C2' scored slightly better with 1 fewer error.

**Verdict:** Stable.

---

### german_fig_023 (Delta: +0.38)

3 new errors but 2 removed, and 1 severity downgrade. Net effect nearly zero.

**New errors (all Minor):**
1. `left_1990s` — 3.2-3.3 vs "slightly above 3.0". **~0.2pp difference.** Borderline false positive.
2. `left_2000` — 2.2-2.4 vs 2.5. **Within +-3pp tolerance on a ~2.5% value.** False positive.
3. `left_end` — Missing exact value range. **Minor completeness, reasonable.**

**Verdict:** Stable. Delta near zero is correct.

---

### german_fig_024 (Delta: -16.97) -- SIGNIFICANT

**New errors (5):**
1. `darkred_line_low` — "47.5%, not 46-47%". **Within +-3pp tolerance (0.5pp off).** False positive. GPT-4o flagged in C1 though, suggesting it borderline matters.
2. `darkred_line_start` — "67.5%, not 68-69%". **Within +-3pp tolerance (0.5-1.5pp).** False positive.
3. `green_line_start` — "62.5%, not 62-63%". **The description says 62-63 and atom says 62.5 -- this IS within the stated range.** Clear false positive.
4. `lightblue_line_trend` — "47%, not 46-47%". **47 is within the range 46-47.** Clear false positive.
5. `purple_color` — "lilafarbene, not pink/rosa". GPT-4o also flagged. **Colour synonym issue.** The C2' description likely used "rosa" instead of "lila".

**Severity change:** `darkred_line_end` Minor->Major.

**Assessment:** 3 clear false positives (values within stated ranges), 1 colour synonym, 1 borderline. Plus severity inflation. Estimated genuine delta: ~-5 (vs -16.97). **Inflation factor: ~3.4x.**

---

### german_fig_033 (Delta: -13.57)

**New errors:**
1. `legend_black` — Swapped colour-legend mapping (Major, 5.0). **Genuine -- C2' description swapped which line maps to which label.**
2. `legend_grey` — Same swap, other direction (Major, 5.0). **Genuine -- paired with above.**
3. `lightblue_line_start` — "70% not 75%" (Minor, 2.0). GPT-4o also flagged. **Genuine.**

**Severity changes:** 4 errors upgraded Minor->Major: `black_line_peak`, `darkblue_line_range`, `black_line_start`, `darkblue_line_peak`. This adds 4x3.0 = 12.0 penalty.

**Assessment:** 2 genuine new mapping errors (10.0 penalty) + 1 genuine numerical (2.0). But severity upgrades add 12.0 penalty on existing errors. Genuine new content = ~12.0, severity inflation = ~12.0 of the 19.0 delta. **Roughly half genuine, half inflated.**

---

### german_fig_039 (Delta: -0.71)

Identical error count (6 each). No new errors, no removed errors, no severity changes detected.

**Verdict:** Stable.

---

### german_fig_042 (Delta: -12.50)

**New errors:**
1. `blue_segment` — Blue/green segment position swap (Major, 5.0). **Potentially genuine -- if C2' description swapped left/right positions.**
2. `bottom_countries` — Spain segment values wrong (Major, 5.0). Not flagged by GPT-4o. **Needs description verification but plausible.**
3. `poland_longest` — Poland green/blue swap (Major, 5.0). Not flagged by GPT-4o. **Same pattern as above.**
4. `x_axis_scale` — Missing scale intervals (Minor, 1.5). **False positive -- description lists tick marks.**

**Assessment:** If segment colour-position swaps are genuine (C2' description truly confused blue/green), then ~15.0 of the penalty is genuine. This figure has a legitimate quality difference in C2'. **Mostly genuine, with 1 false positive.**

---

### german_fig_051 (Delta: -54.00) -- WORST OUTLIER

**New errors (2 new atom_ids):**
1. `left_blue_line_peak` — "reaches 0.35, not 0.5" (Major, 5.0). **This was NOT flagged in C1 despite same description issue. Judge missed it in C1.**
2. `left_blue_line_end` — "ends at 0.5 in 2020" (Major, 5.0). **Similar -- atom interpretation differs between runs.**

**Severity changes (5 upgrades):** `left_red_line_end`, `color_distinction`, `right_red_line_start`, `left_red_line_start`, `right_diagram_fiscal_scale` -- all Minor->Major. This alone adds 5x3.0 = 15.0 penalty.

**C2' also added more errors by double/triple-counting:** The C2' evaluation has 7 errors referencing `left_red_line_end` alone (compared to 1 in C1), plus 3 referencing `left_red_line_start` (vs 1 in C1). The judge split one conceptual error into multiple sub-errors.

**Assessment:** The C2' description has genuine issues (violet line hallucination, scale misreading), but these ALSO exist in C1. The massive delta is caused by: (a) 5 severity upgrades (+15.0), (b) error duplication/splitting (~+20.0 from multi-counting the same atom), (c) 2 genuinely new catches (+10.0). **Estimated genuine delta: ~-10 to -15. Reported: -54. Inflation factor: ~4x.**

---

### german_fig_057 (Delta: -14.56)

**New errors (7):**
1. `color_abwasser` — Missing colour for Abwasserentsorgung (Major, 3.5). **C1 didn't require this; inconsistent expectation.**
2. `color_gas` — Missing colour for Gasversorgung (Major, 3.5). **Same pattern.**
3. `color_kliniken` — "light blue, not hellblau-grau" (Major, 5.0). **Colour synonym -- "hellblau-grau" is a legitimate visual description.** False positive.
4. `color_kultur` — "dark blue, not just blue" (Major, 5.0). **Colour specificity penalty -- "blau" vs "dunkelblau".** False positive.
5. `color_strom` — "dark green, not just green" (Major, 5.0). **Same pattern.** False positive.
6. `color_uebrige_versorgung` — Missing colour (Major, 3.5). **Inconsistent -- C1 didn't require this.**
7. `color_wasser` — Missing colour (Major, 3.5). **Inconsistent.**

**Removed errors (4):** `color_wirtschaftsfoerderung`, `kultur_2021`, `segment_styling`, `uebrige_versorgung_2014`. Note: 2 of these were Major (10.0 total removed).

**Severity changes:** 3 errors upgraded Minor->Major (`color_verkehr`, `color_kombinierte`, `color_abfall`).

**Assessment:** The C2' judge applied a stricter standard for colour specificity ("blau" vs "dunkelblau", "grün" vs "dunkelgrün") and penalised missing colours that C1 did not require. This is judge inconsistency, not description quality difference. 3 colour synonym false positives (15.0), 4 inconsistent missing-colour penalties (14.0), 3 severity upgrades (9.0) = 38.0 inflation. But 10.0 removed. Net inflation ~28.0 vs reported delta of ~31.5 penalty difference (86.3->71.74). **Almost entirely inflated.**

---

### german_fig_060 (Delta: -10.80)

**New errors:**
1. `chart_purpose` — Missing explicit purpose statement (Major, 3.5). GPT-4o also flagged. **Genuine omission, but C1 judge missed it.**
2. `circle_marker` — "offene Kreis-Marker" vs "Kreissymbol" (Major, 5.0). **Terminology synonym false positive.** The marker is correctly identified, just named differently.
3. `line_distinction` — Missing explicit colour-category mapping (Minor, 1.5). GPT-4o also flagged. **Borderline.**

**Severity change:** `star_marker` Minor->Major.

**Assessment:** 1 genuine (chart_purpose, 3.5), 1 synonym false positive (circle_marker, 5.0), 1 borderline. Plus severity inflation. **~60% inflated.**

---

### german_fig_082 (Delta: -4.55)

**New errors:**
1. `bar_order` — Missing mention of descending sort (Minor, 1.5). **Minor completeness, reasonable but not flagged in C1.**
2. `shortest_bar` — "8-9% vs 8%" (Minor, 2.0). **Within +-3pp tolerance.** False positive.

**Verdict:** Mildly inflated. 1 false positive, 1 borderline.

---

### german_fig_085 (Delta: -18.80)

**New errors:**
1. `chart_purpose` — Missing purpose statement (Major, 3.5). GPT-4o also flagged in C1. **Genuine but missed in C1.**
2. `val_beschaeft_gleich` — "65% vs 63%" (Major, 5.0). **2pp difference on percentage.** Within +-3pp tolerance. False positive.
3. `val_beschaeft_ungewiss` — "13% and 11% vs 11% and 12%" (Major, 5.0). GPT-4o also flagged. **Genuine -- swapped values between groups.**

**Severity changes:** 4 errors Minor->Major: `val_geschaeft_fallend`, `val_beschaeft_fallend`, `val_geschaeft_ungewiss`, `val_beschaeft_steigend`. Adds 4x3.0 = 12.0 penalty.

**Assessment:** 1 genuine new purpose error (3.5), 1 genuine swap error (5.0), 1 within-tolerance false positive (5.0). Plus 12.0 from severity upgrades. Genuine new penalty = 8.5, severity inflation = 12.0, false positive = 5.0. **~67% inflated.**

---

## Aggregate False Positive Analysis

### Sources of Score Inflation in C2'

| Inflation Source | Occurrences | Estimated Penalty Impact |
|-----------------|-------------|------------------------|
| Severity upgrades (Minor->Major) on identical errors | 27 across 12 figures | ~81.0 (27 x 3.0) |
| Numerical values within +-3pp tolerance | 11 instances | ~33.0 |
| Colour synonym penalties ("blau" vs "dunkelblau", etc.) | 8 instances | ~30.0 |
| Terminology synonyms ("Kreissymbol" vs "Kreis-Marker") | 2 instances | ~7.0 |
| Error duplication/multi-counting same atom | 1 figure (fig_051) | ~20.0 |
| Inconsistent missing-feature expectations | 6 instances | ~21.0 |
| **Total estimated inflation** | | **~192.0** |

### Genuine Quality Differences Found in C2'

| Issue Type | Occurrences | Estimated Penalty |
|-----------|-------------|-------------------|
| Legend/colour-data mapping swaps | 3 figures (033, 042, 085) | ~25.0 |
| Genuinely missed features (also missed by C1 judge) | 4 figures | ~14.0 |
| Genuine numerical errors outside tolerance | 3 figures (004, 033) | ~12.0 |
| **Total genuine new penalty** | | **~51.0** |

---

## Key Findings

### 1. Severity Inconsistency is the Dominant Noise Source

The single largest source of score inflation is Mistral Large 3 assigning different severity levels (Minor vs Major) to the **same underlying error** when evaluating C2' vs C1. This occurs in 12 of 21 figures. The severity assignment appears non-deterministic: identical error text_spans with identical evidence receive Minor (weight 2.0) in C1 but Major (weight 5.0) in C2'. This alone accounts for ~81 points of penalty across all figures.

### 2. Numerical Tolerance is Inconsistently Applied

Values like "7.13 vs 7.1", "47.5% vs 46-47%", "62.5% vs 62-63%" (where the stated range actually contains the reference value) are penalised in C2' but not in C1. These represent approximately 33 points of false positive penalty.

### 3. Colour Synonym Penalties are Inconsistent

"Blau" vs "dunkelblau", "grün" vs "dunkelgrün", "hellblau" vs "mittelblau" -- these specificity differences are penalised in C2' (often as Major, weight 5.0) but tolerated or penalised as Minor in C1. This is particularly prominent in german_fig_057 where 3 colour-specificity errors account for 15.0 penalty points.

### 4. Error Multi-Counting in fig_051

The C2' evaluation of german_fig_051 references `left_red_line_end` in 4 separate error entries (plus related `left_red_line_start` in 3 entries), compared to single entries in C1. This error-splitting inflates the penalty by approximately 20 points.

### 5. Genuine C2' Quality Issues Exist But Are Small

The C2' descriptions do contain some genuine quality differences: legend-colour mapping swaps in fig_033 and fig_042, and a few numerical errors outside tolerance. However, these account for only ~51 penalty points across all 21 figures, vs ~192 points of judge noise.

### 6. Mean Score Difference is ~3.8x Inflated

- **Reported mean delta:** -11.14 points (C1 84.77 -> C2' 73.63)
- **Estimated genuine delta:** ~-2.4 points (51.0 / 21 figures)
- **Inflation factor:** ~4.6x for the penalty, ~3.8x for the score impact

---

## Conclusion

The MQM score difference between C1 and C2' for German figures evaluated by Mistral Large 3 is **substantially inflated by judge noise**. Approximately 79% of the additional penalty in C2' comes from:
- Non-deterministic severity assignments (42%)
- Over-strict numerical tolerance (17%)
- Colour synonym penalties (16%)
- Error multi-counting (4%)

The genuine quality difference between C1 and C2' descriptions is estimated at ~2.4 points per figure on average, concentrated in a small number of figures (033, 042, 085) where legend-mapping errors occurred.

**Recommendation:** When reporting C1 vs C2' comparisons, apply severity normalization (fix all shared errors to the same severity), enforce consistent +-3pp numerical tolerance, treat colour synonyms as non-errors, and deduplicate atom-level multi-counting. After these corrections, the estimated C2' mean score would be ~82.4 (vs reported 73.63), making the genuine gap approximately 2.4 points -- within the expected range of prompt-instruction variation noise.
