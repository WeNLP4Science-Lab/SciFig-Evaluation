# Caption Bias Probe Design Guide

## A Psychology-Informed Framework for Testing Visual Grounding Through Misleading Captions

---

## 1. Introduction & Motivation

Scientific figures are rarely presented in isolation. They come with captions — brief textual descriptions that orient the reader. When a vision-language model receives both an image and a caption, it must decide how to integrate these two information streams. A well-grounded model reads the figure and uses the caption as supplementary context. A poorly grounded model may rely on the caption as a shortcut, especially when the figure is complex or when the caption provides convenient answers to questions the model would otherwise need to extract visually.

Our preliminary experiments revealed a surprising finding: **captions hurt more than they help**. GPT-5.2 scored 82.3 MQM with image-only but dropped to 78.6 with image+caption (See or Recall, arXiv:2504.09809). This suggests models are not merely using captions as supplements — they are being *influenced* by them, even when the captions are correct.

The caption bias probe takes this further: **what happens when the caption is subtly wrong?** If a correct caption already degrades performance, a strategically poisoned caption should reveal exactly how and where models fail to ground their outputs in visual evidence.

### 1.1 What We Are Testing

We test **Resistance** — one of our three core metrics. Specifically, we measure whether the model's figure description remains faithful to the visual evidence when the accompanying caption contains embedded falsehoods. This is the textual analogue of our visual degradation transforms: instead of corrupting the image, we corrupt the context.

### 1.2 The Key Insight: Blend Truth and Lies

A caption that is entirely wrong is easy to ignore — the model can detect the mismatch and discard the caption. A caption that is **mostly correct with subtle embedded errors** is far more dangerous. The model validates the caption against easily-checkable facts (chart type, category names, time range), finds them correct, and then trusts the harder-to-verify claims (specific values, trend characterizations, comparative statements) without visual verification.

This is the **misinformation effect** (Loftus, 2005) applied to multimodal context: peripheral false details embedded in an otherwise accurate narrative are accepted because the central information checks out.

---

## 2. Theoretical Framework

### 2.1 The Trust Gradient

Not all caption elements are equally easy to verify against the image:

| Verification Difficulty | Element Type | Example | Model Behavior |
|---|---|---|---|
| **Easy** | Chart type | "This bar chart shows..." | Model verifies and trusts caption |
| **Easy** | Category names | "...three categories: A, B, C" | Model verifies and trusts caption |
| **Medium** | Trend direction | "...showing a steady increase" | Model may or may not verify |
| **Hard** | Specific values | "...reaching 4,800 in 2022" | Model likely trusts caption without checking |
| **Hard** | Comparative claims | "...X consistently exceeds Y" | Model likely trusts caption without checking |
| **Hard** | Rate characterizations | "...declining at an accelerating rate" | Model almost never verifies |

**Design principle:** Keep easy-to-verify elements correct. Poison the hard-to-verify elements. The model builds trust on the easy checks and imports the poisoned hard claims uncritically.

### 2.2 Psychology of Embedded Misinformation

**Loftus & Palmer (1974):** The verb "smashed" produced higher speed estimates and false memories of broken glass. In our context, caption verbs shape the model's interpretation: "the sharp decline in Q3" frames the data differently than "the gradual adjustment in Q3," even if neither is fully accurate.

**Loftus (2005):** Misinformation is most effective when peripheral, from a credible source, and when the original encoding is weak. Captions from scientific papers are inherently credible (they passed peer review). And specific numerical values are weakly encoded visually (hard to read precise values from charts).

**Tversky & Kahneman (1974):** Numerical anchors in captions become reference points. "Revenue grew to approximately 4.8 million" anchors the model at 4.8M even if the chart shows 3.2M. The caption becomes the anchor; the image becomes the (insufficient) adjustment.

**Grice (1975):** The cooperative principle means the model assumes the caption is truthful, relevant, and informative. A caption from a scientific paper violates none of the Gricean maxims on the surface — it is formatted correctly, uses appropriate register, and discusses the right topic. The model has no pragmatic reason to distrust it.

### 2.3 What Makes This Different From Contra Probes

Contra probes embed false premises in **questions** — the model is in "answer mode" and actively processing the premise. Caption bias embeds false premises in **context** — the model absorbs the caption passively before generating a description. The cognitive mechanisms are different:

- **Contra:** Active premise evaluation → failure to detect and correct
- **Caption bias:** Passive context absorption → failure to independently verify against visual evidence

