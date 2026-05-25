# ACL Reviewer 3 -- Clarity & Presentation: Full Paper Review

**Paper:** SciFig-Eval: A Multi-Dimensional Benchmark for Evaluating Scientific Figure Understanding in Vision-Language Models

**Overall Clarity Score: 4/5** -- Well-written paper with a clear narrative arc. The reader never gets truly lost. Several structural and terminological issues prevent a 5.

---

## Section-by-Section Review

### Abstract
**Clarity: 4/5**

The abstract does its job: it states the problem (perception vs. behaviour gap), names the benchmark, names the framework, and delivers the headline finding (GPT-5.2 vs. Gemini divergence). At 170 words it is appropriately dense.

**Issues:**
- "collapsing them into a single accuracy score" -- slightly straw-man; prior benchmarks do report per-task breakdowns. Consider "rather than treating correctness under clean conditions as sufficient."
- The A-R-I framework names are introduced without even one-word glosses. A reader seeing "Admittance--Resistance--Inductance" for the first time has no intuition until the next sentence partially explains. Consider embedding the glosses inline: "Admittance (acknowledging uncertainty), Resistance (rejecting misleading context), and Inductance (inferring from partial evidence)."

### Introduction (Section 1)
**Clarity: 4/5**

Strong opening hook with the bar chart example. The contribution list is well-structured. The transition from the anecdote to the A-R-I framework is smooth.

**Flow Issues:**
- The sentence beginning "This failure illustrates one part of a broader behavioural dimension..." is 53 words and tries to do too much: (1) name the dimension, (2) distinguish it from perception/reasoning, (3) reference the framework, (4) define all three axes. Consider splitting.
- The paragraph about deployed vision systems (Beede et al., NHTSA) at the end of the second paragraph feels detached. The link between medical imaging failures and scientific figure fabrication is implied but not stated. One clause would bridge this.

**Redundancy:**
- "250 scientific figures" and "more than 23,000 evaluation instances" appear in both the abstract and the introduction. This is standard for conference papers, so not a problem.
- Contribution 3 largely repeats the second paragraph of the introduction, especially the A-R-I definition. Consider making contribution 3 shorter by referring back.

**Terminology Issues:**
- "Admittance--Resistance--Inductance": The electrical-engineering metaphor is never motivated. Why these names? The paper uses them as if they are self-evident. A brief parenthetical ("borrowing the terminology from...") or a sentence justifying the analogy would help. Currently, a reader unfamiliar with circuit theory gains nothing from the names.
- "epistemic honesty" is introduced without definition. It is a philosophy term that not all ACL readers will know.
- "binding verification" appears in contribution 1 implicitly ("MQM-adapted criteria") but is not named until Section 3. Consider a forward pointer or omit from the introduction.

**Line-Level Edits:**
- Line 9: "This failure illustrates one part of a broader behavioural dimension, distinct from perception and reasoning, that existing benchmarks seldom capture." --> "This failure illustrates a behavioural dimension -- distinct from perception and reasoning -- that existing benchmarks seldom measure."
- Line 11: "Across 8 frontier models and more than 23,000 evaluation instances constructed from 250 scientific figures" --> "Across eight frontier models and 23,000+ evaluations on 250 scientific figures" (use words for numbers under 10 per ACL style; reduce word count).

### Related Work (Section 2)
**Clarity: 4/5**

Well-organized into three subsections that position the paper clearly. The final paragraph of each subsection links back to SciFig-Eval, which is good practice.

**Flow Issues:**
- Section 2.1 reads as a list of benchmarks rather than a narrative. Consider grouping by *gap* rather than by *benchmark name*: "Prior benchmarks address chart QA [cite], scientific figure understanding [cite], and multi-chart reasoning [cite], but none evaluate behavioural reliability under degraded or misleading evidence."
- Section 2.3 is titled "Evaluation Methodology" but covers two distinct topics: (1) honesty/abstention/sycophancy and (2) MQM/LLM-as-judge. These deserve separate paragraphs with clearer topic sentences.

**Redundancy:**
- The sentence "These benchmarks show that chart and figure understanding remains difficult even for frontier VLMs" at the end of 2.1 is generic and could be cut.
- The phrase "selectively blurred" or "selective blur" appears in both 2.2 and the introduction. This is fine for clarity.

**Space Optimization:**
- At roughly 0.75 pages, Related Work is within budget. No cuts needed.

### Dataset (Section 3.1)
**Clarity: 4/5**

The dataset section is clear and well-structured. Table 1 is helpful.

