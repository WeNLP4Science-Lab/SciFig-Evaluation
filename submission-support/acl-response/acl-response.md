How Do VLMs Behave When Blind or Misled? Behavioural Evaluation of VLMs on Scientific Figures
Download PDF
Paul Osemudiame Oamen, Owusu-Banahene Osei, Ananya Mukherjee, Christian Greisinger, Steffen Eger, Pius Onobhayedo, Wei Zhao 
26 May 2026 (modified: 24 Jun 2026)
ACL ARR 2026 May Submission
May, Senior Area Chairs, Area Chairs, Reviewers, Authors, Secondary Reviewers
Revisions
CC BY 4.0
Keywords: Scientific Figure Understanding, Vision-Language Models, Behavioural Evaluation, Hallucination Detection, Benchmark, Selective Blur, Admittance-Resistance-Inductance, Chart Understanding, MQM Evaluation, Epistemic Honesty
Abstract:
Existing benchmarks of vision-language models emphasize perception and reasoning accuracy (describing and inferring what they see in an image), while overlooking behavioral reliability under uncertainty (when visual evidence is missing or misleading). We introduce SciFig-Eval, a diagnostic benchmark for scientific figure understanding with 250 annotated figures and more than 34,000 evaluations across eight models. The benchmark combines MQM-based scoring, targeted reasoning questions, image perturbations, misleading captions, false-premise probes, and selective-blur tests. We further propose the Admittance-Resistance-Inductance (A-R-I) framework to evaluate whether models acknowledge insufficient evidence, resist misleading context, and infer cautiously from partial information. Our results reveal substantial behavioral differences among models with similar perception scores. GPT-5.2 achieves the highest description quality (MQM 91.6) but hallucinates unreadable content in 96% of cases, whereas Gemini 3.1 Pro attains comparable perception performance (MQM 90.2), admits uncertainty in 71% of such cases, and achieves the strongest resistance score (0.91). These findings show that high perception accuracy alone does not guarantee reliable scientific reasoning, highlighting the need for evaluation frameworks that explicitly measure robustness under uncertainty.

