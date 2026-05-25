# ACL Reviewer 1 -- Methodology Rigor: Full Paper Review

**Paper:** SciFig-Eval: Benchmarking Perception, Reasoning, and Behaviour in Vision-Language Models on Scientific Figures

**Overall Recommendation:** Borderline Accept (leans accept)

**Overall Soundness:** 3.5 / 5

---

## Section-by-Section Soundness Scores

### Introduction -- Soundness: 4/5

The introduction is well-motivated and clearly frames the perception-behaviour disconnect. The hook example (GPT-5.2 fabricating "Customer Support" on a blurred chart) is compelling and concrete. The A-R-I framing is introduced at the right level of abstraction.

**Issues:**
1. The claim "fabricates answers for elements it cannot see 94% of the time" (line ~11, introduction) does not match the statistics file, which shows GPT-5.2 fabrication rate at 98% (mean 0.98, CI [0.94, 1.0]) for active admittance. The 94% figure appears to be the lower bound of the CI, not the point estimate. The paper should report the point estimate (98%) or clearly label which statistic is being quoted.
2. "while a comparably-scoring model admits uncertainty 90% of the time" -- Gemini's MQM is 90.2 vs GPT-5.2's 91.6. Whether a 1.4-point gap makes them "comparably-scoring" is a judgment call, but the CIs do overlap slightly at some conditions, so this is defensible.

**Strengths:**
- Clean narrative arc from concrete failure to framework motivation.
- Contributions are specific and enumerated precisely.

---

### Related Work -- Soundness: 4/5

Thorough and well-organized across three subsections. Coverage of recent chart benchmarks (ChartMuseum, ChartQAPro, EncQA, MultiChartQA) is up-to-date. The connection to hallucination, sycophancy, and abstention literatures is appropriate.

**Issues:**
3. No comparison to CHAOS or CHART NOISe methodologies in terms of what transforms they use vs. what SciFig-Eval uses. A sentence or two on methodological differentiation (not just scope) would strengthen this.
4. The MQM adaptation is described as using "checklist-based scoring and binding verification," but the related work section does not discuss how this differs from standard MQM beyond a passing mention.

**Strengths:**
- Situates A-R-I clearly within honesty/abstention/sycophancy literatures.
- Honest about what existing benchmarks do well.

---

### Dataset -- Soundness: 3/5

This section has several methodological concerns.

**Issues:**
5. **Inter-annotator agreement metric is underspecified.** The paper reports "94% agreement on verifiable checklist items (exact values, label names, axis ranges)." This is raw agreement, not a chance-corrected metric (Cohen's kappa, Krippendorff's alpha). For a benchmark paper at ACL, chance-corrected IAA is expected. With structured checklist items, 94% raw agreement could correspond to different kappa values depending on label distribution.
6. **Annotator count is low.** Two annotators with a third adjudicator is minimal. For a benchmark, at least two independent annotators on all items with a reported kappa would be standard.
7. **Sampling bias.** The corpus is drawn exclusively from arXiv papers in NLP/ML/CL. This is acknowledged in limitations but should be flagged more prominently in the dataset section itself. Bar/line/pie are the only chart types; scatter plots and heatmaps (common in ML papers) are absent.
8. **Primary subset selection.** The stratified random sample (seed=42) of 100 figures from 250 is reasonable, but the paper should clarify whether the 100-figure subset is balanced by complexity or difficulty, not just chart type. A subset that happens to contain mostly simple figures would bias results.
9. **Admittance/inductance sample sizes are small.** 50 admittance blur candidates and 48 inductance blur candidates yield wide confidence intervals (e.g., Gemini admittance: [82%, 98%], GPT-5.2 admittance: [0%, 14%]). While the directional findings are clear, some model-level comparisons in the middle of the pack cannot be distinguished from noise at these sample sizes. For example, Llama 4 (22%) vs. Qwen-235B (12%) on active admittance -- the CIs likely overlap substantially.

**Strengths:**
- Depth-over-breadth is a defensible design choice, and the paper is transparent about it.
- The seed is reported for reproducibility.
- The multi-model consensus approach for blur candidate selection is thoughtful.

---

### Framework -- Soundness: 4/5

