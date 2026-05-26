# ACL Reviewer 1 -- Methodology Rigor: Round 3 Review

**Paper:** SciFig-Eval: Benchmarking Perception, Reasoning, and Behaviour in Vision-Language Models on Scientific Figures

**Overall Recommendation:** Accept

**Overall Soundness:** 4.5 / 5 (up from 4.0)

---

## Primary Focus: Does the Expanded Dataset Resolve the Small-n Concern?

### Issue 9 (Round 2, Moderate): Small n for admittance/inductance (was 50/48)
**RESOLVED.** Admittance has been expanded from 50 to 228 figures and inductance from 48 to 215 figures. These are now substantial subsets covering 91% and 86% of the full 250-figure corpus, respectively. At n=228, the admittance rates reported in Table 4 (e.g., Gemini at 71%, GPT-5.2 at 8%) have tight enough margins to support the paper's claims with confidence. The 4.6x increase in admittance sample size and 4.5x increase in inductance sample size move these from pilot-scale findings to well-powered comparisons. The gap between Gemini (71%) and the next-best model (Llama 4 at 19%) is far too large to be a sampling artifact at n=228.

Table 3 (table3_description_quality.tex) correctly reports AdmB n=228 and IndB n=215 in its caption. Table 4 (table4_behavioral.tex) also correctly states 228 figures for admittance and 215 for inductance. The comprehensive dataset table (table_a_dataset_comprehensive.tex) shows the updated counts with corresponding evaluation instance totals (1,824 and 1,720 per protocol). All three locations are internally consistent.

This was the most substantive remaining concern from Round 2 and it is now fully addressed.

---

## Consistency Check

### Issue 30 (New, Minor): Behavioural probes count in Table 1 is stale.
The dataset summary (dataset.tex, Table 1) reports "Behavioural probes: 948." Under the old counts this was 750 resistance + 100 caption bias + 50 admittance + 48 inductance = 948. With the expanded admittance (228) and inductance (215), the correct total is now 750 + 100 + 228 + 215 = 1,293. This table has not been updated to reflect the expansion. **Must fix.**

### Issue 31 (New, Minor): Fabrication rate changed from 98% to 96% without explanation.
Round 2 resolved an inconsistency between the introduction (which originally said 94%) and results (which said 98%) by aligning both to 98%. In this revision, both the abstract and introduction now report 96%, and the results section (line 50) also states 96%. These are internally consistent, which is good. However, the change from 98% to 96% is presumably a consequence of expanding the admittance set from 50 to 228 figures -- a larger sample produced a slightly lower estimate. This should be noted briefly, or at minimum the reader should not be left wondering why the number changed between revisions. A parenthetical like "(n=228)" after the 96% figure in the introduction would suffice.

### Issue 32 (New, Minor): Limitations section still says "expanding them is a priority."
The limitations section (conclusion.tex, line 30) states: "The admittance and inductance conditions use smaller subsets (Table~\ref{tab:dataset-comprehensive}); expanding them is a priority." With n=228 and n=215, these are no longer "smaller subsets" -- they cover the vast majority of the 250-figure corpus. This sentence should be updated to reflect the current state. The remaining gap (22 figures without admittance targets, 35 without inductance) could be noted as a natural ceiling (some figures may lack suitable blur targets) rather than framed as a limitation requiring expansion.

### Issue 33 (New, Minor): Admittance figure in introduction vs. results.
The introduction states "admits uncertainty 71% of the time" for the comparably-performing model, while the results section and Table 4 confirm Gemini at 71% active admittance. Consistent.

### Other numbers verified as consistent:
- MQM scores (91.6 GPT-5.2, 90.2 Gemini): consistent across abstract, introduction, results, analysis, conclusion.
- Resistance scores (0.91 Gemini, 0.81 GPT-5.2): consistent across results and analysis.
- Caption bias (0.89 for both, p=0.44): consistent in results.
- 34,000+ evaluation instances: the comprehensive table sums to approximately this figure, consistent with abstract and introduction.
- Admittance-behaviour disconnect (63 percentage points): 71% - 8% = 63, consistent in analysis and conclusion.
- Krippendorff's alpha 0.91, rho 0.80: consistent between framework, appendix, and limitations.

---

## Resolution of Remaining Round 2 Issues

