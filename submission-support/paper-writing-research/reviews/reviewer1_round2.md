# ACL Reviewer 1 -- Methodology Rigor: Round 2 Review

**Paper:** SciFig-Eval: Benchmarking Perception, Reasoning, and Behaviour in Vision-Language Models on Scientific Figures

**Overall Recommendation:** Accept

**Overall Soundness:** 4.0 / 5 (up from 3.5)

---

## Resolution Status of Round 1 Issues

### Issue 1 (Minor, Intro): 94% fabrication rate is CI lower bound, not point estimate
**RESOLVED.** The introduction now correctly states "fabricates answers for elements it cannot see 98% of the time" (line 11 of introduction.tex), consistent with the results section and the statistics file.

### Issue 2 (Minor, Intro): "Comparably-scoring" is borderline with 1.4-point gap
**RESOLVED.** No change needed; this was noted as defensible in Round 1 and remains so. The paper now explicitly states "The 1.4-point gap is statistically significant (p < 0.01) but practically small (Cliff's delta = 0.09)" in the results section, which makes the comparison transparent.

### Issue 3 (Minor, Related Work): Missing methodological comparison with CHAOS/CHART NOISe
**RESOLVED.** The related work now explicitly cites CHAOS and CHART NOISe as "robustness benchmarks ... that evaluate how chart understanding degrades under perturbation, corruption, and occlusion" (related_work.tex, line 13). A brief methodological differentiation is present, though still minimal.

### Issue 4 (Minor, Related Work): MQM adaptation differences underexplained
**PARTIALLY RESOLVED.** The related work now states "we adapt this idea to scientific figure descriptions using checklist-based scoring and binding verification" and refers to validation against human judgments. The full MQM pipeline is described in detail in Appendix (evaluation_appendix.tex, Section on MQM Evaluation Pipeline), including checklist generation, judge scoring with binding verification, and penalty computation. The main text could still benefit from one sentence on what binding verification adds beyond standard MQM, but the appendix coverage is now adequate.

### Issue 5 (Major, Dataset): IAA should use chance-corrected metric
**RESOLVED.** The paper now reports Krippendorff's alpha = 0.91 on the interval scale (framework.tex, line 13; appendix_human_validation.tex, line 7), computed on 39 double-annotated pairs. This is a chance-corrected metric and exceeds the 0.80 reliability threshold. ICC(2,1) = 0.91 and Pearson r = 0.92 are additionally reported in the appendix.

### Issue 6 (Moderate, Dataset): Only two annotators
**RESOLVED.** The paper now uses three annotators who independently scored 120 (figure, model) pairs (appendix_human_validation.tex, line 3). This is a meaningful improvement from the original two-annotator design.

### Issue 7 (Minor, Dataset): Sampling bias to NLP/ML acknowledged but underemphasized
**REMAINING (Minor).** The dataset section still describes the corpus as "spanning NLP, machine learning, and computational linguistics" without flagging this as a limitation inline. The limitations section does acknowledge this clearly ("findings may not transfer to ... domains outside the computer science and machine learning literature"), so this is adequate but could be more prominent in Section 3 itself.

### Issue 8 (Minor, Dataset): Subset not balanced by difficulty
**REMAINING (Minor).** The paper still does not discuss whether the 100-figure primary subset is balanced by difficulty or complexity beyond chart type. However, the split-half reliability analysis (rho = 0.979) and scale convergence analysis provide indirect evidence that the subset is representative. This mitigates the concern without directly addressing it.

### Issue 9 (Moderate, Dataset): Small n for admittance/inductance (50/48)
**REMAINING (Moderate).** Sample sizes are unchanged at 50 admittance and 48 inductance figures. The limitations section now explicitly flags this: "The admittance and inductance conditions use smaller subsets of 50 and 48 figures; expanding them is a priority." This transparency is appreciated, but the fundamental limitation persists. The directional findings remain convincing; mid-tier model comparisons remain noisy.

