# SciFig-Eval: Comprehensive Insights & Analysis Plan

## Data Inventory

| Dataset | Location | n (per model) | Models | Notes |
|---|---|---|---|---|
| Baseline MQM | `results/evaluation/description_tasks/baseline_descriptions/{model}/` | 250 | 8 | Full figure set |
| Transform MQM (noise, rotation, low_contrast) | `results/evaluation/description_tasks/transforms/{transform}/{model}/` | ~97 | 8 | Subset of 250 |
| Transform MQM (in_paper, in_paper_blur) | `results/evaluation/description_tasks/transforms/{transform}/{model}/` | ~97 | 8 | Context effect |
| Transform MQM (caption_bias) | `results/evaluation/description_tasks/transforms/caption_bias/{model}/` | ~100 | 5 (missing phi, qwen-30b, qwen-8b) | MQM under poisoned caption |
| Transform MQM (admittance_blur, inductance_blur) | `results/evaluation/description_tasks/transforms/{transform}/{model}/` | ~50 | 5-8 | Selective blur MQM |
| Caption Bias Behavioral | `results/evaluation/caption_bias/{model}/` | 100 | 8 | per-modification: type, principle, mapped_to, resistance |
| Resistance (hallucination probes) | `results/evaluation/resistance/{model}/` | 250 | 8 | probe_type: inexist/contra/unanswerable, judge_score |
| Resistance (Mistral ablation) | `results/evaluation/resistance_mistral/gpt-5.2/` | 50 | 1 (GPT-5.2 only) | Ablation probe designer |
| Caption Bias (Mistral ablation) | `results/evaluation/caption_bias_mistral/` | ? | ? | Ablation probe designer |
| Active Probes (admittance) | `results/evaluation/active_probes/{model}/admittance/` | 50 | 8 | admits, fabricates, correct |
| Active Probes (inductance) | `results/evaluation/active_probes/{model}/inductance/` | 50 | 8 | admits, fabricates, correct |
| Passive Probes (admittance) | `results/evaluation/passive_probes/{model}/admittance/` | 50 | 8 | admits, fabricates, correct, mentioned |
| Passive Probes (inductance) | `results/evaluation/passive_probes/{model}/inductance/` | 50 | 8 | admits, fabricates, correct, mentioned |
| Capability Questions | `results/generation/capability/gpt-5.2/` | 100 | 1 (GPT-5.2 only) | Generated Qs: counting, computation, comparison, pattern_analysis |
| Human Evaluation | `results/evaluation/human_evaluation/human_eval.json` | 30 figs | 4 models | 3 annotators, 159 annotations |

### Key Fields per File Type

- **MQM files**: `figure_type`, `mqm_deduped`, `penalties_deduped[].{category, severity, sub_type, id, weight, source, detail}`
- **Resistance files**: `evaluations[].{probe_type, judge_score}`, `scores.{inexist, contra, unanswerable}`, `figure_type`
- **Caption Bias files**: `evaluations[].{type, principle, mapped_to}`, `resistance`, `followed_image`, `followed_caption`, `figure_type`
- **Active Probes**: `probe_type`, `blurred_element`, `admits`, `fabricates`, `correct`
- **Passive Probes**: `probe_type`, `blurred_element`, `admits`, `fabricates`, `correct`, `mentioned`, `description_length`
- **Capability Qs**: `questions[].{category, difficulty, answer_type}`

---

## A. MQM Quality Analysis

### A1. Overall Leaderboard (8 models)
- **Data**: All 250 baseline MQM files per model. Average `mqm_deduped`.
- **Available**: YES
- **Placement**: Main paper (Table 3)
- **Impact**: HIGH -- core result, establishes quality ranking
- **Computation**: Mean mqm_deduped across 250 figures per model. Include std dev. Report median too for robustness.

