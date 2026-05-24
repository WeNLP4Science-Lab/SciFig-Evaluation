# ACL Reviewer 2 -- Novelty & Contribution
## Wave 1 Combined Review: Related Work, Dataset, Framework

---

## Section 1: Related Work

### Excitement: 3/5

The related work is competent and well-organized into three clean subsections. It correctly identifies the gap (quality-only evaluation vs. behavioral reliability) and positions the paper against the right baselines (FigureQA, PlotQA, ChartQA, POPE, HallusionBench). The cognitive science grounding (Loftus, Tversky & Kahneman, Grice, sycophancy) is the most interesting move here -- it elevates the work beyond "we made harder questions" into principled probe design.

### Novelty Assessment

- **Genuinely new:** The explicit mapping of VLM failure modes onto named cognitive biases (presupposition embedding, anchoring bias, conversational implicature). This is not just labeling -- it generates specific, testable probe designs. I have not seen this systematization in prior chart-understanding work.
- **Incremental:** The claim that scientific figures differ from natural images. This is true but well-established; ChartBench, SciGraphQA, and others have already made this argument.
- **Done before:** The observation that existing hallucination benchmarks focus on natural images. POPE, HallusionBench, and CHAIR are correctly cited, but the "they do objects, we do charts" distinction is a narrow reframing rather than a deep methodological break.

### "So What?" Test

- *"None assess behavioral reliability"* -- This is the core claim, and it lands. If the experiments show quality and reliability rankings truly diverge, this is a real contribution. The related work correctly sets up this expectation. **Verdict: community should care, pending experimental validation.**
- *"Maps VLM failure modes to known cognitive biases"* -- This is appealing but the related work undersells it. The cognitive science references appear in a single dense sentence. If this mapping is a real contribution, it deserves slightly more space explaining *why* the mapping matters (does it predict new failure modes? does it suggest interventions?).

### Positioning Gaps

- **ChartBench (Xu et al., 2024)** is cited but not adequately distinguished from. ChartBench also tests VLMs on diverse chart types with adversarial elements. What specifically can SciFig-Eval reveal that ChartBench cannot? The current text just groups it with earlier benchmarks.
- **SciGraphQA (Li et al., 2023)** is also on scientific graphs from arXiv. The distinction seems to be QA vs. description + behavioral probes, but this should be stated more sharply.
- The final paragraph claims "first framework that unifies description quality measurement with behavioral reliability assessment on scientific figures." This is a strong claim. Has no one done quality + adversarial on charts? Even if not on scientific figures specifically, the claim feels slightly oversold without a more careful sweep. I would accept it if the authors add "on scientific figures" (which they do) and acknowledge that the combination is the contribution rather than either component alone.

### Strengths

- Clean three-part structure (benchmarks, hallucination, methodology) that builds logically toward the gap.
- The MQM adaptation is well-motivated -- borrowing from MT evaluation is a smart move and properly cited.
- Binding verification as an extension to MQM is mentioned early enough to plant the seed.

### Weaknesses

- The cognitive science paragraph (lines 23) is too dense. Four citations and four named biases in one sentence. This is the most novel aspect of the positioning and it is rushed.
- No mention of concurrent/recent work on VLM reliability beyond hallucination (e.g., calibration, refusal behavior, sycophancy benchmarks in text-only LLMs that have been extended to multimodal settings). The sycophancy citation (Sharma et al., 2024) is there but the connection to the broader "LLM alignment" literature is missing.

---

## Section 2: Dataset

### Excitement: 2/5

This is a short, functional dataset section. It does what it needs to do -- describes 250 figures, three chart types, evaluation subsets, adversarial stimuli -- but nothing here excites me. The dataset itself is modest in scale (250 figures) and chart-type coverage (three types). The adversarial stimuli are interesting but they are described so briefly here that I cannot assess their quality.

### Novelty Assessment

- **Genuinely new:** The adversarial stimulus design (four categories targeting distinct behavioral dimensions). This is the novel contribution, but it is barely described here -- the reader is sent to the framework section and appendix.
- **Incremental:** Stratified sampling with a fixed seed. Standard practice.
- **Done before:** Scientific figures from arXiv. SciGraphQA has ~300K figure-text pairs from arXiv. At 250 figures, SciFig-Eval is orders of magnitude smaller. The authors need to justify why 250 is sufficient (and they partly do via the evaluation subsets and per-figure annotation depth, but this should be more explicit).

