# ACL Reviewer 1 -- Methodology Rigor
## Wave 1 Combined Review: Related Work, Dataset, Framework

---

## Section 1: Related Work (Section 2)

### Soundness: 4/5

The related work is well-organized into three coherent subsections and positions the contribution clearly against prior benchmarks and hallucination work. The gap statement is precise and defensible. However, there are methodological framing concerns.

### Specific Issues

1. **Line 9 -- "None assess behavioral reliability" is too strong.** HallusionBench (cited on line 17) does assess a form of behavioral reliability through visual illusions and language traps. The claim should be scoped: "None assess behavioral reliability *on scientific figures*" or "None combine quality measurement with behavioral probes." As written, a reviewer familiar with HallusionBench will flag this as inaccurate.

2. **Line 23 -- Psychology citations are bundled without differentiation.** Four cognitive science principles are listed in a single sentence with four citations. This reads as name-dropping rather than grounding. Each principle maps to a specific probe type (presupposition -> inexist, anchoring -> contra, cooperative principle -> unanswerable, sycophancy -> caption bias), but this mapping is invisible here. Even one clarifying clause per principle would strengthen the claim that probes are "grounded in" these theories rather than merely "inspired by" them.

3. **Line 31 -- "strong agreement between LLM judges and human preferences" (re: Zheng et al.)** This validation was on MT-Bench (open-ended chat), not on structured chart description evaluation. The domain transfer assumption should be acknowledged, or the paper should state that they perform their own human-judge validation (which they do -- rho=1.0 is mentioned in the framework section). Cross-referencing that result here would strengthen the justification.

4. **Line 35 -- "first framework that unifies description quality measurement with behavioral reliability assessment on scientific figures."** This is a strong novelty claim. It is likely true but should be hedged slightly or supported by the comprehensive comparison table in the appendix (reference it here).

5. **Missing: No discussion of LLM-as-judge limitations.** The paper cites Zheng et al. for validation but does not mention known failure modes (position bias, verbosity bias, self-preference). These are addressed later in the framework section's A/B design, but the related work should acknowledge the broader concern.

### Missing Elements

