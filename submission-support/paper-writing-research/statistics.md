# Statistical Analysis Plan for SciFig-Eval

All statistics computed from existing results. No new experiments needed.

---

## Group 1: Bootstrap Confidence Intervals

Every mean reported in Tables 3 and 4 needs a 95% CI.

### What to compute
- For each model x condition cell, take the per-figure scores
- Resample with replacement B=10,000 times
- Compute mean of each resample
- Report 2.5th and 97.5th percentile as 95% CI

### Where it applies
- Table 3: MQM scores for all conditions (baseline, original, noise, rotation, low_contrast, in_paper, in_paper_blur, caption_bias, admittance_blur, inductance_blur)
- Table 4: Resistance overall and per probe type, caption bias resistance, active/passive admittance admits%, active/passive inductance correct%

### How to report
- In tables: mean ± half-width (e.g., 91.6 ± 1.8)
- Or: mean with subscript CI (e.g., 91.6$_{89.2}^{93.8}$)
- Pick one format and use consistently

### Input data
- MQM: `results/evaluation/description_tasks/baseline_descriptions/{model}/{fig_id}.json` field `mqm_deduped`
- Transforms: `results/evaluation/description_tasks/transforms/{transform}/{model}/{fig_id}.json` field `mqm_deduped`
- Resistance: `results/evaluation/resistance/{model}/{fig_id}.json` field `evaluations[].judge_score`
- Caption bias: `results/evaluation/caption_bias/{model}/{fig_id}.json` fields `followed_image`, `followed_caption`
- Active probes: `results/evaluation/active_probes/{model}/{type}/{fig_id}.json` fields `admits`, `fabricates`, `correct`
- Passive probes: `results/evaluation/passive_probes/{model}/{type}/{fig_id}.json` fields `admits`, `fabricates`, `correct`

---

## Group 2: Paired Bootstrap Significance Tests

For model-vs-model comparisons. Tests whether the difference between two models is statistically significant.

### What to compute
- For each pair of models on the same figures, resample figure indices with replacement B=10,000
- Compute difference of means for each resample
- p-value = proportion of resamples where the difference has opposite sign to the observed difference
- Apply Holm-Bonferroni correction for multiple comparisons (8 models = 28 pairs)

### Where it applies
- Table 3: Is GPT-5.2 significantly better than Gemini on baseline MQM? Is the drop from baseline to rotation significant?
- Table 4: Is Gemini significantly more resistant than GPT-5.2? Is the admittance gap (90% vs 6%) significant?

### How to report
- Significance markers as superscripts in tables
- * p < 0.05, ** p < 0.01, *** p < 0.001 (after Holm-Bonferroni correction)
- Compare each model against the best model in each column
- Also compare within-model across conditions (is the drop from baseline to noise significant for GPT-5.2?)

### Key pairs to test
- GPT-5.2 vs Gemini (top 2 on quality)
- GPT-5.2 vs Gemini on admittance (6% vs 90%)
- Gemini vs all others on resistance
- Phi-4 vs all others on caption bias (0.05 vs rest)
- Active vs passive admittance for each model (is the gap significant?)
- Inductance correct vs admittance correct for each model (validates the A-R-I distinction)

---

## Group 3: Effect Sizes

p-values tell you if a difference exists. Effect sizes tell you if it matters.

### What to compute
- Cliff's delta for ordinal data (MQM scores, resistance scores)
  - delta = (number of times model A > model B minus number of times B > A) / (n_A * n_B)
  - Interpretation: |d| < 0.147 negligible, < 0.33 small, < 0.474 medium, >= 0.474 large
- Cohen's d for continuous data where appropriate
  - d = (mean_A - mean_B) / pooled_SD
  - Interpretation: < 0.2 negligible, < 0.5 small, < 0.8 medium, >= 0.8 large

### Where it applies
- Key comparisons in Table 3 and 4
- Most important: GPT-5.2 vs Gemini on MQM (are they practically different or just statistically?)
- Transform drops: is the rotation drop a large or small effect?
- Admittance gap: Cliff's delta between Gemini and GPT-5.2 on admittance scores

### How to report
- In text for key comparisons: "GPT-5.2 outperforms Gemini on MQM (Cliff's delta = 0.23, small effect)"
- In appendix table for all pairs
- Reviewers increasingly expect this alongside p-values

---

## Group 4: Inter-Annotator Agreement

Validates that our annotations are reliable.

### What to compute

#### For structured checklist annotations
- Krippendorff's alpha (ordinal) on checklist item ratings
- Two annotators rated the same figures on the same items
- Items are ordinal: correct/partial/wrong for correctness, complete/partial/missing for coverage

#### For composite MQM scores
- ICC(2,1) (two-way random, single measures) on the final MQM scores
- This measures whether annotators produce consistent composite scores

#### For capability question ground truth
- Cohen's kappa for binary/categorical answers (comparison questions: yes/no)
- Percentage agreement for numeric answers (counting, computation) with tolerance window

### Thresholds (community standards)
- Krippendorff's alpha >= 0.667: tentative conclusions allowed
- Krippendorff's alpha >= 0.80: reliable
- ICC >= 0.75: good
- ICC >= 0.90: excellent
- Cohen's kappa >= 0.61: substantial agreement
- Cohen's kappa >= 0.81: almost perfect

### Where it applies
- Table 1 or Dataset section: report alpha and ICC
- If alpha < 0.667 on any dimension, discuss in limitations

### Input data
- Annotations from `dataset/groundtruth/{fig_id}.json`
- Human evaluation data from the MQM validation study (30 figures, 2 annotators)
- Capability question annotator responses from `dataset/capability_answers/{fig_id}.json`

---

## Group 5: Stability and Generalization

Proves that our sample size is adequate and results generalize.

