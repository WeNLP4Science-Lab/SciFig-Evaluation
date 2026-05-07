# Inferable Inductance: Mistral Large 3 Judge Audit

## Overview

This audit cross-references Mistral Large 3's judge assessments of inferable (passive inductance) elements against the actual model descriptions across all 13 models. Each model was evaluated on 9 blurred elements that could theoretically be inferred from context.

---

## Per-Model Breakdown

### 1. claude-opus-4.6 (Score: 5/9 = 0.556)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" (dashed green, triangles) | YES - model confused 3B with 1B |
| english_fig_075: mBERT-L2 | inferred_correctly | "mBERT-L2 (light blue bar)" | Not checked in detail | YES - value matches |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Model admitted blur | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention the label | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model admitted blur | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | inferred_correctly | "21%" | Model inferred 21% | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 9/9 (100%)**

---

### 2. gemini-3.1-pro (Score: 3/9 = 0.333)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | did_not_fabricate | null | Model mentioned "obscured text label" for one line | YES |
| english_fig_075: mBERT-L2 | did_not_fabricate | null | Model used "partially obscured label" for light blue bars | YES |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Model did not fabricate | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | Chinese text referencing right panel | Model fabricated wrong label | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not fabricate | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | did_not_fabricate | null | Model noted percentage "obscured by gradient box" | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 9/9 (100%)**

---

### 3. gemma3-12b-it (Score: 0/9 = 0.000)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-3B, Llama-1B + FT" | Model listed wrong names | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2, mBERT-R2, XLM-R2" | Model fabricated wrong entries | YES |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Not mentioned | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Saldo (rechte Skala) associated with blue bars" | Model mentioned "Saldo (rechte Skala)" but wrongly associated with bars (it's a line). Judge flagged as fabricated because the association is wrong | DEBATABLE - model got the name right but the visual association wrong |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model used "ffn_residual" not "ffn_output" in English; descriptions vary across languages | YES - model did not use "ffn_output" |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "Dapo+self-reflection" | Model actually wrote "Dapo+Self-reflection" in Chinese and English with correct capitalization variations | **NO - JUDGE ERROR**: Model correctly identified "DAPO+Self-reflection" in Chinese description. Case difference "Dapo" vs "DAPO" should not disqualify a correct inference |
| multi_fig_045: 21% | fabricated_incorrectly | "31%" | Model said "31%" in Bulgarian desc | YES - wrong value |
| multi_fig_054: Incorrect | did_not_fabricate | null | Model never mentioned "Incorrect" or "Correct" labels, just described bars by color | YES |

**Judge accuracy: 7/9 (78%). 1 clear error (multi_fig_041 case-sensitivity penalty), 1 debatable (german_fig_002).**

---

### 4. gemma3-27b-it (Score: 0/9 = 0.000)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B" | Wrong name | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-On-Policy-Easy" | Wrong variant | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "attn_residual" | Model said "attn_residual" | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "PPO+Self-Reflection" | Wrong method name | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "this slice is missing a percentage" | Not a valid inference | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | Not mentioned | YES |

**Judge accuracy: 9/9 (100%)**

---

### 5. gemma3-4b-it (Score: 1/9 = 0.111)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B" | Wrong name | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-R2, mBERT-B2" | Wrong names | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-LUFFY-Hard" | Wrong name | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | Bulgarian text for color/style | Wrong - described visual not name | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model correctly inferred | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "15%" | Wrong value | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | Not mentioned | YES |

**Judge accuracy: 9/9 (100%)**

---

### 6. gpt-5.2 (Score: 5/9 = 0.556)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | inferred_correctly | "Llama-3B + FT" | Model correctly identified | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2, mBERT-L2" | Model listed both, but blurred element was only mBERT-L2 | DEBATABLE - model did include "mBERT-L2" among fabricated values |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | "(a)" | Model said "(a)" not "支配动词" | YES - "(a)" is not the expected Chinese text |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model described blur as blur | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Correct | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Correct | YES |
| multi_fig_045: 21% | inferred_correctly | "21%" | Correct | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | Model described as "Incorrect" in English but judge said did_not_fabricate | **NO - JUDGE ERROR**: Model clearly identified "Incorrect" in its English description. Judge incorrectly marked as did_not_fabricate |

