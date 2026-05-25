# ACL Reviewer 3 -- Clarity & Presentation: Round 2 Review

**Paper:** SciFig-Eval: A Multi-Dimensional Benchmark for Evaluating Scientific Figure Understanding in Vision-Language Models

**Previous Overall Clarity Score: 4/5**
**Updated Overall Clarity Score: 4.5/5**

---

## Status of Previous Issues

### 1. Terminology table or footnote mapping abbreviations to full names
**RESOLVED.** Table 3 caption now defines all column abbreviations explicitly (NoCap, Rot, LowC, InPap, CapB, AdmB, IndB). Table 4 caption defines Cnt, Cmp, Cmpr, Pat, Inex, Cont, Unan, Act, Pas, and explicitly notes which columns are percentages versus 0--1 scores. The inline terminology is now more consistent throughout the paper.

### 2. Motivate the A-R-I naming with one sentence
**RESOLVED.** Section 3.3 now contains: "We borrow the terminology from circuit analysis, where admittance governs how freely current passes, resistance opposes it, and inductance generates it from changing fields, as a loose analogy for how models handle, reject, or reconstruct visual information." This is exactly the kind of sentence I requested. The "loose analogy" framing is honest and helpful.

### 3. Expand Section 4.3 (Reasoning) or merge it into Section 4.4
**RESOLVED.** Section 4.3 is now three substantial paragraphs. The per-category breakdown (counting vs. computation vs. comparison vs. pattern) is well-analysed, with specific numbers and comparative insight ("Gemini excels at tasks grounded in direct visual extraction... while GPT-5.2 is strongest when the task demands derived numerical operations"). This is no longer the thinnest section.

### 4. Unify the scale in Table 4
**REMAINING (partial).** The caption now explicitly notes: "Capability, Admittance, and Inductance columns report percentages; Resistance columns report scores on a 0--1 scale." This is a clear improvement -- the reader is warned. However, the mixed scales still require the reader to mentally convert when comparing across dimensions. This is now a minor nuisance rather than a real problem.

### 5. Add an evaluation pipeline overview figure
**REMAINING.** I do not see evidence of a new pipeline overview figure in the sections provided. The paper still relies on the reader to mentally reconstruct the flow from figures to conditions to scores. Given that the textual descriptions are now clearer, this is less critical, but it would still improve first-read comprehension.

### 6. Convert the probe list in Section 3.2 to a short itemized list
**RESOLVED.** Section 3.2 now includes a formatted block quote with concrete probe examples (Inexist, Contra, Unanswerable) that makes the probe types immediately scannable. The surrounding prose is better structured with paragraph headers. This is a significant readability improvement.

### 7. Clarify the "Orig" column header in Table 3
**RESOLVED.** The column is now labeled "NoCap" with a caption definition "NoCap = original image without caption (no-caption baseline)." This is unambiguous.

### 8. Add "we hypothesize" to the caption-dependency claim in analysis
**RESOLVED.** The analysis section now reads "caption dependency appears tied to how strongly instruction tuning conditions a model to trust provided context over visual evidence" -- the hedging language ("appears tied to") is appropriate for a hypothesis. The framing avoids presenting it as an established finding.

### 9. Note the small sample size when reporting human-judge agreement
**RESOLVED.** The Limitations section now reports: "Human validation on 120 annotated pairs yielded Krippendorff's alpha = 0.91 and model-level ranking agreement of rho = 0.80 (n = 4 models)." The Perception paragraph in Section 3.1 also provides details: "Three annotators independently scored 120 (figure, model) pairs across 30 figures and 4 models; inter-annotator reliability was Krippendorff's alpha = 0.91 (interval scale), and model-level ranking agreement with the automated judge was rho = 0.80 (n = 4 models, p < 0.05)." The previous rho = 1.0 claim has been replaced with a more defensible rho = 0.80, properly scoped. This is a major improvement in methodological honesty.

### 10. Remove the tikz grid background from Figure 4
**NOT VERIFIABLE.** I reviewed only .tex source for text sections and tables; the figure files themselves were not provided. Cannot confirm or deny.

---

## Status of Cross-Cutting Issues

### Terminology Consistency
**LARGELY RESOLVED.** The paper now uses consistent terminology:
- "blur candidates" (Table 1) vs. "blur probes" (text): Table 1 still uses "selective blur" phrasing but now matches the text more closely ("Admittance selective blur," "Inductance selective blur").
- "in-paper" vs. "page-context": The paper now consistently uses "in-paper" and "in-paper page context" throughout. The "InPap" abbreviation is defined in both Table 3 and Table 4 contexts.
- "CapB" is now consistently used in both tables and text as "Cap. Bias R" or "CapB" with definition.

