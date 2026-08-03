# Reviewer Comments — ACL ARR 2026 May Submission #14568

Full thread including desk rejection, reviewer feedback, our submitted responses, and reviewer follow-ups.

---

## ⚠️ Status: DESK REJECTED

**Program Chairs, 30 Jul 2026, 17:30:**
> "This submission has been desk rejected because the Program Chairs determined that it contains hallucinated references."

The desk rejection came **after** the reviewing cycle had produced strong scores.

---

## Post-rebuttal scores (final)

| Reviewer | Overall | Soundness | Excitement | Confidence | Change from initial |
|---|---|---|---|---|---|
| **h9tb** | **4 (Conference)** ↑ | 3 | 3.5 | 3 | Overall raised from 3 → 4 |
| **No6d** | 3 (Findings) ↑ | 3 | 2 | 3 | Overall raised from 2 → 3 (per comment: "positive level") |
| **LhRb** | 3 (Findings) | **3.5** ↑ | 3 | 4 | Soundness raised from 3 → 3.5 |

**Aggregate: 1 Conference + 2 Findings votes.** Absent the desk rejection, this would have been a clear accept.

---

## Reviewer h9tb — Final: Conference (4), Excitement 3.5

### Summary of Strengths
> "The benchmark pipeline features exceptionally precise data interventions. By combining automatic EasyOCR coordinate mapping with a dual-stage blurring protocol (grey-blending plus heavy Gaussian blur), the authors create distinct Admittance Blur (unrecoverable details) and Inductance Blur (inferable variables) conditions. This elegantly differentiates structured visual deduction from ungrounded data fabrication."
>
> "This paper executes exhaustive validation steps to establish the neutrality of its automated metrics."

### W1 — Chart-type coverage

**Reviewer:**
> "Despite harvesting charts from authentic arXiv research papers, the dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding."

**Our submitted response:**
> "We computed the distribution of chart types in the collected scientific papers and found that scatter plots and heatmaps are less common, whereas bar charts, line plots, and pie charts are widely used; that is why we chose to focus on these chart types. We also note that our main dataset contribution is significant, specifically (i) a high-quality human annotation campaign involving 5 annotators for over 600 hours across the perception, reasoning, and behavioural tasks; and (ii) the extension of the original figures into a comprehensive evaluation benchmark through 5 strategies, including image transformations, reasoning, resistance probes, caption-bias probes, and selective-blur targets, producing over 34,000 evaluation setups."

### W2 — Inexist probe failure source

**Reviewer:**
> "Section 5 notes that Inexist probes (which embed false assumptions via definite articles, e.g., asking about non-existent error bars) serve as the most potent deception vectors across all architectures due to a persistent 'must answer' bias. However, the paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressure the model to comply with user prompts regardless of conflicting visual data."

**Our submitted response:**
> "We note that the failure on Inexist probes is unlikely caused by visual blindness, because the models perform strongly (e.g., top models reach an MQM score of 90+) on the perception task (describing what they see), demonstrating that they are visually capable. Therefore, we hypothesise that the failure is more likely due to the models falling for instruction traps in the prompt (e.g., prompts that intentionally sound as if the queried item is present). But this hypothesis requires further scrutiny, which we leave for future work."

### C1 — Llama 4 naming
> "please consistency writing the name of Llama 4"

---

## Reviewer No6d — Final: Findings (3, ↑ from 2), Excitement 2

### Summary of Strengths
> "The paper is clearly written and tackles an important general problem: VLMs may hallucinate or behave unreliably when visual evidence is incomplete or misleading."
>
> "The evaluation is broad in scope, combining perception, reasoning, and behavioral probes within a single benchmark."
>
> "The results surface interesting differences between models that reach similar description quality but diverge sharply in how they handle uncertainty."

### Reviewer follow-up after our rebuttal
> "Thanks for the detailed response. Most of my concerns have been addressed. However, the natural limitation still exists and cannot be solved by the rebuttal or a revision. Therefore, I will change my rating to a positive level but not fight for acceptance."

### W1a — Stress tests build on existing ideas

**Reviewer:**
> "Most of the stress tests build on existing ideas — image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment — rather than introducing new techniques."

**Our submitted response:**
> "We note that our novelty is to adapt existing probe techniques to answer the main research question: whether behavioural reliability under uncertainty on scientific figures follows from perception quality and reasoning capability, or instead emerges as a distinct dimension. Our adaptations are novel, specifically (i) matched-condition perturbations on open-ended descriptions scored via an MQM-adapted rubric that captures error types and severity, rather than binary accuracy or closed-form QA metrics used in prior work; and (ii) OCR-driven selective blurring separating inferable from non-inferable evidence, a controlled visual-uncertainty design."

### W1b — A-R-I renames known dimensions

**Reviewer:**
> "The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method."

