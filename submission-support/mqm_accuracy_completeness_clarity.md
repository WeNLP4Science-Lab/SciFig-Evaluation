# MQM Weight Assignment for Scientific Chart Description Evaluation

## Research Summary for ACL Submission

This document reviews evidence from the MQM literature, chart evaluation benchmarks, and cognitive science to inform weight selection in our adapted MQM framework for evaluating VLM-generated scientific figure descriptions.

---

## 1. Standard MQM Severity Weights

### 1.1 The Official MQM 2.0 Scoring Model

The MQM (Multidimensional Quality Metrics) framework defines three severity levels with recommended **Severity Penalty Multipliers** (SPMs) following an exponential scale (MQM Consortium, themqm.org):

| Severity | Weight |
|----------|--------|
| Neutral  | 0      |
| Minor    | 1      |
| Major    | 5      |
| Critical | 25     |

The exponential relationship (0-1-5-25) reflects increasing risk and impact between severity levels. This 1:5 Minor:Major ratio is the canonical MQM default, used in WMT shared tasks since 2021 (Freitag et al., 2021) and adopted widely in the language industry.

### 1.2 Error Type Weights (ETWs)

MQM separates **severity weights** from **error type weights** (ETWs). ETWs allow different error categories (e.g., Accuracy vs. Style) to carry different importance. Key design principles from the official MQM documentation:

- **Default ETW = 1** for all error types (i.e., all categories weighted equally by default).
- **Recommended ETW range: 0.5 to 2.0**, to "accentuate more than distort."
- Example: for legal content, Accuracy errors might receive ETW = 2 while Style errors receive ETW = 1, making a minor Accuracy error count as much as a minor Style error times two.

**Implication for our framework:** The standard MQM approach does not inherently privilege Accuracy over Completeness -- they are both subtypes of the same top-level Accuracy dimension in translation. Weighting them differently in our adapted framework is a design choice that must be justified.

### 1.3 The WMT Implementation

Freitag et al. (2021) operationalized MQM for WMT 2020 with weights Minor=1, Major=5, Critical=25. Subsequent WMT campaigns (2021-2023) maintained these severity weights. The score is computed as:

```
Score = -(sum of weighted penalties) / (number of source segments)
```

In the WMT implementation, **Omission and Mistranslation are both subtypes of the Accuracy dimension** and carry the same error type weight. They are differentiated only by severity (Major vs. Minor), not by category.

---

## 2. Omission vs. Mistranslation in Standard MQM

### 2.1 Same Parent Category, Same Weight

In the MQM Error Typology, the top-level **Accuracy** dimension contains three subtypes:

- **Mistranslation** (content is translated incorrectly)
- **Omission** (content is missing from the translation)
- **Addition** (content is added that was not in the source)

All three are children of the same Accuracy node and, by default, carry **identical error type weights** (ETW = 1). The severity of individual instances (Minor vs. Major) determines their penalty, not their subtype.

### 2.2 Rationale: Information Fidelity is Indivisible

The MQM design philosophy treats all accuracy failures as violations of information fidelity. Saying something wrong (mistranslation) and failing to say something (omission) are both distortions of the source content. The Multi-Range Theory of Translation Quality Measurement (Burchardt et al., 2024) reinforces that omission and mistranslation should carry the same base weight, with severity determining the magnitude of the penalty.

### 2.3 Implications for Our Framework

Our current weights give Completeness (Major=3.5, Minor=1.5) less weight than Accuracy (Major=5.0, Minor=2.0). In the MQM translation context, this would be analogous to weighting Omission less than Mistranslation -- a departure from the standard. The proposed equal weights (both Major=5.0, Minor=2.0) are more aligned with canonical MQM practice.

---

## 3. Chart Evaluation Benchmarks: How They Handle Accuracy vs. Completeness

### 3.1 CHOCOLATE (Huang et al., 2024)

CHOCOLATE introduces a factual error typology for chart captioning. Error categories include value errors, label errors, trend errors, and fabricated information. The framework focuses on **factual precision** (errors of commission) and does not separately weight omissions. Evaluation is via ChartVE (visual entailment), which checks whether the caption is entailed by the chart -- a binary accuracy check with no explicit completeness scoring.

**Key point:** CHOCOLATE treats omissions implicitly. A caption that omits key information is not penalized unless it makes a false claim.

### 3.2 ChartHal (Cui et al., 2025)

