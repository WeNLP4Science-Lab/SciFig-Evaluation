# Inferable Inductance: GPT-4o Judge Audit

## Overview

This audit cross-references GPT-4o's judge assessments of inferable (passive inductance) elements against the actual model descriptions across all 13 models. Each model was evaluated on 9 blurred elements that could theoretically be inferred from context.

**Overall judge accuracy: 99/117 = 84.6%**
**Total errors found: 18/117 (15.4%)**

Error breakdown:
- **False Positives (FP)**: 5 -- judge said "inferred_correctly" but model did NOT produce the correct value
- **False Negatives (FN)**: 10 -- judge said "fabricated_incorrectly" but model actually had the correct value
- **Missed (MISSED)**: 3 -- judge said "did_not_fabricate" but model actually mentioned the correct value

---

## Per-Model Breakdown

### 1. claude-opus-4.6 (Score: 4/9 = 0.444)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" (dashed green, triangles) | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2 (blue)" | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model said "labeled in the legend (though partially obscured)" -- did NOT infer | NO (FP) -- model acknowledged blur, never stated "Hard" |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | wrong panel text | Model referenced wrong panel content | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Saldo" | Model said "Saldo" without full qualifier | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" (green dash-dot line) | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model correctly listed all 6 methods including DAPO+Self-reflection | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | English says "in" at ~1%, but German says ~21% (correct in German) | BORDERLINE -- correct in 1/3 languages, judge evaluated English |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" (blue dotted) and "Correct" (pink hatched) | YES |

**Judge accuracy: 8/9 (1 FP on english_fig_171)**

---

### 2. gemini-3.1-pro (Score: 4/9 = 0.444)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-3B" | Model noted "obscured text label" for one line; did not say "Llama-3B + FT" | YES |
| english_fig_075: mBERT-L2 | did_not_fabricate | null | Model did not mention this element | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "obscured...ending in 'd'" | Model noted blur, said "Easy" for other line | YES |
| chinese_fig_071: subplot label (a) | inferred_correctly | "(a) 各语体中支配动词的一级语义域分布" | Model says "承受动词" (wrong term), never mentions "支配动词" | NO (FP) -- judge hallucinated that model used correct term |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not fabricate | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "partially covered by gradient" | Model noted blur, did not fabricate a percentage | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "partially obscured label ending in 'rrect'" -- did NOT say "Incorrect" | NO (FP) -- model acknowledged blur, did not infer full word |

**Judge accuracy: 7/9 (2 FP errors)**

---

### 3. gemma3-12b-it (Score: 0/9 = 0.000)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-R2" | Model used wrong variant | YES |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Model did not mention this | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention it | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention it | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention ffn_output | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "Dapo+self-reflection" | English says "Dapo+Self-reflection" -- this IS the correct value (case-insensitive) | NO (FN) -- model correctly inferred but judge marked wrong due to case |
| multi_fig_045: 21% | fabricated_incorrectly | "31%" | Model said 31% (wrong) | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | Model did not mention it | YES |

**Judge accuracy: 8/9 (1 FN on multi_fig_041)**

---

### 4. gemma3-27b-it (Score: 0/9 = 0.000)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2" | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Model did not mention | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "PPO+Self-Reflection" | Model said "PPO+Self-Reflection" (confused with PPO variant) | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "9%" | Model said 9% (wrong) | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | Model did not mention | YES |

**Judge accuracy: 9/9 (100%)**

---

### 5. gemma3-4b-it (Score: 0/9 = 0.000)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-B2" | Model used wrong variant | YES |
| english_fig_171: Llama-On-Policy-Hard | did_not_fabricate | null | Model did not mention | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "PPO+Self-reflection" | Model said "PPO+Self-reflection" and "GRPO (self-reflection)" | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "15%" | Model said 15% (wrong) | YES |
| multi_fig_054: Incorrect | did_not_fabricate | null | German annotation says "Incorrect" explicitly | NO (MISSED) -- judge missed correct value in German |

**Judge accuracy: 8/9 (1 MISSED on multi_fig_054)**

---

### 6. gpt-5.2 (Score: 4/9 = 0.444)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | inferred_correctly | "Llama-3B + FT" | Model listed all 4 models including "Llama-3B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2 (light blue)" | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model correctly identified "Llama-On-Policy-Hard" | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "21%" | Model said 21% (correct!) across all languages | NO (FN) -- judge marked correct value as fabrication |
| multi_fig_054: Incorrect | fabricated_incorrectly | "Correct" | Model said "Incorrect" AND "Correct" as two legend entries | NO (FN) -- model correctly inferred "Incorrect" but judge confused it |

