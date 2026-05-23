# Evaluating Clarity and Readability in Scientific Chart Descriptions: A Research Survey for MQM-Based Evaluation

## 1. How Existing Benchmarks Define and Evaluate Clarity

### 1.1 VisText (Tang et al., 2023)

VisText does not isolate clarity as a standalone evaluation dimension. Instead, it defines a semantic level hierarchy (building on Lundgard and Satyanarayan, 2022) where captions are classified as L1 (elemental/encoded properties), L2 (statistical and relational), or L3 (perceptual and cognitive phenomena). Clarity is implicitly evaluated through a qualitative error analysis that identifies six error categories in generated captions, including **repetition** (models restating the same information), **nonsensical text** (incoherent output), and **directional errors** (stating a trend is declining when it is increasing). The first two categories map directly onto our "Overly Verbose" and "Poor Sentence Structure" sub-types, while directional errors straddle clarity and accuracy -- the statement may be grammatically clear but factually misleading.

VisText's error taxonomy reveals that clarity failures in chart captioning are typically entangled with factual failures: a model rarely produces a perfectly accurate but poorly phrased caption, but it frequently produces fluent text with wrong content.

### 1.2 Chart-to-Text (Kantharaj et al., 2022)

Chart-to-Text evaluates generated summaries along three human evaluation dimensions: **fluency**, **informativeness**, and **factual correctness**. Fluency is the closest proxy for clarity, defined as whether the summary is grammatically correct and reads naturally. Their analysis found that "while the best models usually generate fluent summaries and yield reasonable BLEU scores, they also suffer from hallucinations and factual errors as well as difficulties in correctly explaining complex patterns and trends." This finding is significant: models tend to be fluent (clear) but inaccurate, suggesting that in the chart domain, clarity is often the easier dimension while accuracy is the bottleneck.

### 1.3 ChartSumm (Rahman et al., 2023)

ChartSumm extends Chart-to-Text with 84,363 charts and uses BLEURT, CIDEr, and Content Selection (CS) metrics. These automatic metrics do not separate clarity from content quality. The authors note that models "often face issues like suffering from hallucination, missing out important data points, in addition to incorrect explanation of complex trends." Clarity is not evaluated independently; the implicit assumption is that transformer-generated text is generally fluent.

### 1.4 CHOCOLATE (Huang et al., 2024)

CHOCOLATE focuses specifically on **factual errors** in chart captions, establishing a typology that includes Value Error, Label Error, Trend Error, and other categories. The benchmark found that 82.06% of generated captions contain at least one factual error. Critically, CHOCOLATE does not evaluate clarity at all -- it treats caption quality as primarily a factual correctness problem. This omission actually supports the argument that clarity assessment requires a separate evaluation dimension, because factual-error-only evaluation misses important quality failures like ambiguity and verbosity.

### 1.5 SciCap and SciCap-Eval (Hsu et al., 2021; Hsu et al., 2023)

SciCap-Eval is the most relevant benchmark for clarity evaluation. It contains human judgments for 3,600 scientific figure captions and uses a holistic quality score (1-6) based on "potential to aid reader understanding." The companion tool **SciCapenter** (Hsu et al., 2024) provides a checklist that evaluates captions on six aspects: **Helpfulness**, **OCR mention**, **Takeaway**, **Visual Properties**, **Relation**, and **Stats**. Among these, Helpfulness and Takeaway are the dimensions most closely related to clarity.

A key finding from SciCap-Eval: less-experienced readers (undergraduates) cared more about **clear takeaway messages**, while expert readers (PhD students) prioritized **numerical precision and technical detail**. This suggests that clarity evaluation is audience-dependent, and an MQM framework should specify the assumed audience.

### 1.6 Summary Table

