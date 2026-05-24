# ACL Reviewer 3 -- Clarity & Presentation
## Wave 1 Combined Review: Related Work, Dataset, Framework

---

## 1. Related Work (`related_work.tex`)

### Clarity Score: 4/5

Well-structured and purposeful. Each subsection positions the paper against a specific literature strand and ends by naming the gap SciFig-Eval fills. The reader always knows *why* they are reading each paragraph. Minor issues keep it from a 5.

### Flow Issues

- The transition from Section 2.1 to 2.2 is abrupt. The last sentence of 2.1 introduces "behavioral reliability" -- the concept lands well -- but 2.2 opens with hallucination as if starting fresh. A single bridging clause ("While chart understanding benchmarks ignore behavioral reliability entirely, the hallucination literature addresses it -- but only for natural images.") would tighten the thread.
- The final paragraph (lines 35-36) reads like a mini-conclusion restating the contribution. This is appropriate for related work, but the phrase "the first framework that unifies..." is a strong claim that belongs in the introduction, not buried here. Consider softening to "the first benchmark designed to measure both..." or moving the claim.

### Redundancy

- The gap statement appears twice in nearly identical form: line 9 ("None assess behavioral reliability...") and line 36 ("Existing benchmarks measure quality *or* detect hallucinations; we measure both"). The second instance adds the divergence finding, so it earns its place, but the first could be tightened to avoid the echo.

### Terminology Issues

- Line 16: "polling-based binary classification task" -- jargon-heavy for a positioning paragraph. Consider "binary probing task" or simply "binary classification probes."
- Line 23: The sentence listing four cognitive science principles is long (47 words from "Our work draws..." to the end). It reads as a list dump. Consider restructuring: name the category ("probes grounded in four cognitive biases") and cite parenthetically rather than inline.
- Style guide says "resistance probes" not "hallucination tests" -- line 22 uses "hallucination benchmarks" which is fine since it refers to *other* work, not ours. Consistent.

### Table/Figure Critique

No tables or figures in this section. Appropriate for related work.

### Space Optimization

- At roughly 0.75 pages, this section is right on target per the style guide. No cuts needed.
- The sentence on line 6 directing the reader to Appendix for a benchmark comparison table is good practice -- keeps the main text lean.

### Line-Level Edits

**Line 6** (long sentence):
> "A comprehensive comparison of these and additional benchmarks appears in Appendix~\ref{sec:benchmark-comparison}."

This is fine but could be folded into the previous sentence:
> "...diverse chart types \citep{xu2024chartbench}; a comprehensive comparison appears in Appendix~\ref{sec:benchmark-comparison}."

**Lines 8-10** (gap statement):
> "These benchmarks share a common limitation: they evaluate VLMs exclusively through question answering on clean images, measuring whether a model produces a correct answer."

"Common limitation" is slightly hedging. Consider: "These benchmarks share a structural blind spot: they evaluate..." -- stronger and more specific.

**Line 17** (hallucination modes):
> "...expert-crafted visual illusions and language traps to diagnose entangled hallucination modes"

"Entangled hallucination modes" is opaque. What are the modes? If space allows, name them briefly; if not, drop "entangled" which adds nothing for the reader.

**Line 23** (long list sentence):
Current: "Our work draws on cognitive science to design probes grounded in presupposition embedding~\citep{...}, anchoring bias~\citep{...}, the cooperative principle~\citep{...}, and sycophantic agreement~\citep{...}---mapping VLM failure modes to known cognitive biases rather than treating hallucination as a monolithic category."

Suggested rewrite:
> "Rather than treating hallucination as a monolithic category, we ground our probes in four cognitive biases---presupposition embedding~\citep{...}, anchoring~\citep{...}, the cooperative principle~\citep{...}, and sycophantic agreement~\citep{...}---mapping each to a distinct VLM failure mode."

Leads with the "why," reduces clause nesting.

---

## 2. Dataset (`dataset.tex`)

### Clarity Score: 3/5

The section is dense and efficient -- perhaps too efficient. It reads like a specification rather than a narrative. A reader unfamiliar with the framework will struggle to understand what "admittance blur" and "inductance blur" mean at this point in the paper, since the A-R-I framework has not been introduced yet. The section's placement *before* the framework section creates a forward-reference problem.

### Flow Issues