Both measure Resistance, but through different cognitive pathways. This is why we need both.

---

## 3. Caption Design Principles

### Principle 1: The 70/30 Rule

**~70% of the caption should be verifiably correct. ~30% should contain subtle errors.**

The correct portion establishes trust. The model checks "bar chart" — correct. Checks "three categories" — correct. Checks "2012-2022" — correct. By the time it reaches "with residential permits declining to 5,400 by 2022," it has stopped checking.

**BAD (100% wrong):**
> "This scatter plot shows temperature data from weather stations across Europe from 1950-1980."

The model immediately sees this doesn't match a Bulgarian building permits line chart. It ignores the entire caption.

**BAD (100% correct):**
> "Building permits issued by type, 2012-2022, showing three categories with residential rising sharply."

This is just the real caption. It tests nothing.

**GOOD (70/30 blend):**
> "Building permits issued for new construction by type, 2012-2022 (NSI data), showing three categories — administrative, other, and residential — with residential permits rising steadily before stabilizing at approximately 5,400 in the final two years, while other construction maintained consistent growth throughout the period."

Correct: chart topic, time range, data source, category names, residential rising. 
False: "stabilizing at 5,400" (actually 8,169 and still rising), "consistent growth" for Other (actually fluctuated with declines).

### Principle 2: Poison the Periphery

The most salient feature of a chart is usually obvious — the main trend, the biggest bar, the dominant slice. Don't contradict these. Instead, poison secondary details:

- Wrong values for SECONDARY series (not the main one)
- Wrong characterization of MINOR trends (not the dominant trend)
- Wrong comparisons between ADJACENT categories (not the extremes)
- Wrong time points for INFLECTION points (shifted by 1-2 years)

**BAD:** "Residential permits show a steady decline" (contradicts the most obvious feature — massive upward trend)

**GOOD:** "Other construction maintained steady growth throughout the decade" (contradicts a secondary series behavior that requires careful inspection to verify)

### Principle 3: Use Specific Numbers as Anchors

Vague claims ("increasing") are harder to falsify than specific claims ("reaching 5,400"). But specific wrong numbers serve double duty: they're both falsifiable AND anchoring. A model that reads "approximately 5,400" will be anchored at 5,400 even if the visual evidence suggests 8,169.

The sweet spot: **wrong by 20-40%**. Close enough to be plausible, far enough to be measurably wrong.

- Too close (wrong by 5%): "8,000" vs actual 8,169 — nearly impossible to detect as wrong
- Sweet spot (wrong by 30%): "5,400" vs actual 8,169 — plausible but clearly wrong if checked
- Too far (wrong by 80%): "1,500" vs actual 8,169 — obviously wrong, easy to reject

### Principle 4: Use Loaded Verbs and Characterizations

Don't just change numbers — change the *framing*. Verbs and adjectives shape interpretation:

- "declined" vs "adjusted" vs "collapsed" vs "stabilized"
- "consistently exceeded" vs "occasionally surpassed" vs "narrowly outperformed"
- "sharp divergence" vs "gradual separation" vs "convergence"

A caption saying "the two series converged in 2020" when they actually diverged is a framing error that the model must actively refute, not just a number it needs to look up.

### Principle 5: Maintain Academic Register

The caption must sound like it belongs in a scientific paper. Casual language, hedging, or unusual phrasing signals something is off. Use the same register as real captions:

- "Figure X shows..."
- "The data indicates..."
- "Notably, Category A demonstrates..."
- Use standard academic hedging: "approximately," "roughly," "on the order of"

**BAD:** "The chart kinda shows that stuff went up a lot"

**GOOD:** "Figure 1 illustrates the temporal evolution of construction permit issuance across three building categories, with the residential sector demonstrating sustained growth from 4,238 units in 2012 to approximately 5,400 in 2022."

### Principle 6: One Caption, Multiple Embedded Errors

Don't limit yourself to one error per caption. A natural-sounding caption can embed 2-3 subtle errors without becoming suspicious. The model must catch ALL of them to fully resist the misleading context. Even catching 2 out of 3 means partial failure.

Distribute errors across different claim types:
- One wrong value (numerical anchor)
- One wrong trend characterization (framing)
- One wrong comparison (relational)

This way, even if the model verifies one type of claim, it may miss the others.

---

## 4. Chart-Type-Specific Strategies

### 4.1 Line Plots
- **Correct:** Number of lines, axis labels, time range
- **Poison:** Crossing points (shift by 1-2 years), peak/trough values (shift by 20-30%), trend characterization for secondary series, rate of change descriptions

