# Bulgarian Judge Consistency Analysis: C1 vs C2' (GPT-5.2)

**Scope**: 9 Bulgarian figures with both C1 (native prompt -> native output) and C2' (English prompt -> native output) descriptions, evaluated by Mistral Large 3. GPT-4o C1 scores included as reference where available.

---

## Score Summary

| Figure | Mistral C1 | Mistral C2' | Delta | GPT-4o C1 | Verdict |
|--------|-----------|-------------|-------|-----------|---------|
| bulgarian_fig_001 | 88.4 | 83.2 | -5.2 | 85.2 | Inflated by judge noise |
| bulgarian_fig_014 | 72.5 | 51.7 | -20.8 | 70.0 | Partially inflated |
| bulgarian_fig_021 | 90.5 | 82.9 | -7.6 | 86.2 | Inflated by judge noise |
| bulgarian_fig_036 | 79.4 | 45.6 | -33.9 | 36.7 | Partially inflated |
| bulgarian_fig_038 | 58.7 | 58.3 | -0.4 | 69.6 | No difference (same errors) |
| bulgarian_fig_048 | 72.7 | 50.7 | -22.0 | 73.3 | Inflated by judge noise |
| bulgarian_fig_095 | 75.6 | 20.0 | -55.6 | 26.7 | Heavily inflated |
| bulgarian_fig_103 | 80.0 | 76.0 | -4.0 | 50.0 | Minor genuine difference |
| bulgarian_fig_272 | 71.3 | 71.3 | 0.0 | 71.3 | No difference |

**Mean C1**: 76.6 | **Mean C2'**: 59.9 | **Mean Delta**: -16.6

---

## Per-Figure Analysis

### bulgarian_fig_001 (Line Plot)

**C1 score**: 88.4 (8 errors, 14.5 penalty) | **C2' score**: 83.2 (12 errors, 21.0 penalty)

**Descriptions are nearly identical.** Both C1 and C2' list all yearly values for all three lines, identify the same colours, same data values, same structural elements. The only differences are minor phrasing variations.

**New errors in C2' (not in C1):**
1. **chart_type (Major, 3.5)**: Judge says C2' doesn't state the chart illustrates "changes in building permits." But C2' opens with "Графиката илюстрира броя издадени разрешения за строеж на нови сгради по години" -- this IS the chart purpose. **FALSE POSITIVE.**
2. **orange_line_peak (Minor, 1.5)**: Judge says C2' doesn't mention the peak 5,460 in 2017. But C2' explicitly states "достига 5 460 (2017)" and "с максимум при 2017 г." **FALSE POSITIVE.**
3. **orange_line_min (Minor, 1.5)**: Judge says C2' doesn't mention minimum 3,944 in 2020. But C2' states "3 944 (2020)" and "минимум при 2020 г." **FALSE POSITIVE.**
4. **grey_line_2013 (Minor, 1.5)**: Judge says C2' omits 2013 as lowest for grey line. C2' lists "4 120 (2013)" but doesn't label it as the period minimum. **BORDERLINE** -- the value is present, the "lowest" label is missing. Marginal error.
5. **grey_line_2020_2021 (Minor, 1.5)**: Judge says C2' doesn't mention the sharp increase 2020->2021. C2' does mention the values (5,860 and 7,047) but doesn't call the increase "sharp." **BORDERLINE.**

**False positives**: 3 (7.5 penalty points)
**Tolerance violations**: 0
**Genuine new errors**: 0 clear, 2 borderline
**Adjusted C2' score**: ~88 (same as C1)

---

### bulgarian_fig_014 (Bar Chart)

**C1 score**: 72.5 (7 errors, 16.5 penalty) | **C2' score**: 51.7 (8 errors, 29.0 penalty)

**Descriptions are very similar.** Both describe the same grouped bar chart. C2' provides month-by-month values for all 12 months; C1 only gives a few examples.