| Benchmark | Clarity Evaluated? | How? | Key Limitation |
|-----------|-------------------|------|---------------|
| VisText | Implicitly | Error taxonomy (repetition, nonsensical) | No standalone clarity metric |
| Chart-to-Text | Partially | Fluency dimension in human eval | Fluency is narrow (grammar only) |
| ChartSumm | No | Automatic metrics only | Metrics conflate all dimensions |
| CHOCOLATE | No | Factual errors only | Misses non-factual quality issues |
| SciCap-Eval | Partially | Holistic helpfulness score | Does not decompose clarity sub-types |
| SciCapenter | Partially | Checklist (Helpfulness, Takeaway) | Binary checklist, no severity |


## 2. Is Clarity Independent from Accuracy/Completeness?

Research consistently shows that clarity, accuracy, and completeness are **correlated but not redundant** dimensions.

### 2.1 The Reiter Framework

Reiter (2019) establishes three evaluation dimensions for NLG: **accuracy** (content is correct), **fluency/clarity** (text is readable), and **utility** (text is useful). Crucially, he argues these "are not independent; for example a text with poor linguistic quality will not be useful, and may have unknown accuracy (if we don't understand the text, we cannot check if it's accurate)." However, the reverse does not hold -- a text can be perfectly clear and fluent while being completely wrong. This asymmetry means clarity is necessary but not sufficient for quality.

### 2.2 UniEval Evidence

Zhong et al. (2022) in UniEval evaluated text across four dimensions -- coherence, consistency, fluency, and relevance -- and found that these dimensions are partially correlated but capture distinct quality aspects. UniEval achieves 23% higher correlation with human judgments on summarization compared to single-dimension evaluators, precisely because each dimension captures unique signal.

### 2.3 Chart-Specific Evidence

In the chart description domain specifically:
- Chart-to-Text (Kantharaj et al., 2022) found that models routinely score high on fluency but low on factual correctness, confirming that clarity and accuracy are separable.
- CHOCOLATE (Huang et al., 2024) found 82% of captions have factual errors despite being generally fluent, further confirming independence.
- SciCap-Eval (Hsu et al., 2023) found only moderate correlation (Kendall tau = 0.401) between GPT-4's holistic quality scores and human rankings, suggesting that LLM judges may weight clarity differently than humans weight accuracy.

### 2.4 Implications for Our Framework

Clarity should be evaluated as a **separate dimension** from accuracy and completeness, with its own weight in the MQM score. Our current weight matrix (Accuracy: Major=5.0/Minor=2.0; Completeness: 3.5/1.5; Clarity: 2.0/1.0) correctly assigns clarity the lowest weight, consistent with the finding that in scientific chart descriptions, accuracy failures are more damaging than clarity failures. However, clarity errors should still be flagged because they compound with accuracy errors -- an inaccurate description that is also unclear is worse than an inaccurate but clearly stated description (the reader can at least identify the error in the latter case).


## 3. How an LLM Judge Should Assess Clarity

### 3.1 Known LLM Judge Biases

Research on LLM-as-judge evaluation reveals several biases directly relevant to clarity assessment:

1. **Verbosity bias**: LLMs systematically prefer longer, more verbose outputs regardless of substantive quality (Saito et al., 2023). GPT-4 prefers longer answers more than humans do. This is particularly problematic for our "Overly Verbose" sub-type -- an LLM judge may fail to penalize unnecessary repetition.

2. **Position bias**: Judges may favor responses based on presentation order, with accuracy shifts exceeding 10% from simple response-order swaps (Zheng et al., 2023).

3. **Fluency-quality conflation**: LLM judges "often prefer verbose, formal, or fluent outputs regardless of substantive quality -- an artifact of generative pretraining and RLHF" (survey by Li et al., 2024).

### 3.2 Recommended Assessment Signals

For each clarity sub-type, the LLM judge should look for specific, operationalizable signals rather than holistic impressions:

**Ambiguous Description:**
- Pronouns without clear antecedents ("it increases" -- what increases?)
- Vague quantifiers ("some bars," "several categories") when specific labels are visible
- Hedging language that obscures factual claims ("appears to show," "seems like")

**Missing Takeaway:**
- Absence of any sentence describing the overall pattern, trend, or main finding
- Description that only lists individual data points without synthesizing

