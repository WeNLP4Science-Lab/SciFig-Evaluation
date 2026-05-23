# Evaluating Value-to-Label Mapping Correctness Without Double-Penalising

Research notes for the SciFig-Evaluation description task. Compiled May 2026.

---

## 1. The Problem: Transposition Errors in Chart Descriptions

Consider a pie chart where the ground truth is:

> Happiness (8.1%, blue), Excitement (14.1%, red)

A VLM produces:

> Happiness (14.1%, light purple), Excitement (8.1%, light blue)

Both values (8.1%, 14.1%) are present. Both labels (Happiness, Excitement) are present. But the values are **swapped** -- 14.1% is bound to "Happiness" instead of "Excitement," and vice versa. Additionally, the colours are wrong for both slices.

Under a checklist with separate items for completeness ("all labels mentioned"), value accuracy ("values are correct"), mapping ("values correctly assigned"), and colour ("colour-to-label mapping correct"), a single root cause -- transposition of two slices -- can trigger failures on 3-4 items per swapped element. This is the **double-penalisation** problem for transposition errors.

This document surveys how existing benchmarks, evaluation frameworks, and error taxonomies handle this class of error, and recommends a checklist structure that catches transposition without over-penalising.

---

## 2. How Chart QA Benchmarks Handle Value-Label Association

### 2.1 ChartQA: Bound Questions by Design

ChartQA (Masry et al., 2022) contains 9,600 human-written and 23,100 machine-generated questions over chart images. The question format is inherently **bound**: questions take forms like "What is the value for [category X]?" or "Which category has the highest value?" These question templates force the model to produce a value-label binding in its answer. A transposition error -- where the model has the right value in mind but assigns it to the wrong category -- would be caught because the question anchors the expected binding.

Critically, ChartQA does **not** ask existence-style questions like "Does the value 14.1% appear in this chart?" Such unbound questions would miss transposition entirely because the value does exist, just on the wrong slice.

**Implication for our setting:** ChartQA's question design implicitly treats value-label binding as the unit of evaluation. Each question tests one binding. This is equivalent to our "bound item" approach (Section 7).

### 2.2 PlotQA: Template-Based Bound Reasoning

PlotQA (Methani et al., 2020) generates 28.9 million question-answer pairs over 224,377 plots using crowd-sourced question templates. The templates produce bound queries: "What is the value of [variable] in [year/category]?" Answers are often real-valued and require reading specific data points from specific series -- inherently testing the binding between a data series identifier and its value at a given position.

PlotQA's template structure means that transposition errors (e.g., reporting Country A's GDP as Country B's) are caught because each question specifies which entity's value is requested. The evaluation is per-binding, not per-value-existence.

### 2.3 DVQA: Chart-Specific Vocabulary Binding

DVQA (Kafle et al., 2018) tests bar chart understanding with questions that "require processing words and answers that are unique to a particular bar chart." Questions bind values to specific bars via their labels. The model must identify which bar a question refers to and extract its value -- a bound evaluation by construction.

### 2.4 FigureQA: Relational but Bound

FigureQA (Kahou et al., 2018) tests 15 question templates across line plots, bar graphs, and pie charts. Questions probe relationships ("Is X greater than Y?", "Does X have the maximum value?") which are inherently bound -- the answer depends on correctly associating each label with its value and comparing them. A transposition error where X and Y values are swapped would produce the wrong relational answer.

### 2.5 CharXiv: Descriptive and Reasoning Questions

CharXiv (Wang et al., 2024) evaluates chart understanding with 2,323 charts from arXiv papers, using both descriptive questions ("examining basic chart elements") and reasoning questions ("synthesizing information across complex visual elements"). The descriptive questions test specific element-attribute bindings. GPT-4o achieves only 47.1% on CharXiv, compared to 80.5% for humans, and performance degrades by up to 34.5% under simple presentation variations -- suggesting that value-label bindings are fragile even for frontier models.

