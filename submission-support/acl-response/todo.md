# TODO — ACL ARR 2026 May Reviewer Concerns

Ranked from most critical (multi-reviewer, blocks acceptance) to least critical (polish).
Source of every item: `acl-response.md` (Reviewer h9tb, Reviewer No6d, Reviewer LhRb).
Action plan is deliberately not included here — that will be drafted separately.

## Scores snapshot

| Reviewer | Overall | Soundness | Excitement | Confidence | Reproducibility | Datasets | Software |
|---|---|---|---|---|---|---|---|
| h9tb | 3 Findings | 3 | 3.5 | 3 | 5 Enabling | 5 Enabling | 5 Enabling |
| No6d | **2 Resubmit** | 2.5 | 2 | 3 | **2 Hard to reproduce** | 2 Documentary | 2 Documentary |
| LhRb | 3 Findings | 3 | 3 | **4** | 3 Some difficulty | 3 Potentially useful | 3 Potentially useful |

Aggregate: Overall 2.67, Soundness 2.83, Excitement 2.83.
Two Findings votes plus one Resubmit. The Resubmit (No6d) is the vote to lift; LhRb is the highest-confidence vote and lands on Findings.

---

## P0 — Critical (multi-reviewer, gates acceptance)

### 1. Reposition the A-R-I framework (novelty framing)

- Raised by: **No6d, LhRb**
- No6d: "The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method." Suggests "position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm."
- LhRb: "The A-R-I framework is useful, but I am not fully convinced that these three dimensions are sufficient to cover behavioral reliability." Suggests: "The A-R-I dimensions could be better justified as a necessary and relatively complete decomposition."
- Todo:
  - Reframe A-R-I in the introduction/framework section as a **diagnostic taxonomy / decomposition**, not a new evaluation paradigm.
  - Add a subsection arguing **necessity and sufficiency** of the three axes (why exactly these three, why not more, why not fewer, what deployment risk each captures uniquely).
  - Acknowledge related behavioural axes from prior work explicitly (uncertainty acknowledgment, robustness to misleading context, contextual inference) and state clearly what A-R-I contributes on top (unified probing setup, cross-axis empirical separation, targeted probe design).

### 2. Chart-type coverage (only bar, line, pie)

- Raised by: **h9tb, No6d**
- h9tb: "The dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding."
- No6d: "The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie)."
- Todo:
  - Add a **scatter + heatmap pilot** (target ~20–40 figures each) to the corpus.
  - Rerun A-R-I probes on the new chart types, at minimum for the top-3 models, to show the framework generalises.
  - Update Table 5 (dataset comprehensive) and Section 3.1 with the new counts.
  - Update abstract/intro to reflect broader chart-type coverage.

### 3. Dataset scale (250 figures is modest for a benchmark paper)

