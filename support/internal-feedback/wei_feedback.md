# Wei's Feedback — Response Tracker

## 1. A-R-I "orthogonal" claim (Section 4.2.4)
**Feedback:** A, R, I aren't necessarily orthogonal unless correlations say so.
**Action:** Replaced "near-orthogonal" with "conceptually distinct" throughout. The axes are designed to capture different failure modes (honesty about blur, rejection of false premises, reasoning from partial evidence). With n=13 models, correlation testing is underpowered. The empirical evidence (rank inversions: GPT-5.2 high I but low R, Gemma low A low R) supports distinctness without needing a statistical orthogonality claim.
**Status:** Done

## 2. Figure 4.3 total not 1,005?
**Feedback:** The total of figures are not 1,005?
**Action:** The chart was missing the "Multi-language" subset (177 figures). The four visible bars summed to 828, not 1,005. Added a 5th bar for Multi-language (117 line, 55 bar, 5 pie), so all bars now visually sum to 1,005.
**Status:** Done

## 3. Table 6.1 E/H columns
**Feedback:** Where do errors/hallucinations per figure come from, are they part of MQM?
**Action:** Clarified caption: E = mean MQM errors per figure, H = mean fabricated content per figure (a subset of E counting descriptions of elements not present in the figure). Both are derived from the same MQM judge evaluation, not a separate assessment.
**Status:** Done

## 4. Table 6.1(b) per-model error distributions + examples
**Feedback:** Do you have detailed error distributions per model? Also, examples are missing.
**Action:** Per-model error distributions already exist in the appendix (error profile tables). Added a new sideways Table (tab:error-examples) in the appendix with one concrete error example per sub-type, showing model output vs ground truth. Table 6.1(b) caption now cross-references it.
**Status:** Done

## 5. Table 6.3 capability category definitions
**Feedback:** Comp, Val, etc. — cannot find their definitions.
**Action:** Added Appendix Table A.x (tab:capability-cats) defining all 5 categories with descriptions and example questions. Table 6.3 caption now cross-references it.
**Status:** Done

## 6. Section 6.4 broken references
**Feedback:** Some references are broken.
**Action:** All references verified — resolved in earlier revision. Wei was reading an older version. Current build has zero broken refs (170 labels, 106 refs, all matched).
**Status:** Done (no change needed)

## 7. Table 6.4 Pa/Ps abbreviations undefined
**Feedback:** Pa = passive axis-.. Ps = .. undefined?
**Action:** Added Appendix Table A.x (tab:ari-defs) defining all 8 A-R-I sub-components with full descriptions. Table 6.4 caption now cross-references it instead of inline definitions.
**Status:** Done

## 8. "tolerance accepts +/-3 percentage points" — which setup?
**Feedback:** Which setup does this apply to, MQM?
**Action:** Clarified: "our MQM judge instructions already accept ±3 percentage points as correct."
**Status:** Done

## 9. MQM penalises errors, not thoroughness
**Feedback:** MQM doesn't penalise thoroughness but errors; long texts tend to contain more errors.
**Action:** Reframed in all 3 locations (discussion.tex x2, conclusion.tex x1). Now states: longer descriptions contain more verifiable claims, increasing the error surface — a structural trade-off between detail and score, not a flaw in MQM itself.
**Status:** Done

## 10. System-level Spearman doesn't mean LLM-as-judge is good
**Feedback:** Good system-level scores don't mean LLM-as-judge is good; segment-level is more nuanced.
**Action:** No change needed. Section 7.4 already leads with the ranking-scoring dissociation, explicitly reports per-figure divergence of 10-25 points, and frames system-level rho as sufficient for ranking only. Both sides are presented.
**Status:** Done (no change needed)

## 11. Section 7.6: do MQM errors affect comprehension?
**Feedback:** Do some MQM errors affect comprehension?
**Action:** Added paragraph in Section 7.6 noting that shared perceptual weaknesses (e.g., Claude's colour confusion) can produce correlated failures across description and comprehension. Flagged formal per-figure correlation analysis as future work.
**Status:** Done

## 12. Future work: why VLMs are good or bad
**Feedback:** Missing the question of "why". Future work should mention internal representations, attention, mechanistic interpretability.
**Action:** Added "Mechanistic interpretability" paragraph in future work: internal representations, attention visualisation, saliency mapping on failure cases, visual encoder vs language decoder attribution.
**Status:** Done
