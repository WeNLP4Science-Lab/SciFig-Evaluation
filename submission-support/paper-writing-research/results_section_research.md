# Results and Analysis Section Research for ACL Benchmark Papers

Deep research on how top ACL/NLP papers write Results and Analysis sections,
specifically for benchmark and evaluation papers.

---

## 1. How ACL 2024-2025 Best Paper Winners Structure Results

### ACL 2024 Best Papers (for reference)
- "Mission: Impossible Language Models" (Kallini et al.)
- "Semisupervised Neural Proto-Language Reconstruction" (Lu et al.)
- "Why are Sensitive Functions Hard for Transformers?" (Hahn & Rofin)
- "Deciphering Oracle Bone Language with Diffusion Models" (Guan et al.)
- "Causal Estimation of Memorisation Profiles" (Lesci et al.)
- "Aya Model" (Ustun et al.) -- 101 languages, multi-model
- "AppWorld" (Trivedi et al.) -- Best Resource Paper, benchmark

### ACL 2025 Best Papers
- "A Theory of Response Sampling in LLMs" (Sivaprasad et al.)
- "Fairness through Difference Awareness" (Wang et al.)
- "Language Models Resist Alignment" (Ji et al.)
- "Native Sparse Attention" (Yuan et al.)

### Structural Patterns Observed

**Number of subsections in Results**: Typically 2-4 subsections under a single
"Experiments" or "Results" heading. The pattern is:

1. Setup subsection (models, metrics, data -- often labeled "Experimental Setup")
2. Main results subsection (the big table, the headline finding)
3. Analysis/ablation subsections (1-2 of these, each focused on one angle)

**Example from HallusionBench (CVPR 2024)**:
- Section 5: Experimental Results
  - 5.1 Models (1 paragraph listing what was evaluated)
  - 5.2 Result Analysis (the bulk -- multiple paragraphs with Tables 2-3, Figures 4-5)

**Example from AppWorld (ACL 2024 Best Resource)**:
- Experiments section benchmarks ReAct and Plan-And-Execute with GPT-4 variants,
  LLaMA3, and DeepSeek-Coder
- Leads with headline finding: best approach (GPT4O + ReAct) achieves only 48.8%
  on normal tasks, 30.2% on challenge tasks
- Then breaks down by difficulty level and approach type

**Example from Mission: Impossible Language Models (ACL 2024 Best Paper)**:
- Evaluations performed "at various stages throughout training"
- Core structure: control comparison (English) vs impossible languages
- Progressive revelation: shows learning curves across training, not just final numbers

### Key Takeaway: The "Lead with Punchline" Pattern

Best papers overwhelmingly **lead with the main finding**, then unpack it.
They do NOT build mystery. As Michael Ernst (UW) advises: "A technical paper is
not a joke or a mystery novel. The reader should not encounter any surprises,
only deeper explanations of ideas that have already been introduced."

**Pattern**: State the main finding in the first paragraph of Results, reference
the main table, then spend remaining subsections explaining why and exploring
edge cases.

---

## 2. Best Practices for Multi-Condition Results (8+ Models x 10+ Conditions)

### The "Wall of Numbers" Problem

When you have many models and many conditions, the worst thing you can do is
present a giant table and say "Table 3 shows the results." The reader drowns.

### Strategies from Top Papers

#### Strategy 1: The Headline Table + Targeted Drill-Downs

Use ONE main results table with aggregated or representative conditions, then
use smaller tables or figures to drill into specific phenomena.

- **Main table**: Models (rows) x 3-4 key aggregate metrics (columns)
- **Drill-down tables**: Specific breakdowns only for the interesting patterns
- **Figures**: Use bar charts or heatmaps for patterns that are visual

**Example (Aya Model, ACL 2024)**: With 101 languages and multiple models, they:
- Aggregated by language family / resource level rather than listing all 101
- Used held-out task evaluation tables with clear category groupings
- Separated discriminative vs generative task results
- Put per-language breakdowns in the appendix

#### Strategy 2: The Tiered Presentation

Present results in 3 tiers:
1. **Tier 1 (main paper, ~1 paragraph)**: The top-line finding in prose
2. **Tier 2 (main paper, 1 table + 1-2 figures)**: Key comparisons
3. **Tier 3 (appendix)**: Full model x condition matrices

#### Strategy 3: Narrative Ordering by Finding, Not by Table

Instead of organizing by "here's Table 1, here's Table 2," organize by finding:

```
Finding 1: Open models lag behind proprietary models by X points on average.
  [Reference Table 2, highlight relevant rows]

Finding 2: But the gap narrows dramatically on [specific condition].
  [Reference same Table 2, different columns, or a targeted Figure]

Finding 3: Surprisingly, [unexpected pattern].
  [Reference Table 3 or a figure specifically designed to show this]
```

#### Strategy 4: Bold/Highlight Key Cells

In large tables, use **bold** for best results, underline for second-best.
Use color or shading in figures to draw the eye. HallusionBench uses this
extensively -- readers can scan the table visually before reading prose.

#### When to Use Prose vs Tables vs Figures

| Content Type | Best Format |
|---|---|
| Exact numbers for 3+ models on 3+ metrics | Table |
| Trends across conditions (monotonic, U-shaped) | Line chart or bar chart |
| Rankings that change across dimensions | Heatmap or radar chart |
| A single key comparison | Prose with inline numbers |
| Distribution or spread of results | Box plot or violin plot |
| Correlation between two metrics | Scatter plot |
| Per-example qualitative analysis | Figure with examples |

---

## 3. Analysis Section Best Practices

### What Distinguishes Good Analysis from Restating Results

**Bad analysis** (just restating):
> "As shown in Table 2, GPT-4V achieves 31.42% accuracy, while LLaVA-1.5
> achieves 11.2%."

**Good analysis** (explaining why):
> "GPT-4V's 20-point advantage over LLaVA-1.5 (31.4% vs 11.2%) likely stems
> from its stronger visual grounding: when we examine the language-only subset
> (Table 3), the gap narrows to just 5 points, suggesting that LLaVA-1.5's
> deficit is primarily perceptual rather than linguistic."

### The Analysis Paragraph Formula

Top papers follow a consistent 4-part paragraph structure:

```
1. CLAIM:    State the finding/pattern (1 sentence)
2. EVIDENCE: Reference specific numbers from table/figure (1-2 sentences)
3. EXPLAIN:  Propose WHY this pattern exists (1-2 sentences)
4. CONNECT:  Link to broader implications or next finding (1 sentence)
```

**Example paragraph (modeled on HallusionBench style)**:

> Models exhibit a strong "yes" bias that inflates their apparent accuracy.
> As shown in Table 3, LLaVA-1.5 answers "yes" to 87% of binary questions,
> compared to GPT-4V's more balanced 54% yes-rate. We attribute this to
> instruction-tuned models being trained to be agreeable and helpful, which
> manifests as affirmative bias when faced with visual uncertainty. This bias
> has direct implications for evaluation design: benchmarks relying on
> yes/no accuracy without controlling for response distribution will
> systematically overestimate model capabilities.

### How to Handle Surprising vs Expected Results

**For expected results**: Acknowledge briefly, then move on. Don't belabor
the obvious.
> "Consistent with prior work (Chen et al., 2023), we find that proprietary
> models outperform open-source alternatives on average."

**For surprising results**: Give them MORE space. Use explicit surprise markers
and then offer explanations.
> "Surprisingly, [Model X] outperforms [Model Y] on [specific condition]
> despite [Model Y]'s generally stronger performance. We hypothesize that
> this reversal stems from [mechanism], supported by the observation that
> [additional evidence]."

HallusionBench does this well: when models perform *worse* than random chance,
they explicitly flag it and attribute it to mechanisms like "scarcity of
human-edited images in their training set."

### How to Explain WHY Patterns Exist

Techniques used in best papers:

1. **Ablation**: Remove a factor and show the effect changes
2. **Subset analysis**: Show the pattern holds/breaks in specific subsets
3. **Correlation**: Show two metrics move together (or don't)
4. **Case studies**: Pick 2-3 examples that illustrate the mechanism
5. **Reference to model architecture/training**: Link to known properties
6. **Contrast with baselines**: Show the pattern doesn't appear in simpler models

### Limitations Within Analysis vs Separate Section

ACL **requires** a separate "Limitations" section after the conclusion (does not
count toward page limit). However, best papers ALSO acknowledge relevant caveats
inline during analysis:

> "While this pattern is consistent across all 4 judges, we note that our
> figure sample skews toward bar and line charts (see Section 2), and the
> pattern may differ for other chart types."

The separate Limitations section covers broader methodological caveats:
- Convenience sampling of models/languages
- Compute constraints
- Directions of generalizability not tested

---

## 4. Patterns from Specific Benchmark Papers

### HallusionBench (CVPR 2024) -- Diagnostic Benchmark

**Structure**: 2 subsections (Models, Result Analysis)
**Key technique**: Multi-layered metrics
- Correctness accuracy (the obvious metric)
- Yes/No bias analysis (diagnosing WHY models fail)
- Language vs vision diagnosis (separating failure modes)

**Narrative arc**: "Models perform poorly" -> "But WHY?" -> "Bias is a key factor"
-> "And the failure is specifically visual, not linguistic"

**Tables**: Reference BEFORE showing ("Results are given in Tab. 2"), then
3-4 paragraphs of prose analysis follow each table.

**Amount of analysis per table**: ~3-4 substantive paragraphs, each making a
distinct analytical point.

### POPE (EMNLP 2023) -- Hallucination Evaluation

**Key technique**: Stability analysis of the evaluation method itself
- Shows POPE's F1 score std dev (0.78) vs CHAIR's (3.22) -- argues for method reliability
- Identifies that top 30 objects comprise ~70% of all hallucinated objects (concentration)

**Narrative arc**: "Hallucination is pervasive" -> "Co-occurring objects are most
prone" -> "Our evaluation method is more stable than alternatives"

### AppWorld (ACL 2024 Best Resource) -- Agent Benchmark

**Key technique**: Headline number + difficulty stratification
- Leads with: "GPT-4O achieves only 48.8% on normal, 30.2% on challenge"
- Then shows: next-best LLM is far behind at 32.7% and 17.5%
- Uses programmatic "unit test" evaluation (avg 8, max 22 per task)

**Narrative arc**: "Even the best models solve less than half" -> "Gap widens
on harder tasks" -> "This benchmark has room for years of progress"

### Mission: Impossible Language Models (ACL 2024 Best Paper)

**Key technique**: Training dynamics, not just final performance
- Shows learning curves at various stages, not just endpoint accuracy
- Uses synthetic "impossible" languages as controlled conditions
- Clear control comparison (English vs impossible variants)

**Narrative arc**: "Models DO distinguish possible from impossible" -> "But the
difficulty gradient matches linguistic theory" -> "This challenges Chomsky's
claims with actual evidence"

### Aya Model (ACL 2024 Best Paper) -- Multilingual

**Key technique**: Aggregation by meaningful categories
- Groups 101 languages by resource level (high/mid/low)
- Separates discriminative vs generative evaluation
- Uses human evaluation AND automatic metrics
- Puts per-language details in appendix

**Narrative arc**: "Aya outperforms baselines across the board" -> "But gains
are largest for low-resource languages" -> "Data mixture composition matters
more than scale alone"

---

## 5. Common Mistakes in Results Sections

### Mistake 1: Over-Reporting (Wall of Numbers)
**Symptom**: Every cell of every table is discussed in prose.
**Fix**: Identify 3-5 key findings. Reference the table for details, but only
discuss the numbers that support your findings.

### Mistake 2: Under-Analyzing (Tables with No Interpretation)
**Symptom**: "Table 2 shows the results" with no follow-up.
**Fix**: Every table needs at least 1 paragraph of analysis. If a table doesn't
warrant analysis, it belongs in the appendix.

### Mistake 3: Cherry-Picking (Highlighting Only Wins)
**Symptom**: Only discussing conditions where your method/finding looks strong.
**Fix**: Explicitly address where results are weak or unexpected. Reviewers WILL
check the tables for patterns you don't discuss.

### Mistake 4: No Baselines or Unfair Comparisons
**Symptom**: Comparing your best setup to others' default setups.
**Fix**: Include random baselines, human performance, and compare under
matched conditions.

### Mistake 5: Not Connecting to Research Questions
**Symptom**: Results section reads like a data dump disconnected from the intro.
**Fix**: Open each results subsection by restating which RQ it addresses.
Close by answering that RQ explicitly.

### Mistake 6: Treating All Findings as Equally Important
**Symptom**: Equal space for trivial and groundbreaking findings.
**Fix**: Lead with your most important/surprising finding. Give it the most
space. Minor confirmatory results get 1-2 sentences.

### Mistake 7: No Error Analysis or Failure Cases
**Symptom**: Only aggregate metrics, no examples of where things go wrong.
**Fix**: Include 2-3 qualitative examples of failures. This shows depth of
understanding and honesty.

---

## 6. How to Present Cross-Dimensional Findings

### When Quality and Reliability Rankings Diverge

This is YOUR paper's key scenario: models that score high on quality might
score differently on reliability/hallucination. Here's how to present this:

#### Technique 1: The Divergence Table

Create a compact table showing both rankings side by side:

| Model | Quality Rank | Reliability Rank | Gap |
|-------|-------------|-----------------|-----|
| GPT-4V | 1 | 3 | -2 |
| Claude | 2 | 1 | +1 |
| Gemini | 3 | 2 | +1 |

Then discuss the gap column explicitly.

#### Technique 2: The Scatter Plot

Plot quality (x-axis) vs reliability (y-axis). Models in different quadrants
tell different stories:
- Upper-right: good at both (the ideal)
- Lower-right: high quality but unreliable (the "eloquent hallucinator")
- Upper-left: reliable but low quality (the "honest but basic")
- Lower-left: bad at both

**This is one of the most powerful visualizations for your paper.**

#### Technique 3: The Correlation Analysis

Report Spearman/Kendall rank correlation between dimensions. If rho is low,
that IS your finding:

> "Quality and reliability rankings show only weak correlation (Spearman rho =
> 0.34, p = 0.12), indicating that these dimensions capture fundamentally
> different model capabilities that should be evaluated independently."