**Flow Issues:**
- The section is labeled as a subsection (\subsection{Dataset}) within the "Benchmark and Evaluation Framework" section, but it reads like an independent section. This is fine structurally but creates a mild discontinuity: the reader transitions from the framework overview (Section 3 paragraph 1) to dataset details, then back to evaluation methodology.
- "The depth of evaluation per figure is what distinguishes SciFig-Eval from prior benchmarks" -- this is a claim that belongs in the introduction or related work positioning, not in the dataset description. It breaks the descriptive register.

**Terminology Issues:**
- "stratified random sampling (seed=42)" -- nice for reproducibility but the parenthetical seed is a detail better suited for the appendix or a footnote.
- "probe-designer independence studies" -- this phrase appears before the ablation is described. A reader encountering it here has no idea what it means. Add a brief clause: "...for probe-designer independence studies, which test whether behavioural scores depend on which model generated the probes (\S5.5)."

**Table 1 Critique:**
- Clean and readable. Minor: "Admittance blur candidates" and "Inductance blur candidates" use "candidates" but the text uses "probes." Terminology should be consistent.

### Framework (Section 3)
**Clarity: 4/5**

The three-dimension decomposition (perception, reasoning, behaviour) is clearly stated. The A-R-I framework is well-motivated.

**Flow Issues:**
- The first paragraph of Section 3 repeats material from the introduction (250 figures, 187 papers, chart type counts). This is necessary for a reader who skipped the intro, but for a sequential reader it feels redundant. Consider: "The 250-figure corpus is described in \S\ref{sec:dataset}; here we focus on the evaluation framework."
- The five probe families in Section 3.2 are listed in a single dense paragraph. A short itemized list or small table would improve scanability. Currently the reader must parse: visual transforms (5 types), caption-bias probes, resistance probes, admittance blur, inductance blur -- all in one paragraph.
- Sections 3.1 and 3.2 share labels: `\label{sec:caption-bias}` and `\label{sec:resistance}` are both assigned to Section 3.2. This is a LaTeX issue -- two labels on one subsection means one of them will point to the wrong place.

**Terminology Issues:**
- "binding verification" (Section 3, Perception paragraph) is used without explanation. What does "binding" mean here? The phrase "value-label-colour correspondences" partially clarifies, but the term itself is jargon. Consider: "Binding verification checks that the model associates each value with the correct label and colour, rather than swapping correspondences across elements."
- "rule engine" -- what rule engine? This sounds like a software component. Briefly explain or remove.

**Space Optimization:**
- The A-R-I framework subsection (3.3) is well-proportioned. No cuts needed.
- The last paragraph ("These dimensions are intentionally independent...") is excellent framing and worth keeping.

### Results (Section 4)
**Clarity: 4/5**

Results are clearly organized by dimension (perception, reasoning, behaviour) and the writing is crisp. The "confident fabricator" profile is memorable and effective.

**Flow Issues:**
- The section opens with the central finding before presenting the models or methodology. This is effective for a reader who wants the punchline, but it creates a forward reference to Table 4 before the models are even listed. Consider moving the opening sentence to after the Models subsection.
- Section 4.3 (Reasoning) is a single paragraph, conspicuously short. It references Table 4 but provides almost no analysis. Either expand with one key finding per capability type, or merge into Section 4.4.
- The ablation (Section 4.5) is important but feels bolted on. It tests probe-designer independence but could also address judge-independence. If GPT-4o is both the judge and one of the probe designers, circularity is a concern worth raising.

**Redundancy:**
- "94% of the time" (GPT-5.2 fabrication rate) appears in the abstract, introduction, and results. This is the headline number, so repetition is defensible, but consider varying the phrasing.
- The in-paper-blur result ("all models fall below 31 MQM points") is interesting but feels like it belongs in analysis rather than perception results, since it involves a context condition, not a perceptual transform.

**Table 3 (Description Quality) Critique:**
- Effective design: conditions as columns, models as rows, bold/underline for ranks. The caption is self-contained and informative.
- Issue: "Orig" column header is ambiguous. From the caption: "Base = baseline with caption" and "Orig" presumably means original without caption. But the label "Orig" does not communicate this. Suggest "NoCap" or "Orig (no cap)".
- The `\mdot{clrX}` colored bullets are a nice touch for linking to figures, but their purpose is not explained anywhere in the paper. A footnote in the first table using them would help.
- Column "InPap" appears under "Context" but Table 3 caption says "Context embeds the figure in its PDF page." The values shown are for the *non-blurred* in-paper condition, correct? The in-paper-blur condition described in Section 4.2 ("all models fall below 31 MQM points") is not in this table. This is potentially confusing. Clarify in the caption whether InPap is the clean or blurred page-context condition.

