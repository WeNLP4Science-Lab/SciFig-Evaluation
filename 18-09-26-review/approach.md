# Rebuttal Approach — Prof. Wei Zhao's Strategy

Reference document for how to structure and tone our rebuttal responses.
Derived from Prof. Zhao's guidance and the pattern that lifted the May submission
from 2.5 average to 3.2–3.3 across the panel.

---

## Core rebuttal strategies (Prof. Zhao)

Four moves. Every criticism gets classified into one of these:

1. **Defend our approach.** Explain why we did what we did, especially when the
   reviewer misunderstood. Cite specific sections, appendices, tables, or numbers.

2. **Acknowledge the reviewer.** Frame the issue as a limitation or explain why it
   is out of scope for our research question. Don't over-concede or surrender the
   contribution.

3. **Offer additional results.** Only if doable in 2–3 hours. During rebuttal,
   allowed additions are minor add-ons to existing experiments (new ablations,
   different hyperparameter settings, comparison with a different baseline). New
   human studies at scale are NOT allowed in the rebuttal window — defer those to
   camera-ready.

4. **Commit to new analyses / additions.** Make narrow, credible promises for the
   updated version. Specific, not vague ("we will add X to Appendix Y with per-model
   agreement statistics" rather than "we plan to improve validation").

---

## The pattern that worked in May

Extracted from the successful May rebuttal (2.5 → 3.2 / 3.3 across the panel):

1. **Answer each concern directly.** Quote or restate the reviewer's exact concern,
   then respond immediately. No preamble, no hedge.

2. **Correct misunderstandings with evidence.** Don't just disagree. Cite concrete
   results, sections, appendices, experimental counts, reliability statistics.

3. **Reframe apparently weak numbers.** "250 figures" becomes "34,000+ evaluation
   setups across 8 models via 5 augmentation strategies, backed by 600+ annotation
   hours." Show scale by aggregating what's already in the paper.

4. **Defend novelty precisely.** Acknowledge that individual techniques may exist,
   then name what is genuinely new — the adaptation, controlled combination,
   evaluation setting, and connection to the research question.

5. **Protect the paper's scope.** Acknowledge broader dimensions without accepting
   that the paper must cover all of them. Explain why the chosen scope follows
   naturally from the central research question.

6. **Connect abstractions to realistic use cases.** Map probes to real-world failure
   modes (blur → PDF degradation / OCR loss; caption bias → retrieval errors,
   multimodal RAG; false premises → agent-propagated assumptions).

7. **Use additional analyses strategically.** New results are introduced only when
   they directly remove uncertainty — e.g., item-level agreement statistics,
   reliability numbers, cross-judge checks.

8. **Make narrow, credible commitments.** Promise specific additions or clarifications
   in the revision, not vague future work.

9. **Concede without surrendering the contribution.** Genuine limitations are
   acknowledged, but carefully separated from threats to validity.

10. **Follow up politely.** Asking whether concerns were resolved after posting the
    response prompted at least one reviewer to explicitly state "most concerns had
    been addressed."

---

## Tone

- **Respectful but firm.**
- **Heavily quantified.** Numbers and section references anchor every claim.
- Centered on **"why this design is sufficient for our research question"** rather
  than "we did everything the reviewer might want."

---

## Classification checklist — apply to every weakness

For each criticism, pick one:

| Category | When to use | What the response looks like |
|---|---|---|
| **A. Reviewer misunderstanding** | The reviewer misread what we did, missed a section, or attributed a design choice we didn't make | Clarify + cite the exact section/table where the paper already addresses it |
| **B. Valid but non-fatal limitation** | The reviewer is right, but it doesn't threaten our central claim | Acknowledge and delimit. Explain scope. Don't over-concede |
| **C. Answerable in 2–3 hours** | A small ablation, new statistic, or targeted analysis on existing data would remove the doubt | Run it, report the result inline. This must be a minor add-on, not a new study |
| **D. Revision-level concern** | Requires substantive new work or new material for camera-ready | Make a concrete commitment with named scope |

---

## Hard rule from the May desk-reject lesson

The May submission was ultimately desk-rejected for hallucinated references — not
by the reviewers, by the Program Chairs. For every response and every revision:
**verify every citation and avoid introducing any unverified claim or reference,
regardless of how persuasive it sounds.**

If a response mentions a specific paper, prior benchmark, or external number, we
cross-check that it exists and is what we say it is BEFORE posting.

---

## Response-writing template per criticism

Prof. Zhao's preferred structure for working through each weakness:

1. **Which point are we answering** — one-line summary
2. **Quote the reviewer's exact criticism** — verbatim
3. **Our interpretation** — what the reviewer is really asking / assuming
4. **Response direction** — which of A/B/C/D above, and what evidence we cite

Then draft the actual text under whatever word/character limit applies.

---

## Constraints for this round

- **Max 2000 characters per reviewer response**, not per weakness. MMh1 has 6
  weaknesses; we need tight budgeting.
- Rebuttal-window experiments must be minor add-ons only. Human validation of
  behavioural labels is a camera-ready commitment, not a rebuttal-time deliverable.
- Prompt-variant ablation IS an allowed minor add-on if we choose to run it.
