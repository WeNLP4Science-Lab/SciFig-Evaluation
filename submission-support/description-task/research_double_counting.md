# Handling Double-Counting and Cascading Errors in LLM-as-Judge Evaluation Pipelines

## 1. Problem Statement

In multi-criteria LLM-as-judge evaluation, a single root-cause error in the evaluated text can trigger penalties across multiple scoring dimensions. We observe two distinct manifestations in our scientific chart description evaluation pipeline:

**Cascading errors.** A hallucinated data series in a line plot is penalised under colour accuracy, value accuracy, trend accuracy, legend accuracy, and the global hallucination constraint. One root cause produces 5+ penalties.

**Checklist-global overlap.** An accuracy error on a checklist item (e.g., wrong chart purpose) is also flagged as a global hallucination or interpretation violation. The same text span receives two independent penalties from two evaluation layers.

Prompt-level mitigations ("do not flag as global violation anything already penalised under a checklist item") are unreliable. This is consistent with findings that LLMs degrade on complex multi-constraint instructions (Saha et al., 2023; Masood, 2026), and that criterion bleed is a well-documented failure mode when rubrics contain too many overlapping criteria.

---

## 2. How Existing Evaluation Frameworks Handle Correlated Errors

### 2.1 MQM (Multidimensional Quality Metrics) for Translation

MQM is the dominant error-annotation protocol for machine translation evaluation since WMT 2021 (Freitag et al., 2021). Its scoring model sums severity-weighted error counts (Minor=1, Major=5, Critical=25) across a hierarchical error taxonomy (e.g., Accuracy/Mistranslation, Fluency/Grammar).

**MQM's stance on cascading errors:** The MQM framework acknowledges the issue implicitly through its error compilation stage, which applies "root cause filtering and duplicate error conflation to create an error summary" (Lommel et al., 2014). However, the standard scoring model does not prescribe a specific deduplication algorithm. In practice, MQM annotators are trained to mark each error span once under its most specific category. When a single mistranslation causes both an accuracy error and a fluency error, MQM guidelines allow annotators to mark both, and the penalties accumulate. The framework's primary mitigation is the hierarchical taxonomy itself -- annotators are instructed to select the most specific applicable category, which reduces but does not eliminate double-counting.

**Error Span Annotation (ESA):** Kocmi et al. (2024) proposed ESA as a lighter-weight alternative that combines continuous quality ratings with high-level error span marking. ESA defines span overlap simply: "any span that overlaps with another one is considered a hit, even if only with a single character." This binary overlap detection is used for inter-annotator agreement but does not address the double-counting problem directly.

**MQM-APE:** Lu et al. (2024) introduced MQM-APE, a post-processing framework that filters out non-impactful errors from GEMBA-MQM annotations. The key idea is to use automatic post-editing as a verification step: for each flagged error, the LLM post-edits the translation to fix only that error, then a pairwise quality verifier checks whether the fix actually improved quality. Errors that do not improve quality when fixed are discarded. This approach implicitly handles cascading errors because fixing the root cause would improve quality, but fixing downstream symptoms individually would not. This is the closest existing approach to principled deduplication in MQM-based evaluation.

### 2.2 FActScore

FActScore (Min et al., 2023) decomposes generated text into atomic facts -- minimal, independent factual claims -- and verifies each against a knowledge source. The framework addresses double-counting by design: the decomposition templates are engineered to produce facts that are "independent and minimal." If successful, each atomic fact captures exactly one verifiable claim, so no single error in the source text can fail multiple atomic facts.

**Limitation for our setting:** FActScore's independence assumption works for biographical text but is harder to enforce for chart descriptions, where facts are inherently correlated. A hallucinated data series simultaneously produces wrong values, wrong colours, wrong trends, and wrong legends -- these are genuinely different facts about the same hallucinated entity, making clean atomic decomposition difficult.

### 2.3 CHAIR (Caption Hallucination Assessment with Image Relevance)

CHAIR (Rohrbach et al., 2018) measures object hallucination in image captioning via two metrics: CHAIRi (per-instance, fraction of hallucinated object instances) and CHAIRs (per-sentence, fraction of sentences containing a hallucination). CHAIR avoids double-counting by design: it counts unique hallucinated object types against a ground-truth object set. If a caption mentions "cat" three times and no cat is present, CHAIRi counts it once (one hallucinated object type), not three times.

**Relevance:** CHAIR's type-level deduplication is a useful model. For chart descriptions, the analogue would be counting hallucinated chart elements (e.g., one phantom data series) rather than counting every downstream claim about that element.

### 2.4 ChartHal

ChartHal (Cui et al., 2025) evaluates hallucination in chart understanding via a taxonomy of 12 hallucination-triggering scenarios. The framework focuses on question-level binary accuracy (correct/hallucinated) rather than continuous scoring, which sidesteps cascading penalties. Each question tests exactly one scenario, so there is no mechanism for a single error to cascade across questions.