- **Critical ordering problem.** The dataset section uses terminology from the A-R-I framework (admittance blur, inductance blur, resistance probes, caption bias probes) before that framework is defined. A reader encounters "admittance blur (50 figures with unrecoverable elements selectively blurred)" on line 11 without knowing what admittance means in this context. Two fixes: (a) move Dataset to *after* Framework, or (b) add a single forward-reference sentence ("These categories correspond to the three dimensions of the A-R-I behavioral framework introduced in \S\ref{sec:framework}").
- The section is a single subsection (`\subsection{Dataset}`) nested under the Framework section. This is an odd structural choice -- the dataset is typically a peer-level section, not a child of the framework. If this is intentional (framework + dataset = one section), the parent section needs a brief orienting paragraph before the subsection starts.

### Redundancy

- The figure counts appear three times: in the text (line 5: "bar charts (99), line plots (99), and pie charts (52)"), in Table 1 (rows for each type), and in the parenthetical subset ratios (line 8: "40/40/20"). The first two are acceptable (text + table is standard), but the subset ratios in the text AND in the table is redundant. Pick one location.

### Terminology Issues

- "Adversarial stimuli" (line 10) -- the style guide says "transform" not "perturbation" but does not address "stimuli." "Stimuli" has a psychology connotation that may confuse NLP readers. Consider "adversarial probes" or "adversarial conditions" (the latter matches Table 2).
- "seed$=$42" (line 8) -- implementation detail that does not aid comprehension. Move to appendix or footnote. It matters for reproducibility but interrupts the narrative.
- "multi-model consensus" (line 11) -- undefined. How many models? What threshold? Either define briefly or cite the appendix.

### Table/Figure Critique

**Table 1** (Dataset statistics):
- Clean and well-formatted with booktabs. Good use of grouped rows with italic category headers.
- The caption is self-contained -- a reader can understand the table without reading the text. Good.
- Missing: source information. Where do the arXiv papers come from? How many unique papers? This is important for a dataset paper. Consider adding a row or a caption note.
- Minor: "Admittance blur candidates" and "Inductance blur candidates" use the word "candidates" -- are some not used? If all 50 are used, drop "candidates."

### Space Optimization

- At roughly 0.4 pages (including table), this is lean -- possibly too lean for a dataset section. The reader needs to know: (1) how figures were sourced, (2) how annotations were created, (3) inter-annotator agreement or quality control. All three are absent from the main paper. Even one sentence per item would help: "Figures were drawn from arXiv papers published between X and Y across N fields" and "Annotations were created by [who] and verified by [how]."
- The table earns its space. Keep it.

### Line-Level Edits

**Line 5** (opening sentence):
> "\textsc{SciFig-Eval} comprises 250 English-language scientific figures extracted from arXiv papers, spanning bar charts (99), line plots (99), and pie charts (52)."

This is good but "English-language" modifying "figures" is slightly odd -- figures are language-independent; the *papers* are English-language. Consider: "...250 scientific figures extracted from English-language arXiv papers..."

**Line 5** (continued):
> "Each figure is paired with a structured expert annotation describing axes, data series, labels, color mappings, and trends, verified against the original PDF context."

"Verified against the original PDF context" is a dangling modifier -- it could modify "trends" or "annotation." Rewrite: "Each figure is paired with a structured expert annotation -- covering axes, data series, labels, color mappings, and trends -- verified against the source PDF."

**Line 8**:
> "From the 250-figure pool, we construct a primary subset of 100 figures (40 bar, 40 line, 20 pie) via stratified random sampling (seed$=$42), and a nested ablation subset of 50 figures (20/20/10) for probe-designer independence studies (\S\ref{sec:ablation})."

This is one sentence carrying too much information. Split:
> "From the 250-figure pool, we construct a primary evaluation subset of 100 figures (40 bar, 40 line, 20 pie) via stratified sampling. A nested 50-figure subset (20/20/10) supports probe-designer independence studies (\S\ref{sec:ablation})."

**Line 11**:
> "Selective blur candidates were identified through multi-model consensus and confirmed via human review on a purpose-built dashboard."

"Purpose-built dashboard" is an interesting methodological detail that deserves either a brief explanation (one clause) or a figure in the appendix. Currently it is a throwaway mention that raises more questions than it answers.

---

## 3. Framework (`framework.tex`)

### Clarity Score: 4/5

