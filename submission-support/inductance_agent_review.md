# Inductance Blur Candidates -- Agent Review

## Summary

- **Total entries reviewed**: 46 (with targets; 5 `rejected_no_replacement` skipped)
- **OK**: 30
- **ISSUE**: 11

## Review Table

| # | figure_id | status | target | verdict | notes |
|---|-----------|--------|--------|---------|-------|
| 1 | fig_013 | approved | mBERT-B2 | OK | Target visible in legend as "mBERT-B2". Question valid: mBERT-B2 does show highest effect in case and number categories. Inferable from bar heights. |
| 2 | fig_016 | approved | 20 | OK | "20" visible on y-axis. Semitic group max effect is around 20 for mBERT-B2. Inferable from bar heights and gridlines. |
| 3 | fig_033 | approved | 30 | ISSUE | Target "30" is a y-axis tick. The "Ours (Iterative RLHF)" bar for LC AlpacaEval-2 reads approx 31-32, not 30. The answer is inferable from the bar height against the gridline, but the stated answer of 30 is slightly off. |
| 4 | fig_037 | approved | 30 | OK | "30" on y-axis. The "same" model in IE-Slavic reads approx 28, and the y-axis tick 30 is the blur target. The value is inferable from the bar and gridlines. |
| 5 | fig_038 | approved | Incorrect | OK | "Incorrect" label visible in legend with blue dotted pattern. Question asks to identify the category for blue dotted bars. Directly inferable from other legend entries (Correct is the hatched pattern). |
| 6 | fig_042 | approved | 30 | ISSUE | Target "30" is a y-axis tick. Question asks about "NoR QA" in "2WikiMQA" -- the chart shows that value is 29 (annotated above the bar). Blurring axis tick "30" and asking a question whose answer is 29 is workable, but the question says "approximate number" so it is OK. However, the answer (29) is directly annotated on the bar, so the y-axis tick "30" is not needed to answer the question -- the inductance principle is weakened since the annotation itself gives the answer without needing to infer from the blurred element. |
| 7 | fig_043 | approved | 2 | OK | "2" is visible as the value annotation on the "Overall Summary" bar. Question valid, answer directly readable and also inferable from the bar length against the x-axis. |
| 8 | fig_045 | approved | 6393 | OK | "6393" is the annotation above the 0-shot bar. Question asks total token count for 0 shots. Inferable from the bar height against the y-axis gridlines (bar reaches about 6400). |
| 9 | fig_050 | rejected | Weak Supervision | OK | "Weak Supervision" visible in legend. The question asks which approach yields less gain -- inferable from comparing bar heights (Weak Supervision bars are shorter than Strong Supervision). |
| 10 | fig_051 | rejected | 50 | ISSUE | Target "50" is a y-axis tick. Question asks about FactTune average performance -- the bar height for FactTune reads about 52. The y-axis tick "50" is the blur target, but the answer (approx 52) needs to be inferred from the bar position. The reviewer note says "50 to 53 is correct" which is reasonable. However, blurring the "50" tick makes it harder to read the FactTune bar precisely since that is the nearest reference gridline. This is borderline OK for inductance since the "40" and "60" ticks remain. Marking OK. |
| 11 | fig_052 | approved | Acc=1 & GT Ans | OK | "Acc=1 & GT Ans" visible in legend. Question asks to identify the label. Inferable from the pattern of empty/white bars in the chart matching the legend entry. |
| 12 | fig_061 | approved | 4.5 | ISSUE | Target "4.5" is a y-axis tick. Question asks entropy average for Llama under Baseline. The Baseline bar for Llama reads about 4.55. However, the y-axis tick "4.5" is visible on the chart. The answer is inferable from surrounding ticks (4.0 and 5.0). This works for inductance. Actually re-checking: the y-axis shows 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0. The Llama Baseline bar is near 4.55. If "4.5" is blurred, the value can be inferred from 4.0 and 5.0 ticks. OK for inductance. Changing to OK. |
| 13 | fig_064 | rejected | No | OK | "No" visible in legend (green bars). Question asks which Deceived option occurs least across all categories. Green "No" bars are visibly the shortest in all categories. Inferable from bar lengths. |
| 14 | fig_067 | rejected | 0.1 | ISSUE | Target "0.1" is a y-axis tick. Question asks about mBERT at "hidden:[], linear". The mBERT bar at hidden:[], linear reads about 0.08-0.09. The answer "0.1" seems approximate. The value is inferable from the 0.0 and 0.2 gridlines if 0.1 is blurred. Works for inductance but the stated answer of 0.1 does not precisely match what the chart shows (mBERT at hidden:[], linear is closer to 0.08). |
| 15 | fig_069 | rejected | 1.00 | ISSUE | Target "1.00" appears as the value annotations above the SOLAR-10.7B-v1.0 (base) bars -- every entry shows "1.00". The question asks for the average value of SOLAR across all entries. If all "1.00" annotations are blurred, the answer must be inferred from bar heights -- the SOLAR bars are uniformly the tallest, reaching the top. However, without any reference scale on the y-axis (no tick labels visible other than the annotations themselves), inferring the exact value "1.00" is difficult. The y-axis has no labeled ticks in this chart. ISSUE: answer may not be reliably inferable without annotations or y-axis scale. |
| 16 | fig_073 | rejected | Supervised_SimCSE | OK | "Supervised_SimCSE" visible on x-axis. Question asks which category is most similar to 2-Tier SimCSE. From the chart, Supervised_SimCSE has the most similar bar pattern to 2-Tier SimCSE. Inferable from visual comparison. |
| 17 | fig_083 | rejected | Increasing | OK | "Increasing" visible as label under first histogram shape. Question asks which shape has monotonically increasing bars. Inferable from the visual pattern of the bars. |
| 18 | fig_085 | approved | 30 | OK | "30" on y-axis. MMAR for Qwen2-Audio-Instruct reads about 30. Inferable from gridlines (20 and 40 remain). |
| 19 | fig_102 | approved | ChemBART Medium 20M | ISSUE | Target "ChemBART Medium 20M" appears in the legend. The question asks which model corresponds to the blue line. In this small chart, there are many lines with similar colors (red, orange, green, blue, purple, brown). The legend is quite small. "ChemBART Medium 20M" does appear to be associated with a blue-ish line. However, the chart is very small and the lines are hard to distinguish. The question is valid for inductance: if the legend label is blurred, the model can be identified from the line's training loss trajectory and color matching. OK for inductance, though chart readability is marginal. Changing to OK. |
| 20 | fig_103 | rejected | DPR w/ top-1 | OK | "DPR w/ top-1" visible in legend (green line). At 10 queries, DPR w/ top-1 (green solid) reaches the highest MRR@10 value (~36.4). Inferable from line trajectories and colors. |
| 21 | fig_104 | rejected | -25% | ISSUE | Target "-25%" is a y-axis tick. The lowest relative change is reached by the "RULER4k of 1x tokens,16-bit" (dark blue) line at Layer13-20, which dips to about -26%. The y-axis tick "-25%" is the blur target. If blurred, the value can be inferred from -15% and other ticks, but the exact answer "-25%" is the tick itself, and the actual lowest point is slightly below -25%. The question asks for the lowest value "reached by any line" which is approximately -26%, not exactly -25%. Minor mismatch between target and actual answer. |
| 22 | fig_105 | rejected | 3 x 100 | ISSUE | Target is "3 x 100" (i.e., 3 x 10^0 = 3.0 on the log scale). Question asks "What loss value does Ex1 Validation Loss approach?" The reviewer note says the answer is actually "4 x 10^0" (i.e., 4.0), not 3.0. The Ex1 Validation Loss (dashed blue) converges around 3.1. The target "3 x 100" is a y-axis tick, but the question's implied answer contradicts the reviewer's own note. Confusing entry. The target and the stated answer do not agree, and the reviewer note contradicts the question. |
| 23 | fig_115 | rejected | 0. 15 | OK | "0.15" is a y-axis tick (with odd spacing "0. 15"). The green line (en&el) at Layer 6 reads about 0.14-0.15. Inferable from surrounding ticks (0.10 and 0.20). Reviewer note allows 0.14-0.16. |
| 24 | fig_122 | approved | w/o Prompt & Augmentation | OK | "w/o Prompt & Augmentation" visible on x-axis. Question asks for the name of the variant excluding both. Directly readable as an x-axis label and inferable from the ablation pattern (combination of the two individual ablations). |
| 25 | fig_123 | rejected | 1.26x | OK | "1.26x" annotation visible in the chart between the two model curves at loss=2.5. Inferable from the horizontal distance between the two curves at the 2.5 loss line. |
| 26 | fig_126 | rejected | 34.4 | OK | "34.4" is the data annotation above GPT-4o at tree width 5. Inferable from the y-axis gridlines (between 30 and 35). |
| 27 | fig_137 | rejected | attn_output | OK | "attn_output" visible in legend (blue dashed line). The blue dashed line stays near 0 across all layers, clearly the lowest. Inferable from line trajectories. |
| 28 | fig_142 | rejected | 1 | ISSUE | Target "1" is a y-axis tick. Question asks about the "hidden state mean before gate, avg 0.71" line at layer 20. At layer 20 this line reads about 0.85-0.9, not 1. The reviewer note says "0.9 to 1.1" is correct, but the visual reading is closer to 0.85. If the "1" tick is blurred, the value is inferable from 0 and 2 ticks. The main issue is the answer accuracy -- the actual value at layer 20 appears to be below 1. |
| 29 | fig_144 | approved | 40 | OK | "40" on y-axis. Re-TACRED at K=16 reads about 40. Inferable from gridlines (35 and 45). |
| 30 | fig_145 | approved | 30 | OK | "30" on y-axis. "Github files" at x=1000 (which appears to be around x=800-1000 given the scale shows 200-1000) reads about 30. Inferable from gridlines (20 and 40). |
| 31 | fig_153 | approved | 0.6 | OK | "0.6" on y-axis. Blue "Final Accuracy" line at o_pop frequency=1 reads about 0.65. Inferable from 0.4 and 0.8 ticks. |
| 32 | fig_156 | rejected | tiny AdaLoRA_int4 | OK | "tiny AdaLoRA_int4" visible in legend (solid circle line). Starts highest (~69 WER at epoch 0) and ends around 40 at epoch 6. The question says "ends at approximately 35 WER at epoch 6" which is slightly off (actual is about 40), but the model identity is inferable from the trajectory. Minor answer inaccuracy but target and question match for inductance. |
| 33 | fig_160 | rejected | 20.0 | ISSUE | Target "20.0" is a y-axis tick. Question asks LLaMA1-13B perplexity at M=3. The chart shows LLaMA1-13B (orange line) at M=3 reads about 17-18. The answer "20.0" is the tick value, not the actual data point value. The question asks for the perplexity value, and the correct answer from the chart is approximately 17-18, not 20. Target/answer mismatch. |
| 34 | fig_193 | rejected | small int8 | OK | "small int8" visible in legend (dashed square line). Looking at the chart, small int8 (dashed orange square) decreases from about 36 to about 25 by epoch 6, which appears to be the lowest final WER. Inferable from line trajectories. |
| 35 | fig_195 | approved | Only MoHD ATTN | ISSUE | Target "Only MoHD ATTN" is in the legend. The question asks which method is represented by the purple line with circular markers. In the chart, "Only MoHD ATTN" is shown with a dark circle marker (navy/dark blue), and the line colors are gray, dark navy, and blue-with-x. The chart does not clearly have a "purple" line. The "Only MoHD ATTN" line appears dark blue/navy, not purple. Minor color description mismatch. However, it is the line with circular markers (as opposed to square or x markers), so the question is partially valid. Borderline. |
| 36 | fig_204 | approved | 13 | OK | "13" visible as the data annotation on the "Other" slice. Question asks about Other category percentage. Inferable from the pie slice size relative to other annotated slices. |
| 37 | fig_217 | approved | 6.7% | OK | "6.7%" visible next to "Med & Health" label. Question valid. Inferable from the pie slice size relative to other labeled slices. |
| 38 | fig_221 | rejected | 23,108 | OK | "23,108" visible as annotation on the Syntactic Roles slice. Question asks for the numerical value. Inferable from slice size relative to other annotated slices (45,387 and 43,000 and 30,000). |
| 39 | fig_226 | rejected | 31.6% | OK | "31.6%" visible on the inner ring (Ambiguity 2) for the "Partially" (yellow) slice. Question valid. Inferable from other percentage labels on the same ring (23.5% Deceived, and the remainder). |
| 40 | fig_233 | rejected | 1.6% | OK | "1.6%" visible next to XSUMHUL label in the pie chart. Question valid. Inferable from slice size and other labeled percentages. |
| 41 | fig_243 | approved | 14.7% | OK | "14.7%" visible on the Sadness slice. Question valid. Inferable from slice size and the other annotated percentages. |
| 42 | fig_245 | approved | 94.5% | OK | "94.5%" visible on the LOCAL slice. Question valid. Inferable from the other two slices (1.6% and 3.9%) since they must sum to 100%. Strong inductance. |
| 43 | fig_248 | approved | (30.08%) | OK | "(30.08%)" visible on the Efficient deployment slice. Question valid. Inferable from the other slice showing (69.92%) since they must sum to 100%. Strong inductance. |
| 44 | fig_024 | not_reviewed | w/o select | OK | "w/o select" visible on x-axis with 88.80% annotation above. Question asks which 'w/o [component]' method has 88.80% accuracy in PHEME. Inferable from bar heights and annotations. |
| 45 | fig_079 | not_reviewed | 0.003 | ISSUE | Target "0.003" is on the x-axis scale. Question asks about SESHA ft model in "Add Spacing" category. The chart shows the SESHA value for Add Spacing is 0.00344 (annotated on the bar). The target "0.003" is an axis tick, but the question asks for the value, which is 0.00344, not 0.003. If the axis tick "0.003" is blurred, the annotated value "0.00344" is still visible. The target and answer do not align -- blurring an axis tick while the data annotation remains visible does not create a meaningful inductance test. |
| 46 | fig_091 | not_reviewed | 0.6 | OK | "0.6" on y-axis. ChatGPT accuracy for Emoji Tweets reads about 0.67. Inferable from 0.4 and 0.8 ticks if 0.6 were present (but axis shows 0.0, 0.2, 0.4, 0.6, 0.8). Inferable from surrounding ticks. |
| 47 | fig_092 | not_reviewed | 0.3 | OK | "0.3" on y-axis. The "- critiquing" bar reads about 0.29. Inferable from 0.2 and 0.4 ticks. |
| 48 | fig_094 | not_reviewed | 31.7% | OK | "31.7%" visible as annotation on the "Generated Response" portion of the "Ours" bar. Inferable from the other annotations (60.6% and 7.7%) since they must sum to 100%. Strong inductance. |
| 49 | fig_098 | not_reviewed | 550 | ISSUE | Target "550" is a y-axis tick. Question asks about category (270,360]. The bar for (270,360] reads about 590-595 based on the axis. The answer "550" is the tick value, not the data value. Target/answer mismatch. Also, the axis label says "Avg. Like #" not "average number of likes." Minor. |