ChartHal evaluates hallucination in chart understanding across 12 hallucination-triggering scenarios. It uses accuracy on question-answer pairs rather than weighted error penalties. The framework does not distinguish omission severity from fabrication severity -- both are simply wrong answers.

### 3.3 FActScore (Min et al., 2023)

FActScore decomposes generated text into **atomic facts** and computes precision:

```
FActScore = (# supported atomic facts) / (# total atomic facts)
```

FActScore is explicitly a **precision-only** metric. It measures accuracy of what is said but **does not penalize omissions**. A description that states one correct fact and omits everything else scores 100%. This is a known limitation acknowledged by the authors, and subsequent work (e.g., Wei et al., 2025, "Beyond Precision") has proposed importance-aware recall to address it.

**Relevance to our work:** FActScore demonstrates that precision-only evaluation is insufficient for scientific descriptions, where coverage matters as much as correctness.

### 3.4 VisText (Tang et al., 2023)

VisText evaluates chart captions using standard NLG metrics (BLEU, ROUGE, WMD, TER) against reference captions. These metrics implicitly capture both accuracy and completeness through n-gram overlap, but do not explicitly weight them. A novel Visual Consistency Score regenerates a chart from the caption and measures similarity to the original, which implicitly rewards completeness.

**No explicit accuracy/completeness weight distinction.**

### 3.5 ChartBench (Xu et al., 2024)

ChartBench evaluates chart understanding via QA accuracy across multiple chart types and reasoning tasks. It uses binary correct/incorrect scoring without error severity weights.

### 3.6 CharXiv (Wang et al., 2024)

CharXiv uses two question types -- descriptive (basic elements) and reasoning (synthesis) -- evaluated by LLM-based grading of short answers. Binary accuracy, no weighted error framework.

### 3.7 REO Metric (Jiang et al., 2019)

The REO (Relevance, Extraness, Omission) metric is the closest existing work to our framework in separately measuring omission. It decomposes caption quality into three **independent, equally-weighted** scores using vector orthogonal projection. Relevance measures accuracy, Extraness measures hallucination, and Omission measures completeness. The three dimensions are treated as **co-equal** aspects of caption quality.

**Key finding:** The only benchmark that explicitly separates omission from accuracy treats them as equally important.

### 3.8 Summary Table

| Benchmark   | Accuracy/Completeness Distinction | Relative Weighting         |
|-------------|-----------------------------------|----------------------------|
| CHOCOLATE   | Accuracy only (precision)         | No completeness penalty    |
| ChartHal    | Binary QA                         | Equal (correct/incorrect)  |
| FActScore   | Precision only                    | No recall/completeness     |
| VisText     | Implicit via n-gram overlap       | Not distinguished          |
| ChartBench  | Binary QA                         | Equal                      |
| CharXiv     | Binary QA                         | Equal                      |
| REO         | Explicit three-way split          | Equal across all three     |

**No existing chart benchmark weights accuracy higher than completeness.** Those that distinguish the two at all treat them equally.

---

## 4. Omission vs. Inaccuracy in Scientific Communication

### 4.1 Research Integrity: Omission as Falsification

The U.S. Office of Research Integrity (ORI) explicitly states that **omission of data constitutes falsification** when it misleads the reader about the results of the research. Selective reporting -- intentionally omitting results -- is classified as an intermediate form of bias between data fabrication and legitimate data filtering (ORI, ori.hhs.gov).

### 4.2 Scientist Perceptions

Engineers and scientists perceive media inaccuracies primarily as **subjective omissions** of relevant information rather than outright factual errors (Peters et al., 1995). Studies of science journalism find that omission of limitations, caveats, and context is the most frequently cited form of inaccuracy by researchers whose work is covered.

### 4.3 Omission vs. Commission in Psychology

Feldman (2020) reviews 35+ years of research on the omission-commission asymmetry in judgment and decision-making:

- **Short-term:** Errors of commission (wrong information) generate more immediate regret and perceived harm.
- **Long-term:** Errors of omission (missing information) generate greater cumulative regret and are perceived as more harmful over time.
- **Moral judgments:** Omissions are judged as less wrong than commissions in the moment, but this reverses with temporal distance.

For scientific chart descriptions intended as lasting reference material, the long-term perspective is more relevant, suggesting **omissions are at least as harmful as inaccuracies**.

### 4.4 Distorted Science Communication

Research on science communication (Sumner et al., 2014; Adams et al., 2017) shows that omission of key results, limitations, and caveats in scientific reporting leads to:

- Public misunderstanding of scientific findings
- Unhealthy behavior changes based on incomplete information
- Decreased trust in scientific institutions

A chart description that omits a key result (e.g., failing to mention that one method significantly outperforms others) can be as misleading as one that misstates the result.

### 4.5 Implications

The weight of evidence supports treating omission and inaccuracy as equally harmful in scientific contexts. A description that says nothing about a critical chart element is as problematic as one that says something wrong about it: both distort the reader's understanding of the scientific content.

---

## 5. Clarity and Readability Weights

### 5.1 MQM Treatment of Fluency vs. Accuracy

In standard MQM, Fluency (covering grammar, style, readability) is a separate top-level dimension from Accuracy. By default, both have ETW = 1 (equal weight). However, MQM explicitly recommends that implementers **adjust ETWs based on content type**:

- For **informational/technical content**: Accuracy ETW > Fluency ETW (a factual error in a medical translation is worse than an awkward sentence).
- For **marketing/creative content**: Fluency ETW >= Accuracy ETW (readability and style matter as much as or more than literal accuracy).

### 5.2 Current and Proposed Weights

| Dimension              | Current (Major/Minor) | Proposed (Major/Minor) |
|------------------------|-----------------------|------------------------|
| Clarity and Readability | 2.0 / 1.0            | 2.5 / 1.0             |

The proposed change increases Major clarity errors from 2.0 to 2.5 while keeping Minor at 1.0.

### 5.3 Rationale for Lower Clarity Weights

Scientific figure descriptions are **informational content**. The primary purpose is to convey factual information accurately and completely; stylistic elegance is secondary. This aligns with:

- **MQM best practice** for technical content, where Accuracy should outweigh Fluency.
- **Existing benchmarks**, none of which give stylistic issues equal weight to factual errors.
- **The nature of the task**: a description that is factually correct but awkwardly written is far more useful than one that reads beautifully but misrepresents the chart.

### 5.4 Is 2.5/1.0 Reasonable?

With Accuracy and Completeness at 5.0/2.0, the proposed Clarity weights create these ratios:

- Major Accuracy/Completeness : Major Clarity = 5.0 : 2.5 = **2:1**
- Minor Accuracy/Completeness : Minor Clarity = 2.0 : 1.0 = **2:1**

A 2:1 ratio between factual and stylistic errors is well within the MQM-recommended ETW range of 0.5-2.0 and is consistent with the principle that factual errors should dominate scoring for technical content. The slight increase from 2.0 to 2.5 for Major clarity errors reflects that severely ambiguous or misleading phrasing in scientific writing can approach the harm of a factual error (e.g., a description so ambiguous that the reader cannot determine which data series is being discussed).

---

## 6. Score Distribution Implications: Equal vs. Unequal Weights

### 6.1 The Empty Description Problem

With our normalization formula:

```
MQM_score = max(0, 1 - (total_penalty / (num_items * max_weight)))
```

If `max_weight` is the highest weight in the system (currently 5.0 for Accuracy Major), then:

- **Unequal weights (current):** A description that is completely empty receives penalties only from Completeness errors (max weight 3.5). The total penalty for N items is `N * 3.5`, but the denominator is `N * 5.0`, yielding a minimum score of `1 - 3.5/5.0 = 0.30`. An empty description scores **30%**, which is incorrect -- it should score 0%.

- **Equal weights (proposed):** A completely empty description receives penalties from Completeness errors at weight 5.0. Total penalty = `N * 5.0`, denominator = `N * 5.0`, yielding `1 - 5.0/5.0 = 0.0`. An empty description correctly scores **0%**.

This is a strong mathematical argument for equal Accuracy and Completeness weights under this normalization scheme.

### 6.2 Impact on Model Discrimination

Equal weights will:

- **Increase the penalty range** for completeness errors, spreading out scores for models that differ in coverage.
- **Reduce the relative advantage** of terse-but-correct descriptions over verbose-but-complete descriptions.
- **Better discriminate** between models that are merely cautious (omitting uncertain information) vs. those that are genuinely informative.

### 6.3 Impact on Model Rankings

Models that generate short, conservative descriptions (high precision, low recall) will see their scores **decrease** under equal weights, since their completeness penalties now carry the same weight as accuracy penalties. Models that attempt comprehensive descriptions may see relative improvement, even if they incur some minor accuracy errors, because the penalty for omission is now commensurate with the penalty for inaccuracy.

This better reflects the intended use case: in scientific contexts, a description that captures all key chart elements with minor imprecisions is more valuable than one that describes two elements perfectly but ignores the rest.

