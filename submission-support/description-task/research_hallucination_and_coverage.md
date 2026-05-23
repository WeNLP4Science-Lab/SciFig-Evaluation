# Hallucination Detection and Extra-Checklist Coverage in MQM-Based Chart Description Evaluation

Research notes for the SciFig-Evaluation description task. Compiled May 2026.

---

## Part 1: Hallucination Detection

### 1.1 How Existing Frameworks Define and Detect Hallucination

**CHOCOLATE** (Huang et al., 2024) is the most directly relevant framework. The paper "Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning" (ACL Findings 2024) introduces a comprehensive typology of factual errors in chart captions. Key findings: even GPT-4V produces captions with an 81.27% non-factual rate. The framework introduces CHARTVE, a visual entailment model that evaluates caption factuality by checking whether claims in a caption are entailed by the chart image. CHOCOLATE also proposes C2TFEC, a two-stage correction pipeline. Error types include value errors, label errors, trend errors, and out-of-scope claims.

**ChartHal** (Cui et al., 2025) provides a fine-grained hallucination taxonomy specifically for chart understanding. It classifies chart-question relations into four categories:
- **Irrelevant**: question is unrelated to chart content
- **Inexist**: question asks about information absent from the chart
- **Contradictory**: question is based on false premises inconsistent with chart data
- **Normal**: valid question aligned with chart content

ChartHal benchmarks 15 LVLMs on 1,062 human-validated samples. Even GPT-5 and o4-mini achieve only 34.46% and 22.79% accuracy. Questions involving inexistent or contradictory information are especially likely to trigger hallucinations.

**CHAIR** (Rohrbach et al., 2018) is the foundational metric for object hallucination in image captioning. It extracts objects from candidate captions via string matching against MS COCO classes and synonyms, then checks whether those objects appear in ground-truth annotations. CHAIR measures hallucination at both the instance level (CHAIRi: fraction of hallucinated objects) and sentence level (CHAIRs: fraction of sentences containing a hallucination). Limitation: restricted to a closed vocabulary of MS COCO object classes.

**ALOHa** (Petryk et al., 2024) modernises CHAIR with open-vocabulary hallucination detection. It uses an LLM to extract groundable objects from captions, measures semantic similarity to reference objects, and uses Hungarian matching for a final hallucination score. ALOHa identifies 13.6% more hallucinated objects than CHAIR on the HAT benchmark and 30.8% more on nocaps (where objects extend beyond MS COCO categories).

**FActScore** (Min et al., 2023) decomposes long-form text into atomic facts and computes the fraction supported by a knowledge source. Each atomic fact receives a binary label (supported / not supported). ChatGPT achieves only 58% FActScore on biographies. The automated estimator using retrieval + a strong LLM has less than 2% error rate vs human judgments. FActScore's key insight: binary quality judgments on whole passages are inadequate because generations contain mixtures of supported and unsupported claims.

**HaluEval** (Li et al., 2023) is a large-scale hallucination benchmark using ChatGPT-generated hallucinated samples via a sampling-then-filtering framework. GPT-4.1 achieves 75.2% accuracy on HaluEval for identifying hallucinated responses. The benchmark demonstrates that providing external knowledge or adding reasoning steps improves hallucination recognition.

**ChartCap** (Lim et al., 2025, ICCV) tackles hallucination in dense chart captioning by constructing a 565K-sample dataset of chart images paired with type-specific captions that exclude extraneous information. It introduces the Visual Consistency Score, which evaluates caption quality by measuring similarity between a chart regenerated from the caption and the original chart.

### 1.2 Taxonomy of Hallucination Types in Chart Descriptions

Drawing from CHOCOLATE, ChartHal, and the broader hallucination taxonomy literature (Huang et al., 2025; Rawte et al., 2023):

