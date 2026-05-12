# Statistical Metrics for RQ1

## 1. Inter-Annotator Agreement (Human Judges)

### Krippendorff's Alpha (primary)
- **What**: Gold-standard agreement metric for ordinal/interval data
- **Why**: Handles 3+ annotators, tolerates missing values, works with continuous MQM scores
- **Compute on**: 39 double-annotated items (Judge 1 vs Judge 13), MQM scores as interval data
- **Package**: `krippendorff` Python package
- **Report**: Single alpha value with 95% bootstrap CI
- **Interpretation**: alpha > 0.80 = reliable, 0.67-0.80 = acceptable, < 0.67 = tentative
- **Reference**: Krippendorff (2011). Computing Krippendorff's Alpha-Reliability

### Cohen's Kappa (pairwise, secondary)
- **What**: Pairwise agreement correcting for chance
- **Why**: Standard supplementary metric; reviewers expect it
- **Compute on**: Judge 1 vs Judge 13 on the 39 overlapping items
- **Note**: Requires discretization — bin MQM scores into categories (e.g., Poor <50, Fair 50-70, Good 70-85, Excellent >85) or use weighted kappa on ordinal bins
- **Package**: `sklearn.metrics.cohen_kappa_score` with `weights='quadratic'`
- **Report**: Weighted kappa with 95% CI

### Intraclass Correlation Coefficient (ICC)
- **What**: Measures absolute agreement between raters on continuous scores
- **Why**: More appropriate than kappa for continuous MQM scores; standard in psychometrics
- **Compute**: ICC(2,1) — two-way random, single measures, absolute agreement
- **Package**: `pingouin.intraclass_corr`
- **Report**: ICC value with 95% CI

---

## 2. Human-Judge Correlation

### Spearman's Rho (primary)
- **What**: Rank correlation between human and LLM judge scores
- **Why**: Standard in WMT metrics shared tasks since 2020; robust to non-linear relationships
- **Compute on**: 4 models × 30 figures = 120 (figure, model) pairs with both human and judge scores
- **Pairs**: Human vs GPT-4o, Human vs Mistral, GPT-4o vs Mistral
- **Package**: `scipy.stats.spearmanr`
- **Report**: rho value + p-value + 95% bootstrap CI

### Kendall's Tau (secondary)
- **What**: Rank correlation based on concordant/discordant pairs
- **Why**: WMT standard for segment-level metric evaluation; more conservative than Spearman
- **Compute on**: Same pairs as Spearman
- **Package**: `scipy.stats.kendalltau`
- **Report**: tau value + p-value

### Pearson's r (supplementary)
- **What**: Linear correlation
- **Why**: Shows whether relationship is linear (not just monotonic)
- **Compute on**: Same pairs
- **Report**: r value + p-value; include only if relationship appears linear in scatter plot

---

## 3. Confidence Intervals

### Bootstrap CIs on MQM Scores (primary)
- **Method**: BCa (bias-corrected and accelerated) bootstrap, 10,000 resamples
- **Compute on**: Every cell in the main leaderboard table (13 models × overall + 4 languages)
- **Report**: 95% CI as (lower, upper) or as +/- after the mean
- **Implementation**:
  ```python
  from scipy.stats import bootstrap
  res = bootstrap((scores,), np.mean, n_resamples=10000, method='BCa')
  ci_low, ci_high = res.confidence_interval
  ```
- **Reference**: Efron & Tibshirani (1993). An Introduction to the Bootstrap

### Standard Error
- **Compute**: SE = std / sqrt(n) for each model's score distribution
- **Report**: In parentheses in tables where CI is too wide to display

---

## 4. Statistical Significance (Pairwise Model Comparisons)