**Over-Generalization:**
- Absolute claims where the data shows exceptions ("all bars increase" when one decreases)
- Superlative language not supported by the data ("dramatically," "significantly" without evidence)
- Trend claims that ignore important deviations

**Overly Verbose:**
- Repeated information stated in different words
- Unnecessary qualifiers and filler phrases
- Description length > 2x the information content (as measured by unique claims)

**Poor Sentence Structure:**
- Subject-verb disagreement
- Run-on sentences
- Awkward passive constructions that obscure the agent
- Nested clauses exceeding 3 levels deep

### 3.3 Mitigation Strategies for Bias

To counteract known LLM judge biases:
- Use **structured rubrics** with binary yes/no questions per sub-type rather than holistic scoring
- Include **explicit length-neutrality instructions** ("A shorter description that covers the same information is not worse than a longer one")
- Use **chain-of-thought prompting** to force the judge to cite specific text spans as evidence for each error
- Consider **calibration examples** showing both over-verbose and appropriately concise descriptions rated correctly


## 4. Should "Missing Takeaway" Be a Clarity Issue or a Completeness Issue?

This is a genuine taxonomic boundary problem. The research provides arguments for both positions.

### 4.1 Arguments for Clarity

Lundgard and Satyanarayan (2022) define Level 3 content as "larger takeaways, such as trends and patterns." In their framework, a description can be complete at L1/L2 (listing all data points and statistics) without providing an L3 takeaway. The takeaway is what makes the description **interpretable** and **useful**, which is a communicative quality -- a matter of how well the description serves the reader, not whether it covers all data items.

SciCap-Eval found that less-experienced readers prioritize clear takeaway messages over numerical precision. From the reader's perspective, a description without a takeaway feels unclear about what the chart means, even if it is factually comprehensive.

In MQM translation evaluation, the Fluency dimension includes "register" and "style" sub-types that address whether the text achieves its communicative purpose -- analogous to whether a chart description conveys the "so what."

### 4.2 Arguments for Completeness

A takeaway is fundamentally **content** -- it is information about what the data shows. Not providing it means the description is missing information, which is the definition of incompleteness. The SciCapenter checklist (Hsu et al., 2024) treats "Takeaway" as one of its six quality aspects alongside "OCR mention" and "Stats," all of which are content coverage items.

CHOCOLATE (Huang et al., 2024) and VisText (Tang et al., 2023) both treat the failure to describe trends as a factual/content issue, not a clarity issue.

### 4.3 Recommendation

**Keep "Missing Takeaway" under Clarity, but annotate it as a boundary case.** The rationale:

1. Our checklist items already cover completeness at the item level (e.g., "trends correctly described," "comparisons stated"). If these items are satisfied, the raw content for a takeaway is present -- the failure is in not synthesizing it into a reader-facing summary.

2. A description can satisfy every checklist item (all facts reported) and still fail to communicate the chart's main message. That communicative failure is a clarity problem.

3. Keeping it under Clarity avoids double-penalizing: if we put it under Completeness, a model that describes trends but fails to provide a summary sentence would be penalized for both "missing takeaway" (Completeness) and the same information gap captured by existing trend-related checklist items.

4. However, if our checklist does NOT include trend/pattern items, then "Missing Takeaway" should move to Completeness, as it would then be the only mechanism to capture this content gap.


## 5. Is Verbosity Actually a Problem in Scientific Descriptions?

### 5.1 Evidence That More Detail Helps

- Expert audiences expect "the greatest level of detail and comprehensive presentation" (tailored communication literature).
- SciCap-Eval (Hsu et al., 2023) found that PhD students preferred descriptions with more numerical precision and technical detail.
- For accessibility, Lundgard and Satyanarayan (2022) found that blind readers wanted descriptions covering all four semantic levels, suggesting that more content is better for this audience.

### 5.2 Evidence That Verbosity Hurts

