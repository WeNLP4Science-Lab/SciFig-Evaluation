# ACL Paper Research: What Makes Top Papers Successful

Research compiled May 2026 for SciFig-Evaluation benchmark paper submission.

---

## 1. ACL 2026 Submission Requirements

**Conference:** 64th ACL, San Diego, California, July 2-7, 2026

### Deadlines
- ARR submission: January 5, 2026
- Commitment to ACL 2026: March 14, 2026
- Acceptance notification: April 4, 2026
- Camera-ready: April 19, 2026

### Page Limits
- **Long papers:** 8 pages of content + unlimited references + mandatory Limitations section (not counted)
- **Short papers:** 4 pages of content + unlimited references + mandatory Limitations section
- Accepted papers get +1 page for revisions (9 / 5 total)
- Supplementary materials allowed but optional

### Formatting
- Follow ARR templates (LaTeX/Word available from ARR submission portal)
- Two-way anonymized review (double-blind)
- No anonymity period requirement
- Papers with hallucinated references will be desk-rejected
- Missing Limitations section = desk rejection
- Style guide/length violations = desk rejection

### Relevant Topic Areas for SciFig
- **Resources and Evaluation** (primary)
- **Multimodality and Language Grounding to Vision, Robotics and Beyond** (primary)
- **Interpretability and Analysis of Models for NLP**
- **Multilinguality and Language Diversity**
- **AI/LLM Agents** (if framing VLMs as agents)

### Special Theme: Explainability of NLP Models
Focus on making internal decision-making processes transparent. Relevant angles for SciFig:
- Using evaluation to detect biased predictions
- Understanding VLM failure modes as a form of explainability
- Identifying internal mechanisms controlling model behaviors

---

## 2. ARR Review Criteria: Exactly What Reviewers Score

### Three Primary Scores (all 1-5 scale with half-points)

#### Soundness (1-5)
| Score | Meaning |
|-------|---------|
| 5 | Most thorough study possible for this type of paper |
| 4 | Sufficient support; extra experiments not essential |
| 3 | Main claims supported; minor gaps in details |
| 2 | Major claims unsupported; major technical problems |
| 1 | Not sufficiently thorough to warrant publication |

**What this measures:** Technical correctness, sound argumentation, appropriate claim scoping, sufficient evidence, reproducibility.

**Actionable for SciFig:** Every claim about VLM performance must be backed by statistical evidence. If you say "GPT-4o hallucinates more than Gemini," show the numbers, confidence intervals, and methodology. Reviewers must justify low soundness scores with specific faults, so making your methodology airtight removes their ability to score low.

#### Excitement (1-5)
| Score | Meaning |
|-------|---------|
| 5 | Would recommend to others and attend presentation |
| 4 | Would mention to colleagues; attend if possible |
| 3 | Might mention some points; attend if time permits |
| 2 | Doesn't resonate personally but might with community |
| 1 | Won't resonate with *ACL community |

**Actionable for SciFig:** Frame findings as surprising and actionable. Don't just report scores -- highlight unexpected failures, counterintuitive results, and implications for the field. The "counting gap" and "caption bias" findings are excitement drivers.

#### Overall Assessment (1-5)
| Score | Meaning |
|-------|---------|
| 5 | Consider for Award (top 2.5%) |
| 4 | Conference acceptance worthy |
| 3 | Findings acceptance worthy |
| 2 | Needs substantial revisions |
| 1 | Do not resubmit |

### Additional Scored Dimensions
- **Reproducibility (1-5):** From easily reproducible to impossible. Release code and data.
- **Datasets (1-5):** Value if released. Score separately from main paper.
- **Software (1-5):** Value if released.
- **Reviewer Confidence (1-5):** How well the reviewer knows the area.
- **Limitations and Societal Impact:** Adequacy of discussion.

### Key Rule
"The soundness scores must be justified by the text of the review. If you give a low Soundness score without finding any major faults, this means that your review is not a faithful explanation of your recommendation."

This means: if your paper has no identifiable faults, reviewers cannot give low soundness scores without violating guidelines. Make the paper fault-proof.

---

## 3. Common Rejection Reasons (ARR Codes)

