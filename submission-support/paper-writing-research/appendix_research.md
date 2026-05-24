# Appendix Research for SciFig-Eval ACL Submission

## 1. ACL/ARR 2024-2025 Appendix Conventions

### Page Limits
- **ACL/ARR: No page limit on appendix.** Long papers get 8 pages of content + unlimited references + unlimited appendix.
- **TACL (stricter):** 5 pages for replication details, 3 pages for complementary results/figures. No supplementary files allowed. (New policy effective March 2024.)
- **EMNLP 2025:** Same as ACL — unlimited appendix pages.

### Format Requirements
- **Double-column format required** (same ACL template). Starting July 2025, papers with appendices not in double-column format will be **desk rejected** (exception: math-heavy sections can use single-column for readability).
- Appendix appears **after the bibliography** in the same PDF.
- Must follow the same **anonymity guidelines** as the main paper.
- Separate supplementary archives (.tgz or .zip) allowed for software and data, but reviewers are not required to look at them.

### What MUST Be in Main Paper vs Appendix
**MUST be in main paper (not appendix):**
- Key results and findings
- Literature review / related work
- Core methodology (enough for a reviewer to understand the approach)
- Important figures and tables needed to interpret the paper
- The paper must be **self-contained and readable without the appendix**

**Appropriate for appendix:**
- Preprocessing decisions, model parameters, feature templates
- Lengthy proofs or derivations
- Pseudocode
- Sample system inputs/outputs
- Annotation guidelines
- Additional error analysis
- Details necessary for **replication**

### Critical Rule (Source: Ehud Reiter, March 2026 blog + ARR guidelines)
> "If the literature review or key results are in an appendix, I automatically reject the paper."
> — Ehud Reiter, senior ACL reviewer

Reviewers are **not required** to read the appendix. However, if a reviewer has a question and the paper explicitly refers to the appendix for that specific answer, looking it up saves time. Relegating something to the appendix that belongs in the main paper is a "reasonable suggestion to improve the paper" from reviewers, but not necessarily a fatal weakness.

### Responsible NLP Research Checklist
- At EMNLP 2025+, the checklist is published as an appendix to accepted papers.
- From December 2024, inappropriately filled checklists can be grounds for **desk rejection**.
- Authors must provide section references (not just yes/no) for each checklist item.
- The checklist covers: experimental details, annotation protocols, IRB approval, compute costs, bias discussion, data licensing, etc.

---

## 2. What Top Benchmark Papers Put in Appendix

### Common Appendix Sections in Benchmark/Evaluation Papers

Based on analysis of MathVista (ICLR 2024), HallusionBench (CVPR 2024), POPE, ChartQA, and AppWorld (ACL 2024):

| Section | Content | Who Does It |
|---------|---------|-------------|
| Dataset Details | Construction pipeline, filtering criteria, statistics, splits | All benchmark papers |
| Annotation Guidelines | Full guidelines given to annotators, examples of good/bad annotations | Most benchmark papers |
| Prompt Templates | Complete system prompts, user prompts, few-shot examples | All LLM-based papers |
| Per-Model Results | Full tables broken down by model, category, difficulty | All benchmark papers |
| Error Analysis | Categorized failure cases with examples | Most papers |
| Human Evaluation | Inter-annotator agreement, qualification criteria, interface screenshots | Papers with human eval |
| Statistical Tests | Full significance tables, confidence intervals, effect sizes | Rigorous papers |
| Additional Visualizations | Confusion matrices, distribution plots, heatmaps | Many papers |
| Compute Details | GPU hours, API costs, inference times | Reproducibility-focused |

### MathVista Appendix Structure (Exemplary — 40+ pages)
MathVista is the gold standard for benchmark paper appendices. Its appendix sections include:
- §A: Dataset statistics and construction details
- §B: Data source descriptions (all 31 source datasets)
- §C: Evaluation methodology details
- §D: Full prompt texts for all evaluation modes
- §E: Per-task-type results tables
- §F: Per-model detailed results
- §G: Error taxonomy with examples
- §H: In-depth analysis (GPT-4V capabilities, self-verification, self-consistency, multi-turn dialogue)

