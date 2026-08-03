# Response to Reviewer LhRb

## Reviewer scores (for our reference, do not include in submitted rebuttal)

Overall: 3 (Findings) · Soundness: 3 · Excitement: 3 · Confidence: 4
Reproducibility: 3 · Datasets: 3 · Software: 3

---

We thank the reviewer for the positive assessment and thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1.** The benchmark contains only 250 figures, which is limited for the broad space of scientific figures. The reviewer would also prefer more diverse figure sources and a concrete discussion of how arXiv figure sampling affects benchmark coverage.

A: We agree that 250 figures cannot represent the broad space of scientific figures. As stated in the Dataset section, Appendix E, and our Limitations, SciFig-Eval contains 250 English-language figures from 187 arXiv papers published between 2023 and 2025, spanning NLP, machine learning, and computational linguistics, with stratified sampling used to preserve the chart-type distribution. This sampling provides authentic and varied content within the selected scope, while naturally biasing coverage towards recent English-language computer-science research and limiting generalisation to other disciplines and figure types. Within this scope, we prioritise diagnostic depth, supporting more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 capability questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets. As also reported, split-half reliability is $\rho=0.979$, and resistance scores converge by 100 figures with a maximum deviation of 0.02 from the full set. Broader and more diverse scientific corpora remain important future work.

**W2.** GPT-4o is used heavily in probe generation and judging. Although the existing validation helps, broader human evaluation would strengthen the benchmark.

A: We agree that broader human validation would strengthen the benchmark. GPT-4o did not design the probes without human specification or independent checks. The resistance and caption-bias pipelines use detailed human-designed criteria, constraints, and positive and negative examples. During prompt engineering, we manually inspected generated samples and iteratively refined these specifications. We will document this human-in-the-loop development process more explicitly, while distinguishing it from the independent human-agreement evaluation. As detailed in Section 3 and Appendices B.3 and F, capability questions are independently filtered by Mistral Large 3 using five quality criteria. Every selective-blur target is confirmed or replaced by a human reviewer before inclusion, as described in Appendix B.6. We further regenerated probes with Mistral Large 3 on a matched 50-figure subset, preserving model rankings, as reported in Section 4.5 and Appendix C.

For judging, Appendix C.1 reports human comparison on 120 MQM items, while Appendix C, Table 9 reports independent Mistral Large 3 judging of 344 capability items, yielding 87.2% item-level agreement and identical model rankings. We will extend this validation using a fresh stratified sample across the behavioural probes and report the missing item-level agreements with human judgements. Broader figure sources remain important future work, as discussed in our response to W1.

**W3.** The reviewer is not fully convinced that the three A-R-I dimensions are sufficient to cover behavioural reliability and asks that they be justified as a necessary and relatively complete decomposition.

A: As stated in Section 3.4, A-R-I is not intended to be exhaustive. It provides a targeted decomposition of model behaviour based on the relationship between a query and its supporting evidence. Within the conditions studied by SciFig-Eval, Admittance applies when a target element exists but is obscured and unrecoverable from the remaining evidence. Resistance applies when the query introduces a non-existent, false, or misleading premise. Inductance applies when a target element exists and is obscured but remains recoverable from the surrounding context. These axes cover the benchmark’s principal evidence conditions and are empirically separable, but we do not claim that they exhaust every possible query-evidence relationship or model behaviour. We will make this intended scope more prominent.

## Comments Suggestions And Typos

**C1.** The paper should discuss model-version drift, especially for API models such as GPT and Gemini.

A: We agree that version drift is an important limitation of API-based evaluation. As reported in Appendix E, we provide the model identifiers, serving backends, Azure region and API version, inference settings, and experiment period of March to May 2026. Temperature 0 and fixed sampling seeds reduce run-level variability, while our bootstrap, split-half, and scale analyses establish stability across dataset samples. These controls do not, however, prevent providers from updating the underlying model behind an API identifier. We will make this distinction explicit and additionally report the underlying model or deployment versions and exact inference dates where exposed by the providers. We will also release the original prompts and model outputs, allowing future reruns to quantify changes caused by model-version drift.