### A2. Per Chart Type Breakdown (bar vs line vs pie)
- **Data**: Baseline MQM, group by `figure_type`. Three groups: Bar Chart, Line Plot, Pie Chart.
- **Available**: YES
- **Placement**: Main paper (Table 3, sub-columns or separate rows)
- **Impact**: HIGH -- reveals which chart types are harder. Pie charts likely harder (percentage estimation). Line plots may be easier or harder depending on trend complexity.
- **Computation**: Mean mqm_deduped per (model, figure_type). Also compute how many figures per type.

### A3. Per MQM Dimension Breakdown (Accuracy vs Completeness vs Clarity)
- **Data**: `penalties_deduped[].category` across all baseline files. Three categories from checklists.py: Accuracy, Completeness, Clarity and Readability.
- **Available**: YES
- **Placement**: Main paper or appendix (depends on how interesting the split is)
- **Impact**: MEDIUM -- shows what KIND of errors dominate. If Accuracy dominates, models hallucinate values. If Completeness, models miss elements. If Clarity, descriptions are messy.
- **Computation**: For each model, count and sum penalties by category. Report % of total penalty per dimension. Identify dominant error dimension.

### A4. Per Severity Breakdown (Major vs Minor)
- **Data**: `penalties_deduped[].severity` across all baseline files.
- **Available**: YES
- **Placement**: Appendix (less interesting than dimension)
- **Impact**: LOW -- mostly confirms Major errors are more common/impactful
- **Computation**: Count Major vs Minor penalties per model. Ratio of Major/Minor errors.

### A5. Most Common Error Sub-Types Across Models
- **Data**: `penalties_deduped[].sub_type`. Sub-types from checklists.py: Incorrect Numerical Value, Incorrect Trend Interpretation, Incorrect Axis or Legend Interpretation, Incorrect Label Mapping, Missing Key Information, Hallucinated Content, Ambiguous Description, Missing Takeaway, Over-Generalization, Overly Verbose Description, Poor Sentence Structure.
- **Available**: YES
- **Placement**: Main paper or appendix (if space). Top 5 error types in a bar chart could be compelling.
- **Impact**: HIGH -- practical takeaway for users ("models most commonly get numerical values wrong")
- **Computation**: Aggregate sub_type counts across all models. Also per-model breakdown.

### A6. Which Checklist Items Models Struggle With Most
- **Data**: `penalties_deduped[].id` links to checklist items (bar_01 through bar_14, line_01 through line_15, pie_01 through pie_11).
- **Available**: YES
- **Placement**: Appendix (detailed, but useful for future work)
- **Impact**: MEDIUM -- shows bar_11 (numerical values) is likely the hardest item across models
- **Computation**: Error rate per checklist item across all models. Heatmap: models x checklist items.

### A7. Model Size vs Quality Correlation
- **Data**: MQM scores + model parameter counts. Sizes: GPT-5.2 (unknown/large), Gemini (unknown/large), Llama4 (17Bx128E MoE), Qwen-235B (22B active), Qwen-30B (3B active), Qwen-8B (8B dense), Gemma (27B dense), Phi-4 (small/14B).
- **Available**: PARTIALLY -- commercial model sizes unknown. Open-weight sizes known.
- **Placement**: Analysis section (1-2 sentences + Figure 3 or scatter)
- **Impact**: MEDIUM -- interesting if there's a clear correlation or notable outliers (Qwen-235B MoE vs Gemma dense)
- **Note**: Use "active parameters" for MoE models for fair comparison.

### A8. Open vs Closed Model Comparison
- **Data**: Split models into commercial (GPT-5.2, Gemini, Phi-4) vs open-weight (Llama4, Qwen-235B, Qwen-30B, Qwen-8B, Gemma).
- **Available**: YES
- **Placement**: Analysis section (1-2 sentences)
- **Impact**: MEDIUM -- ACL audience cares about open-weight viability
- **Computation**: Mean MQM for each group. Statistical test (Mann-Whitney U).

---

## B. Transform Robustness Analysis

