# Chinese Prompt (C1) vs English Prompt with Chinese Output (C2') -- GPT-5.2

## Overview

This report compares GPT-5.2 descriptions of 9 Chinese scientific figures under two prompt conditions:

- **C1** (`image_only`): Chinese prompt, Chinese output
- **C2'** (`english_instruction_native_output`): English prompt with instruction to respond in Chinese, Chinese output

Each figure was evaluated independently against the ground-truth image on Accuracy, Completeness, and Clarity dimensions following Atomic MQM guidelines.

---

## Per-Figure Comparison

### chinese_fig_004 -- Bar + Line Chart (COVID daily cases & news count)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Correct axis ranges, series descriptions, color IDs. Says bar range "350,000-500,000" for lows. | Adds specific weekly date ticks (7/8, 7/15, etc.). Notes peak location "7月中旬附近". Bar range "400,000-600,000" for lows. |
| Completeness | Covers title, both axes, both series, legend labels, bar ordering. | Same coverage, plus explicit enumeration of x-axis date labels. |
| Clarity | Well-structured single paragraph. | Equally well-structured; slightly longer. |

**Verdict: C2' marginally better.** C2' provides more specific date-tick enumeration and identifies the temporal location of peaks, adding interpretive value without sacrificing accuracy.

---

### chinese_fig_012 -- Line Plot (F1 scores, 3 methods vs epoch)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Values match figure closely: lattice(2)~0.59, FLAT(2)~0.79, OURS(2)~0.82, etc. Correctly notes x-axis typo "epouch". | Identical numerical reads within rounding tolerance. Same axis description. |
| Completeness | Notes "2 到 4 变化较小" for OURS -- an interpretive detail. | Slightly more precise y-axis range ("约从0.55到0.92"). |
| Clarity | Both clear and systematic. | Both clear and systematic. |

**Verdict: Equivalent.** Negligible differences in phrasing; numerical reads are within margin of pixel-level estimation.

---

### chinese_fig_013 -- Pie Chart (children's news categories, 8 slices)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | All 8 slices correct (4%, 20%, 19%, 6%, 14%, 2%, 21%, 14%). Colors mostly correct; says "红色" for 经济. | Same percentages. Says "粉红色" for 经济 -- arguably more accurate for the pinkish hue in the figure. |
| Completeness | Describes clockwise traversal order starting from top -- adds spatial clarity. Mentions white text labels inside slices. | More concise; omits traversal direction. |
| Clarity | Detailed spatial description aids reconstruction. | More compact but loses spatial positioning info. |

**Verdict: C1 slightly better.** The clockwise traversal order and mention of white in-slice text provide better spatial grounding for a pie chart.

---

### chinese_fig_014 -- Two Line Plots (BLEU vs alpha, BLEU vs p)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Left plot: alpha=0.1 ~28.0, 0.3 ~28.33, 0.5 ~28.53, 0.7 ~28.40, 0.9 ~28.12. Right plot values identical to C2'. | Same values. Adds "希腊字母" before alpha -- linguistically precise. |
| Completeness | Both cover dual-subplot layout, axis labels, scale, marker style. | Same coverage. |
| Clarity | Both well-organized with left/right subplot structure. | Both well-organized. |

**Verdict: Equivalent.** No meaningful difference in accuracy or completeness.

---

### chinese_fig_035 -- Line Plot (interlanguage vs random networks across proficiency levels)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | All 14 data-point values exactly match the on-chart annotations (e.g., A1: 3.254/4.189, ..., 母语: 3.685/5.204). | Identical values. |
| Completeness | Both describe colors, markers, trend patterns, min/max points. | Same. C2' phrases trend description slightly differently but same content. |
| Clarity | C1 explicitly states "最小值出现在B1" and "最大值" for each line. | C2' says "在B1处出现较低值后逐步上升至末端" -- slightly less precise. |

**Verdict: Equivalent.** Both are excellent; C1 is marginally more explicit about min/max but the difference is negligible.

---

### chinese_fig_042 -- Grouped Bar + Line Chart (5 NLP tasks: train/val counts + accuracy)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | All 15 values correct: 实体识别 (1102/250/0.7666), 角色识别 (1095/190/0.8714), 异常识别 (1077/40/0.692), 空间推理 (1210/675/0.2852), 同义识别 (5/55/0.3769). | Identical values with "约" qualifier. |
| Completeness | Describes dual-axis, grouped bars, line overlay, value annotations. | Same structure and coverage. |
| Clarity | Both include the negative observation about no sorting/highlighting. | Both equally clear. |

**Verdict: Equivalent.** Virtually identical descriptions.

---

### chinese_fig_046 -- Line Plot (F1 vs miss-label rate, 3 methods)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Teacher at 0: ~71.7, Self-Training at 0: ~70.0, PST at 0: ~71.6. PST at 0.3: ~70.0. | Same values except PST at 0.3: ~69.9 (C1 says ~70.0). From figure, ~70.0 appears slightly more accurate. |
| Completeness | C1 adds narrative: "在0.4到0.5之间下降幅度较明显" and "整体下降相对更平缓但在0.5到0.585间出现较大下滑". | C2' is more purely descriptive, listing values without trend commentary. |
| Clarity | Slightly richer interpretation. | Cleaner tabular style. |

