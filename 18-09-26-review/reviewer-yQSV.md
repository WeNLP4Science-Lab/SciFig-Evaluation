# Reviewer yQSV

**Overall:** 2.5 (Borderline Findings)
**Soundness:** 3 · **Excitement:** 2.5 · **Confidence:** 4
**Reproducibility:** 3 · **Datasets:** 3 · **Software:** 2
**Posted:** 7 Sept 2026 (modified 15 Sept 2026, 15:28)

> This is the most critical reviewer — lowest overall + lowest excitement + lowest software score. Also caught real numerical inconsistencies. Fixing their specific issues has highest marginal impact.

## Paper Summary (their words)

> The paper introduces SciFig-Eval, a benchmark for evaluating VLM understanding of scientific charts and their behaviour under missing or misleading visual evidence. It contains 250 figures across three chart types with expert descriptions and 1,000 reasoning questions. Its Admittance–Resistance–Inductance framework evaluates uncertainty acknowledgement, resistance to misleading context and inference from recoverable information. Experiments across VLMs show that similar description-quality and reasoning scores can coexist with substantial differences in uncertainty handling. The revised submission adds human–judge agreement analyses and alternative-model checks to assess evaluation reliability.

## Strengths (summarised)

- Revision improved evaluation transparency (human-agreement analyses, alternative-model checks)
- Recoverability distinction is a useful benchmark contribution — separates "inferable" from "cannot be recovered"
- Empirical comparison shows behavioural evaluation matters (GPT-5.2 vs Gemini: 8% vs 71% active admittance)
- Active/passive analysis reveals task-dependent uncertainty handling

## Weaknesses

### W1 — Novelty vs. closest competitors under-established
- **ChartHal and CHART-NOISe directly overlap** with false-premise and degraded-evidence evaluations.
- Their **omission from Table 1** makes the comparison less informative.
- **Ask:** clearly identify what the controlled recoverability design adds beyond existing benchmarks.

### W2 — Prompt for admittance doesn't establish appropriate handling
- Judge marks admittance as true for "ANY uncertainty" AND explicitly allows a response to "both admit AND fabricate."
- A model can therefore receive admittance credit while still supplying an unsupported answer.
- **Ask:** report the proportion that acknowledges uncertainty **without supplying unsupported specifics**.

### W3 — Weak human agreement on some MQM error categories
- Appendix C.1: for "Hallucinated Content," judge identifies only **2 of 30** human-flagged cases.
- **Ask:** clarify whether the remaining 28 cases receive penalties under other categories or are missed entirely. Establishes how disagreement affects final MQM scores.

### W4 — Dataset scale not resolved by evaluation count
- Benchmark covers 250 source figures, 3 chart types. The reported 34,000 evaluations include repeated testing across models and operations.
- Demonstrates experimental effort but does not expand diversity of visual evidence covered.

## Comments / suggestions / typos — SPECIFIC AND ACTIONABLE

### Numerical inconsistencies (must fix)

1. **Figure 3 caption vs Table 4 mismatch.**
   Fig 3 caption states Gemini acknowledges uncertainty 90% of the time.
   Table 4 reports 71% active, 59% passive.
   Reconcile.

2. **Section 4.3 claim contradicts Table 4.**
   §4.3 claims "none of the remaining six models exceeds 53.4% in any reasoning category."
   Table 4 shows **Qwen-235B: 65.2% on counting, 63.7% on computation.**
   Fix the claim.

3. **Section 4.2 + Table 3 in-paper drop.**
   Claimed 2–5-point page-context drop, but displayed GPT-5.2 scores are 91.6 (Base) vs 77.8 (InPap).
   These columns use different evaluation subsets.
   **Need matched-subset comparison** to support the stated drop.

### Wording softening

4. **Figure caption "Quality does not predict behaviour"** is stronger than the evidence supports.
   Table 14 shows high correlations between MQM and behavioural dimensions.
   More precise: *"similar quality scores can conceal differences in particular behaviours."*

5. **Section 5 heading "Caption dependency as training artifact, not capability limitation"** — soften. Limitations section already acknowledges this uncertainty.

### Citation error (must fix)

6. **CHART-NOISe attribution wrong.**
   - Currently attributed to Mahbub et al. (whose paper is "The Perils of Chart Deception").
   - **CHART-NOISe is Shin et al., "Losing the Plot: How VLM responses degrade on imperfect charts."**
   - Fix both the attribution AND add the correct citation.

## What this reviewer would most reward in a revision

Concrete fixable items (5 of 6 are pure edits — high ROI):

1. **Fix numerical inconsistencies** #1, #2, #3 (fastest wins)
2. **Fix CHART-NOISe citation** — Shin et al., not Mahbub et al.
3. **Add ChartHal + CHART-NOISe to Table 1**
4. **Soften "quality does not predict behaviour"** in captions and headings
5. **Add stricter "admits without fabricating" metric** alongside admittance
6. **Clarify hallucinated-content case handling** (are the 28 missed cases penalised elsewhere?)
