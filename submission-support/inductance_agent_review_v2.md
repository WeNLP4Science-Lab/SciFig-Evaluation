# Inductance Blur Candidates -- Agent Review v2

Review of flagged figures (fig_042, fig_069, fig_098, fig_105, fig_160, fig_195) and not_reviewed entries (fig_024, fig_091, fig_092, fig_094).

| Figure   | Verdict | Target | Notes |
|----------|---------|--------|-------|
| fig_042  | OK      | 5      | IRCoT QA blue bar on HotpotQA is labeled "5". If label is blurred, value is recoverable from y-axis gridlines (every 5 units). Inductance holds. |
| fig_069  | OK      | 1.00   | SOLAR-10.7B-v1.0 (base) gray bar at PT-EVAL labeled "1.00". Bar clearly reaches top of chart. Even with label blurred, the bar height relative to other labeled bars (0.42, 0.46) and the y-axis makes 1.00 inferable. Inductance holds. |
| fig_098  | OK      | 600    | Bar for (0,90] reaches ~600 on y-axis. Y-axis gridlines at 400, 450, 500, 550, 600 make the value readable even without a bar label. Accept range 597-603 is reasonable. Inductance holds. |
| fig_105  | ISSUE   | Ex2 Validation Loss | Question: "What losses hit (10^1)*1.1 at 0 steps?" -- (10^1)*1.1 = 11. At step 0, only Ex2 Loss (solid cyan) reaches ~11. Ex2 Validation Loss (dashed cyan) starts around 4-5, and Ex1 Validation Loss (dashed blue) starts around 3.5. The reviewer notes say "the answer is ex1 and ex2 validation loss" but neither validation loss line reaches 11 at step 0. The target and notes contradict the visible data. Needs correction: either change target to "Ex2 Loss" or revise the question threshold. |
| fig_160  | ISSUE   | 8      | Question: "At what M point does Llama1-7B hit its highest perplexity?" The green line (LLaMA1-7B) peaks at M=3 (~27.5), not M=8 (~25). M=8 shows a rebound but is not the maximum. Target should be 3, not 8. |
| fig_195  | ISSUE   | 50     | Question: "At what activated parameters ratio did 'Only MoHD ATTN' get its lowest Eval PPL score?" The dark circle line (Only MoHD ATTN) has lowest PPL at 100% (~11.5), not 50% (~12.2). PPL increases as the ratio decreases. Target should be 100, not 50. |
| fig_024  | OK      | w/o select | not_reviewed. "w/o select" label visible at 88.80% in PHEME. Question directly references the accuracy value, so blurring the label makes the model identify which bar has that value. Inductance holds. Suggest accept range: "w/o select" only. |
| fig_091  | ISSUE   | 0.6    | not_reviewed. ChatGPT (green solid bar) accuracy for Emoji Tweets appears to be ~0.65-0.68 by visual reading against y-axis gridlines, not 0.6. Target is too low. Suggest updating target to 0.65 with accept range 0.63-0.68. |
| fig_092  | OK      | 0.3    | not_reviewed. The "- critiquing" bar reads ~0.29 from y-axis. Target 0.3 is a reasonable approximation. Suggest accept range 0.27-0.31. Note: x-axis label is "- critiquing" (with leading dash) but question says "critiquing" -- minor, acceptable. |
| fig_094  | OK      | 31.7%  | not_reviewed. "Generated Response" in "Ours" bar is explicitly labeled 31.7%. Value is directly readable. Inductance holds trivially since the percentage is also constrained by the other labeled segments (60.6% + 7.7% = 68.3%, leaving 31.7%). |

## Summary

- **6 OK**: fig_042, fig_069, fig_098, fig_024, fig_092, fig_094
- **4 ISSUE**: fig_105 (wrong target -- only Ex2 Loss reaches 11, not validation losses), fig_160 (wrong answer -- peak is at M=3 not M=8), fig_195 (wrong answer -- lowest PPL at 100% not 50%), fig_091 (target 0.6 underestimates the visible bar height of ~0.65-0.68)