### Methodology Problems (M1-M5) -- Most Common
- **M1: LLM evaluation without validation.** If using LLM-as-judge, you MUST validate against human judgments. Show inter-annotator agreement, correlation with human scores.
- **M2: Reproducibility gaps.** Missing hyperparameters, unclear code availability, undisclosed prompts. Publish everything.
- **M3: Undisclosed data quality problems.** Acknowledge and characterize noise in your data.
- **M4: Unmotivated model/benchmark selection.** Explain WHY you chose these 11 models and 4 judges. Don't just list them.
- **M5: Incomplete proofs or unstated assumptions.** State all assumptions about your evaluation framework.

### Results Problems (R1-R5)
- **R1: Unfair baselines, misleading statistics.** Use proper statistical tests, not just raw numbers.
- **R2: Overclaiming beyond evaluation scope.** If you tested on scientific figures, don't claim your findings generalize to all VLM tasks.
- **R3: Speculation presented as fact.** Mark hypotheses clearly.
- **R4: Overclaiming (e.g., "LLMs understand language").** Avoid language like "VLMs cannot understand charts" -- say "VLMs score X on chart understanding tasks."
- **R5: Missing statistical significance.** Include confidence intervals, significance tests, or effect sizes.

### General Problems (G1-G5)
- **G1: Unclear research question.** State RQs explicitly, ideally numbered.
- **G2: Reliance on unsound precedent.** Don't build on flawed prior benchmarks without acknowledging their limitations.
- **G3: Misrepresented related work.** Be thorough and fair in positioning.
- **G4: Undefined key terms.** Define "hallucination," "faithfulness," "grounding" as you use them.
- **G5: Misleading citations.** Cite primary sources accurately.

### Reviewer Anti-Patterns (What Reviewers Should NOT Do -- But Often Do)
These are documented biases you can preemptively address:

| Bias | What happens | How to preempt |
|------|-------------|----------------|
| SOTA fixation | "Doesn't beat SOTA" | Emphasize your contribution is the benchmark/analysis, not a new method |
| Surprise as criticism | "Results seem obvious" | Frame findings against prior assumptions; cite what people expected |
| Methodology prejudice | "Too simple" | Argue that simplicity is a feature for reproducibility |
| Unfounded demands | "Should test on X too" | Acknowledge scope limitations upfront in Limitations section |
| Language/niche bias | Penalizing non-English or narrow work | Frame multilingual coverage as a strength |

---

## 4. ACL 2024 Best Paper Winners: Patterns and Lessons

### Best Papers (7 winners)
1. **Mission: Impossible Language Models** -- Tested whether LLMs learn impossible languages equally well as natural ones. Won for rigorous experimental design testing a prominent theoretical claim.
2. **Semisupervised Neural Proto-Language Reconstruction** -- Historical linguistics + neural methods.
3. **Why are Sensitive Functions Hard for Transformers?** -- Theoretical analysis of transformer limitations.
4. **Natural Language Satisfiability** -- Problem formalization + transformer evaluation.
5. **Deciphering Oracle Bone Language with Diffusion Models** -- Novel application domain.
6. **Causal Estimation of Memorisation Profiles** -- Methodological contribution.
7. **Aya Model** -- Large-scale multilingual resource (open-access, 101 languages).

### Best Resource Papers (3 winners)
1. **Latxa** -- Open language model + evaluation suite for Basque.
2. **Dolma** -- 3 trillion token open corpus with full documentation of curation practices.
3. **AppWorld** -- 750-task benchmark for coding agents with 457 APIs.

### Best Social Impact Papers (3 winners)
1. **Persuading LLMs to Jailbreak** -- Safety evaluation.
2. **DIALECTBENCH** -- NLP benchmark for dialects and language varieties.
3. **Cultural Bias in LLMs** -- Bias measurement benchmark.

### Patterns Across Winners