### HallusionBench Appendix
- Visual Dependent vs Visual Supplement question examples
- Full annotation protocol
- Per-model per-category breakdown tables
- Failure case galleries with model outputs

### ChartQA
- Chart type breakdowns
- Question complexity analysis
- Annotation interface details
- Human baseline construction

---

## 3. Appendix Organization Patterns

### Naming Convention
Standard ACL practice: **Appendix A, B, C** (not A.1, A.2 at top level). Use subsections within: **A.1, A.2, A.3**.

### Typical Section Count
- Minimum for a solid benchmark paper: **5-8 appendix sections**
- Top papers: **8-15 sections** (MathVista has 8 major sections, each with subsections)

### Cross-Referencing Pattern
In main paper text:
```latex
See Appendix~\ref{sec:appendix-prompts} for full prompt templates.
Full per-chart-type breakdowns appear in Table~\ref{tab:appendix-chart-mqm}.
```
**Best practice:** Every appendix section should be referenced from the main paper at least once. Orphan appendix sections suggest disorganization.

### Self-Contained vs Dependent
- Each appendix section should have a **1-2 sentence introduction** explaining what it contains and why
- Tables and figures in appendix should have **full captions** (not abbreviated)
- A reader should be able to jump to any appendix section and understand what they're looking at without reading the others
- But the appendix as a whole should NOT be needed to understand the main paper's claims

---

## 4. What Reviewers Check in Appendix

### Reproducibility Details (Most Important)
- **Prompts:** Full system + user prompts, not paraphrased. Reviewers want exact text.
- **Hyperparameters:** Temperature, top-p, max tokens, seed. For our paper: temperature=0 is critical to state.
- **API versions:** Model versions/dates, endpoints (Azure vs direct API).
- **Compute:** Total API calls, estimated cost, wall-clock time.

### Statistical Rigor
- Full significance test tables (not just "p < 0.05" claims)
- Per-condition breakdowns (not just aggregates)
- Confidence intervals or standard deviations
- Effect sizes where relevant

### Dataset Transparency
- Sample figures from the dataset
- Annotation examples (good and bad)
- Inter-annotator agreement details (Cohen's kappa, Krippendorff's alpha)
- Filtering/exclusion criteria

### Failure Analysis
- Categorized error examples with model outputs
- Specific failure patterns by model
- Visual examples showing what went wrong

### What Reviewers Do NOT Want in Appendix
- Key results they need to evaluate the paper's claims
- The only place where a methodology is explained
- Raw data dumps without organization or explanation

---

## 5. Recommended Appendix for SciFig-Eval

### Appendix A: MQM Checklist Definitions
**Content:**
- Full 14-item bar chart checklist with definitions and scoring criteria
- Full 15-item line chart checklist
- Full 11-item pie chart checklist
- Explanation of binding verification process
- Example of a scored checklist (one complete evaluation)
- Human validation protocol (how Spearman rho=1.0 was computed)

**Why:** Reviewers will want to see the exact items. Main paper should show 2-3 example items and the overall methodology. The full lists belong here.

**Cross-reference from main paper:** "The complete MQM checklists for all three chart types are provided in Appendix A."

### Appendix B: Judge and Generator Prompts
**Content:**
- System prompt for MQM judge evaluation
- User prompt template with placeholders
- Caption bias prompt variants (with-caption vs without-caption)
- Resistance probe templates: presupposition embedding, false premise anchoring, unanswerable domain
- Admittance/Inductance probe templates
- Transform description prompts

**Why:** This is the #1 thing reviewers check for reproducibility. Include exact text, not summaries.

**Cross-reference:** "Full prompts for all evaluation conditions appear in Appendix B."