### "So What?" Test

- *250 figures, 3 chart types* -- Why should I trust findings from 100 primary figures? This is a real concern. The authors mention stratified sampling and ablation subsets, which helps. But for a benchmark paper, 250 is thin. **The "so what" for the dataset is not the size but the annotation depth and adversarial design** -- the authors should lead with that framing.
- *"Selective blur candidates were identified through multi-model consensus and confirmed via human review on a purpose-built dashboard"* -- This is actually interesting methodology for constructing adversarial stimuli, but it is buried in a subordinate clause. It suggests a principled selection process that goes beyond random degradation.

### Positioning Gaps

- No comparison to dataset sizes of prior benchmarks in this section (ChartQA: 4.8K, PlotQA: 28.9M, SciGraphQA: 295K). The reader will wonder about scale. This comparison is apparently in the appendix, but some acknowledgment belongs here.
- The 99/99/52 split across chart types is not justified. Why these proportions? Are they reflective of arXiv figure distributions?

### Strengths

- The four-category adversarial stimulus design (resistance, caption bias, admittance blur, inductance blur) is well-aligned with the A-R-I framework. Tight experimental design.
- Table 1 is clean and informative.
- Reproducibility signals: fixed seed, explicit subset sizes.

### Weaknesses

- **Too brief.** At what looks like ~0.4 pages, this section underdescribes the most important aspects. How were figures selected from arXiv? What domains/fields? How were expert annotations created and validated? Inter-annotator agreement? These details matter for a benchmark paper.
- **Scale concern is unaddressed.** 250 figures will trigger every reviewer's "is this enough?" instinct. Pre-empt it.
- **No examples.** A figure showing sample charts from each type with their annotations would help. (This may be Figure 2 per the style guide, but it is not referenced here.)

---

## Section 3: Framework

### Excitement: 4/5

This is where the paper earns its contribution. The 2x2 evaluation matrix (description/reasoning x standard/adversarial) is clean and genuinely useful as an organizing principle. The A-R-I framework (Admittance-Resistance-Inductance) is the real intellectual contribution, and it is well-articulated here. The distinction between admittance and inductance -- between acknowledging what you cannot see and reasoning about what you can infer -- is novel and empirically grounded.

### Novelty Assessment

- **Genuinely new:**
  - The A-R-I decomposition. I have not seen behavioral reliability decomposed into these three orthogonal dimensions in prior VLM evaluation work. The closest is POPE's polling-based approach, but POPE only measures one dimension (object hallucination) without the admittance/inductance distinction.
  - The inductance dimension specifically. Measuring whether a model's fabrication is "correct reasoning" vs. "lucky guess" by comparing performance on inferable vs. non-inferable blurred elements (21--81% vs. 0--14%) is a clever validation. This is the kind of finding that makes me trust the framework captures something real.
  - Caption bias probe design with the 70/30 rule, anchoring sweet spot, and randomized A/B judging. This is thoughtful adversarial design, not just "add noise."
  - Binding verification in MQM -- checking relationships between elements, not just presence. This is a meaningful extension.

- **Incremental:**
  - MQM adaptation from MT evaluation. Useful but the core idea is borrowed.
  - LLM-as-judge with checklists. Follows established paradigm (Zheng et al., 2023).

- **Done before:**
  - Resistance probes individually resemble existing adversarial QA (leading questions, false premises). The contribution is the systematization via cognitive science, not the individual probe types.

### "So What?" Test

- *"Rankings under standard conditions diverge substantially from rankings under adversarial conditions"* -- This is THE claim. If true, it means every chart-understanding leaderboard is incomplete. **The community should care because this challenges the validity of quality-only evaluation.** The teaser statistic (best MQM model admits limitations 6% of the time vs. second-ranked at 90%) is striking and I want to see the full results.
- *"A model can excel at admittance while failing at inductance"* -- This implies that behavioral dimensions are independently measurable and not just noise. If the A-R-I dimensions are truly orthogonal, this framework could be adopted by other benchmarks beyond chart understanding. **High potential impact.**
- *Binding verification achieving Spearman rho = 1.0 with human rankings* -- Strong validation claim. Almost too perfect -- I would want to see the n for this correlation and understand whether it is ranking 8 models (in which case rho = 1.0 on 8 points is less impressive but still good) or something more granular.