The three-dimension framework (perception, reasoning, behaviour) is clearly described and the A-R-I decomposition is well-motivated. The operationalization of each A-R-I component is concrete.

**Issues:**
10. **Judge validation is incomplete.** The paper uses GPT-4o as the automated judge for MQM scoring. Human validation is mentioned ("perfect agreement, rho = 1.0") but no details are given in the main text: how many figures were validated? What aspects of the MQM judgment were validated? A rho of 1.0 on model rankings is suspicious -- this likely means the rank-order of 8 models was identical, which is less impressive than it sounds for ordinal data with clear performance tiers.
11. **Capability question generation pipeline.** Questions are "generated from the figure image and expert annotation, validated by a separate model, and filtered to one accepted question per category." Using an LLM to validate LLM-generated questions raises circularity concerns. The ablation in Section 5.5 addresses probe designer independence for behavioral probes, but not for capability questions.
12. **No discussion of prompt sensitivity.** All models receive "identical prompts," but the paper does not report what those prompts are in the main text or whether any prompt tuning was done. Prompt sensitivity is a known confound in VLM evaluation.

**Strengths:**
- A-R-I dimensions are well-defined and empirically separable.
- The distinction between admittance (unrecoverable) and inductance (inferable) is a genuine conceptual contribution.
- Binding verification in MQM is a meaningful methodological improvement over standard checklist scoring.

---

### Results -- Soundness: 3.5/5

Results are generally well-presented with confidence intervals throughout. The central finding (perception-behaviour disconnect) is convincing.

**Issues:**
13. **Statistical tests are inconsistent.** The GPT-5.2 vs. Gemini MQM gap is tested with a p-value and Cliff's delta. The resistance gap is tested with a p-value and n. But many other comparisons (e.g., middle-tier model rankings, Qwen family scaling trends) are reported without any significance test. If the paper is going to use significance tests, they should be applied consistently.
14. **Multiple comparisons.** With 8 models and many pairwise comparisons, no correction for multiple testing is applied or discussed. This is common in the field but worth noting for a methodology-focused review.
15. **The "94% fabrication" claim in the introduction.** As noted in Issue 1, the statistics file shows GPT-5.2 fabricates at 98% (point estimate) with CI [94%, 100%]. The introduction says "94% of the time." The results section says "98% of the time" (Section 5.4, line about "fabricating answers 98% of the time"). These need to be reconciled. The 94% in the introduction appears to be the CI lower bound.
16. **Capability question results are thin.** Table 4 shows accuracy percentages but there is minimal analysis of capability questions beyond "Gemini leads overall, while GPT-5.2 is strongest on computation and pattern analysis." No breakdown by chart type for reasoning, no error analysis, no discussion of question difficulty.
17. **Caption bias resistance values differ between Table 4 and statistics.** Table 4 shows CapB resistance for GPT-5.2 and Gemini both at 0.89. The statistics file shows GPT-5.2 at 0.8906 and Gemini at 0.8939 -- these round to 0.89, but the paper calls these identical when they are not. Table 4 for Qwen-235B shows 0.54 but the statistics file shows 0.5374, which rounds correctly. Minor, but the paper should not claim both models "reach 0.89" when there is a gap, however small.
18. **Probe designer ablation is limited.** The ablation compares GPT-4o vs. Mistral Large probes on 50 figures with GPT-5.2 as target. This tests only one target model. If the concern is circularity, the ablation should ideally test multiple target models, since GPT-5.2 might be uniquely robust to probe designer variation while weaker models might show larger differences.

**Strengths:**
- Bootstrap CIs are reported throughout -- this is above-average statistical practice for the field.
- The "confident fabricator" characterization of GPT-5.2 is well-supported.
- Split-half reliability analysis is a good robustness check.
- The inductance validation (correct-given-fabrication rates diverge between admittance and inductance conditions) is a clean experimental design.

---

### Analysis -- Soundness: 3.5/5

The analysis section provides interpretive depth beyond the results. The presupposition embedding analysis and the caption dependency analysis are insightful.