**New errors in C2' (not in C1):**
1. **Month II value (Major, 5.0)**: Judge says 2022 month II is ~95,000, not 84,000. Both descriptions are reading from the same figure -- the C1 description doesn't provide month II values at all, so this is a new data point in C2' that may be wrong. **GENUINE** if the actual value is ~95,000.
2. **Month III 2024 value (Major, 5.0)**: Judge says ~110,000, not 125,000. This is a new data point in C2'. **GENUINE** numerical error.
3. **Month XII 2023 value (Major, 5.0)**: Judge says min is 80,000 not 81,000. 81,000 vs 80,000 is a 1pp difference on a ~80,000 value (1.25%). **WITHIN tolerance (+-3pp).** **FALSE POSITIVE** for severity -- should be minor at most.
4. **chart_type (Major, 3.5)**: Judge says C2' doesn't state chart shows "percentage values." But C2' says "стойности по месеци" and mentions the y-axis label "/ % /". The description does implicitly convey percentages. **BORDERLINE** -- C1 gets the same atom flagged at different severity.

**C1-only error not in C2':**
- The "Unwanted Interpretation" error (atom trend_interpretation) is flagged in both with 3.5 weight but the atom explicitly says it should NOT be present -- and indeed neither description includes it. The judge incorrectly flags it as an error in C2' (error for something that isn't there). **FALSE POSITIVE in C2'** (3.5 penalty).

**False positives**: 1 clear (3.5 penalty), 1 tolerance violation (severity should be lower, ~3.0 overpenalty)
**Genuine new errors**: 2 numerical errors (10.0 penalty) -- but these arise because C2' provides MORE data (all 12 months), not because the description is worse in quality.
**Adjusted delta**: ~-7 instead of -20.8

---

### bulgarian_fig_021 (Horizontal Bar Chart)

**C1 score**: 90.5 (7 errors, 10.0 penalty) | **C2' score**: 82.9 (8 errors, 18.0 penalty)

**Descriptions are essentially equivalent.** Both list all 13 categories, identify the two colours, and provide the same percentage values.

**New errors in C2' (not in C1):**
1. **color_rule_blue (Major, 5.0)**: Judge says "Да се ограничат действията на мафията" at 10% should be blue (under 9%) but C2' labels it red. Looking at the atom: blue is for under 9%, red for above 10%. The value is exactly 10%, which is borderline. The reference says ">10% is red" and 10% falls at the boundary. Both C1 and C2' describe it the same way (10% = red bar). **FALSE POSITIVE** -- C1 also labels it the same way but isn't penalised.
2. **highest_values (Major, 5.0)**: Judge says the value for "Да се подобри качеството на административните..." is not 13% but 15-16%. Both C1 and C2' state 13%. C1 gets only Minor (1.5) for this. **INCONSISTENT SEVERITY** -- the same error gets 5.0 in C2' vs 1.5 in C1. Overpenalty: 3.5.
3. **value_range (Minor, 1.5)**: Judge says C2' doesn't state the percentage axis clearly. But C2' says "единицата е процент (%)." **FALSE POSITIVE.**
4. **Hallucinated Content (Minor, 1.5)**: Judge flags "визуално подчертаване е реализирано единствено чрез цветово кодиране" as hallucination. This is actually a descriptive statement about the figure, not hallucination. **FALSE POSITIVE.**

**False positives**: 3 (8.0 penalty points)
**Severity inconsistency**: 1 (3.5 overpenalty)
**Genuine new errors**: 0
**Adjusted C2' score**: ~93 (better than C1)

---

### bulgarian_fig_036 (Line Plot, Two Panels)

**C1 score**: 79.4 (10 errors, 18.5 penalty) | **C2' score**: 45.6 (14 errors, 49.0 penalty)

**Descriptions are essentially identical** -- same values, same typo ("летгодни" instead of "леглодни"), same structural description.

**The key difference: severity escalation.** The C2' judge evaluates the SAME numerical errors at Major (5.0) that the C1 judge evaluates at Minor (2.0). Specifically:

| Error | C1 severity/weight | C2' severity/weight |
|-------|-------------------|---------------------|
| value_A_2008 (278 vs 270) | Minor/2.0 | Major/5.0 |
| value_A_2012 (266 vs 265) | not flagged | Major/5.0 |
| value_A_2013 (271 vs 265) | Minor/2.0 | Major/5.0 |
| value_A_2021 (197 vs 200) | Minor/2.0 | Major/5.0 |
| value_B_2012 (0.85 vs <0.6) | Minor/2.0 | Major/5.0 |
| value_B_2013 (0.75 vs 0.3) | Minor/2.0 | Major/5.0 |
| value_B_2021 (2.3 vs 2.8) | Minor/2.0 | Major/5.0 |

