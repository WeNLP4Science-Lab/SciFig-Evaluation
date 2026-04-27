# Chapter 6 (Results) — RQ1 Section Structure

**Budget**: ~5 pages (text + tables + figures)
**Principle**: 2 tables + 3-4 figures in main text. All other tables and figures in appendix, referenced inline.

---

## Page 1-2: Main Results (~2 pages)

### Table 1 (MAIN): Model Leaderboard
- 13 models x (Overall, EN, BG, CN, DE) with 95% CI
- Bold best, underline second-best per column
- Grouped by family (Proprietary / Qwen / LLaMA / Gemma / Phi)
- Booktabs style, no vertical lines
- Takes ~0.5 page

### Figure 1 (MAIN): Heatmap — Model x Language
- Visual companion to Table 1
- 13 rows x 6 columns (EN, BG, CN, DE, Multi, Overall)
- Annotated cells with MQM scores, RdYlGn diverging colormap
- Double-column width (~6.75")
- Takes ~0.4 page

### Text (~1 page):
- Headline: best model (GPT-5.2), worst (Gemma-4B), score range
- Proprietary vs open-source gap — is it narrowing?
- Scaling within families: Qwen 235B > 32B > 30B > 8B, Gemma 27B > 12B > 4B
- Per-language findings inline: German consistently highest, language gaps (reference Appendix Table A.2 for EN-X gap details)
- Per chart type findings inline: hardest/easiest types with 2-3 numbers (reference Appendix Table A.3 for full breakdown)
- Significance: which adjacent-rank differences are significant? (reference Appendix Table A.4 for full pairwise tests)
- Scaling trend in 1 sentence (reference Appendix Figure A.1 for scaling plot)

---

## Page 3: Human Validation (~1 page)

### Table 2 (MAIN): Human vs LLM Judge Comparison
- 4 models x (Human MQM, GPT-4o MQM, Mistral MQM)
- Footer rows: Spearman rho, Kendall tau, Krippendorff's alpha
- Compact: ~0.3 page

### Figure 2 (MAIN): Scatter — Human vs LLM Judge
- Two panels side by side: Human vs GPT-4o | Human vs Mistral
- Points colored by model (4 colors)
- Dashed y=x identity line, solid regression line
- Annotated with Spearman rho + p-value
- Double-column width
- Takes ~0.4 page

### Text (~0.3 page):
- Both judges preserve model ranking (key validation)
- Both score 10-25 points lower than humans (systematic harshness)
- Mistral closer to human; GPT-4o harsher
- Gap largest for GPT-5.2 (25 pts) — judges over-penalize high-quality descriptions
- Severity split: Mistral 26-31% Major vs GPT-4o 69-71% Major (same errors, different severity)
- IAA inline: Krippendorff alpha = X, mean diff 7.6, 69% within 10 pts (reference Appendix Figure A.2 for IAA box plot)

---

## Page 4: Error Analysis + Ablations (~1 page)

### Figure 3 (MAIN): Stacked Bar — Error Type Proportions per Model
- Horizontal 100% stacked bars, 13 models
- 6 segments: Acc/Maj, Acc/Min, Comp/Maj, Comp/Min, Clar/Maj, Clar/Min
- Total error count annotated at end of each bar
- Single or double-column
- Takes ~0.4 page

### Text (~0.6 page):
**Error analysis** (~0.3 page):
- Accuracy errors dominate (~80%), completeness secondary, clarity rare
- Top sub-types: Incorrect Numerical Value (29-36%), Visual Attribute Mapping
- Human annotators confirm same error ranking — not a judge artifact
- Hallucination rates inline: X% for worst model, Y% for best (reference Appendix Table A.5)
- Colour tolerance limitation: 1 sentence

**Ablation findings** (~0.3 page):
- Prompt language (C1/C2/C2'): which condition wins, key delta numbers inline (reference Appendix Table A.6)
- Chain-of-thought: CCoT effect size inline, +X.X for model Y (reference Appendix Table A.7)
- Cross-lingual controlled (13 parallel figs): confirms/contradicts main findings, 1-2 sentences (reference Appendix Table A.8)

---

## Page 5: Summary + Optional Figure (~0.5-1 page)

### Figure 4 (MAIN, optional): Scaling Plot OR Radar
- Option A: Scaling plot — params (log x) vs MQM, lines per family. Shows diminishing returns. Single-column.
- Option B: Radar — 2-3 top models across dimensions. Visually striking.
- Include whichever tells a more interesting story. Other goes to appendix.
- Takes ~0.3 page

### Text (~0.3 page):
- 5-6 bullet points summarizing key RQ1 findings
- Bridge sentence to RQ2 (adversarial robustness)

---

## Appendix Tables (referenced from main text)

| ID | Content | Referenced from |
|----|---------|-----------------|
| Table A.1 | Full leaderboard with all CIs and significance markers | Page 1 |
| Table A.2 | Per-language EN-X gap metrics (13 models x 3 gaps) | Page 1 |
| Table A.3 | Per chart type breakdown (type x avg MQM x best/worst) | Page 1 |
| Table A.4 | Pairwise significance tests + Cliff's delta | Page 1 |
| Table A.5 | Hallucination rates per model | Page 4 |
| Table A.6 | Prompt ablation C1/C2/C2' full results | Page 4 |
| Table A.7 | Chain-of-thought ablation full results | Page 4 |
| Table A.8 | Cross-lingual controlled (13 figs x 4 langs) | Page 4 |
| Table A.9 | Error sub-type detailed counts per model | Page 4 |
| Table A.10 | Judge agreement matrix (full) | Page 3 |

## Appendix Figures (referenced from main text)

| ID | Content | Referenced from |
|----|---------|-----------------|
| Figure A.1 | Scaling plot (params vs MQM) | Page 1 |
| Figure A.2 | IAA box plot (annotator variability) | Page 3 |
| Figure A.3 | Violin plots (score distributions per model) | Page 1 |
| Figure A.4 | Slope chart (EN vs non-EN gap) | Page 1 |
| Figure A.5 | Radar chart (model capability profiles) | Page 5 |
| Figure A.6 | Ablation delta chart (diverging bars) | Page 4 |
| Figure A.7 | Cross-lingual controlled bar chart | Page 4 |

---

## Summary

**In main text**: 2 tables + 3-4 figures + ~2.5 pages text = ~5 pages
**In appendix**: ~10 tables + ~7 figures = comprehensive backup
**Every appendix item** has a "(see Table/Figure A.X)" reference in the main text
