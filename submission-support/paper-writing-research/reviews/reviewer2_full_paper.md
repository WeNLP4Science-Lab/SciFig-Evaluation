# ACL Reviewer 2 -- Novelty & Contribution Review

**Paper:** SciFig-Eval: Evaluating Scientific Figure Understanding across Perception, Reasoning, and Behaviour
**Reviewer Role:** Novelty & Contribution (Reviewer 2)
**Overall Excitement:** 3.5 / 5

---

## Section-by-Section Review

### Introduction
**Excitement: 4/5**

The hook is effective. The GPT-5.2 bar chart example -- where a model confidently names "Customer Support" as a category that appears nowhere in the figure -- is the kind of concrete, memorable failure that justifies an entire paper. The framing around "perception-behaviour disconnect" is clear and sets up a genuine tension: two models can score near-identically on quality but diverge wildly on epistemic honesty.

The A-R-I framework is introduced cleanly. The electrical engineering metaphor (admittance, resistance, inductance) is slightly forced -- these terms carry specific mathematical meanings in circuit theory that do not map neatly onto the cognitive constructs described -- but the underlying decomposition is intuitive and well-motivated.

**Novelty Assessment:**
- *Genuinely new:* The perception-behaviour disconnect as a first-class evaluation axis. The specific finding that MQM-best models are also the worst fabricators is novel and surprising.
- *Incremental:* MQM adaptation for figure descriptions is an application of existing methodology.
- *Done before:* Hallucination probing (POPE, HallusionBench, CHOCOLATE), robustness testing (CHAOS, CHART NOISe). The paper must work harder to distinguish the behavioural dimension from these.

**"So What?" Test:**
The central claim -- that quality scores mask dangerous behavioural differences -- passes the "so what?" test convincingly. If you are selecting a VLM for a scientific pipeline, this paper tells you something ChartQA cannot: which model will lie to you versus which will say "I don't know."

### Related Work
**Excitement: 3/5**

Competent but not distinctive. The three subsections (benchmarks, hallucination, evaluation methodology) cover the right territory. The positioning against ChartQA, CharXiv, SciFIBench, ChartMuseum, etc. is adequate. The connection to sycophancy literature (Sharma et al., Zhao et al.) is appropriate for the resistance dimension.

**Positioning Gaps:**
1. The paper mentions CHOCOLATE and ChartHal as chart hallucination benchmarks but does not explain precisely what A-R-I measures that these do not. Both already identify fabricated chart elements and factual errors. The distinction seems to be the *controlled blur methodology* and the *admittance/inductance split*, but this is not stated explicitly enough.
2. CHAOS and CHART NOISe test perturbation robustness on charts. The paper's visual transforms (noise, rotation, low contrast) overlap substantially with CHAOS. The paper should state why its transform results add anything beyond what CHAOS already reports.
3. The BeHonest and KnowLimits citations are appropriate, but the paper does not discuss whether those benchmarks already measure something equivalent to "admittance" in a text-only setting and whether the findings transfer.

### Dataset
**Excitement: 3/5**

250 figures is small by benchmark standards. The paper acknowledges this and argues for depth over breadth, which is a defensible choice, but it limits the generalizability claims. The stratified sampling and seed reporting are good practices.

The adversarial stimuli construction is the most interesting part of the dataset section. The distinction between admittance blur (unrecoverable) and inductance blur (inferable) is the key methodological contribution and deserves more space. How exactly were "unrecoverable" vs. "inferable" elements determined? The paper says "multi-model consensus and confirmed via human review on a purpose-built dashboard" but this is thin. What was the inter-annotator agreement on recoverability? What percentage of initial candidates were rejected?

**"So What?" Test:**
The dataset itself is not the contribution -- it is the vehicle for the A-R-I framework. This is fine, but it means the paper's value depends entirely on whether the behavioural findings are surprising and actionable. If you removed the A-R-I probes, this would be a small-scale ChartQA variant with MQM scoring.

### Framework
**Excitement: 3.5/5**

The three-axis decomposition (perception, reasoning, behaviour) is clean. The five probe families are well-motivated. The A-R-I framework is the paper's core intellectual contribution, and it is presented clearly.

**Novelty Assessment:**
- *Admittance* (epistemic honesty under uncertainty): This is the most novel dimension. The selective blur methodology -- distinguishing "you cannot possibly know this" from "you could infer this from context" -- is a genuine contribution. I have not seen this exact experimental design in prior VLM evaluation work.
- *Resistance* (robustness to false premises): Less novel. POPE tests object hallucination under leading questions. SycEval tests sycophancy. The specific application to chart false premises (inexist, contra, unanswerable) is useful but incremental.
- *Inductance* (bounded inference from partial evidence): Conceptually interesting but less developed. The paper shows models can sometimes infer blurred labels from context, but does not deeply analyze *how* they do it or what visual features enable inference.

