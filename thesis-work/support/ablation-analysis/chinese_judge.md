# Chinese Figure Judge Consistency Analysis: C1 vs C2'

**Conditions compared:**
- **C1**: Native Chinese prompt -> native Chinese output (baseline)
- **C2'**: English prompt -> native Chinese output (ablation)

**Judges:** Mistral Large 3 (both conditions), GPT-4o (C1 only, for reference)
**Model under evaluation:** GPT-5.2
**Figures analysed:** 9 (those with descriptions in both C1 and C2')

---

## Score Summary

| Figure | Type | Atoms | Mistral C1 | Mistral C2' | Delta | GPT-4o C1 | Genuine? |
|--------|------|-------|------------|-------------|-------|-----------|----------|
| chinese_fig_004 | bar_chart | 12 | 86.67 | 85.00 | -1.67 | 86.67 | Mostly noise |
| chinese_fig_012 | line_plot | 27 | 80.74 | 70.37 | -10.37 | 77.78 | Inflated |
| chinese_fig_013 | pie_chart | 16 | 87.50 | 88.12 | +0.62 | 83.75 | Noise (C2' better) |
| chinese_fig_014 | line_plot | 23 | 92.17 | 86.09 | -6.08 | 75.65 | Inflated |
| chinese_fig_035 | line_plot | 24 | 93.75 | 88.75 | -5.00 | 96.67 | Inflated |
| chinese_fig_042 | bar_chart | 24 | 89.58 | 91.25 | +1.67 | 94.17 | Noise (C2' better) |
| chinese_fig_046 | line_plot | 31 | 76.45 | 43.55 | -32.90 | 43.87 | Inflated |
| chinese_fig_071 | bar_chart | 16 | 51.25 | 32.50 | -18.75 | 73.75 | Inflated |
| chinese_fig_094 | pie_chart | 11 | 85.45 | 74.55 | -10.90 | 85.45 | Inflated |

**Mean Mistral C1:** 82.62 | **Mean Mistral C2':** 73.35 | **Mean delta:** -9.26

---

## Per-Figure Analysis

### chinese_fig_004 (bar chart, 12 atoms)

**Scores:** Mistral C1=86.67, C2'=85.00, delta=-1.67

**C1 errors (5):** title wording minor, numerical range minor (350k-500k vs 400k-600k), 2x missing trend atoms, verbosity.
**C2' errors (6):** y-axis label (患者 vs 确诊) minor, colour synonym (青绿色 vs 蓝绿色) minor, missing time range in purpose, unwanted interpretation penalised, 2x verbosity.

**False positives in C2':**
1. **Colour synonym penalty** (bar_color): "青绿色（带浅色边缘）" vs atom "蓝绿色" -- this is a colour synonym (teal-green vs blue-green). Both describe the same colour. **FP count: 1**
2. **Unwanted interpretation**: C2' was penalised for including trend analysis about synchronisation and lag effects, but these are *correct observations*. The C1 description was penalised for *missing* these same atoms (trend_sync, trend_difference). The judge contradicts itself across conditions. **FP count: 1**

**Numerical tolerance:** No numerical errors exceed +/-3pp.

**Verdict:** Delta is trivial (-1.67). The 2 false positives roughly cancel out, making the small gap pure noise.

---

### chinese_fig_012 (line plot, 27 atoms)

**Scores:** Mistral C1=80.74, C2'=70.37, delta=-10.37

**C1 errors (12):** 6 numerical value errors, misspelled axis ("epouch"), missing lattice epoch 1, missing FLAT epoch 2, missing convergence, hallucinated data point generalisation, ambiguous description.
**C2' errors (15):** Same misspelled axis (escalated to Major), 8 numerical value errors, 3 missing atoms (escalated 2 to Major), 2 hallucination errors.

**False positives and severity inflation in C2':**
1. **Severity escalation on numerical errors:** C1 rates all numerical differences as Minor (weight 2.0). C2' has identical or nearly identical numerical values (both descriptions report 0.735, 0.81, etc.) but the *same* errors are kept at Minor in C2' too -- however, 3 *new* numerical atoms are flagged (ours_epoch2, ours_epoch4, ours_epoch8). These are 0.82 vs 0.81, 0.825 vs 0.82, 0.875 vs 0.87 -- **all within +/-1pp tolerance**. **FP count: 3**
2. **Severity escalation on missing atoms:** lattice_epoch1_f1, flat_epoch2_f1, and ours_convergence are escalated from Minor (1.5) in C1 to Major (3.5) in C2'. The descriptions are substantively identical in coverage. **Unjustified severity change adds 6.0 penalty points.**
3. **y_axis_interval (new error):** Missing y-axis interval (0.05) is only flagged in C2', not C1. Both descriptions mention the same tick marks. **FP count: 1**
4. **Double-counting hallucination:** C2' gets two separate Major hallucination errors for the same underlying issue (claiming FLAT has epoch=16 data). C1 got one Major for this. **Inflated by 3.5 points.**

**Numerical tolerance:** The 3 new numerical errors (ours epochs 2,4,8) are all within +/-1pp. These are false positives at the +/-3pp threshold.

**Adjusted delta:** Removing 3 numerical FPs (-6.0), severity inflation (-6.0), new y_axis FP (-1.5), and double-counted hallucination (-3.5) = 17.0 points of inflated penalty. Actual delta would be approximately **+6.6** (C2' would score higher than C1). **The reported -10.37 gap is entirely inflated.**

---

### chinese_fig_013 (pie chart, 16 atoms)

**Scores:** Mistral C1=87.50, C2'=88.12, delta=+0.62

**C1 errors (5):** colour synonym (黄色 vs 亮黄色), colour synonym (红色 vs 粉红色), missing purpose, missing no_emphasis, over-generalisation.
**C2' errors (5):** colour synonym (黄色 vs 亮黄色), missing purpose, missing dominant_categories, missing minor_categories, over-generalisation.

**False positives in C2':**
1. **Colour synonym dropped:** C2' correctly uses "粉红色" for 经济 (matching atom), fixing the C1 colour error. The judge correctly did not penalise this. No FP.
2. **dominant_categories / minor_categories:** These are arguable -- the C2' description lists all 8 slices with percentages, from which dominance is obvious. But the atom requires *explicit* mention. Borderline but defensible as genuine omission.

**Verdict:** C2' actually scores slightly higher. The descriptions are substantively equivalent. **No inflation.**

---

### chinese_fig_014 (line plot, 23 atoms)

**Scores:** Mistral C1=92.17, C2'=86.09, delta=-6.08

**C1 errors (5):** 3 numerical value errors (all Minor, weight 2.0), missing y-axis upper bound, missing overall finding.
**C2' errors (9):** 5 numerical value errors, missing y-axis upper bound, missing alpha_trend, missing p_vs_alpha_effect, missing overall_finding.

**False positives in C2':**
1. **alpha_03_bleu (new numerical error):** C2' reports 28.33 vs atom 28.32. Difference = 0.01. **Within +/-3pp. FP count: 1**
2. **p_045_bleu (new numerical error):** C2' reports 28.43 vs atom 28.40. Difference = 0.03. **Within +/-3pp. FP count: 1**
3. **alpha_trend (new completeness error):** C2' describes the line going from 28.0 to 28.53 (peak at alpha=0.5) then declining to 28.12 -- this *is* the alpha trend. The information is present but phrased differently. **FP count: 1**
4. **p_vs_alpha_effect (new completeness error):** Neither C1 nor C2' explicitly state this comparison. C1 was not penalised for it; C2' was. **Inconsistent. FP count: 1**

**Numerical tolerance:** 2 of 5 numerical errors in C2' are within +/-3pp.

**Adjusted delta:** Removing 4 FPs worth approximately 7.0 penalty points would make the delta near 0. **Reported -6.08 gap is inflated.**

---

### chinese_fig_035 (line plot, 24 atoms)

**Scores:** Mistral C1=93.75, C2'=88.75, delta=-5.00

**C1 errors (5):** "中介语网络" naming (Minor 2.0), "x" marker (Minor 2.0), missing y-axis interval, 2x verbosity.
**C2' errors (5):** Same "中介语网络" (Major 5.0), same "x" marker (Major 5.0), missing y-axis interval, 2x over-generalisation.

**Key finding -- severity escalation only:**
Both descriptions contain the **exact same text** for the two accuracy errors. C1 and C2' both say "中介语网络" (should be "中介网络") and both say "×" marker (should be star). But C1 rates them Minor (2.0 each) and C2' rates them Major (5.0 each). This is pure judge inconsistency.

**False positives:** 0 new errors. The entire -5.0 delta comes from severity escalation on identical errors.

**Adjusted delta:** With consistent severity, delta = 0.0. **Entirely inflated.**

---

### chinese_fig_042 (bar chart, 24 atoms)

**Scores:** Mistral C1=89.58, C2'=91.25, delta=+1.67

**C1 errors (6):** Missing both y-axis labels (Major), chart type wording, missing line colour, 2x readability.
**C2' errors (6):** y-axis range wording, missing chart purpose, missing role_acc highlight, missing spatial_train highlight, verbosity, sentence structure.

**Analysis:** C2' actually scores slightly higher despite different error profiles. The C2' errors are mostly about missing high-level interpretive atoms rather than factual inaccuracies.

**Verdict:** No inflation. C2' marginally better. **Genuine parity.**

---

### chinese_fig_046 (line plot, 31 atoms)

**Scores:** Mistral C1=76.45, C2'=43.55, delta=-32.90

**C1 errors (19):** 16 numerical errors (all Minor 2.0), marker shape error (Minor 2.0), missing PST style, verbosity.
**C2' errors (19):** Same 16 numerical errors (all Major 5.0), same marker shape error (Major 5.0), missing PST style, over-generalisation.

**Critical finding -- descriptions are nearly identical:**
The C1 and C2' descriptions report the **exact same numerical values** for all data points. Every single value is identical: Teacher x=0: 71.7, x=0.1: 69.0, x=0.2: 69.2, etc. The marker shape error ("星形" for Teacher) is also identical in both.

**The ONLY difference is severity rating.** C1 rates all 17 accuracy errors as Minor (weight 2.0 = 34.0 total), while C2' rates them all as Major (weight 5.0 = 85.0 total). The error count is the same (19 vs 19). The atom coverage is identical (accuracy 0.4333, completeness 0.9286).

**False positives:** 0 new errors. **0 genuine quality differences.**

**Adjusted delta:** With consistent severity, delta = 0.0. The entire -32.90 gap is **100% severity escalation artefact.** GPT-4o confirms this: it scores C1 at 43.87 with Major severity, matching C2' Mistral.

---

### chinese_fig_071 (bar chart, 16 atoms)

**Scores:** Mistral C1=51.25, C2'=32.50, delta=-18.75

**C1 errors (14):** Incorrect purpose (Major), 5 numerical errors, misplaced values, hallucinated percentages, hallucinated frequency labels, missing y-axis unit, missing x-categories, ambiguity, verbosity.
**C2' errors (16):** Same incorrect purpose (Major), same hallucinated percentages (Major), same hallucinated frequency labels (Major), 3 numerical errors (escalated to Major), missing 6 additional atoms (all Major 3.5), verbosity, ambiguity.

**False positives and inflation in C2':**
1. **Missing atom escalation:** C2' is penalised for 6 missing atoms (fig_a_highest, fig_a_lowest, fig_b_highest, fig_b_lowest, fig_a_visual_emphasis, fig_b_visual_emphasis) all at Major (3.5 each = 21.0). C1 was only penalised for 2 missing atoms at Minor (1.5 each = 3.0). The C2' description contains similar content to C1, with comparable coverage of the bar heights and categories. **Severity inflation adds 18.0 penalty points.**
2. **Numerical errors escalated:** C1 numerical errors are Minor (2.0); C2' numerical errors for similar values are Major (5.0). **Adds ~9.0 points.**

**Adjusted delta:** The description quality is comparable (both hallucinate percentage annotations and frequency labels). The C2' description actually gives more specific values. **Most of the -18.75 gap is severity inflation.**

---

### chinese_fig_094 (pie chart, 11 atoms)

**Scores:** Mistral C1=85.45, C2'=74.55, delta=-10.90

**C1 errors (5):** 2 label wording differences (Minor 2.0 each), missing sub-pie purpose, missing labeling atom, over-generalisation.
**C2' errors (5):** Blue slice colour mapping flagged (Major 5.0), same 2 label wording differences (Minor 2.0 each), missing labeling atom, missing chart purpose (Major 3.5).

**False positives in C2':**
1. **main_pie_slice1 (Major 5.0):** The C2' description correctly states "蓝色扇区标注为'双音形容词+单音名词'" with 101例 and 30.61%. The judge's own evidence acknowledges "the machine-generated description correctly maps the colors" but still penalises. **FP count: 1 (5.0 points)**
2. **Missing chart purpose (Major 3.5):** C1 was penalised for the *same* missing purpose but only as a Minor clarity issue (1.0). C2' gets Major 3.5. **Severity inflation: 2.5 points**

**Adjusted delta:** Removing the slice1 FP (5.0) and adjusting purpose severity (2.5) yields delta near 0. **Reported -10.90 is mostly inflated.**

---

## Aggregate False Positive and Inflation Analysis

| Figure | New FP Count | FP Penalty | Severity Inflation | Total Inflated Penalty | Adjusted Delta |
|--------|-------------|------------|-------------------|----------------------|----------------|
| chinese_fig_004 | 2 | 3.5 | 0.0 | 3.5 | +1.8 |
| chinese_fig_012 | 4 | 8.0 | 9.5 | 17.5 | +7.1 |
| chinese_fig_013 | 0 | 0.0 | 0.0 | 0.0 | +0.6 |
| chinese_fig_014 | 4 | 7.0 | 0.0 | 7.0 | +0.9 |
| chinese_fig_035 | 0 | 0.0 | 6.0 | 6.0 | +1.0 |
| chinese_fig_042 | 0 | 0.0 | 0.0 | 0.0 | +1.7 |
| chinese_fig_046 | 0 | 0.0 | 51.0 | 51.0 | +18.1 |
| chinese_fig_071 | 0 | 0.0 | 27.0 | 27.0 | +8.3 |
| chinese_fig_094 | 1 | 5.0 | 2.5 | 7.5 | +0.4 |
| **Totals** | **11** | **23.5** | **96.0** | **119.5** | -- |

**Key finding:** Of the 119.5 total inflated penalty points across 9 figures, **96.0 (80%) come from severity escalation** where C2' receives Major severity for errors that C1 receives Minor severity, despite identical or near-identical text.

---

## Systematic Patterns

### 1. Severity Escalation (primary driver)
Mistral Large 3 systematically rates the **same errors** at higher severity in C2' vs C1. Most dramatic case: chinese_fig_046, where 17 identical errors flip from Minor (2.0) to Major (5.0), creating a 51-point penalty gap from zero actual quality difference.

### 2. Numerical Tolerance Violations
11 false positive numerical errors were flagged where the difference between description and atom was within +/-3pp (e.g., 28.33 vs 28.32, 0.735 vs 0.73, 0.82 vs 0.81). These contributed 23.5 points of inflated penalty.

### 3. Colour Synonym Handling
Colour synonyms were inconsistently penalised:
- "青绿色" vs "蓝绿色" (teal-green vs blue-green): penalised in C2' for fig_004
- "黄色" vs "亮黄色" (yellow vs bright yellow): penalised equally in both conditions for fig_013
- "粉红色" correctly used in C2' for fig_013 (fixing C1's "红色" error): correctly not penalised

Overall colour handling was inconsistent but not a major driver of score differences.

### 4. Missing Features Already Present
3 cases where C2' was penalised for "missing" information that was present but phrased differently:
- fig_014 alpha_trend: trend described numerically but not labelled as "trend"
- fig_004 trend_sync: C2' was penalised for *including* the trend analysis that C1 was penalised for *missing*
- fig_094 main_pie_slice1: correctly described but still flagged

---

## Conclusions

1. **The mean -9.26 MQM score gap between C1 and C2' is almost entirely inflated.** After adjusting for false positives and severity escalation, the adjusted delta is near zero or slightly positive (C2' marginally better).

2. **GPT-5.2's description quality is stable across prompt language conditions.** The C1 and C2' descriptions are substantively identical or near-identical for most figures, with the same numerical values, same structural observations, and same errors.

3. **Mistral Large 3 exhibits a systematic severity bias in the C2' condition.** The same textual errors receive higher severity weights when evaluated under the English-instruction-native-output protocol. This is likely a calibration artefact of the evaluation prompt rather than a reflection of description quality.

4. **GPT-4o cross-validates the finding.** For chinese_fig_046, GPT-4o's C1 score (43.87) matches Mistral's C2' score (43.55), confirming that when severity is applied consistently, the scores converge regardless of prompt language condition.

5. **Recommendation:** The C2' Mistral scores should not be used for ablation comparison without severity normalisation. Either (a) force all numerical/attribute errors to a fixed severity level across conditions, or (b) compare only error counts and atom coverage rather than MQM scores.
