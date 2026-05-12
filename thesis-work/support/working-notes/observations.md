# Key Observations, Gaps, and Limitations

Findings across all four research questions. These feed into the Discussion and Limitations sections of the thesis.

---

## RQ1 Discussion Topics (Description Quality)

### 1. Proprietary-Open Gap Is Narrowing But Uneven
Qwen-235B within 4.7 of GPT-5.2, but Gemma lags 17+ points. Architecture matters more than parameters: Qwen-32B outperforms Gemma-27B by 11.6 points despite similar size. The convergence may reflect rapid improvements in open-source visual instruction tuning, particularly within the Qwen-VL family.

### 2. Numerical Precision as the Fundamental Bottleneck
Incorrect Numerical Value is the #1 error type at 30.6% of all errors. Models cannot reliably read exact percentages, axis values, and data points from figures, even with ±3 percentage point tolerance. This is not an OCR problem but an imprecision problem (reporting "approximately 45%" when figure shows 42.3%). Mean 2.7 incorrect numerical values per figure. Implications for accessibility are sobering: a blind researcher would encounter nearly 3 wrong numbers per figure.

### 3. Verbosity-Accuracy Trade-off (Claude)
Claude Opus produces the longest descriptions (mean 224 words vs 164-195 for other top models). More words create more verifiable claims, inflating error counts under MQM. Claude's atom accuracy (0.75) trails GPT-5.2 and Gemini (0.80). Its thoroughness backfires under strict MQM evaluation. Claude also gets the highest Incorrect Numerical Value rate from Mistral (3.3/fig vs 2.5-2.7 for peers) and higher Visual Attribute Mapping errors (1.3-1.7/fig vs 0.8-1.3).

### 4. Completeness-Accuracy Trade-off
Models face an implicit trade-off between completeness and accuracy. Top models resolve this better: GPT-5.2 achieves both higher atom accuracy (75.0%) and higher completeness (74.5%) than Gemma-4B (55.5% and 50.3%). Weaker models do not fail on one dimension alone; they fail on both. Smaller models hallucinate MORE, not less, contradicting the assumption that being conservative would preserve accuracy.

### 5. The Language Paradox
German scores highest uncontrolled (mean 72.5), but controlled cross-lingual comparison (13 parallel figures × 4 languages) reverses this entirely: English scores highest, German drops to middle/bottom. Dataset composition confound: German figures are simpler (15.8 atoms/fig vs 19.4 English) with more bar charts and fewer pie charts. Chinese is the most resilient non-English language (EN-CN gap 4-17%). Bulgarian trails due to under-representation in training corpora. Small models degrade disproportionately on non-English (Gemma-4B 42% EN-DE gap vs Claude 2%).

### 6. LLM-as-Judge Reliability
Segment vs system dissociation: per-figure Spearman ~0.6 (moderate) but system-level ~0.95 (near-perfect). Judges should not be trusted for individual figures but are reliable for ranking models. Asymmetric harshness bias: strongest for high-quality descriptions (GPT-5.2: -25.6 from GPT-4o) and weakest for poor ones (Gemma-27B: -2.2). Severity split: GPT-4o 78% Major vs Mistral 47% on same errors. Dual-judge averaging stabilises rankings.

### 7. Pie Chart Difficulty + Atom Granularity Artefact
Pie charts score 15-25 points below line/bar charts. ~11 points from scoring artefact (dense atoms pack multiple verifiable facts per sentence, generating 5-7 errors from one atom), ~14 points genuine difficulty. Capping at 1 error/atom lifts pie charts by 11 points while barely affecting other types (<3 points).

### 8. Colour Tolerance Limitation
Judges penalise semantically equivalent colour descriptions ("cyan" vs "blue", "crimson" vs "red") despite explicit tolerance instructions. English disproportionately affected (~5.1% penalty vs ~2.0% Chinese) due to richer colour vocabulary. Multiple fix attempts (compound rules, few-shot examples, self-reflection) failed or worsened results. Documented as systematic LLM-judge limitation.