### Appendix C: Dataset Construction
**Content:**
- Figure selection criteria and pipeline
- Source paper selection process
- Language distribution details (English, Chinese, Bulgarian, German, multi-language)
- Complexity criteria for adversarial subset (multi-panel, log-scale, error bars, dual-axis)
- Chart type distribution and balancing
- Groundtruth construction and audit process
- Selective blur target selection methodology and rules ("blur in-chart elements, not axis labels or margins")

**Cross-reference:** "Dataset construction details are in Appendix C."

### Appendix D: Model Details
**Content:**
- Full table of all 11 generator models with: API version/date, endpoint (Azure/OpenRouter/GCP), parameter settings (temperature=0, max_tokens, etc.)
- Full table of all 4 judge models with same details
- Judge backend configuration (OpenRouter, Azure OpenAI, GCP Vertex AI)
- Any model-specific notes (context window, vision resolution)
- Estimated API costs and total inference calls

**Cross-reference:** "Complete model configurations are provided in Appendix D."

### Appendix E: Per-Chart-Type MQM Results
**Content:**
- Table A.1: MQM scores by chart type (bar/line/pie) × model (already drafted as `table_a1_chart_type_mqm.tex`)
- Table A.2: MQM dimension breakdowns (already drafted as `table_a2_mqm_dimensions.tex`)
- Table A.3: Error subtype frequencies (already drafted as `table_a3_error_subtypes.tex`)
- Saturation curve analysis (if computed)

**Cross-reference:** "Per-chart-type MQM breakdowns appear in Appendix E (Tables 5-7)."

### Appendix F: Behavioral Probe Details
**Content:**
- Table A.4: Caption bias by chart type (already drafted)
- Table A.8: Resistance by chart type (already drafted)
- Table A.9: Cross-dimensional analysis (already drafted)
- Caption bias methodology: what counts as "biased" vs "resistant"
- Resistance probe design: how presupposition, false premise, and unanswerable probes were constructed
- Per-probe-type breakdown of resistance scores

**Cross-reference:** "Detailed behavioral probe results are in Appendix F."

### Appendix G: Statistical Analysis
**Content:**
- Table A.5: Full pairwise significance matrices (already drafted)
- Table A.6: Ablation results (already drafted)
- Table A.7: Stability analysis (already drafted)
- Statistical test methodology (which tests, corrections for multiple comparisons)
- Effect sizes
- Judge agreement analysis (inter-judge correlation)

**Cross-reference:** "Statistical significance results and ablation details are in Appendix G."

### Appendix H: A-R-I Framework Details
**Content:**
- Full Admittance-Resistance-Inductance definitions with scoring rubrics
- Selective blur methodology: how blur targets were selected, blur parameters
- Example figures: original vs blurred (2-3 visual examples)
- Per-model A-R-I scores broken down by chart type
- Example model outputs showing high-admittance vs low-admittance behavior
- Comparison of model responses to blurred vs original figures

**Cross-reference:** "Complete A-R-I framework definitions and selective blur examples are in Appendix H."

### Appendix I: Transform Robustness Details
**Content:**
- All 6 transforms with parameter values (JPEG quality level, noise sigma, rotation degrees, etc.)
- Visual examples of each transform applied to a sample figure
- Per-transform per-model results table
- In-paper page embedding methodology

**Cross-reference:** "Transform specifications and per-transform results are in Appendix I."

### Appendix J: Qualitative Examples
**Content:**
- 2-3 "good" model outputs (high MQM, correct under adversarial conditions)
- 2-3 "bad" model outputs (hallucination, caption bias capitulation, false precision under blur)
- Side-by-side comparisons for caption bias (with vs without misleading caption)
- Example of model admitting uncertainty vs fabricating data

**Why:** Reviewers love concrete examples. This makes the paper vivid and reviewable.

**Cross-reference:** "Representative model outputs are shown in Appendix J."

---

## 6. Common Appendix Mistakes to Avoid

