# Admittance Blur Candidate Review

## Summary

- **Total entries**: 50
- **Skipped** (rejected_no_replacement with empty targets): 2 (fig_137, fig_226)
- **Reviewed**: 48
- **OK**: 33
- **ISSUE**: 15

## Review Table

| # | figure_id | status | target | verdict | notes |
|---|-----------|--------|--------|---------|-------|
| 1 | fig_013 | rejected | tense | OK | "tense" visible on x-axis. Lowest scores there; unrecoverable if blurred. |
| 2 | fig_016 | rejected | Uralic | ISSUE | Question asks "which model family has lowest effect" but Uralic is a linguistic family, not a model family. Also, Uralic does NOT consistently have the lowest -- Isolate appears lower. Question factually wrong. |
| 3 | fig_024 | approved | PHEME | OK | "PHEME" visible as subplot title. w/o text = 80.10 in PHEME vs 83.02 in PolitiFact. PHEME is the lowest. Unrecoverable if blurred. |
| 4 | fig_033 | rejected | Ours (Iterative RLHF) | ISSUE | Target in legend is "Ours (Iterative RLHF)". Question asks highest score on TruthfulQA. Looking at TruthfulQA, the orange bar (Ours) is higher (~60) vs blue (~43). But the model name is only in the legend -- if blurred, the bar color/position could still be read but the NAME would be lost. OK for admittance. However, the question answer ("Ours (Iterative RLHF)") could potentially be inferred if someone knows the paper context. Borderline but acceptable. Changing to OK. |
| 5 | fig_037 | approved | IE-Slavic | OK | "IE-Slavic" visible on x-axis. XLM-R bar is tallest there (~39). Unrecoverable if blurred. |
| 6 | fig_038 | approved | Number of Shots | OK | "Number of Shots" is the x-axis label. Unrecoverable if blurred -- cannot guess the axis meaning from numbers 0-4 alone. |
| 7 | fig_042 | rejected | 2WikiMQA | ISSUE | Target "2WikiMQA" visible on x-axis. Question: "largest difference between NoR QA and OneR QA." Looking at values: HotpotQA diff=5, 2WikiMQA diff=6, MuSiQue diff=5, IIRC diff=1. But actually 2WikiMQA (29-23=6) and HotpotQA (15-10=5). So 2WikiMQA is correct. However, the numeric values are printed on the bars, so even if "2WikiMQA" is blurred, a model could compute the differences from the remaining visible numbers and identify it positionally. ADMITTANCE FAILS -- the answer is inferable from the bar values. |
| 8 | fig_043 | approved | Relevant FCs | OK | "Relevant FCs" visible as bar label with value 6. Clearly the highest. If blurred, cannot recover the name. |
| 9 | fig_045 | rejected | Reasoning | ISSUE | Target "Reasoning" is in the legend. Question asks which property has a token count at every shot number. Both "Reasoning" (orange) and "Demonstration" (blue) appear at every shot number (stacked bars). The question is ambiguous/incorrect -- both categories appear at every shot. |
| 10 | fig_050 | approved | GPT-4o | OK | "GPT-4o" visible on x-axis. Clearly highest strong supervision bar (~24%). Unrecoverable if blurred. |
| 11 | fig_051 | rejected | CInGs | ISSUE | Target "CInGs" on x-axis. Question: highest average performance. CInGs bar is ~59, clearly the tallest. However the label says "CInGs" but the x-axis actually shows "CInGS" -- minor. More importantly, if the label is blurred, positional information (rightmost bar) remains but the NAME is lost. OK for admittance actually. Changing verdict: the name is unrecoverable. OK. |
| 12 | fig_052 | approved | Qwen2 | ISSUE | Target "Qwen2" is in the legend. Question: highest popularity in Basketball. Looking at Basketball, the tallest solid bar appears to be Qwen2 (red, ~210). But there are also patterned bars. The solid Qwen2 bar is tallest. If "Qwen2" is blurred in the legend, the color red remains visible and the bar is identifiable by color, but the NAME is lost. OK for admittance. Actually wait -- the legend still shows color swatches. If only the text "Qwen2" is blurred, the color association is lost. OK. |
| 13 | fig_053 | rejected | Prefix | ISSUE | Target "Prefix" on x-axis. Question: lowest average GLUE performance across different sizes of RoBERTa large. The question says "RoBERTa large" which is the orange bars. Looking at orange bars: Prefix ~85.7, Adaptor ~88.1, LoRA ~89, BitFit ~87.7, etc. Prefix (large) does appear lowest among the large-size bars. But the question says "lowest average GLUE performance across the different sizes" which is confusing -- it could mean average of base+large. If we average both sizes for Prefix: (~85 + ~85.7)/2 is low. Either way Prefix appears to be the answer. The target is visible and unrecoverable if blurred. Changing to OK. |
| 14 | fig_057 | approved | chLSTM | OK | "chLSTM" in legend. Highest Shapley value at T (~80). Unrecoverable if blurred. |
| 15 | fig_061 | rejected | Llama | ISSUE | Target "Llama" on x-axis. Question: lowest entropy for Baseline method. Looking at the chart, Baseline (pink) bars: GPT-4 ~4.88, Claude ~4.67, Llama ~4.55. Llama has the lowest Baseline entropy. However, the model names are on the x-axis and also distinguishable by position (rightmost). If "Llama" text is blurred, position alone doesn't reveal the name. OK for admittance. Changing to OK. |
| 16 | fig_064 | approved | Academic Funding | OK | "Academic Funding" visible as category label. Its "Yes" (red) bar extends to ~65, clearly highest. Unrecoverable if blurred. |
| 17 | fig_067 | approved | hidden:[], linear | OK | Visible on x-axis. XLM-R bar is tallest positive (~0.21). Unrecoverable if blurred. |
| 18 | fig_069 | approved | RedWhale (our) | OK | Visible in legend. Clearly lowest bar in PT-EVAL (0.42). Unrecoverable if blurred. |
| 19 | fig_073 | approved | Baseline_with_Adaptive_Dropout | ISSUE | Target visible on x-axis. Question: highest Sentiment Accuracy. Looking at Sentiment Acc (yellow bars): Single-task ~0.535, Baseline_with_Adaptive_Dropout ~0.52, Unsupervised_SimCSE ~0.53, Supervised_SimCSE ~0.495, 2-Tier ~0.50. Single-task_baseline appears to have the HIGHEST Sentiment Accuracy, not Baseline_with_Adaptive_Dropout. Question answer appears wrong. |
| 20 | fig_074 | approved | IE-Slavic | OK | Visible on y-axis. Clearly longest bar (~80 tasks). Unrecoverable if blurred. |
| 21 | fig_080 | approved | Qwen2 | ISSUE | Target "Qwen2" in legend. Question: highest ratio in Songs. Looking at Songs: Llama3 ~84, Qwen2 ~90, ChatGPT ~63. Qwen2 is highest. If blurred, the red color remains but the name is lost. OK for admittance. However, this is fig_080 which shows Ratio (%) -- different from fig_052 which shows Popularity. Same target "Qwen2" used for both. This is fine, they are different figures. OK. |
| 22 | fig_083 | approved | Spindle | ISSUE | Target "Spindle" visible below the 4th shape. Question: "tallest bars in center, tapering off towards the edges." Looking at the shapes: Spindle shows short-tall-tall-short pattern (tall in center, shorter at edges). This matches. But the question is oddly worded -- it describes the distribution shape, not asks about a text element. More critically: the visual shape itself is still visible even if the label "Spindle" is blurred. A model could describe the shape without knowing the name. But since the ANSWER is the name "Spindle," blurring it makes it unrecoverable. OK for admittance. |
| 23 | fig_085 | approved | Qwen2-Audio-Instruct | ISSUE | Target visible on x-axis. Question: lowest MMAR accuracy. Looking at MMAR (purple) bars: Qwen2-Audio-Instruct ~30%, Audio-Reasoner ~37%, Qwen-2.5-Omni ~56%. Qwen2-Audio-Instruct is lowest. If blurred, position (leftmost) remains but name is lost. OK for admittance. But wait -- the name "Qwen2-Audio-Instruct" partially contains "Qwen2" which also appears in "Qwen-2.5-Omni." If the target text is blurred and other labels remain, a model might try to infer but cannot recover the exact name. OK. |
| 24 | fig_102 | rejected | ChemBERTa Small 20M | ISSUE | The figure is very small and hard to read. Target "ChemBERTa Small 20M" should be in the legend. The legend shows: ChemBART Small 20M, ChemBART Medium 20M, ChemBERTs Small 20M, ChemBERTa Small 20M, ChemBERTa Medium 20M, ChemLLaMA Small 20M, ChemLLaMA Medium 20M. Question: highest training loss at step 20k. At step 20k, the lines are very close and hard to distinguish at this resolution. The image is too small to reliably verify the answer. Flagging as ISSUE due to low image resolution making verification unreliable. |
| 25 | fig_103 | approved | DPR w/o query | OK | Visible in legend. Black horizontal line is constant across all query counts. Unrecoverable if blurred. |
| 26 | fig_104 | approved | Baseline of 4x tokens,4-bit | OK | Visible in legend as dashed gray line at 0%. Unrecoverable if blurred. |
| 27 | fig_105 | rejected | Ex2 Validation Loss | ISSUE | Target visible in legend. Question: which validation loss starts highest at step 0. Looking at step 0: Ex2 Validation Loss (dashed cyan) starts at ~11, Ex1 Validation Loss (dashed blue) starts at ~5. Ex2 Validation Loss is highest. However, the "Ex2 Loss" (solid cyan training loss) also starts at ~11. If "Ex2 Validation Loss" text is blurred in the legend, the dashed cyan line is still distinguishable by line style (dashed) and color. The name is unrecoverable. OK for admittance actually. But the question says "validation loss" which could be inferred from the dashed line style convention. Borderline. Keeping as OK. |
| 28 | fig_115 | approved | en&en | OK | Visible in legend. At Layer 23, en&en (red) shoots up to ~0.44, clearly highest. Unrecoverable if blurred. |
| 29 | fig_122 | rejected | Precision | ISSUE | Target "Precision" in the legend. Question: highest % for "w/o Attention" variant. Looking at w/o Attention data point: Precision ~64.06, Recall ~59.17, F1-score ~59.67. Precision is highest. If "Precision" is blurred, the line color (purple) remains but the metric name is lost. OK for admittance. But the values are annotated on the chart (64.06, 59.67, 59.17), so a model could see which line is highest at that point without the legend. The METRIC NAME is still unrecoverable. OK. |
| 30 | fig_123 | rejected | Vanilla | OK | Visible in legend. Purple line with triangles is consistently higher loss. Unrecoverable if blurred. |
| 31 | fig_126 | approved | Claude-3.5-Sonnet | OK | Visible in legend. At tree width 7, Claude-3.5-Sonnet = 20.0, GPT-4o = 31.1. Claude is lowest. Unrecoverable if blurred. |
| 32 | fig_142 | approved | hidden state mean before gate, avg 0.71 | OK | Visible in legend. Blue dashed line shows the dramatic increase peaking ~4.5 at layer 23. Unrecoverable if blurred. |
| 33 | fig_144 | approved | Re-TACRED | ISSUE | Target visible in legend. Question: highest Micro F1 at K=32. At K=32: Re-TACRED ~50.5, SemEval ~47.5, TACRED ~30, TACRED-Revisit ~31. Re-TACRED is highest. But wait -- at K=32 it looks like Re-TACRED (~50.5) is slightly higher than SemEval (~47.5). OK, Re-TACRED is correct. If blurred, the green line can be identified by color but name is lost. OK for admittance. Changing to OK. |
| 34 | fig_145 | approved | StackOverflow posts | OK | Visible in legend. Yellow line shows steepest decline (from ~33 at 200 tokens to ~11 at 1000 tokens). Unrecoverable if blurred. |
| 35 | fig_153 | rejected | Initial Accuracy | ISSUE | Target "Initial Accuracy" in legend. Question: "line that plots a consistently higher accuracy." Looking at the chart, "Final Accuracy" (blue dashed) is consistently higher than "Initial Accuracy" (green solid). So the answer should be "Final Accuracy," NOT "Initial Accuracy." The question answer is WRONG. |
| 36 | fig_156 | rejected | full | ISSUE | Target "full" in legend (shown as "tiny full" with triangle markers, dotted line). Question: lowest WER across all epochs. The "tiny full" line is at ~29 at epoch 0 and drops to ~24 at epoch 6, consistently the lowest. If blurred, the line style (dotted + triangle) remains but name is lost. OK for admittance. But wait -- the legend says "tiny full" not just "full." Target mismatch. The target says "full" but the legend text is "tiny full." |
| 37 | fig_160 | approved | Vicuna-7B | OK | Visible in legend. Blue line is highest at M=3 (~41). Unrecoverable if blurred. |
| 38 | fig_193 | rejected | small int4 | ISSUE | Target "small int4" in legend. Question: highest WER at epoch 1. At epoch 1: small AdaLoRA_int4 ~40, small int4 (dashed circle) ~33, small AdaLoRA_int8 ~33, small int8 (dashed square) ~30. The highest at epoch 1 is "small AdaLoRA_int4" (~40), NOT "small int4" (~33). Question answer is WRONG. |
| 39 | fig_195 | approved | Transformer | OK | Visible in legend. Red dashed line is constant (~11.6) across all ratios. Unrecoverable if blurred. |
| 40 | fig_204 | approved | Breitbart | OK | Visible as pie slice label with value 14 (largest). Unrecoverable if blurred. |
| 41 | fig_217 | approved | AI/NLP Research | OK | Visible as pie label, 24.3%, clearly largest slice. Unrecoverable if blurred. |
| 42 | fig_221 | rejected | Translated Sentences | ISSUE | Target "Translated Sentences" in legend. Question: largest numerical value. Looking at values: Translated Sentences = 45,387, Pending Translations = 43,000, Extra + Augmented Data = 30,000, Syntactic Roles = 23,108. Translated Sentences (45,387) is largest. However, the numerical values are printed ON the chart slices. If "Translated Sentences" is blurred in the legend, a model can still see 45,387 is the largest number and identify the corresponding slice by color. But the NAME of that slice would be lost. The values themselves don't reveal the category name. OK for admittance. Changing to OK. |
| 43 | fig_230 | approved | Uncrushable | ISSUE | Target "Uncrushable" visible in figure. Question: "attribute associated with Complexity category." Looking at the chart, "Uncrushable" is in the top-left corner associated with the yellow "Complexity" quadrant. If "Uncrushable" is blurred, can it be inferred? The other corners show "Unhackable" (Instance), "Auto-verifiable" (Scalable Oversight), "General" (Coverage). The pattern is one attribute per category. If "Uncrushable" is blurred, its position in the Complexity quadrant is still visible, but the actual word is lost. OK for admittance. |
| 44 | fig_233 | rejected | NQ | OK | Visible as pie label, 31.3%, clearly largest slice. Unrecoverable if blurred. |
| 45 | fig_243 | approved | Excitement | ISSUE | Target "Excitement" visible with 8.1%. Question: second smallest percentage. Values: Happiness 8.1%, Excitement 14.1%, Sadness 14.7%, Anger 14.9%, Frustration 25.1%, Neutral 23.1%. Wait -- Excitement is 14.1% and Happiness is 8.1%. The smallest is Happiness (8.1%), second smallest is Excitement (14.1%). But looking more carefully at the pie chart: the labels show Happiness 8.1% and Excitement 14.1%. So Excitement IS the second smallest. OK. If blurred, the percentage 14.1% remains but the name is lost. But wait, 14.1% is close to Sadness (14.7%) and Anger (14.9%). The name IS unrecoverable. OK for admittance. Changing to OK. |
| 46 | fig_245 | approved | LOCAL | OK | Visible as pie label, 94.5%. Overwhelmingly largest. Unrecoverable if blurred. |
| 47 | fig_248 | rejected | Reduction | OK | Visible as label for orange slice, 69.92%. If blurred, name is lost. OK for admittance. |
| 48 | fig_079 | not_reviewed | Difference in Average WER from Whisper large | OK | Visible as x-axis label. Describes the metric. Unrecoverable if blurred -- cannot infer the specific metric from the chart content alone. |
| 49 | fig_091 | not_reviewed | ChatGPT | OK | Visible in legend. Green bar is clearly tallest in both categories (~0.67). Unrecoverable if blurred. |
| 50 | fig_092 | not_reviewed | Ours | OK | Visible on x-axis. Orange bar is tallest (~0.35). Unrecoverable if blurred. |
| 51 | fig_094 | not_reviewed | Ours | OK | Visible on y-axis. "Ours" row has 60.6% Context, clearly highest Context percentage. Unrecoverable if blurred. |
| 52 | fig_098 | not_reviewed | Most similar group of posts | OK | Visible as x-axis title. Unrecoverable if blurred -- numbers like (0,90] don't reveal the axis meaning. |