**What best papers have in common:**
1. **They challenge a prevailing assumption.** Mission: Impossible challenged Chomsky's claim. Dolma challenged the closed-data norm. Frame SciFig as challenging the assumption that VLMs are good at scientific figure understanding.
2. **They release everything.** Every resource winner released data, code, and models. No exceptions.
3. **They have massive scale OR surgical precision.** Either test at scale (Dolma: 3T tokens, Aya: 101 languages) or do a precise, elegant experiment (Mission: Impossible).
4. **They serve an underserved community.** Latxa (Basque), DIALECTBENCH (dialects), Aya (101 languages). SciFig's multilingual angle (4 languages) fits this pattern.
5. **They document methodology obsessively.** Dolma dedicated pages to documenting curation decisions. AppWorld has 60K lines of code + 40K lines of benchmark.

---

## 5. ACL 2025 Best Paper Winners: Updated Patterns

### Best Papers (4 winners)
1. **A Theory of Response Sampling in LLMs** -- Theoretical + practical.
2. **Fairness through Difference Awareness** -- Measurement methodology for LLM bias.
3. **Language Models Resist Alignment** -- Data compression perspective on alignment.
4. **Native Sparse Attention** -- Hardware-aligned efficiency innovation.

### Best Resource Papers (3 winners)
1. **UniMoral** -- Multilingual moral reasoning pipeline.
2. **BRIGHTER** -- Emotion recognition dataset for 28 languages.
3. **Palm** -- Culturally inclusive Arabic dataset.

### Best Theme Papers (3 winners -- theme was "Generalization")
1. **MaCP** -- Adaptation via hierarchical cosine projection.
2. **Meta-rater** -- Data selection for pre-training.
3. **SubLIME** -- Data-efficient LLM evaluation via subset selection.

### Updated Patterns (2024+2025 combined)
- **Multilingual/multicultural is a consistent winner category.** 5 of 6 resource winners across both years are multilingual. SciFig covers 4 languages -- lean into this heavily.
- **Measurement methodology papers win.** Fairness through Difference Awareness (2025) and DIALECTBENCH (2024) are both "here's how to measure X properly" papers. Frame SciFig as "here's how to properly measure VLM scientific figure understanding."
- **Resource papers that change research practice win.** Dolma enabled open pre-training research. AppWorld enabled agent benchmarking. Position SciFig as enabling proper VLM evaluation for scientific figures.

---

## 6. Specific Advice for Benchmark/Evaluation Papers

### What Makes a Benchmark Paper Stand Out (Synthesized from Winners)

#### Structure That Works
1. **Motivation section (1-1.5 pages):** Why existing benchmarks fail. Be specific -- name benchmarks and their limitations. Don't just say "existing benchmarks are insufficient." Say "ChartQA tests only English bar charts; FigureQA lacks expert-level analysis tasks; neither tests multilingual capabilities."
2. **Benchmark design (2 pages):** Taxonomy of tasks, data collection methodology, quality control, statistics. Include a figure showing the benchmark design overview.
3. **Experimental setup (1 page):** Models tested, evaluation metrics, prompting strategies.
4. **Results and analysis (2-3 pages):** Not just tables. Per-category breakdowns, error analysis, surprising findings, qualitative examples.
5. **Limitations (0.5 page):** Honest, specific, not generic.

#### The "So What" Test
Every benchmark paper must answer: "Why should the community use this benchmark instead of what already exists?" Specific answers:
- "Because existing benchmarks don't test X" (coverage gap)
- "Because existing benchmarks inflate scores via Y" (measurement flaw)
- "Because this benchmark reveals Z failure mode" (diagnostic value)

For SciFig, the answers should be:
- Coverage: multilingual, diverse figure types, expert-level analysis
- Measurement: MQM framework vs simple accuracy, 4 independent judges
- Diagnostic: reveals specific failure modes (counting, hallucination, axis reading)

#### What AppWorld Did Right (Best Resource Paper 2024)
1. **Two-component design:** Environment (60K LoC) + Benchmark (40K LoC). Separating the tool from the tasks.
2. **Difficulty calibration:** "Normal" and "challenge" tiers. Showed GPT-4o gets 49% normal, 30% challenge.
3. **Performance spread:** Multiple models tested, clear differentiation. Not just "everything fails."
4. **Collateral damage detection:** Measured unintended side effects, not just task completion.

#### What Dolma Did Right (Best Resource Paper 2024)
1. **Full transparency:** Every curation decision documented.
2. **Toolkit release:** Not just data, but the tools to create similar data.
3. **Empirical findings about curation:** The paper contributed knowledge about data curation, not just the data itself.