### Issue 7 (Minor): NLP/ML sampling bias underemphasized in dataset section
**REMAINING (Minor).** Unchanged. The limitations section covers this adequately.

### Issue 8 (Minor): Subset not balanced by difficulty
**REMAINING (Minor).** Unchanged. Split-half reliability mitigates.

### Issue 13 (Minor): Inconsistent significance testing
**REMAINING (Minor).** Unchanged. Acceptable for the scope of claims.

### Issue 14 (Minor): No multiple comparison correction
**REMAINING (Minor).** Unchanged. Few pairwise claims.

### Issue 19 (Minor): Causal language about training
**REMAINING (Minor).** Analysis section (line 13) now reads "appears tied to instruction tuning that encourages models to trust provided context over visual evidence." The "appears tied to" framing is marginally better than before. Still somewhat assertive but within acceptable bounds for a discussion section.

### Issue 21 (Minor): Correlation at n=8
**REMAINING (Minor).** Unchanged. The paper uses correlation as setup, not as the main evidence.

### Issue 25 (Minor): No qualitative error examples
**REMAINING (Minor).** Still a nice-to-have.

### Issue 27 (Minor, Round 2): Judge bias stability across chart types
**REMAINING (Minor).** Not addressed. Low priority.

### Issue 28 (Minor, Round 2): English-only vs. four-language discrepancy in appendix
**Unknown.** Not checked in this round; was a copy-paste issue in the reproducibility appendix.

### Issue 29 (Minor, Round 2): Capability question circularity (GPT-4o as seeder and judge)
**RESOLVED.** The limitations section now explicitly addresses this: "For capability questions, where GPT-4o serves as both question seeder and answer judge, a cross-judge check with Mistral Large 3 scoring 344 questions preserved model rankings perfectly (rho = 1.000)." This is a direct and convincing response to the concern.

---

## Summary

| Status | Count | Issues |
|--------|-------|--------|
| RESOLVED | 16 | 1-6, 9-11, 15-17, 22, 24, 29 |
| PARTIALLY RESOLVED | 4 | 4, 12, 19, 20 |
| REMAINING (Minor) | 7 | 7, 8, 13, 14, 21, 25, 27 |
| NEW (Minor, must fix) | 1 | 30 (stale probe count) |
| NEW (Minor) | 2 | 31, 32 |
| REMAINING (Major) | 0 | -- |

---

## Updated Section Soundness Scores

| Section | R1 | R2 | R3 | Notes |
|---------|----|----|-----|-------|
| Introduction | 4.0 | 4.5 | 4.5 | 96% now consistent; minor wording |
| Related Work | 4.0 | 4.0 | 4.0 | No change needed |
| Dataset | 3.0 | 4.0 | 4.5 | Expanded blur sets resolve main concern; stale count in Table 1 |
| Framework | 4.0 | 4.5 | 4.5 | Unchanged; solid |
| Results | 3.5 | 4.0 | 4.5 | Numbers consistent at new scale |
| Analysis | 3.5 | 3.5 | 3.5 | Causal framing unchanged |
| Conclusion/Limitations | 4.0 | 4.5 | 4.5 | Stale "expanding is a priority" sentence |

---

## Overall Assessment

The expansion from 50/48 to 228/215 figures for admittance and inductance is the single most important change in this revision. It resolves what was the last moderate methodological concern. The behavioural findings -- particularly the 71% vs 8% admittance gap between Gemini and GPT-5.2 -- are now supported by sample sizes that leave no room for doubt about the direction or magnitude of the effect.

The cross-judge ablation for capability questions (rho = 1.000 with Mistral Large 3 on 344 questions) closes the circularity concern raised in Round 2 Issue 29.

Three items require attention before camera-ready: (1) update the behavioural probe count in Table 1 from 948 to 1,293; (2) revise the limitations sentence that still frames admittance/inductance as "smaller subsets" needing expansion; (3) optionally note the sample size when reporting 96% fabrication to explain the shift from 98%.

All remaining issues are minor and none threatens the validity of the core findings.

### Updated Scores

- **Soundness:** 4.5 / 5
- **Significance:** 4.0 / 5
- **Clarity:** 4.5 / 5
- **Overall Recommendation:** Accept

### Confidence

High. The expanded dataset directly addresses the concern I flagged. Numerical consistency has been verified across all tables and sections, with two minor exceptions noted above.
