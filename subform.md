# ACL Submission Form

## Keywords
Scientific Figure Understanding, Vision-Language Models, Behavioural Evaluation, Hallucination Detection, Benchmark, Selective Blur, Admittance-Resistance-Inductance, Chart Understanding, MQM Evaluation, Epistemic Honesty

## TL;DR
A benchmark for scientific figure understanding revealing that top-scoring VLMs can fabricate confidently when visual evidence is missing or misleading, and that perception quality alone does not predict behavioural reliability under uncertainty.

## Research Area
**Resources and Evaluation**

Rationale: SciFig-Eval is a benchmark (resource) with a novel evaluation framework (A-R-I). The paper's core contribution is the evaluation methodology and dataset, not a new model or application. "Multimodality and Language Grounding to Vision, Robotics and Beyond" is a close second since we evaluate VLMs, but the primary contribution is the benchmark and evaluation framework itself.

Alternative consideration: Should we pick "Multimodality and Language Grounding to Vision, Robotics and Beyond" instead? That track may have reviewers more familiar with VLM evaluation. Discuss with team.

## Research Area Keywords
benchmarking, evaluation methodologies, evaluation, NLP datasets, metrics, vision question answering, multimodality

Rationale: Selected from both "Resources and Evaluation" (primary track) and "Multimodality" (secondary relevance). "benchmarking" and "evaluation methodologies" are the core fit. "vision question answering" and "multimodality" capture the VLM aspect.

## Contribution Types
- **Model analysis & interpretability** (we analyse 8 VLMs across behavioural dimensions)
- **NLP engineering experiment** (systematic evaluation with controlled probes)
- **Data resources** (250 annotated figures, 34,000+ evaluation instances, selective blur dataset)
- **Publicly available software and/or pre-trained models** (evaluation scripts, prompts, and dataset released upon publication)

## Languages Studied
English

## Previous URL
N/A (first submission)

## Reassignment Request Area Chair
This is not a resubmission

## Preprint
TODO: Discuss with team. Options:
- **Yes** — ARR releases an anonymous preprint on OpenReview. Increases visibility but makes the work public before acceptance.
- **No** — Keep submission private until accepted.

Recommendation: Yes, if the team is comfortable with early visibility. Most benchmark papers benefit from community feedback.

## Preprint Status
TODO: Discuss with team. Options:
- "We are considering releasing a non-anonymous preprint in the next two months" — safest if you might want to put it on arXiv during review. Keeps options open.
- "There is no non-anonymous preprint and we do not intend to release one" — **binding**, cannot change later.

Recommendation: "We are considering releasing a non-anonymous preprint in the next two months" — keeps flexibility without committing.

## Preferred Venue
TODO: Discuss with team. Key decision:
- **ACL** — top venue, most competitive, highest visibility. Deadline alignment unclear for May cycle.
- **EMNLP** — explicitly aligned with May cycle. Strong venue for evaluation/benchmark papers.
- **AACL** — also aligned with May cycle. Regional but growing.

Note: This is **binding** for EMNLP and AACL for the May cycle. If you select EMNLP, you cannot later commit to AACL from this submission, and vice versa.

Recommendation: **EMNLP** — strong fit for benchmark/evaluation papers, explicitly aligned with this cycle.

## Visa Needs
TODO: Discuss with team. Does the presenting author need a visa to attend EMNLP? Depends on venue location and presenter's nationality.

## Consent To Share Data
Yes