---

## 7. The Minor:Major Ratio

### 7.1 Standard MQM Ratio

The canonical MQM ratio is **Minor=1 : Major=5** (i.e., 1:5), following the exponential severity scale 0-1-5-25 (MQM Consortium).

### 7.2 Our Ratio

Our current and proposed weights use a **Minor:Major ratio of 2:5** for Accuracy and Completeness:

| Category     | Major | Minor | Ratio (Minor:Major) |
|--------------|-------|-------|---------------------|
| Standard MQM | 5     | 1     | 1:5                 |
| Ours         | 5.0   | 2.0   | 2:5 (= 1:2.5)      |

Our ratio is **less steep** than the MQM default. A minor error in our framework carries 40% of the weight of a major error, compared to 20% in standard MQM.

### 7.3 Justification for a Flatter Ratio

The steeper 1:5 ratio was designed for translation, where minor errors (e.g., slightly unnatural phrasing) are genuinely trivial compared to major errors (e.g., meaning-changing mistranslation). In scientific chart description:

- **Minor accuracy errors** (e.g., reporting "approximately 45%" when the value is ~47%) still convey meaningful misinformation.
- **Minor completeness errors** (e.g., omitting tick interval information) still reduce the description's utility.

A 2:5 ratio better reflects the compressed severity range in chart description evaluation, where even minor errors have consequences for scientific interpretation.

### 7.4 Clarity Ratio

For Clarity and Readability, the proposed ratio is **Minor=1.0 : Major=2.5** (1:2.5), which is even flatter. This reflects the narrower impact range of stylistic issues: a major clarity error (ambiguous reference) and a minor one (verbose phrasing) are less differentiated than factual error severities.

---

## 8. Human Evaluator Behavior: Completeness vs. Accuracy

### 8.1 Inter-Annotator Agreement in MQM

Lommel, Burchardt, and Popovic (2014) found low inter-annotator agreement (kappa = 0.25-0.34) in MQM annotation overall, but noted that **omission errors achieve better agreement** than other error types because they are more objectively identifiable -- either content is present or it is not.

This has two implications for our work:

1. **Completeness errors are more reliably annotated** than accuracy errors, making them a more stable signal for evaluation.
2. **If human judges can reliably identify omissions, they should be weighted commensurately** with the errors they can less reliably identify (accuracy), to avoid systematic underweighting of the more reliable signal.

### 8.2 Freitag et al. (2021) WMT Study

In the largest MQM study to date, Freitag et al. found that professional translators, given the full MQM typology with equal weights for omission and mistranslation subtypes, produced rankings that **substantially differed** from crowd-worker holistic ratings. This suggests that explicit error annotation with appropriate weights yields more discriminating evaluation than holistic human judgment.

### 8.3 MQM Re-Annotation Studies

Recent MQM re-annotation work (Zouhar et al., 2025) shows that collaborative re-annotation improves agreement, and that **category-level agreement is higher than span-level agreement**. For our framework, which annotates at the category level (Accuracy/Completeness/Clarity) rather than highlighting specific spans, this suggests our annotations should be reasonably reliable.

### 8.4 Omission Bias in Human Evaluation

Cognitive research on omission bias (Spranca et al., 1991; Baron & Ritov, 2004) shows that human judges systematically **underweight omissions relative to commissions** in moral and quality judgments. This is a cognitive bias, not a rational assessment of harm. Explicit equal weighting in a rubric counteracts this bias, producing evaluations that better reflect the actual harm of missing information.

---

## 9. Recommendation

### 9.1 Proposed Weights

| Category                | Major | Minor |
|-------------------------|-------|-------|
| Accuracy                | 5.0   | 2.0   |
| Completeness            | 5.0   | 2.0   |
| Clarity and Readability | 2.5   | 1.0   |

### 9.2 Justification Summary

1. **MQM precedent:** Standard MQM treats Omission and Mistranslation as equal subtypes of Accuracy (same ETW). Equal Accuracy/Completeness weights are the canonical default.

2. **Normalization correctness:** Under our scoring formula, unequal weights produce a mathematical artifact where empty descriptions score above zero. Equal weights fix this.

3. **Benchmark alignment:** No existing chart evaluation benchmark weights accuracy higher than completeness. The REO metric (the only one that separates them) treats them as co-equal.

4. **Scientific communication norms:** Research integrity standards classify omission as a form of falsification. In scientific contexts, missing a key result is as misleading as misstating it.

