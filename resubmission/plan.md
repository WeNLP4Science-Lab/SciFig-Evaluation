# Resubmission Plan — SciFig-Eval

For each reviewer concern (and the desk-rejection bibliography issue), we record: what the current paper does, what still needs to change, and the concrete plan.

Priority tiers:
- **P0** — Blocks resubmission (bibliography); non-negotiable
- **P1** — Critical (multi-reviewer or promised in rebuttal); must land
- **P2** — Important (single reviewer but substantive)
- **P3** — Polish (minor/consistency)

---

## P0 · Bibliography

### Issue: Hallucinated references (desk rejection cause)

Program Chairs flagged 6 citations as hallucinated. All 6 papers are real but the ACL bib was regenerated with LLM assistance and reintroduced author-name errors that had already been fixed for the thesis.

**Currently in paper:**
- `references.bib` contains the flagged entries with wrong author names/keys.

**Plan:**
1. **Rebuild `references.bib` from scratch** using the verified thesis `.bbl` (`thesis-work/support/thesis/main/abdnthesis.bbl`) as the source of truth.
2. **Every entry must be verified** against (a) the thesis `.bbl` and (b) the arXiv abstract page for the paper's actual metadata.
3. Cross-check with `thesis-work/support/internal-feedback/bib_corrections.md` for the specific corrections already applied to the thesis.
4. Add a note in the appendix stating we manually verified every citation.
5. **No LLM-generated bib entries at any point**, even for filling in missing fields.

**Owner:** Manual (Paul + Wei).

---

## P1 · Multi-reviewer / promised commitments

### Issue 1: A-R-I novelty framing (No6d W1b + C2, LhRb W3 + C3)

**Currently in paper (`framework.tex` §3.4):**
- New paragraph added: "A-R-I is not intended to exhaustively characterize behavioural reliability. Rather, it focuses on three complementary dimensions..." — partial fix.
- No explicit framing of A-R-I as extending established uncertainty metrics via the two ground-truth conditions we developed in the rebuttal.
- No citations to related behavioural dimensions (calibration, multi-turn dialogue consistency, prompt sensitivity).

**Still needs:**
1. Add the reframe from rebuttal: "A-R-I extends established uncertainty metrics to two novel settings: (i) whether the queried element exists, (ii) whether it is recoverable despite obscuration."
2. Explicit statement of scope: "A-R-I is not intended to exhaust behavioural reliability. Complementary axes such as verbalised confidence calibration, multi-turn visual-dialogue consistency, and prompt-form sensitivity remain outside our scope."
3. Cite 3 real papers for the excluded axes (Xuan et al. 2025 EMNLP for calibration + others from the rebuttal thread).
4. Add explicit necessity argument for the three dimensions.

**Where to add:** Framework §3.4 (extend the existing paragraph).

### Issue 2: Human annotation campaign details (No6d W3, LhRb W1)

**Currently in paper (`dataset.tex`):**
- Only says "two trained annotators (94% agreement) with a third adjudicator for disagreements."
- No mention of 5 annotators / 600+ hours across all tasks.
- No breakdown of hours per task (description / reasoning / blur / MQM eval).

**This was our headline defence of dataset scale in the rebuttal — it must be visible in the paper.**

**Still needs:** Add a paragraph to the Dataset section:
> "A high-quality human annotation campaign involving 5 annotators over 600+ hours was carried out across perception, reasoning, and behavioural tasks. This includes 250 figure descriptions annotated by 3 student annotators over ~240 hours (with an overlapping subset for inter-annotator agreement), 1,000 reasoning questions post-edited by 4 annotators over ~200 hours, 443 selective-blur targets post-edited by 3 annotators over ~100 hours, and human MQM evaluation of 4 LLMs on 30 figures by 3 annotators over ~90 hours."

**Where to add:** Dataset section (`dataset.tex`) or Framework §3.1.

### Issue 3: GPT-4o vs human item-level agreement (No6d W4)

**Currently in paper (`appendix_human_validation.tex`):**
- Reports model-level Spearman ρ=0.80 between GPT-4o and humans on 120 MQM items.
- Reports Krippendorff's α=0.91 inter-annotator.
- Reports per-pair Pearson r=0.65 (this IS item-level for MQM but not for behavioural probes).
- **Nothing on item-level agreement for behavioural probes** (Admittance, Resistance, Inductance).

**We promised in rebuttal:** "We will add the item-level correlation between GPT-4o and humans in the updated version."

**Still needs:**
1. Small annotation study — 30–50 items × 2–3 annotators judging model responses to behavioural probes, compared against GPT-4o labels.
2. Report Cohen's κ or raw agreement.
3. Add subsection to `appendix_human_validation.tex`.

**Owner:** Human annotation task by the team + Paul to compute stats.

### Issue 4: Real-world grounding of probes (No6d W2 + C1)