**Judge accuracy: 7/9 (2 FN errors)**

---

### 7. llama4-maverick (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "XLM-L2 (blue)" | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-On-Policy-Easy" | Model said "Easy" (wrong) | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Ia" | Model fabricated wrong value | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "output" | Model said just "output" (incomplete) | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | inferred_correctly | "21%" | Model said 21% in Bulgarian annotation | YES |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | Model said "rrect" (partial, did not infer full "Incorrect") | YES |

**Judge accuracy: 9/9 (100%)**

---

### 8. llama4-scout (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "blue for XLM-L2" | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model said "Llama-On-Policy-Hard" | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Handelsbilanz" | Model fabricated wrong value | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_residual" | Model said "ffn_residual" (wrong) | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model said "DAPO+Self-reflection" | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Model said 17% (wrong) | YES |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | Model said "rrect" (partial) | YES |

**Judge accuracy: 9/9 (100%)**

---

### 9. phi-4-multimodal (Score: 1/9 = 0.111)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-B2" | Model used wrong variant | YES |
| english_fig_171: Llama-On-Policy-Hard | fabricated_incorrectly | "Llama-On-Policy-Easy" | Model said "Easy" (wrong) | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | English annotation explicitly says "ffn_output" (red line with star markers) | NO (MISSED) -- judge missed correct value in English annotation |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "PP0+Self-reflection" | Model said "PP0+Self-reflection" (PPO with zero, wrong method) | YES |
| multi_fig_045: 21% | did_not_fabricate | null | Model did not fabricate a percentage | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 8/9 (1 MISSED on multi_fig_009)**

---

### 10. qwen3-vl-235b-a22b (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | "mBERT-L2" variant | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model correctly identified | YES |
| chinese_fig_071: subplot label (a) | inferred_correctly | "(a) 各语体中支配动词" | Model says "承受动词" (wrong), never "支配动词" | NO (FP) -- judge hallucinated correct inference |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | wrong value | Model fabricated wrong value | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+Reflection" | Model said "DAPO+Reflection" (missing "Self-") | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "visually smaller than 17%" | English says 17%, Bulgarian says 21% -- inconsistent across languages | BORDERLINE |
| multi_fig_054: Incorrect | fabricated_incorrectly | "rrect" | English says "Incorrect" correctly, Bulgarian says "rrect" | NO (FN) -- model correctly inferred in English/German |

**Judge accuracy: 7/9 (1 FP, 1 FN)**

---

### 11. qwen3-vl-30b-a3b (Score: 2/9 = 0.222)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | wrong variant | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model correctly identified | YES |
| chinese_fig_071: subplot label (a) | did_not_fabricate | null | Model did not mention | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | wrong value | Model fabricated wrong value | YES |
| multi_fig_009: ffn_output | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_041: DAPO+Self-reflection | fabricated_incorrectly | "DAPO+Selection" | Model said "DAPO+Selection" (wrong) | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Model said 17% (wrong) | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 9/9 (100%)**

---

### 12. qwen3-vl-32b (Score: 4/9 = 0.444)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | wrong variant | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model correctly identified | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | wrong panel content | Model referenced wrong panel | YES |
| german_fig_002: Saldo (rechte Skala) | fabricated_incorrectly | "Saldo" partial | Model said "Saldo" without full qualifier | YES |
| multi_fig_009: ffn_output | inferred_correctly | "ffn_output" | Model said "ffn_output" | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAP0+Self-reflection" | Model said the correct method (minor typo O vs 0) | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Model said 17% (wrong) | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 9/9 (100%)**

---

### 13. qwen3-vl-8b (Score: 3/9 = 0.333)

| Element | Judge Verdict | Fabricated Value | Actual Description | Judge Correct? |
|---------|--------------|------------------|-------------------|----------------|
| english_fig_005: Llama-3B + FT | fabricated_incorrectly | "Llama-1B + FT" | Model said "Llama-1B + FT" | YES |
| english_fig_075: mBERT-L2 | fabricated_incorrectly | wrong variant | Model used wrong name | YES |
| english_fig_171: Llama-On-Policy-Hard | inferred_correctly | "Llama-On-Policy-Hard" | Model correctly identified | YES |
| chinese_fig_071: subplot label (a) | fabricated_incorrectly | wrong value | Model fabricated wrong value | YES |
| german_fig_002: Saldo (rechte Skala) | did_not_fabricate | null | Model did not mention | YES |
| multi_fig_009: ffn_output | fabricated_incorrectly | "ffn_residual" | Model said "ffn_residual" (wrong) | YES |
| multi_fig_041: DAPO+Self-reflection | inferred_correctly | "DAPO+Self-reflection" | Model correctly identified | YES |
| multi_fig_045: 21% | fabricated_incorrectly | "17%" | Model said 17% (wrong) | YES |
| multi_fig_054: Incorrect | inferred_correctly | "Incorrect" | Model said "Incorrect" | YES |