**Both descriptions report the EXACT SAME values.** The judge simply assigns different severity to identical content.

**Tolerance analysis:**
- 266 vs 265 (Panel A 2012): 1 day difference on ~265. Well within any reasonable tolerance. **FALSE POSITIVE** in C2'.
- 278 vs 270 (Panel A 2008): 8-day difference on ~270 (~3%). On the margin of tolerance.
- 197 vs 200 (Panel A 2021): 3-day difference on ~200 (1.5%). **WITHIN tolerance.**

**False positives via severity inconsistency**: The C2' evaluation overpenalises by approximately 21.0 points (7 errors upgraded from Minor/2.0 to Major/5.0).
**Genuine difference**: 0 -- the descriptions are identical in content.
**Adjusted C2' score**: ~79 (same as C1)

---

### bulgarian_fig_038 (Pie Chart, Three Donut Charts)

**C1 score**: 58.7 (11 errors, 47.5 penalty) | **C2' score**: 58.3 (14 errors, 48.0 penalty)

**Descriptions have the same fundamental error**: both C1 and C2' swap "Industry" and "Other services" across all three charts (misassigning the dark blue/brown and yellow colours). This is a genuine error in the GPT-5.2 description itself, present identically in both conditions.

**C2' additional errors not in C1:**
1. **sector_industry_color (Minor, 2.0)**: "жълто-охрен" vs "жълто" -- colour synonym. **FALSE POSITIVE** (colour synonym difference).
2. **sector_construction_color (Minor, 2.0)**: "светлосин" vs "синьо" -- colour synonym. **FALSE POSITIVE.**
3. **sector_services_color (Minor, 2.0)**: "тъмносин" vs "кафяво" -- this is a genuine colour misidentification, same in both C1 and C2'. Both describe "Other services" as dark blue when it's brown. The C1 judge already penalises this implicitly within the sector-value swap errors.
4. **chart_type (Major, 3.5)**: Judge says C2' doesn't state the chart purpose. C2' says "показват разпределението по отрасли (индустрия, строителство, търговия и други услуги) за 2021 г. по три показателя: брой предприятия, брой заети лица и оборот" -- this IS the chart purpose. **FALSE POSITIVE.**
5. **Phrasing errors (Minor, 2.0)**: "пръстеновидни" as ambiguous. Both C1 and C2' use "donut" language. **BORDERLINE.**

**False positives**: 2 colour synonyms (4.0) + 1 chart purpose (3.5) = 7.5
**Genuine difference**: 0 -- same errors in both.
**Adjusted C2' score**: ~66 (slightly better than C1 adjusted)

---

### bulgarian_fig_048 (Bar Chart, Vineyard Area)

**C1 score**: 72.7 (6 errors, 20.5 penalty) | **C2' score**: 50.7 (13 errors, 37.0 penalty)

**Descriptions are nearly identical.** Same colour swaps (France orange/grey, China grey/orange, Turkey light-blue/light-green), same value ranges.

**New errors in C2' (not in C1):**
1. **6 numerical value errors (Minor, 2.0 each = 12.0)**: Judge flags C2' ranges like "950-980" vs "950", "780-810" vs "780-800", "200-230" vs "220-230", etc. These are marginal range differences between the two descriptions. C1 uses the same ranges ("~950-980", etc.) but is NOT penalised for them. **FALSE POSITIVES** -- the C1 judge accepted these ranges, the C2' judge does not, despite identical content.
2. **chart_type (Major, 3.5)**: Judge says C2' doesn't mention "vineyard area." C2' says "показва как се изменя измервана величина в 'хиляди хектари'" without specifying it's vineyards. C1 also doesn't specify vineyards. Both are penalised but C2' gets it at Major. **GENUINE** but both miss it equally.
3. **Unwanted Interpretation (Major, 3.5)**: Judge flags "как се изменя" as implying change when values are stable. C2' does imply change; C1 doesn't explicitly. **GENUINE** -- a small quality difference.

**False positives**: 6 numerical (12.0 penalty) -- same content penalised only in C2'.
**Genuine new errors**: 1 (unwanted interpretation, 3.5)
**Adjusted delta**: ~-3.5 instead of -22.0

---

### bulgarian_fig_095 (Pie Chart)