### B1. MQM Drop from Baseline per Transform
- **Data**: Compare baseline MQM (original subset only, matched figures) vs each transform MQM. Transforms: noise, rotation, low_contrast, in_paper, in_paper_blur, caption_bias, admittance_blur, inductance_blur. Also `original` (rerun on same subset as control).
- **Available**: YES
- **Placement**: Main paper (Table 4)
- **Impact**: HIGH -- key robustness finding. Which transforms degrade quality most?
- **Computation**: For each model and transform, compute mean MQM on the matched figure subset. Delta = transform_mqm - baseline_mqm (on matched figures). Use the `original` transform as control to measure variance from re-running.

### B2. Which Transforms Hurt Most/Least (Averaged Across Models)
- **Data**: Same as B1, but aggregate across models.
- **Available**: YES
- **Placement**: Main paper (discussion of Table 4)
- **Impact**: HIGH -- "rotation causes the largest average MQM drop" or "noise has minimal impact"
- **Computation**: Mean delta per transform (averaged across all 8 models).

### B3. Which Models Are Most/Least Robust
- **Data**: Same as B1, but rank models by average delta across all transforms.
- **Available**: YES
- **Placement**: Main paper (1-2 sentences in Table 4 discussion)
- **Impact**: HIGH -- Gemini or GPT-5.2 likely most robust. Phi-4 likely least.
- **Computation**: Average absolute MQM drop across all transforms per model.

### B4. Per Chart Type Sensitivity to Transforms
- **Data**: Transform MQM results grouped by figure_type.
- **Available**: YES (if subset has all three chart types)
- **Placement**: Appendix
- **Impact**: LOW-MEDIUM -- interesting if pie charts are more sensitive to noise (harder to read values)
- **Computation**: Mean delta per (transform, figure_type).

### B5. In-Paper vs In-Paper-Blur Comparison (Context Effect)
- **Data**: `in_paper` transform (figure embedded in PDF page) vs `in_paper_blur` (same but with background blur). Both compared to baseline.
- **Available**: YES
- **Placement**: Main paper (key finding about context)
- **Impact**: HIGH -- Does surrounding page context help or hurt? Does blurring the page context change anything?
- **Computation**: Mean MQM for in_paper vs in_paper_blur vs baseline (matched figures). Paired comparison.

### B6. Admittance/Inductance Blur MQM Impact
- **Data**: `admittance_blur` and `inductance_blur` transforms. These are MQM scores on descriptions of selectively blurred images (50 figures).
- **Available**: YES
- **Placement**: Main paper (connects to A-R-I framework section)
- **Impact**: HIGH -- Shows quality degradation from selective blur. Does blur of inferable elements (inductance) cause less MQM drop than blur of unrecoverable elements (admittance)?
- **Computation**: Mean MQM for each blur type vs baseline (matched 50 figures).

### B7. Original Transform as Control (Rerun Reliability)
- **Data**: `original` transform (same images rerun). Should yield similar MQM to baseline.
- **Available**: YES
- **Placement**: Appendix (methodology validation)
- **Impact**: MEDIUM -- validates that MQM scoring is stable across runs
- **Computation**: Correlation and mean absolute difference between baseline and original rerun.

---

## C. Caption Bias Analysis

### C1. Overall Resistance Score per Model
- **Data**: Caption bias files: `resistance` field per figure. Average across 100 figures.
- **Available**: YES (8 models)
- **Placement**: Main paper (Table 5)
- **Impact**: HIGH -- shows which models trust image vs caption
- **Computation**: Mean resistance per model. resistance = followed_image / (followed_image + followed_caption).

### C2. Resistance by Modification Type
- **Data**: `evaluations[].type` -- types include: value_anchor, trend_characterization, and potentially others.
- **Available**: YES
- **Placement**: Main paper or appendix
- **Impact**: HIGH -- which kind of false claim is hardest to resist? Value anchors (wrong numbers) vs trend characterizations (wrong direction)?
- **Computation**: Per (model, modification_type), compute fraction of modifications where model followed image.

