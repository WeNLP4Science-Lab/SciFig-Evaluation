# ACL Reviewer 2 -- Novelty & Contribution: Round 2 Review

**Paper:** SciFig-Eval: Evaluating Scientific Figure Understanding across Perception, Reasoning, and Behaviour
**Reviewer Role:** Novelty & Contribution (Reviewer 2)
**Review Type:** Revision check against Round 1 feedback

---

## Status of Previous Issues

### Issue 1: Strengthen the distinction from CHOCOLATE/ChartHal/CHAOS
**STATUS: RESOLVED**

The revision addresses this directly. The related work section now explicitly names CHOCOLATE and ChartHal and explains what they measure (structured factual errors in chart captions and answers) versus what A-R-I adds (controlled selective blur that distinguishes unrecoverable from inferable missing evidence, plus false-premise resistance that separates presupposition embedding from explicit contradiction). The new benchmark comparison table (Table A10, Appendix) provides the direct comparison I requested, showing columns for scientific figures, open perception, stress tests, misleading context, uncertainty, and behavioural profile. SciFig-Eval is the only benchmark checking all seven columns. CHAOS and CHART NOISe are also cited with a clear statement of what they cover (perturbation and corruption) and what they do not (epistemic honesty, misleading context resistance). This was a key weakness and it is now adequately addressed.

### Issue 2: Expand the inductance analysis
**STATUS: PARTIALLY RESOLVED (REMAINING)**

The results section now reports inductance correctness ranges (21%-80% for inferable elements, 0%-14% for unrecoverable elements) and highlights GPT-5.2's 74% inductance correctness vs. 14% admittance correctness as empirical validation that A-R-I separates inference from fabrication. This is a meaningful improvement -- the numbers make the admittance-inductance distinction concrete and testable.

However, my original request was for analysis of *what makes an element inferable vs. unrecoverable*. Can inferability be predicted from visual features (e.g., colour consistency, axis regularity, legend proximity)? The paper still treats inferability as a binary label assigned during construction rather than analysing the visual properties that enable or prevent inference. This would elevate inductance from a measurement category to a finding about how visual reasoning works. The issue is less severe now that the quantitative validation is present, but the deeper analysis remains missing.

### Issue 3: Connect to calibration literature
**STATUS: RESOLVED**

The related work section now includes an explicit sentence: "Our admittance dimension relates to the broader question of whether models know what they do not know, studied in calibration research where models assign confidence scores to predictions" with a citation to Kadavath et al. (2022). This is exactly the connection I asked for. It is brief but sufficient -- the paper does not overclaim the parallel, simply acknowledges it.

### Issue 4: Consider dropping or compressing the basic transform results
**STATUS: PARTIALLY RESOLVED (REMAINING)**

The transform results remain in the paper at roughly the same level of detail (Section 5.2, "Transform robustness" paragraph). They still report rotation as most damaging (19.4 MQM points), noise as negligible, and in-paper-blur as catastrophic. These are unsurprising findings that overlap with CHAOS.

That said, the revised paper compresses these into a single paragraph rather than giving them a full subsection, and the space savings appear to have been redirected toward the behavioural results (active/passive admittance, inductance validation, ablation). This is a reasonable editorial choice. The transforms provide context for the selective blur methodology, even if the individual findings are not novel. I consider this partially addressed -- the compression helps, but I would still prefer seeing more space given to the inductance analysis (Issue 2) rather than restating expected transform results.

### Issue 5: Add cross-judge validation
**STATUS: REMAINING**

The limitations section acknowledges this gap directly: "Cross-judge validation with a non-OpenAI model would further strengthen confidence." The probe designer ablation (GPT-4o vs. Mistral Large as probe generators) is presented as partial evidence of robustness, but this tests probe generation, not judging. The paper relies on a single GPT-4o judge throughout. Human validation ($\alpha = 0.91$, $\rho = 0.80$) on 120 pairs partially mitigates the concern, but cross-judge validation remains absent.

This is an acknowledged limitation rather than a flaw -- the authors are transparent about it. But for a benchmark paper at ACL, having at least a small-scale cross-judge check (even 50 pairs scored by Claude or Gemini as judge) would meaningfully strengthen the contribution.

### Issue 6: A-R-I branding is somewhat forced (electrical engineering metaphor)
**STATUS: RESOLVED**

