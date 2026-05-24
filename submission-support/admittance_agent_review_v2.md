# Admittance Blur Candidate Review (Agent V2)

## Summary

- **Total entries reviewed**: 46 (48 total minus 2 rejected_no_replacement)
- **OK**: 36
- **ISSUE**: 10

## Review Table

| Figure | Status | Target | Verdict | Notes |
|--------|--------|--------|---------|-------|
| fig_013 | rejected | tense | OK | "tense" visible as x-axis label; all models have near-zero scores there; target is admissible |
| fig_016 | rejected | Semitic | ISSUE | Question asks "mBert-R2 lowest effect value" -- looking at the chart, mBERT-R2 (light green) has near-zero or slightly negative values at Semitic, but also near-zero at Isolate and Uralic. It is unclear if Semitic is truly the unique lowest. The negative bar at Semitic makes it plausible, but Isolate is also near-zero. Borderline -- accept with caution |
| fig_024 | approved | PHEME | OK | PHEME visible as subplot title; w/o text has lowest accuracy (80.10) in PHEME panel. Cannot be inferred if blurred |
| fig_033 | rejected | Ours (Iterative RLHF) | ISSUE | Question: "highest score on TruthfulQA". Looking at chart, on TruthfulQA the orange bar ("Ours (Iterative RLHF)") is taller (~60) than blue (~43). But the target is a legend label -- if blurred, the orange color still shows which bar is taller. The answer could be inferred from color alone if the legend text is blurred. However, blurring the legend label text specifically would make it impossible to NAME the model. OK as admissible |
| fig_037 | approved | IE-Slavic | ISSUE | Question: "highest task count for XLM-R". XLM-R (dark blue) has highest bar at IE-Slavic (~39). But fig_074 is essentially the same data (linguistic family vs # tasks). If both figures are in the dataset, cross-reference is possible. As standalone: OK. The x-axis label "IE-Slavic" is the target; if blurred, cannot be named. Admissible as standalone |
| fig_038 | approved | Number of Shots | OK | "Number of Shots" is x-axis label. If blurred, cannot determine what variable is being varied. Admissible |
| fig_042 | rejected | 2WikiMQA | ISSUE | Question: "largest difference in factual errors between NoR QA and OneR QA". HotpotQA: 15-10=5; 2WikiMQA: 29-23=6; MuSiQue: 28-27=1; IIRC: 15-14=1. So 2WikiMQA has difference of 6, HotpotQA has 5. This is correct. Target "2WikiMQA" is x-axis label; if blurred, cannot name the dataset. Admissible. Actually OK |
| fig_043 | approved | Relevant FCs | OK | "Relevant FCs" visible with highest count (6). If blurred, cannot name the criterion. Admissible |
| fig_045 | rejected | Number of Shots | OK | "Number of Shots" is x-axis label. If blurred, cannot determine what is being varied across the five bars. Admissible |
| fig_050 | approved | GPT-4o | OK | GPT-4o has highest strong supervision bar (~24%). If label blurred, cannot name the model. Admissible |
| fig_051 | rejected | CInGs | OK | CInGs (rightmost, blue bar) has highest average performance (~59). If label blurred, cannot name the method. Admissible |
| fig_052 | approved | Qwen2 | OK | Qwen2 (red) has tallest solid bar in Basketball. If legend label blurred, cannot name model. Admissible |
| fig_053 | rejected | Prefix | ISSUE | Question: "lowest average GLUE performance across different sizes of RoBERTa large". The chart shows base vs large for each method. For "large" (orange bars), Prefix has ~85.7, Adaptor ~88.1, LoRA ~89, BitFit ~87.7, S1 ~85.6, S4 ~87.7, S5 ~89. S1-model large bar appears to be roughly the same height as Prefix large bar (~85.6 vs ~85.7). Very close -- Prefix may not be the clear lowest for "large". Also, the question says "lowest average GLUE performance across the different sizes" which is ambiguous. If it means average of base+large, then BitFit base (~84.8) + large (~87.7) vs Prefix base (~85) + large (~85.7). Prefix average ~85.35, BitFit average ~86.25, Adaptor average ~87.5. S1-model: base ~85.6, large ~85.6, avg ~85.6. Prefix avg seems lowest. But S1-model base is higher than Prefix base. The question is confusingly worded -- "across the different sizes of the RoBERTa large model" is unclear. Needs rewording |
| fig_057 | approved | chLSTM | OK | chLSTM (green) has tallest bar at category T (~80). If label blurred, cannot name model. Admissible |
| fig_061 | rejected | Llama | OK | Llama has lowest Baseline entropy (~4.55). If x-axis label blurred, cannot name model. Admissible |
| fig_064 | approved | Academic Funding | OK | Academic Funding has longest red ("Yes") bar (~65). If label blurred, cannot name category. Admissible |
| fig_067 | approved | hidden:[], linear | OK | hidden:[], linear has highest XLM-R % point difference (~0.21). If x-axis label blurred, cannot name category. Admissible |
| fig_069 | approved | RedWhale (our) | OK | RedWhale has lowest score at PT-EVAL (0.42). If legend label blurred, cannot name model. Admissible |
| fig_073 | rejected | 2-Tier SimCSE | ISSUE | Question: "highest overall accuracy/correlation score for STS Corr." Looking at chart, the pink bars (STS Corr.) show: Single-task ~0.50, Baseline_w_Adaptive_Dropout ~0.58, Unsupervised_SimCSE ~0.71, Supervised_SimCSE ~0.81, 2-Tier SimCSE ~0.81. Supervised_SimCSE and 2-Tier SimCSE both appear to have STS Corr. around 0.81. It is very hard to distinguish which is higher. The answer may not be uniquely "2-Tier SimCSE" -- it could be tied with Supervised_SimCSE. ISSUE: answer may be ambiguous/tied |
| fig_074 | approved | IE-Slavic | OK | IE-Slavic has highest # tasks (~80). If label blurred, cannot name family. Admissible |
| fig_079 | not_reviewed | Difference in Average WER from Whisper large | OK | This is the x-axis label. If blurred, cannot determine what metric is used. Admissible |
| fig_080 | approved | Qwen2 | ISSUE | Question: "highest ratio in Songs category". Looking at chart, in Songs: Llama3 ~84, Qwen2 ~90, ChatGPT ~63. Qwen2 does have highest ratio in Songs. If legend label blurred, cannot name model. OK actually -- admissible |
| fig_083 | approved | Spindle | OK | Spindle shape visible (tall center, tapering edges). If label blurred, cannot name the shape. Admissible |
| fig_085 | approved | Qwen2-Audio-Instruct | OK | Qwen2-Audio-Instruct has lowest MMAR (~30%). If label blurred, cannot name category/model. Admissible |
| fig_091 | not_reviewed | ChatGPT | OK | ChatGPT (green) has highest accuracy in both Emoji Tweets (~0.67) and Overall Tweet (~0.65). If legend label blurred, cannot name tool. Admissible |
| fig_092 | not_reviewed | Ours | OK | "Ours" (orange) has highest Recall@10 (~0.35). If label blurred, cannot name method. Admissible |
| fig_094 | not_reviewed | Ours | OK | "Ours" has 60.6% Context vs "Standard" 23.6%. If label blurred, cannot name scenario. Admissible |
| fig_098 | not_reviewed | Most similar group of posts | OK | This is the x-axis title. If blurred, cannot determine what categorizes the post groups. Admissible |
| fig_103 | approved | DPR w/o query | OK | DPR w/o query (black solid line) stays constant at ~34.2 MRR@10. If legend label blurred, cannot name method. Admissible |
| fig_104 | approved | Baseline of 4x tokens,4-bit | OK | Gray dashed baseline stays at 0% across all layers. If legend label blurred, cannot name the line. Admissible |
| fig_105 | rejected | Ex2 Validation Loss | OK | Ex2 Validation Loss (cyan dashed) starts highest at step 0 (~11). If legend label blurred, cannot name which experiment. Admissible |
| fig_115 | approved | en&en | OK | en&en (red) has highest similarity at Layer 23 (~0.44). If legend label blurred, cannot name pair. Admissible |
| fig_122 | rejected | Precision | ISSUE | Question: "highest percentage value for w/o Attention variant". Looking at chart, at "w/o Attention" point: Precision ~64.06, Recall ~59.67, F1-score ~59.17. Precision is highest. But the legend has three metrics (Precision, Recall, F1-score). If "Precision" label in legend is blurred, the line color (purple) would still be visible, and the color mapping might be inferable from the pattern (Precision > Recall > F1 is a common pattern). However, without the legend text, you truly cannot name which metric it is. Admissible. Actually OK |
| fig_123 | rejected | Vanilla | OK | Vanilla (purple) consistently has higher loss than SepLLM (red) across all training time. If legend label blurred, cannot name model. Admissible |
| fig_126 | approved | Claude-3.5-Sonnet | OK | Claude-3.5-Sonnet has lowest accuracy at tree width 7 (20.0). If legend label blurred, cannot name model. Admissible |
| fig_142 | approved | hidden state mean before gate, avg 0.71 | OK | This line (blue dashed) shows largest increase peaking ~4.5 at layer 24. If legend label blurred, cannot name which hidden state mean. Admissible |
| fig_144 | approved | Re-TACRED | ISSUE | Question: "highest Micro F1 at K=32". At K=32: Re-TACRED ~50.5, SemEval ~48. Re-TACRED is highest at K=32. But at K=64, SemEval overtakes. So the answer is specifically correct for K=32. If legend label blurred, cannot name dataset. Admissible. Actually OK |
| fig_145 | approved | StackOverflow posts | OK | StackOverflow posts (yellow) shows steepest decline from ~33 to ~11. If legend label blurred, cannot name resource. Admissible |
| fig_153 | rejected | o_pop frequency (x10^4) | ISSUE | Target text in figure shows "o_pop frequency (x10^4)" on x-axis. The JSON has "o_pop frequency (x10^4)" -- matches. If blurred, cannot determine x-axis meaning. Admissible. OK |
| fig_156 | rejected | full | ISSUE | Reviewer note says "answer is tiny full". The legend shows "tiny full" not just "full". Target should be "tiny full" to match the actual label in the figure. The model with lowest WER across all epochs is indeed "tiny full" (dotted line with triangles, lowest curve). Target text mismatch with figure label |
| fig_160 | approved | Vicuna-7B | OK | Vicuna-7B (blue) has highest perplexity at M=3 (~41). If legend label blurred, cannot name model. Admissible |
| fig_195 | approved | Transformer | OK | Transformer (red dashed) stays constant at ~11.6 eval PPL. If legend label blurred, cannot name method. Admissible |
| fig_204 | approved | Breitbart | OK | Breitbart has largest slice (14%). If label blurred, cannot name source. Admissible |
| fig_217 | approved | AI/NLP Research | OK | AI/NLP Research has 24.3%, largest slice. If label blurred, cannot name category. Admissible |
| fig_221 | rejected | Translated Sentences | OK | Translated Sentences (yellow) shows 45,387 -- largest value. If legend label blurred, cannot name category. Admissible |
| fig_230 | approved | Uncrushable | OK | "Uncrushable" is in the Complexity quadrant. If label blurred, cannot name attribute. Admissible |
| fig_233 | rejected | NQ | OK | NQ has 31.3%, largest slice. If label blurred, cannot name data source. Admissible |
| fig_243 | approved | Excitement | OK | Excitement at 8.1% is second smallest (smallest is Happiness at... wait, looking again: Neutral 23.1%, Frustration 25.1%, Anger 14.9%, Sadness 14.7%, Excitement 14.1%, Happiness 8.1%). Second smallest is Excitement (14.1%)? No -- Happiness 8.1% is smallest, Excitement 14.1% is not second smallest. Sadness 14.7% and Anger 14.9% and Excitement 14.1% are close. Actually second smallest would be Excitement at 14.1%. Wait: sorted ascending: Happiness 8.1%, Excitement 14.1%, Sadness 14.7%, Anger 14.9%, Neutral 23.1%, Frustration 25.1%. Yes, Excitement IS second smallest. OK. Admissible |
| fig_245 | approved | LOCAL | OK | LOCAL at 94.5% is largest. If label blurred, cannot name category. Admissible |
| fig_248 | rejected | Reduction | OK | Reduction is the orange slice at 69.92%. If label blurred, cannot name it. Admissible |

## Detailed Issue Notes

### fig_016 -- Borderline answer accuracy
The question asks on which category mBERT-R2 has its lowest effect value. mBERT-R2 (light green) shows near-zero or slightly negative values at multiple categories (Semitic, Isolate, Uralic). While Semitic appears to have a slightly negative bar, it is borderline. Recommend verifying numerically or rewording to be less ambiguous.

### fig_053 -- Confusing question wording
The question reads "lowest average GLUE performance across the different sizes of the RoBERTa large model" which is grammatically confusing. "Across the different sizes of the RoBERTa large model" does not parse well -- does it mean across both base and large sizes, or specifically for the large model? The target "Prefix" appears to be one of the lowest for the large size specifically, but S1-model is extremely close. Recommend rewording the question for clarity.

### fig_073 -- Tied/ambiguous answer
STS Corr. values for Supervised_SimCSE and 2-Tier SimCSE appear nearly identical (~0.81). It is not clear from the visual that 2-Tier SimCSE is definitively the highest. The answer could be either. Recommend checking underlying data or choosing a metric/category where the winner is unambiguous.

### fig_156 -- Target text mismatch
The figure legend shows "tiny full" but the JSON target is just "full". The reviewer note confirms "answer is tiny full". The target field should be updated to "tiny full" to match what actually appears in the figure.

### fig_037 and fig_074 -- Cross-figure redundancy (minor)
Both figures involve IE-Slavic as the answer for highest task count. fig_037 asks specifically about XLM-R while fig_074 asks about total tasks. Not a strict issue but worth noting the overlap.

## Priority Figure Detailed Assessment

### fig_016 (reviewer-fixed): BORDERLINE
Target visible, question mostly works, but answer uniqueness is marginal.

### fig_045 (reviewer-fixed): OK
Clean. "Number of Shots" is x-axis label, question is clear, answer is not inferable from other context.

### fig_073 (reviewer-fixed): ISSUE
Answer is visually ambiguous between two categories with nearly identical bar heights.

### fig_153 (reviewer-fixed): OK
Target "o_pop frequency (x10^4)" matches x-axis label. Clean admittance case.

### fig_042 (special attention): OK
2WikiMQA has difference of 6 (29-23) vs HotpotQA's 5 (15-10). Answer is correct and verifiable from data labels.