### 2.6 ChartBench: Unannotated Charts Force Binding

ChartBench (Xu et al., 2023) uses 66,600 charts across 42 categories with 600,000 QA pairs. Notably, many charts "lack data point annotations, which requires MLLMs to derive values similar to human understanding by leveraging inherent chart elements such as color, legends, and coordinate systems." This forces the model to perform explicit binding between visual elements (colours, positions) and semantic labels via the legend -- exactly the process where transposition errors occur.

### 2.7 Summary: All Major Benchmarks Test Bound Associations

| Benchmark | Question Style | Tests Binding? | Would Catch Transposition? |
|-----------|---------------|----------------|---------------------------|
| ChartQA | "What is X's value?" | Yes | Yes |
| PlotQA | "Value of X in Y?" | Yes | Yes |
| DVQA | Bar-specific queries | Yes | Yes |
| FigureQA | "Is X > Y?" | Yes | Yes |
| CharXiv | Element-specific | Yes | Yes |
| ChartBench | Value derivation | Yes | Yes |

No major chart QA benchmark uses unbound existence checks ("does value V appear?"). The field consensus is that the unit of evaluation is the **bound tuple** (label, value) or (label, value, colour), not the individual element.

---

## 3. FActScore and Entity-Attribute Binding

### 3.1 How FActScore Decomposes Text

FActScore (Min et al., 2023) decomposes generated biographies into atomic facts -- minimal, independent claims -- and verifies each against a knowledge source (Wikipedia). The decomposition is designed to produce facts that are "independent and minimal," each capturing exactly one verifiable claim.

For a sentence like "John was born in 1990 in Paris," FActScore would decompose this into:
- "John was born in 1990."
- "John was born in Paris."

Each atomic fact **binds the attribute to the entity**. The fact is not "someone was born in 1990" (unbound) but "John was born in 1990" (bound to John). This is critical: if the source text said "John was born in 1990 and Mary in 1985" but the generation swapped these to "John was born in 1985 and Mary in 1990," FActScore would produce:
- "John was born in 1985." --> NOT SUPPORTED (John was born in 1990)
- "Mary was born in 1990." --> NOT SUPPORTED (Mary was born in 1985)

Both atomic facts would fail, correctly penalising the transposition. However, note that FActScore penalises **each wrong binding independently** -- the two-element swap produces two failures, not one. FActScore does not attempt to identify that these two failures share a single root cause (transposition). The framework accepts this as a feature, not a bug: from the reader's perspective, two facts are wrong, so two penalties are appropriate.

### 3.2 Limitation: Independence Assumption

FActScore's independence assumption is harder to enforce for chart descriptions where facts are inherently correlated. A hallucinated data series simultaneously produces wrong values, wrong colours, wrong trends, and wrong legends. These are genuinely different facts about the same hallucinated entity, making clean atomic decomposition difficult without cascade. Our earlier research document (research_double_counting.md) covers this limitation in detail.

### 3.3 Relevance to Our Problem

FActScore's approach validates the **bound-item** model: each atomic fact binds an attribute to a specific entity. Applied to our pie chart example, the atomic facts would be:
- "Happiness has a value of 14.1%." -- WRONG (should be 8.1%)
- "Excitement has a value of 8.1%." -- WRONG (should be 14.1%)
- "Happiness is light purple." -- WRONG (should be blue)
- "Excitement is light blue." -- WRONG (should be red)

This produces four failures for what might be considered two root causes (two swapped slices). Whether this constitutes double-penalisation depends on the granularity at which we define "one error."

---

## 4. Structured Chart Evaluation Frameworks

### 4.1 StructChart: Structured Triplet Representations

StructChart (Xia et al., 2023) converts chart understanding from free-form visual QA to structured data extraction. It introduces Structured Triplet Representations (STR), which "reformulate chart data from the tabular form (linearized CSV) to STR." Each triplet binds a chart element to its attributes in a structured format, and the Structuring Chart-oriented Representation Metric (SCRM) evaluates perception accuracy by comparing predicted triplets against ground-truth triplets.