### Issue 10 (Major, Framework): Judge validation details insufficient
**RESOLVED.** This was the most significant concern in Round 1. The revision provides substantial new detail:
- 120 (figure, model) pairs across 30 figures and 4 models, scored by 3 annotators (appendix_human_validation.tex).
- Krippendorff's alpha = 0.91, ICC(2,1) = 0.91, Pearson r = 0.92, Spearman rho = 0.87 for inter-annotator reliability.
- Per-pair Pearson r = 0.65 with mean absolute error of 16.9 points for human-judge agreement.
- Model-level ranking rho = 0.80 (n = 4 models) -- notably, the previous claim of rho = 1.0 has been corrected to rho = 0.80, which is more credible and more informative.
- The appendix reports systematic biases (judge is stricter on mid-tier models by ~14.8 points, slightly lenient on weakest model) and states these do not affect rankings.

This is now a solid validation. The per-pair r = 0.65 is honestly reported and shows the judge is imperfect at the individual level but reliable for aggregate comparisons. The correction from rho = 1.0 to rho = 0.80 is commendable.

### Issue 11 (Moderate, Framework): Capability question validation circularity
**RESOLVED.** The capability pipeline now uses a cross-family design: GPT-4o generates candidates, and Mistral Large 3 validates them (evaluation_appendix.tex, Capability Question Pipeline). This directly addresses the circularity concern from Round 1.

### Issue 12 (Moderate, Framework): No prompt sensitivity analysis
**PARTIALLY RESOLVED.** The paper now includes a full prompt inventory in Appendix (appendix_prompts.tex) with all prompt texts reproduced, and states "All evaluated models received the same task prompt for a given condition." The probe designer ablation (GPT-4o vs. Mistral Large) provides indirect evidence of robustness to prompt variation in probe generation. However, there is still no explicit test of prompt sensitivity for the core description or reasoning tasks -- i.e., whether rephrasing the description prompt changes model rankings. This is a common gap in the field and not a dealbreaker.

### Issue 13 (Moderate, Results): Inconsistent application of significance tests
**REMAINING (Minor).** The paper still applies significance tests selectively -- the GPT-5.2/Gemini MQM gap gets p-value and Cliff's delta, the resistance gap gets a p-value, caption bias gets a p-value, but middle-tier comparisons and Qwen scaling trends do not. The inconsistency is less problematic now that the paper focuses on well-separated comparisons rather than making fine-grained mid-tier claims. Downgraded from Moderate to Minor.

### Issue 14 (Minor, Results): No multiple comparison correction
**REMAINING (Minor).** Still not addressed, but the paper makes relatively few pairwise claims and focuses on top vs. bottom contrasts. This is acceptable for the scope of claims made.

### Issue 15 (Minor, Results): 94% vs 98% inconsistency
**RESOLVED.** As noted in Issue 1, both introduction and results now consistently report 98%.

### Issue 16 (Moderate, Results): Capability question analysis is shallow
**RESOLVED.** The results section now includes a detailed per-category breakdown (results.tex, Section 5.3) with specific model comparisons: Gemini dominates counting (89.2% vs 76.1%) and comparison (89.6% vs 77.9%), GPT-5.2 leads computation (82.8% vs 79.4%) and pattern analysis (72.0% vs 70.0%). The analysis discusses complementary strengths (visual extraction vs. derived numerical operations) and notes the sharp drop-off below the frontier pair. This is substantively improved.

### Issue 17 (Minor, Results): Caption bias rounding obscures differences
**RESOLVED.** Table 4 now shows both models at 0.89 and the text states they reach "0.89 [0.85, 0.93] with no significant difference (p = 0.44, n = 99)." The explicit non-significance test makes clear that the identical rounding is not masking a meaningful gap.