Paper Type: Long
Research Area: Multimodality and Language Grounding to Vision, Robotics and Beyond
Research Area Keywords: Benchmarking, evaluation methodologies, evaluation, NLP datasets, metrics, vision question answering, multimodality
Contribution Types: Model analysis & interpretability, NLP engineering experiment, Publicly available software and/or pre-trained models, Data resources
Languages Studied: English
Reassignment Request Area Chair: This is not a resubmission
Reassignment Request Reviewers: This is not a resubmission
A1 Limitations Section: This paper has a limitations section.
A2 Potential Risks: Yes
A2 Elaboration: See the Ethics Statement (unnumbered section, after Limitations). The benchmark reveals behavioural limitations of VLMs rather than developing adversarial attacks. Adversarial probes (false premises, misleading captions, selective blur) are diagnostic evaluation tools, not attack vectors. All figures are from openly accessible arXiv preprints with no personally identifiable information.
B Use Or Create Scientific Artifacts: Yes
B1 Cite Creators Of Artifacts: Yes
B1 Elaboration: 8 evaluated models are cited in Section 4.1 (Models) with references to their technical reports or model cards. The judge model (GPT-4o) and validator (Mistral Large 3) are also cited. Prior benchmarks (ChartQA, CharXiv, CHOCOLATE, CHAOS, etc.) are cited in Section 2 (Related Work).
B2 Discuss The License For Artifacts: Yes
B2 Elaboration: The Ethics Statement notes that all scientific figures are sourced from arXiv preprints, which are openly accessible and licensed for research use. The dataset, evaluation scripts, model outputs, and prompts will be released upon publication.
B3 Artifact Use Consistent With Intended Use: Yes
B3 Elaboration: See Ethics Statement. All VLMs are used via their public APIs for research evaluation, consistent with their terms of service. ArXiv figures are used for research purposes consistent with arXiv's open access licence. Our benchmark is intended for research evaluation of VLMs and is not designed for commercial deployment or adversarial attack development.
B4 Data Contains Personally Identifying Info Or Offensive Content: Yes
B4 Elaboration: See Ethics Statement. The dataset contains only scientific figures (bar charts, line plots, pie charts) from arXiv papers. No personally identifiable information is present. The figures depict quantitative research results, not personal data or offensive content.
B5 Documentation Of Artifacts: Yes
B5 Elaboration: Section 3.1 (Dataset) describes corpus composition (250 figures, 187 arXiv papers, 3 chart types, English-language, NLP/ML domain). The appendix provides a comprehensive dataset table (Table 5) with full breakdowns of all components, evaluation instances, and probe counts. Appendix E documents API configurations, model identifiers, and reproducibility details.
B6 Statistics For Data: Yes
B6 Elaboration: Section 3.1 (Dataset) provides a summary table with counts for all benchmark components (250 figures, 1,686 transforms, 1,000 reasoning questions, 1,293 behavioural probes). The appendix comprehensive table breaks down all evaluation instances per condition, model, and probe type, totalling 34,000+. Split-half reliability and scale convergence analyses are reported in the appendix.
C Computational Experiments: Yes
C1 Model Size And Budget: Yes
C1 Elaboration: Appendix E (API Configuration and Reproducibility) reports model identifiers, API backends (Azure, OpenRouter), and inference settings. The experimental setup table reports ~24,700 total API calls. Parameter counts are reported where publicly available (e.g. Llama 4 Maverick 17B×128E MoE, Qwen3-VL variants). Commercial model sizes (GPT-5.2, Gemini) are not publicly disclosed. No local GPU training was performed; all experiments use API-based inference.
C2 Experimental Setup And Hyperparameters: Yes
C2 Elaboration: Section 4 (Experiments and Results) and Appendix E (API Configuration and Reproducibility) report all inference settings: temperature=0 for all calls, max tokens=2,048 (Gemini: 16,000), seed=42, Azure API version. No hyperparameter search was conducted as all models use deterministic decoding at temperature 0.
C3 Descriptive Statistics: Yes
C3 Elaboration: Section 4 reports bootstrap 95% confidence intervals (B=10,000) for key comparisons, paired bootstrap significance tests with p-values, and Cliff's delta effect sizes. The experimental setup table states all results are from single deterministic runs (temperature=0). Appendix tables report per-chart-type and per-dimension breakdowns with bootstrap CIs. Split-half reliability (rho=0.979) validates ranking stability.
C4 Parameters For Packages: Yes
C4 Elaboration: The experimental setup table (Appendix) lists all software used: OpenAI Python SDK (API client), OpenCV/NumPy/Pillow (image processing), EasyOCR (text extraction), SciPy (bootstrap, Cliff's delta). Blur parameters are specified in Appendix D.6 (Gaussian kernel size 75, grey blend factor 0.7). Image transform parameters are in Appendix D.2 (noise sigma=25, contrast alpha=0.3/beta=50, rotation 15 degrees).
D Human Subjects Including Annotators: Yes
D1 Instructions Given To Participants: Yes
D1 Elaboration: Appendix A.1 (Human Validation) describes the annotation task (MQM scoring rubric, 0-100 scale). Annotators used the MQM checklist described in Section 3.2 and Appendix D.1. Capability question annotators used the dashboard review interface with clear task instructions. The Ethics Statement notes that human annotations were performed by consenting graduate researchers who were informed of the study's purpose. No risks to participants were identified as the task involves evaluating scientific figure descriptions.
D2 Recruitment And Payment: Yes
D2 Elaboration: Annotators were graduate researchers within the research group, not crowdworkers. They participated as part of their research activities, not as paid external participants. This is acknowledged in the Ethics Statement ("consenting graduate researchers who were informed of the study's purpose"). No external recruitment or payment was involved.
D3 Data Consent: Yes
D3 Elaboration: See Ethics Statement. Annotators were informed of the study's purpose and consented to participate. The scientific figures are from arXiv preprints which are publicly available under open access terms and do not require individual consent for research use.
D4 Ethics Review Board Approval: N/A
D4 Elaboration: The study involves evaluation of publicly available AI models on publicly available scientific figures. Annotators are graduate researchers within the team performing standard research tasks. No sensitive personal data, vulnerable populations, or deceptive protocols are involved. This type of NLP research is typically exempt from ethics board review.
E Ai Assistants In Research Or Writing: Yes
E1 Information About Use Of Ai Assistants: Yes
E1 Elaboration: Claude Code (Anthropic) was used to assist with code development, statistical analysis, and manuscript drafting. All scientific claims, experimental design decisions, and final text were reviewed and approved by the authors.
Author Submission Checklist: yes
EMNLP 2026 AI Reviewing Experiment: yes
TLDR: A benchmark for scientific figure understanding revealing that top-scoring VLMs can fabricate confidently when visual evidence is missing or misleading, and that perception quality alone does not predict behavioural reliability under uncertainty.
Preprint: no
Preprint Status: We are considering releasing a non-anonymous preprint in the next two months (i.e., during the reviewing process).
Preferred Venue: EMNLP
Visa Needs: yes
Consent To Share Data: yes
Consent To Share Submission Details: On behalf of all authors, we agree to the terms above to share our submission details.
Association For Computational Linguistics - Blind Submission License Agreement: On behalf of all authors, I agree
Submission Number: 14568
Discussion
Filter by reply type...
Filter by author...
Search keywords...

Sort: Newest First
3 / 3 replies shown
Add:
Official Review of Submission14568 by Reviewer h9tb
Official Reviewby Reviewer h9tb06 Jul 2026, 07:03 (modified: 08 Jul 2026, 23:59)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Reviewer h9tb, AuthorsRevisions
Paper Summary:
This paper introduces SCIFIG-EVAL, a diagnostic evaluation benchmark engineered to measure the behavioral reliability of Vision-Language Models (VLMs) under conditions of visual uncertainty and misleading context when processing scientific charts. The benchmark utilizes 250 English-language scientific figures (comprising 99 bar charts, 99 line plots, and 52 pie charts) curated from 187 arXiv papers, with each entry accompanied by high-quality human-annotated expert descriptions.

Summary Of Strengths:
The benchmark pipeline features exceptionally precise data interventions. By combining automatic EasyOCR coordinate mapping with a dual-stage blurring protocol (grey-blending plus heavy Gaussian blur), the authors create distinct Admittance Blur (unrecoverable details) and Inductance Blur (inferable variables) conditions. This elegantly differentiates structured visual deduction from ungrounded data fabrication.

This paper executes exhaustive validation steps to establish the neutrality of its automated metrics.

Summary Of Weaknesses:
Despite harvesting charts from authentic arXiv research papers, the dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding.

Section 5 notes that Inexist probes (which embed false assumptions via definite articles, e.g., asking about non-existent error bars) serve as the most potent deception vectors across all architectures due to a persistent "must answer" bias. However, the paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressure the model to comply with user prompts regardless of conflicting visual data.

Comments Suggestions And Typos:
please consistency writing the name of Llama 4

Confidence: 3 =  Pretty sure, but there's a chance I missed something. Although I have a good feel for this area in general, I did not carefully check the paper's details, e.g., the math or experimental design.
Soundness: 3 = Acceptable: This study provides sufficient support for its main claims. Some minor points may need extra support or details.
Excitement: 3.5
Overall Assessment: 3 = Findings: I think this paper could be accepted to the Findings of the ACL.
Ethical Concerns:
There are no concerns with this submission

Needs Ethics Review: No
Reproducibility: 5 = They could easily reproduce the results.
Datasets: 5 = Enabling: The newly released datasets should affect other people's choice of research or development projects to undertake.
Software: 5 = Enabling: The newly released software should affect other people's choice of research or development projects to undertake.
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I used a privacy-preserving tool exclusively for the use case(s) approved by PEC policy, such as language edits
Add:
Official Review of Submission14568 by Reviewer No6d
Official Reviewby Reviewer No6d30 Jun 2026, 16:14 (modified: 08 Jul 2026, 23:59)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Reviewer No6d, AuthorsRevisions
Paper Summary:
This paper presents SCIFIG-EVAL, a benchmark for evaluating vision-language models (VLMs) on scientific figures. Built from 250 arXiv figures, it assesses models along three axes: open-ended figure descriptions, targeted reasoning questions, and behavioral stress tests that include visual perturbations, misleading captions, false-premise questions, and selective blur. The authors also propose the Admittance-Resistance-Inductance (A-R-I) framework, which characterizes whether a model admits uncertainty when evidence is missing, resists misleading context, and infers cautiously from partial visual evidence.

Summary Of Strengths:
The paper is clearly written and tackles an important general problem: VLMs may hallucinate or behave unreliably when visual evidence is incomplete or misleading.

The evaluation is broad in scope, combining perception, reasoning, and behavioral probes within a single benchmark.

The results surface interesting differences between models that reach similar description quality but diverge sharply in how they handle uncertainty.

Summary Of Weaknesses:
Most of the stress tests build on existing ideas — image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment — rather than introducing new techniques. The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method.

The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots.

The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie). This is modest for a benchmark paper, particularly given that the probe types are themselves not especially novel.