(No downside — it's anonymised metadata only, helps the research community study review processes.)

## Consent To Share Submission Details
On behalf of all authors, we agree to the terms above to share our submission details.

(Standard requirement — ensures no dual submission. Must agree to submit.)

## A1 Limitations Section
Yes — this paper has a limitations section.

(Located in conclusion.tex after the main conclusion, covers: English-only scope, dataset size, GPT-4o judge reliance, cross-judge validation.)

## A2 Potential Risks
Yes

Elaboration: See the Ethics Statement (unnumbered section, after Limitations). The benchmark reveals behavioural limitations of VLMs rather than developing adversarial attacks. Adversarial probes (false premises, misleading captions, selective blur) are diagnostic evaluation tools, not attack vectors. All figures are from openly accessible arXiv preprints with no personally identifiable information.

## B Use Or Create Scientific Artifacts
Yes

Elaboration: We create a benchmark dataset (250 annotated scientific figures with groundtruth descriptions, 1,000 capability questions, 228 admittance blur probes, 215 inductance blur probes, 750 resistance probes, 100 caption bias probes) and evaluation code (MQM scoring pipeline, probe generation and evaluation scripts, statistics computation). We also use existing scientific artifacts (8 VLMs via API, GPT-4o as judge, Mistral Large 3 as validator, EasyOCR for text extraction).

## B1 Cite Creators Of Artifacts
Yes

Elaboration: All 8 evaluated models are cited in Section 4.1 (Models) with references to their technical reports or model cards. The judge model (GPT-4o) and validator (Mistral Large 3) are also cited. Prior benchmarks (ChartQA, CharXiv, CHOCOLATE, CHAOS, etc.) are cited in Section 2 (Related Work).

## B2 Discuss The License For Artifacts
Yes

Elaboration: The Ethics Statement notes that all scientific figures are sourced from arXiv preprints, which are openly accessible and licensed for research use. The dataset, evaluation scripts, model outputs, and prompts will be released upon publication.

## B3 Artifact Use Consistent With Intended Use
Yes

Elaboration: See Ethics Statement. All VLMs are used via their public APIs for research evaluation, consistent with their terms of service. ArXiv figures are used for research purposes consistent with arXiv's open access licence. Our benchmark is intended for research evaluation of VLMs and is not designed for commercial deployment or adversarial attack development.

## B4 Data Contains Personally Identifying Info Or Offensive Content
Yes

Elaboration: See Ethics Statement. The dataset contains only scientific figures (bar charts, line plots, pie charts) from arXiv papers. No personally identifiable information is present. The figures depict quantitative research results, not personal data or offensive content.

## B5 Documentation Of Artifacts
Yes

Elaboration: Section 3.1 (Dataset) describes corpus composition (250 figures, 187 arXiv papers, 3 chart types, English-language, NLP/ML domain). The appendix provides a comprehensive dataset table (Table~\ref{tab:dataset-comprehensive}) with full breakdowns of all components, evaluation instances, and probe counts. Appendix E documents API configurations, model identifiers, and reproducibility details.

## B6 Statistics For Data
Yes

Elaboration: Section 3.1 (Dataset) provides a summary table with counts for all benchmark components (250 figures, 1,686 transforms, 1,000 reasoning questions, 1,293 behavioural probes). The appendix comprehensive table breaks down all evaluation instances per condition, model, and probe type, totalling 34,000+. Split-half reliability and scale convergence analyses are reported in the appendix.

## C Computational Experiments
Yes

## C1 Model Size And Budget
Yes

Elaboration: Appendix E (API Configuration and Reproducibility) reports model identifiers, API backends (Azure, OpenRouter), and inference settings. The experimental setup table reports ~24,700 total API calls. Parameter counts are reported where publicly available (e.g. Llama 4 Maverick 17B×128E MoE, Qwen3-VL variants). Commercial model sizes (GPT-5.2, Gemini) are not publicly disclosed. No local GPU training was performed; all experiments use API-based inference.

## C2 Experimental Setup And Hyperparameters
Yes

Elaboration: Section 4 (Experiments and Results) and Appendix E (API Configuration and Reproducibility) report all inference settings: temperature=0 for all calls, max tokens=2,048 (Gemini: 16,000), seed=42, Azure API version. No hyperparameter search was conducted as all models use deterministic decoding at temperature 0.

## C3 Descriptive Statistics
Yes

Elaboration: Section 4 reports bootstrap 95% confidence intervals (B=10,000) for key comparisons, paired bootstrap significance tests with p-values, and Cliff's delta effect sizes. The experimental setup table states all results are from single deterministic runs (temperature=0). Appendix tables report per-chart-type and per-dimension breakdowns with bootstrap CIs. Split-half reliability (rho=0.979) validates ranking stability.

## C4 Parameters For Packages
Yes

Elaboration: The experimental setup table (Appendix) lists all software used: OpenAI Python SDK (API client), OpenCV/NumPy/Pillow (image processing), EasyOCR (text extraction), SciPy (bootstrap, Cliff's delta). Blur parameters are specified in Appendix D.6 (Gaussian kernel size 75, grey blend factor 0.7). Image transform parameters are in Appendix D.2 (noise sigma=25, contrast alpha=0.3/beta=50, rotation 15 degrees).

## D Human Subjects Including Annotators
Yes

## D1 Instructions Given To Participants
Yes

Elaboration: Appendix A.1 (Human Validation) describes the annotation task (MQM scoring rubric, 0-100 scale). Annotators used the MQM checklist described in Section 3.2 and Appendix D.1. Capability question annotators used the dashboard review interface with clear task instructions. The Ethics Statement notes that human annotations were performed by consenting graduate researchers who were informed of the study's purpose. No risks to participants were identified as the task involves evaluating scientific figure descriptions.

## D2 Recruitment And Payment
No

Elaboration: Annotators were graduate researchers within the research group, not crowdworkers. They participated as part of their research activities, not as paid external participants. This is acknowledged in the Ethics Statement ("consenting graduate researchers who were informed of the study's purpose"). No external recruitment or payment was involved.

## D3 Data Consent
Yes

Elaboration: See Ethics Statement. Annotators were informed of the study's purpose and consented to participate. The scientific figures are from arXiv preprints which are publicly available under open access terms and do not require individual consent for research use.

## D4 Ethics Review Board Approval
N/A

Elaboration: The study involves evaluation of publicly available AI models on publicly available scientific figures. Annotators are graduate researchers within the team performing standard research tasks. No sensitive personal data, vulnerable populations, or deceptive protocols are involved. This type of NLP research is typically exempt from ethics board review.

## E AI Assistants In Research Or Writing
Yes

## E1 Information About Use Of AI Assistants
Yes

Elaboration: AI assistants were used in two capacities: (1) As part of the benchmark methodology itself, GPT-4o serves as the automated judge and probe generator, and Mistral Large 3 as the validator, both fully documented in Sections 3 and 4 and Appendix D. (2) Claude Code (Anthropic) was used to assist with code development, statistical analysis, and manuscript drafting. All scientific claims, experimental design decisions, and final text were reviewed and approved by the authors.

## Author Submission Checklist
Yes

TODO: Before submitting, verify against the checklist at https://aclrollingreview.org/authorchecklist:
- [ ] Paper is within page limits (8 pages + unlimited appendix/references)
- [ ] Anonymous (no author names in PDF, no identifying URLs)
- [ ] Limitations section present
- [ ] Ethics Statement present
- [ ] References complete
- [ ] No concurrent submission to other venues
- [ ] ACL format used correctly
- [ ] Remove \todo and \wz markers before final PDF

## Visa Country of Origin
NG

## EMNLP 2026 AI Reviewing Experiment
TODO: Discuss with team. This opts your paper into receiving an additional AI-generated review alongside human reviews. 
- **Yes** — you get an extra AI review (informational, doesn't replace human reviewers). Could be useful feedback.
- **No** — standard human-only review process.

No downside to opting in — it's experimental and supplementary. Recommendation: Yes.

## Software
TODO: Create a .zip archive containing evaluation scripts, prompts, and pipeline code from `anonymous-submission/scripts/`. Must be under 200MB and anonymised (no author names, no Azure keys, no .env files). Discuss with team whether to include this now or at camera-ready.

## Abstract
Existing benchmarks of vision-language models emphasize perception and reasoning accuracy (describing and inferring what they see in an image), while overlooking behavioral reliability under uncertainty (when visual evidence is missing or misleading). We introduce SciFig-Eval, a diagnostic benchmark for scientific figure understanding with 250 annotated figures and more than 34,000 evaluations across eight models. The benchmark combines MQM-based scoring, targeted reasoning questions, image perturbations, misleading captions, false-premise probes, and selective-blur tests. We further propose the Admittance-Resistance-Inductance (A-R-I) framework to evaluate whether models acknowledge insufficient evidence, resist misleading context, and infer cautiously from partial information. Our results reveal substantial behavioral differences among models with similar perception scores. GPT-5.2 achieves the highest description quality (MQM 91.6) but hallucinates unreadable content in 96% of cases, whereas Gemini 3.1 Pro attains comparable perception performance (MQM 90.2), admits uncertainty in 71% of such cases, and achieves the strongest resistance score (0.91). These findings show that high perception accuracy alone does not guarantee reliable scientific reasoning, highlighting the need for evaluation frameworks that explicitly measure robustness under uncertainty.