### Too Sparse
- Just 2-3 extra tables with no explanation
- Missing the prompts (biggest reproducibility gap)
- No examples of actual model outputs

### Too Dense / Unorganized
- Dumping raw results without section headers
- No table captions or figure labels
- No introductory text explaining what each section contains

### Missing Critical Details
- Putting key methodology only in appendix (desk rejection risk)
- Not mentioning temperature, API versions, or model dates anywhere
- Claiming inter-annotator agreement without showing the protocol

### Not Cross-Referenced
- Appendix sections that are never mentioned in the main paper
- Reviewers won't discover orphaned appendix sections on their own

### Poor Formatting
- Switching to single-column without justification (desk rejection from July 2025)
- Inconsistent table formatting between main paper and appendix
- Missing page numbers or section labels

### Specific to Our Paper — Watch For:
- **Do NOT put the A-R-I framework explanation only in appendix** — the core concept must be in the main paper (Section 5.5), with details in appendix
- **Do NOT put Spearman rho=1.0 validation only in appendix** — this is a headline result that must be in the main paper
- **Do NOT put all model names only in appendix** — at minimum the main paper must list and briefly describe all 11 generators and 4 judges
- **DO put the full 14/15/11 checklists in appendix** — main paper needs 2-3 example items only
- **DO put full prompt texts in appendix** — main paper should describe the prompting strategy

---

## 7. The "Reproducibility Appendix" Pattern

### Checklist Approach (Preferred for ACL)
Structure the appendix so that each section of the ARR Responsible NLP Research Checklist can point to a specific appendix section:

| Checklist Item | Where Addressed |
|---------------|-----------------|
| Compute budget | Appendix D (Model Details) |
| Hyperparameter search | Appendix D + G (temperature=0, no search needed) |
| Dataset details | Appendix C (Dataset Construction) |
| Annotation process | Appendix A (MQM Checklists) + C |
| Prompt templates | Appendix B (Complete Prompts) |
| Statistical tests | Appendix G (Statistical Analysis) |
| Error analysis | Appendix J (Qualitative Examples) |
| Reproducibility | Appendix D (exact API versions + endpoints) |

### Code and Data Availability
- Include a statement about code/data release plans
- If anonymous during review: "Code and data will be released upon acceptance at [anonymized URL]."
- If using anonymous GitHub: ensure the repo is actually anonymized

### What Wins Reproducibility Recognition
Papers that win reproducibility recognition typically:
1. Provide exact prompts, not paraphrases
2. Report API versions and dates
3. Include per-run variance (even if temperature=0, show this)
4. Provide code and scripts
5. Document the full pipeline from raw data to reported numbers
6. Make it possible for someone to reproduce results without contacting the authors

---

## 8. Recommended Appendix Section Outline (Final)