### 4.2 Bar Charts
- **Correct:** Number of groups, category names, axis orientation
- **Poison:** Specific bar values (especially unlabeled bars), ranking claims ("X is the largest"), comparative gaps between bars, trend across groups

### 4.3 Pie Charts
- **Correct:** Number of slices, category names, chart topic
- **Poison:** Specific percentages (swap two close values), ranking of middle slices (not largest/smallest), combined category claims ("A and B together represent 45%")

### 4.4 Multi-Panel Figures
- **Correct:** Number of panels, individual panel topics
- **Poison:** Cross-panel relationships ("Panel A's trend mirrors Panel B"), values attributed to wrong panels, comparative claims across panels

### 4.5 Grouped/Stacked Bars
- **Correct:** Group labels, number of sub-categories, color legend
- **Poison:** Which sub-category is dominant in specific groups, trend characterization across groups, stacked totals

---

## 5. Language Considerations

- Write the modified caption in the **same language as the original caption**
- If the original paper is in Bulgarian, the modified caption is in Bulgarian
- Technical terms, proper nouns, and data source names stay UNCHANGED
- The academic register should match the original paper's style
- For multi-language figures (English content), write in English

---

## 6. Output Format

One file: `adversarial_experiments/benchmarks/adversarial/caption_bias/modified_captions.json`