### Paired Bootstrap Test (primary)
- **What**: Tests whether the difference between two models is significant
- **Why**: Recommended by Dror et al. (ACL 2018, "The Hitchhiker's Guide")
- **Method**: 10,000 bootstrap resamples of paired score differences
- **Compute on**: All adjacent model pairs in the ranking (13 models = 12 adjacent pairs minimum; or all 78 pairs)
- **Report**: p-value; mark significant differences with * (p<0.05) and ** (p<0.01) in tables
- **Implementation**:
  ```python
  def paired_bootstrap(scores_a, scores_b, n_resamples=10000):
      diffs = np.array(scores_a) - np.array(scores_b)
      n = len(diffs)
      count = 0
      for _ in range(n_resamples):
          sample = np.random.choice(diffs, size=n, replace=True)
          if sample.mean() <= 0:
              count += 1
      return count / n_resamples
  ```

### Wilcoxon Signed-Rank Test (secondary)
- **What**: Non-parametric paired test
- **Why**: Doesn't assume normal distribution of score differences
- **Package**: `scipy.stats.wilcoxon`
- **Apply Bonferroni correction** for multiple comparisons

---

## 5. Effect Size

### Cliff's Delta (primary)
- **What**: Non-parametric effect size; probability that a score from model A exceeds model B
- **Why**: MQM scores are unlikely normal; Cliff's delta is robust to skewness
- **Interpretation**: |d| < 0.147 = negligible, < 0.33 = small, < 0.474 = medium, else large
- **Compute on**: All pairwise model comparisons where difference is significant
- **Implementation**:
  ```python
  def cliffs_delta(x, y):
      n_x, n_y = len(x), len(y)
      more = sum(1 for xi in x for yi in y if xi > yi)
      less = sum(1 for xi in x for yi in y if xi < yi)
      return (more - less) / (n_x * n_y)
  ```

---

## 6. MQM-Specific Metrics

### Error Density
- **Formula**: errors_per_figure = total_errors / num_figures
- **Report per**: model, category (Accuracy/Completeness/Clarity), severity (Major/Minor)

### Severity Ratio
- **Formula**: major_ratio = major_errors / total_errors
- **Report per**: model and per judge (human vs GPT-4o vs Mistral)
- **Key finding**: Judges differ in severity assignment (Mistral 26-31% Major vs GPT-4o 69-71%)

### Normalized MQM Score (already implemented)
- **Formula**: MQM = max(0, 100 - (sum_penalties / (num_atoms * 5.0)) * 100)
- **Weights**: Accuracy Major=5.0, Minor=2.0; Completeness Major=3.5, Minor=1.5; Clarity Major=2.0, Minor=1.0

### Atom-Level Accuracy and Completeness
- **Accuracy**: correct_atoms / (correct_atoms + inaccurate_atoms)
- **Completeness**: correct_atoms / (correct_atoms + missing_atoms)
- **Report per**: model, language

---

## 7. Cross-Lingual Metrics

### Performance Gap (EN-X)
- **Formula**: gap_X = (score_EN - score_X) / score_EN * 100
- **Report for**: X in {Bulgarian, Chinese, German}
- **Per model**: Shows which models degrade most for non-English
- **Reference**: BenchMAX (EMNLP 2025 Findings)

### Script-Family Grouping
- **Latin script**: English, German
- **Cyrillic script**: Bulgarian
- **CJK script**: Chinese
- **Report aggregate**: performance per script group to distinguish script-related failures from language understanding failures

---

## Summary of What to Report Where

| Metric | Where | Priority |
|--------|-------|----------|
| Bootstrap 95% CI | Every score in main leaderboard | Required |
| Krippendorff's alpha | Judge agreement section | Required |
| Spearman's rho + Kendall's tau | Human-judge correlation | Required |
| Paired bootstrap p-values | Pairwise model comparisons | Required |
| Cliff's delta | Alongside significant comparisons | Recommended |
| Cohen's weighted kappa | Supplementary agreement | Recommended |
| ICC | Supplementary agreement | Recommended |
| Wilcoxon test | Secondary significance test | Optional |
| Pearson's r | Only if scatter is linear | Optional |