The STR approach is inherently **bound**: each triplet ties a specific label to its value and visual encoding. If a model swaps two values between two labels, the SCRM metric would flag two incorrect triplets -- one for each label whose value is wrong. This is analogous to FActScore's per-fact evaluation.

**Key insight:** StructChart's triplet representation makes transposition detection automatic. Because evaluation is per-triplet, swapped values produce per-element failures without needing a separate "mapping correctness" check. The mapping is embedded in the triplet structure itself.

### 4.2 ChartInstruct: Instruction-Tuned Extraction

ChartInstruct (Masry et al., 2024) uses two approaches to chart understanding: (1) end-to-end vision-language models and (2) a pipeline that extracts data tables, then reasons over them. The pipeline approach is relevant because extracting a data table forces explicit binding: each row in the extracted table maps a label to its values. If values are transposed, the extracted table is wrong at the cell level -- each misplaced value is an independent cell error.

### 4.3 UniChart: Pretraining with Chart-Specific Tasks

UniChart (Masry et al., 2023) pretrains on "chart-specific low- and high-level tasks to extract visual components and develop reasoning capabilities." The low-level tasks include extracting text, data, and visual elements from charts -- tasks that inherently produce bound (element, attribute) pairs. UniChart's pretraining tasks thus frame chart understanding as a binding problem, not an existence problem.

### 4.4 DePlot: Chart-to-Table as Binding Evaluation

DePlot (Liu et al., 2023) converts chart images to linearised data tables, which are then processed by an LLM for downstream tasks. The chart-to-table conversion step produces a structured representation where each row binds a label to its values. Evaluation of the conversion step (table accuracy) inherently tests value-label binding: a transposition would appear as two cell-level errors.

### 4.5 Summary

All structured chart evaluation frameworks represent chart data as **bound tuples** (element-attribute pairs or triplets). None separate element existence from element-attribute binding. The binding is the atomic unit of evaluation.

---

## 5. Information Extraction: Slot-Filling and Entity-Type Errors

### 5.1 NER Evaluation: Entity Type vs. Boundary Errors

Named Entity Recognition (NER) evaluation has long distinguished between two error types:

1. **Boundary errors:** The entity span is partially correct (e.g., recognising "New" instead of "New York").
2. **Type errors:** The entity span is correct but assigned the wrong type (e.g., recognising "Paris" as an ORG instead of LOC).

The standard CoNLL evaluation (Tjong Kim Sang and De Meulder, 2003) uses strict matching: both boundary and type must be correct for a true positive. Under strict matching, a type error produces one false positive (the wrong-type prediction) and one false negative (the missed correct-type entity). This is the NER analogue of our transposition problem: the entity text exists, and the type exists in the taxonomy, but they are bound incorrectly.

NoiseBench (2024) explicitly evaluates "incorrect labels for entity types and entity boundaries" as separate error categories, establishing that the field recognises these as distinct failure modes with different implications.

Recent work on NER error analysis (arXiv:2508.09323, 2025) introduces "an error taxonomy highlighting common failure modes such as boundary drift and type confusion," further formalising the distinction between recognition (does the entity exist?) and binding (is it the right type?).

### 5.2 Relation Extraction: Triple-Level Evaluation

Relation extraction evaluation uses triple-based matching: a predicted triple (entity1, relation, entity2) is correct only if all three components match the ground truth. If a model predicts (Paris, capital-of, Germany) when the truth is (Berlin, capital-of, Germany), this is one false positive and one false negative -- not a "partially correct" prediction. The evaluation is inherently bound at the triple level.

This is directly analogous to our chart setting: a predicted tuple (Happiness, 14.1%, purple) is evaluated against the ground truth tuple (Happiness, 8.1%, blue) as a complete unit.