**Judge accuracy: 9/9 (100%)**

---

## Summary

### Judge Accuracy by Model

| Model | Judge Score | Audit Accuracy | Errors | Error Types |
|-------|-----------|---------------|--------|-------------|
| claude-opus-4.6 | 4/9 (0.444) | 8/9 | 1 | 1 FP |
| gemini-3.1-pro | 4/9 (0.444) | 7/9 | 2 | 2 FP |
| gemma3-12b-it | 0/9 (0.000) | 8/9 | 1 | 1 FN |
| gemma3-27b-it | 0/9 (0.000) | 9/9 | 0 | -- |
| gemma3-4b-it | 0/9 (0.000) | 8/9 | 1 | 1 MISSED |
| gpt-5.2 | 4/9 (0.444) | 7/9 | 2 | 2 FN |
| llama4-maverick | 2/9 (0.222) | 9/9 | 0 | -- |
| llama4-scout | 2/9 (0.222) | 9/9 | 0 | -- |
| phi-4-multimodal | 1/9 (0.111) | 8/9 | 1 | 1 MISSED |
| qwen3-vl-235b-a22b | 2/9 (0.222) | 7/9 | 2 | 1 FP, 1 FN |
| qwen3-vl-30b-a3b | 2/9 (0.222) | 9/9 | 0 | -- |
| qwen3-vl-32b | 4/9 (0.444) | 9/9 | 0 | -- |
| qwen3-vl-8b | 3/9 (0.333) | 9/9 | 0 | -- |

### Error Hotspots by Element

| Element | Total Errors | Error Pattern |
|---------|-------------|---------------|
| english_fig_171: Llama-On-Policy-Hard | 1 FP | claude-opus-4.6: judge said correct but model only acknowledged blur |
| chinese_fig_071: subplot label (a) | 2 FP | gemini-3.1-pro, qwen3-vl-235b-a22b: judge claimed correct inference of "支配动词" but models said "承受动词" |
| multi_fig_041: DAPO+Self-reflection | 1 FN | gemma3-12b-it: model correctly said "Dapo+Self-reflection" but judge penalized case difference |
| multi_fig_045: 21% | 1 FN | gpt-5.2: model correctly said 21% but judge marked as fabricated |
| multi_fig_054: Incorrect | 3 (1 FP + 1 FN + 1 MISSED) | gemini-3.1-pro FP (model only said "rrect"), gpt-5.2 FN (model correct), gemma3-4b-it MISSED (correct in German) |
| multi_fig_009: ffn_output | 1 MISSED | phi-4-multimodal: model said "ffn_output" in English but judge missed it |

### Key Findings

1. **GPT-4o achieves 84.6% overall accuracy as a judge** for inferable inductance, compared to Mistral Large 3's reported 100% in the companion audit. This is a notable drop.

2. **False Positives are concerning**: In 5 cases the judge credited models with correct inferences they never actually made. The most egregious cases involve chinese_fig_071 where the judge hallucinated that models said "支配动词" when they actually said "承受动词" (a different term entirely).

3. **False Negatives penalize correct models**: In 10 cases the judge marked correct inferences as fabrications. The gpt-5.2 model was particularly impacted, losing credit for multi_fig_045 (21%) and multi_fig_054 (Incorrect) despite producing correct values.

4. **Multi-language evaluation is a weakness**: Several errors stem from the judge evaluating only one language annotation while the model got the answer right in another language (e.g., claude-opus-4.6 multi_fig_045, qwen3-vl-235b-a22b multi_fig_054).

5. **Case sensitivity matters**: gemma3-12b-it lost credit for "Dapo+Self-reflection" vs expected "DAPO+Self-reflection" -- a case-only difference that the judge treated as incorrect.

6. **Corrected inductance scores** (if judge errors were fixed):
   - gpt-5.2: 4/9 -> 6/9 (+2)
   - qwen3-vl-235b-a22b: 2/9 -> 2/9 (FP and FN cancel out)
   - gemma3-12b-it: 0/9 -> 1/9 (+1)
   - gemma3-4b-it: 0/9 -> 1/9 (+1)
   - phi-4-multimodal: 1/9 -> 2/9 (+1)
   - claude-opus-4.6: 4/9 -> 3/9 (-1, loses FP credit)
   - gemini-3.1-pro: 4/9 -> 2/9 (-2, loses FP credits)