**Issues:**
19. **Causal claims about training.** "Caption dependency appears tied to how strongly instruction tuning conditions a model to trust provided context over visual evidence." This is a hypothesis, not a finding. The paper has no access to training data or procedures and cannot distinguish instruction tuning effects from pretraining effects. Should be framed more cautiously.
20. **The RLHF "must answer" interpretation.** "This pattern is consistent with RLHF-trained helpfulness pressures." Again, this is speculation. Multiple models with different training procedures show similar patterns. The paper should present this as a hypothesis.
21. **Cross-dimension correlation.** The reported rho of 0.83-0.95 between quality and behavior at "the population level" -- what does "population level" mean here? Across all 8 models? A correlation of 8 data points with rho 0.83 is not particularly informative (p ~ 0.01 for n=8 at rho=0.83, but statistical power is very low).

**Strengths:**
- The presupposition embedding analysis connecting to Loftus eyewitness findings is a creative and appropriate analogy.
- The observation that caption dependency is non-monotonic within Qwen is a genuine finding that resists simple explanations.
- Methodological robustness paragraph directly addresses reviewer concerns preemptively.

---

### Conclusion and Limitations -- Soundness: 4/5

The conclusion is appropriately scoped. The limitations section is commendably honest about sample sizes, chart type coverage, and judge reliance.

**Issues:**
22. **"Perfect agreement (rho = 1.0)" for human validation needs more context.** How many figures? How many annotators? What was being compared -- full MQM scores or just rank ordering? A perfect rank correlation of 8 models is achievable if the models are well-separated, so this does not validate fine-grained MQM scoring.
23. The claim "any domain where models must acknowledge uncertainty..." is strong. The A-R-I framework was tested only on scientific figures. Generalization claims should be softened or removed.

**Strengths:**
- Limitations section is thorough and pre-empts likely reviewer concerns.
- The practical recommendation (do not select VLMs on quality alone) is well-earned by the evidence.

---

## Cross-Cutting Issues

24. **Reproducibility.** The paper specifies temperature=0 and GPT-4o as judge, but does not report: API dates/versions (model snapshots change), exact prompt templates used for each evaluation condition, or seeds for any stochastic components beyond dataset sampling. For closed-model evaluations, API version dates are critical.

25. **No error analysis or qualitative examples beyond the hook.** The paper would benefit from a table of representative fabrication examples across models, showing what GPT-5.2 fabricates vs. what Gemini admits vs. what Phi-4 produces. This would help readers assess whether the automated judge is classifying correctly.

26. **LLM judge failure modes.** The paper acknowledges using GPT-4o as judge but does not discuss known failure modes of LLM-as-judge (position bias, verbosity bias, self-enhancement bias). GPT-4o judging GPT-5.2 outputs raises potential bias concerns (same model family). Was any cross-family judge validation done?

---

## Verification Against Statistics File

I verified the following claims against `all_statistics.json`:

| Claim | Paper Value | Statistics Value | Match? |
|-------|------------|-----------------|--------|
| GPT-5.2 baseline MQM | 91.6 | 91.5914 | Yes (rounded) |
| Gemini baseline MQM | 90.2 | 90.1724 | Yes (rounded) |
| GPT-5.2 MQM CI | [90.4, 92.8] | [90.37, 92.77] | Yes (rounded) |
| Gemini MQM CI | [88.9, 91.4] | [88.88, 91.43] | Yes (rounded) |
| Phi-4 MQM | 62.2 | 62.158 | Yes |
| Gemini resistance | 0.91 [0.89, 0.93] | 0.9113 [0.8913, 0.93] | Yes |
| GPT-5.2 resistance | 0.81 [0.79, 0.84] | 0.8133 [0.786, 0.8407] | Yes |
| Phi-4 resistance | 0.21 [0.18, 0.24] | 0.2113 [0.1827, 0.24] | Yes |
| GPT-5.2 active admits | 6% | 6% (0.06) | Yes |
| GPT-5.2 fabricates | 98% (results), 94% (intro) | 98% (0.98), CI lower 94% | **Mismatch in intro** |
| Gemini active admits | 90% [82%, 98%] | 0.90 [0.82, 0.98] | Yes |
| Llama contra resistance | 0.76 | 0.758 | Yes (rounded) |
| Llama inexist resistance | 0.63 | 0.632 | Yes (rounded) |
| Llama unanswerable | 0.94 | 0.94 | Yes |
| GPT-5.2 inductance correctness | 74% | ? (not directly in early portion of stats) | Could not fully verify |