### C3. Which Psychological Principle Is Most Effective
- **Data**: `evaluations[].principle` -- principles include: anchoring, loaded_verb, and potentially others.
- **Available**: YES
- **Placement**: Main paper (connects to psychology framing)
- **Impact**: HIGH -- "anchoring is most effective at misleading models" connects to Tversky & Kahneman
- **Computation**: Per principle, compute average resistance (fraction image-following). Lower = more effective deception.

### C4. Correlation Between MQM Quality and Caption Resistance
- **Data**: Baseline MQM per model + caption bias resistance per model.
- **Available**: YES
- **Placement**: Main paper (Figure 3 scatter plot)
- **Impact**: HIGH -- core orthogonality argument. If correlation is low, proves quality != reliability.
- **Computation**: Spearman rho between MQM rank and resistance rank (8 models).

### C5. Models That Resist Values but Fall for Trends (or Vice Versa)
- **Data**: Combine C2 per model. Look at value_anchor resistance vs trend_characterization resistance.
- **Available**: YES
- **Placement**: Analysis section (1-2 sentences)
- **Impact**: MEDIUM -- nuanced finding about model vulnerability profiles
- **Computation**: Per model, delta between value_anchor_resistance and trend_characterization_resistance.

### C6. Caption Bias MQM vs Baseline MQM (Quality Impact of Poisoned Captions)
- **Data**: `results/evaluation/description_tasks/transforms/caption_bias/{model}/` (MQM under poisoned caption) vs baseline MQM on matched figures.
- **Available**: YES (5 models only: gemini, gemma, gpt-5.2, llama4, qwen-235b)
- **Placement**: Main paper
- **Impact**: HIGH -- if caption-following models also get LOWER MQM under poisoned captions, it shows the practical danger
- **Computation**: Matched figure MQM comparison. Models that follow captions more should have larger MQM drops.

### C7. Per Chart Type Caption Bias Vulnerability
- **Data**: Caption bias files grouped by `figure_type`.
- **Available**: YES
- **Placement**: Appendix
- **Impact**: MEDIUM -- are models more caption-dependent for certain chart types?
- **Computation**: Mean resistance per (model, figure_type).