**Table 4 (Behavioral) Critique:**
- This is the most information-dense table in the paper. 13 columns is a lot. The grouping with cmidrules helps, but a reader must consult the caption repeatedly.
- The mix of scales is a problem: Capability in %, Resistance in 0-1, Admittance in %, Inductance in %. Converting Resistance to percentage or vice versa would reduce cognitive load.
- "Inex", "Cont", "Unan" abbreviations are defined in the caption but not intuitive. Consider "NonEx", "Contra", "UnAns" or simply spelling them out since the table is already full-width.
- The Inductance columns show "percentage of fabricated answers that were correct." This denominator shifts by model (models that admit more have fewer fabricated answers to score). The caption should note this.

**Figure Critiques:**

*Figure 1 (Hook):*
- Effective. The side-by-side original/blurred comparison is immediately clear. Caption is self-contained.
- Minor: The caption refers to "GPT-5.2" without the model dot color, while Tables 3-4 use colored dots. Consistency would help.

*Figure 2/3 (Results Overview, combined):*
- Using a combined figure* with two subfigures is a good use of space.
- The degradation panel (2a) has too many grey lines that are hard to distinguish. Consider labeling the top and bottom models on the plot directly.
- The A-R-I panel (2b/3) uses three sub-panels (admittance, resistance, inductance) with different marker shapes. This works but the shapes ($\triangledown$, $\diamond$, $\triangle$) are defined only in the caption. Consider a legend within the figure.

*Figure 4 (Blur Triptych):*
- Excellent pedagogical figure. Showing four conditions on the same chart makes the evaluation design concrete. The tikz grid background is a nice touch (lab-notebook feel) but adds visual noise. Consider removing it.
- The caption mentions "three false claims (red)" for the caption bias panel. Can the reader actually see red text at this figure size? If not, the claim is unverifiable.

*Figure 5 (Scatter):*
- Clean and effective. The dashed identity line clearly shows where quality would predict behaviour. The GPT-5.2 outlier position is immediately visible.
- The two panels (admittance vs. quality, resistance vs. quality) share an x-axis but use different y-axis scales. This is correct but could be clearer with explicit axis labels visible in the figure.

### Analysis (Section 5)
**Clarity: 4.5/5**

The strongest section of the paper in terms of insight density. Each paragraph makes a distinct analytical point, and the Loftus citation connecting presupposition embedding to eyewitness testimony is the kind of cross-disciplinary connection that elevates a paper.

**Flow Issues:**
- The section reads as four independent analytical paragraphs rather than a narrative. Each paragraph starts with a bold topic label, which helps scanability but reduces flow. Consider adding a one-sentence preamble: "Four findings emerge from the results that have implications beyond this benchmark."
- The "Methodological robustness" paragraph at the end is defensive rather than analytical. It belongs in the results or as a subsection thereof, not in the analysis.

**Redundancy:**
- "GPT-5.2 ranks first on MQM (91.6) but fourth on active admittance (6%); Gemini ranks second on MQM (90.2) but first on admittance (90%)" -- this specific comparison appears for the third time (abstract, results, analysis). By this point, the reader knows. Consider referring to Figure 5 instead of restating the numbers.

**Line-Level Edits:**
- "A benchmark reporting only MQM would rank the two models as near-equivalent while missing opposite behaviours under uncertainty." -- Strong sentence. Keep.
- "a lie is harder to resist when embedded as a presupposition than when stated directly." -- Punchy. Keep.
- "caption dependency appears tied to how strongly instruction tuning conditions a model to trust provided context over visual evidence" -- This is a hypothesis presented as a finding. Add "we hypothesize that" or "one possible explanation is that."

### Conclusion (Section 6)
**Clarity: 4/5**

Concise and forward-looking. The final paragraph ("Selecting VLMs for scientific workflows on quality benchmarks alone risks embedding a confident fabricator into the research pipeline") is the best sentence in the paper.

**Flow Issues:**
- The first sentence ("Perception and reasoning scores mask a third dimension...") overlaps heavily with the abstract opening. For a conclusion, this is acceptable.
- "Several directions extend this work" is generic. The three directions listed (broader coverage, training interventions, domain transfer) are reasonable but could be more specific.

**Limitations:**
- Well-written and appropriately self-critical. The acknowledgment of small sample sizes for admittance/inductance (50/48 figures) is honest.
- The limitation about GPT-4o as judge is important. The paper claims "human validation of MQM rankings yielded perfect agreement (rho = 1.0)" -- a perfect correlation with only 8 data points (one per model) is not statistically compelling. Consider noting the sample size.

**Ethics Statement:**
- Adequate but brief. No concerns.

---

## Cross-Cutting Issues

### Terminology Consistency

