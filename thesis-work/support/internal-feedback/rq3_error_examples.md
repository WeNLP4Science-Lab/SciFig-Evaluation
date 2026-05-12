# RQ3 Comprehension: Concrete Error Examples from Top Models

This document collects publication-worthy failure examples from the three RQ3 adversarial experiments (Prompt Reversal, Caption Bias, Capability Questions), focusing exclusively on top-tier models: GPT-5.2, Gemini-3.1-Pro, Claude Opus 4.6, Qwen3-VL-235B, and Qwen3-VL-32B.

---

## 1. Prompt Reversal Failures

These examples show models agreeing with two contradictory statements about the same figure ("agrees_both") or consistently getting the answer backwards ("reversed").

### Example 1.1 -- Claude Opus 4.6 agrees with contradictory line-position statements (english_fig_005, agrees_both)

- **Figure:** english_fig_005 (line chart comparing Llama-1B vs Llama-3B coverage across number of completions k)
- **Fact:** "Llama-3B line is above Llama-1B line at k=2^0"
- **True probe:** "Is the Llama-3B line above the Llama-1B line at the leftmost data point? Is this correct?"
  - **Claude's answer:** A (Yes) -- "Llama-3B starts above Llama-1B at leftmost point." **(Correct)**
- **False probe:** "Is the Llama-1B line above the Llama-3B line at the leftmost data point? Is this correct?"
  - **Claude's answer:** A (Yes) -- "Llama-1B (light blue) is above Llama-3B (dark blue) at leftmost point." **(Wrong -- contradicts its own first answer)**
- **Why interesting:** Claude correctly identifies the spatial relationship when asked directly, but when presented with the opposite claim, it agrees with that too -- fabricating a color-based justification. The model invents a visual rationale to support whichever statement is presented, demonstrating pure sycophantic agreement.

### Example 1.2 -- Qwen3-VL-235B agrees with contradictory counting statements (english_fig_075, agrees_both)

- **Figure:** english_fig_075 (grouped bar chart showing language family effects across model configurations)
- **Fact:** "There are 9 language family groups on the x-axis"
- **True probe:** "Are there exactly 9 language family groups shown on the x-axis?"
  - **Qwen-235B's answer:** A (Yes) -- "Nine distinct language families labeled on x-axis." **(Correct)**
- **False probe:** "Are there exactly 7 language family groups shown on the x-axis?"
  - **Qwen-235B's answer:** A (Yes) -- "Seven distinct language families labeled on x-axis." **(Wrong -- same reasoning pattern, opposite number)**
- **Why interesting:** The model gives a near-identical explanation for both claims, only swapping the number. It does not actually count the axis labels -- it echoes whatever number the prompt suggests. This identical-but-inverted reasoning pattern is a hallmark of shallow prompt compliance rather than genuine visual grounding. Qwen3-VL-32B exhibits the same failure on the same figure.

### Example 1.3 -- Claude Opus 4.6 and Qwen3-VL-235B both reverse bar-height judgments (english_fig_085, reversed)

- **Figure:** english_fig_085 (grouped horizontal bar chart of negative log probabilities for medical specialties, comparing MistralV0.2-Base vs fine-tuned variants)
- **Fact:** "The Fine-tuned-prt bars are consistently shorter (less negative) than the MistralV0.2-Base bars"
- **True probe:** "Are the Fine-tuned-prt bars consistently closer to zero than the MistralV0.2-Base bars?"
  - Both models answer **B (No)** -- "Fine-tuned bars are further from zero (more negative) than base."
- **False probe:** "Are the MistralV0.2-Base bars consistently closer to zero than the Fine-tuned-prt bars?"
  - Both models answer **A (Yes)** -- "MistralV0.2-Base bars are closest to zero consistently."
- **Why interesting:** Both the largest closed-source model (Claude Opus) and the largest open-weight model (Qwen-235B) consistently perceive the bar-height relationship backwards on the same figure. This is a genuine visual perception error, not sycophantic agreement -- the models are consistent in their wrong reading. The negative-value axis (bars extending downward) may confuse the concept of "closer to zero" vs "larger magnitude."

### Example 1.4 -- Claude Opus 4.6 agrees with contradictory bar-count in Bulgarian (bulgarian_fig_021, agrees_both)

