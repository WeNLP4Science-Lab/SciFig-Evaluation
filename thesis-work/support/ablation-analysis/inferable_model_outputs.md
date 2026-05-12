# Inferable Blurred Elements: Model Output Analysis

9 elements were blurred in the selective-blur condition but are logically deducible from surrounding context. This file records whether each of the four frontier VLMs correctly inferred, fabricated, or silently skipped each element.

## Legend

| Symbol | Meaning |
|--------|---------|
| CORRECT | Model explicitly stated the correct value for the blurred element |
| INCORRECT | Model mentioned the element but assigned a wrong value |
| SILENT | Model did not mention the blurred element at all |
| PARTIAL | Model acknowledged something was obscured but gave incomplete info |

---

## Summary Table

| # | Element | GPT-5.2 | Gemini-3.1-Pro | Claude-Opus-4.6 | Qwen3-VL-32B |
|---|---------|---------|----------------|------------------|--------------|
| 1 | english_fig_005 / Llama-3B+FT legend | CORRECT | PARTIAL | SILENT | SILENT |
| 2 | english_fig_075 / mBERT-L2 legend | CORRECT | CORRECT | CORRECT | CORRECT |
| 3 | english_fig_171 / Llama-On-Policy-Hard legend | CORRECT | CORRECT | CORRECT | CORRECT |
| 4 | chinese_fig_071 / Subplot label (a) | CORRECT | CORRECT | INCORRECT | INCORRECT |
| 5 | german_fig_002 / Saldo (rechte Skala) legend | PARTIAL | SILENT | CORRECT | PARTIAL |
| 6 | multi_fig_009 / ffn_output legend | CORRECT | PARTIAL | PARTIAL | PARTIAL |
| 7 | multi_fig_041 / DAPO+Self-reflection legend | CORRECT | PARTIAL | CORRECT | CORRECT |
| 8 | multi_fig_045 / 21% slice value | CORRECT | PARTIAL | INCORRECT | INCORRECT |
| 9 | multi_fig_054 / Incorrect legend | CORRECT | PARTIAL | CORRECT | PARTIAL |

**Correct counts:** GPT-5.2: 8/9, Claude: 5/9, Gemini: 3/9, Qwen-32B: 3/9

---

## Detailed Evidence

### 1. english_fig_005 / Llama-3B+FT legend
**Expected:** "Llama-3B+FT" (inferable from the pattern: Llama-1B and Llama-1B+FT exist, so the fourth line following Llama-3B should be Llama-3B+FT)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Explicitly named all four lines: "Llama-3B", "Llama-3B + FT", "Llama-1B", "Llama-1B + FT" |
| Gemini-3.1-Pro | PARTIAL | Named "Llama-3B", "Llama-1B", "Llama-1B + FT" but described the fourth as "an obscured text label in the legend" with dotted dark green line and triangle markers. Acknowledged the blur but did not infer the name. |
| Claude-Opus-4.6 | SILENT | Only described three lines: "Llama-3B", "Llama-1B", "Llama-1B + FT". Completely omitted the fourth line (Llama-3B+FT). |
| Qwen3-VL-32B | SILENT | Only described three lines: "Llama-3B", "Llama-1B", "Llama-1B + FT". Completely omitted the fourth line. |

---

### 2. english_fig_075 / mBERT-L2 legend
**Expected:** "mBERT-L2" (inferable from grid pattern: mBERT and XLM-R each appear with L2, R2, B2 variants)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Named "mBERT-L₂" explicitly among the legend entries. |
| Gemini-3.1-Pro | CORRECT | Named "mBERT-L₂" explicitly. |
| Claude-Opus-4.6 | CORRECT | Named "mBERT-L₂" explicitly. |
| Qwen3-VL-32B | CORRECT | Named "mBERT-L₂" explicitly. |

---

### 3. english_fig_171 / Llama-On-Policy-Hard legend
**Expected:** "Llama-On-Policy-Hard" (inferable from Easy/Hard subplot pattern: Easy subplot has Llama-On-Policy-Easy, so Hard subplot should have Llama-On-Policy-Hard)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Named "Llama-On-Policy-Hard" explicitly in the Hard Training Set subplot. |
| Gemini-3.1-Pro | CORRECT | Named "Llama-On-Policy-Hard" explicitly. |
| Claude-Opus-4.6 | CORRECT | Named "Llama-On-Policy-Hard" explicitly. |
| Qwen3-VL-32B | CORRECT | Named "Llama-On-Policy-Hard" explicitly with teal line and circular markers. |