| Term in one place | Term in another place | Issue |
|---|---|---|
| "admittance blur" | "selective-blur admittance probes" | Inconsistent phrase ordering |
| "blur candidates" (Table 1) | "blur probes" (text) | candidate vs. probe |
| "inexist probes" | "non-existent chart elements" | abbreviation vs. full form |
| "contra probes" | "contradictory numerical premises" | same |
| "CapB" (Table 4) | "Cap. Bias R" (text) | different abbreviations |
| "open-ended description" | "passive admittance" | same task, different names |
| "targeted question" | "active admittance" | same task, different names |
| "in-paper" | "page-context" | same condition, two names |

Recommendation: Create a terminology table (in appendix or as a footnote) mapping abbreviations to full names. In the main text, settle on one name per concept.

### The A-R-I Naming Problem

The electrical-engineering analogy (Admittance, Resistance, Inductance) is the paper's most distinctive contribution but also its biggest communication risk. In electrical engineering:
- Admittance = ease of current flow (inverse of impedance)
- Resistance = opposition to current flow
- Inductance = property of storing energy in a magnetic field

The paper's usage inverts the valence of "admittance" (high admittance is *good* in the paper, but in circuits it means *less* opposition). "Resistance" maps reasonably. "Inductance" maps loosely at best.

The metaphor adds memorability but introduces confusion for readers who know the electrical meanings. At minimum, acknowledge the analogy is loose. Better: add a one-sentence motivation ("We borrow the circuit terminology to evoke a system's response to signals under varying impedance conditions; the analogy is suggestive rather than formal.").

### Space Budget Assessment

| Section | Estimated pages | Budget | Verdict |
|---|---|---|---|
| Abstract | 0.3 | -- | Fine |
| Introduction | 1.0 | ~1.25 | Slightly under; could add motivation for A-R-I names |
| Related Work | 0.75 | ~0.5-0.75 | At upper bound; could trim 2.1 survey |
| Framework + Dataset | 1.75 | ~2.0 | Slightly under; room for the probe list improvement |
| Results | 2.0 | ~2.0-2.5 | Fine; reasoning subsection is thin |
| Analysis | 0.75 | ~0.5-1.0 | Fine |
| Conclusion + Limitations + Ethics | 0.75 | ~0.5 | Slightly over; limitations could be tighter |

Total estimated: ~7.3 pages (before figures/tables). Within the 8-page limit.

### What Should Move to Appendix
- The seed=42 detail
- The in-paper-blur MQM numbers (interesting but tangential to the main argument)
- The specific CI ranges throughout the results (keep the point estimates, move CIs to appendix tables)

### What Is Missing from the Main Paper
- A single orientation table or figure showing the full evaluation pipeline at a glance (input figure --> conditions --> tasks --> scoring dimensions). The reader must reconstruct this mentally.
- Inter-annotator agreement details beyond the 94% number -- what was the disagreement resolution process?
- Any qualitative examples of model outputs beyond the hook figure. One short example box showing a "confident fabricator" response vs. an honest one would be powerful.

---

## Summary of Recommendations (Prioritized)

1. **Terminology table or footnote** mapping abbreviations to full names and resolving inconsistencies (high impact, low effort).
2. **Motivate the A-R-I naming** with one sentence explaining why these electrical terms were chosen (high impact, low effort).
3. **Expand Section 4.3 (Reasoning)** or merge it into Section 4.4. A single-paragraph results subsection looks incomplete (medium impact, low effort).
4. **Unify the scale in Table 4** -- either all percentages or all 0-1 (medium impact, low effort).
5. **Add an evaluation pipeline overview figure** showing the flow from figures to conditions to scores (high impact, medium effort).
6. **Convert the probe list in Section 3.2 to a short itemized list** for scanability (medium impact, low effort).
7. **Clarify the "Orig" column header in Table 3** (low impact, trivial effort).
8. **Add "we hypothesize" to the caption-dependency-as-training-artifact claim** in the analysis (low impact, trivial effort).
9. **Note the small sample size** (n=8 models) when reporting rho=1.0 for human-judge agreement in Limitations (medium impact, trivial effort).
10. **Remove the tikz grid background** from Figure 4 to reduce visual noise (low impact, trivial effort).

---

## Overall Assessment

This is a well-structured benchmark paper that tells a clear story: perception quality alone does not predict behavioural reliability. The A-R-I framework is the paper's most original contribution and is clearly operationalized. The writing is generally strong, with several memorable formulations ("confident fabricator," the Loftus analogy). The main clarity weaknesses are terminology inconsistency, the unmotivated electrical-engineering metaphor, and a few structural choices (thin reasoning section, mixed scales in Table 4) that could be fixed in a revision pass. The paper is well within page limits and the figures are effective, particularly Figure 1 (hook) and Figure 4 (blur triptych). With the ten fixes listed above, this paper would reach a 4.5/5 on clarity.