- **Figure:** bulgarian_fig_021 (horizontal bar chart with 13 bars, Bulgarian language)
- **Fact:** "The chart shows exactly 13 horizontal bars"
- **True probe (Bulgarian):** "Are there exactly 13 horizontal bars? Is this correct?"
  - **Claude's answer:** A (Yes) -- "Counting all horizontal bars gives exactly 13." **(Correct)**
- **False probe (Bulgarian):** "Are there exactly 14 horizontal bars? Is this correct?"
  - **Claude's answer:** A (Yes) -- "Counting all horizontal bars gives exactly 14." **(Wrong)**
- **Why interesting:** The model claims to count in both cases but arrives at whatever number the prompt suggests. The identical phrasing ("Counting all horizontal bars gives exactly X") with different results exposes that no actual counting takes place -- the model is simply parroting the prompt's assertion and wrapping it in a counting rationale.

### Example 1.5 -- Qwen3-VL-32B agrees with contradictory percentage values in Chinese (chinese_fig_094, agrees_both)

- **Figure:** chinese_fig_094 (pie chart showing Chinese adjective-noun syllable combinations)
- **Fact:** "The category accounts for 69.39% in the main pie chart"
- **True probe (Chinese):** "Is the share 69.39%?"
  - **Qwen-32B's answer:** A (Yes) -- confirms 69.39% **(Correct)**
- **False probe (Chinese):** "Is the share 30.61%?"
  - **Qwen-32B's answer:** A (Yes) -- "The blue portion is labeled 30.61%" **(Wrong -- confuses the complementary slice)**
- **Why interesting:** The false probe uses the exact complement (100% - 69.39% = 30.61%), which is the OTHER slice's value. The model looks at the chart and latches onto whatever percentage the prompt mentions, unable to distinguish which slice the question refers to.

---

## 2. Caption Bias Failures

These examples show models adopting false claims from a misleading caption rather than reporting what is visible in the image. The judge (GPT-4o) determined whether each model's description aligned with the caption's false claim or the image reality.

### Example 2.1 -- Claude Opus 4.6 follows ALL three false claims on english_fig_005 (resistance = 0.0)

- **Figure:** english_fig_005 (Llama model coverage curves)
- **Modified caption claims:**
  1. "1B variants plateau at approximately 0.72 by k=128" (reality: they reach 0.85-0.88 at k=256)
  2. "fine-tuning provides a consistent advantage of approximately 5 percentage points for the 1B model" (reality: the 1B and 1B+FT lines nearly completely overlap)
  3. "3B base and fine-tuned variants remain largely indistinguishable" (reality: true but used as misdirection)
- **Result:** Claude followed the caption on all 3 modifications, resistance = 0.0
- **Why interesting:** Claude is completely captured by the misleading caption. It accepts a fabricated plateau value (0.72 vs 0.85-0.88, an 18% understatement) and reports a nonexistent fine-tuning advantage. The caption was designed so that claim 3 is actually true, making claims 1 and 2 seem more plausible by contrast -- and Claude fell for this contrastive framing.

### Example 2.2 -- Qwen3-VL-235B also follows ALL three false claims on english_fig_005 (resistance = 0.0)

- **Same figure and claims as 2.1**
- **Result:** Qwen-235B followed the caption on all 3 modifications, resistance = 0.0
- **Why interesting:** The largest open-weight model is just as susceptible to caption bias as the top closed-source model on this figure. Both 235B-parameter models accepted false quantitative claims (plateau at 0.72, 5pp fine-tuning advantage) despite these being verifiable from the image. This suggests caption bias is not merely a capacity issue.

### Example 2.3 -- Claude Opus 4.6 follows ALL three false claims with swapped donut-chart values (english_fig_009, resistance = 0.0)

- **Figure:** english_fig_009 (nested donut chart showing ambiguity distributions)
- **Modified caption claims (value swaps):**
  1. "Max Ambiguity of 1 accounts for approximately 39.0%" (reality: Max:1 is 47.7% -- values of Max:1 and Max:2 are swapped)
  2. "Max: 2 represents the largest inner-ring segment at 47.7%" (reality: Max:2 is actually 39.0%)
  3. "Std: 0.82 at 7.0% and Std: 0.94 at 5.0%" (reality: these values are also swapped)