**Our submitted response:**
> "The novelty of our A-R-I framework is outlined below:
>
> First, A-R-I extends established uncertainty metrics, which measure whether a model refuses under confusion, to two novel settings: (i) whether the queried element exists in the figure, and (ii) whether it is recoverable despite obscuration. These conditions give rise to three behavioural dimensions: Resistance, Admittance, and Inductance.
>
> Second, we note that applying these behavioural dimensions to VLMs on scientific figures under controlled uncertainty is itself a novel extension.
>
> Third, one of our dimensions, Inductance (inference under recoverable uncertainty), is to our knowledge novel as an evaluation axis. Prior work either treats uncertainty as a binary refuse-or-answer decision or folds inference into accuracy; Inductance measures whether a model can correctly infer from partial evidence when the answer remains recoverable from context."

### W2 — No real-world grounding

**Reviewer:**
> "The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots."

**Our submitted response:**
> "We fully agree that the mapping from our tests to real-world scenarios is crucial. Concretely, our visual perturbations and selective blur represent real-world challenges like degraded PDF rendering, OCR loss, cropping, and low-resolution inputs; our caption bias represents incorrect figure-caption retrieval in document processing or multimodal RAG; our false-premise probes represent erroneous assumptions introduced by users or propagated between agents; our page-context conditions represent models processing figures within complete scientific documents. We will clarify these points in the updated version."

### W3 — Modest benchmark size

**Reviewer:**
> "The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie). This is modest for a benchmark paper, particularly given that the probe types are themselves not especially novel."

**Our submitted response:**
> "We note that our benchmark dataset started with 250 figures, which were then extended into a comprehensive evaluation benchmark through image transformations (1,243 transformed and page-context cases), 1,000 reasoning questions, 750 resistance probes, 100 caption-bias probes, and 443 confirmed selective-blur targets, producing over 34,000 evaluation setups across 8 models.
>
> Furthermore, we provided a high-quality human annotation campaign involving 5 annotators for over 600 hours across the perception, reasoning, and behavioural tasks. This includes 250 high-quality figure descriptions annotated by 3 student annotators over ~240 hours, including an overlapping subset for computing inter-annotator agreement. Additionally, 1,000 GPT-generated reasoning questions were post-edited by 4 annotators over ~200 hours to ensure correctness, and 443 OCR-generated selective-blur targets were post-edited by 3 annotators over ~100 hours. Furthermore, we provided a high-quality human evaluation of 4 LLMs on 30 figures using the MQM scheme, involving 3 annotators over 90 hours."

### W4 — GPT-4o judge dependence + version drift

**Reviewer:**
> "Although the authors include some human validation, the main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report direct agreement between GPT-4o and humans, ideally at the item level. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified."

**Our submitted response:**
> "Indeed, our work reported the correlation (agreement) between GPT-4o and humans on 120 MQM items (see Section 3 and Appendix A.1). Three annotators achieved Krippendorff's α = 0.91 (inter-annotator agreement), and the correlation between GPT-4o and humans was Spearman's ρ = 0.80 in terms of model-level ranking. We have also computed item-level correlation between Mistral Large 3 and humans over 344 capability items, where Spearman's ρ = 0.87. We will add the item-level correlation between GPT-4o and humans in the updated version.
>
> Regarding reproducibility, GPT-4o still remains accessible through the OpenAI API."

### C1 — Justify real-world relevance (comment)
> "The authors should more strongly justify the real-world relevance of the proposed probes, ideally by grounding them in realistic failure cases from scientific workflows — for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines."

### C2 — Position A-R-I more modestly (comment)
> "It would also help to position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm."

---

## Reviewer LhRb — Final: Findings (3), Soundness 3.5 (↑ from 3), Confidence 4

### Summary of Strengths
> "I think the value of this paper is that it does not reduce scientific figure understanding to description quality or QA accuracy. It directly studies uncertainty behavior, which is important in scientific settings. If a model answers confidently when it cannot actually see the evidence, that can be more problematic than an ordinary mistake. I also appreciate the probe-designer ablation, human agreement check, and split-half stability analysis, which make the benchmark more convincing."

### Reviewer update after our rebuttal
> "Thanks for the detailed response. The additional clarifications have increased my confidence in the experimental design and evaluation reliability, so I will raise the Soundness score from 3 to 3.5. However, some other concerns remain partially unresolved, so I will maintain the overall score at 3."

### W1 — Dataset scale + diverse sources

**Reviewer:**
> "My main reservation is about scale and dependence on automatic evaluation. 250 figures is still limited for the broad space of scientific figures. The validation helps, but I would still have liked to see broader human evaluation or more diverse figure sources."

**Our submitted response (partial — scale):**
> "We note that our benchmark dataset started with 250 figures, which were then extended into a comprehensive evaluation benchmark through image transformations (1,243 transformed and page-context cases), 1,000 reasoning questions, 750 resistance probes, 100 caption-bias probes, and 443 confirmed selective-blur targets, producing over 34,000 evaluation setups across 8 models.
>
> Furthermore, we provided a high-quality human annotation campaign involving 5 annotators for over 600 hours across the perception, reasoning, and behavioural tasks. [Same annotation breakdown as above.]"