**Relevance:** ChartHal's scenario isolation suggests that evaluation instruments should test each potential error source independently rather than allowing cross-contamination between evaluation dimensions.

---

## 3. Deduplication Strategies in the Literature

### 3.1 Text Span Overlap Detection

The simplest deduplication approach identifies errors that reference the same text span. Two errors are considered duplicates if their annotated spans overlap beyond a threshold.

**Exact match:** Two errors are duplicates if and only if they reference identical character offsets. High precision but low recall -- a span of "the red line shows 45%" and "red line" would not match despite referring to the same error.

**Overlap-based:** Following ESA (Kocmi et al., 2024), any character-level overlap counts as a match. Higher recall but may over-merge errors that happen to reference adjacent text.

**Jaccard similarity on spans:** Compute token-level Jaccard similarity between error spans; merge if above a threshold (e.g., 0.5). Balances precision and recall.

### 3.2 Root Cause Analysis and Error Dependency Graphs

Borrowing from fault diagnosis in distributed systems (Meng et al., 2020), errors can be modelled as nodes in a directed graph where edges represent causal dependencies. A root-cause error (e.g., hallucinated data series) is a source node; downstream errors (wrong colour, wrong values) are descendant nodes. Deduplication removes all descendant nodes and retains only root causes.

**Construction approaches:**
- **Temporal ordering:** If the hallucinated element is mentioned first in the text, subsequent errors referencing the same entity are likely downstream.
- **Causal prompting:** Ask the LLM judge to explicitly identify which errors are root causes vs. symptoms (though this adds another LLM inference step).
- **Entity co-reference:** Errors referencing the same chart element (same data series, same axis) are grouped, and only the highest-severity error is retained.

### 3.3 Penalty Capping per Root Cause

Rather than fully deduplicating, cap the total penalty attributable to any single root cause. For example, if three checklist items fail because of one hallucinated series, and each carries a 5-point penalty, cap the combined penalty at 5 (or some multiple like 1.5x the single-item penalty).

**Advantage:** Preserves the information that an error affected multiple dimensions while preventing runaway penalty accumulation.

**Disadvantage:** Requires defining what constitutes a "root cause group," which may require manual annotation or heuristic rules.

### 3.4 Maximum Penalty per Text Span

A simpler variant: for any text span that is referenced by multiple errors, apply only the highest-severity penalty. This is analogous to the "most specific category" principle in MQM annotation.

### 3.5 Semantic Similarity of Error Explanations

When the judge provides explanations for each error, compute pairwise semantic similarity between explanations using embeddings (e.g., sentence-transformers). Errors with similarity above a threshold are grouped, and only the most severe penalty in each group is applied.

**Relevance:** This works well when the judge's explanations explicitly reference the same underlying phenomenon ("the red line is not present in the chart" vs. "the colour red does not correspond to any data series").

---

## 4. How LLM-as-Judge Systems Handle Double-Counting

### 4.1 Branch-Solve-Merge (BSM)

Saha et al. (2023) decompose evaluation into parallel sub-tasks, each evaluating a single criterion. Sub-task scores are solved independently and then merged. BSM reduces position and length bias by up to 50% and improves human-LLM agreement by up to 26%.

**Double-counting implications:** BSM explicitly isolates criteria into independent evaluation branches, which prevents the judge from being influenced by cross-criterion contamination during scoring. However, the merge step (typically averaging or weighted sum) does not deduplicate -- if two branches independently penalise the same root cause, the penalties accumulate in the merged score.

**Mitigation opportunity:** A deduplication layer between the solve and merge steps could compare error explanations across branches and suppress duplicate penalties before aggregation.

### 4.2 DnA-Eval (Decomposition and Aggregation)

DnA-Eval (Liu et al., 2024) decomposes evaluation into aspect-level pairwise comparisons, inspired by pedagogical rubric design. The framework proposes criteria, rates each aspect independently, and aggregates.

**Double-counting implications:** Like BSM, DnA-Eval isolates aspect evaluation but does not explicitly deduplicate across aspects during aggregation. The framework's contribution is improving criterion specificity (reducing overlap by better criterion definitions), which indirectly mitigates double-counting.

### 4.3 CARE (Confounder-Aware Aggregation)

CARE (Chen et al., 2026) addresses correlated errors in LLM-as-judge ensembles by modelling judge scores as arising from both a latent true-quality signal and shared confounding factors. The framework separates quality from confounders, reducing aggregation error by up to 26.8%.

**Relevance to double-counting:** While CARE targets inter-judge correlation rather than intra-judge cascading errors, its mathematical framework (latent factor models separating signal from confounders) could be adapted. In our setting, the "confounder" is the root-cause error, and the "correlated scores" are the checklist items affected by that root cause.