| Type | Definition | Example | Severity |
|------|-----------|---------|----------|
| **Entity fabrication** | Introducing a data series, category, or visual element that does not exist in the chart | "The green line representing Method C..." when no such line exists | Critical |
| **Value fabrication** | Stating a specific numerical value that is not present or significantly wrong | "Sales reached 450 million" when the actual value is 280 million | Major |
| **Label fabrication** | Inventing or misattributing axis labels, legend entries, or titles | "The x-axis shows temperature" when it shows time | Major |
| **Trend fabrication** | Describing a trend that contradicts the visual data | "Revenue declined steadily" when it clearly increases | Major |
| **Relationship fabrication** | Inventing correlations, comparisons, or causal links not present | "Method A consistently outperforms Method B" when they alternate | Major |
| **Colour/style fabrication** | Misattributing visual encodings | "The red dashed line" when it is blue and solid | Minor |
| **Structural fabrication** | Misrepresenting chart structure | "The stacked bar chart" when it is grouped | Major |
| **Out-of-scope fabrication** | Introducing information that cannot be inferred from the chart at all | "This data was collected in 2019" when no date is shown | Minor-Major |

### 1.3 Should Different Hallucination Types Have Different Severities?

**Yes.** The evidence strongly supports graduated severity:

1. **CHOCOLATE** distinguishes error types by their impact on downstream understanding. Value errors and entity errors are treated as more severe than style errors because they change the factual content a reader would extract.

2. **ChartHal** shows that inexistent and contradictory hallucinations are far more damaging than irrelevant ones, because they actively inject false information vs merely adding noise.

3. **MQM in translation** (Lommel et al., 2014) uses a well-established graduated severity system: critical errors (meaning reversal, safety-critical mistranslation) receive higher penalties than minor errors (style issues, acceptable alternatives). The "non-translation" category penalises incoherent output equivalent to a cluster of severe errors.

4. **ALOHa** implicitly supports this by measuring hallucination at the object level rather than treating all hallucinations equally.

**Recommended graduated weights for our framework:**

| Hallucination subtype | Proposed category | Proposed weight |
|----------------------|-------------------|-----------------|
| Entity / series fabrication | Accuracy / Critical | 7.0 |
| Value fabrication (>20% error) | Accuracy / Major | 5.0 |
| Trend / relationship fabrication | Accuracy / Major | 5.0 |
| Label / structural fabrication | Accuracy / Major | 5.0 |
| Value approximation error (10-20%) | Accuracy / Minor | 2.0 |
| Colour / style misattribution | Accuracy / Minor | 2.0 |
| Out-of-scope speculation | Completeness / Minor | 1.5 |

### 1.4 Hallucination vs Reasonable Inference

This is one of the hardest boundary problems. ChartHal's taxonomy is instructive:

**Clear hallucination:**
- Fabricating entities, values, or data not visually present
- Stating specific numbers not readable from the chart
- Describing visual elements (lines, bars, annotations) that do not exist

**Borderline / reasonable inference:**
- "The trend suggests improvement" -- this is an interpretation of a visible upward slope. If the slope is objectively upward, this is a valid perceptual description, not hallucination.
- "Sales appear to plateau around 2020" -- reading approximate inflection points from visual data is standard chart interpretation.
- "Method A may be more robust given its lower variance" -- this crosses into analytical inference. Our `global_interpretation` constraint already covers this.

**Recommended decision procedure:**
1. Is the claim about something visually present in the chart? If yes, it can only be wrong (accuracy error), not hallucinated.
2. Does the claim introduce an entity, value, or relationship with no visual basis? If yes, it is hallucination.
3. Does the claim make a subjective judgment or causal inference beyond what is shown? If yes, it is an interpretation violation (our existing `global_interpretation` constraint), not hallucination.

This three-way distinction (accuracy error vs hallucination vs interpretation) prevents conflation. CHOCOLATE makes a similar distinction: factual errors about visible content are accuracy problems; claims about non-existent content are fabrication; and evaluative language is a separate category.

### 1.5 Counting and Stacking Hallucination Penalties

**FActScore's approach:** Each atomic fact is independently scored. A description with 5 fabricated claims gets 5 penalties. This is the cleanest approach and avoids the problem of a single "hallucination: yes/no" flag that treats 1 fabrication the same as 10.