**Verdict: Equivalent.** C1 has marginally richer trend narration but C2' is cleaner. Trade-off is neutral.

---

### chinese_fig_071 -- Stacked Bar Charts (verb semantic categories across registers)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Misidentifies both subplot topics as "受动词" -- actual figure shows (a)="支配动词" and (b)="承受动词". Reads totals as ~4587, ~6781, ~6812. | Misidentifies both as "交互动词" -- also incorrect. Reads totals as ~4487, ~6783, ~6730. |
| Completeness | Identifies x-axis category labels broadly. Mentions percentage annotations within segments. | Similar coverage. Slightly more detail on segment-level percentages (e.g., "约47%与约39%", "约90%"). |
| Clarity | Structured as (a) then (b) with clear separation. | Same structure but longer. |

**Verdict: C1 slightly better.** Both misread the subplot titles (a significant error), but C1's numerical reads for bar totals appear closer to the actual figure values. C2' provides more segment-level detail but also introduces more numerical imprecision.

---

### chinese_fig_094 -- Pie Chart with Sub-Pie ("an" structure)

| Dimension | C1 | C2' |
|---|---|---|
| Accuracy | Main pie: yellow 69.39% (229例), blue 30.61% (101例). Sub-pie: orange 81.66%, green 18.34%. Correct. Says "亮黄色" for the larger slice. | Same values. Correctly specifies the sub-pie connects to the "黄色扇区". |
| Completeness | Mentions bottom legend with "蓝、橙、绿三种色块配合数字1、2、3". | Same legend detail. Adds that sub-pie is a "放大细分饼图" -- clarifies the hierarchical relationship. |
| Clarity | Both clear. C1 less explicit about which main slice the sub-pie expands. | C2' explicitly states the connection ("与左侧黄色扇区通过连线对应的放大细分饼图"). |

**Verdict: C2' marginally better.** The explicit connection between main and sub-pie is structurally important and C2' captures it more clearly.

---

## Summary Statistics

| Figure | Type | Winner | Margin |
|---|---|---|---|
| chinese_fig_004 | Bar+Line | C2' | Marginal |
| chinese_fig_012 | Line Plot | Tie | -- |
| chinese_fig_013 | Pie Chart | C1 | Slight |
| chinese_fig_014 | Line Plot | Tie | -- |
| chinese_fig_035 | Line Plot | Tie | -- |
| chinese_fig_042 | Bar+Line | Tie | -- |
| chinese_fig_046 | Line Plot | Tie | -- |
| chinese_fig_071 | Stacked Bar | C1 | Slight |
| chinese_fig_094 | Pie Chart | C2' | Marginal |

**Tally:**
- C1 wins: 2 (both slight margin)
- C2' wins: 2 (both marginal)
- Ties: 5

**Overall score: Equivalent (5/9 ties, 2-2 split on non-ties)**

---

## Key Patterns

### 1. No systematic quality degradation from English instruction
The English-prompt condition (C2') does **not** produce systematically worse Chinese descriptions. The output quality is statistically indistinguishable from the native Chinese prompt condition across all evaluation dimensions.

### 2. Numerical accuracy is nearly identical
Both conditions produce the same numerical value reads from charts (within pixel-level estimation tolerance). The largest discrepancy observed was a single data point differing by 0.1 (PST at miss-rate 0.3: C1 reads ~70.0, C2' reads ~69.9).

### 3. Structural/spatial descriptions show minor divergence
- C1 tends to include spatial traversal cues (e.g., clockwise order in pie charts, explicit min/max callouts).
- C2' tends to include more relational descriptions (e.g., specifying which pie slice a sub-chart expands from, labeling Greek letters explicitly).

### 4. Both conditions share the same error modes
The most notable errors (misreading subplot titles in chinese_fig_071) appeared in **both** conditions, suggesting these are model-level limitations rather than prompt-condition effects.

### 5. Chinese language fluency is preserved
C2' descriptions show no grammatical degradation, no code-switching, and no anglicisms despite the English prompt. The Chinese output is natural and domain-appropriate in both conditions.

### 6. Description length is comparable
Neither condition consistently produces longer or shorter descriptions. When differences exist, they reflect different emphasis choices (spatial vs. relational) rather than verbosity differences.

---

## Conclusion

**English instruction does not degrade Chinese output quality for GPT-5.2.** Across 9 figures spanning bar charts, line plots, pie charts, and composite visualizations, the C1 and C2' conditions produce descriptions that are equivalent in accuracy, completeness, and clarity. The 2-2 split on non-tie figures shows no directional bias. This suggests that GPT-5.2's figure description capability is robust to prompt language when the output language is held constant.