**Currently in paper:** Introduction has an added broader-applicability paragraph (medical imaging, autonomous systems, etc.). But no explicit mapping of each probe family to specific real-world failure modes.

**Rebuttal commitment:** "We will clarify these points in the updated version."

**Still needs:** Add a short paragraph to Dataset or Framework section:
> "Our probes correspond to real-world failure modes: visual perturbations and selective blur represent degraded PDF rendering, OCR loss, cropping, and low-resolution inputs; caption bias represents incorrect figure-caption retrieval in document processing or multimodal RAG; false-premise probes represent erroneous assumptions introduced by users or propagated between agents; page-context conditions represent models processing figures within complete scientific documents."

**Where to add:** `framework.tex` or `dataset.tex` (near where probe types are introduced).

---

## P2 · Important single-reviewer concerns

### Issue 5: Chart-type coverage (h9tb W1)

**Currently in paper (`dataset.tex`):**
- Now includes: "We selected bar charts, line plots, and pie charts because they were the most prevalent visualization types in the collected corpus."
- Broad-applicability paragraph in intro.

**Status:** Partially addressed. Reviewer h9tb ultimately raised their score to Conference (4), so this is not blocking.

**Optional enhancement:**
- Report the actual chart-type distribution numbers (e.g., "X% bar / Y% line / Z% pie in our arXiv corpus").
- Explicitly acknowledge scatter/heatmap as future work in Limitations.

**Where to update:** Dataset section or Limitations.

### Issue 6: arXiv sampling and benchmark coverage (LhRb C1)

**Currently in paper:** No dedicated discussion of arXiv sampling methodology and coverage implications.

**Still needs:**
- Add a paragraph to Dataset or Limitations explaining:
  - Sampling method (e.g., stratified by chart type)
  - What the sample represents (recent English-language ML/NLP arXiv)
  - What it doesn't (other disciplines, other figure conventions, older papers)

**Where to add:** Limitations section or extend `dataset.tex`.

### Issue 7: Model version drift (LhRb C2)

**Currently in paper:** Model identifiers listed in `appendix_reproducibility.tex` and `evaluation_appendix.tex`, but no discussion of version drift for API models.

**Still needs:** Add a short discussion in reproducibility appendix:
- Note that API model versions may change over time.
- Report exact model identifiers, API versions, deployment names, dates of inference.
- Note that Temperature=0 + fixed seed reduce run-level variability but do not prevent provider-side model updates.
- Commit to releasing prompts + model outputs so future re-runs can quantify drift.

**Where to add:** `appendix_reproducibility.tex`.

### Issue 8: A-R-I as necessary + relatively complete (LhRb C3)

**Currently in paper:** The added paragraph in framework says A-R-I focuses on 3 complementary dimensions but doesn't argue necessity strongly.

**Still needs:**
- Argue each axis captures a distinct deployment risk (already partially there: "admittance failures produce silent fabrication, resistance failures allow context manipulation, and inductance failures reflect an inability to reason from partial evidence").
- Point at empirical dissociation between axes (rank inversions, cross-dim correlations Table).

**Where to update:** Framework §3.4 (folds into Issue 1 above).

---

## P3 · Polish

### Issue 9: Inexist perception-vs-instruction-tuning confound (h9tb W2)

**Currently in paper (`analysis.tex`):**
- Analysis paragraph says: "These failures may arise from instruction-following behaviour rather than deficient visual perception, given the strong perception performance of leading models (MQM > 90). However, our benchmark does not disentangle these factors, which we leave for future work."

**Status:** Addressed. Reviewer h9tb went to Conference (4).

**Optional enhancement:** Small perception-vs-instruction dissociation table or footnote.

### Issue 10: Llama 4 naming consistency (h9tb C1)

**Currently in paper:** Need to grep for "Llama 4" variants (Llama-4, LLaMA 4, Llama 4 Maverick, etc.).

**Plan:** Systematic grep + replace with "Llama 4 Maverick" everywhere in text, tables, and captions.

**Where to update:** All `.tex` files.

---

## Cleanup tasks

- Remove all `\todo{}` markers left in the paper (e.g., in `results.tex`, `analysis.tex`).
- Verify Figure 4 is referenced (SE noted it wasn't).
- Fix minor typos flagged in TODOs.
- Ensure the arXiv link footnote for SciFig-Eval is anonymised or removed for the resubmission (paper is under review again).

---

## Suggested execution order

1. **P0 bibliography** (blocks everything else — do first)
2. **P1 Issue 2** (human annotation paragraph — largest missing chunk, easiest to add)
3. **P1 Issue 4** (real-world grounding paragraph — short, easy)
4. **P1 Issue 1** (A-R-I framing — most consequential rewrite)
5. **P1 Issue 3** (item-level GPT-4o vs human agreement — needs new annotation work)
6. **P2 items 5–8** (single-reviewer additions)
7. **P3 items 9–10** (polish + cleanup)
