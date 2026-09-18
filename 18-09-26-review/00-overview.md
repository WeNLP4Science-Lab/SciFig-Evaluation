# ACL ARR August 2026 — Review Summary

**Submission:** #2289 · *How Do VLMs Behave When Blind or Misled? Behavioural Evaluation of VLMs on Scientific Figures*
**Preferred venue:** EACL
**Round:** Resubmission (previous forum: `/forum?id=AGJdWaFn1l`)

## Scores at a glance

| Reviewer | Overall | Soundness | Excitement | Confidence | Datasets | Software | Reproducibility |
|---|---|---|---|---|---|---|---|
| **MMh1** | 3.5 (Borderline Conference) | 3 | 4 | 3 | 4 | 4 | 4 |
| **YLTQ** | 3.0 (Findings) | 3 | 4 | 4 | 3 | 3 | 3 |
| **yQSV** | 2.5 (Borderline Findings) | 3 | 2.5 | 4 | 3 | 2 | 3 |
| **k3yc** | 3.0 (Findings) | 3 | 4 | 4 | 4 | 4 | 4 |

**Aggregate signal:** two Findings (3.0), one Borderline Conference (3.5), one Borderline Findings (2.5) → **overall trajectory = Findings, with room to push to Main track** if the strongest weaknesses are addressed.

## Recurring themes across reviewers

Ranked by how many reviewers raised them:

### 🔴 Raised by 3–4 reviewers — must-address
1. **Behavioural labels not human-validated** (MMh1, yQSV, k3yc)
   Only MQM has human agreement numbers; A-R-I labels (admittance / resistance / inductance / fabrication) rely entirely on GPT-4o judgments. Item-level MQM agreement is only Spearman 0.58; hallucination-content F1 = 0.12.
2. **Prompts cue the behaviour being measured** (MMh1, k3yc)
   The resistance answering prompt explicitly says "If a question asks about something not present in the figure, say so clearly" — that's the exact behaviour the probes test. Absolute scores may reflect compliance more than spontaneous robustness.
3. **Inductance metric conditions on fabrication → rewards guessing** (MMh1, k3yc)
   Correctness computed only over fabricated answers; excludes abstentions. A cautious model gets penalised.
4. **Caption-bias resistance excludes unaddressed claims** (MMh1, k3yc)
   Denominator is only claims the description actually addresses. Terse or evasive models get inflated resistance scores.
5. **Scope narrower than "scientific figures" implies** (MMh1, YLTQ)
   3 chart types (bar, line, pie), English, NLP/ML arXiv only. Title, abstract, and conclusion should say "chart-focused" or narrow the domain explicitly.
6. **A-R-I dimensions not shown to be empirically distinct** (MMh1)
   Table 14 rank correlations across dimensions are high. Only 8 models — a few reversals don't prove construct separability.

### 🟠 Raised by 2 reviewers
7. **Numerical inconsistencies in tables/captions** (yQSV, k3yc)
   - Figure 3 caption says Gemini admits 90% but Table 4 says 71% (active) / 59% (passive).
   - Section 4.3 claim "no other model exceeds 53.4% in any reasoning category" contradicted by Table 4 (Qwen-235B: 65.2% on counting, 63.7% on computation).
   - In-paper 2–5-point drop claim (§4.2 + Table 3) uses different subsets; needs matched-subset comparison.
8. **CHART-NOISe citation attribution wrong** (yQSV — explicit; k3yc adjacent concerns about missing closest competitors)
   CHART-NOISe is Shin et al. "Losing the Plot", NOT Mahbub et al. "The Perils of Chart Deception".
9. **Dataset scale not increased** (YLTQ, yQSV)
   Response mainly argues via 34K+ evaluation instances (repeated views of same 250 figures) rather than base-figure diversity.

### 🟡 Raised by 1 reviewer — still worth addressing
10. **Missing overlap with ChartHal + CHART-NOISe in Table 1** (yQSV)
11. **Admittance judge marks true for "ANY uncertainty" AND allows co-fabrication** (yQSV)
    So a model gets admittance credit while still supplying an unsupported answer. Need a stricter "admits without also fabricating" metric.
12. **"Quality does not predict behaviour" wording too strong** (yQSV, k3yc echo)
    Table 14 shows fairly high dimension correlations. Soften to "similar quality scores can conceal differences in particular behaviours."
13. **Appendix pipeline figures (Figs 6-11) too small / AI-generated look** (YLTQ, PC comment)
14. **Reproducibility wording bug** (k3yc)
    Appendix E: "all other models (open-weight)" via OpenRouter — but Gemini 3.1 Pro is in that group and isn't open-weight.
15. **Reference formatting** (YLTQ)
    arXiv entries should be `@misc` not `@article`; check for peer-reviewed versions to replace preprints.
16. **Dataset/code not available at review time** (YLTQ, yQSV)
17. **Human MQM validation covers only 4 models, omits Gemini/Phi-4** (MMh1)
18. **Speculative causal claims** (MMh1)
    Claims about RLHF pressure / training artifacts / deployment risk stated as facts rather than hypotheses.
19. **Bootstrap independence — multiple questions from same figure not independent** (MMh1)
20. **Gemini token budget disparity** (MMh1)
    Gemini uses 16k max tokens vs 2k default for others. Could affect completeness / abstention behavior.

### 🟢 Editorial (PC comment, 31 Aug 2026)
- **Figure font size** too small in multiple figures (Figs 2, 5–11). Not desk-rejected but must be fixed for camera-ready or resubmission.

## Reviewer-specific files

- `reviewer-MMh1.md` — most rigorous methodological review; borderline conference (3.5)
- `reviewer-YLTQ.md` — high confidence, focuses on scope claims and reproducibility; Findings (3.0)
- `reviewer-yQSV.md` — most critical; focuses on numerical inconsistencies, competitor citations, metric limitations; Borderline Findings (2.5)
- `reviewer-k3yc.md` — high confidence, echoes MMh1's methodological concerns; Findings (3.0)
- `pc-comment.md` — Program Chairs' figure-size heads-up