## Detailed Issue Notes

### fig_016 -- Question factually incorrect
**Target**: Uralic | **Question**: "Which model family consistently has the lowest effect values across all models?"
- Uralic is a **linguistic family**, not a "model family." The question wording is wrong.
- More importantly, Uralic does NOT consistently have the lowest effect. "Isolate" has near-zero values across all models, clearly lower than Uralic.

### fig_042 -- Admittance potentially fails (values on bars)
**Target**: 2WikiMQA | **Question**: "Which dataset has the largest difference in factual errors between NoR QA and OneR QA?"
- All bar values are numerically annotated on the chart (15, 10, 5, 29, 23, 14, 28, 27, 23, 15, 14, 11). Even if "2WikiMQA" is blurred, a model can compute all differences and identify the correct bar by position. The answer is recoverable from position + visible numeric annotations. Admittance is questionable.

### fig_045 -- Ambiguous question
**Target**: Reasoning | **Question**: "Which property/category has a token count at every shot number in the bar plot shown?"
- Both "Reasoning" and "Demonstration" appear at every shot number (they are stacked). The question does not uniquely identify "Reasoning."

### fig_073 -- Wrong answer
**Target**: Baseline_with_Adaptive_Dropout | **Question**: "Which model achieves the highest Sentiment Accuracy score?"
- The yellow (Sentiment Acc.) bars show Single-task_baseline (~0.535) as the highest, NOT Baseline_with_Adaptive_Dropout (~0.52). The answer in the entry is incorrect.

