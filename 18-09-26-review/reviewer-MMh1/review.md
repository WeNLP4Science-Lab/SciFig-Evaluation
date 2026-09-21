# Reviewer MMh1

**Overall:** 3.5 (Borderline Conference)
**Soundness:** 3 · **Excitement:** 4 · **Confidence:** 3
**Reproducibility:** 4 · **Datasets:** 4 · **Software:** 4
**Posted:** 16 Sept 2026 (modified 16 Sept 2026, 13:38)

## Paper Summary (their words)

> This paper introduces SCIFIG-EVAL, a benchmark for VLM understanding of scientific bar, line, and pie charts. Beyond description quality and visual reasoning, it evaluates behavioral reliability under missing or misleading visual evidence through the proposed Admittance-Resistance-Inductance framework. The benchmark includes 250 figures, 1,000 reasoning questions, image transformations, misleading-caption probes, false-premise questions, and selectively blurred chart elements. Experiments across eight VLMs find that conventional perception/reasoning scores do not fully predict behavior under uncertainty.
>
> This is a well-motivated and substantial benchmark contribution. The behavioral framing is useful, the benchmark construction is unusually detailed, and the empirical results are potentially valuable for scientific-document and multimodal-RAG settings. My main concerns are about evaluation validity, prompt-induced behavior, and overinterpretation of the proposed dimensions.

## Strengths (summarised)

- Meaningful gap: clean-chart correctness ≠ reliability under uncertainty
- Benchmark is substantial and detailed (implementation, prompt inventories, transformation params, model IDs, bootstrap)
- Robustness checks: alternative capability judge, probe-generator ablation, split-half reliability, chart-type breakdown
- Interesting qualitative finding: similar clean-chart scores → very different uncertainty behavior

## Weaknesses

### W1 — Behavioural evaluation lacks human validation
- GPT-4o generates questions/probes, judges MQM, scores resistance, judges selective-blur outcomes.
- Human evaluation in Appendix C validates MQM only — NOT the core behavioural labels (resistance, admittance, fabrication, inductance).
- Reported MQM bias is substantial; hallucination-content F1 low.
- **Ask:** provide human annotation for a stratified sample per behavioural probe family; report agreement per behavioural label; evaluate central results with an independent judge (not only capability tasks or the small probe-design ablation).

### W2 — Prompts may cue the behaviour being measured
- Resistance answering prompt (Appendix F, R2) says: *"If a question asks about something not present in the figure, say so clearly."*
- That literally is the behaviour probed by Inexist / Unanswerable.
- Resistance scores may partly measure task-instruction compliance rather than spontaneous robustness.
- **Ask:** compare neutral prompts, explicit abstention-supporting prompts, adversarially framed prompts. Also clarify whether identical system-level and answer-level prompts are used across all providers.

### W3 — A-R-I not shown to be empirically distinct constructs
- Table 14 shows very high rank correlations across MQM / resistance / capability / inductance.
- 8 models is too few for construct-separability arguments; a couple of rank reversals (GPT-5.2 / Gemini) don't prove distinct dimensions.
- **Ask:** distinguish "not perfectly predicted by baseline quality" vs. "empirically distinct behavioral dimension." Use instance-level correlations, partial correlations controlling for baseline capability, reliability-adjusted factor analysis, or broader model pool.

### W4 — Inductance metric rewards guessing
- Inductance = % of fabricated answers that are correct on inferable elements.
- Conditioning on fabrication excludes abstentions → cautious models get penalised.
- **Ask:** report full outcome distribution (correct inference / incorrect fabrication / admitted uncertainty / omission / abstention). Consider utility-based score or selective-risk curve.

### W5 — Caption-bias scoring excludes unaddressed claims → favours evasive outputs
- Appendix B.5: resistance computed only over false claims a description addresses.
- Terse / incomplete descriptions escape penalty. Worse when models differ in verbosity and max output length.
- **Ask:** report claim coverage; use a fixed structured response format; or add a complementary metric that treats "failure to address a relevant claim" separately from resistance.

### W6 — Scope narrower than title/deployment claims imply
- Only English bar/line/pie charts from arXiv NLP/ML/CL papers.
- No scatter plots, heatmaps, microscopy, diagrams, tables, multi-panel mixed figures.
- Limitations acknowledges some of this, but **abstract and conclusion should frame SciFig-Eval as a chart-focused scientific-figure benchmark**, not a comprehensive one.

## Comments / suggestions / typos

- Verify all source figures can be redistributed under their individual arXiv licenses ("openly accessible" ≠ redistribution permission).
- "Cached at stable weights" claim for OpenRouter open-weight models needs stronger evidence (revision hashes, preprocessing, image-resolution policies, routing settings).
- **Gemini gets a much larger token budget** than other models — explain why this doesn't affect completeness / reasoning / apparent abstention.
- Human MQM validation covers only 4 models and **omits Gemini, Phi-4, and behavioural probes** — make this more prominent.
- State how multiple questions/claims from the same base figure are handled in bootstrap inference (not fully independent).
- Add examples of borderline model responses + corresponding judge/human labels for each A-R-I category.
- Several claims about training artifacts, RLHF "must answer" pressure, and deployment risk are speculative — state as hypotheses, not causal explanations.

## What this reviewer would most reward in a revision

1. Human validation of a stratified subset of each A-R-I behavioural label
2. Prompt-variant ablation isolating instruction compliance from spontaneous behaviour
3. Full outcome distribution for inductance (not conditional-on-fabrication correctness)
4. Coverage-aware caption-bias metric
5. Narrower scope claim in title/abstract/conclusion