Although the authors include some human validation, the main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report direct agreement between GPT-4o and humans, ideally at the item level. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified.

Comments Suggestions And Typos:
The authors should more strongly justify the real-world relevance of the proposed probes, ideally by grounding them in realistic failure cases from scientific workflows — for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines. It would also help to position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm.

Confidence: 3 =  Pretty sure, but there's a chance I missed something. Although I have a good feel for this area in general, I did not carefully check the paper's details, e.g., the math or experimental design.
Soundness: 2.5
Excitement: 2 = Potentially Interesting: this paper does not resonate with me, but it might with others in the *ACL community.
Overall Assessment: 2 = Resubmit next cycle: I think this paper needs substantial revisions that can be completed by the next ARR cycle.
Ethical Concerns:
There are no concerns with this submission

Needs Ethics Review: No
Reproducibility: 2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided.
Datasets: 2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)
Software: 2 = Documentary: The new software will be useful to study or replicate the reported research, although for other purposes it may have limited interest or limited usability. (Still a positive rating)
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I used a privacy-preserving tool exclusively for the use case(s) approved by PEC policy, such as language edits
Add:
Official Review of Submission14568 by Reviewer LhRb
Official Reviewby Reviewer LhRb24 Jun 2026, 06:42 (modified: 08 Jul 2026, 23:59)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Reviewer LhRb, AuthorsRevisions
Paper Summary:
This paper introduces SCIFIG-EVAL, a benchmark for evaluating VLM behavior on scientific figures when visual evidence is missing or misleading. The authors propose the A-R-I framework, Admittance, Resistance, and Inductance, to test whether models admit uncertainty, resist misleading context, and infer cautiously from partial evidence.