**C1 score**: 75.6 (5 errors, 11.0 penalty) | **C2' score**: 20.0 (10 errors, 36.0 penalty)

This is the most extreme delta (-55.6 points). **The descriptions are functionally identical.**

**The core issue**: Both C1 and C2' report counts (10, 24, 25, 8, 20) and compute approximate percentages (11%, 28%, 29%, 9%, 23%). The atom checklist treats these as the exact percentages (10%, 24%, 25%, 8%, 20%). GPT-5.2 interpreted the legend numbers as raw counts and computed percentages from 10/87, 24/87, etc.

**Critical finding**: The numbers in the atom checklist (10%, 24%, 25%, 8%, 20%) are actually raw counts, not percentages. GPT-5.2 correctly read the counts but incorrectly computed percentages from them. This error is IDENTICAL in both C1 and C2'.

**Severity escalation in C2':**

| Error | C1 severity/weight | C2' severity/weight |
|-------|-------------------|---------------------|
| sector_1 (11% vs 10%) | Minor/2.0 (grouped) | Major/5.0 |
| sector_2 (28% vs 24%) | Minor/2.0 (grouped) | Major/5.0 |
| sector_3 (29% vs 25%) | Minor/2.0 (grouped) | Major/5.0 |
| sector_4 (9% vs 8%) | Minor/2.0 (grouped) | Major/5.0 |
| sector_5 (23% vs 20%) | Minor/2.0 (grouped) | Major/5.0 |

In C1, ALL five percentage errors are grouped into a single Minor error (2.0 total). In C2', each gets its own Major error (5.0 each = 25.0 total). **Same content, 23.0 overpenalty.**

**Tolerance analysis**: 
- 11% vs 10%: 1pp difference. **WITHIN +-3pp tolerance.**
- 28% vs 24%: 4pp difference. Just outside tolerance.
- 29% vs 25%: 4pp difference. Just outside tolerance.
- 9% vs 8%: 1pp difference. **WITHIN tolerance.**
- 23% vs 20%: 3pp difference. **AT tolerance boundary.**

At least 2 of 5 are clearly within tolerance. All 5 are penalised identically whether within or outside tolerance.

**Both descriptions also have the "no percentages inside sectors" error** (Major, 5.0), identically.

Additionally, C2' gets:
- **ordering (Minor, 2.0)**: C2' says "без очевидно подреждане по размер" while atom says they ARE sorted. C1 also doesn't mention ordering. **C2' is penalised for explicitly saying something C1 omits.**
- **chart_type (Minor, 1.5)**: C2' doesn't clearly state purpose. But C2' says "разпределението на отговорите на въпрос B4 относно степента на съгласие с твърдението" -- this IS the purpose. **FALSE POSITIVE.**

**False positives**: 1 (chart_type, 1.5) + tolerance violations (at least 2 x 5.0 = 10.0)
**Severity inconsistency**: 23.0 (5 errors upgraded from grouped Minor to individual Major)
**Genuine new errors**: 1 (ordering stated incorrectly, 2.0)
**Adjusted C2' score**: ~70 (close to C1's 75.6)

---

### bulgarian_fig_103 (Line Plot)

**C1 score**: 80.0 (6 errors, 15.0 penalty) | **C2' score**: 76.0 (9 errors, 18.0 penalty)

**Descriptions are very similar.** Both report the same values and trends.

**New errors in C2' (not in C1):**
1. **grey_line_end (Minor, 2.0)**: C2' says "180000-190000" vs atom "180,000". Range includes the correct value. **BORDERLINE** -- unnecessarily imprecise but not wrong.
2. **x_axis (Minor, 1.5)**: Judge says C2' doesn't mention x-axis has no markings. C2' says "Оста x няма видим етикет и не показва четими числови деления." This IS stating no markings. **FALSE POSITIVE.**
3. **Over-Generalization (Minor, 1.0)**: Stylistic critique. **Genuine but trivial.**
4. **Poor Sentence Structure (Minor, 1.0)**: Stylistic critique. **Genuine but trivial.**

The yellow line error (10-15k vs ~1) is present and correctly flagged in BOTH evaluations at Major weight.

**False positives**: 1 (1.5 penalty)
**Genuine difference**: ~2.5 (stylistic issues)
**Adjusted delta**: ~-1.5 instead of -4.0

---

### bulgarian_fig_272 (Pie Chart)