## Detailed Issue Notes

### fig_033 -- Answer value mismatch
The "Ours (Iterative RLHF)" bar for LC AlpacaEval-2 reads approximately 31-32, not exactly 30. The target "30" is the y-axis tick. The question asks for the score which would be ~31, not 30. Minor issue since "approximate" could cover this.

### fig_042 -- Redundant annotation
The bar for "NoR QA" in "2WikiMQA" has the value "29" annotated directly above it. Blurring the y-axis tick "30" does not prevent reading the answer since the annotation "29" remains visible. Weak inductance test.

### fig_067 -- Answer precision
mBERT at "hidden:[], linear" appears to be about 0.08, not 0.1. The question answer may not match visual reality.

### fig_069 -- No y-axis scale
If all "1.00" annotations on SOLAR bars are blurred, there is no y-axis tick scale to infer the value from. The bars reach the top but without a scale the exact value "1.00" cannot be reliably inferred. Weak inductance.

### fig_104 -- Answer vs actual
The lowest point is about -26%, slightly below the -25% y-axis tick. The question answer should be approximately -26%, not -25%.

### fig_105 -- Contradictory reviewer note
The target is "3 x 10^0" but the reviewer note says the answer should be "4 x 10^0". The Ex1 Validation Loss actually converges around 3.1. The entry is internally inconsistent.

### fig_142 -- Value at layer 20
The "hidden state mean before gate" line at layer 20 appears to be about 0.85, not 1. The reviewer allows 0.9-1.1 but visual reading suggests it is below that range.

### fig_160 -- Wrong answer value
LLaMA1-13B at M=3 reads about 17-18, not 20.0. The target "20.0" is a y-axis tick, not the data value.

### fig_195 -- Color description
The "Only MoHD ATTN" line appears dark blue/navy rather than purple. The question references "purple line with circular markers" which may cause confusion.

### fig_079 -- Data annotation makes target redundant
The SESHA value for Add Spacing is annotated as 0.00344 on the bar itself. Blurring the axis tick "0.003" does not hide the answer. Not a meaningful inductance test.

### fig_098 -- Wrong answer value
The bar for (270,360] reads about 590-595, not 550. The target "550" is a y-axis tick, not the actual data value.