**Positioning Gaps:**
The paper does not discuss how A-R-I relates to the broader "calibration" literature in NLP (e.g., Desai & Durrett 2020, Kadavath et al. 2022). Admittance is essentially visual calibration -- does the model know what it doesn't know? This connection would strengthen positioning considerably.

### Results
**Excitement: 4/5**

This is the strongest section. Several findings are genuinely surprising:

1. **GPT-5.2 as "confident fabricator"**: MQM 91.6, admittance 6%. This is a striking, quotable result. An expert would not have confidently predicted that the best-describing model would also be the worst at admitting uncertainty. This passes the "so what?" test emphatically.

2. **Presupposition embedding as strongest deception vector**: Inexist probes are harder to resist than explicit contradictions. The eyewitness testimony analogy (Loftus 1975) is apt and adds theoretical grounding.

3. **Caption dependency is non-monotonic across Qwen scales**: This is a smaller but interesting finding. It suggests caption dependence is a training artifact, not a capability correlate.

4. **Passive vs. active admittance gap**: GPT-5.2 mentions blur 26% of the time in descriptions but only 6% under direct questioning. This "must-answer bias" finding connects well to RLHF literature.

**What does NOT surprise me:**
- Rotation is the most damaging transform. This is expected -- chart text becomes unreadable.
- Noise has negligible impact. Expected for models trained on web-scale data.
- In-paper-blur causes catastrophic drops. Obvious -- the figure content is destroyed.
- Larger models generally score higher on capability questions. Expected.

**"So What?" Test:**
The key actionable finding: if you are deploying a VLM for scientific figure understanding, do not trust quality benchmarks alone. Specifically, GPT-5.2 will give you the best descriptions but will confidently fabricate when it cannot see. Gemini will give you slightly worse descriptions but will tell you when it cannot see. This is deployment-relevant.

The inductance validation is important: it shows that A-R-I is not just measuring refusal tendency but genuinely separating fabrication from inference. GPT-5.2's 74% inductance correctness vs. 14% admittance correctness confirms the model can reason from context when context exists.

### Analysis
**Excitement: 3.5/5**

The analysis section is well-organized around four key findings. The perception-behaviour disconnect analysis is convincing, especially with the split-half reliability ($\rho = 0.979$) confirming stability.

The presupposition embedding analysis is the most intellectually interesting paragraph. The connection to cognitive psychology (Loftus leading questions) elevates the finding from "some probes are harder" to "there is a systematic vulnerability to embedded assumptions." This is the kind of finding that changes how people design adversarial probes.

The caption dependency analysis raises an important question about training artifacts but does not fully resolve it. The claim that "caption dependency appears tied to how strongly instruction tuning conditions a model to trust provided context over visual evidence" is plausible but speculative without access to training data or ablations on the instruction tuning stage.

**Weaknesses:**
- The "must answer" bias discussion is brief. The 26% passive vs. 6% active gap for GPT-5.2 deserves more analysis. What kinds of elements trigger passive acknowledgment? Is there a severity threshold?
- The cross-dimension correlation table is mentioned but not shown in the main text (Table referenced as \ref{tab:cross-dim}). If this is in the appendix, the key numbers should be in the main text.

### Conclusion
**Excitement: 3/5**

Standard conclusion. The generalizability claim ("any domain where models must acknowledge uncertainty, refuse misleading premises, or infer from partial evidence can apply the same decomposition") is appropriately hedged but also somewhat generic. Future work directions (tables, multi-panel figures, other languages) are obvious.

### Tables
**Table 3 (MQM):** Well-structured. The condition columns tell a clear story: models that are close at baseline diverge under adversarial conditions. The in-paper-blur column is dramatic -- Gemini at 8.4, GPT-5.2 at 13.3. But this seems like a different phenomenon (page-level confusion) than the nuanced behavioural findings the paper emphasizes.

**Table 4 (Behavioral):** This is the paper's most important table. The GPT-5.2 row -- high capability, high resistance, 6% active admittance -- tells the "confident fabricator" story at a glance. The Gemini row -- dominant across all behavioural dimensions -- is equally clear. The table design is effective.

---

## Overall Novelty Assessment

### What is genuinely new?
1. The admittance-inductance distinction via selective blur: testing whether models acknowledge unrecoverable information versus correctly infer recoverable information. This is a methodological contribution that others could adopt.
2. The "confident fabricator" finding: the best-describing model (GPT-5.2) is also the most prolific fabricator under uncertainty. This is surprising and actionable.
3. The passive-active admittance gap, connecting to RLHF "must answer" pressure.

### What is incremental?
1. MQM-adapted scoring for scientific figures -- useful engineering but not novel methodology.
2. Resistance probes -- variations on hallucination probing that exist in POPE, CHOCOLATE, etc.
3. Visual transform robustness -- covered by CHAOS and CHART NOISe.

### What has been done before?
- Chart QA benchmarks: ChartQA, CharXiv, SciFIBench, ChartMuseum
- Chart hallucination: CHOCOLATE, ChartHal
- Chart robustness: CHAOS, CHART NOISe
- VLM sycophancy: Zhao et al. 2024, Fanous et al. 2025
- Abstention/honesty: BeHonest, KnowLimits, SimpleQA

