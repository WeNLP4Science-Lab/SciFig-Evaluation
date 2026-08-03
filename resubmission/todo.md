# Resubmission TODO

Outstanding tasks tracked here. Each has a clear scope and completion criterion.

---

## T1 — Add a "Complete Example" appendix section

**Motivation:** Steffen's Group B2 comment ("more examples would be helpful, the paper is dense, and the setup could be better illustrated"). The paper currently has scattered examples (3 text probes in framework §3.2, 2 hook figures, text examples for 2 of 3 resistance sub-types) but no single place a reader can go to see how every evaluation type applies to one figure.

**Canonical figure:** **`multi_fig_004`** — the sunburst chart. Already well-tested in the presentation slides. Multi-tier structure makes it a natural target for varied probes (labels at different rings can be admittance targets or inductance targets).

**Placement:** New appendix section, e.g., `\section{Appendix: Complete Example}`, at the end of the appendix stack — after `evaluation_appendix.tex`.

### Proposed structure

**E.1 Canonical figure and ground truth**
- Figure image (sunburst `multi_fig_004`)
- Ground-truth expert description (from `dashboard/public/manifest.json` for this figure)
- MQM checklist snippet showing what the description is scored against

**E.2 Perception under transforms** (visual)
- Original image
- Noise variant
- Low-contrast variant
- Rotation variant
- One-liner caption per variant explaining what stresses which perception faculty

**E.3 Reasoning — one capability question per category**
- Counting: one Q + expected answer (from `dashboard/public/capability_questions/multi_fig_004.json`)
- Computation: one Q + expected answer
- Comparison: one Q + expected answer
- Pattern analysis: one Q + expected answer

**E.4 Behavioural probes on the same figure**

For each: probe input → expected reliable behaviour → 1-2 real model response snippets showing behavioural divergence (one "good" model + one "bad" model, both drawn from `results/generation/active_probes/*/` etc.).

- Admittance target — text label ring made unrecoverable via selective blur
- Inductance target — text label ring made obscured but recoverable from surrounding context
- Resistance / Inexist — probe about a non-existent ring or slice
- Resistance / Contra — probe with false numerical anchor
- Resistance / Unanswerable — probe requesting data beyond the chart
- Caption bias — original caption vs modified caption with 2–3 false claims highlighted in red

### Data sources

All raw material already exists in the repo — this is a selection + formatting task, not generation.

- Figure image: already in dashboard/public/figures/
- Ground-truth annotations: `dashboard/public/manifest.json`
- Capability questions: `dashboard/public/capability_questions/multi_fig_004.json`
- Resistance probes: `dashboard/public/resistance_probes/` + `dataset/resistance_probes/`
- Blur images: `dashboard/public/adversarial_admittance/multi_fig_004.png` and `adversarial_inductance/`
- Caption-bias probes: `dashboard/public/caption_bias/`
- Model responses: `results/generation/active_probes/*/admittance/`, `.../inductance/`, `.../resistance/`

### Effort

- Selection of good examples from data: ~45 min
- Figure/table LaTeX authoring: ~2 h
- One appendix page (possibly two) of content
- Total: half a day

### Priority

**Medium-high.** Not in the P0/P1 rebuttal commitments, but directly answers Steffen's B2 concern and helps the density issue that came up in multiple reviewer comments (No6d "the paper is dense," LhRb "would like more examples of behavioural probes"). Worth landing before final submission.

### Completion criterion

- A new appendix section that contains one example per evaluation type on the sunburst figure
- Real model response snippets included for at least the behavioural probes
- Reader can trace the same figure through every kind of evaluation

---

## Other resubmission tasks (see also `plan.md` for full inventory)

- Group B remaining items (B3: `results.tex:38` "more examples + human construction details")
- Group C: source cleanup (4 hidden `%\todo{}` + ~65 commented-out old paragraphs + remove `todonotes` package)
- Group D: `\am{}` macro audit
- P1 human-annotation-campaign paragraph (5 annotators / 600+ hours) — must appear in dataset or framework section
- P1 real-world-grounding paragraph (PDF/OCR/RAG mapping) — must appear in framework or dataset section
- P1 item-level GPT-4o vs human agreement study
- Bibliography: manual verification of the ~24 non-thesis entries listed in `bibliography-audit.md`