### 5.3 Slot-Filling in Dialogue Systems

Slot-filling evaluation in task-oriented dialogue (Henderson et al., 2014; Budzianowski et al., 2018) distinguishes between:
- **Slot detection:** Was the slot type correctly identified? (e.g., recognising that a "departure city" slot exists)
- **Slot value:** Was the correct value assigned to the slot? (e.g., "departure city = London")

A transposition error in slot-filling would mean filling slot A with slot B's value and vice versa. Standard evaluation counts this as two errors (two wrong slot-value pairs), not one. The field does not attempt to identify that these form a single transposition event.

### 5.4 Relevance to Chart Description Evaluation

The IE evaluation literature consistently treats the **bound pair** (entity, type) or (slot, value) as the atomic unit. The field does not penalise existence and binding separately -- it penalises wrong bindings directly. There is no separate "existence check" that would pass when bindings are wrong.

This supports removing separate existence checks from our checklist (see Section 7).

---

## 6. The CHOCOLATE Error Taxonomy and Transposition

### 6.1 CHOCOLATE's Error Categories

CHOCOLATE (Huang et al., 2024) introduces a typology of factual errors in VLM-generated chart captions, published at ACL Findings 2024. The paper found an 81.27% non-factual rate in GPT-4V-generated chart captions. The error types include:

- **Value errors:** Incorrect numerical values stated for chart elements.
- **Label errors:** Wrong labels associated with chart elements (e.g., calling a "Revenue" bar "Profit").
- **Trend errors:** Incorrectly described trends (e.g., "increasing" when decreasing).
- **Out-of-scope claims:** Information not derivable from the chart.

### 6.2 Does CHOCOLATE Cover Transposition?

CHOCOLATE's taxonomy does **not** explicitly define a "transposition" or "swap" error category. A transposition -- where two labels have each other's values -- would be classified as either:
- Two **value errors** (each label has the wrong value), or
- Two **label errors** (each value is attached to the wrong label), or
- Some combination thereof.

The ambiguity is instructive. CHOCOLATE's categories are defined by what is wrong (the value, the label, the trend), not by the **root cause** of the error (transposition, hallucination, misreading). A single transposition produces two errors under any categorisation. CHOCOLATE does not attempt root-cause deduplication.

### 6.3 CHARTVE: Visual Entailment as Binding Verification

CHOCOLATE also introduces CHARTVE, a visual entailment model that checks whether claims in a caption are entailed by the chart image. CHARTVE operates at the claim level -- each claim is independently verified against the chart. A transposed pair of claims would produce two "not entailed" verdicts, one per claim. CHARTVE does not cross-reference claims to detect that they form a swap.

### 6.4 Gap in CHOCOLATE for Our Setting

CHOCOLATE does not provide guidance on:
1. Whether a transposition should count as one error or two.
2. How to instruct a judge to distinguish transposition from independent value/label errors.
3. How to avoid double-penalising when the same root cause (swap) manifests across multiple error categories.

This gap is what our checklist design (Section 7) must fill.

---

## 7. Bound vs. Unbound Checklist Design

### 7.1 The Two Approaches

**Approach A: Unbound Items (current design)**

Separate checklist items for each dimension:
1. "All slice labels mentioned" (completeness)
2. "All slice values accurate" (accuracy)
3. "Values correctly assigned to their slices" (mapping)
4. "Colour-to-label mapping correct" (colour)

Under this design, a transposition can fail items 2, 3, and 4 simultaneously. Item 1 passes (labels are all mentioned), item 2 may pass or fail depending on interpretation (are the values "accurate" if they exist but are on the wrong slice?), item 3 fails (mapping is wrong), and item 4 likely fails (colours are wrong too).

**Approach B: Bound Items (per-element tuples)**

One checklist item per chart element, each testing the complete binding:
1. "Happiness: value correct AND colour correct" (pass/fail)
2. "Excitement: value correct AND colour correct" (pass/fail)
3. ... (one item per slice)