**CHAIR's approach:** Reports both instance-level (per-object) and sentence-level (per-sentence) rates. Both are useful but instance-level is more granular.

**Our current implementation** (from `checklists.py`) already supports multiple violations per global constraint -- each violation in the `violations` list generates a separate penalty. This is correct.

**Recommendation:** Maintain the current per-violation penalty approach. Each fabricated claim should be a separate penalty entry with its own weight based on the subtype taxonomy above. A description that fabricates 3 data series should receive 3 x 5.0 = 15.0 penalty, not a single 3.5 penalty.

**Practical concern:** The judge prompt should explicitly instruct the LLM to enumerate each fabricated claim separately rather than grouping them. The current prompt in `evaluate_mqm.py` says "List each violation separately with the quoted text and explanation" -- this is correct.

### 1.6 False Positive Rates for LLM Judges Detecting Hallucination

Evidence on LLM judge reliability:

1. **GPT-4 hallucination rate as evaluator:** Approximately 28.6% hallucination rate when generating reference evaluations, and a conservative general estimate of ~15% for LLM evaluator hallucination rates (Factored AI, 2025).

2. **GPT-4.1 on HaluEval:** 75.2% accuracy in identifying hallucinated responses, meaning a ~25% error rate combining false positives and false negatives.

3. **FActScore automated model:** Less than 2% error rate vs human annotation when using retrieval + strong LLM (Min et al., 2023). This is the best-case scenario with retrieval augmentation.

4. **GPT-4 as zero-shot evaluator for scientific figure captions** (Hsu et al., 2023): Achieves Kendall correlation of 0.401 with PhD-level human rankings -- moderate agreement, indicating substantial room for disagreement on individual items.

5. **MC1 benchmark analysis:** More than 25% of test samples scored as incorrect by MC1 could have been factually correct, highlighting evaluation benchmark limitations themselves.

**Key risk for our pipeline:** The main false-positive pattern is the judge flagging a reasonable approximation or valid alternative interpretation as hallucination. Our existing tolerance rules (colour families, numerical tolerances, wording equivalence) mitigate this partially, but the hallucination check itself has no built-in tolerance. 

**Mitigation strategies:**
- Require the judge to quote the specific text span and explain why it is fabricated (already implemented)
- Use the image as grounding (already implemented -- image is in the prompt)
- Consider a two-pass approach: first pass identifies potential hallucinations, second pass verifies each against the image
- For high-stakes evaluations, use majority voting across multiple judge calls

---

## Part 2: Extra-Checklist Correct Content

### 2.1 How Existing Frameworks Handle Correct Content Not in the Rubric

**FActScore** (Min et al., 2023): Evaluates precision only -- what fraction of stated claims are correct. It does not penalise for omission. Extra correct content always helps the score (more supported atoms = same or higher percentage). But FActScore deliberately does not measure recall; a one-sentence correct description scores 100% FActScore even if it omits 90% of relevant information.

**CHOCOLATE** (Huang et al., 2024): Focused on factual error detection and correction, not on rewarding extra correct content. The framework classifies claims as factual or non-factual; correct claims beyond expectations are simply not penalised.

**MQM in translation** (Lommel et al., 2014): The original MQM framework is error-based and subtractive. There is no "bonus" for elegant translation or extra helpful content. The score starts at 100 and only goes down. This is by design: MQM measures how much is wrong, not how much is right. However, MQM's Completeness dimension penalises omission, which partially addresses the coverage problem from the penalty side.

**VisText** (Tang et al., 2023): Introduces semantic levels for chart captions:
- L1: Elemental/structural (chart type, axes, encoding)
- L2: Statistical (specific values, extrema, averages)
- L3: Perceptual/cognitive (trends, patterns, comparisons, anomalies)

VisText's level system implicitly defines what content is expected. L1 content is the minimum; L2 and L3 are progressively richer. 95% of human-written captions contain L2 or L3 content, with ~1.4x more L3 than L2 statements.

**ChartCap** (Lim et al., 2025): Explicitly distinguishes between "discernible data from the chart" (which should be captioned) and "extraneous information that cannot be inferred" (which should not). Their dataset excludes extraneous information, suggesting that correct content should be bounded by what is visually present.

