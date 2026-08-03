# Response to Reviewer LhRb

## Reviewer scores (for our reference, do not include in submitted rebuttal)

Overall: 3 (Findings) · Soundness: 3 · Excitement: 3 · Confidence: 4
Reproducibility: 3 · Datasets: 3 · Software: 3

---

We thank the reviewer for the positive assessment and thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1.** The benchmark contains only 250 figures, which is limited for the broad space of scientific figures. The reviewer would also prefer more diverse figure sources and a concrete discussion of how arXiv figure sampling affects benchmark coverage.

A: We agree that 250 figures cannot represent the broad space of scientific figures. As stated in the Dataset section, SciFig-Eval contains 250 English-language figures from 187 arXiv papers (2023–2025), with stratified sampling to preserve the chart-type distribution. Within this scope, the dataset contribution extends beyond the raw figure count in two respects.

First, high-quality human annotation was carried out across perception, reasoning, and behaviour. All 250 figures received human-annotated expert ground-truth descriptions. 1,000 reasoning questions were independently human-reviewed against the source figures. 443 selective-blur targets were confirmed or replaced through human review using our OCR-localised pipeline. MQM judge validation was performed by three graduate-level annotators, with Krippendorff's α=0.91 on double-annotated pairs.

Second, the 250 figures were extended into a comprehensive evaluation benchmark through image transformations (1,243 transformed and page-context cases), 1,000 reasoning questions, 750 resistance probes, 100 caption-bias probes, and 443 confirmed selective-blur targets, producing over 34,000 evaluation setups across eight models. Split-half reliability is ρ=0.979 across 100 random splits, and resistance scores converge by 100 figures with a maximum deviation of 0.02 from the full set.

Broader and more diverse scientific corpora remain important future work, as already stated in our Limitations section.

**W2.** GPT-4o is used heavily in probe generation and judging. Although the existing validation helps, broader human evaluation would strengthen the benchmark.

A: We note that GPT-4o is involved in dataset construction (perception, reasoning, and behavioural probes) with human-in-the-loop oversight: expert descriptions, capability questions, and selective-blur targets receive per-item human review, and probe generation follows human-designed criteria (Section 3, Appendices B.3, B.6, F).

Regarding GPT-4o as a judge, this is a common practice in NLP as a surrogate for costly human evaluation. We evaluated GPT-4o against human annotators on 120 MQM items (Section 3, Appendix A.1), finding Spearman ρ=0.80 with identical model rankings, suggesting the reliability of GPT-4o as a judge. We further re-judged 344 capability items using Mistral Large 3, obtaining 87.2% item-level agreement and identical rankings. Item-level GPT-4o vs human agreement on the behavioural probes was not reported in the current draft; we will extend this validation across the behavioural probes in the updated version.

**W3.** The reviewer is not fully convinced that the three A-R-I dimensions are sufficient to cover behavioural reliability and asks that they be justified as a necessary and relatively complete decomposition.

A: As stated in Section 3.4, A-R-I is not intended to exhaust behavioural reliability for VLMs on scientific figures. Complementary dimensions such as verbalised confidence calibration, multi-turn consistency under repeated user pushback, and prompt-form sensitivity remain outside our scope. We focus on A-R-I because it addresses our central research question: how models behave when visual evidence is missing, misleading, or partially recoverable. Its axes correspond to deployment-relevant failures, including silent fabrication when an existing element becomes unrecoverable, acceptance of false or misleading premises, and failure to infer from partial but sufficient evidence. These conditions can also be objectively annotated for individual figure-query pairs, enabling behavioural metrics distinct from accuracy. Other dimensions require different experimental protocols that we consider valuable but outside the scope of this single-figure benchmark.

Within this scope, SciFig-Eval provides substantial diagnostic depth across eight proprietary and open-weight models, with 1,243 transformed or page-context cases, 1,000 reasoning questions, 750 Resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets separating Admittance from Inductance, producing more than 34,000 evaluation setups. Split-half reliability is ρ=0.979 across 100 random splits.

We will make this intended scope more prominent in the revised version.

## Comments Suggestions And Typos

**C1.** The paper should discuss model-version drift, especially for API models such as GPT and Gemini.

A: We agree that version drift is an important limitation of API-based evaluation. As reported in Appendix E, we provide the model identifiers, serving backends, Azure region and API version, inference settings, and experiment period of March to May 2026. Temperature 0 and fixed sampling seeds reduce run-level variability, while our bootstrap, split-half, and scale analyses establish stability across dataset samples. These controls do not, however, prevent providers from updating the underlying model behind an API identifier. We will make this distinction explicit and additionally report the underlying model or deployment versions and exact inference dates where exposed by the providers. We will also release the original prompts and model outputs, allowing future reruns to quantify changes caused by model-version drift.
