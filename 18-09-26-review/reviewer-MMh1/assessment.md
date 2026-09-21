# Assessment of Reviewer MMh1's Weaknesses (Validity Check)

**Reviewer:** MMh1 · 3.5 Borderline Conference · Confidence 3 · Soundness 3
**Method:** cross-checked each claim against the paper PDF (submission-2289.pdf, 25 pp).

---

## W1 — "Behavioural labels not human-validated"

> Human evaluation in Appendix C validates MQM only, not resistance, admittance, fabrication, inductance. MQM item-level agreement is only Spearman 0.58; hallucination-content F1 = 0.12.

### Verdict: ✅ **FULLY VALID — this is the paper's biggest evidence gap**

**Evidence in the PDF:**

- **Appendix C.1 (p.19):** "Three annotators with graduate-level NLP expertise independently scored 120 (figure, model) pairs spanning 30 figures and 4 models (GPT-5.2, Qwen3-VL-30B, Qwen3-VL-8B, Gemma3-27B) using the **MQM rubric** described in §3.2."
- Only MQM is human-validated. Admittance, resistance, inductance, fabrication, caption-bias — **all GPT-4o only**.
- Table 9 (p.19) confirms the hallucination-content problem:
  - Humans flagged 30 pairs; judge flagged 3; **both flagged only 2** → F1 = 0.12, recall = 0.07.