### 2.2 Does Ignoring Extra Correct Content Bias Scores?

**Yes, it creates a systematic bias against verbose, thorough models and in favour of conservative, minimal models.** Here is the evidence:

1. **Precision-recall trade-off in chart captioning** (identified in ChartCap and VisText research): Longer captions show lower precision scores but higher recall scores. They capture more visual content but also introduce more opportunities for errors. An error-only metric (like our MQM) penalises the longer caption for its errors without crediting its additional correct content.

2. **Concrete example from our pipeline:** Consider two bar chart descriptions:
   - Model A: Correctly describes all 14 checklist items. Score: 100.
   - Model B: Correctly describes all 14 checklist items AND accurately notes error bar patterns, sub-panel layout, specific annotation text, and data label values. Score: 100 (same), but with higher risk of hallucination penalties if any extra claim is slightly wrong.

   Model B is objectively more useful but cannot score higher and may score lower. This penalises thoroughness.

3. **FActScore's insight:** Binary or coarse evaluation "is inadequate because generations contain mixtures of supported and unsupported claims." The same logic applies to our checklist: a fixed checklist creates a ceiling that makes all thorough models look identical to minimal models.

### 2.3 Should We Penalise for NOT Describing Extra Content?

**No, not within the current generic-checklist design.** Rationale:

1. The checklist is generic per chart type. We cannot penalise a model for not describing error bars if the checklist does not mention error bars and the judge does not know whether error bars are present.

2. Our checklist already includes "Annotations noted if present" items (bar_13, line_14) which partially cover this. These items have `severity: Minor`, so missing them costs only 1.5 points.

3. Penalising omission of content we did not ask about would make the evaluation subjective and judge-dependent. Different judges would identify different "extra" content as missing.

**However:** If we move to figure-specific evaluation (see 2.4-2.5), then penalising omission of figure-specific details becomes feasible and desirable.

### 2.4 Figure-Specific Atoms vs Generic Checklists: The Trade-off

**The thesis approach (figure-specific atoms extracted from human annotations):**
- Pros: Captures every detail specific to the figure; enables recall measurement; treats each figure as unique
- Cons: Requires human annotation per figure; does not scale; annotations themselves may be incomplete or biased

**Our generic checklist approach:**
- Pros: Scales to any figure of a given type; consistent across evaluations; reproducible; no per-figure annotation cost
- Cons: Misses figure-specific details; cannot reward extra correct content; creates a score ceiling; all bar charts evaluated identically regardless of their visual complexity

**How other benchmarks handle it:**

| Benchmark | Approach | Granularity |
|-----------|----------|-------------|
| FActScore (Min et al., 2023) | Atomic decomposition of generated text | Per-claim, but precision-only |
| CHOCOLATE (Huang et al., 2024) | Error annotation on generated captions | Per-error in generated text |
| VisText (Tang et al., 2023) | Semantic level classification (L1/L2/L3) | Per-statement level |
| ChartCap (Lim et al., 2025) | Visual Consistency Score (regeneration) | Holistic, reference-free |
| CHAIR (Rohrbach et al., 2018) | Object-level matching vs ground truth | Per-object |
| ChartHal (Cui et al., 2025) | Question-answer hallucination probes | Per-question |
| SciCap-Eval (Hsu et al., 2023) | Holistic 1-6 score by GPT-4 | Single score |

### 2.5 Hybrid Approaches: Generic Checklist + Dynamic Claim Extraction

This is the most promising direction. Several strategies exist:

**Strategy A: Post-hoc claim decomposition (FActScore-style)**

1. Use the generic checklist for the base MQM score (current approach).
2. After scoring, decompose the model's description into atomic claims using an LLM.
3. Classify each claim as: (a) covered by a checklist item, (b) correct but extra, (c) hallucinated.
4. Report an auxiliary "coverage richness" metric alongside the MQM score.

Advantage: Does not change the MQM score, so comparability is maintained. Adds a complementary precision-recall view.