### Positioning Gaps

- The 2x2 matrix (Table 2) is clean but the paper should acknowledge that the "standard vs. adversarial" axis is a continuum, not a binary. Modified captions with 70% true content are "adversarial" but also somewhat realistic (real captions contain errors).
- The connection between the probe design principles and their empirical effectiveness could be stronger. Do presupposition-embedded probes (Inexist) actually fool models more than simpler phrasings? This is an empirical question the framework section should flag for the experiments.

### Strengths

- **A-R-I is a genuine conceptual contribution.** It provides vocabulary and measurement for behavioral dimensions that existing benchmarks conflate or ignore. I would tell a colleague: "There is a paper that decomposes VLM reliability into admittance, resistance, and inductance, and shows they are independent of quality. Worth reading."
- **The probe design is principled, not ad hoc.** Each probe type maps to a named cognitive bias with a citation. This is what elevates the paper above "we wrote tricky questions."
- **The inductance validation (21--81% vs. 0--14%) is compelling.** It provides an internal consistency check that the framework measures real reasoning.
- **The MQM scoring formula is transparent and reproducible.** Severity weights, penalty normalization, binding verification, deduplication -- this reads like production-grade evaluation infrastructure.
- **The caption bias A/B randomization for judging eliminates a known confound.** Small methodological detail but shows care.

### Weaknesses

- **rho = 1.0 needs qualification.** How many models? How many figures in the human evaluation? Perfect correlation on 8 data points is suggestive but not definitive. This should be discussed with appropriate caveats.
- **"Eight models" appears in the related work (line 33) but the framework section and style guide list 8 models.** Consistency check: are there 8 or 11 models? The project overview mentions 11 models but the paper seems to evaluate 8. Clarify.
- **The A-R-I framework is introduced at the end of the section (3.5).** Consider whether it should come first as the organizing principle, with subsections explaining each dimension. Currently the reader encounters MQM, caption bias, and resistance probes before understanding the overarching theory. This is a structural choice, not a fatal flaw, but reorganizing could strengthen the narrative.
- **No explicit discussion of A-R-I limitations.** Are there behavioral dimensions not captured? What about temporal consistency (does a model give the same answer twice)? Or calibration (does the model's expressed confidence match its accuracy)?

---

## Overall Assessment

### Combined Excitement: 3.5/5 (rounds to 4 -- I would attend the talk)

The framework section carries this paper. The A-R-I decomposition is a genuine contribution that could influence how the community evaluates VLM reliability beyond scientific figures. The related work does its job but does not fully exploit the novelty of the cognitive science grounding. The dataset section is underdeveloped and will draw reviewer fire on scale.

### The "Best Paper" Test

- **A finding that surprises experts?** The quality-reliability divergence (MQM-best model admits 6% vs. second-best at 90%) is surprising if it holds up in the full results. Pending.
- **A framework that others will adopt?** The A-R-I framework has adoption potential. It provides clear, measurable dimensions with intuitive names. Yes, conditionally.
- **A methodological innovation?** Binding verification in MQM and the inductance validation methodology (inferable vs. non-inferable comparison) are solid innovations. Modest but real.

**Verdict: This paper has a real contribution in the A-R-I framework and the quality-reliability orthogonality finding. It is not "just another benchmark." But the dataset section and scale concerns need to be addressed proactively, and the related work should amplify the cognitive science contribution rather than compress it.**

### Priority Revisions

1. **Dataset section:** Add one paragraph justifying the 250-figure scale (annotation depth, per-figure adversarial stimuli count, total evaluation instances). Cite the comparison to prior benchmark sizes.
2. **Related work:** Expand the cognitive science paragraph. Give each bias its own sentence with a one-line explanation of why it maps to a specific VLM failure mode.
3. **Framework structure:** Consider moving A-R-I (Section 3.5) to the beginning of Section 3 as the organizing principle, then describing each component under its A-R-I dimension.
4. **rho = 1.0 claim:** Add sample size and caveats.
5. **Model count consistency:** Clarify whether 8 or 11 models are evaluated and why.