Under this design, a transposition fails exactly the items corresponding to the swapped elements. Each element is evaluated as a unit. No separate mapping check is needed because mapping is embedded in the per-element evaluation.

### 7.2 Trade-Off Analysis

| Criterion | Unbound (Approach A) | Bound (Approach B) |
|-----------|---------------------|-------------------|
| **Double-penalisation risk** | High. One swap can fail 3+ items. | Low. One swap fails exactly the affected element items. |
| **Diagnostic granularity** | High. Can distinguish "all values present but misassigned" from "values missing entirely." | Lower. A failed element item does not indicate whether the value was wrong, the colour was wrong, or both. |
| **Judge instruction complexity** | High. Must instruct judge to check existence, accuracy, AND mapping as separate steps. Risk of bulk existence checks passing when mapping is wrong. | Lower. Judge evaluates one element at a time. Natural chain-of-thought: "For Happiness, the description says 14.1% -- does the chart show Happiness at 14.1%? No, it shows 8.1%. FAIL." |
| **Transposition detection** | Requires explicit mapping item that is easy for LLM judges to miss. | Automatic. Each element's binding is checked independently. |
| **Scalability** | Fixed number of items regardless of element count. | Number of items scales with number of elements. |
| **Cascading from hallucination** | A hallucinated element affects multiple unbound items (completeness, accuracy, mapping, colour). | A hallucinated element produces one "extra element" failure plus individual element mismatches. |
| **Severity assignment** | Can assign different severity per dimension (minor for colour, major for value). | Must assign severity per element, losing dimensional distinction. |

### 7.3 Hybrid Approach (Recommended)

The optimal design combines both approaches:

**Layer 1: Per-element bound evaluation.** For each ground-truth chart element, check whether the description correctly reports its (label, value, colour) tuple. Score each element as a unit. This catches transposition without double-penalising.

**Layer 2: Dimensional summary (derived, not separately scored).** After per-element evaluation, derive summary statistics: "How many elements have correct values?", "How many have correct colours?" These are analytical outputs, not additional penalty items. They provide diagnostic granularity without additional penalisation.

**Layer 3: Structural checks (independently scored).** A small number of structural items that are genuinely independent of element-level correctness:
- "Correct number of elements mentioned" (catches omissions and hallucinations at the count level)
- "No fabricated elements" (catches elements that appear in the description but not in the chart)

This three-layer design ensures:
- Transposition is penalised once per affected element (Layer 1), not once per dimension.
- Dimensional analysis is available for error characterisation (Layer 2) without score inflation.
- Structural correctness is checked independently (Layer 3).

### 7.4 Scoring Under the Hybrid Approach

For a pie chart with N slices, the scoring would be:

**Per-element score (Layer 1):**
For each ground-truth slice i, define a match score:
- Value correct AND colour correct: 1.0
- Value correct, colour wrong: 0.7 (colour is minor)
- Value wrong, colour correct: 0.3 (value is major)
- Both wrong: 0.0

Element-level score = (1/N) * sum of match scores.

**Structural score (Layer 3):**
- All elements present (no omissions): +1
- No fabricated elements: +1
- Penalty per omission: -0.5 (major)
- Penalty per fabrication: -0.5 (major)

**Total = weighted combination of element-level and structural scores.**

Under this scheme, the transposition example produces:
- Happiness: value wrong, colour wrong -> 0.0
- Excitement: value wrong, colour wrong -> 0.0
- Element-level score: 0.0 (both elements fully wrong)
- Structural score: all present, none fabricated -> full marks
- Total reflects that the description has the right elements but wrong bindings.

Compare to the unbound approach where the same error might score:
- Labels mentioned: PASS
- Values accurate: FAIL (ambiguous)
- Mapping correct: FAIL
- Colours correct: FAIL
- Three failures for one root cause.

---

## 8. Instructing an LLM Judge for Per-Element Binding Verification