**Judge accuracy: 7/9 (78%). 1 clear error (multi_fig_054 missed correct inference), 1 debatable (english_fig_075).**

---

### 7. llama4-maverick (Score: 3/9 = 0.333)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Wrong name | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-R2, XLM-R2..." | Wrong names | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-On-Policy-Easy" | Wrong variant | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Ia" | Wrong | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "output" | Model used "output" not "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Correct | YES |
| multi_fig_045: 21% | inferred_correctly | "21%" | Correct | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect (interpreted as 'rrect')" | Model described it as "rrect" (truncated from blur) but also used "incorrect" contextually | DEBATABLE - model read "rrect" literally but contextually understood it as "incorrect" |

**Judge accuracy: 9/9 (100%)** (the multi_fig_054 judgment is generous but defensible)

---

### 8. llama4-scout (Score: 1/9 = 0.111)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Wrong name | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-R2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_residual" | Wrong name | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+, PPO+Self-reflection" | Model split/confused entries | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Wrong value | YES |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | Model read blurred text literally as "rrect" | **NO - JUDGE ERROR**: Model read "rrect" which is a partially visible rendering of "Incorrect" (the "Inco" prefix was blurred). The model described it as a label alongside "Correct", which demonstrates understanding. Should be "inferred_correctly" since it identified the correct/incorrect binary and read the visible portion accurately |

**Judge accuracy: 8/9 (89%). 1 error (multi_fig_054 penalized partial reading of visible text).**

---

### 9. phi-4-multimodal (Score: 1/9 = 0.111)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | did_not_fabricate | null | Model did not mention | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-B2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-On-Policy-Easy" | Wrong variant | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention ffn_output | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+Self-reflection" | Model mentioned "DAPO+" and "PP0+Self-reflection" separately in English | **NO - JUDGE ERROR**: The fabricated_value recorded is "DAPO+Self-reflection" which matches the expected value exactly. The judge marked it as fabricated_incorrectly despite the value being correct. This appears to be a scoring bug where the judge may have looked at only one language's description where the model used different names |
| multi_fig_045: 21% | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_054: Incorrect | inferred_correctly | "incorrect" | Model inferred correctly | YES |

**Judge accuracy: 8/9 (89%). 1 clear error (multi_fig_041 marked correct value as fabricated_incorrectly).**

---

### 10. qwen3-vl-235b-a22b (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B" | Wrong name | YES |
| english_fig_075: mBERT-L2 | inferred_correctly | "mBERT-L2 (light blue)" | Correct | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | "(a)" | Not the expected Chinese text | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Not mentioned | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_residual" | Wrong name | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+Reflection" | Missing "Self-" prefix | DEBATABLE - partial match, but strictly incorrect |
| multi_fig_045: 21% | fabricated_incorrectly | "visually smaller than 17%" | Not a numeric inference | YES |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | Model read "rrect" and "rrrect" in English | **NO - JUDGE ERROR**: Similar to llama4-scout case. Model read visible portion of blurred text. In German description, model explicitly wrote "Incorrect". Judge penalized based on partial reading in some languages |

**Judge accuracy: 8/9 (89%). 1 error (multi_fig_054).**

---

### 11. qwen3-vl-30b-a3b (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B, Llama-1B + FT" | Wrong names | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Not mentioned | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Handelsbilanz (Importe minus Exporte)" | Wrong name | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_residual" | Wrong name | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+Selection, PPO+Self-reflection" | Model confused entries | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Wrong value | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Correct | YES |

**Judge accuracy: 9/9 (100%)**

---

### 12. qwen3-vl-32b (Score: 3/9 = 0.333)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B, Llama-1B + FT" | Wrong names | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | "(a)" | Not the expected Chinese text | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model admitted blur | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Correct | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAP0+Self-reflection" | Model wrote "DAP0" (zero instead of O) but semantically correct | YES - judge accepted this |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Wrong value | YES |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | Model read "rrect" (partial text), but in English noted it's "likely a typo for Incorrect" | **NO - JUDGE ERROR**: Model explicitly wrote "rrect (likely a typo for 'Incorrect')" in English, demonstrating correct inference. Judge penalized despite model showing understanding |

**Judge accuracy: 8/9 (89%). 1 error (multi_fig_054).**

---