### 4.4 GEMBA-MQM and MQM-APE

Kocmi et al. (2023) introduced GEMBA-MQM, using GPT-4 to produce structured MQM error annotations. Lu et al. (2024) extended this with MQM-APE, which filters non-impactful errors via automatic post-editing. As discussed in Section 2.1, MQM-APE's verify-by-fixing approach is the most principled existing method for identifying truly independent errors, because it tests whether each error's removal independently improves quality.

### 4.5 Rubric Engineering Best Practices

Masood (2026) synthesises best practices for LLM-as-judge rubrics, emphasising four properties: specific, measurable, criterion-independent, and exhaustive. The key recommendation for avoiding double-counting is to "run a correlation pass; if two criteria scores always move together, merge them into a single criterion." This is a design-time mitigation rather than a post-processing approach.

---

## 5. Recommended Algorithmic Approaches for Deduplication

Given our pipeline structure (structured JSON output with checklist items, global constraints, error explanations, and text references), we recommend a multi-stage deduplication pipeline:

### Stage 1: Text Span Grouping

```
For each pair of errors (e_i, e_j):
    span_overlap = jaccard(e_i.text_span_tokens, e_j.text_span_tokens)
    if span_overlap > 0.3:
        group(e_i, e_j)
```

This catches the obvious case where multiple errors reference the same quoted text.

### Stage 2: Entity Co-reference Grouping

```
For each error e:
    extract chart_element(e)  # e.g., "red line", "Series B", "y-axis"
For each pair of errors referencing the same chart_element:
    group(e_i, e_j)
```

This catches cases where different text spans refer to the same chart element using different language.

### Stage 3: Semantic Similarity of Explanations

```
For each pair of ungrouped errors (e_i, e_j):
    sim = cosine_similarity(embed(e_i.explanation), embed(e_j.explanation))
    if sim > 0.75:
        group(e_i, e_j)
```

This catches semantically equivalent errors with different surface forms.

### Stage 4: Cross-Layer Deduplication (Checklist vs. Global)

```
For each global constraint violation g:
    For each checklist error c in the same group as g:
        suppress g  # keep checklist penalty, remove global penalty
```

Rationale: checklist items are more specific and interpretable than global constraints. When the same error is captured by both layers, retaining the checklist penalty preserves granularity.

### Stage 5: Within-Group Penalty Resolution

For each group of related errors, apply one of:
- **Keep-max:** Retain only the highest-severity penalty. Most aggressive deduplication.
- **Capped-sum:** Sum penalties within the group but cap at 1.5x the maximum single penalty. Preserves some signal about breadth of impact.
- **Root-cause-only:** If one error in the group can be identified as the root cause (e.g., "hallucinated data series"), keep only that error's penalty. Requires root-cause identification.

### Recommended Default: Capped-Sum

For reporting, we recommend the **capped-sum** strategy as the primary deduplicated metric, with raw (uncapped) MQM as a secondary metric for transparency:

- It acknowledges that cascading errors do have compound impact (a hallucinated series that corrupts five aspects is worse than one that corrupts two).
- It prevents runaway penalty accumulation from a single root cause.
- The cap factor (1.5x) is a hyperparameter that can be tuned against human judgment correlation.

---

## 6. Impact of Double-Counting on Score Validity

### 6.1 Effect on Model Rankings

Double-counting inflates scores non-uniformly. Models that produce structured hallucinations (e.g., fabricating entire data series) are penalised far more heavily than models that produce scattered minor inaccuracies, even when the total information loss is comparable. This can distort model rankings, particularly:

- Penalising models that hallucinate confidently (one big fabrication) more than models that make many small errors.
- Favouring models that produce vague, non-committal descriptions (fewer specific claims to penalise).

### 6.2 Effect on Correlation with Human Judgments

Double-counting typically reduces correlation with human judgments because human evaluators naturally apply root-cause reasoning. A human annotator seeing a hallucinated data series would note "hallucinated series" as one major error, not five separate penalties. MQM studies show low inter-annotator agreement partly due to inconsistent treatment of correlated errors (Freitag et al., 2021).

### 6.3 Systematic Bias by Error Type

Double-counting disproportionately affects:
- **Hallucination errors:** A single hallucinated entity cascades across all attributes of that entity.
- **Structural errors:** Misidentifying the chart type affects every downstream description element.
- **Fewer-affected error types:** Formatting errors, language fluency errors, and omission errors are less susceptible because they tend to be localised to a single evaluation dimension.

This means double-counting creates a systematic bias toward over-penalising hallucination relative to omission, even when both represent equivalent information loss.

### 6.4 Empirical Recommendation