### Common Reasons Benchmark Papers Get Rejected
1. **"Just another benchmark" syndrome.** No clear differentiation from existing work. Fix: dedicate a full comparison table showing what you cover that others don't.
2. **Insufficient analysis.** Tables of numbers without insight. Fix: for every result table, add 1-2 paragraphs of analysis explaining WHY, not just WHAT.
3. **No baselines or unfair baselines.** Fix: test multiple model families, sizes, and prompting strategies.
4. **Unclear evaluation methodology.** Fix: describe your scoring rubric in enough detail that someone could replicate it without your code.
5. **Data quality concerns.** Fix: report inter-annotator agreement, quality control procedures, data statistics.
6. **Limited scope presented as comprehensive.** Fix: be honest about scope in the title and throughout. "SciFig: Evaluating VLMs on Scientific Figure Understanding" not "The Definitive VLM Benchmark."

---

## 7. Paper Structure Template for SciFig

Based on analysis of winning benchmark papers, here is a recommended structure:

### Abstract (150-250 words)
Formula: [Problem] + [Gap in existing work] + [What we built] + [Scale: N figures, M models, K languages] + [Key finding that surprises] + [Release statement]

Example flow: "Vision-language models are increasingly used for scientific figure analysis, yet no comprehensive benchmark exists for evaluating this capability across languages and figure types. We present SciFig, a benchmark of 1,005 scientific figures spanning 4 languages, evaluated across 11 VLMs using 4 independent judges with the MQM error typology framework. Our evaluation reveals that [most surprising finding]. We release our benchmark, evaluation framework, and all annotations at [URL]."

### Introduction (1.5 pages)
- Paragraph 1: VLMs are being used for science. Stakes are high (wrong figure interpretation = wrong conclusions).
- Paragraph 2: Existing benchmarks are insufficient (name 3-4 and their specific limitations).
- Paragraph 3: Our contributions (numbered list, 3-4 items).
- Paragraph 4: Key findings preview (the hook -- what surprising thing did you find?).
- Figure 1: Overview figure showing benchmark design and a sample evaluation.

### Related Work (1 page)
Three subsections:
1. VLM benchmarks (ChartQA, FigureQA, etc.) -- what they lack
2. Scientific document understanding -- broader context
3. Evaluation methodology for VLMs -- MQM and alternatives

### Benchmark Design (2 pages)
- 2.1 Figure taxonomy and collection
- 2.2 Task design and annotation
- 2.3 Quality control and inter-annotator agreement
- 2.4 Multilingual considerations
- Table 1: Benchmark statistics (figures by type, language, difficulty)
- Figure 2: Example figures from each category with annotations

### Experimental Setup (1 page)
- 3.1 Models evaluated (justify each choice)
- 3.2 Evaluation framework (MQM details)
- 3.3 Judge models and human validation
- 3.4 Prompting strategy

### Results (2 pages)
- 4.1 Overall performance (Table 2: main results)
- 4.2 Performance by figure type
- 4.3 Cross-lingual analysis
- 4.4 Error analysis and failure modes
- 4.5 Judge agreement and reliability
- Figure 3-4: Visualizations of key findings

### Analysis and Discussion (1 page)
- 5.1 Why do VLMs fail at [specific task]?
- 5.2 The caption bias problem
- 5.3 Implications for scientific practice
- 5.4 Adversarial robustness (if including blur experiments)

### Limitations (0.5 page)
Be specific and honest:
- Languages covered (4 of ~7,000)
- Figure types not included
- Annotation biases
- Model snapshot problem (evaluations are time-bound)

### Conclusion (0.25 page)
Restate key finding + call to action for the community.

---

## 8. Writing Quality Checklist

### What Gets Papers from 3 to 4 (Findings to Conference)
- [ ] Every claim has a citation or experimental evidence
- [ ] All tables have analysis paragraphs, not just numbers
- [ ] Related work is fair and comprehensive (no strawmanning)
- [ ] Figures are informative and self-contained (readable without text)
- [ ] The paper has a clear "story" -- reads as narrative, not report
- [ ] Research questions are stated explicitly (RQ1, RQ2, RQ3)
- [ ] Limitations section is substantive, not perfunctory