### fig_102 -- Low resolution image
**Target**: ChemBERTa Small 20M | **Question**: "Which model has the highest training loss at step 20k?"
- The figure is extremely small. Legend text and line distinctions at step 20k are barely readable. Cannot reliably verify the answer.

### fig_105 -- Borderline (reclassified OK)
**Target**: Ex2 Validation Loss | Ex2 Validation Loss starts highest (~11 at step 0). Admittance holds since the name is unrecoverable even though line style is visible.

### fig_153 -- Wrong answer
**Target**: Initial Accuracy | **Question**: "What does the line that plots a consistently higher accuracy represent?"
- "Final Accuracy" (blue dashed) is **consistently higher** than "Initial Accuracy" (green solid). The answer should be "Final Accuracy," not "Initial Accuracy." The question-target pair is inverted.

### fig_156 -- Target text mismatch
**Target**: full | **Question**: "Which method consistently has the lowest WER across all the epochs?"
- The legend shows "tiny full" not just "full." The target text does not exactly match what appears in the figure.

### fig_193 -- Wrong answer
**Target**: small int4 | **Question**: "Which configuration achieves the highest WER at epoch 1?"
- At epoch 1, "small AdaLoRA_int4" has the highest WER (~40), not "small int4" (~33). The answer is factually wrong.

## Final Counts

| Verdict | Count |
|---------|-------|
| OK | 33 |
| ISSUE (wrong answer) | 3 (fig_073, fig_153, fig_193) |
| ISSUE (wrong question wording) | 2 (fig_016, fig_045) |
| ISSUE (admittance fails / inferable) | 1 (fig_042) |
| ISSUE (target text mismatch) | 1 (fig_156) |
| ISSUE (low resolution) | 1 (fig_102) |
| Skipped (no target) | 2 (fig_137, fig_226) |