Report both raw and deduplicated scores. If model rankings change between raw and deduplicated scoring, this itself is an informative finding -- it reveals which models are disproportionately affected by cascading penalties and which error types drive the divergence.

---

## 7. Should We Cap or Deduplicate Entirely?

| Strategy | Pros | Cons |
|----------|------|------|
| **Full deduplication** (keep one error per root cause) | Cleanest interpretation; mirrors human judgment | Loses information about error breadth; a hallucination affecting 5 dimensions is treated identically to one affecting 1 |
| **Penalty capping** (cap total penalty per root cause group) | Preserves severity gradient; tuneable cap factor | Requires grouping accuracy; cap factor is arbitrary |
| **Weighted deduplication** (first error full penalty, subsequent errors in group at reduced weight, e.g., 0.25x) | Smooth penalty curve; preserves all error information | More complex; weight factor is a hyperparameter |

**Our recommendation for the SciFig evaluation pipeline:**

1. **Primary reported metric:** Capped-sum deduplicated MQM, with cap = 1.5x the maximum single-item penalty per root-cause group.
2. **Secondary metric:** Raw MQM (no deduplication) for full transparency.
3. **Analysis metric:** Fully deduplicated MQM (one penalty per root cause) for understanding the number of distinct error sources.

Report all three. If rankings are stable across all three, the double-counting problem does not affect conclusions. If rankings diverge, analyse which models and error types are affected and discuss in the paper.

---

## 8. Practical Implementation for Our Pipeline

Given our current setup (GPT-4o judge producing structured JSON with checklist scores, global constraint scores, and explanations):

### 8.1 Minimal Viable Deduplication

```python
def deduplicate_errors(checklist_errors, global_errors):
    """
    Stage 1: Remove global violations that overlap with checklist errors.
    Uses text_span Jaccard overlap.
    """
    deduplicated_globals = []
    for g in global_errors:
        is_duplicate = False
        for c in checklist_errors:
            if jaccard_token_overlap(g.text_span, c.text_span) > 0.3:
                is_duplicate = True
                break
            if cosine_sim(embed(g.explanation), embed(c.explanation)) > 0.75:
                is_duplicate = True
                break
        if not is_duplicate:
            deduplicated_globals.append(g)
    
    return checklist_errors, deduplicated_globals
```

### 8.2 Within-Checklist Cascading Penalty Cap

```python
def cap_cascading_penalties(checklist_errors, cap_factor=1.5):
    """
    Group checklist errors by referenced chart element.
    Cap total penalty per group.
    """
    groups = group_by_chart_element(checklist_errors)
    capped_total = 0
    for group in groups:
        raw_sum = sum(e.penalty for e in group)
        max_single = max(e.penalty for e in group)
        capped_total += min(raw_sum, max_single * cap_factor)
    return capped_total
```

### 8.3 Requiring Judge Output Changes

To enable post-processing deduplication, require the judge to output:
- `text_span`: the exact quoted text that contains the error
- `chart_element`: the chart element referenced (e.g., "Series B", "y-axis label")
- `explanation`: free-text rationale for the penalty

These fields enable all three grouping strategies (span overlap, entity co-reference, semantic similarity).

---

## References

Chen, Y., et al. (2026). CARE: Confounder-Aware Aggregation for Reliable LLM Evaluation. arXiv:2603.00039.

Cui, Y., et al. (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. arXiv:2509.17481.

Freitag, M., et al. (2021). Experts, Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation. *Transactions of the Association for Computational Linguistics*, 9, 1460--1474.

Kocmi, T., & Federmann, C. (2023). GEMBA-MQM: Detecting Translation Quality Error Spans with GPT-4. In *Proceedings of WMT 2023*.

Kocmi, T., et al. (2024). Error Span Annotation: A Balanced Approach for Human Evaluation of Machine Translation. In *Proceedings of WMT 2024*, 1440--1453.

Liu, Y., et al. (2024). DnA-Eval: Enhancing Large Language Model Evaluation through Decomposition and Aggregation. arXiv:2405.15329.

Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics. *Revista Tradumatica*, 12, 455--463.

Lu, Z., et al. (2024). MQM-APE: Toward High-Quality Error Annotation Predictors with Automatic Post-Editing in LLM Translation Evaluators. In *Proceedings of COLING 2025*.

Masood, A. (2026). Rubric-Based Evaluations & LLM-as-a-Judge: Methodologies, Biases, and Empirical Validation in Domain-Specific Contexts. *Medium*.

Min, S., et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In *Proceedings of EMNLP 2023*.

Rohrbach, A., et al. (2018). Object Hallucination in Image Captioning. In *Proceedings of EMNLP 2018*.

Saha, S., et al. (2023). Branch-Solve-Merge Improves Large Language Model Evaluation and Generation. arXiv:2310.15123.