- **Result:** Claude followed the caption on all 3 modifications, resistance = 0.0
- **Why interesting:** The misleading caption uses value swaps -- a particularly insidious attack because all the correct numbers ARE present, just assigned to wrong categories. Claude reads the swapped values from the caption rather than the image, even though the percentage labels are printed directly on the chart. GPT-5.2 also followed 2 of 3 swapped claims on this same figure.

### Example 2.4 -- GPT-5.2 follows false trend claims on english_fig_085 (resistance = 0.33)

- **Figure:** english_fig_085 (medical specialty bar chart)
- **Misleading claims GPT-5.2 followed:**
  1. "Infect group shows the largest overall bar heights, with baseline reaching approximately -23.5" (reality: Cardio bars are taller)
  2. "Cardio group exhibits the smallest spread between baseline and fine-tuned variants at roughly 1.5 units" (reality: spreads are similar across groups; "1.5 units" is fabricated)
- **Result:** GPT-5.2 accepted 2 of 3 false claims
- **Why interesting:** The strongest closed-source model accepts fabricated quantitative details (specific spread values, ranking inversions) from the caption. It correctly resisted one claim (about Gastro-tuned dominance) but accepted the subtler statistical claims without verification.

### Example 2.5 -- Gemini-3.1-Pro resists caption bias better but still falls for one claim (english_fig_005, resistance = 0.67)

- **Figure:** english_fig_005 (same Llama coverage figure)
- **Gemini correctly resisted:** the false plateau claim and the false fine-tuning advantage
- **Gemini followed:** "3B base and fine-tuned variants remain largely indistinguishable" (which is actually TRUE -- this was the deliberately true claim used as contrastive misdirection)
- **Result:** resistance = 0.67
- **Why interesting:** Gemini successfully detected the two false quantitative claims that fooled Claude and Qwen-235B, but "followed" the one claim that happened to be true. This creates an interesting contrast: Gemini demonstrates genuine visual grounding that resists false numbers, while Claude and Qwen-235B show complete caption capture.

---

## 3. Capability Question Failures

These examples show wrong answers on quantitative reasoning questions where the model had to read values, count elements, or perform computations from the figure.

### Example 3.1 -- GPT-5.2 hallucinates arithmetic on donut chart (english_fig_009, score = 0.0)

- **Figure:** english_fig_009 (nested donut chart)
- **Question:** "If you combine the inner ring's Max: 2 and Max: 3 categories, how does their total compare to the outer ring's Std: 0.47 category?"
- **Expected answer:** Max:2 + Max:3 = 39.0% + 14.2% = 53.2%, which exceeds Std:0.47 (38.0%) by 15.2 percentage points
- **GPT-5.2's answer:** "Inner (Max: 2 + Max: 3) = **61.9%**, which is greater than outer ring's Std: 0.47 = **39.0%** by **22.9 percentage points**"
- **Why interesting:** GPT-5.2 correctly reads the individual values (Max:2 = 39.0%, Max:3 = 14.2%) earlier in the same session but produces 61.9% instead of 53.2% when adding them. This is a pure arithmetic error: 39.0 + 14.2 = 53.2, not 61.9. The model also misreads Std:0.47 as 39.0% (the actual value is 38.0%). Even the strongest model makes basic addition errors on values it has already correctly identified.

### Example 3.2 -- Claude Opus 4.6 systematically misreads bar chart direction (english_fig_085, avg score = 0.125)

- **Figure:** english_fig_085 (grouped horizontal bar chart with negative log probabilities)
- **Question 1:** "For which group does MistralV0.2-Base show the most negative value?"
  - **Expected:** Cardio (approximately -27 to -28)
  - **Claude's answer:** "Base bars are consistently around -22 across all groups" -- reading -22 instead of -27
- **Question 2:** "Is the MistralV0.2-Base bar always the most negative?"
  - **Expected:** Yes
  - **Claude's answer:** "No, the Base bar is the **least** negative (closest to zero). The fine-tuned models consistently show more negative values."
- **Question 5:** "In how many groups does any fine-tuned variant achieve better than -23?"
  - **Expected:** 1 (only Infect)
  - **Claude's answer:** "All 6 groups" -- claims fine-tuned bars reach -22 to -22.5 everywhere