- Discussion of concurrent/recent work on chart hallucination (e.g., ChartBench's hallucination subset, if applicable).
- Any mention of robustness evaluation under image degradation in VLM benchmarks (some exist for natural images).

### Strengths

- Clean three-part structure: benchmarks -> hallucination -> methodology.
- The gap statement (line 35-36) is precise and sets up the contribution well.
- Appropriate use of \citet vs \citep throughout.
- Appendix deferral for the full benchmark comparison table is good space management.

### Suggestions

- Soften line 9 to scope the "none" claim to scientific figures specifically.
- Add a single sentence acknowledging LLM-as-judge limitations before citing your mitigations.
- Consider moving the psychology citations to the framework section where the probes are fully described, and keeping the related work reference lighter.

---

## Section 2: Dataset (Section 3.1)

### Soundness: 3/5

The dataset description is concise and the table is clean. However, several methodological details critical for reproducibility and validity assessment are missing or insufficiently justified.

### Specific Issues

6. **Line 3 -- No description of the arXiv sampling strategy.** "Extracted from arXiv papers" is insufficient. Which fields? Which date range? Were papers randomly sampled or purposively selected? Were figures extracted automatically (e.g., PDFFigures2) or manually? Sampling bias is a serious concern for a benchmark paper: if figures were cherry-picked for visual clarity, results may not generalize. Even a brief statement ("from 2020-2024 papers across CS, physics, and biology") would help.

7. **Line 3 -- Chart type distribution is imbalanced but unjustified.** 99/99/52 is roughly 2:2:1 for bar:line:pie. Why this ratio? Is it reflective of the distribution in arXiv papers? If so, cite evidence. If purposive, justify the design choice. The primary subset (40/40/20) preserves this ratio, which is good, but the rationale is missing.

8. **Line 5 -- "structured expert annotation" -- who are the experts?** How many annotators? What are their qualifications? Is there inter-annotator agreement (IAA) reported? For a benchmark paper at ACL, IAA is expected. If a single annotator created all 250 annotations, this is a significant limitation that should be disclosed.

9. **Line 5 -- "verified against the original PDF context" -- verification process unclear.** Who verified? Was there a second annotator? What was the error rate before/after verification? "Verified" without a described process is a trust-me statement.

10. **Line 8 -- Subset sizes may be underpowered.** The ablation subset is 50 figures (20/20/10). For probe-designer independence, this means comparing probe performance across designers on only 10 pie charts. With 8 models, that is 80 model-figure pairs for pie charts -- possibly sufficient for rank correlation but tight for any per-type analysis. The paper should acknowledge this limitation or justify the sample size.

11. **Line 11 -- "multi-model consensus" for blur candidate identification.** How many models? What threshold for consensus? This is a methodological choice that directly affects what gets measured (admittance/inductance), so it needs specification, not just an appendix pointer.

12. **No mention of language or domain diversity.** The dataset is English-only (stated) but there is no discussion of domain coverage. Are all figures from CS? Are there figures from medicine, physics, social sciences? Domain diversity affects generalizability claims.

13. **Table 1 -- "Adversarial stimuli" counts need clarification.** Resistance probes: 250 means one per figure? Or 250 total probes across three types (which would be ~83 per type)? Line 10 says "three types per figure" which would be 750 total probes. The table count is ambiguous -- does "250" mean 250 figures each with 3 probes = 750 probes, or 250 probes total?

### Missing Elements

- Inter-annotator agreement statistics.
- Sampling methodology for arXiv paper/figure selection.
- Domain distribution of source papers.
- Justification for chart type ratios.
- Power analysis or sample size justification.

### Strengths

- Clean, informative table.
- Stratified sampling with fixed seed is good practice.
- The nested subset design (250 -> 100 -> 50) is methodologically sound for enabling different analysis granularities.
- Mentioning the dashboard for human review of blur candidates signals a careful process.

### Suggestions

- Add 2-3 sentences on the arXiv sampling strategy (fields, date range, extraction method).
- Report IAA or explain why single-annotator is sufficient (e.g., checklist items are objective/verifiable).
- Clarify the probe count ambiguity in Table 1 (250 figures x 3 types = 750 probes).
- Acknowledge the English-only, potentially CS-heavy limitation explicitly.

---

## Section 3: Framework (Section 3)

### Soundness: 4/5

This is the strongest section methodologically. The 2x2 matrix is a clear organizational device, the MQM adaptation is well-described, and the psychology-grounded probe design is genuinely novel. The A-R-I decomposition is the paper's main theoretical contribution and is presented with empirical grounding. Two concerns prevent a 5.

### Specific Issues

14. **Line 37 -- rho=1.0 Spearman correlation is extraordinary and suspicious.** Perfect rank correlation between automated MQM and human rankings demands scrutiny. How many models were ranked? If 8 models, rho=1.0 on 8 data points is possible but should be reported with the p-value and sample size. How many human rankers? Was there consensus? A perfect correlation could also indicate overfitting the scoring rubric to match a single human ranker. This is the most critical methodological concern in the section.

15. **Line 29 -- MQM formula normalization.** The formula divides by D (maximum possible penalty), but D depends on the checklist composition, which varies by chart type (14/15/11 items). This means MQM scores are not directly comparable across chart types without acknowledging the different denominators. Is cross-type comparison intended? If so, the normalization needs discussion.

16. **Line 42 -- "20-40% deviation" for anchoring sweet spot.** Is this range empirically validated or adopted from the psychology literature? If empirical, what was the pilot study? If from literature, cite the specific finding. As written, it reads as a design choice without justification.

17. **Line 44 -- A/B randomization for caption bias judging.** This is excellent methodology for eliminating position bias. However, is the randomization per-claim or per-figure? If per-figure, all claims for one figure get the same order, which could introduce correlated errors. Specify.

18. **Line 63 -- Resistance scoring rubric (1.0/0.5/0.0).** Who designed this rubric? Is there human validation of the judge's rubric application? What is the inter-rater reliability between the LLM judge and human scorers on resistance probes? The caption bias section mentions judge validation, but resistance scoring validation is not mentioned.

19. **Line 70 -- Admittance: "A model can do both simultaneously."** This is an important observation, but the scoring is unclear. If a model admits AND fabricates, what is its admittance score? Is admittance binary (admits = 1, doesn't = 0) or graded? The decomposition into two binary dimensions is described but the aggregation into a single admittance score is not.

20. **Line 74 -- Inductance: "21-81% correctness on inferable elements versus 0-14% on non-inferable."** These are compelling numbers that validate the inferable/non-inferable distinction. However, the sample sizes behind these ranges are not stated here. With only 48-50 blur candidates, split into inferable and non-inferable, the per-cell counts could be very small (potentially <10 per model per category). Report sample sizes.

21. **Line 76 -- "highest-scoring model on MQM admits visual limitations only 6% of the time."** This is the paper's headline finding, but it appears in the framework section rather than results. Consider whether this belongs here or whether a forward reference is more appropriate. Including specific results in the framework description blurs the line between methodology and findings.

22. **The 2x2 matrix (Table 2) -- "passive admittance / inductance" in the Description/Adversarial cell.** The distinction between passive and active evaluation modes is introduced in the table before being explained in the text. Consider reordering or adding a brief note.

### Missing Elements

- Validation of resistance probe scoring (LLM judge vs. human on a sample).
- Confidence intervals or variance estimates for any reported metrics.
- Discussion of edge cases in the MQM scoring (what happens when a model describes elements not on the checklist? Is this penalized or ignored?).
- Cost and latency estimates for the full evaluation pipeline.

### Strengths

- The 2x2 matrix is an elegant organizational device that makes the contribution immediately clear.
- Psychology-grounded probe design with specific citations is genuinely novel and well-executed.
- Binding verification and deduplication engine show careful attention to scoring artifacts.
- The A/B randomization for caption bias judging is strong methodology.
- The A-R-I framework is a real conceptual contribution, not just a label. The inferable vs. non-inferable distinction with empirical validation (21-81% vs. 0-14%) is convincing.
- The inductance dimension is creative and captures something no existing benchmark measures.

### Suggestions

- Report p-value and human ranker details for the rho=1.0 claim. If based on a single ranker, add a second.
- Clarify the admittance aggregation scoring.
- Move specific numerical results (6% admittance, 21-81% inductance) to the results section or mark them clearly as previews.
- Add a brief discussion of MQM cross-chart-type comparability.
- State sample sizes for the inductance validation numbers.

---

## Overall Assessment

| Section | Soundness | Key Concern |
|---|---|---|
| Related Work | 4/5 | Overclaims on "none assess behavioral reliability"; LLM-as-judge limitations unaddressed |
| Dataset | 3/5 | Missing IAA, sampling strategy, and domain distribution; probe count ambiguous |
| Framework | 4/5 | rho=1.0 needs scrutiny; admittance aggregation unclear; sample sizes for inductance validation missing |

The framework section is the clear strength -- the A-R-I decomposition and psychology-grounded probe design are genuine contributions. The dataset section is the weakest link: a benchmark paper lives or dies on its dataset construction methodology, and key details (annotator qualifications, IAA, sampling strategy) are absent. These could be in the appendix, but they should at least be summarized in the main text.

The most actionable fix is to add 3-4 sentences to the dataset section covering sampling strategy, annotator details, and IAA. The most important fix is to scrutinize and properly report the rho=1.0 claim in the framework section.