The framework section now includes an honest framing: "We borrow the terminology from circuit analysis, where admittance governs how freely current passes, resistance opposes it, and inductance generates it from changing fields, as a loose analogy for how models handle, reject, or reconstruct visual information." The key phrase is "loose analogy" -- the paper no longer implies a deep theoretical mapping. It uses the terminology as a naming convention and immediately defines each term operationally in plain language. This is a pragmatic resolution. The names are memorable even if the metaphor is imperfect.

### Issue 7: Resistance is not sufficiently differentiated from prior work
**STATUS: RESOLVED**

The probe taxonomy table (Table A11) clearly maps each probe family to its input manipulation, target behaviour, cognitive motivation, and A-R-I axis. The inexist/contra/unanswerable decomposition is now explicitly tied to presupposition embedding, anchoring bias, and cooperative pressure, with citations to Loftus (1975) and Tversky & Judgment (1974). The distinction from POPE (which tests object hallucination, not presupposition-based deception) is now clear from context, even if not stated in a single sentence. The cognitive motivation column in the taxonomy table is what makes this work -- it shows that the resistance probes are theory-driven, not just variations on "ask about things that aren't there."

---

## New Issues Identified in Revision

### New Issue 1: Dataset description mentions four languages but paper evaluates English only

The reproducibility appendix states: "The evaluation dataset comprises 250 scientific figures sampled from arXiv publications across four languages (English, Bulgarian, Chinese, German)." However, the dataset section says: "The benchmark comprises 250 English-language scientific figures." These statements appear contradictory. The broader thesis corpus may span four languages, but the benchmark is English-only. The reproducibility appendix text should be corrected to avoid confusion.

### New Issue 2: The "8 models" framing underweights the Qwen family dominance

Three of eight models are Qwen variants. This means 37.5% of the model set is a single family. While the within-family scaling analysis is valuable, the paper should acknowledge that the eight-model comparison is not eight independent data points. Conclusions like "across eight models" may overstate generalizability when three share an architecture and training pipeline.

---

## Updated Scores

| Criterion | Round 1 | Round 2 | Change |
|-----------|---------|---------|--------|
| Excitement | 3.5/5 | 3.75/5 | +0.25 |
| Novelty | 3.5/5 | 3.75/5 | +0.25 |
| Positioning | 3/5 | 4/5 | +1.0 |
| Findings significance | 4/5 | 4/5 | -- |
| Impact potential | 3.5/5 | 3.5/5 | -- |
| Scope honesty | 3.5/5 | 4/5 | +0.5 |

**Overall: 3.75/5 (up from 3.5/5)**

---

## Updated Recommendation

The revision addresses the most important weaknesses from Round 1. The positioning against prior work is now clear (benchmark comparison table, probe taxonomy table, explicit CHOCOLATE/CHAOS differentiation). The calibration literature connection is made. The A-R-I metaphor is honestly framed. The resistance probes are now clearly theory-grounded.

Two issues remain partially unresolved: the inductance analysis still lacks depth on what visual features enable inference, and cross-judge validation is still absent. The first is an opportunity for a stronger paper; the second is a methodological gap that the authors honestly acknowledge.

The paper's core contribution -- the perception-behaviour disconnect, operationalised through admittance-inductance selective blur -- remains clear, novel, and actionable. The "confident fabricator" finding (GPT-5.2 at MQM 91.6 / 98% fabrication) is memorable and deployment-relevant. The revision has tightened the argument and addressed the positioning gaps that were the primary concern in Round 1.

**Updated verdict: Accept.** The remaining issues (inductance depth, cross-judge validation) are improvement opportunities, not blockers. The paper makes a clear contribution that existing chart benchmarks do not provide, and the findings are surprising enough to merit publication at ACL.

---

## Summary of Resolutions

| Issue | Status |
|-------|--------|
| 1. Distinction from CHOCOLATE/ChartHal/CHAOS | RESOLVED |
| 2. Expand inductance analysis | PARTIALLY RESOLVED |
| 3. Connect to calibration literature | RESOLVED |
| 4. Compress basic transform results | PARTIALLY RESOLVED |
| 5. Add cross-judge validation | REMAINING |
| 6. A-R-I branding too forced | RESOLVED |
| 7. Resistance not differentiated from prior work | RESOLVED |

**Resolved: 4/7. Partially resolved: 2/7. Remaining: 1/7.**