---

### 4. chinese_fig_071 / Subplot label (a) with title
**Expected:** "(a) 支配动词" (inferable from pairing with "(b) 求受动词" visible in the other subplot)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Described "左侧子图（a）" (left subplot (a)) as a stacked bar chart, correctly identifying it as subplot (a). While it did not explicitly write "支配动词" as a title, it correctly identified the subplot label. |
| Gemini-3.1-Pro | CORRECT | Correctly identified both subplots and described the right as "(b) 各语体中承受动词的一级语义域分布" and referred to the left subplot structure. Named gender categories within each bar group. |
| Claude-Opus-4.6 | INCORRECT | Only described one subplot, labeling it as "(b) 各语体中求受动词的一级语义域分布". Did not identify or describe subplot (a) at all; appears to have treated the figure as a single subplot (b). |
| Qwen3-VL-32B | INCORRECT | Labeled left subplot as "(a)" but gave the wrong title context. Described both subplots as showing "承受动词" (a single verb type) rather than distinguishing subplot (a) as "支配动词" (governing verbs) vs (b) as a different verb type. Fabricated category names like "运动", "心理", "物理" instead of the actual semantic domain labels. |

---

### 5. german_fig_002 / Saldo (rechte Skala) legend
**Expected:** "Saldo (rechte Skala)" — trade balance on the right scale (inferable because the bars show the difference between exports and imports)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | PARTIAL | Described the bars as "ohne lesbare Legendenbezeichnung" (without readable legend label) and correctly identified they refer to the right scale and lie in the negative range. Did not infer "Saldo" as the name. |
| Gemini-3.1-Pro | SILENT | Did not describe the blue bars at all. Only described the Export and Import lines. |
| Claude-Opus-4.6 | CORRECT | Described "eine zugehörige Saldogröße (dargestellt als Balken, deren Legendenbeschriftung teilweise verdeckt ist und auf die rechte Skala referenziert)" — explicitly inferred "Saldo" as the balance metric, noted legend was partially obscured, and correctly associated it with the right scale. |
| Qwen3-VL-32B | PARTIAL | Described "einen zusätzlichen, nicht beschrifteten blauen Balken" (an additional, unlabeled blue bar) and speculated "vermutlich den Handelsbilanzsaldo" (presumably the trade balance). Correctly guessed the concept but did not commit to naming it "Saldo (rechte Skala)." |

---

### 6. multi_fig_009 / ffn_output legend
**Expected:** "ffn_output" (inferable from the pattern: attn_output, attn_residual, ffn_output, ffn_residual — the four transformer components)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Explicitly named all four: "attn_output", "attn_residual", "ffn_output", "ffn_residual". |
| Gemini-3.1-Pro | PARTIAL | Named three explicitly but described the green line as having a "partially obscured" label that "ends in '_output'". Did not commit to "ffn_output". |
| Claude-Opus-4.6 | PARTIAL | Described the green line as "'_output' (likely ffn_output)". Acknowledged the blur and made the correct guess but hedged with "likely". |
| Qwen3-VL-32B | PARTIAL | Labeled the green line simply as "output" — dropped the "ffn_" prefix. Did not acknowledge any blur or make the full inference. |

---

### 7. multi_fig_041 / DAPO+Self-reflection legend
**Expected:** "DAPO+Self-reflection" (inferable from the pattern: PPO and PPO+Self-reflection exist, plus DAPO exists, so the solid blue bar should be DAPO+Self-reflection)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Explicitly named "DAPO+Self-reflection" as solid medium blue. |
| Gemini-3.1-Pro | PARTIAL | Described the solid blue bar as having "a partially obscured label ending in 'lection'". Did not reconstruct "DAPO+Self-reflection" from context. |
| Claude-Opus-4.6 | CORRECT | Explicitly named "DAPO+Self-reflection" as solid blue. |
| Qwen3-VL-32B | CORRECT | Explicitly named "DAPO+Self-reflection (blue solid)". |

---