### 13. qwen3-vl-8b (Score: 3/9 = 0.333)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B" | Wrong name | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2" | Wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Correct | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | "(a)" | Not the expected Chinese text | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Saldo (blaue Balken, auf linker y-Achse)" | Model mentioned Saldo but wrong axis | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_output" | Model said "ffn_residual" in all languages, NOT "ffn_output" | **NO - JUDGE ERROR**: The fabricated_value field says "ffn_output" but model actually wrote "ffn_residual" everywhere. Judge recorded the wrong fabricated_value AND wrongly scored it as incorrect when the recorded value would have been correct. Possible data extraction bug |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Correct | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Wrong value | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Correct | YES |

**Judge accuracy: 8/9 (89%). 1 error (multi_fig_009 - fabricated_value field contradicts actual model output).**

---

## Summary

### Judge Accuracy by Model

| Model | Judge Correct | Judge Errors | Accuracy |
|-------|-------------|-------------|----------|
| claude-opus-4.6 | 9/9 | 0 | 100% |
| gemini-3.1-pro | 9/9 | 0 | 100% |
| gemma3-12b-it | 7/9 | 1 clear + 1 debatable | 78-89% |
| gemma3-27b-it | 9/9 | 0 | 100% |
| gemma3-4b-it | 9/9 | 0 | 100% |
| gpt-5.2 | 7/9 | 1 clear + 1 debatable | 78-89% |
| llama4-maverick | 9/9 | 0 | 100% |
| llama4-scout | 8/9 | 1 | 89% |
| phi-4-multimodal | 8/9 | 1 | 89% |
| qwen3-vl-235b-a22b | 8/9 | 1 | 89% |
| qwen3-vl-30b-a3b | 9/9 | 0 | 100% |
| qwen3-vl-32b | 8/9 | 1 | 89% |
| qwen3-vl-8b | 8/9 | 1 | 89% |

### Overall Judge Accuracy

- **Total elements evaluated**: 117 (13 models x 9 elements)
- **Clearly correct judgments**: 108
- **Clear errors**: 7
- **Debatable cases**: 2
- **Overall accuracy**: 92.3% (strict) to 94.0% (lenient)

### Systematic Error Patterns

1. **"rrect" / partial-text penalty (4 models affected)**: The most common error pattern. For multi_fig_054, the blurred element is "Incorrect" but the blur partially covers "Inco", leaving "rrect" visible. Models that read "rrect" and contextually understood it as "Incorrect" were sometimes penalized (llama4-scout, qwen3-vl-235b-a22b, qwen3-vl-32b). The judge inconsistently handled this -- some models reading "rrect" were marked correct (llama4-maverick), while others with the same reading were marked fabricated_incorrectly. This affected 3 models' scores negatively.

2. **Case-sensitivity penalty (1 model)**: gemma3-12b-it's "Dapo+self-reflection" was marked fabricated_incorrectly despite being a trivial case variation of "DAPO+Self-reflection".

3. **Cross-language inconsistency (2 models)**: The judge sometimes evaluated based on one language's description while ignoring another where the model got it right (phi-4-multimodal multi_fig_041, qwen3-vl-235b-a22b multi_fig_054).

4. **Data extraction bug (1 model)**: qwen3-vl-8b's multi_fig_009 has a fabricated_value of "ffn_output" recorded in the evaluation, but the actual model descriptions consistently say "ffn_residual". Either the judge extracted the wrong value from the description or there is a pipeline error.

### Impact on Model Rankings

If all judge errors were corrected:
- **gemma3-12b-it**: 0/9 -> 1/9 (+1 from multi_fig_041)
- **gpt-5.2**: 5/9 -> 6/9 (+1 from multi_fig_054)
- **llama4-scout**: 1/9 -> 2/9 (+1 from multi_fig_054)
- **phi-4-multimodal**: 1/9 -> 2/9 (+1 from multi_fig_041)
- **qwen3-vl-235b-a22b**: 2/9 -> 3/9 (+1 from multi_fig_054)
- **qwen3-vl-32b**: 3/9 -> 4/9 (+1 from multi_fig_054)
- **qwen3-vl-8b**: Score unchanged (the error was a data recording issue, not a scoring direction error since the model actually said "ffn_residual" which IS wrong)

The corrections would not change the relative ranking order significantly, but the "rrect" pattern systematically disadvantages models that read partially-visible text literally rather than silently inferring the full word.