Summary Of Strengths:
I think the value of this paper is that it does not reduce scientific figure understanding to description quality or QA accuracy. It directly studies uncertainty behavior, which is important in scientific settings. If a model answers confidently when it cannot actually see the evidence, that can be more problematic than an ordinary mistake. I also appreciate the probe-designer ablation, human agreement check, and split-half stability analysis, which make the benchmark more convincing.

Summary Of Weaknesses:
My main reservation is about scale and dependence on automatic evaluation. 250 figures is still limited for the broad space of scientific figures. GPT-4o is used quite heavily in probe generation and judging. The validation helps, but I would still have liked to see broader human evaluation or more diverse figure sources. The A-R-I framework is useful, but I am not fully convinced that these three dimensions are sufficient to cover behavioral reliability.

Comments Suggestions And Typos:
I would suggest discussing more concretely how arXiv figure sampling affects benchmark coverage. The paper should also discuss model version drift, especially for API models such as GPT and Gemini. The A-R-I dimensions could be better justified as a necessary and relatively complete decomposition. I did not notice major typos.

Confidence: 4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.
Soundness: 3 = Acceptable: This study provides sufficient support for its main claims. Some minor points may need extra support or details.
Excitement: 3 = Interesting: I might mention some points of this paper to others and/or attend its presentation in a conference if there's time.
Overall Assessment: 3 = Findings: I think this paper could be accepted to the Findings of the ACL.
Ethical Concerns:
There are no concerns with this submission

Reproducibility: 3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.
Datasets: 3 = Potentially useful: Someone might find the new datasets useful for their work.
Software: 3 = Potentially useful: Someone might find the new software useful for their work.
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I used a privacy-preserving tool exclusively for the use case(s) approved by PEC policy, such as language edits