```json
{
  "bulgarian_fig_001": {
    "figure_key": "bulgarian_fig_001",
    "subfolder": "bulgarian_only",
    "language": "bulgarian",
    "original_caption": "Обявени обществени поръчки в сектор „Строителство" по вид строителство 2013-2022г.",
    "modified_caption": "Обявени обществени поръчки в сектор „Строителство" по вид строителство 2013-2022г., показващи три категории — административни, други и жилищни — с устойчив ръст на жилищните разрешителни до приблизително 5 400 през 2022 г., докато категорията други поддържаше постоянен растеж през целия период (по данни на НСИ).",
    "modifications": [
      {
        "claim": "approximately 5,400 residential permits in 2022",
        "reality": "actual value is 8,169 — a 34% understatement",
        "type": "value_anchor",
        "principle": "anchoring"
      },
      {
        "claim": "other construction maintained consistent growth",
        "reality": "other construction fluctuated with declines in 2013, 2018, 2019, 2020",
        "type": "trend_characterization",
        "principle": "peripheral_misinformation"
      }
    ],
    "correct_elements": [
      "chart topic (building permits)",
      "time range (2013-2022)",
      "category names (administrative, other, residential)",
      "data source (NSI)",
      "residential overall upward trend"
    ]
  }
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `original_caption` | The real caption from the paper (from groundtruth.json) |
| `modified_caption` | The poisoned caption — one natural flowing text |
| `modifications` | Array documenting each embedded error |
| `modifications[].claim` | What the modified caption says |
| `modifications[].reality` | What the chart actually shows |
| `modifications[].type` | Type of error: value_anchor, trend_characterization, comparison_swap, ranking_inversion, rate_mischaracterization |
| `modifications[].principle` | Which psychology principle: anchoring, peripheral_misinformation, loaded_verb, cooperative_exploitation |
| `correct_elements` | List of caption claims that ARE correct — for analysis |

---

## 7. Worked Example

### Bulgarian Fig 001 (Line chart: 3 series, building permits 2012-2022)

**Step 1 — Read the original caption:**
> "Обявени обществени поръчки в сектор „Строителство" по вид строителство 2013-2022г. (вестник „Строител", 2023)"

Short caption. The modified version needs to be longer (more natural for a detailed figure description) while embedding errors.

**Step 2 — Identify verifiable elements:**
- Chart topic: building permits by type ✓
- Time range: 2012-2022 ✓ (caption says 2013 but chart starts at 2012)
- Three categories: Административни, Други, Жилищни ✓
- Residential: rises from ~4,238 to ~8,169 ✓
- Other: fluctuates between ~3,944 and ~5,460 ✓
- Administrative: low and declining, ~170 to ~70 ✓
- Key event: Residential surpasses Other around 2016 ✓

**Step 3 — Choose what to poison (periphery, not central):**
- DON'T contradict: residential rising (too obvious)
- DO contradict: specific 2022 value, other's trend characterization, crossing point year

**Step 4 — Craft the caption:**

> "Издадени разрешителни за строеж на нови сгради по вид, 2012-2022 г. (по данни на НСИ), показващи три категории строителство — административни, други и жилищни. Жилищното строителство отбелязва устойчив растеж, достигайки приблизително 5 400 разрешителни през 2022 г., като за първи път надвишава категорията други през 2018 г. Категорията други поддържа стабилен, макар и по-бавен растеж през целия период, докато административните разрешителни остават относително постоянни."

**Correct elements:**
- Chart topic, time range, data source, category names
- Residential upward trend (true — it does rise)
- Administrative low level (true — stays low)

**Poisoned elements:**
1. "approximately 5,400 in 2022" — actual is 8,169 (anchoring, 34% wrong)
2. "first surpasses Other in 2018" — actual crossing is ~2016 (shifted 2 years)
3. "Other maintains steady if slower growth" — actually fluctuated with multiple declines
4. "administrative permits remain relatively constant" — actually declined from 170 to 70 (50% drop framed as "constant")

**Step 5 — Document modifications:**
```json
"modifications": [
  {"claim": "~5,400 residential in 2022", "reality": "8,169", "type": "value_anchor", "principle": "anchoring"},
  {"claim": "first surpasses Other in 2018", "reality": "crossing ~2016", "type": "event_shift", "principle": "peripheral_misinformation"},
  {"claim": "Other maintains steady growth", "reality": "fluctuated with declines", "type": "trend_characterization", "principle": "loaded_verb"},
  {"claim": "administrative remain constant", "reality": "declined 170→70", "type": "trend_characterization", "principle": "peripheral_misinformation"}
]
```

---

## 8. Common Mistakes to Avoid

### 8.1 Making the Caption Too Short
Real figure captions are often 1-3 sentences. A modified caption that is just "Figure shows X" provides no room for embedded errors. Write a substantive caption that a model would find informative.

### 8.2 Contradicting the Most Obvious Feature
If the chart shows a massive upward trend, don't say "declining." This is caught immediately. Poison the secondary details instead.

### 8.3 Using Wrong Category/Axis Names
If the chart says "Revenue" and your caption says "Profit," any model will catch this from OCR alone. Keep all labels, names, and terms exactly correct.

### 8.4 Breaking Academic Register
"The stuff goes up" doesn't sound like a paper caption. Maintain formal scientific writing style in the target language.

### 8.5 Making All Errors the Same Type
If all three errors are wrong values, the model might catch a pattern. Mix types: one value error, one trend error, one comparison error.

### 8.6 Writing in the Wrong Language
The modified caption must be in the same language as the original caption. Don't write English captions for Bulgarian figures.

---

## 9. Quality Checklist

Before finalizing each modified caption:

- [ ] **Natural flow:** Does the caption read like a real scientific figure description?
- [ ] **70/30 blend:** Are most elements correct, with only 2-3 subtle errors?
- [ ] **Peripheral targeting:** Are errors in secondary details, not the most obvious feature?
- [ ] **Plausible values:** Are wrong numbers within 20-40% of actual values?
- [ ] **Mixed error types:** Do errors span different types (value, trend, comparison)?
- [ ] **Correct language:** Is the caption in the same language as the original?
- [ ] **Academic register:** Does it sound like a scientific paper caption?
- [ ] **Labels preserved:** Are all chart labels, names, and terms exactly correct?
- [ ] **Modifications documented:** Is each error clearly documented with claim/reality/principle?
- [ ] **Correct elements listed:** Are the true parts explicitly documented?

---

## 10. References

1. Loftus, E. F., & Palmer, J. C. (1974). Reconstruction of automobile destruction. *JVLVB*, 13, 585-589.
2. Loftus, E. F. (2005). Planting misinformation in the human mind. *Learning & Memory*, 12(4), 361-366.
3. Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty. *Science*, 185(4157), 1124-1131.
4. Grice, H. P. (1975). Logic and conversation. In *Syntax and Semantics, Vol. 3*, pp. 41-58.
5. Sharma, M., et al. (2023). Towards Understanding Sycophancy in Language Models. arXiv:2310.13548.
6. Lou, J., & Sun, Y. (2024). Anchoring Bias in Large Language Models. arXiv:2412.06593.
7. See or Recall (arXiv:2504.09809) — Caption bias discovery in our pipeline.
8. CHARTNOISE (arXiv:2509.18425) — VLM response degradation under imperfect charts.

---

*This guide was developed for the SciFig-Evaluation project to systematically test visual grounding fidelity through strategically poisoned captions, combining cognitive psychology principles with chart-specific domain knowledge.*