### 8.1 The Bulk Existence Check Problem

When given an unbound checklist, LLM judges (including GPT-4o) tend to perform **bulk existence checks**: "Are all the values mentioned in the description present in the chart? Yes, 14.1% and 8.1% both appear. PASS." This misses that 14.1% is assigned to the wrong slice. The judge sees both values exist and does not verify which slice each belongs to.

This failure mode is well-documented in the LLM-as-judge literature. Zheng et al. (2023) found that LLM judges exhibit positional bias and verbosity preference; we add that they also exhibit **binding neglect** -- a tendency to verify element existence without verifying element-attribute binding.

### 8.2 Chain-of-Verification (CoVe) for Binding

Chain-of-Verification (Dhuliawala et al., 2023) provides a framework for structured self-verification. The method works in four steps: (1) draft an initial response, (2) plan verification questions, (3) answer verification questions independently, (4) generate a final verified response.

Applied to our setting, a CoVe-inspired judge would:
1. Read the description and identify all claimed (label, value, colour) tuples.
2. For each claimed tuple, generate a verification question: "Does the chart show that Happiness has a value of 14.1%?"
3. Answer each verification question by examining the chart image independently.
4. Compile results into a per-element binding assessment.

Step 3 is critical: by answering each verification question **independently** (not in the context of the full description), the judge avoids confirmation bias from having already seen the description's framing.

### 8.3 Element-by-Element Comparison Protocol

Based on the research, we recommend the following judge instruction protocol:

```
STEP 1: EXTRACT BINDINGS
From the description, extract each claimed element as a tuple:
(label, value, colour).
List all tuples.

STEP 2: EXTRACT GROUND TRUTH
From the chart image (or ground-truth annotation), extract
the actual (label, value, colour) for each element.

STEP 3: PER-ELEMENT VERIFICATION
For each ground-truth element:
  a. Find the matching label in the description's tuples.
  b. Check: Is the claimed value correct for this label?
  c. Check: Is the claimed colour correct for this label?
  d. Record: (label, value_correct, colour_correct).

STEP 4: STRUCTURAL CHECKS
  a. Are there elements in the description not in the chart? (fabrication)
  b. Are there elements in the chart not in the description? (omission)

STEP 5: COMPILE RESULTS
Report per-element binding scores and structural scores.
Do NOT add separate penalties for "mapping correctness" or
"value accuracy" beyond the per-element checks.
```

This protocol forces element-by-element comparison and prevents bulk existence checks.

### 8.4 Research on Forcing Structured LLM Evaluation

G-Eval (Liu et al., 2023) demonstrates that chain-of-thought prompting with a form-filling paradigm improves LLM evaluation quality, achieving 0.514 Spearman correlation with human judgments on summarisation. The form-filling approach -- where the judge fills in a structured form rather than producing free-text judgments -- is directly applicable to our per-element binding protocol. Each element's (value_correct, colour_correct) assessment is a form field, not a free-text opinion.

The Perturbation CheckLists framework (Sai et al., 2021) uses "templates which target a specific criteria and perturb the output such that the quality gets affected only along this specific criteria." This isolation principle supports our recommendation to evaluate each element independently rather than through cross-cutting dimensional checks.

MENLO (arXiv:2509.26601) shows that "zero-shot LLM judges benefit significantly from structured annotation rubrics," reinforcing that structured per-element evaluation outperforms holistic assessment for fine-grained quality dimensions.

### 8.5 Cross-Examination for Binding Verification

Cohen et al. (2023) propose LM-vs-LM cross-examination for detecting factual errors, where a second LM poses questions to expose inconsistencies. Applied to chart description evaluation, a cross-examination approach would:
1. Present the description without the chart to an LM and ask it to predict what the chart looks like.
2. Compare the predicted chart structure against the actual chart.
3. Inconsistencies reveal binding errors.

While more expensive than single-pass evaluation, cross-examination can catch subtle transposition errors that single-pass judges miss.

