# Response to Reviewer No6d

## Reviewer scores (for our reference — do not include in submitted rebuttal)

Overall: 2 (Resubmit next cycle) · Soundness: 2.5 · Excitement: 2 · Confidence: 3
Reproducibility: 2 · Datasets: 2 · Software: 2

---

We thank the reviewer for the thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1a.** Most of the stress tests build on existing ideas — image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment — rather than introducing new techniques.

A: Thank you for the feedback. We agree these categories have prior conceptual roots, which we discuss in Section 2 and will make more explicit. Our probe-level contribution lies in two design differences. (1) We apply these perturbations in matched conditions to systematically diagnose how open-ended figure descriptions change under altered visual evidence, using an MQM-adapted rubric that captures error types and severity rather than relying only on binary accuracy, BLEU, or closed-form QA metrics commonly used in prior work. (2) For uncertainty, we decompose visual evidence into inferable and non-inferable elements, operationalised through OCR-driven selective blurring of specific chart targets. This is a controlled visual-uncertainty design that, to our knowledge, prior VLM benchmarks do not implement.

**W1b.** The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method.

A: We agree that the component behaviours have precedents, although, to our knowledge, inference under recoverable uncertainty is rarely treated as a distinct evaluation axis. Rather than aggregating existing metrics, A-R-I constructs controlled evidence conditions to evaluate model behavioural profiles based on the relationship between a query and its evidence, mapping each response to the behaviour appropriate to that condition. For example, a query about a non-existent element, often classified under uncertainty or unanswerability in prior work, maps to Resistance because the appropriate response is to reject the false premise. If the element exists but is obscured and unrecoverable, Admittance applies. If it remains recoverable from the available context, Inductance applies. These correspond to distinct operational failure modes that accuracy or a single uncertainty score can obscure. Accuracy may reward a lucky guess even when the evidence is unrecoverable, while a single uncertainty score cannot reveal the specific behavioural failure. A-R-I captures these distinctions because a model may infer and resist but fail to admit. GPT-5.2 demonstrates this profile, achieving strong Resistance (0.81) and Inductance (59%) but only 8% active Admittance.

**W2.** The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots.

A: We agree that the paper should distinguish the prevalence of these conditions from their consequences. SciFig-Eval does not estimate how frequently each failure occurs in scientific workflows. Instead, it uses controlled conditions to measure model behaviour when such evidence failures occur. We will clarify this scope and connect the probes explicitly to practical settings. Visual perturbations and selective blur represent degraded PDF rendering, OCR loss, cropping, and low-resolution inputs. Caption bias represents incorrect figure-caption retrieval in document processing or multimodal RAG. False-premise probes represent erroneous assumptions introduced by users or propagated between agents. Page-context conditions represent models processing figures within complete scientific documents. We will add this mapping to the benchmark design section.

**W3.** The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie). This is modest for a benchmark paper, particularly given that the probe types are themselves not especially novel.

A: We acknowledge that 250 figures and three chart types limit the benchmark’s breadth, as stated in our Limitations. We emphasise three considerations.

- **Diagnostic depth.** The 250 authentic figures from 187 papers support more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 reasoning questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets.

- **Probe-level innovations.** While several broad probe categories have precedents, our OCR-localised and human-confirmed selective-blur pipeline separates unrecoverable from recoverable visual evidence to measure Admittance and Inductance. Our paired in-paper ablation compares an isolated figure, the figure within its original page, and the same page with the target figure blurred, separating direct visual understanding from reliance on surrounding document context. To our knowledge, these controlled designs have not been implemented in prior scientific-figure benchmarks.

- **Reliability within scope.** Split-half reliability is $\rho=0.979$ across 100 random splits, and resistance scores converge by 100 figures with a maximum deviation of 0.02 from the full set. Broader coverage of scatter plots, heatmaps, and other scientific figures remains important future work, as already stated in our Limitations section.

**W4.** Although the authors include some human validation, the main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report direct agreement between GPT-4o and humans, ideally at the item level. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified.

A:

- **Judge validation.** Unlike holistic open-ended judging, our behavioural evaluation supplies the judge with the known blurred element, expected answer, false premise, and expected behaviour, and restricts its output to explicit binary or three-level labels. While engineering the judge prompts, we manually inspected output samples across models and probe types and iteratively refined the rubrics, although this was not reported as a separate agreement study. As reported in the paper, we also compared GPT-4o with humans on 120 MQM items and independently judged 344 capability items using Mistral Large 3, obtaining 87.2% item-level agreement and identical model rankings. We will extend this validation using a stratified sample across the behavioural probes and report the missing item-level agreements with human judgements.

- **Model availability and reproducibility.** We clarify that GPT-4o was retired from the ChatGPT interface, whereas our evaluation used Azure OpenAI. GPT-4o remains available through both the OpenAI API and Azure at present, although Azure has scheduled its GPT-4o versions for retirement on October 1, 2026. The paper already reports the Azure region, deployment name, API version, temperature, and seed. We agree that long-term reproducibility additionally requires the underlying model version and inference dates, which we will report alongside the released benchmark data and annotations, prompts, model outputs, and evaluation scripts. The independent Mistral Large 3 validation already tests judge dependence for the 344-item capability evaluation, while the planned stratified behavioural validation will extend this robustness check to the behavioural probes.

## Comments Suggestions And Typos

**C1.** The authors should more strongly justify the real-world relevance of the proposed probes, ideally by grounding them in realistic failure cases from scientific workflows — for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines.

A: Please see our response to W2. We agree and will revise the benchmark design section to make these real-world correspondences explicit.

**C2.** It would also help to position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm.

A: We agree that A-R-I includes a diagnostic taxonomy, but it is not limited to categorising behaviours. Please see our response to W1b. Its taxonomy defines the behavioural axes, while the controlled evidence conditions and corresponding metrics operationalise those axes as a targeted multidimensional evaluation framework based on the relationship between a query and its evidence.