**Strategy B: Dynamic checklist extension**

1. Start with the generic checklist.
2. Before evaluation, use an LLM to examine the figure and extract figure-specific items (e.g., "error bars present on all bars", "annotation arrow pointing to peak at x=5", "sub-panel (b) shows zoomed region").
3. Add these as bonus items to the checklist with Minor severity.
4. Evaluate the model on the extended checklist.

Advantage: Rewards thoroughness. Risk: The extraction step may itself hallucinate items, creating false expectations.

**Strategy C: Dual-metric reporting**

1. MQM score from the generic checklist (error-based, subtractive).
2. FActScore-style precision from atomic decomposition (claim-based, proportion).
3. Report both. MQM measures "how much is wrong"; FActScore measures "how much of what you said is right."

This is analogous to how BLEU (precision) and METEOR (recall-weighted) coexist in machine translation evaluation.

**Strategy D: Visual Consistency Score (ChartCap-style)**

1. Use the model's description to regenerate a chart.
2. Measure similarity between the regenerated chart and the original.
3. This implicitly rewards extra correct content (more detail = more faithful reconstruction) and penalises hallucination (fabricated elements = divergent reconstruction).

Advantage: Fully reference-free. Disadvantage: Requires a chart-generation model and similarity metric; currently impractical for diverse scientific charts.

**Recommended approach for our paper:** Strategy C (dual-metric reporting). Keep MQM as the primary error-based metric. Add a secondary "claim precision" metric that decomposes descriptions into atomic claims and verifies each against the image. Report both in the paper. This is lightweight to implement (one additional LLM call per description), maintains backward compatibility with existing MQM scores, and directly addresses the reviewer concern that thorough descriptions are under-rewarded.

---

## Summary of Actionable Recommendations

### For hallucination detection:
1. **Subdivide hallucination types** with graduated severity weights (Section 1.3 table).
2. **Maintain per-violation penalties** -- each fabricated claim is a separate penalty (already implemented).
3. **Add a decision procedure** to the judge prompt distinguishing hallucination vs accuracy error vs interpretation (Section 1.4).
4. **Acknowledge the ~15-25% judge error rate** in the paper's limitations section.

### For extra-checklist coverage:
1. **Add a secondary claim-precision metric** (Strategy C) alongside MQM scores.
2. **Do not modify the MQM score** itself -- keep it as a pure error-based metric for comparability.
3. **Report the precision-recall gap** as a known limitation of generic checklists.
4. **Consider Strategy B (dynamic checklist extension)** for future work if per-figure annotation is available.

---

## References

- Cui, Y., et al. (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. arXiv:2509.17481.
- Huang, K.-H., et al. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. Findings of ACL 2024. (CHOCOLATE dataset)
- Hsu, T.-Y., Huang, C.-Y., Rossi, R., Kim, S., Giles, C. L., & Huang, T.-H. (2023). GPT-4 as an Effective Zero-Shot Evaluator for Scientific Figure Captions. Findings of EMNLP 2023.
- Li, J., et al. (2023). HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models. EMNLP 2023.
- Lim, J., Ahn, J., & Kim, G. (2025). ChartCap: Mitigating Hallucination of Dense Chart Captioning. ICCV 2025 (Highlight).
- Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics.
- Min, S., et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. EMNLP 2023.
- Petryk, S., et al. (2024). ALOHa: A New Measure for Hallucination in Captioning Models. NAACL 2024.
- Rawte, V., Sheth, A., & Das, A. (2023). A Survey of Hallucination in Natural Language Generation. ACM Computing Surveys.
- Rohrbach, A., Hendricks, L. A., Burns, K., Darrell, T., & Saenko, K. (2018). Object Hallucination in Image Captioning. EMNLP 2018.
- Tang, B., Boggust, A., & Satyanarayan, A. (2023). VisText: A Benchmark for Semantically Rich Chart Captioning. ACL 2023.
- Huang, Y., et al. (2025). A Comprehensive Taxonomy of Hallucinations in Large Language Models. arXiv:2508.01781.