### Issue 18 (Moderate, Results): Ablation tests only one target model
**REMAINING (Minor).** The ablation still tests only GPT-5.2 as the target. However, the practical concern (circularity) is mitigated by three factors: (1) the capability validation now uses cross-family models (GPT-4o generates, Mistral validates), (2) the probe designer ablation shows negligible differences, and (3) the paper is transparent about the single-target limitation. Downgraded from Moderate to Minor.

### Issue 19 (Minor, Analysis): Causal claims about training unsupported
**PARTIALLY RESOLVED.** The analysis section still contains "Caption dependency appears tied to how strongly instruction tuning conditions a model to trust provided context over visual evidence" (analysis.tex, line 12). However, the heading now reads "Caption dependency as training artifact, not capability limitation" and the argument is framed more as an interpretation ("appears tied to") rather than a finding. This is borderline -- "appears tied to" is still somewhat assertive given the lack of access to training procedures. A hedge like "may reflect" would be stronger.

### Issue 20 (Minor, Analysis): RLHF speculation needs hedging
**PARTIALLY RESOLVED.** The text still states "This pattern is consistent with RLHF-trained helpfulness pressures" (analysis.tex, line 15), which is framed as consistency rather than causation. The "consistent with" framing is acceptable scientific language, though the paragraph title "The 'must answer' bias" implies a stronger claim than the evidence supports.

### Issue 21 (Minor, Analysis): Correlation of 8 points is low-power
**REMAINING (Minor).** The paper still reports rho = 0.83-0.95 at "the population level" without clarifying that n = 8 models. However, the paper does not make strong claims based on this correlation alone -- it uses it as a setup for the more compelling rank-reversal analysis. The real evidence is the GPT-5.2/Gemini reversal, not the correlation coefficient.

### Issue 22 (Moderate, Conclusion): Human validation rho=1.0 needs context
**RESOLVED.** The rho = 1.0 claim has been replaced with rho = 0.80 (n = 4 models, p < 0.05), and the full validation details are in the appendix. The limitations section accurately reports "Human validation on 120 annotated pairs yielded Krippendorff's alpha = 0.91 and model-level ranking agreement of rho = 0.80 (n = 4 models)." This is honest and appropriately scoped.

### Issue 23 (Minor, Conclusion): Generalization claim too strong
**PARTIALLY RESOLVED.** The conclusion still states "The framework is not specific to scientific figures: any domain where models must acknowledge uncertainty, refuse misleading premises, or infer from partial evidence can apply the same decomposition." This is phrased as an assertion rather than a hypothesis. However, the limitations section appropriately scopes the empirical findings. The conceptual claim is defensible (the A-R-I dimensions are domain-general by construction) even if the empirical validation is domain-specific.

### Issue 24 (Moderate, Cross-cutting): API versions and prompts not reported
**RESOLVED.** Appendix (appendix_reproducibility.tex) now provides: exact model identifiers and backends for all 8 models, Azure API version (2024-12-01-preview), temperature = 0, seed = 42, max tokens, and routing details. Appendix (appendix_prompts.tex) reproduces all prompt families (D1-D4, M1, Q1-Q7, B1-B2, R1-R2, S1-S3) with implementation file paths. This is thorough.

### Issue 25 (Minor, Cross-cutting): No qualitative error examples
**REMAINING (Minor).** The paper still lacks a table of representative fabrication/admission examples across models. The hook example in the introduction provides one case, but systematic qualitative examples would strengthen the paper. This is a nice-to-have, not essential.

### Issue 26 (Moderate, Cross-cutting): LLM judge failure modes not discussed
**PARTIALLY RESOLVED.** The limitations section now mentions "Cross-judge validation with a non-OpenAI model would further strengthen confidence," acknowledging the same-family concern. The capability pipeline now uses cross-family validation (GPT-4o + Mistral Large). The probe designer ablation provides indirect evidence of cross-family robustness. However, there is still no explicit discussion of known LLM-as-judge failure modes (position bias, verbosity bias, self-enhancement bias) in the main text. The caption-bias judge does use randomised A/B ordering to mitigate position bias (evaluation_appendix.tex, line 89), which is good practice but not highlighted as addressing a known failure mode.

