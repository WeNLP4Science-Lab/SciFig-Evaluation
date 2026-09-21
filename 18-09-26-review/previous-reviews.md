# Previous Round — May 2026 Submission (#14568)

**Outcome:** Desk-rejected 30 Jul 2026 by Program Chairs for "hallucinated references."
The submission had already collected three reviews before the desk-reject; we can and should
learn from them because current-round reviewers are surfacing the same concerns.

## Previous reviewers & scores

| Reviewer | Overall | Soundness | Excitement | Confidence |
|---|---|---|---|---|
| h9tb | 4 (Conference) | 3 | 3.5 | 3 |
| No6d | 3 (Findings) | 3 | 2 | 3 |
| LhRb | 3 (Findings) → then Soundness raised to 3.5 post-rebuttal | 3.5 | 3 | 4 |

## Themes carried over into the current round

The behavioral-label human-validation concern that current-round MMh1 raises as W1
was **also raised by two of three previous reviewers** — and was NOT resolved before
the paper was desk-rejected for an unrelated reason. It is a **repeat concern**, which
matters strategically: reviewers this round will be checking whether we actually
addressed it, not just discussed it.

---

# Focused point: Behavioral labels lack human validation

## Current-round quote (Reviewer MMh1)

> The behavioral evaluation relies almost entirely on GPT-4o without sufficient human
> validation. GPT-4o generates many questions and probes, judges MQM descriptions,
> scores resistance, and judges selective-blur outcomes. The human evaluation in
> Appendix C validates MQM only, not the core behavioral labels: resistance,
> admittance, fabrication, and inductance. Moreover, the MQM analysis reports a
> substantial mean automated-versus-human bias and low F1 for hallucinated content
> detection. Since the paper's central claims concern fabrication and epistemic
> reliability, the authors should provide human annotation for a stratified sample of
> each behavioral probe family, report agreement for each behavioral label, and
> evaluate all central results with an independent judge rather than only selected
> capability tasks or a small probe-design ablation.

## Previous-round equivalents

### Reviewer No6d (Jun 30, 2026) — Weakness 4

> Although the authors include some human validation, the main evaluation still relies
> heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of
> uncertainty and resistance to misleading premises, the paper should report direct
> agreement between GPT-4o and humans, ideally at the item level. This is also a
> reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact
> judge version and robustness to a current judge model should be clarified.

### Reviewer LhRb (Jun 24, 2026) — Weakness (main reservation)

> My main reservation is about scale and dependence on automatic evaluation. 250
> figures is still limited for the broad space of scientific figures. GPT-4o is used
> quite heavily in probe generation and judging. The validation helps, but I would
> still have liked to see broader human evaluation or more diverse figure sources.

## What the authors said in reply last round

### To No6d
> Indeed, our work reported the correlation (agreement) between GPT-4o and humans on
> 120 MQM items (see Section 3 and Appendix A.1). Three annotators achieved
> Krippendorff's α = 0.91 (inter-annotator agreement), and the correlation between
> GPT-4o and humans was Spearman's ρ = 0.80 in terms of model-level ranking. We have
> also computed item-level correlation between Mistral Large 3 and humans over 344
> capability items, where Spearman's ρ = 0.87. We will add the item-level correlation
> between GPT-4o and humans in the updated version.
>
> Regarding reproducibility, GPT-4o still remains accessible through the OpenAI API.

### To LhRb
> We note that GPT-4o was involved in dataset construction (perception, reasoning, and
> behavioural probes) **with human-in-the-loop oversight to ensure reliability,
> efficiency, and correctness**. GPT-generated descriptions, capability questions, and
> selective-blur targets were carefully reviewed and corrected by human annotators
> whenever necessary. Details are provided in Section 3, Appendices B.3, B.6, F.
>
> Regarding GPT-4o as a judge, this is a common practice in NLP as a surrogate for
> costly human evaluation. We evaluated GPT-4o against humans on 120 MQM items (see
> Section 3, Appendix A.1), and found positive correlation (Spearman ρ=0.80) in terms
> of model ranking, suggesting the reliability of GPT-4o as a judge.

## What actually got added in the resubmission

Cross-checked against the current PDF (Appendix C.1, C.2, D):