---

## 9. Putting It Together: Recommended Checklist Structure

### 9.1 For Pie Charts

Replace the current four unbound items:
- ~~"All slice labels mentioned"~~
- ~~"Slice values accurate"~~
- ~~"Values correctly assigned to their slices"~~
- ~~"Colour-to-label mapping correct"~~

With:

**Per-element items (one per ground-truth slice):**

| Item ID | Item Text | Severity |
|---------|-----------|----------|
| PIE-E1 | Slice "[Label]": value correctly reported as [X]% | Major |
| PIE-E2 | Slice "[Label]": colour correctly described | Minor |

(Repeat for each slice in the ground truth.)

**Structural items:**

| Item ID | Item Text | Severity |
|---------|-----------|----------|
| PIE-S1 | All slices from the chart are mentioned in the description | Major |
| PIE-S2 | No fabricated slices appear in the description | Critical |
| PIE-S3 | Total number of slices correctly stated (if stated) | Minor |

### 9.2 Scoring the Transposition Example

Ground truth: Happiness (8.1%, blue), Excitement (14.1%, red).
Description: Happiness (14.1%, light purple), Excitement (8.1%, light blue).

| Item | Verdict | Notes |
|------|---------|-------|
| PIE-E1: Happiness value = 8.1% | FAIL | Description says 14.1% |
| PIE-E2: Happiness colour = blue | FAIL | Description says light purple |
| PIE-E1: Excitement value = 14.1% | FAIL | Description says 8.1% |
| PIE-E2: Excitement colour = red | FAIL | Description says light blue |
| PIE-S1: All slices mentioned | PASS | Both labels present |
| PIE-S2: No fabricated slices | PASS | No extra slices |

Total: 4 element-level failures (2 major + 2 minor), 0 structural failures.

Compare to the unbound approach: the same errors would trigger failures on "values accurate" (ambiguous -- both values exist), "mapping correct" (clear fail), and "colours correct" (fail). The unbound approach might count 2-3 failures depending on interpretation, but the failures are at the wrong granularity -- they describe dimensions rather than elements, making it unclear which elements are wrong.

### 9.3 Generalisation to Other Chart Types

The bound-item approach generalises naturally:

- **Bar charts:** One item per bar: "Bar [Label]: value correctly reported as [X]."
- **Line charts:** One item per data series at each key point: "Series [Name] at [X]: value correctly reported as [Y]."
- **Scatter plots:** Per-cluster or per-annotated-point binding.

The structural items (omission, fabrication, count) remain the same across chart types.

---

## 10. Open Questions

1. **Severity of transposition vs. independent errors.** Should two swapped values (a single transposition) receive lower total penalty than two independently wrong values? FActScore and IE evaluation say no -- each wrong binding is equally wrong regardless of whether it forms a swap. But from a human-reader perspective, a swap may be less harmful than two random errors because a reader who notices the swap can mentally correct both values.