### 5a. Split-Half Reliability
- Take the 100 primary figures, randomly split into two halves of 50 (seed=42)
- Compute model rankings on each half separately
- Report Spearman rho between the two half-rankings
- Repeat for 100 random splits, report mean rho and CI
- Target: rho > 0.90 means rankings are stable

### 5b. Stratified Stability
- Compute model rankings separately for bar charts (40), line plots (40), pie charts (20)
- Report Spearman rho between each pair of chart-type rankings
- Show Kendall's W (coefficient of concordance) across all three types
- If rankings hold across types, results generalize beyond chart-type composition

### 5c. Saturation Curve
- For the 100-figure primary subset, compute the metric at incremental sample sizes: 20, 40, 60, 80, 100
- For each size, sample 50 random subsets, compute mean and CI of the metric
- Plot the curve showing convergence
- If CI narrows and mean stabilizes by 60-80, the sample size is sufficient
- Do this for MQM baseline and resistance score

### 5d. Scale Validation (100 vs 250)
- We ran resistance on 100 (sampled) and 250 (all) figures
- Compare rankings: if Spearman rho between 100-figure and 250-figure rankings is high, the sample generalizes
- Report the rho and individual score changes

### Where it applies
- Main paper: one sentence summarizing split-half rho and scale validation
- Appendix: full saturation curves, stratified rankings, all splits

### Input data
- All existing MQM and resistance results
- `dataset/sampled_100.json` for the primary subset figure IDs
- Groundtruth for chart type labels

---

## Group 6: Ablation Statistics

Proves our methodology is robust to design choices.

### 6a. Probe Designer Independence
- Same 50 figures, GPT-4o vs Mistral probes, GPT-5.2 as test model
- Paired bootstrap on the difference in resistance scores
- Paired bootstrap on the difference in caption bias scores
- If CIs of the difference include zero, no significant effect of probe designer

### 6b. Judge Consistency
- If we have results from multiple judge models, compare rankings
- If only GPT-4o, acknowledge as limitation but cite Zheng et al. (2023) on judge-human agreement

### Where it applies
- Main paper: one paragraph in Analysis section
- Report paired bootstrap p-value and Cliff's delta for each ablation

### Input data
- Resistance: `results/evaluation/resistance/gpt-5.2/` vs `results/evaluation/resistance_mistral/gpt-5.2/`
- Caption bias: `results/evaluation/caption_bias/gpt-5.2/` vs `results/evaluation/caption_bias_mistral/gpt-5.2/`
- Same 50 figure IDs from `dataset/ablation_50.json`

---

## Implementation Plan

### Script: `compute_statistics.py`

Single script that reads all results and outputs a JSON file with all computed statistics.

#### Functions needed:

```
bootstrap_ci(scores, B=10000, ci=0.95)
    -> returns (mean, lower, upper)

paired_bootstrap_test(scores_a, scores_b, B=10000)
    -> returns (diff, p_value, ci_lower, ci_upper)

cliffs_delta(scores_a, scores_b)
    -> returns (delta, interpretation)  # negligible/small/medium/large

cohens_d(scores_a, scores_b)
    -> returns (d, interpretation)

krippendorff_alpha(ratings_matrix, level='ordinal')
    -> returns alpha

icc_2_1(ratings_matrix)
    -> returns icc

split_half_reliability(scores_dict, n_splits=100, seed=42)
    -> returns (mean_rho, ci_lower, ci_upper)

saturation_curve(scores_dict, sizes=[20,40,60,80,100], n_samples=50)
    -> returns {size: (mean, ci_lower, ci_upper)}

stratified_stability(scores_dict, chart_types)
    -> returns {type_pair: spearman_rho}
```

#### Output: `results/statistics/all_statistics.json`

```json
{
  "bootstrap_cis": {
    "baseline_mqm": {"gpt-5.2": {"mean": 91.6, "ci_lower": 89.2, "ci_upper": 93.8}, ...},
    "resistance": {...},
    ...
  },
  "significance_tests": {
    "baseline_mqm": {"gpt-5.2_vs_gemini": {"diff": 1.4, "p": 0.23, "significant": false}, ...},
    ...
  },
  "effect_sizes": {...},
  "iaa": {"krippendorff_alpha": 0.87, "icc": 0.92},
  "stability": {
    "split_half": {"mean_rho": 0.94, "ci": [0.91, 0.97]},
    "stratified": {"bar_vs_line": 0.93, "bar_vs_pie": 0.88, ...},
    "saturation": {...},
    "scale_validation": {"rho_100_vs_250": 0.98}
  },
  "ablation": {
    "probe_designer_resistance": {"diff": 0.06, "p": 0.12, "significant": false},
    "probe_designer_caption_bias": {"diff": 0.02, "p": 0.45, "significant": false}
  }
}
```

This JSON feeds directly into table generation. One source of truth for all numbers in the paper.

---

## What Goes Where

### Main Paper Tables
- Bootstrap CIs on every cell (Group 1)
- Significance markers vs best model (Group 2)
- Key effect sizes mentioned in text (Group 3)
- IAA in dataset section (Group 4)
- Split-half rho mentioned in one sentence (Group 5a)
- Ablation result in one paragraph (Group 6a)

### Appendix Tables
- Full pairwise significance matrix (Group 2)
- All effect sizes for all pairs (Group 3)
- Stratified stability per chart type (Group 5b)
- Saturation curves (Group 5c, as figure)
- Scale validation details (Group 5d)
- Per-dimension MQM breakdown (Accuracy, Completeness, Clarity)
- Per chart type breakdown for all metrics
- Per probe type breakdown with CIs

### Limitations Section
- Single judge model (GPT-4o) without cross-judge validation
- English only
- 3 chart types
- IAA if below 0.80 on any dimension
