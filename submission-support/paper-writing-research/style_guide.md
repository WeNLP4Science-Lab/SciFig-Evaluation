# SciFig-Eval Paper Style Guide

All agents writing paper sections MUST follow this guide for consistency.

---

## Voice and Tone

- **Academic but direct.** No filler ("it is worth noting that..."), no hedging unless genuinely uncertain.
- **Active voice preferred.** "We evaluate" not "evaluation was performed."
- **Present tense for claims and framework.** "Our framework measures..." "Models exhibit..."
- **Past tense for experiments.** "We evaluated 8 models..." "GPT-5.2 scored..."
- **Confident but precise.** State findings clearly. Qualify with data, not weasel words.
- **No first-person singular.** Always "we" (anonymous multi-author paper).

## Terminology (use consistently throughout)

| Concept | Use This | NOT This |
|---|---|---|
| Our benchmark | SciFig-Eval | SciFig, SciFig-Evaluation, the benchmark |
| Evaluation metric | MQM score | quality score, description score |
| Chart types | bar chart, line plot, pie chart | bar graph, line chart, pie graph |
| Image degradation | transform | perturbation, corruption, augmentation |
| Poisoned caption | modified caption | fake caption, wrong caption, adversarial caption |
| Model honesty | admittance | honesty, transparency, self-awareness |
| Pushing back on lies | resistance | robustness (reserve for transforms) |
| Inferring from context | inductance | inference, reasoning (too generic) |
| The framework | A-R-I framework | ARI, A.R.I., admittance-resistance-inductance |
| Hallucination probes | resistance probes | hallucination tests, adversarial questions |
| Element that can't be recovered | unrecoverable element | hidden element, missing element |
| Element that can be inferred | inferable element | recoverable element, deducible element |
| Visual uncertainty | visual limitation | blindness, inability |
| Model gives answer despite blur | fabrication | hallucination (overloaded term), guessing |
| Model acknowledges blur | admission | acknowledgment, confession |
| Description task | open-ended description | free-form description |
| Reasoning task | targeted question | specific question, direct question |
| Baseline condition | standard evaluation | clean evaluation, normal evaluation |
| Adversarial condition | behavioral evaluation | stress test, adversarial test |

## Model Names (use short names in text, full in table footnotes)

| Short Name | Full Name | Notes |
|---|---|---|
| GPT-5.2 | GPT-5.2 (Azure) | Commercial, closed |
| Gemini | Gemini 3.1 Pro | Commercial, closed |
| Llama 4 | Llama 4 Maverick 17B-128E | Open-weight, MoE |
| Qwen-235B | Qwen3-VL-235B-A22B | Open-weight, MoE (22B active) |
| Qwen-30B | Qwen3-VL-30B-A3B | Open-weight, MoE (3B active) |
| Qwen-8B | Qwen3-VL-8B | Open-weight, dense |
| Gemma | Gemma3-27B-IT | Open-weight, dense |
| Phi-4 | Phi-4-Multimodal | Commercial, small |

## Numbers and Statistics

- MQM scores: one decimal place (91.6, not 91.62)
- Resistance/bias scores: two decimal places (0.89, not 0.893)
- Percentages in text: "89%" not "0.89" (except in formal metric definitions)
- Counts: no decimals ("250 figures" not "250.0")
- Ranges: en-dash ("0.73--0.95")
- Use $\rho$ for Spearman correlation, not "r" or "rho"
- Statistical claims need sample size: "across 250 figures" or "(n=100)"

## Tables and Figures

### Reserved assignments:
- **Table 1**: Dataset statistics (figure types, counts, sources)
- **Table 2**: Evaluation dimensions overview (the 2×2 matrix)
- **Table 3**: MQM baseline leaderboard (8 models × overall + per-type)
- **Table 4**: Transform robustness results (8 models × 6 transforms)
- **Table 5**: Behavioral evaluation leaderboard (resistance, caption bias, admittance)
- **Table 6**: Active probe results (admits/fabricates/correct for admittance + inductance)
- **Figure 1**: Overview diagram (2×2 framework)
- **Figure 2**: Example figures from dataset with probe illustrations
- **Figure 3**: Quality vs reliability scatter plot
- **Figure 4**: A-R-I radar charts per model (or selected models)

### Table style:
- Use \booktabs (\toprule, \midrule, \bottomrule)
- Bold the best result in each column
- Use \textbf{} for best, \underline{} for second best
- Right-align numbers, left-align text
- Model names in leftmost column

### Figure style:
- Clean, minimal, no gridlines unless necessary
- Colorblind-friendly palette
- Font size readable at column width
- Captions should be self-contained (reader should understand without reading text)

## Section Length Targets (8 pages total)

| Section | Pages | Words (~600/page) |
|---|---|---|
| Introduction | 1.25 | ~750 |
| Related Work | 0.75 | ~450 |
| Framework | 2.0 | ~1200 |
| Experiments & Results | 2.5 | ~1500 |
| Analysis | 1.0 | ~600 |
| Conclusion | 0.5 | ~300 |
| **Total** | **8.0** | **~4800** |

Note: Tables and figures consume space. Budget ~1.5 pages for tables/figures, so actual text is ~6.5 pages worth.

## Citation Style

- Use \citet{} for "Author (Year)" in text: "Following \citet{loftus1975leading}..."
- Use \citep{} for "(Author, Year)" parenthetical: "...presupposition embedding \citep{loftus1975leading}"
- Cite all baselines we compare against
- Cite the psychology sources for probe design principles
- Do NOT hallucinate citations — only cite papers we can verify exist

## Key Framing Rules

1. **Never call this "just a benchmark."** It's a diagnostic evaluation framework with a behavioral theory (A-R-I).
2. **Lead with findings, not methodology.** Methodology serves the findings.
3. **The main claim is orthogonality.** Quality rankings ≠ reliability rankings. Everything supports this.
4. **Name the gap explicitly.** "Existing benchmarks measure X but not Y. We measure both and show they're independent."
5. **Psychology-informed ≠ psychology paper.** Reference the principles but don't over-explain the psychology. One sentence per principle, cite, move on.
6. **A-R-I is a contribution, not just a label.** Show it captures real behavioral distinctions (inductance validation: 75% vs 14% correct).
7. **Ablation defends methodology.** Mistral vs GPT-4o probes → consistent results → probe design is robust.

## LaTeX Conventions

- \textsc{SciFig-Eval} for the benchmark name
- \textbf{} for emphasis, not \emph{} (which is for introducing terms)
- \emph{} only for first use of a technical term
- Use \paragraph{} for inline headings within subsections
- Cross-reference: \S\ref{sec:label} for sections, Table~\ref{tab:label}, Figure~\ref{fig:label}
- Use ~ (non-breaking space) before \ref, \cite, numbers with units

## Forbidden Patterns

- "It is important/interesting/noteworthy to note that..." → just state the thing
- "As shown in Table X, ..." at the start of a paragraph → lead with the finding
- "We believe/think that..." → state it as a finding with evidence
- "To the best of our knowledge..." → check if it's actually true, then state it
- "State-of-the-art" without specifying what task/metric
- "Significantly" without a statistical test
- Bullet points in the paper body (use in appendix only)
- Excessive self-citation of the thesis (this is anonymous + ACL version is standalone)