2. **Partial credit for near-correct bindings.** If Happiness is 8.1% and the description says 8.5%, this is a minor value error. If it says 14.1% (Excitement's value), this is a swap. Should these receive different penalties at the element level? The current scheme treats both as "value wrong." A refinement could distinguish near-misses from swaps by checking whether the wrong value belongs to another element.

3. **Judge reliability on per-element evaluation.** Per-element evaluation requires the judge to match each label in the description to the correct ground-truth element. For charts with many similar labels, this matching step itself may introduce errors. Testing judge reliability on per-element vs. dimensional evaluation is an empirical question.

4. **Scaling to large charts.** A pie chart with 12 slices produces 24 per-element items (value + colour for each). Combined with structural items, this may approach the instruction-following limits of current LLM judges. Chunking (evaluating 4-5 elements at a time) may be necessary.

---

## References

Budzianowski, P., Wen, T.-H., Tseng, B.-H., Casanueva, I., Ultes, S., Ramadan, O., and Gasic, M. (2018). MultiWOZ -- A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling. In *Proceedings of EMNLP*.

Cohen, R., Hamri, M., Geva, M., and Berant, J. (2023). LM vs LM: Detecting Factual Errors via Cross Examination. In *Proceedings of EMNLP*. arXiv:2305.13281.

Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., and Weston, J. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. arXiv:2309.11495.

Henderson, M., Thomson, B., and Williams, J. D. (2014). The Second Dialog State Tracking Challenge. In *Proceedings of SIGDIAL*.

Huang, K.-H., Zhou, M., Chan, H. P., Fung, Y. R., Wang, Z., Zhang, L., Chang, S.-F., and Ji, H. (2024). Do LVLMs Understand Charts? Analyzing and Correcting Factual Errors in Chart Captioning. In *Findings of ACL 2024*. arXiv:2312.10160.

Kafle, K., Price, B., Cohen, S., and Kanan, C. (2018). DVQA: Understanding Data Visualizations via Question Answering. In *Proceedings of CVPR*. arXiv:1801.08163.

Kahou, S. E., Michalski, V., Atkinson, A., Kadar, A., Trischler, A., and Bengio, Y. (2018). FigureQA: An Annotated Figure Dataset for Visual Reasoning. In *ICLR 2018 Workshop*. arXiv:1710.07300.

Liu, F., Piccinno, F., Krichene, S., Pang, C., Lee, K., Joshi, M., Altun, Y., Collier, N., and Eisenschlos, J. (2023). DePlot: One-shot visual language reasoning by plot-to-table translation. In *Findings of ACL 2023*.

Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., and Zhu, C. (2023). G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment. In *Proceedings of EMNLP*. arXiv:2303.16634.

Masry, A., Do, X. L., Tan, J. Q., Joty, S., and Hoque, E. (2022). ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning. In *Proceedings of ACL*. arXiv:2203.10244.

Masry, A., Kavehzadeh, P., Do, X. L., Hoque, E., and Joty, S. (2023). UniChart: A Universal Vision-language Pretrained Model for Chart Comprehension and Reasoning. In *Proceedings of EMNLP*. arXiv:2305.14761.

Masry, A., Shahmohammadi, M., Parvez, M. R., Hoque, E., and Joty, S. (2024). ChartInstruct: Instruction Tuning for Chart Comprehension and Reasoning. In *Findings of ACL 2024*. arXiv:2403.09028.

Methani, N., Ganguly, P., Khapra, M. M., and Kumar, P. (2020). PlotQA: Reasoning over Scientific Plots. In *Proceedings of WACV*. arXiv:1909.00997.

Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, P. W., Iyyer, M., Zettlemoyer, L., and Hajishirzi, H. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In *Proceedings of EMNLP*. arXiv:2305.14251.

Sai, A. B., Dixit, T., Sheth, D. Y., Mohan, S., and Khapra, M. M. (2021). Perturbation CheckLists for Evaluating NLG Evaluation Metrics. In *Proceedings of EMNLP*. arXiv:2109.05771.

Tjong Kim Sang, E. F. and De Meulder, F. (2003). Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition. In *Proceedings of CoNLL*.

Wang, Z., Xia, M., He, L., Chen, H., et al. (2024). CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs. arXiv:2406.18521.

Xia, R., Peng, H., Ye, H., Li, M., Yan, X., Ye, P., Shi, B., Qiao, Y., Yan, J., and Zhang, B. (2023). StructChart: Perception, Structuring, Reasoning for Visual Chart Understanding. arXiv:2309.11268.

Xu, Z., Du, S., Qi, Y., Xu, C., Yuan, C., and Guo, J. (2023). ChartBench: A Benchmark for Complex Visual Reasoning in Charts. arXiv:2312.15915.

Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., and Stoica, I. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In *NeurIPS 2023 Datasets and Benchmarks*. arXiv:2306.05685.