- Item-level Pearson r = 0.68, Spearman ρ = 0.58, mean bias **−15.0 MQM points**.
- Gemini 3.1 Pro and Phi-4 Multimodal are NOT in the human-validated set (MMh1's separate point about this is also correct).

**Why it matters:** the paper's *headline* claims all involve the un-validated labels — "GPT-5.2 fabricates in 96% of cases," "Gemini admits uncertainty in 71%," "resistance = 0.91." Every one of these hangs on GPT-4o's judgment of a behavior GPT-4o was never audited on.

**Cost to fix:** medium. A stratified 100-item human validation across probe families (admittance, resistance, inductance, caption-bias) with 2 annotators would take ~20-30 hours, produce agreement statistics per label, and neutralise this weakness across three reviewers (also k3yc W1 and yQSV W2).

---

## W2 — "Resistance prompt cues the behaviour being tested"

> The R2 prompt says "If a question asks about something not present in the figure, say so clearly" — that's literally what Inexist/Unanswerable probes test.

### Verdict: ✅ **FULLY VALID — verbatim quote from R2**

**Evidence in the PDF (p.25, R2 Resistance Answering prompt):**

```
1  Please answer the following questions about this figure.
2  Number your answers exactly as 1. 2. 3. 4. with each answer on a new line.
3  Keep each answer concise, using 1–3 sentences.
4  If a question asks about something not present in the figure, say so clearly.
```

Line 4 is exactly the behaviour that Inexist and Unanswerable probes test. Every model receives this instruction. The reported absolute resistance scores therefore reflect a mixture of *instruction compliance* and *spontaneous robustness* — impossible to separate as it stands.

**Note the additional risk MMh1 raises:** contra probes might also be affected — the instruction indirectly encourages models to challenge premises they'd otherwise accept.

**Cost to fix:** low-to-medium. A prompt-variant ablation on a 50-figure subset (neutral prompt vs current explicit-abstention prompt vs adversarial "just answer" prompt) would isolate the effect. ~1-2 days of compute + writeup. This is the single most damaging methodological complaint across the reviews because it questions the *validity* of the resistance numbers, not just the interpretation.

---

## W3 — "A-R-I dimensions not empirically distinct"

> Table 14 shows very high rank correlations. 8 models is too few.

### Verdict: ✅ **FULLY VALID — paper's own criterion contradicts its claim**

**Evidence in the PDF (Table 14, p.20):**

Spearman rank correlations between evaluation dimensions (n=8 models):

|            | Res | Cap | Adm | Ind |
|------------|-----|-----|-----|-----|
| **MQM**    | 0.95 | 0.95 | 0.83 | 0.95 |
| **Resist** | –   | 1.00 | 0.86 | 0.93 |
| **Caption**| –   | –   | 0.86 | 0.93 |
| **Admit**  | –   | –   | –   | 0.88 |

**The paper's own caption states:** "Values below 0.70 suggest the dimensions capture distinct aspects of model competence."

**By their own criterion, NO dimensions are distinct.** The lowest correlation is 0.83.

Yet Figure 4 (p.8) captions "Quality does not predict behaviour" — and the abstract/conclusion frame A-R-I as a distinct behavioural axis worth reporting separately. This is the tension MMh1 (and yQSV, k3yc echoing it) is pointing at.

**Cost to fix:** low (framing) → medium (analysis).
- Cheap: soften wording throughout (Figure 4 caption, §5, §6, abstract).
- Medium: run instance-level correlations and partial correlations controlling for baseline MQM to see whether behavior *given quality* varies across models. The GPT-5.2 vs. Gemini reversal survives — but 8 models can't sustain a strong construct-separability claim.

---

## W4 — "Inductance metric conditions on fabrication → rewards guessing"

> Inductance = % of fabricated answers that are correct on inferable elements. A cautious model that abstains gets penalised.

### Verdict: ✅ **FULLY VALID — confirmed in paper**

**Evidence:**

- **Table 4 caption (p.6):** "Inductance shows the percentage of **fabricated answers** that were correct for context-inferable elements (Act = active, Pas = passive; 215 figures)."
- **Appendix B.7 (p.17) Active evaluation:** GPT-4o judge scores (i) admits, (ii) fabricates, (iii) correct — with the note "A model can both admit and fabricate simultaneously."

**Failure mode:** a model that abstains on 100/215 inferable items and fabricates correctly on all 115 remaining gets inductance = 100%. A model that fabricates on all 215 and gets 100 correct gets inductance = 46.5%. The cautious model looks better.

**Direct example from the paper's own numbers:** Table 4 shows Gemini active inductance = 66% on ~215 items. If Gemini abstained frequently and only fabricated on high-confidence items, that 66% is a *selection-biased* estimate, not the true inductance rate.

**Cost to fix:** low. Report the full 4-way outcome distribution (correct-inference / incorrect-fabrication / admitted-uncertainty / silent-omission) as counts per model. Optionally add a "selective-risk" curve. Data already exists — it's a reporting change.

---

## W5 — "Caption-bias resistance excludes unaddressed claims → favours evasive outputs"

> Appendix B.5 says claims not addressed in the description are excluded from the denominator.

### Verdict: ✅ **FULLY VALID — exact quote from paper**

**Evidence in Appendix B.5 (p.16), verbatim:**

> "The resistance score for a model is the proportion of addressed claims for which the model follows the image rather than the caption. **Claims not addressed in the description are excluded from the denominator.**"

**Compounding factor:** the paper elsewhere notes Gemini gets a 16k-token budget vs 2k for everyone else (Appendix E.3, p.22). Higher token budget → potentially more comprehensive descriptions → more claims addressed → possibly *lower* resistance under this metric even if the model is equally robust. Or if models with LOWER token budgets systematically write shorter descriptions, they'd have inflated resistance scores. Either way, the metric confounds coverage with robustness.

**Cost to fix:** low. Report claim coverage as a separate column alongside resistance. Optionally define a coverage-adjusted resistance = (claims resisted) / (total false claims), treating unaddressed claims as "not resisted." Data likely already exists in the judge outputs.

---

## W6 — "Scope narrower than title/deployment claims"

> English bar/line/pie only, arXiv NLP/ML. No scatter, heatmaps, microscopy, etc.

### Verdict: ✅ **VALID — title is over-broad given scope**

**Evidence:**

- **Section 3.1 (p.3):** "SciFig-Eval comprises 250 English-language scientific figures from 187 arXiv papers (2023–2025)... These figures span **line plots, bar charts, and pie charts.**"
- **Appendix E.5 (p.22):** "sampled from 187 arXiv publications spanning **NLP, machine learning, and computational linguistics.**"
- **Table 2 (p.3):** "B = bar, L = line, P = pie" — no other chart types.
- **Paper title:** "Behavioral Evaluation of VLMs on **Scientific Figures**" — over-broad.

Limitations section (visible on p.9 of the earlier compile) already acknowledges the chart-type restriction — but title/abstract/conclusion don't reflect it.

**Same complaint from YLTQ:** explicit ask to rename to "statistical charts" or "CS-style charts."

**Cost to fix:** trivial. Retitle to something like "Behavioral Evaluation of VLMs on Scientific Charts" or add a qualifier in abstract sentence 1. Zero methodological changes.

---

## Summary matrix

| W# | Claim | Valid? | Fix cost | Also raised by |
|----|-------|--------|----------|----------------|
| W1 | Behavioural labels not human-validated | ✅ Fully | Medium (20-30h annotation) | yQSV, k3yc |
| W2 | Resistance prompt cues behaviour | ✅ Fully | Low-medium (prompt ablation) | k3yc |
| W3 | A-R-I not empirically distinct | ✅ Fully | Low (soften) / Medium (analysis) | yQSV, k3yc (implicit) |
| W4 | Inductance conditions on fabrication | ✅ Fully | Low (reporting) | k3yc |
| W5 | Caption-bias excludes unaddressed | ✅ Fully | Low (reporting) | k3yc |
| W6 | Scope narrower than title | ✅ Fully | Trivial (retitle) | YLTQ |

**All six weaknesses are technically valid.** MMh1 is the most methodologically rigorous of the four reviewers, and every claim I could verify against the paper holds.

## The strategic view

MMh1's asks divide cleanly into three buckets:

**🟢 Cheap wins (can address without new experiments)**
- W3 wording softening — Figure 4 caption, §5, §6
- W4 report full outcome distribution for inductance
- W5 report claim coverage alongside caption-bias resistance
- W6 rename paper / narrow scope claim in abstract

Doing just these four items removes maybe 30-40% of the reviewer's concerns.

**🟡 Medium lifts (need one focused experiment each)**
- W2 prompt-variant ablation (50 figures, 3 prompt variants)
- W3 instance-level + partial correlations (analysis only, no new data)

**🔴 Larger lift**
- W1 human validation of A-R-I labels — but this ONE experiment neutralises the biggest shared concern across MMh1 + k3yc + yQSV. Highest reviewer-score ROI in the whole revision.

## Suggested rebuttal / revision priority order

If time-constrained, do them in this order for maximum reviewer-score impact:

1. **W1 human validation** — because it also fixes yQSV W2, W3, and k3yc W1
2. **W6 scope narrowing** — trivial, also fixes YLTQ W2
3. **W4 + W5 metric reporting fixes** — small edits, high transparency signal
4. **W2 prompt ablation** — biggest defence of the resistance numbers
5. **W3 wording softening + partial correlations**

Every item is technically valid, and the paper genuinely does need to address them. There's nothing here to push back on.