### C8. Not-Addressed Rate Analysis
- **Data**: `not_addressed` field in caption bias files (modifications the model didn't address at all).
- **Available**: YES
- **Placement**: Appendix
- **Impact**: LOW -- supplementary to C1
- **Computation**: Mean not_addressed per model.

---

## D. Hallucination Resistance Analysis

### D1. Overall Resistance Score per Model
- **Data**: Resistance files: mean of `scores.{inexist, contra, unanswerable}` per figure, averaged across 250 figures.
- **Available**: YES (8 models)
- **Placement**: Main paper (Table 5)
- **Impact**: HIGH -- core behavioral metric

### D2. Per Probe Type Breakdown (inexist vs contra vs unanswerable)
- **Data**: `scores.inexist`, `scores.contra`, `scores.unanswerable` per figure.
- **Available**: YES
- **Placement**: Main paper (Table 5 or sub-table)
- **Impact**: HIGH -- key finding: inexist is hardest, unanswerable is easiest (Finding 4 in framing)
- **Computation**: Mean score per (model, probe_type). 3 columns in Table 5.

### D3. Which Probe Type Is Hardest (Averaged Across Models)
- **Data**: Same as D2.
- **Available**: YES
- **Placement**: Main paper (discussion)
- **Impact**: HIGH -- connects to psychology: presupposition embedding (inexist) is most effective deception
- **Computation**: Mean resistance per probe_type across all models.

### D4. Per Chart Type Vulnerability
- **Data**: Resistance files grouped by `figure_type`.
- **Available**: YES
- **Placement**: Appendix
- **Impact**: MEDIUM -- are models more vulnerable to hallucination probes on certain chart types?
- **Computation**: Mean resistance per (model, figure_type, probe_type).

### D5. Model Family Patterns
- **Data**: Group Qwen models (235B, 30B, 8B) and compare. Track if MoE architecture correlates with resistance.
- **Available**: YES
- **Placement**: Analysis section
- **Impact**: MEDIUM -- "Qwen family shows consistent pattern: larger active params = more resistant" or "MoE architecture doesn't help resistance"
- **Computation**: Qwen-235B vs Qwen-30B vs Qwen-8B resistance scores.

### D6. Resistance Score Distribution (Variance Analysis)
- **Data**: Per-figure resistance scores.
- **Available**: YES
- **Placement**: Appendix
- **Impact**: LOW -- shows whether models are consistently resistant or variable
- **Computation**: Std dev and IQR of resistance per model.

---

## E. A-R-I Framework Analysis

### E1. Active Admittance Rate per Model
- **Data**: Active probes admittance files: `admits` field. Rate = count(admits=true) / total.
- **Available**: YES (8 models, 50 figures each)
- **Placement**: Main paper (Table 6)
- **Impact**: HIGH -- the "honesty gap" finding. Gemini admits 90%, GPT-5.2 admits 6%.

### E2. Active Inductance Correct Rate per Model
- **Data**: Active probes inductance files: `correct` field. Rate = count(correct=true) / total.
- **Available**: YES (8 models, 50 figures each)
- **Placement**: Main paper (Table 6)
- **Impact**: HIGH -- validates inductance concept. Models can infer from context.

### E3. Passive vs Active Comparison for Admittance
- **Data**: Passive probes admittance (in description task) vs active probes admittance (targeted question).
- **Available**: YES
- **Placement**: Main paper (Table 6, two rows)
- **Impact**: HIGH -- do models admit more when asked directly (active) vs in open-ended description (passive)?
- **Computation**: Compare admit rates: passive vs active per model.

### E4. Passive vs Active Comparison for Inductance
- **Data**: Passive probes inductance vs active probes inductance.
- **Available**: YES
- **Placement**: Main paper (Table 6, two rows)
- **Impact**: MEDIUM -- same comparison for inference ability

### E5. Fabrication Rate per Model
- **Data**: `fabricates` field in both active and passive probes.
- **Available**: YES
- **Placement**: Main paper (key finding)
- **Impact**: HIGH -- "98% fabrication rate across most models" is headline-worthy
- **Computation**: Mean fabrication rate per model (both admittance and inductance).

### E6. Correct Fabrication Rate: Admittance vs Inductance (The Validation)
- **Data**: `correct` field for admittance probes (should be low -- element is unrecoverable) vs inductance probes (should be higher -- element is inferable).
- **Available**: YES
- **Placement**: Main paper (Finding 5 in framing)
- **Impact**: HIGH -- validates the A-R-I distinction. If correct rate for inductance >> correct rate for admittance, the framework captures real behavioral differences.
- **Computation**: Mean correct rate per (probe_type) across all models. Expected: admittance correct ~0-14%, inductance correct ~21-81%.

### E7. Text vs Numeric Blur Target Performance
- **Data**: `blurred_element` field in probe files. Could categorize as text labels vs numeric values.
- **Available**: PARTIALLY -- would need to inspect blurred_element values and classify them
- **Placement**: Appendix
- **Impact**: MEDIUM -- are models better at admitting when numbers are blurred vs text labels?
- **Computation**: Classify blurred_element as text/numeric, then compare admit/correct rates.

### E8. Per Chart Type A-R-I Patterns
- **Data**: Cross-reference probe figure_ids with baseline MQM to get figure_type. Or check if probe files contain figure_type.
- **Available**: PARTIALLY -- probe files don't seem to contain figure_type directly. Need to join with baseline.
- **Placement**: Appendix
- **Impact**: LOW-MEDIUM
- **Computation**: Join probe results with baseline by figure_id to get chart type, then aggregate.

### E9. The "Mentioned" Field in Passive Probes
- **Data**: `mentioned` field in passive probes (did the model mention the blurred element at all in its description?).
- **Available**: YES
- **Placement**: Appendix or analysis section
- **Impact**: MEDIUM -- models that mention a blurred element are actively fabricating (vs just ignoring it)
- **Computation**: Mentioned rate per model for admittance (should not mention) vs inductance (might reasonably mention if inferred).

### E10. Correlation Between Admittance and Resistance
- **Data**: Active admittance rate per model + resistance score per model.
- **Available**: YES
- **Placement**: Main paper (cross-dimensional scatter)
- **Impact**: HIGH -- tests whether honest models are also resistant (or if they're independent)
- **Computation**: Spearman rho between admittance rank and resistance rank.

---

## F. Cross-Dimensional Analysis

### F1. Quality Rank vs Resistance Rank
- **Data**: MQM ranking + resistance ranking (both from 8 models).
- **Available**: YES
- **Placement**: Main paper (Figure 3 scatter or Analysis section)
- **Impact**: HIGH -- core orthogonality claim
- **Computation**: Spearman rho. Expected: moderate positive but not 1.0.

### F2. Quality Rank vs Admittance Rank
- **Data**: MQM ranking + admittance ranking.
- **Available**: YES
- **Placement**: Main paper (Figure 3 or Analysis)
- **Impact**: HIGH -- GPT-5.2 is #1 quality but #4 admittance. This is the key "quality != honesty" finding.
- **Computation**: Spearman rho.

### F3. MQM vs Caption Bias Resistance Scatter
- **Data**: Mean MQM per model + mean caption bias resistance per model.
- **Available**: YES
- **Placement**: Main paper (combined into Figure 3 multi-panel scatter)
- **Impact**: HIGH
- **Computation**: Plot 8 points. Annotate each with model name.

### F4. Model Size vs Behavioral Reliability
- **Data**: Parameter count + A-R-I scores.
- **Available**: PARTIALLY (commercial model sizes unknown)
- **Placement**: Analysis
- **Impact**: MEDIUM -- does scaling improve honesty?
- **Note**: Can focus on open-weight Qwen family (8B, 30B, 235B) for controlled comparison.

### F5. Commercial vs Open-Weight Behavioral Comparison
- **Data**: Split models and compare A-R-I + resistance scores.
- **Available**: YES
- **Placement**: Analysis (1-2 sentences)
- **Impact**: MEDIUM
- **Computation**: Mean behavioral scores per group.

### F6. Radar Chart per Model (A-R-I + Quality + Resistance)
- **Data**: Normalize all metrics to 0-1 scale: MQM/100, resistance, caption bias resistance, admittance rate, inductance correct rate.
- **Available**: YES
- **Placement**: Main paper (Figure 4)
- **Impact**: HIGH -- visually compelling way to show model profiles
- **Computation**: 5 axes per model. Plot 8 overlapping radar charts (or pick top 4 models for clarity).

### F7. Transform Robustness vs Behavioral Reliability
- **Data**: Average MQM drop across transforms per model + resistance score.
- **Available**: YES
- **Placement**: Appendix or analysis
- **Impact**: MEDIUM -- are transform-robust models also behaviorally reliable?
- **Computation**: Spearman rho between robustness rank and resistance rank.

---

## G. Ablation & Validation Studies

### G1. Mistral vs GPT-4o Probe Designer
- **Data**: `resistance_mistral` (Mistral-designed probes) vs `resistance` (GPT-4o-designed probes) for GPT-5.2 (50 figures).
- **Available**: YES (resistance_mistral has 50 files for gpt-5.2)
- **Placement**: Main paper (Analysis section, 1-2 sentences)
- **Impact**: HIGH -- addresses circularity concern. If both probe designers yield similar resistance scores, results are robust.
- **Computation**: Mean resistance for GPT-5.2 under Mistral probes vs GPT-4o probes. Report both and delta.
- **Note**: Also check `caption_bias_mistral` for caption bias ablation.

### G2. Human Evaluation Agreement
- **Data**: `human_evaluation/human_eval.json` -- 30 figures, 4 models, 3 annotators, 159 annotations.
- **Available**: YES
- **Placement**: Main paper (validates automated MQM)
- **Impact**: HIGH -- inter-annotator agreement + correlation with automated MQM scores
- **Computation**: 
  - IAA (Krippendorff's alpha or Spearman between annotators)
  - Correlation between human MQM and automated MQM for the 4 evaluated models
  - Whether automated MQM preserves the ranking from human eval

### G3. Split-Half Reliability (250-Figure Stability)
- **Data**: Baseline MQM for 250 figures. Split randomly, compute MQM on each half, check correlation.
- **Available**: YES (can compute from raw data)
- **Placement**: Appendix
- **Impact**: MEDIUM -- validates that 250 figures is sufficient
- **Computation**: Random 50/50 split, Spearman between model rankings on each half. Repeat N times for bootstrap CI.

### G4. 100 vs 250 Figure Resistance Comparison
- **Data**: Resistance on full 250 figures. Can compute on subset of 100 and compare to full 250.
- **Available**: YES
- **Placement**: Appendix
- **Impact**: LOW -- supplementary stability check
- **Computation**: Compare model rankings on first 100 vs full 250.

### G5. Caption Bias MQM Ablation: with vs without Poisoned Caption
- **Data**: Compare MQM from `transforms/caption_bias/` (poisoned caption) vs `transforms/original/` (clean rerun) on matched figures.
- **Available**: YES (5 models)
- **Placement**: Main paper or appendix
- **Impact**: MEDIUM -- quantifies the MQM cost of caption poisoning
- **Computation**: Paired MQM difference on matched figures.

---

## H. Capability Question Analysis (Reasoning Axis)

### H1. Capability Baseline Results per Category
- **Data**: `results/generation/capability/gpt-5.2/` -- 100 figures with 4 questions each (counting, computation, comparison, pattern_analysis).
- **Available**: PARTIALLY -- generation files exist for GPT-5.2 only. Need to check if evaluation files exist for all models.
- **Placement**: Main paper (if multi-model) or appendix (if GPT-5.2 only)
- **Impact**: MEDIUM-HIGH -- completes the 2x2 matrix (standard reasoning axis)
- **Note**: Check `results/generation/capability/` for other models. If only GPT-5.2, this is a limitation.

### H2. Difficulty vs Accuracy
- **Data**: `difficulty` field in capability questions (hard, very_hard).
- **Available**: YES (in generation files)
- **Placement**: Appendix
- **Impact**: LOW -- supplementary
- **Computation**: Accuracy per difficulty level.

---

## I. Additional High-Value Insights

### I1. The Sycophancy Spectrum
- **Data**: Caption bias resistance (0 to 1) ordered across models.
- **Available**: YES
- **Placement**: Analysis section
- **Impact**: HIGH -- connect to RLHF literature. Phi-4 (0.05) is almost fully sycophantic. Gemini (0.90) is independent.
- **Narrative**: "Models fall on a sycophancy spectrum from near-total caption dependency (Phi-4, R=0.05) to visual independence (Gemini, R=0.90)"

### I2. The Confident Fabricator Profile
- **Data**: Combine: high MQM + low admittance + high fabrication rate.
- **Available**: YES
- **Placement**: Main paper (Introduction hook)
- **Impact**: HIGH -- GPT-5.2 is #1 quality but fabricates 94%+ of the time under blur. This is the paper's headline.
- **Narrative**: "The model that writes the best descriptions is also the one that most confidently fabricates information it cannot see."

### I3. MoE vs Dense Architecture Comparison
- **Data**: Qwen-235B (MoE, 22B active) vs Gemma (27B dense) -- similar active parameter count, different architecture.
- **Available**: YES
- **Placement**: Analysis
- **Impact**: MEDIUM -- does MoE architecture help/hurt behavioral reliability at similar active param count?
- **Computation**: Compare all metrics between Qwen-235B and Gemma.

### I4. Error Correlation Across Figures
- **Data**: Per-figure MQM scores across models. Do all models struggle with the same figures?
- **Available**: YES
- **Placement**: Appendix
- **Impact**: MEDIUM -- if correlation is high, some figures are intrinsically harder. If low, model-specific weaknesses.
- **Computation**: Spearman between per-figure MQM vectors for each model pair.

### I5. Judge Consistency (GPT-4o Self-Bias Check)
- **Data**: GPT-5.2 MQM is judged by GPT-4o (same family). Compare with how GPT-4o judges other models.
- **Available**: YES (all evals use gpt-4o as judge)
- **Placement**: Limitations section
- **Impact**: MEDIUM -- address reviewer concern about judge bias. If human eval (G2) confirms rankings, this is mitigated.

### I6. Penalty Density Analysis
- **Data**: `num_penalties_deduped` and `num_items` per file. How many items get penalized on average?
- **Available**: YES
- **Placement**: Appendix
- **Impact**: LOW -- supplementary
- **Computation**: Mean penalties per model. Distribution of penalty counts.

---

## Priority Ranking for Paper

### Must-Have (Main Paper)
1. A1 -- Overall MQM leaderboard
2. A2 -- Per chart type MQM
3. B1 -- Transform robustness table
4. B5 -- In-paper vs in-paper-blur context effect
5. C1 -- Caption bias resistance per model
6. C3 -- Psychological principle effectiveness
7. D1 -- Overall hallucination resistance
8. D2 -- Per probe type breakdown
9. E1 -- Active admittance rate (honesty gap)
10. E5 -- Fabrication rate
11. E6 -- Admittance vs inductance correct rate (validation)
12. F1-F3 -- Orthogonality correlations
13. F6 -- Radar chart
14. G1 -- Probe designer ablation
15. G2 -- Human evaluation agreement

### Should-Have (Main Paper if Space, Otherwise Appendix)
16. A3 -- Per MQM dimension breakdown
17. A5 -- Common error sub-types
18. B2-B3 -- Most/least robust transforms and models
19. B6 -- Selective blur MQM impact
20. C2 -- Resistance by modification type
21. C6 -- Caption bias MQM impact
22. D5 -- Model family patterns (Qwen scaling)
23. E3-E4 -- Active vs passive comparison
24. E10 -- Admittance-resistance correlation
25. I1 -- Sycophancy spectrum narrative
26. I2 -- Confident fabricator profile narrative
27. I3 -- MoE vs dense comparison

### Nice-to-Have (Appendix)
28. A4 -- Major vs Minor severity
29. A6 -- Checklist item difficulty heatmap
30. A7-A8 -- Model size and open/closed comparisons
31. B4 -- Per chart type transform sensitivity
32. B7 -- Original transform control
33. C5 -- Value vs trend resistance per model
34. C7-C8 -- Chart type caption bias, not-addressed rate
35. D4 -- Per chart type hallucination vulnerability
36. D6 -- Resistance variance analysis
37. E7-E9 -- Text vs numeric blur, chart type A-R-I, mentioned field
38. F4-F5, F7 -- Size/open-closed behavioral, robustness-reliability correlation
39. G3-G5 -- Split-half, 100 vs 250, caption bias MQM ablation
40. H1-H2 -- Capability question results
41. I4-I6 -- Error correlation, judge bias check, penalty density

---

## Data Gaps & Limitations to Flag

1. **Capability questions**: Only GPT-5.2 generation exists. If not evaluated across all 8 models, the "reasoning standard" cell of the 2x2 matrix is incomplete.
2. **Caption bias transforms MQM**: Only 5 of 8 models have MQM under poisoned captions (missing Phi-4, Qwen-30B, Qwen-8B).
3. **Mistral ablation**: Only GPT-5.2 resistance_mistral data exists (50 figures). No multi-model ablation.
4. **Human evaluation**: Only 4 of 8 models evaluated by humans (GPT-5.2, Qwen-8B, Qwen-30B, Gemma). Missing Gemini, Llama4, Qwen-235B, Phi-4.
5. **Commercial model sizes**: Unknown parameter counts for GPT-5.2 and Gemini prevent full size-quality correlation analysis.
6. **Single judge**: All automated evals use GPT-4o as judge. Addressed by human eval + Mistral ablation, but remains a limitation.