#### Technique 4: The Narrative Frame

Frame the divergence as your paper's central contribution:

> "A model's ability to produce detailed, well-structured descriptions of
> scientific figures does not predict its tendency to hallucinate information.
> This disconnect -- between apparent quality and factual reliability -- is
> the central finding of our evaluation."

### How to Frame the Main Finding of a Multi-Dimensional Benchmark

The main finding should be a **relationship between dimensions**, not the
performance on any single dimension. Options:

1. **Independence finding**: "Quality and reliability are independent"
2. **Tradeoff finding**: "Higher detail comes at the cost of accuracy"
3. **Surprising winner**: "The best model on X is not the best on Y"
4. **Evaluation gap**: "Single-metric evaluation misses critical failures"

---

## 7. Word Budget Management in 8-Page Papers

### ACL Format Constraints
- 8 pages of content (9 on camera-ready)
- Unlimited references
- Limitations section after conclusion (does NOT count toward page limit)
- Ethics/broader impact section (does NOT count)
- Appendix after references (does NOT count)

### Typical Space Allocation (for a benchmark/evaluation paper)

| Section | Pages | % of 8 pages |
|---------|-------|-------------|
| Introduction | 1.0-1.25 | ~15% |
| Related Work | 0.75-1.0 | ~10% |
| Dataset/Benchmark Description | 1.5-2.0 | ~22% |
| Evaluation Framework/Method | 1.0-1.5 | ~15% |
| Results | 1.5-2.0 | ~22% |
| Analysis | 0.75-1.0 | ~12% |
| Conclusion | 0.25-0.5 | ~4% |

For your paper (benchmark with multi-dimensional evaluation):
- **Results + Analysis combined**: aim for 2.5-3.0 pages
- **Of that**: ~1.5 pages for main results (tables + key findings), ~1.0-1.5 pages for analysis

### What Goes in Main Paper vs Appendix

**Main paper (must be self-contained)**:
- 1 main results table (the headline comparison)
- 1-2 analysis figures (the key visual insight)
- 1 smaller table for the most important drill-down
- All prose explaining findings and their significance

**Appendix (supporting detail)**:
- Full per-model, per-condition results matrices
- Per-language or per-chart-type breakdowns
- Additional qualitative examples beyond the 2-3 in main paper
- Prompt templates, annotation guidelines
- Statistical significance tests / confidence intervals
- Implementation and hyperparameter details

### Conciseness Techniques

1. **Merge Results and Analysis**: Don't separate them. Present a finding,
   immediately analyze it, move to next finding. This saves the overhead
   of two separate section intros.

2. **Use footnotes for caveats**: Instead of a full sentence about a minor
   exception, use a footnote.

3. **Use "notably" and "in contrast" as transitions**: Skip full transition
   sentences. Just pivot with a discourse marker.

4. **One paragraph per finding**: Each analytical paragraph should make exactly
   one point. If you're making two points, split into two paragraphs.

5. **Reference appendix freely**: "Full per-model breakdowns appear in
   Appendix B" saves you from repeating minor numbers.

---

## 8. Example Results Section Skeleton (For Your Paper)

Here is a concrete skeleton tailored to a benchmark/evaluation paper with
multiple models, multiple judges, and multiple quality dimensions:

```
## 5 Results and Analysis

[Opening paragraph: 2-3 sentences stating the experimental scope --
how many models, how many figures, how many judges, what dimensions.
Then state the headline finding in 1 sentence.]

### 5.1 Overall Performance

[Main results table: Models x Aggregate Dimensions]

[Paragraph 1: Claim + Evidence -- who wins overall, by how much]
[Paragraph 2: The key surprise -- where rankings diverge across dimensions]
[Paragraph 3: Judge agreement -- do all judges see the same pattern?]

### 5.2 Quality vs Reliability Disconnect

[Figure: Scatter plot or divergence visualization]

[Paragraph 1: The disconnect is the main finding -- state it clearly]
[Paragraph 2: Evidence -- specific model pairs that illustrate it]
[Paragraph 3: Why this matters -- implications for evaluation practice]

### 5.3 Failure Mode Analysis

[Small table or figure: Common failure types and their frequency]

[Paragraph 1: What kinds of errors dominate? (hallucination types)]
[Paragraph 2: Which models are prone to which errors?]
[Paragraph 3: Connection to model architecture/training (why)]

### 5.4 [Optional: Adversarial Robustness / Specific Probe]

[Results from your adversarial transforms]

[Paragraph 1: Do models degrade gracefully or catastrophically?]
[Paragraph 2: Which transforms reveal the most about model behavior?]
```

### Example Opening Paragraph

> We evaluate 11 vision-language models across 1,005 scientific figures spanning
> 4 languages, using 4 LLM judges to assess both descriptive quality and
> factual reliability. Our central finding is that quality and reliability are
> largely independent: the models producing the most detailed, well-structured
> descriptions are not necessarily the most factually accurate (Section 5.2).

### Example Analysis Paragraph

> Proprietary models produce significantly more detailed descriptions than
> open-source alternatives, with GPT-4V averaging 287 tokens per description
> compared to LLaVA's 142 (Table 2). However, this verbosity comes with a cost:
> GPT-4V's hallucination rate (23.4%) exceeds LLaVA's (18.1%) despite its
> higher quality scores. We attribute this to a "fluency trap" -- models that
> generate more text create more opportunities for unsupported claims. This
> finding suggests that evaluation frameworks measuring only descriptive quality
> systematically favor models that are verbose but unreliable.

### Example Transition Between Findings

> While the overall rankings favor proprietary models (Section 5.1), a different
> picture emerges when we examine reliability in isolation.

or:

> The quality-reliability disconnect documented above raises a natural question:
> do these patterns hold uniformly across chart types, or are some visual
> formats more challenging than others?

---

## 9. Sentence Templates for Results Writing

### Introducing a table
- "Table X reports [metric] across [conditions]."
- "We summarize [what] in Table X."
- "Results are shown in Table X."
- (Always reference the table BEFORE it appears, or in the same paragraph.)

### Stating a main finding
- "Our central finding is that [X]."
- "The most striking pattern in Table X is [Y]."
- "Across all conditions, [pattern] holds consistently."

### Noting a surprise
- "Surprisingly, [finding] -- counter to expectations based on [prior work]."
- "Contrary to [assumption], we find that [result]."
- "An unexpected pattern emerges in [condition]: [description]."

### Providing explanation
- "We attribute this to [mechanism]."
- "This likely reflects [explanation], as evidenced by [supporting data]."
- "One possible explanation is [hypothesis], supported by the observation that [evidence]."

### Acknowledging caveats inline
- "While this pattern is robust across [subset], we note that [caveat]."
- "This result should be interpreted with caution given [limitation]."

### Connecting to implications
- "This has practical implications for [application]: [consequence]."
- "For practitioners, this suggests that [actionable takeaway]."

### Transitioning between findings
- "Having established [finding 1], we now examine [aspect 2]."
- "A different picture emerges when we consider [dimension]."
- "This pattern is further nuanced by [additional factor]."
- "Notably, [contrasting finding]."
- "In contrast to [previous finding], [new finding]."

---

## 10. Checklist Before Submitting Results Section

- [ ] Does the first paragraph of Results state the headline finding?
- [ ] Is every table/figure referenced in the text BEFORE it appears?
- [ ] Does every table have at least 1 paragraph of analysis?
- [ ] Are tables bolding best results and underlining second-best?
- [ ] Do you discuss both strengths AND weaknesses in results?
- [ ] Do you explain WHY, not just WHAT, for key patterns?
- [ ] Are full-matrix results in the appendix, with only key comparisons in main paper?
- [ ] Does each analysis paragraph follow the Claim-Evidence-Explain-Connect pattern?
- [ ] Are your findings ordered by importance (most important first)?
- [ ] Do you explicitly answer each research question from the introduction?
- [ ] Is there at least 1 qualitative example / case study?
- [ ] Have you reported baselines (random, human) for comparison?
- [ ] Is the Results+Analysis section 2.5-3.0 pages?
- [ ] Are per-item breakdowns in the appendix, not the main paper?
- [ ] Does the narrative tell a story, not just list numbers?