---

## "Best Paper" Test

**A finding that surprises experts?** Yes -- partially. The GPT-5.2 confident fabricator result is surprising in its magnitude (94% fabrication rate). The presupposition embedding vulnerability is also non-obvious. But neither is completely unexpected to someone following the hallucination literature closely.

**A framework that others will adopt?** Possibly. The A-R-I decomposition is clean and the selective blur methodology is reproducible. But adoption depends on whether the community finds the electrical engineering terminology natural. The underlying idea -- test what models do when they can't see, when they're lied to, and when they can infer -- is simple enough to be adopted even if the A-R-I branding doesn't stick.

**A methodological innovation?** The admittance/inductance split via controlled selective blur is a genuine methodological contribution. Distinguishing "the model fabricated because it couldn't possibly know" from "the model inferred correctly from context" is a better way to measure honesty than binary hallucination detection.

**Verdict:** This paper does NOT meet the "best paper" bar, but it is above the acceptance threshold. It has one genuinely novel contribution (the admittance-inductance methodology) and one surprising finding (the perception-behaviour disconnect). The rest is solid but incremental.

---

## Strengths

1. **Clear, memorable central finding.** "The best describer is also the worst fabricator" is a one-sentence contribution that sticks. This is rare for benchmark papers.
2. **The admittance-inductance split is methodologically sound.** Distinguishing unrecoverable from inferable blur is a real contribution to evaluation design.
3. **Good experimental controls.** Probe designer ablation, split-half reliability, scale validation, confidence intervals throughout. The paper takes methodological rigor seriously.
4. **Actionable for deployment.** A practitioner reading this paper knows to test admittance before deploying a VLM in a scientific pipeline. That is concrete value.
5. **Well-written.** The hook example is effective, the framework is clearly presented, the tables are well-designed.

## Weaknesses

1. **Small dataset.** 250 figures, with admittance/inductance tested on only 50/48. The paper argues depth over breadth, but this limits confidence in generalizability. The bar/line/pie restriction (no scatter plots, heatmaps, diagrams, tables) is acknowledged but still a significant scope limitation.
2. **The A-R-I branding is somewhat forced.** The electrical engineering metaphor does not deepen understanding -- it is a naming convention, not a theoretical framework with predictive power. "Honesty, robustness, and inference" would communicate the same content without the metaphorical baggage.
3. **Resistance is not sufficiently differentiated from prior work.** The inexist/contra/unanswerable probes are useful but not clearly distinguished from what POPE, CHOCOLATE, or ChartHal already do. The paper needs a sharper "what we reveal that they cannot" argument here.
4. **Inductance is underdeveloped.** The paper shows that models sometimes infer correctly from context, but does not analyze what visual features enable inference or build a predictive model of when inference succeeds vs. fails. This dimension of A-R-I feels preliminary.
5. **Single judge (GPT-4o).** Although human validation shows perfect rank agreement, the paper relies on a single automated judge. Cross-judge validation is mentioned as future work but should be present.
6. **Missing calibration literature.** The admittance dimension is closely related to calibration (does the model know what it knows?). The paper does not cite or discuss Kadavath et al. (2022), Desai & Durrett (2020), or other calibration work. This is a positioning gap.
7. **The transform robustness results add limited value.** Rotation hurts, noise doesn't, in-paper-blur is catastrophic -- none of these are surprising. This portion of the paper could be compressed to make room for deeper analysis of the novel behavioural findings.

---

## Recommendations

1. **Strengthen the distinction from CHOCOLATE/ChartHal/CHAOS.** A direct comparison table showing what each benchmark measures and what gaps SciFig-Eval fills would be valuable.
2. **Expand the inductance analysis.** What makes an element inferable vs. unrecoverable? Can you predict inferability from visual features? This would elevate inductance from a measurement to a finding.
3. **Connect to calibration literature.** Admittance is visual calibration -- make this connection explicit.
4. **Consider dropping or compressing the basic transform results** (noise, rotation, low contrast). These are the least novel part of the paper and consume space that could go to the behavioural findings.
5. **Add cross-judge validation.** Even a small-scale comparison with Claude or Gemini as judge would address the single-judge concern.

---

## Overall Recommendation

**Score: 3.5/5 -- Between "Solid but incremental" and "Novel and interesting"**

This paper has a clear contribution (the perception-behaviour disconnect, operationalized through admittance-inductance selective blur probes) and a memorable finding (GPT-5.2 as confident fabricator). It is above the bar for ACL publication. However, parts of the evaluation (transform robustness, basic resistance probes) retread ground covered by existing benchmarks, and the inductance dimension needs deeper analysis to fully deliver on its promise. The paper would benefit from sharper positioning against CHOCOLATE/CHAOS and connection to the calibration literature.

I would vote **weak accept** at ACL, contingent on the authors strengthening the positioning against prior chart hallucination/robustness work and expanding the inductance analysis.