```latex
\appendix

\section{MQM Checklist Definitions}
\label{sec:appendix-mqm}
% A.1 Bar Chart Checklist (14 items)
% A.2 Line Chart Checklist (15 items)
% A.3 Pie Chart Checklist (11 items)
% A.4 Binding Verification Protocol
% A.5 Scored Example

\section{Complete Evaluation Prompts}
\label{sec:appendix-prompts}
% B.1 MQM Judge System Prompt
% B.2 MQM Judge User Prompt Template
% B.3 Caption Bias Prompt Variants
% B.4 Resistance Probe Templates
% B.5 A-R-I Probe Templates
% B.6 Transform Description Prompts

\section{Dataset Construction}
\label{sec:appendix-dataset}
% C.1 Figure Selection Pipeline
% C.2 Source Paper Criteria
% C.3 Language Distribution
% C.4 Adversarial Subset Selection
% C.5 Groundtruth Construction and Audit
% C.6 Selective Blur Target Selection

\section{Model Configurations}
\label{sec:appendix-models}
% D.1 Generator Models (11 models: versions, endpoints, parameters)
% D.2 Judge Models (4 models: versions, endpoints, parameters)
% D.3 Compute Budget and API Costs

\section{Extended MQM Results}
\label{sec:appendix-mqm-results}
% E.1 Per-Chart-Type MQM Scores (Table A.1)
% E.2 MQM Dimension Breakdowns (Table A.2)
% E.3 Error Subtype Frequencies (Table A.3)

\section{Behavioral Probe Results}
\label{sec:appendix-behavioral}
% F.1 Caption Bias by Chart Type (Table A.4)
% F.2 Resistance by Chart Type (Table A.8)
% F.3 Cross-Dimensional Analysis (Table A.9)
% F.4 Per-Probe-Type Breakdowns

\section{Statistical Analysis}
\label{sec:appendix-stats}
% G.1 Pairwise Significance Matrices (Table A.5)
% G.2 Ablation Study (Table A.6)
% G.3 Stability Analysis (Table A.7)
% G.4 Inter-Judge Agreement

\section{A-R-I Framework and Selective Blur}
\label{sec:appendix-ari}
% H.1 Complete A-R-I Definitions and Scoring
% H.2 Selective Blur Parameters and Examples
% H.3 Per-Model A-R-I Breakdowns
% H.4 Example Model Outputs (Admittance vs Fabrication)

\section{Transform Robustness Details}
\label{sec:appendix-transforms}
% I.1 Transform Specifications (6 transforms + in-paper embedding)
% I.2 Visual Examples
% I.3 Per-Transform Per-Model Results

\section{Qualitative Examples}
\label{sec:appendix-examples}
% J.1 High-Quality Model Outputs
% J.2 Hallucination and Failure Cases
% J.3 Caption Bias: With vs Without Misleading Caption
% J.4 Blur Response: Honesty vs False Precision
```

### Estimated Length
- Sections A-B (Checklists + Prompts): ~4-5 pages
- Section C (Dataset): ~2 pages
- Section D (Models): ~1 page
- Sections E-G (Results + Stats): ~4-5 pages (mostly tables)
- Sections H-I (A-R-I + Transforms): ~3-4 pages
- Section J (Examples): ~2-3 pages
- **Total estimated: 16-20 pages**

This is within the normal range for top benchmark papers (MathVista: 40+ pages, HallusionBench: ~20 pages).

---

## Sources

- [ACL Paper Formatting Guidelines (ACLPUB)](https://acl-org.github.io/ACLPUB/formatting.html)
- [ACL Rolling Review — Call for Papers](http://aclrollingreview.org/cfp)
- [ACL Rolling Review — Author Checklist](http://aclrollingreview.org/authorchecklist)
- [ACL Rolling Review — Reviewer Guidelines](http://aclrollingreview.org/reviewerguidelines)
- [ACL Rolling Review — Responsible NLP Research Checklist](http://aclrollingreview.org/responsibleNLPresearch/)
- [EMNLP 2025 Checklist as Appendix Policy](http://aclrollingreview.org/responsible-nlp-checklist-appendices)
- [TACL New Appendices Policy](https://transacl.org/index.php/tacl/announcement/view/105)
- [Ehud Reiter — Please Follow the Rules for ARR/ACL Papers (March 2026)](https://ehudreiter.com/2026/03/16/please-follow-the-rules-for-arr-acl-papers/)
- [ARR Authors Guidelines](http://aclrollingreview.org/authors)
- [MathVista Paper (arXiv 2310.02255)](https://arxiv.org/abs/2310.02255)
- [HallusionBench (CVPR 2024)](https://openaccess.thecvf.com/content/CVPR2024/papers/Guan_HallusionBench_An_Advanced_Diagnostic_Suite_for_Entangled_Language_Hallucination_and_CVPR_2024_paper.pdf)
- [Responsible NLP Research Checklist PDF](https://aclrollingreview.org/static/responsibleNLPresearch.pdf)
- [Reproducibility in NLP: What Have We Learned from the Checklist?](https://arxiv.org/html/2306.09562)