This is the strongest section of the three. The 2x2 matrix provides an excellent orienting device, and each subsection follows a clear pattern: what we measure, how we measure it, and what the score means. The A-R-I framework section at the end ties everything together well. Two issues prevent a 5: (a) the MQM subsection is notation-heavy and could be more accessible, and (b) the Inductance paragraph buries a key empirical finding in a definitional section.

### Flow Issues

- The opening paragraph (lines 3-5) and the paragraph after Table 2 (line 22) both explain the 2x2 matrix. The second paragraph adds the empirical motivation ("rankings under standard conditions diverge substantially..."), but it partially re-explains the matrix. Consider merging or making the second paragraph purely about the divergence finding.
- Section 3.4 (A-R-I framework) summarizes components already described in 3.1-3.3. This is intentional -- it unifies them under a theory -- but the Resistance paragraph (line 72) is almost entirely a back-reference with no new information. Tighten to: "Resistance aggregates the hallucination and caption bias probes (\S\ref{sec:resistance}, \S\ref{sec:caption-bias}), capturing whether the model prioritizes visual evidence over false textual context."
- The "Independence of dimensions" paragraph (line 76) introduces a strong empirical claim (the 6% vs 90% admittance divergence). This is compelling but feels premature in the framework section -- it previews results. Consider whether a forward reference ("as we show in \S\ref{sec:experiments}") would be cleaner, or whether this should move to the results/analysis section.

### Redundancy

- The phrase "whether a model fabricates information it cannot see" or close variants appears at least three times across the framework section (lines 22, 55, 70). This is the central concept, so some repetition is expected, but the third occurrence in the Admittance paragraph could be varied: "whether the model invents answers for obscured elements."
- Lines 43-44: "An LLM judge then evaluates each false claim independently through a randomized A/B design: for each modification, the judge receives the claim and the ground-truth reality in randomized order (A or B) and determines which the model's description aligns with, eliminating position bias." The explanation after the colon re-says what "randomized A/B design" means. If readers know what A/B means, the explanation is redundant. If they do not, "A/B design" is the wrong term. Suggest: "An LLM judge evaluates each claim by receiving the false version and ground truth in randomized order and determining which the model's output aligns with, eliminating position bias."

### Terminology Issues

- Line 27: "chart-type-specific variant" -- consider just "chart-type-specific adaptation" for smoother reading.
- Line 29: "An LLM judge (GPT-4o)" -- the style guide says GPT-5.2, and elsewhere the paper seems to use GPT-5.2. Is this an outdated reference? Check consistency.
- Line 37: "binding verification" is introduced with italics in related work (line 29 of related_work.tex) and then defined here. Good.
- Line 68: "A-R-I framework" -- first use in this section should probably use `\emph{}` per style guide conventions for introducing terms. Currently it uses `\emph{A-R-I framework}` which is correct.
- Line 74: "inductance captures real reasoning rather than noise" -- "noise" is vague. Consider "rather than random agreement" or "rather than chance."

### Table/Figure Critique

**Table 2** (Evaluation matrix):
- Effective orienting device. The 2x2 structure is immediately graspable.
- The caption is self-contained. Good.
- Minor: the cell contents use inconsistent phrasing. "Baseline MQM" is a method name; "Caption bias, passive admittance / inductance" is a list of probe types. Consider making both rows parallel: either both name methods or both name what is measured.
- "Capability Qs" -- abbreviation is informal for a table in an ACL paper. Consider "Capability questions" or "Targeted questions."

**Equation 1** (MQM score):
- Clear and well-defined. The inline definition of $w_i$ and $D$ immediately after is good practice.
- However, "severity-adjusted maximum" for $D$ is vague. Is $D$ the sum of maximum possible $w_i$ values? State explicitly.

**Equation 2** (Caption bias resistance):
- Clean and intuitive. The variable names are descriptive.

### Space Optimization

- At roughly 2 pages, this section matches the style guide target. Good.
- The Resistance paragraph in A-R-I (line 72) could be cut to one sentence without information loss, saving 2-3 lines.
- Consider whether the full A/B judging procedure description (lines 43-44) belongs in the main paper or appendix. The core idea ("randomized presentation eliminates position bias") is one clause; the procedural details could move.

### Line-Level Edits

**Line 5** (opening):
> "This yields a $2\!\times\!2$ evaluation matrix (Table~\ref{tab:eval-matrix}) that structures every experiment in the benchmark."

"Structures every experiment" is slightly vague. Consider: "...that organizes every experiment in the benchmark into one of four evaluation modes."