- **Repetition degrades quality**: VisText (Tang et al., 2023) identified repetition as one of six common captioning errors, where models restate the same information in slightly different words.
- **Verbosity correlates with hallucination**: longer generated descriptions have more opportunities for factual errors. CHOCOLATE (Huang et al., 2024) found that models with longer average caption lengths tended to have higher error rates.
- **Reader efficiency**: Scientific figure captions in publications are typically 100 words or fewer. Excessively long descriptions impose a cognitive load that undermines their purpose.
- **Verbosity bias in training**: Saito et al. (2023) showed that training with LLM feedback when verbosity bias is present leads to models generating excessively long responses, creating a self-reinforcing cycle.

### 5.3 The Key Distinction

The literature supports distinguishing between **information density** and **verbosity**:
- High information density (many unique facts, minimal redundancy) = good, even if the description is long
- Low information density (repeated facts, filler phrases, hedging language) = bad, regardless of length

For our framework, "Overly Verbose" should not penalize long descriptions per se. It should penalize descriptions where the ratio of unique claims to total word count is low -- i.e., descriptions that are long without being informative. An operational test: if a sentence can be removed without losing any information, it is verbose.


## 6. How Do Human Annotators Reliably Assess Clarity?

### 6.1 Inter-Annotator Agreement Patterns

Human agreement on clarity is consistently **lower** than agreement on factual accuracy:

- In readability assessment generally, Quadratic Weighted Kappa averages around 0.81 (substantial agreement), but this is for well-defined readability scales, not free-form quality judgments (Arabic readability corpus study).
- SciCap-Eval (Hsu et al., 2023) found significant divergence between expert and non-expert raters on overall caption quality, with differences reflecting "differing perspectives on caption quality." PhD students and undergraduates disagreed substantially on what makes a good caption.
- The MQM framework (Lommel et al., 2014) addresses this by decomposing clarity into specific error types with severity levels, which improves annotator agreement compared to holistic clarity ratings. In MQM translation evaluation, inter-annotator agreement on fluency error spans is moderate (Cohen's kappa ~0.4-0.6) compared to higher agreement on accuracy errors (~0.6-0.8).

### 6.2 Why Clarity Agreement Is Lower

Several factors contribute:
1. **Subjectivity**: What counts as "awkward phrasing" varies by reader background and language norms.
2. **Audience dependence**: Expert readers tolerate technical jargon that non-experts find unclear.
3. **Threshold effects**: Minor fluency issues are harder to consistently flag than factual errors, which are either correct or not.
4. **Interaction with content knowledge**: A description may seem unclear to someone who does not understand the domain, but perfectly clear to a domain expert.

### 6.3 Best Practices for Reliable Annotation

Based on the MQM framework and NLG evaluation literature:

1. **Use error-span annotation, not holistic scores**: Annotators should highlight specific text spans and classify them by error type (ambiguous, verbose, etc.), not rate overall "clarity" on a Likert scale.
2. **Provide calibration examples**: For each sub-type, provide 2-3 clear examples and 2-3 borderline cases with their correct labels.
3. **Define the audience**: Explicitly state that the target audience is "a researcher reading the paper" to anchor judgments.
4. **Separate passes**: Have annotators first read for comprehension, then do a second pass for error annotation. This reduces the tendency to conflate "I don't understand" (clarity) with "this is wrong" (accuracy).
5. **Binary first, severity second**: For each flagged span, first classify the error type, then assign severity. This two-step process improves consistency.


## 7. Operationalized Criteria for Each Sub-Type

### 7.1 Ambiguous Description

| Criterion | Severity | Operationalization |
|-----------|----------|-------------------|
| Pronoun without clear antecedent | Minor | Any pronoun (it, they, this) where the referent is ambiguous given the preceding 2 sentences |
| Vague reference to chart elements | Minor | Using "some," "several," "a few" when the exact count or labels are determinable from the chart |
| Ambiguous comparison | Major | A comparative statement (higher, lower, more) where both the referent and the comparand are not explicitly named |
| Hedging on determinable facts | Minor | Using "appears to," "seems to," "might" for facts that are unambiguously determinable from the chart |

**LLM Judge Signal**: Check if every claim names its subject explicitly. Flag sentences where removing the chart image would make the sentence's referent unknowable.

### 7.2 Missing Takeaway

| Criterion | Severity | Operationalization |
|-----------|----------|-------------------|
| No summary of overall pattern | Major | The description contains no sentence that characterizes the chart's main message (e.g., "overall, X increases with Y" or "the dominant category is Z") |
| Only lists data without synthesis | Minor | The description mentions 3+ data points but never relates them to each other or to a broader pattern |

**LLM Judge Signal**: Check for the presence of at least one sentence that would qualify as Lundgard and Satyanarayan's Level 3 (perceptual/cognitive takeaway). If the description only contains L1 (construction) and L2 (statistics) content, flag Missing Takeaway.

### 7.3 Over-Generalization

| Criterion | Severity | Operationalization |
|-----------|----------|-------------------|
| False universal claim | Major | Using "all," "every," "none" when the data contains exceptions |
| Exaggerated magnitude | Minor | Using "dramatically," "significantly," "vastly" without quantitative support |
| Simplified trend | Minor | Describing a non-monotonic trend as monotonic (e.g., "steadily increasing" when there are dips) |
| Omitted caveats | Minor | Describing a general trend without mentioning notable outliers or exceptions that are visually prominent |

**LLM Judge Signal**: Check absolute claims against checklist items. If the checklist confirms exceptions to a stated pattern, flag Over-Generalization. Cross-reference with accuracy errors -- an over-generalization that leads to a factual error should be scored under Accuracy, not Clarity.

### 7.4 Overly Verbose

| Criterion | Severity | Operationalization |
|-----------|----------|-------------------|
| Exact repetition | Minor | The same fact is stated in two or more sentences with different wording |
| Filler phrases | Minor | Phrases like "It is worth noting that," "It should be mentioned that," "As can be seen from the chart" that add no information |
| Redundant enumeration | Minor | Listing every single data point when a summary with range would suffice (e.g., listing all 20 bar values instead of stating range and notable items) |
| Excessive qualification | Minor | Multiple hedge phrases per sentence ("It appears that it might possibly be the case that...") |

**LLM Judge Signal**: Count unique factual claims vs. total sentences. If the ratio of unique claims to sentences drops below 0.5, flag verbosity. Note: this sub-type should never be Major severity, as verbosity alone does not undermine scientific interpretation -- it only wastes reader time.

**Important caveat**: The LLM judge's own verbosity bias (Saito et al., 2023) means it will under-detect this error type. Explicit instructions to penalize repetition and filler are necessary.

### 7.5 Poor Sentence Structure

| Criterion | Severity | Operationalization |
|-----------|----------|-------------------|
| Grammatical error | Minor | Subject-verb disagreement, tense inconsistency, article errors |
| Run-on sentence | Minor | A sentence containing 3+ independent clauses without proper conjunction or punctuation |
| Ambiguity from structure | Major | A sentence where the grammatical structure creates factual ambiguity (e.g., dangling modifier that changes which element a description refers to) |
| Nonsensical output | Major | A sentence that is grammatically broken to the point of unintelligibility |

**LLM Judge Signal**: For grammar, LLMs are strong detectors -- they can identify most grammatical errors reliably. The main risk is false positives on domain-specific constructions. For structural ambiguity, the judge should attempt to paraphrase each sentence; if the paraphrase changes the meaning, the original has structural ambiguity.

**Note on severity**: Most sentence structure errors are Minor in the MQM framework (Lommel et al., 2014), since "unnaturalness errors generally have a minor impact on translation quality compared to other sub-error types." The exception is when poor structure creates factual ambiguity, which should be Major because it affects interpretation.


## 8. Synthesis and Recommendations

### 8.1 Key Takeaways

1. **No existing benchmark isolates clarity** with the granularity our MQM framework targets. SciCap-Eval comes closest but uses holistic scores. Our five-sub-type decomposition is a contribution.

2. **Clarity is separable from accuracy** but not fully independent. In chart descriptions, clarity failures are rarer and less damaging than accuracy failures, supporting our lower weights.

3. **LLM judges have a systematic blind spot for verbosity**. The evaluation prompt must explicitly counteract verbosity bias.

4. **"Missing Takeaway" is defensibly placed under Clarity** as long as our completeness checklists cover the underlying factual content (trends, comparisons).

5. **Verbosity is a real problem** in generated chart descriptions, but must be distinguished from appropriate detail. The signal is information density, not length.

6. **Human agreement on clarity is moderate** (kappa ~0.4-0.6 for error spans), lower than on accuracy. Our five sub-types with binary criteria should improve this.

### 8.2 Recommended MQM Clarity Evaluation Prompt Structure

For the LLM judge, evaluate clarity in a separate pass from accuracy/completeness:

1. Read the description for comprehension (no chart reference needed)
2. For each sub-type, apply the binary criteria above
3. For each flagged error, cite the specific text span
4. Assign severity (Minor or Major) based on the operationalization table
5. Explicitly check: "Is this description longer than necessary? Could the same information be conveyed in fewer sentences?"


## References

- Hsu, T.-Y., Huang, C.-Y., Rossi, R., Kim, S., Giles, C.L., & Huang, T.-H.K. (2023). GPT-4 as an Effective Zero-Shot Evaluator for Scientific Figure Captions. *Findings of EMNLP 2023*. https://aclanthology.org/2023.findings-emnlp.363/

- Hsu, T.-Y., Huang, C.-Y., & Huang, T.-H.K. (2024). SciCapenter: Supporting Caption Composition for Scientific Figures with Machine-Generated Captions and Ratings. *CHI Extended Abstracts 2024*. https://dl.acm.org/doi/10.1145/3613905.3650738

- Hsu, T.-Y., Lee, S., Hsu, M.-Y., & Huang, T.-H.K. (2021). SciCap: Generating Captions for Scientific Figures. *Findings of EMNLP 2021*. https://aclanthology.org/2021.findings-emnlp.277/

- Hsu, T.-Y., & Huang, T.-H.K. (2025). Five Years of SciCap: What We Learned and Future Directions for Scientific Figure Captioning. *arXiv preprint 2512.21789*.

- Huang, K.-H., et al. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. *Findings of ACL 2024*. https://aclanthology.org/2024.findings-acl.41/

- Kantharaj, S., et al. (2022). Chart-to-Text: A Large-Scale Benchmark for Chart Summarization. *ACL 2022*. https://aclanthology.org/2022.acl-long.277/

- Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics. *Tradumàtica*, 12, 455-463. https://themqm.org/

- Lundgard, A., & Satyanarayan, A. (2022). Accessible Visualization via Natural Language Descriptions: A Four-Level Model of Semantic Content. *IEEE Transactions on Visualization and Computer Graphics*, 28(1), 1073-1083. https://arxiv.org/abs/2110.04406

- Obeid, J., & Hoque, E. (2020). Chart-to-Text: Generating Natural Language Descriptions for Charts by Adapting the Transformer Model. *Proceedings of INLG 2020*.

- Rahman, M.M., et al. (2023). ChartSumm: A Comprehensive Benchmark for Automatic Chart Summarization of Long and Short Summaries. *arXiv preprint 2304.13620*. https://arxiv.org/abs/2304.13620

- Reiter, E. (2019). Accuracy, Fluency, and Utility. *Ehud Reiter's Blog*. https://ehudreiter.com/2019/10/08/accuracy-fluency-and-utility/

- Saito, K., Wachi, A., Wataoka, K., & Akimoto, Y. (2023). Verbosity Bias in Preference Labeling by Large Language Models. *arXiv preprint 2310.10076*. https://arxiv.org/abs/2310.10076

- Tang, B.J., et al. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. *ACL 2023*. https://aclanthology.org/2023.acl-long.401/

- Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2023*.

- Zhong, M., et al. (2022). Towards a Unified Multi-Dimensional Evaluator for Text Generation. *EMNLP 2022*. https://aclanthology.org/2022.emnlp-main.131/