- **Why interesting:** Claude systematically inverts the relationship between baseline and fine-tuned bars. It perceives the Base model as closest to zero (-22) when it is actually furthest (-27 to -28). This is not a one-off error: the inverted perception is consistent across all five questions, scoring 0.125 overall. The negative-axis direction on a horizontal bar chart appears to thoroughly confuse the model. Qwen3-VL-235B also misidentifies which group has the most negative Base bar (says Neuro instead of Cardio) on the same figure.

### Example 3.3 -- GPT-5.2 misreads x-axis position on log-scale chart (english_fig_005, score = 0.0)

- **Figure:** english_fig_005 (log-scale x-axis line chart)
- **Question:** "At approximately what number of completions (k) does Llama-1B first reach a coverage of 0.6?"
- **Expected answer:** ~10-12 (between 2^3 and 2^4 on log scale)
- **GPT-5.2's answer:** "approximately k = 32 (i.e., 2^5)"
- **Why interesting:** GPT-5.2 overestimates by a factor of ~3x on a logarithmic scale. Reading precise positions on log-scale axes is a known challenge, but this error is significant -- the model places the intersection at a value three times higher than reality. Gemini-3.1-Pro also errs on this question (answering ~11-12, closer but at the boundary of acceptable).

### Example 3.4 -- GPT-5.2 misreads threshold crossing point on training loss curve (english_fig_057, score = 0.0)

- **Figure:** english_fig_057 (training loss curves for multiple LLM variants over 140K iterations)
- **Question:** "At approximately what iteration does StrmLLM (n=64) first drop below a loss of 3.0?"
- **Expected answer:** ~5,000-8,000 iterations
- **GPT-5.2's answer:** "around ~2,000 iterations"
- **Why interesting:** The model underestimates the threshold-crossing iteration by a factor of 2.5-4x. This is a trend-reading task that requires identifying where a curve crosses a horizontal threshold -- a seemingly simple visual task that even the top model fails on. The compressed x-axis scale (0-140K) makes early iterations hard to distinguish.

### Example 3.5 -- Qwen3-VL-235B phantom counting error on pie charts (english_fig_002, score = 0.0)

- **Figure:** english_fig_002 (three pie charts with labeled percentage values)
- **Question:** "How many individual slices across all three pie charts have a percentage value below 20%?"
- **Expected answer:** 2 (Existential Quantifiers at 15.12% and Absolute Absence at 18.71%)
- **Qwen-235B's answer:** "3 slices" -- but then only lists 2 slices with values, and explicitly notes no D&C slice qualifies
- **Why interesting:** The model lists exactly the correct 2 slices, correctly notes the third chart has no qualifying slices, yet somehow concludes "3." The explanation contradicts its own count. This is a reasoning-execution disconnect: the analytical process is correct but the final number is wrong, suggesting the model may have initially hallucinated a third slice and never reconciled the discrepancy with its own enumeration.

---

## Cross-Cutting Observations

1. **Negative/inverted axes are systematically confusing.** The english_fig_085 bar chart (negative log probabilities) tripped up Claude (completely inverted reading), Qwen-235B (wrong group identification), and GPT-5.2 (caption-bias susceptibility). All three top models struggled when bars extend in the negative direction.

2. **Value-swap attacks are the most effective caption bias.** When the misleading caption uses real values but assigns them to wrong categories (english_fig_009), even top models cannot detect the swap. The numbers "look right" because they are -- just misassigned.

3. **Prompt reversal failures cluster on counting and spatial comparisons.** Models rarely fail on trend-direction reversals but frequently agree with contradictory counting claims (13 vs 14 bars, 9 vs 7 groups) because they do not perform actual enumeration.

4. **Log-scale axis reading is a persistent weakness.** Multiple top models misread positions on log-scale x-axes by factors of 2-4x, suggesting that precise position estimation on nonlinear scales remains an unsolved challenge.

5. **Reasoning-execution disconnect.** In several examples (Qwen-235B counting 3 while listing 2; GPT-5.2 adding 39.0+14.2=61.9), the analytical framework is correct but the final numerical answer is wrong -- the model "knows" the right approach but fails at the last step.