### W2 — GPT-4o in probe generation + judging

**Reviewer:**
> "GPT-4o is used quite heavily in probe generation and judging. The validation helps, but I would still have liked to see broader human evaluation."

**Our submitted response:**
> "We note that GPT-4o was involved in dataset construction (perception, reasoning, and behavioural probes) with human-in-the-loop oversight to ensure reliability, efficiency, and correctness. GPT-generated descriptions, capability questions, and selective-blur targets were carefully reviewed and corrected by human annotators whenever necessary. Details are provided in Section 3, Appendices B.3, B.6, F.
>
> Regarding GPT-4o as a judge, this is a common practice in NLP as a surrogate for costly human evaluation. We evaluated GPT-4o against humans on 120 MQM items (see Section 3, Appendix A.1), and found positive correlation (Spearman ρ=0.80) in terms of model ranking, suggesting the reliability of GPT-4o as a judge."

### W3 — A-R-I sufficiency

**Reviewer:**
> "The A-R-I framework is useful, but I am not fully convinced that these three dimensions are sufficient to cover behavioral reliability."

**Our submitted response:**
> "We note that A-R-I is not intended to exhaust behavioural reliability in our context. We are fully aware of other behavioural dimensions such as confidence calibration (https://arxiv.org/abs/2305.14975), multi-turn visual-dialogue consistency (https://aclanthology.org/2024.acl-long.658/), and sensitivity to prompt formulation (https://aclanthology.org/2024.findings-emnlp.108/), among others. However, these dimensions are outside our scope, as they are little relevant to our main research question: how models behave when visual evidence is missing, misleading, or only partially recoverable; that is why we chose to focus on A-R-I."

### C1 — arXiv sampling coverage (comment)
> "I would suggest discussing more concretely how arXiv figure sampling affects benchmark coverage."

### C2 — Model version drift (comment)
> "The paper should also discuss model version drift, especially for API models such as GPT and Gemini."

### C3 — A-R-I as necessary + relatively complete decomposition (comment)
> "The A-R-I dimensions could be better justified as a necessary and relatively complete decomposition."

---

## Cross-cutting themes (raised by more than one reviewer)

1. **A-R-I novelty framing** — No6d W1b + C2; LhRb W3 + C3
2. **Dataset scale / chart-type coverage** — h9tb W1; No6d W3; LhRb W1
3. **GPT-4o judge dependence + item-level agreement + version drift** — No6d W4; LhRb W2 + C2
4. **Real-world grounding** — No6d W2 + C1
5. **arXiv sampling / diverse sources** — LhRb W1 + C1

## Reviewer-specific concerns

- **h9tb only:** Inexist perception-vs-instruction-tuning confound (W2); Llama 4 naming (C1)
- **No6d only:** Probe-level novelty of individual techniques (W1a)
- **LhRb only:** (all concerns overlap with cross-cutting themes; specific detailed comments on sampling and drift)

---

## Commitments made in rebuttal (for the resubmission)

Things we explicitly promised in the responses that must be delivered in the revised paper:

1. **Item-level GPT-4o vs human agreement** on behavioural probes (No6d W4) — "We will add the item-level correlation between GPT-4o and humans in the updated version."
2. **Real-world scenario mapping** — "We will clarify these points in the updated version" (No6d W2 + C1)
3. **Human annotation campaign details** — 5 annotators / 600+ hours breakdown (No6d W3, LhRb W1) — must be visible in the paper, not just claimed in rebuttal
4. **A-R-I scope statement** — explicit acknowledgment of what's out of scope + citations to Xuan et al., multi-turn dialogue, prompt sensitivity (LhRb W3)
5. **Llama 4 naming consistency** (h9tb C1)

---

## Bibliography issue that triggered desk rejection

**Separate from the reviewer content**, the Program Chairs flagged six citations as hallucinated:

- Huang, SciFIBench (real: Roberts et al., NeurIPS 2024, arXiv:2405.08807)
- Tang, ChartMuseum (real: Tang, L. et al., NeurIPS 2025, arXiv:2505.13444)
- Pandey, Perils of Chart Deception (real: Mahbub et al., arXiv:2508.09716)
- Ren, Selective Prediction (real: Srinivasan et al., ACL Findings 2024, arXiv:2402.15610)
- Fanous, SycEval (real: Fanous, Aaron et al., arXiv:2502.08177)
- Chen, MultiChartQA (real: Zhu, Zifeng et al., NAACL 2025, arXiv:2410.14179)

**All 6 papers are real** and were correctly cited in the signed thesis (`thesis-work/support/thesis/main/abdnthesis.bbl`). The ACL bib was regenerated with LLM assistance and reintroduced author-name errors that had already been fixed for the thesis (see `thesis-work/support/internal-feedback/bib_corrections.md` for evidence of the earlier correction process).

**For the resubmission:** every citation must be manually verified against the thesis `.bbl` and against arXiv directly. No LLM-generated bib entries.