**Line 22**:
> "A key empirical observation motivating this design is that rankings under standard conditions diverge substantially from rankings under adversarial conditions, suggesting that quality and reliability are distinct dimensions of model competence."

This is a 37-word sentence making a critical claim. Break it up and make the claim punchier:
> "A key empirical observation motivates this design: model rankings under standard conditions diverge substantially from those under adversarial conditions. Quality and reliability, it turns out, are distinct dimensions of competence."

**Line 27** (MQM):
> "Each chart type has a dedicated checklist: 14~items for bar charts, 15~for line plots, and 11~for pie charts."

Good -- specific and parallel. No edit needed.

**Line 29**:
> "An LLM judge (GPT-4o) assesses each checklist item on two axes: \emph{coverage} (complete, partial, or missing) and \emph{correctness} (correct, partial, wrong, or n/a), then scans for violations of seven global constraints."

This sentence carries three distinct pieces of information (judge identity, two scoring axes, global constraints). Consider splitting after the parenthetical: "...or n/a). The judge also scans for violations of seven global constraints."

**Line 37**:
> "Automated MQM rankings achieve a Spearman correlation of $\rho = 1.0$ with human expert rankings, confirming that the approach preserves human judgment at scale."

$\rho = 1.0$ is a perfect correlation. This is a strong claim and demands a sample size. How many models? How many annotators? Add: "...across N models ranked by M annotators." Without this, the claim looks too good.

**Line 42** (Caption bias):
> "The \emph{70/30 rule} ensures that roughly 70\% of the modified caption is verifiably correct, establishing trust before introducing poisoned claims."

"Poisoned claims" -- the style guide says "modified caption" not "poisoned." While "poisoned claims" is technically different from "poisoned caption," it carries the same connotation. Consider "false claims" for consistency.

**Line 57** (Inexist probes):
> "The false element is embedded in a subordinate clause, directing attention to an analytical question \emph{about} the element rather than \emph{whether} it exists, exploiting co-occurrence priors for the chart type."

Excellent sentence -- the italicized contrast between "about" and "whether" is effective. No edit needed.

**Line 70** (Admittance):
> "A model can do both simultaneously (e.g., ``the label is obscured but appears to be X''), and this decomposition captures important behavioral nuance."

"Important behavioral nuance" is vague. The example does the work -- consider cutting after the parenthetical: "A model can do both simultaneously (e.g., ``the label is obscured but appears to be X'')."

**Line 76** (Independence):
> "Empirically, the highest-scoring model on MQM admits visual limitations only 6\% of the time, while the second-ranked model admits 90\%"

This is a compelling statistic. But "second-ranked" -- second on MQM? On admittance? Clarify: "...while the model ranked second on MQM admits 90\%..."

---

## Cross-Section Issues

1. **Section ordering.** Dataset currently appears as a subsection under Framework but uses A-R-I terminology not yet introduced. Either (a) promote Dataset to its own section and place it after Framework, or (b) add a forward-reference sentence when A-R-I terms first appear in the dataset section.

2. **Terminology consistency across sections.** "Adversarial stimuli" (dataset) vs. "adversarial conditions" (framework) vs. "behavioral probes" (related work). The style guide says "behavioral evaluation" for the adversarial condition. Standardize.

3. **The LLM judge model name.** The framework section says "GPT-4o" (line 29). The style guide lists "GPT-5.2" as the model name. If the judge was updated, update the section. If GPT-4o is correct for the judge specifically, note the discrepancy explicitly (e.g., "we use GPT-4o as judge, while evaluated models include GPT-5.2").

4. **Missing overview figure.** The style guide reserves Figure 1 for an overview diagram of the 2x2 framework. Table 2 partially fills this role but a visual diagram would significantly improve accessibility. Consider whether Figure 1 has been drafted elsewhere.

---

## Summary Scores

| Section | Clarity Score | Key Issue |
|---|---|---|
| Related Work | 4/5 | Strong positioning; minor flow and sentence-level issues |
| Dataset | 3/5 | Forward-reference problem; reads as spec, not narrative |
| Framework | 4/5 | Excellent structure; MQM density and premature results claims |

**Overall Wave 1 Clarity: 3.7/5**

The framework section is the backbone and it works well. The related work does its job efficiently. The dataset section needs the most attention -- it should either follow the framework or add bridging language, and it needs at least minimal sourcing and annotation quality information to be credible as a dataset description.