| Ask | Delivered? |
|---|---|
| Item-level GPT-4o vs human on MQM | ✅ Yes — Pearson r=0.68, Spearman ρ=0.58, mean bias −15.0 MQM pts, per-model bias -9.4 to -25.6 |
| Error-type taxonomy agreement (Table 9) | ✅ Yes — but **Hallucinated Content F1 = 0.12, recall = 0.07** (judge caught 2/30) |
| Cross-judge ablation (Mistral Large 3) on **capability** tasks | ✅ Yes — Table 10, ρ = 1.000 model-level ranking preserved |
| Cross-judge ablation on **resistance / admittance / inductance** | ❌ Not done |
| Human validation on **resistance / admittance / inductance / caption-bias** labels | ❌ Not done |
| Item-level GPT-4o vs human on behavioural labels | ❌ Not done |
| Mistral Large 3 comparison on MQM (item-level) | ✅ Yes — ρ=0.65, r=0.80 on 120 pairs (Appendix C.1) |

## Assessment: this concern is technically UNRESOLVED

The previous responses did three things:
1. Added item-level MQM agreement (revealed a real problem — high bias, low hallucination F1)
2. Added a Mistral Large 3 cross-judge on **capability** questions only
3. Argued that GPT-4o was reliable *for ranking* (aggregate) — not for per-item behavioural judgments

**Neither reviewer had asked for capability-question cross-judging.** No6d and LhRb both
asked for direct human agreement on the behavioural labels themselves. That was not
provided last round, and it has not been provided this round either.

MMh1's W1 is essentially No6d's W4 with the exact same weakness restated one round
later. The reviewer is correctly noticing that the additions of item-level MQM
agreement and the Mistral capability cross-judge do NOT address the core ask, which is
human validation of admittance / resistance / inductance / fabrication labels.

## Strategic implication

This is now a **second-round repeat concern**. If we submit again without addressing
it directly, a third-round reviewer will (a) find the same gap and (b) note that
the authors have been asked and not responded to the actual ask. That looks worse
than the original weakness.

**The only fix that closes this out is: run a stratified human validation on each
behavioural probe family, report agreement statistics per label, add to Appendix C.**

Rough scope:
- Sample ~30–50 (figure, model, probe) triples per family across
  {admittance, resistance, inductance, caption-bias}. Say 4 families × 40 = 160 items.
- 2 annotators each (matching current MQM annotation protocol from Appendix C.1).
- Report Krippendorff's α per label, Cohen's κ per (judge, human) pair, item-level
  binary F1 for the fabrication label (since that's where MQM validation was
  weakest).
- Roughly 20–30 human-hours if annotators use the review dashboard already built.

Doing this closes MMh1 W1, k3yc W1, yQSV W2, and retroactively No6d W4 + LhRb's
reservation. It is the single highest-ROI experiment for the next revision.

## What NOT to argue

Arguments that failed last round and will fail again:
- ❌ "GPT-4o as judge is common practice in NLP" — reviewers this round agree, but
  ask specifically because the behaviours in question (uncertainty acknowledgment,
  fabrication detection) are known LLM-judge blind spots and the MQM validation
  already showed poor hallucination-content F1.
- ❌ "We have human-in-the-loop for probe *construction*" — reviewers this round have
  read the paper carefully enough to know construction ≠ label-judgment.
- ❌ "Model-level rankings are stable under cross-judging" — reviewers accept this
  for the capability numbers but say the behavioural labels weren't cross-judged.

## What TO argue if we can't run the experiment before deadline

If time-constrained and we cannot add human validation before the response deadline:
- **Acknowledge the concern directly** — say "reviewer is correct that current
  validation does not cover the behavioural labels."
- Commit in writing to adding it for camera-ready, name a target sample size.
- Meanwhile add a **partial** cross-judge: run Mistral Large 3 as an ADDITIONAL
  behavioural judge on a subset (say, 100 admittance + 100 resistance triples) —
  cheaper than human validation, still provides an independent-judge check, and
  matches the reviewer's fallback wording "evaluate all central results with an
  independent judge rather than only selected capability tasks."

This won't fully satisfy MMh1 but it directly addresses "or a small probe-design
ablation" — showing we heard the criticism and responded with an actual new
experiment even if human validation is deferred.
