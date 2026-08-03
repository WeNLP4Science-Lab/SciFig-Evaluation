# Response to Reviewer No6d

## Reviewer scores (for our reference — do not include in submitted rebuttal)

Overall: 2 (Resubmit next cycle) · Soundness: 2.5 · Excitement: 2 · Confidence: 3
Reproducibility: 2 · Datasets: 2 · Software: 2

---

We thank the reviewer for the thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1a.** Most of the stress tests build on existing ideas — image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment — rather than introducing new techniques.

A: We agree that these probe categories build on prior work, discussed in Section 2 and to be made more explicit. Our contribution is not in the individual probe techniques but in the central question they enable us to investigate: whether behavioural reliability under uncertainty on scientific figures follows from perception quality and reasoning capability, or emerges as a distinct dimension. As stated in Sections 1 and 2, existing VLM benchmarks emphasise perception and reasoning accuracy but rarely measure behavioural reliability directly. To enable this investigation, we adapt existing techniques in two specific ways: (1) matched-condition perturbations on open-ended descriptions scored via an MQM-adapted rubric that captures error types and severity, rather than binary accuracy or closed-form QA metrics used in prior work; (2) OCR-driven selective blurring separating inferable from non-inferable evidence, a controlled visual-uncertainty design that, to our knowledge, no prior VLM benchmark implements.

**W1b.** The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method.

A: We agree that some component behaviours have precedents in prior work. We address the concern in three parts.

First, the A-R-I framework moves beyond the general umbrella of uncertainty metrics used in prior work, which measure whether a model refuses under confusion. In A-R-I, the metric is additionally defined by two ground-truth evidence conditions: the presence of the queried element in the figure, and the recoverability of the evidence given any obscuration. The mapping proceeds by these conditions: if the element is absent, the query maps to Resistance (rejection of a false premise), which prior work would classify under generic uncertainty (e.g., inexist or unanswerable probes); if the element is present but unrecoverable, the query maps to Admittance (acknowledgment of unreadable evidence); if the element is present and recoverable from context, the query maps to Inductance (bounded inference), where a refusal acceptable under generic uncertainty framing is instead incorrect under A-R-I. Because these two ground-truth conditions require per-item annotation that prior VLM benchmarks do not provide, A-R-I scores are incomputable from existing metrics, making the framework structurally distinct rather than a recombination of prior metrics. These distinctions surface operational failure modes that a single uncertainty or accuracy score does not separate. This is key for practical deployment, where the appropriate model behaviour depends on the true state of the evidence rather than the model's subjective confusion.

Second, applying these behavioural dimensions to VLMs on scientific figures under controlled uncertainty is itself a novel extension. Uncertainty acknowledgment, resistance to misleading context, and hallucination measurement have been studied primarily for LLMs on text tasks, and in a limited form in VLM hallucination benchmarks, but they have not been jointly evaluated as first-class metrics for scientific figure understanding.

Third, one of our dimensions, Inductance (inference under recoverable uncertainty), is to our knowledge novel as an evaluation axis. Prior work either treats uncertainty as a binary refuse-or-answer decision or folds inference into accuracy; Inductance measures whether a model can correctly infer from partial evidence when the answer remains recoverable from context.

**W2.** The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots.

A: We fully agree that the mapping from our tests to real-world scenarios is missing from the current draft, and we will add it in the updated version. Concretely, visual perturbations and selective blur represent degraded PDF rendering, OCR loss, cropping, and low-resolution inputs; caption bias represents incorrect figure-caption retrieval in document processing or multimodal RAG; false-premise probes represent erroneous assumptions introduced by users or propagated between agents; and page-context conditions represent models processing figures within complete scientific documents.

**W3.** The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie). This is modest for a benchmark paper, particularly given that the probe types are themselves not especially novel.

A: We acknowledge that 250 figures and three chart types limit the benchmark's breadth, as stated in our Limitations. The dataset contribution, however, extends beyond the raw figure count in two respects.

First, high-quality human annotation was carried out across perception, reasoning, and behaviour. All 250 figures received human-annotated expert ground-truth descriptions. 1,000 reasoning questions were independently human-reviewed against the source figures. 443 selective-blur targets were confirmed or replaced through human review using our OCR-localised pipeline. MQM judge validation was performed by three graduate-level annotators, with Krippendorff's α=0.91 on double-annotated pairs. We will additionally report the total annotator team size and effort estimate in the updated version.

Second, the 250 figures were extended into a comprehensive evaluation benchmark through image transformations (1,243 transformed and page-context cases), 1,000 reasoning questions, 750 resistance probes, 100 caption-bias probes, and 443 confirmed selective-blur targets, producing over 34,000 evaluation setups across eight models.

Broader coverage of scatter plots, heatmaps, and other scientific figures remains important future work.

**W4.** Although the authors include some human validation, the main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report direct agreement between GPT-4o and humans, ideally at the item level. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified.

A: **Judge validation.** We note that our work reports GPT-4o vs human agreement on 120 MQM items in Section 3 and Appendix A.1: three annotators achieved Krippendorff's α=0.91 (interval scale), and model-level ranking agreement between GPT-4o and humans was Spearman ρ=0.80 with identical rankings. Judge dependence is separately tested by re-judging 344 capability items using Mistral Large 3, yielding 87.2% item-level agreement and identical rankings. Behavioural judging is deliberately constrained: probes supply the judge with the known blurred element, expected answer, false premise, and expected behaviour, restricting outputs to binary or three-level labels. Item-level GPT-4o vs human agreement on the behavioural probes was not reported in the current draft; we will extend the validation using a stratified sample across the behavioural probes and report these agreements in the updated version.

**Model availability.** GPT-4o remains available through the OpenAI API.

## Comments Suggestions And Typos

**C1.** The authors should more strongly justify the real-world relevance of the proposed probes, ideally by grounding them in realistic failure cases from scientific workflows — for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines.

A: Please see our response to W2. We agree and will revise the benchmark design section to make these real-world correspondences explicit.

**C2.** It would also help to position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm.

A: We agree that A-R-I includes a diagnostic taxonomy, but it is not limited to categorising behaviours. Please see our response to W1b. Its taxonomy defines the behavioural axes, while the controlled evidence conditions and corresponding metrics operationalise those axes as a targeted multidimensional evaluation framework based on the relationship between a query and its evidence.