**Summary of verification:** Numbers are consistent with one exception. The introduction states "fabricates answers 94% of the time" but the point estimate is 98%; 94% is the CI lower bound. The results section correctly states 98%.

---

## Summary of Numbered Issues

| # | Severity | Section | Issue |
|---|----------|---------|-------|
| 1 | Minor | Intro | 94% fabrication rate is CI lower bound, not point estimate |
| 2 | Minor | Intro | "Comparably-scoring" is borderline with 1.4-point gap |
| 3 | Minor | Related Work | Missing methodological comparison with CHAOS/CHART NOISe |
| 4 | Minor | Related Work | MQM adaptation differences underexplained |
| 5 | Major | Dataset | IAA should use chance-corrected metric |
| 6 | Moderate | Dataset | Only two annotators |
| 7 | Minor | Dataset | Sampling bias to NLP/ML acknowledged but underemphasized |
| 8 | Minor | Dataset | Subset not balanced by difficulty |
| 9 | Moderate | Dataset | Small n for admittance/inductance (50/48) |
| 10 | Major | Framework | Judge validation details insufficient |
| 11 | Moderate | Framework | Capability question validation circularity |
| 12 | Moderate | Framework | No prompt sensitivity analysis |
| 13 | Moderate | Results | Inconsistent application of significance tests |
| 14 | Minor | Results | No multiple comparison correction |
| 15 | Minor | Results | 94% vs 98% inconsistency |
| 16 | Moderate | Results | Capability question analysis is shallow |
| 17 | Minor | Results | Caption bias rounding obscures differences |
| 18 | Moderate | Results | Ablation tests only one target model |
| 19 | Minor | Analysis | Causal claims about training unsupported |
| 20 | Minor | Analysis | RLHF speculation needs hedging |
| 21 | Minor | Analysis | Correlation of 8 points is low-power |
| 22 | Moderate | Conclusion | Human validation rho=1.0 needs context |
| 23 | Minor | Conclusion | Generalization claim too strong |
| 24 | Moderate | Cross-cutting | API versions and prompts not reported |
| 25 | Minor | Cross-cutting | No qualitative error examples |
| 26 | Moderate | Cross-cutting | LLM judge failure modes not discussed |

---

## Overall Assessment

### What This Paper Does Well

1. **The A-R-I framework is a genuine contribution.** The admittance-inductance distinction (unrecoverable vs. inferable blurred elements) is novel and well-operationalized. The finding that models achieve 21-80% correctness on inferable elements but 0-14% on unrecoverable elements is clean evidence that the distinction is real.

2. **The perception-behaviour disconnect is well-demonstrated.** The GPT-5.2 vs. Gemini comparison -- near-identical MQM, opposite admittance -- is the kind of finding that changes how people think about evaluation.

3. **Statistical practice is above field average.** Bootstrap CIs throughout, split-half reliability, scale analysis, and an ablation study all show methodological care.

4. **The paper is well-written.** Clear structure, precise claims, and honest limitations.

### What Needs Work

1. **Judge validation is the weakest link.** A rho of 1.0 on 8-model rankings is a low bar. The paper needs finer-grained human-judge agreement analysis (per-figure MQM correlation, not just ranking) and should discuss GPT-4o judging GPT-5.2 outputs as a potential conflict.

2. **Inter-annotator agreement needs a chance-corrected metric.** 94% raw agreement is not sufficient for a benchmark paper.

3. **Sample sizes for admittance/inductance are borderline.** 50 and 48 figures make the directional findings convincing but limit the precision of model-level comparisons in the middle of the ranking.

4. **Reproducibility details are missing.** API versions, exact prompts, and judge prompts should be in the appendix if not the main text.

### Confidence

I am confident in this review. The statistical claims are largely verified against the data. The methodological concerns are standard for benchmark papers but non-trivial. The core contribution (A-R-I framework and perception-behaviour disconnect) is sound and novel.
