# Reviewer YLTQ

**Overall:** 3.0 (Findings)
**Soundness:** 3 · **Excitement:** 4 · **Confidence:** 4
**Reproducibility:** 3 · **Datasets:** 3 · **Software:** 3
**Posted:** 15 Sept 2026 (modified 15 Sept 2026, 15:28)

## Paper Summary (their words)

> The paper introduces SciFig-Eval, a diagnostic VLM benchmark that jointly evaluates perception, reasoning, and behavioral reliability under uncertainty for scientific figure understanding. The dataset comprises 250 bar/line/pie charts from 187 arXiv papers with expert descriptions, expanded via image transforms, reasoning questions, resistance probes, caption-bias probes, and selective-blur probes into over 34,000 evaluation instances across eight VLMs. The paper proposes the Admittance–Resistance–Inductance (A-R-I) framework to characterize whether models acknowledge insufficient evidence (Admittance), resist misleading context (Resistance), and infer from recoverable partial evidence (Inductance). The headline finding is that models with similar perception/reasoning performance can diverge sharply in behavioral reliability: GPT-5.2 has the highest description quality but fabricates answers for unreadable content 96% of the time, while the comparably capable Gemini 3.1 Pro admits uncertainty in 71% of such cases.

## Strengths (summarised)

- Polished writing and figures; fluent exposition
- Motivation is solid; A-R-I framework and its tasks are novel and reasonable
- Captures behavioural patterns prior work hasn't sufficiently studied
- Useful complement to purely evaluating perception + reasoning; has measurement value for high-stakes deployment
- Experimental design is thorough: cross-judge ablation (Mistral vs. GPT-4o), probe-designer ablation, split-half reliability, 100/250-figure scale validation
- Findings and analysis are valuable; conclusions logically clear

## Weaknesses

### W1 — Previous-round responses under-addressed
Some points were handled well (item-level human agreement, error-type table, alternative-judge ablation). Others got only added discussion or acknowledged limitation, with **no new experiment**:

- **(a)** On frequency of stress conditions in real workflows (previous No6d W2 / LhRb C1): revision only *maps* each probe family to a "deployment failure mode" analogically — doesn't give actual frequency/proportion in real document-processing workflows.
- **(b)** On whether Inexist-probe failures = visual blindness or instruction-following pressure (previous h9tb W2): revision only adds an argumentative sentence in Limitations (top-model MQM ≥ 90 suggests instruction-following is more likely) — doesn't design a controlled experiment (e.g., prompt variant that removes the instruction-following pressure) to actually disentangle these confounded factors.
- **(c)** Dataset scale (250 figures, 3 chart types) was not increased. Response argues via "34,000+ evaluation instances" and "600+ annotation hours" — but these are repeated evaluations of the same base figures from multiple angles; doesn't address the original chart diversity / scale concern.

### W2 — Dataset sources too limited
- **Chart-type coverage:** only 3 simpler statistical chart types (line, bar, pie). No other statistical chart types, no broader experimental chart types, no complex multi-panel figures.
- **Disciplinary coverage:** currently only NLP/ML-direction papers. Title/abstract use "scientific figures" as a general term — reviewer finds this **inappropriate**. Claimed scope should be **narrowed to statistical charts or CS-style charts**, because many disciplines aren't included (physics, biology, chemistry — scatter-plot-dense experimental figures, micrographs, staining images, schematic diagrams).

### W3 — GPT-4o's dual role + item-level noise
- GPT-4o judges MQM/resistance/admittance/inductance AND generates reasoning questions, resistance probes, caption-bias probes, selective-blur targets (some stages cross-checked by Mistral Large 3).
- Model-level rankings hold under cross-judge ablation, BUT item-level human-judge agreement is only moderate: Pearson r = 0.68, Spearman ρ = 0.58, with a systematic −15-point bias.
- Non-trivial noise at the per-item level is averaged out when aggregated into rankings.
- Paper discusses ranking robustness but says relatively little about **per-item judgment quality**.

### W4 — Dataset and evaluation scripts not available for review
Couldn't verify dataset quality or code-logic consistency with the paper. Introduces uncertainty.

## Comments / suggestions

- **Narrow the paper's title claim.** Explicitly state dataset scope (NLP/ML/CL arXiv papers) in abstract + introduction to avoid over-generalised readings of "scientific figures."
- **Flag the visual-blindness vs. instruction-following ambiguity earlier** (in main text, not only Limitations). Directly affects interpretability of Resistance dimension.
- **Appendix B pipeline figures (Figs 6–11)** appear AI-generated; font size very small, unreadable. Manually redraw with reasonable font size per ACL requirements. **Reference them at least once in the main text** to help readers grasp GPT-4o's dual role.
- **Reference formatting:**
  - Per ACL/ARR BibTeX conventions, arXiv preprints should use `@misc` type, not `@article`.
  - Add clickable link to every reference entry.
  - Check whether each arXiv paper now has an official peer-reviewed publication venue; replace preprint citation with peer-reviewed version where one exists.
- **Provide accessible datasets, evaluation code, model outputs at review time** — strengthens reproducibility.

## What this reviewer would most reward in a revision

1. Title/abstract/intro scope narrowing (statistical charts, NLP/ML/CL arXiv)
2. Controlled experiment isolating visual blindness vs. instruction-following pressure
3. Redrawn pipeline figures (larger fonts, referenced from main text)
4. Bibliography cleanup: `@misc` for arXiv, replace preprints with peer-reviewed versions, add DOI/URL links
5. Release datasets + code before/during review
6. Explicit discussion of per-item judgment quality (not just aggregate ranking robustness)
