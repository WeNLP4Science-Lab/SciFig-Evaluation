# Reviewer k3yc

**Overall:** 3.0 (Findings)
**Soundness:** 3 · **Excitement:** 4 · **Confidence:** 4
**Reproducibility:** 4 · **Datasets:** 4 · **Software:** 4
**Posted:** 7 Sept 2026 (modified 15 Sept 2026, 15:28)

## Paper Summary (their words)

> This paper introduces SCIFIG-EVAL, a benchmark for evaluating VLMs on scientific figures not only for perception and reasoning, but also for how they behave when visual evidence is missing or misleading. The benchmark includes selective blur, false-premise and caption-bias stress tests, organized under the A-R-I framework: admittance, resistance and inductance. One of the main findings is that models with similar standard perception/reasoning performance can behave quite differently under uncertainty.

## Strengths (summarised)

- Problem is meaningful: for scientific use it's important to know what a model does when evidence is unclear/missing/contradicted, not just whether the final answer is correct
- A-R-I framework is simple and easy to understand
- Evaluation is fairly broad: transforms, false premises, caption bias, selective blur across several models
- GPT-5.2/Gemini comparison is interesting — similar conventional performance, very different behavioural profiles

## Weaknesses

### W1 — Core behavioural evaluation lacks direct human validation
- Most A-R-I outputs are scored by GPT-4o.
- Reported human validation mainly focuses on MQM description evaluation.
- MQM judge only has **item-level Spearman = 0.58** with humans, and for hallucinated content **F1 = 0.12 with recall = 0.07**.
- **Ask:** directly human-validate a subset of admittance, resistance, and inductance outputs.

### W2 — Resistance prompt cues the behaviour being tested
- Prompt explicitly says: if a question asks about something not present in the figure, say so clearly.
- That's basically what the Inexist and Unanswerable probes are intended to test.
- Since every model gets the same prompt, relative comparison is still useful, but **be more careful interpreting absolute resistance scores**.

### W3 — Inductance metric — conditional-on-fabrication
- Table 4 reports correctness among fabricated/specific answers, not correctness over all probes.
- Makes it hard to compare a model that often abstains vs. one that frequently makes correct contextual inferences.
- **Ask:** report unconditional correctness or inference rate.

### W4 — Caption-bias resistance excludes unaddressed claims
- False claims not addressed by the model are excluded from denominator.
- A shorter or lower-coverage model can get higher resistance simply by not discussing those claims.
- **Ask:** report claim coverage together with resistance.

### W5 — "Quality does not predict behaviour" is stronger than the actual analysis
- Table 14 shows fairly high model-level correlations between dimensions.
- The more nuanced statement in-text is more convincing: overall quality and behaviour are correlated, but this can still hide important model-specific reversals.

## Comments / suggestions / typos

### Most important addition
- **Direct human validation of at least a subset of the A-R-I behavioural labels.** (Reviewer states this explicitly as the top ask.)

### Numerical inconsistency
- Table 4 says Gemini active admittance = 71%, passive = 59%. **Figure 3 caption says 90%.** Check.

### Reproducibility wording bug
- **Appendix E:** claims GPT-5.2 and Phi-4 routed through Azure, "all other models (open-weight)" through OpenRouter.
- **Gemini 3.1 Pro is in the latter group and is NOT open-weight** — fix the wording.

## What this reviewer would most reward in a revision

1. **Human validation of a stratified subset per A-R-I label** (their #1 ask, matches MMh1)
2. Unconditional inductance metric (matches MMh1)
3. Coverage-aware caption-bias metric (matches MMh1)
4. Fix Fig 3 / Table 4 inconsistency
5. Fix Appendix E "open-weight" wording bug
6. Soften "quality does not predict behaviour" claim (matches yQSV)