- Raised by: **No6d, LhRb**
- No6d: "The benchmark comprises only 250 figures ... modest for a benchmark paper, particularly given that the probe types are themselves not especially novel."
- LhRb: "250 figures is still limited for the broad space of scientific figures."
- Todo:
  - Foreground the **34,000 evaluations denominator** more prominently (abstract, intro, related-work comparison).
  - Consider expanding the corpus (see #2) — even 350–400 figures with the new chart types would materially soften this critique.
  - Add a paragraph explicitly comparing per-figure evaluation depth vs prior benchmarks (many benchmarks have more figures but fewer evaluation angles per figure).

### 4. GPT-4o judge dependence, item-level agreement, and version drift

- Raised by: **No6d, LhRb**
- No6d: "The main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report **direct agreement between GPT-4o and humans, ideally at the item level**. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified."
- LhRb: "GPT-4o is used quite heavily in probe generation and judging."
- Todo:
  - Report **item-level judge ↔ human agreement** (Cohen's κ or agreement rate per item), not just system-level ICC.
  - Rerun evaluation with a **current judge model** (Mistral Large 3 already used as validator; add GPT-5.2 or Claude Opus as an independent cross-check).
  - Pin **exact GPT-4o snapshot / Azure API version** used, and add it as a reproducibility note in Appendix E.
  - Add a robustness table showing rankings under alternative judges.

---

## P1 — High (single reviewer, substantive)

### 5. Real-world grounding of probes

- Raised by: **No6d**
- Verbatim: "The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots." Comments: "grounding them in realistic failure cases from scientific workflows — for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines."
- Todo:
  - Add a subsection (or dedicated paragraph in intro / Section 3.2) mapping each probe family to a **concrete real-world failure mode**:
    - Selective blur → PDF-parsing artefacts, low-res screenshots, redacted figures
    - Caption bias → multimodal RAG pipelines with incorrect figure-caption retrieval
    - False premise → user queries with mistaken premises in research assistant workflows
    - Visual perturbations → scanning artefacts, mobile screenshots, low-DPI displays
  - Cite concrete deployed systems where these failures matter (Anthropic Claude for Research, Elicit, Semantic Scholar).

### 6. Overall novelty of stress tests

- Raised by: **No6d**
- Verbatim: "Most of the stress tests build on existing ideas — image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment — rather than introducing new techniques."
- Todo:
  - Explicitly disclose which probe ideas are adapted from prior work and cite them upfront (this actually helps — it turns a weakness into scholarly rigour).
  - Emphasise what is genuinely new: **selective blur with OCR-anchored coordinate mapping and dual-stage grey-blend+Gaussian**, admittance-vs-inductance blur separation, the **unified evaluation across all four probe families on the same corpus**, and the **A-R-I decomposition** that ties them together.
  - Consider a "What is new here" mini-section or paragraph in Section 2 / Section 3.

### 7. Inexist probe: visual blindness vs instruction-tuning compliance

- Raised by: **h9tb**
- Verbatim: "The paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressure the model to comply with user prompts regardless of conflicting visual data."
- Todo:
  - Run a **text-only ablation** on the Inexist probes: pose the false-premise question without the image. If models still fabricate answers, that isolates instruction-tuning compliance pressure; if they refuse or admit, it points to visual blindness.
  - Report the ablation in a short appendix subsection with a table (per-model fabrication rate text-only vs image+text).
  - Discuss the interpretation in Section 5.

### 8. arXiv sampling and benchmark coverage

- Raised by: **LhRb**
- Verbatim: "I would suggest discussing more concretely how arXiv figure sampling affects benchmark coverage."
- Todo:
  - Add a paragraph in the limitations or dataset section on **sampling bias** — arXiv skews NLP/ML, English-language, preprint-stage, particular subfields.
  - Discuss what this excludes (e.g. biomedical figure conventions, engineering schematics, humanities visualisations).
  - Explicitly frame the benchmark's scope claim (representative of arXiv-style NLP/ML scientific figures) rather than "all scientific figures."

### 9. API model version drift discussion

- Raised by: **LhRb**
- Verbatim: "The paper should also discuss model version drift, especially for API models such as GPT and Gemini."
- Todo:
  - Add a paragraph in Appendix E on **version drift risk**: exact model snapshots used, dates of inference, expected drift for closed API models.
  - Recommend future re-runs pinning specific snapshots and reporting delta over time.
  - Note that this is why we release the corpus and prompts (so the setup is replayable against future snapshots).

### 10. Broader human evaluation / more diverse figure sources

- Raised by: **LhRb**
- Verbatim: "I would still have liked to see broader human evaluation or more diverse figure sources."
- Todo:
  - Expand human validation beyond the current 30-figure set (target: 60–90 figures spread across chart types).
  - Report per-chart-type human ↔ judge agreement.
  - Overlaps with #2 (diverse chart types) and #4 (item-level judge agreement).

---

## P2 — Medium (interpretation / framing)

### 11. Reproducibility concerns overall (No6d gave 2)

- Raised by: **No6d** (Reproducibility rating = 2)
- Verbatim: "The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided."
- Todo:
  - Reinforce commitment to **full public release** of dataset, prompts, model outputs, evaluation scripts on acceptance.
  - Consider releasing a **preview / partial dataset now** (e.g. via anonymous OSF or figshare) so reviewers can inspect it during the discussion period.
  - Add a "Data and Code Availability" section prominently.

### 12. Datasets and Software ratings 2 from No6d

- Raised by: **No6d** (Datasets = 2 Documentary, Software = 2 Documentary)
- Todo:
  - Directly follows from #11. Better public-release framing + preview access should lift these ratings.
  - Consider explicitly positioning the benchmark as **reusable for downstream evaluation of new VLMs** (e.g. "run your model through the pipeline and get an A-R-I profile") rather than just replicating our results.

---

## P3 — Low (polish, cosmetic, typos)

### 13. Llama 4 naming consistency

- Raised by: **h9tb**
- Verbatim: "please consistency writing the name of Llama 4"
- Todo:
  - Grep the paper for variants: `Llama 4`, `Llama-4`, `LLaMA 4`, `Llama4`, `Llama 4 Maverick`.
  - Unify to a single canonical form (likely `Llama 4 Maverick` or `Llama 4`).

---

## Meta / process

### 14. Confirm rebuttal window and length limits
- Check ARR May 2026 timeline: is there a rebuttal window? What length is permitted? Which weaknesses can be addressed in rebuttal vs which must wait for camera-ready or next cycle?

### 15. Draft rebuttal responses to each of P0 and P1 items
- Separate from this todo. Belongs in the action plan.

### 16. Decide whether to accept Findings offer or push for main track
- Two Findings votes (h9tb, LhRb) suggest Findings is on the table.
- No6d's Resubmit vote could be flipped to Findings with the P0 fixes.
- Weigh: accept Findings now vs revise for next ARR cycle for a main-track shot.