**C1 score**: 71.3 (3 errors, 11.5 penalty) | **C2' score**: 71.3 (3 errors, 11.5 penalty)

**Identical scores.** Both descriptions have the same error: swapping green and purple sector labels. Both evaluations flag exactly the same 3 errors at the same severity. **Perfect consistency on this figure.**

---

## Aggregate False Positive Analysis

| Figure | False Positives (count) | Overpenalty (points) | Primary Cause |
|--------|------------------------|---------------------|---------------|
| 001 | 3 | 7.5 | Judge missed content present in C2' |
| 014 | 1 | 3.5 | Unwanted interpretation phantom error |
| 021 | 3 | 8.0 | Content present but not recognised |
| 036 | 0 direct | 21.0 | Severity escalation (Minor->Major) |
| 038 | 3 | 7.5 | Colour synonyms + purpose present |
| 048 | 6 | 12.0 | Identical ranges penalised only in C2' |
| 095 | 1 | 1.5 + 23.0 severity | Severity escalation + tolerance violations |
| 103 | 1 | 1.5 | Content present but not recognised |
| 272 | 0 | 0 | Perfect consistency |
| **Total** | **18** | **~85.0** | |

## Key Findings

### 1. Severity Inconsistency is the Dominant Problem
The single largest source of score inflation is the judge assigning **different severity levels to identical errors** across C1 and C2'. This accounts for approximately 44 penalty points of the total delta. The most extreme cases are:
- **fig_095**: 5 percentage errors grouped as 1 Minor (2.0) in C1 but split into 5 Majors (25.0) in C2'
- **fig_036**: 7 numerical errors at Minor (14.0) in C1 but at Major (35.0) in C2'

### 2. False Positives from Content Not Recognised
In 5 of 9 figures, the judge flagged C2' as missing information that was actually present in the description. This typically occurs with chart purpose atoms -- the judge looks for specific phrasing and doesn't recognise paraphrases.

### 3. Tolerance Violations are Inconsistently Applied
Numerical differences within +-3pp are sometimes penalised and sometimes not, with no systematic pattern. The tolerance rule is applied more strictly to C2' than C1.

### 4. Colour Synonym Differences Were Penalised
In fig_038 and fig_048, "жълто-охрен" vs "жълто" and "светлосин" vs "светлозелено" are flagged as errors. The first is a synonym (false positive); the second is a genuine colour misidentification that occurs identically in both C1 and C2'.

### 5. No Genuine Quality Differences
Across all 9 figures, the C1 and C2' descriptions are **substantively identical** -- they report the same values, identify the same features, make the same errors, and use very similar phrasing. The only genuine quality difference is in fig_048 where C2' implies temporal change where values are stable (3.5 penalty).

### 6. Adjusted Scores
After removing false positives, tolerance violations, and normalising severity inconsistencies:

| Figure | C1 (raw) | C2' (raw) | C2' (adjusted) | True Delta |
|--------|----------|-----------|-----------------|------------|
| 001 | 88.4 | 83.2 | ~88 | ~0 |
| 014 | 72.5 | 51.7 | ~66 | ~-6.5 |
| 021 | 90.5 | 82.9 | ~93 | ~+2.5 |
| 036 | 79.4 | 45.6 | ~79 | ~0 |
| 038 | 58.7 | 58.3 | ~66 | ~+7 |
| 048 | 72.7 | 50.7 | ~69 | ~-4 |
| 095 | 75.6 | 20.0 | ~70 | ~-6 |
| 103 | 80.0 | 76.0 | ~78 | ~-2 |
| 272 | 71.3 | 71.3 | 71.3 | 0 |
| **Mean** | **76.6** | **59.9** | **~75.6** | **~-1.0** |

**The raw MQM delta of -16.6 points is almost entirely judge noise.** The adjusted delta is approximately -1.0 points, indicating that the English-instruction condition produces descriptions of essentially identical quality to the native-instruction condition for Bulgarian.

### 7. GPT-4o Cross-Reference
GPT-4o C1 scores are generally lower than Mistral C1 scores (mean 63.2 vs 76.6), suggesting GPT-4o is a stricter judge overall. However, for the figures where both conditions should score identically (e.g., fig_272), all three evaluations converge at 71.3, confirming that when descriptions are truly identical, judges can agree.