### What Gets Papers from 4 to 5 (Conference to Award)
- [ ] Challenges a prevailing assumption with rigorous evidence
- [ ] Findings change how the community thinks about the problem
- [ ] Methodology is novel enough to be reused by others
- [ ] Scale or precision is exceptional
- [ ] Writing is crisp -- no filler, every sentence earns its place
- [ ] The paper serves an underserved community or fills a clear gap

### Specific Pitfalls for VLM Evaluation Papers
- [ ] Don't use only LLM-as-judge without human validation (M1 violation)
- [ ] Report prompts used for evaluation in appendix (M2 violation if missing)
- [ ] Don't claim "VLMs can't do X" when you tested 3 prompting strategies (R2 overclaiming)
- [ ] Include error bars or confidence intervals on all metrics (R5 violation if missing)
- [ ] Define your evaluation metrics precisely (G4 violation if terms undefined)
- [ ] Explain why you chose MQM over other frameworks (M4 violation if unmotivated)

---

## 9. Positioning SciFig for Maximum Impact

### Framing Options (Pick 1-2)

**Option A: "The Multilingual Gap"**
"VLM benchmarks are English-only. Scientific figures are published in many languages. We reveal a X% performance drop in non-English scientific figure understanding." This plays to ACL's consistent reward of multilingual work.

**Option B: "Evaluation Methodology"**
"Current VLM benchmarks use accuracy on simple questions. We introduce MQM-based evaluation that captures error types, severity, and hallucination patterns." This positions as a methodology contribution.

**Option C: "Diagnostic Benchmark"**
"We don't just score VLMs -- we diagnose their failures. Our analysis reveals specific, actionable failure modes: counting errors, axis misreading, hallucinated data points." This plays to the excitement score.

**Option D: "Scale and Rigor"**
"1,005 figures x 11 models x 4 judges = the most comprehensive evaluation of VLM scientific figure understanding to date." This plays to soundness.

**Recommended: Combine B + C.** Lead with methodology innovation (MQM for VLMs), deliver with diagnostic findings. Multilingual is a supporting strength, not the headline (unless the cross-lingual gap is your most dramatic finding).

### Title Suggestions
- "SciFig: A Multilingual Benchmark for Evaluating Vision-Language Models on Scientific Figure Understanding"
- "How Well Do VLMs Read Scientific Figures? A Diagnostic Evaluation Across 11 Models and 4 Languages"
- "Beyond Accuracy: MQM-Based Evaluation of Vision-Language Models on Scientific Figures"

### Key Numbers to Highlight
Pick the 3 most surprising statistics from your results and put them in the abstract. Examples:
- "The best VLM achieves only X% on counting tasks in scientific figures"
- "VLMs hallucinate data points in Y% of chart descriptions"
- "Performance drops Z% on non-English figures"
- "Models score W% higher when captions are visible, revealing caption bias rather than figure understanding"

---

## 10. Desk Rejection Checklist (Prevent Before Submission)

Papers are desk-rejected for:
- [ ] Exceeding page limits (8 pages for long, 4 for short)
- [ ] Missing Limitations section
- [ ] Anonymity violations (author names, self-identifying language, non-anonymized links)
- [ ] Hallucinated references (cite real papers only; ACL 2026 explicitly flags this)
- [ ] Style guide violations (wrong template, margins, font)
- [ ] Missing responsible NLP checklist responses
- [ ] Scope misalignment with CFP topics

---

## Sources

- ACL 2026 CFP: https://2026.aclweb.org/calls/main_conference_papers/
- ACL 2025 CFP: https://2025.aclweb.org/calls/main_conference_papers/
- ACL 2025 Awards: https://2025.aclweb.org/program/awards/
- ACL 2024 Awards: https://2024.aclweb.org/program/best_papers/
- ARR Review Form: https://aclrollingreview.org/reviewform
- ARR Reviewer Guidelines: https://aclrollingreview.org/reviewerguidelines
- ARR CFP: https://aclrollingreview.org/cfp
- ACL Anthology: https://aclanthology.org