### 9. Hallucination-Capacity Inverse
Hallucination rate correlates inversely with model capacity. Gemma-4B at 0.65/fig (4.6× GPT-5.2's 0.14/fig). Claude has the lowest hallucination rate (0.09/fig from GPT-4o judge). Smaller models lack discriminative capacity to distinguish image content from language priors. RLHF alignment helps.

### 10. Scaling Plateau
Qwen 235B ≈ 32B (Δ=0.4, p=.34) — diminishing returns at the top. Gemma scales more steeply (Δ=5 per step, all p<.001). For scientific figure understanding, scaling benefits plateau earlier in Qwen than Gemma, possibly due to architectural differences in visual encoding.

---

## RQ2 Discussion Topics (Degradation)

### 11. Robustness ≠ Baseline Quality
Robustness to image transforms is partially independent of baseline description quality. LLaMA Scout ranks 3rd on originals (71.0) but 12th on robustness (|Δ̄|=6.2). Gemini and Claude are both high-baseline AND robust. Clean-condition benchmark rankings may overestimate real-world utility for accessibility applications where figures are frequently degraded through scanning, photocopying, or PDF re-encoding.

### 12. Spatial Disruption vs Pixel Corruption
Rotation (Δ=-4.7) degrades performance far more than noise (Δ=-0.4) or JPEG compression (Δ=+0.2). VLMs process spatial layout globally rather than reading individual pixels. Rotation disrupts spatial relationships between axes, labels, and data elements. Low contrast (Δ=-1.2) falls between, reducing discriminability without disrupting layout. Consistent with adversarial robustness literature on image classifiers (Hendrycks & Dietterich, 2019).

### 13. Page Context as Double-Edged Sword
Models respond divergently to original-in-paper condition. Gemini (+5.7) and Phi-4 (+18.9) extract useful cues from surrounding paper text (titles, captions, methodology). LLaMA Scout (-16.9) and Gemma-27B (-14.7) degrade substantially, treating page context as noise. Optimal strategy depends on deployment scenario: context extraction beneficial for accessibility tools processing known papers, strict visual grounding safer for general-purpose use.

---

## RQ3 Discussion Topics (Comprehension)

### 14. Description vs Comprehension Are Distinct Capabilities
Ranking inversion between description (RQ1) and comprehension (RQ3). Gemini ranks 2nd on description (72.7) but 1st on comprehension (.81). GPT-5.2 leads description (75.5) but trails on comprehension (.78). Claude rank 5 on description → rank 3 on comprehension. Different model capacities engaged: description rewards thoroughness and precision; comprehension demands selective attention and targeted extraction.

### 15. The Counting Gap
Comparison (.42) and counting (.44) are the hardest question types, while computation (.51) is easiest. Inverts the intuition that numerical computation would be hardest. Models can often compute correctly from approximate values but struggle to compare elements or count discrete visual features. Echoes findings from MMMU and ChartQA.

### 16. Caption Bias as Visual Grounding Test
Providing paper captions can DISTORT model answers. Strong-grounding models resist (Gemini .82, GPT-5.2 .78). Weak-grounding models get anchored by caption framing (Qwen-235B drops .58→.36). Parallels sycophancy in language models: when given strong textual signal, weakly grounded models defer to it regardless of visual evidence.

### 17. Prompt Reversal as Grounding Signal
LLaMA Scout (.14) agrees with nearly any premise. Gemini (.98) maintains its reading regardless of prompt framing. Prompt reversal resistance correlates strongly with overall model quality. Failure indicates models default to linguistic plausibility rather than image evidence. Together with caption bias, forms a practical test battery for visual grounding strength.

---

## RQ4 Discussion Topics (Behavioural Dynamics)

### 18. Admittance-Inductance Tension
Fundamental tension: a model that always admits (high A) won't attempt inference (low I). A model that aggressively infers (high I) risks fabricating when inference isn't warranted (low A). Gemini resolves optimally: admits when unrecoverable (.70) but correctly infers when context supports (.1.0). GPT-5.2 errs toward caution (low active admittance .07, moderate inductance .80). May reflect RLHF training that penalises refusal more than fabrication.

### 19. Resistance as Visual Grounding
GPT-5.2 is surprisingly weak on resistance (.56), engaging with false premises rather than rejecting them. Contra-factual probes are hardest (mean .24) — models struggle to override plausible-sounding incorrect statements. Direct implications for trustworthiness in deployment: a model must not only describe accurately but resist being misled by context or adversarial queries.

### 20. Behavioural Profiles as Model Fingerprints
Each model has a distinctive A-R-I signature visible in the dot-strip chart. Gemini: large balanced profile. Claude: strong admittance and inductance, moderate resistance (tuned for honesty). Qwen-32B: spike in inductance (.95) despite modest admittance (.26) — strong reasoning without epistemic honesty. These profiles cannot be predicted from RQ1 description quality alone.

### 21. The Silent Fabricator Problem
Gemma family and Phi-4 score near zero on Admittance and low on Resistance. They neither admit uncertainty nor resist false premises — they fabricate regardless of whether content is recoverable. This represents the most dangerous deployment scenario: a model that appears confident but is systematically unreliable.

---

## Cross-Cutting Discussion Topics

### 22. Gemini as All-Round Champion
Gemini leads or co-leads on all four RQs: RQ1 rank 2 (72.7), RQ2 most robust (|Δ̄|=1.9), RQ3 rank 1 (.81), RQ4 all three A-R-I axes (.70/.89/1.0). No other model achieves this consistency. GPT-5.2 leads RQ1 but falls behind on RQ3 comprehension and RQ4 resistance.

### 23. Framework Limitations
- Colour synonym false positives (5.1% English penalty)
- Atom granularity artefact (pie charts +11 points from capping)
- Judge severity disagreement (78% vs 47% Major)
- Dataset composition confound (German figures simpler)
- Verbosity penalty in MQM (longer descriptions → more errors)
- Segment-level judge unreliability (ρ~0.6 per figure)

### 24. Implications for Accessibility
What these findings mean for blind researchers using VLM-generated figure descriptions:
- 2.7 wrong numerical values per figure on average
- Pie charts receive least reliable descriptions
- Hallucination rate 0.14-0.65 per figure depending on model
- Descriptions under degraded conditions (scanned PDFs) less reliable
- Models may agree with misleading context rather than visual evidence
- Gemini is the safest choice across all dimensions; GPT-5.2 is most accurate but less robust behaviourally

---

## Summary Statistics

- 13 models, 120 figures, 2 judges, 2,966 evaluations, 26,364 errors
- Human evaluation: 4 models, 30 figures, 3 annotators, 159 annotations, ICC=0.91
- Cross-lingual controlled: 5 models, 13 parallel figures, 4 languages
- Adversarial: 45 figures, 8 transforms, 13 models
- Capability: 630 questions, 5 categories, 13 models
- Behavioural probes: 3 axes (A-R-I), 9 inferable elements, 3 probe types
- Score range: 48.5 (Gemma-4B) to 75.5 (GPT-5.2)
- Three statistically distinct tiers separated at ranks 2-3 and 9-10