---

## Summary of Resolution

| Status | Count | Issues |
|--------|-------|--------|
| RESOLVED | 14 | 1, 2, 3, 5, 6, 10, 11, 15, 16, 17, 22, 24 |
| PARTIALLY RESOLVED | 5 | 4, 12, 19, 20, 26 |
| REMAINING (Minor) | 7 | 7, 8, 9, 13, 14, 21, 25 |
| REMAINING (Major) | 0 | -- |

---

## Updated Section Soundness Scores

| Section | Round 1 | Round 2 | Notes |
|---------|---------|---------|-------|
| Introduction | 4.0 | 4.5 | 94%/98% fixed |
| Related Work | 4.0 | 4.0 | Minor improvements; already solid |
| Dataset | 3.0 | 4.0 | Krippendorff's alpha, 3 annotators, better scoping |
| Framework | 4.0 | 4.5 | Judge validation greatly improved, cross-family capability validation |
| Results | 3.5 | 4.0 | Capability analysis expanded, stats more consistent |
| Analysis | 3.5 | 3.5 | Hedging slightly improved but causal framing persists |
| Conclusion/Limitations | 4.0 | 4.5 | Honest reporting, rho corrected |

---

## New Issues Identified in Round 2

27. **(Minor, Appendix)** The human-judge per-pair correlation (r = 0.65) and mean absolute error (16.9 points) indicate that the automated judge can diverge substantially from human scores at the individual figure level. The paper correctly notes this does not affect model-level rankings, but should mention whether the biases (e.g., -14.8 for Qwen-30B) are stable across chart types or concentrated in specific figure categories.

28. **(Minor, Dataset/Reproducibility)** The reproducibility appendix mentions "250 scientific figures sampled from arXiv publications across four languages (English, Bulgarian, Chinese, German)" but the dataset section states "250 English-language scientific figures." This appears to be a copy-paste artifact from the thesis dataset description. Should be reconciled -- the benchmark as evaluated uses only English figures.

29. **(Minor, Framework)** The capability question validator uses Mistral Large 3, which is good for cross-family validation. However, the seeder is still GPT-4o, and GPT-4o is also the judge for capability scoring. If GPT-4o generates questions that happen to align with its own evaluation biases, this could create a subtle circularity in the capability dimension. The resistance and admittance dimensions are better insulated. Worth noting in limitations.

---

## Overall Assessment

The authors have addressed the two major concerns from Round 1 (judge validation and inter-annotator agreement) thoroughly and honestly. The correction from rho = 1.0 to rho = 0.80 for human-judge agreement is commendable -- it is more credible and still demonstrates adequate reliability. The addition of Krippendorff's alpha = 0.91, three annotators, and detailed validation statistics (per-pair r = 0.65, systematic bias analysis) substantially strengthens the methodology.

The reproducibility improvements are also significant: full prompt inventory, model identifiers, API versions, and routing details. The cross-family capability validation pipeline (GPT-4o seeder + Mistral Large validator) addresses the circularity concern.

Remaining issues are uniformly minor. The small sample sizes for admittance/inductance (50/48) are a genuine limitation but are honestly acknowledged, and the directional findings are robust. The causal language in the analysis section could be further softened. A qualitative error table would be a welcome addition.

The core contribution -- the A-R-I framework and the perception-behaviour disconnect finding -- remains novel and well-supported. The paper is now methodologically sound with appropriate caveats.

### Updated Scores

- **Soundness:** 4.0 / 5
- **Significance:** 4.0 / 5
- **Clarity:** 4.5 / 5
- **Overall Recommendation:** Accept

### Confidence

High. I have verified key claims against the data, reviewed all appendices, and tracked each issue from Round 1. The methodological improvements are genuine and address the most important concerns.