5. **Cognitive bias correction:** Human judges systematically underweight omissions. Explicit equal weighting counteracts this documented bias.

6. **Clarity subordination:** A 2:1 ratio of factual-to-stylistic weights is within MQM's recommended ETW range and reflects the informational purpose of scientific chart descriptions.

---

## References

1. **MQM Consortium.** *The MQM Scoring Models.* https://themqm.org/error-types-2/the-mqm-scoring-models/

2. **MQM Consortium.** *The MQM Error Typology.* https://themqm.org/error-types-2/typology/

3. **MQM Consortium.** *Values and Scores.* https://themqm.org/error-types-2/values-and-scores/

4. **Freitag, M., Foster, G., Grangier, D., Ratnakar, V., Tan, Q., & Macherey, W.** (2021). Experts, Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation. *Transactions of the Association for Computational Linguistics*, 9, 1460-1474. https://aclanthology.org/2021.tacl-1.87/

5. **Burchardt, A., Lommel, A., & Popovic, M.** (2024). The Multi-Range Theory of Translation Quality Measurement: MQM Scoring Models and Statistical Quality Control. *arXiv preprint*. https://arxiv.org/abs/2405.16969

6. **Lommel, A., Burchardt, A., & Popovic, M.** (2014). Assessing Inter-Annotator Agreement for Translation Error Annotation. *Proceedings of LREC 2014*. https://www.dfki.de/fileadmin/user_upload/import/7445_LREC-Lommel-Burchardt-Popovic.pdf

7. **Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, P., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H.** (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. *Proceedings of EMNLP 2023*. https://aclanthology.org/2023.emnlp-main.741/

8. **Huang, K.-H., et al.** (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. *Findings of ACL 2024*. https://aclanthology.org/2024.findings-acl.41/

9. **Cui, Y., et al.** (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. *arXiv preprint*. https://arxiv.org/abs/2509.17481

10. **Tang, B., Boggust, A., & Satyanarayan, A.** (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. *Proceedings of ACL 2023*. https://aclanthology.org/2023.acl-long.401/

11. **Wang, Z., et al.** (2024). CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs. *Proceedings of NeurIPS 2024 Datasets and Benchmarks Track*. https://arxiv.org/abs/2406.18521

12. **Jiang, M., Huang, Q., Zhang, L., Wang, X., Zhang, P., Gan, Z., Diesner, J., & Gao, J.** (2019). REO-Relevance, Extraness, Omission: A Fine-grained Evaluation for Image Captioning. *Proceedings of EMNLP-IJCNLP 2019*. https://aclanthology.org/D19-1156/

13. **Feldman, G.** (2020). Omission and commission in judgment and decision making: Understanding and linking action-inaction effects using the concept of normality. *Social and Personality Psychology Compass*, 14(8). https://compass.onlinelibrary.wiley.com/doi/10.1111/spc3.12557

14. **Spranca, M., Minsk, E., & Baron, J.** (1991). Omission and commission in judgment and choice. *Journal of Experimental Social Psychology*, 27(1), 76-105.

15. **Baron, J., & Ritov, I.** (2004). Omission bias, individual differences, and normality. *Organizational Behavior and Human Decision Processes*, 94(2), 74-85.

16. **Office of Research Integrity.** Selective Reporting of Results. https://ori.hhs.gov/selective-reporting-results

17. **Moorkens, J., Castilho, S., Gaspari, F., & Doherty, S.** (Eds.) (2018). *Translation Quality Assessment: From Principles to Practice.* Machine Translation Series, Springer.

18. **Zouhar, V., et al.** (2025). MQM Re-Annotation: A Technique for Collaborative Evaluation of Machine Translation. *arXiv preprint*. https://arxiv.org/abs/2510.24664

19. **Wei, J., et al.** (2025). Beyond Precision: Importance-Aware Recall for Factuality Evaluation in Long-Form LLM Generation. *arXiv preprint*. https://arxiv.org/abs/2604.03141

20. **Xu, Z., et al.** (2024). ChartBench: A Benchmark for Complex Visual Reasoning in Charts. *arXiv preprint*. https://arxiv.org/abs/2312.15915

21. **Park, S., et al.** (2024). Multi-Dimensional Machine Translation Evaluation: Model Evaluation and Resource for Korean. *arXiv preprint*. https://arxiv.org/abs/2403.12666

22. **Sumner, P., et al.** (2014). The association between exaggeration in health related science news and academic press releases. *BMJ*, 349, g7015.