### 8. multi_fig_045 / 21% slice value
**Expected:** 21% for the "this" slice (inferable because the other five slices sum to 79%: 31+17+15+9+7 = 79, so the remaining slice = 21%)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | Stated "this" slice is "21% (процентът е частично закрит, но стойността се разчита визуално)" in Bulgarian, and "about 21% (its numeric label is partially obscured by a light rectangular overlay)" in English. Correctly identified the value and noted the blur. |
| Gemini-3.1-Pro | PARTIAL | Noted "чийто процент е частично закрит от бял правоъгълен градиент" (whose percentage is partially obscured by a white rectangular gradient) in Bulgarian, and in English "has a percentage label that is obscured by a rectangular gradient box, leaving only the '%' sign visible." Did not infer the 21% value. |
| Claude-Opus-4.6 | INCORRECT | In Bulgarian, assigned "this" = 17% and swapped values around. In English, assigned "this" = 17%, "for" = 15%, "chemical" = 9%, "to" = 7%, "in" = ~1%. The values don't match the expected distribution (missed 21% entirely and fabricated 1% for "in"). |
| Qwen3-VL-32B | INCORRECT | In Bulgarian, assigned "this" = 17% and "in" = 15%. In English, assigned "this" = 17%, and noted "One segment, corresponding to 'this,' has a white rectangular placeholder with a percentage symbol, suggesting a missing or obscured value" but still reported 17%. Contradictory — acknowledged the blur but fabricated a value. |

---

### 9. multi_fig_054 / "Incorrect" legend
**Expected:** "Incorrect" (inferable as complement of "Correct" in a binary classification bar chart)

| Model | Verdict | Evidence |
|-------|---------|----------|
| GPT-5.2 | CORRECT | In Bulgarian, described the blue series as having partially blurred text but in English explicitly named it "Incorrect" — "an 'Incorrect' series shown as blue bars with a dotted hatch pattern". |
| Gemini-3.1-Pro | PARTIAL | In English, described "a partially obscured label ending in 'rrect'" for the blue bars. In Bulgarian, similarly described "частично замъглен етикет, завършващ на 'rrect'". Did not commit to "Incorrect" despite the visible suffix. |
| Claude-Opus-4.6 | CORRECT | Explicitly named both categories: "Incorrect" (blue dotted) and "Correct" (magenta hatched) across all languages. |
| Qwen3-VL-32B | PARTIAL | In English, labeled it "rrect" and added "(likely a typo for 'Incorrect')". In Bulgarian, used "rrect" throughout. Acknowledged the probable identity but did not commit fully, and mislabeled it as a "typo" rather than recognizing it as a blur artifact. |

---

## Key Findings

1. **GPT-5.2 is the strongest inferrer** (8/9 correct). It consistently reconstructed blurred labels from context, including naming "Llama-3B+FT", "ffn_output", "DAPO+Self-reflection", computing 21% arithmetically, and inferring "Incorrect" as the complement of "Correct". Its only miss was partial: it described the trade balance bars correctly but did not name them "Saldo."

2. **Claude-Opus-4.6 is mixed** (5/9 correct). Strong on pattern-based inference (Llama-On-Policy-Hard, mBERT-L2, DAPO+Self-reflection, Incorrect, Saldo) but failed on arithmetic inference (21% slice) and silently dropped elements it couldn't read (Llama-3B+FT).

3. **Gemini-3.1-Pro tends to describe blurs honestly but not infer** (3/9 correct). It frequently acknowledged "obscured label" or "partially covered" text but chose not to infer the missing value from context. This is the most conservative behavior.

4. **Qwen3-VL-32B occasionally fabricates** (3/9 correct). While it correctly inferred some pattern-based elements (mBERT-L2, Llama-On-Policy-Hard, DAPO+Self-reflection), it fabricated incorrect values for the 21% slice and the Chinese subplot label, and truncated "ffn_output" to just "output."

5. **Pattern-based inference is easier than arithmetic inference.** Elements 2, 3 (naming patterns) were universally correct. Element 8 (arithmetic: 100% - 79% = 21%) was only correctly computed by GPT-5.2.

6. **Silent omission vs. honest acknowledgment.** Claude and Qwen sometimes silently dropped blurred elements (treating them as non-existent), while Gemini consistently flagged them as obscured. GPT-5.2 both flagged and resolved them.
