# Inductance Blur Candidate Review v3

## fig_195 -- ISSUE

- **Target:** blur "50" on x-axis (Activated Parameters Ratio)
- **Question:** "At what activated parameters ratio did 'Only MoHD FFN' get its lowest Eval PPL score"
- **Expected answer:** 50%
- **Finding:** The "Only MoHD FFN" line reaches its lowest Eval PPL at **100%** (~11.5), not 50%. At 50% the value is higher (~11.7). The question premise is wrong -- the answer should be 100%, not 50%. If the intended blur target is "50" and the intended answer is "50", this candidate is invalid.
- **Verdict: ISSUE** -- factual mismatch between question and chart data.

## fig_091 -- OK

- **Target:** blur "0.4" on y-axis
- **Question:** "what is the accuracy of textblob on analyzing tweets overall"
- **Expected answer:** ~0.4
- **Finding:** TextBlob (white bar) under "Overall Tweet" reaches approximately 0.38-0.40, consistent with the 0.4 target. Y-axis ticks are evenly spaced at 0.0, 0.2, 0.4, 0.6, 0.8 -- blurring "0.4" leaves it trivially inferrable from neighbors (midpoint of 0.2 and 0.6). Inductance property holds.
- **Verdict: OK** -- target, question, and inductance all valid.