One minor inconsistency remains: the abstract says "fabricates answers about unreadable elements in 98% of cases" while the results section says "fabricating answers 98% of the time." These match in content but the framing shifts from "about unreadable elements" to a more general claim. Minor.

### The A-R-I Naming Problem
**RESOLVED.** See issue 2 above. The one-sentence motivation in Section 3.3 addresses the concern directly.

### Space Budget
The paper remains well within the 8-page limit. The reasoning section expansion does not appear to have caused overflow. The introduction is tighter, the framework section is clearer, and the analysis remains dense and insightful.

---

## New Observations (Round 2)

### Improvements Not Previously Requested

1. **Binding verification clarified.** Section 3.1 now explains: "Binding verification checks value-label-colour correspondences so that models are penalised for binding visible elements to the wrong evidence." This was flagged as jargon in round 1 and is now clear.

2. **"Rule engine" explained.** The MQM paragraph now reads: "a rule engine maps judgments to Accuracy, Completeness, and Clarity penalties." This is still somewhat opaque -- what rules? -- but the context (MQM scoring) makes it interpretable. Acceptable.

3. **Section 2.3 structure.** Related Work Section 2.3 now has two clear paragraphs: one on honesty/abstention/sycophancy and one on MQM/LLM-as-judge. This addresses the flow issue I raised.

4. **Probe-designer independence.** The ablation now clearly states "GPT-4o to Mistral Large 3" as the comparison, removing any ambiguity about which models were involved.

### New Issues

1. **Abstract now says 98% fabrication; results say 98%.** Consistent, but the abstract previously said 94%. This is a factual update, not a clarity problem. Fine.

2. **The "confident fabricator" phrase** appears in Section 4.4 but not in the abstract or introduction. Given its memorability and rhetorical power, it might be worth introducing earlier. This is a suggestion, not a problem.

3. **Appendix references are numerous.** The paper now references Appendix sections A through at least G (benchmark-comparison, probe-taxonomy, dataset-details, human-validation, mqm-details, mqm-pipeline, capability-pipeline, transform-pipeline, blur-pipeline, eval-pipelines). This is appropriate for a benchmark paper but a reader may wonder about the sheer volume. A brief note ("The appendix provides full construction details for all pipelines and probes") in the framework section would orient the reader. This is already partially done.

4. **Table 4 has 12 data columns.** Down from the 13 I counted before. The grouping with cmidrules is effective. The Act/Pas split for both Admittance and Inductance is clear. This table is still dense but well-organized.

---

## Updated Scores

| Criterion | Round 1 | Round 2 | Notes |
|---|---|---|---|
| Logical flow | 4 | 4.5 | Reasoning section expansion, better section transitions |
| Contribution statement | 4 | 4 | Unchanged; was already clear |
| Notation and terminology | 3.5 | 4.5 | Major improvement; abbreviations defined, A-R-I motivated |
| Tables and figures | 4 | 4.5 | NoCap fix, caption definitions, consistent formatting |
| Space efficiency | 4 | 4.5 | Reasoning section now earns its space; no bloat |
| Accessibility | 3.5 | 4 | Better for non-experts; binding and A-R-I explained |

**Overall Clarity: 4.5/5** -- The authors addressed 7 of 10 issues fully, 1 partially, 1 not verifiable, and 1 remaining. The remaining pipeline overview figure would push this toward a 5, but the paper is now well above the threshold for clear scientific communication. The terminology is consistent, the A-R-I framework is motivated, the reasoning section is substantive, and the tables are self-contained. This is a well-revised paper.

---

## Summary

The revision directly addresses the majority of my round 1 feedback. The most impactful changes are: (1) the A-R-I circuit analogy motivation sentence, (2) the expanded reasoning results with per-category analysis, (3) the NoCap column rename and comprehensive caption definitions, and (4) the corrected human validation statistics (rho = 0.80, n = 4 from 120 pairs, replacing the previously overstated rho = 1.0). The paper reads as a coherent story from motivation through results to implications. The "confident fabricator" framing remains the paper's most effective rhetorical device. I would accept this paper with minor revisions (the pipeline overview figure and the mixed-scale Table 4 annotation are the only substantive items remaining).
