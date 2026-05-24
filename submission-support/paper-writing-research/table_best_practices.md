# Table Best Practices for ACL Best Paper Submissions

Research compiled from ACL 2024-2026 standards, ARR reviewer guidelines, Dror et al. (2018),
Berg-Kirkpatrick et al. (2012), and analysis of ACL best paper winners.

---

## 1. Statistical Reporting Requirements (ACL/ARR 2024-2026)

### What ARR Officially Requires

The **Responsible NLP Research Checklist** (mandatory for all ARR submissions) states:

> **C3**: "Error bars can be computed by running experiments with different random seeds,
> Clopper-Pearson confidence intervals can be placed around the results."

> Results must clarify whether reporting **max values, means, single runs, or other aggregations**.
> Validation set results should accompany test set results.

The **ARR Reviewer Guidelines** (codes R1-R5) explicitly instruct reviewers to flag:

- **R1**: "inappropriate/misleading statistics or data presentation, p-hacking, presenting
  the 'best' results out of an unknown number of trials"
- **R5**: "at least the main experimental results should be accompanied by appropriate
  information about their statistical significance (error bars, confidence intervals,
  statistical significance tests)"
- Effect size estimation is "very welcome"

### What This Means for Our Tables

Every main result table MUST have one of:
- Standard deviation across seeds (minimum 3 seeds, preferably 5)
- Bootstrap confidence intervals (95%)
- Both (ideal for best paper)

### Recommended Statistical Tests (per Dror et al. 2018, ACL P18-1128)

**The decision protocol:**

1. **Are observations paired?** (same test items, different models) -> Yes for our setup
2. **Is the metric normally distributed?** -> Usually no for NLP metrics
3. **What is the measurement scale?** -> Ordinal (MQM scores) or ratio (accuracy)

**Test selection by scenario:**

| Scenario | Recommended Test | Alternative |
|----------|-----------------|-------------|
| Two models, same test set, classification | McNemar's test | Paired bootstrap |
| Two models, same test set, continuous metric | Paired bootstrap | Wilcoxon signed-rank |
| Two models, same test set, BLEU/ROUGE-like | Approximate randomization | Paired bootstrap |
| Multiple models, ranking | Friedman test + post-hoc Nemenyi | Bootstrap + Bonferroni |
| Comparing to many baselines | Holm-Bonferroni correction | Bonferroni (more conservative) |

**For our MQM evaluation paper specifically:**
- **Primary**: Paired bootstrap test (models evaluated on same 45/1005 figures)
- **Secondary**: Wilcoxon signed-rank (ordinal MQM scores)
- **For rankings**: Friedman test across 11 models
- **Correction**: Holm-Bonferroni when comparing all model pairs

---

## 2. Bootstrap Confidence Intervals

### Parameters

| Parameter | Minimum | Recommended | Best Paper Standard |
|-----------|---------|-------------|-------------------|
| Resamples (B) | 1,000 | 10,000 | 10,000 |
| Confidence level | 95% | 95% | 95% (report 99% in appendix) |
| Method | Percentile | BCa (bias-corrected accelerated) | BCa |
| Seeds for variance | 3 | 5 | 5+ |

### Implementation for Our Paper

```python
import numpy as np
from scipy import stats

def paired_bootstrap_test(scores_a, scores_b, n_bootstrap=10000, seed=42):
    """
    Paired bootstrap test for comparing two models on same test set.
    Returns p-value and 95% CI of the difference.
    """
    rng = np.random.RandomState(seed)
    n = len(scores_a)
    diff = scores_a - scores_b
    observed_diff = np.mean(diff)
    
    boot_diffs = np.array([
        np.mean(rng.choice(diff, size=n, replace=True))
        for _ in range(n_bootstrap)
    ])
    
    # Two-sided p-value
    p_value = np.mean(np.abs(boot_diffs - np.mean(boot_diffs)) >= np.abs(observed_diff))
    
    # 95% CI using percentile method
    ci_lower = np.percentile(boot_diffs, 2.5)
    ci_upper = np.percentile(boot_diffs, 97.5)
    
    return observed_diff, p_value, (ci_lower, ci_upper)

def bootstrap_ci(scores, n_bootstrap=10000, ci=95, seed=42):
    """Bootstrap CI for a single model's scores."""
    rng = np.random.RandomState(seed)
    n = len(scores)
    boot_means = np.array([
        np.mean(rng.choice(scores, size=n, replace=True))
        for _ in range(n_bootstrap)
    ])
    alpha = (100 - ci) / 2
    return np.percentile(boot_means, alpha), np.percentile(boot_means, 100 - alpha)
```

### How to Report in Tables

**Option A: Plus-minus notation (compact, preferred for main tables)**
```
72.3 +/- 1.2
```

**Option B: CI in parentheses (more precise)**
```
72.3 (70.8, 73.9)
```

**Option C: Subscript CI (very compact, for space-constrained tables)**
```
72.3_{70.8}^{73.9}
```

**Our recommendation**: Option A for main tables, Option B in appendix tables.

---

## 3. Inter-Annotator Agreement (IAA) Metrics

### Which Metric for Which Annotation Type

| Annotation Type | Data Scale | # Annotators | Recommended Metric | Alternative |
|----------------|------------|-------------|-------------------|-------------|
| Binary labels (correct/incorrect) | Nominal | 2 | Cohen's kappa | Scott's pi |
| Binary labels | Nominal | 3+ | Fleiss' kappa | Krippendorff's alpha |
| Categorical (error types) | Nominal | 2+ | **Krippendorff's alpha** | Fleiss' kappa |
| Ordinal ratings (MQM severity) | Ordinal | 2+ | **Krippendorff's alpha (ordinal)** | Weighted kappa |
| Continuous scores | Interval/Ratio | 2+ | **ICC** (two-way, agreement) | Krippendorff's alpha (interval) |
| Rankings | Ordinal | 2+ | Kendall's W | Spearman correlation |
| Mixed missing data | Any | Any | **Krippendorff's alpha** | -- |

### Why Krippendorff's Alpha is Usually Best for ACL Papers

1. Handles **any number of annotators** (not just 2 like Cohen's kappa)
2. Handles **missing data** (annotators don't need to label every item)
3. Works with **any measurement scale** (nominal, ordinal, interval, ratio)
4. **Chance-corrected** (unlike raw agreement)
5. Most widely recognized in ACL/EMNLP community

### When to Use ICC Instead

Use **ICC (Intraclass Correlation Coefficient)** when:
- Scores are continuous (e.g., mean MQM scores across dimensions)
- You care about absolute agreement, not just ranking
- You want to assess both consistency AND absolute agreement

**ICC variants:**
- ICC(2,1): Two-way random, single measures, absolute agreement -- **use this for human judges**
- ICC(2,k): Two-way random, average measures -- use when reporting average of k judges
- ICC(3,1): Two-way mixed -- use when judges are fixed (specific models as judges)

### Acceptable Values for ACL Papers

| Metric | Poor | Fair | Moderate | Good | Excellent |
|--------|------|------|----------|------|-----------|
| Krippendorff's alpha | < 0.40 | 0.40-0.60 | 0.60-0.67 | 0.667-0.80 | > 0.80 |
| Cohen's/Fleiss' kappa | < 0.20 | 0.21-0.40 | 0.41-0.60 | 0.61-0.80 | > 0.80 |
| ICC | < 0.50 | 0.50-0.75 | 0.75-0.90 | -- | > 0.90 |

**Critical threshold**: Krippendorff recommends alpha >= 0.667 for tentative conclusions,
alpha >= 0.80 for reliable conclusions. Most ACL papers report alpha >= 0.60 and discuss
limitations if lower.

**For our MQM annotations**: Report Krippendorff's alpha (ordinal) for severity ratings,
Krippendorff's alpha (nominal) for error type categories, and ICC(2,1) for overall
MQM composite scores.

---

## 4. Table Design for Best Papers

### Column Count Guidelines

| Paper Type | Max Columns (Main Table) | Strategy for More |
|-----------|-------------------------|-------------------|
| Model comparison | 8-10 | Split into subtables or use appendix |
| Ablation study | 6-8 | Group related ablations |
| Multi-metric | 5-7 per metric group | Use separate tables per metric group |
| Cross-lingual | 8-12 (languages as columns) | Group language families |

**Rule of thumb**: If your table doesn't fit in one column of ACL format, either
reduce columns or use a full-width table. More than 12 data columns almost always
needs restructuring.

### Bold and Underline Conventions (ACL Standard)

The de facto standard in ACL/EMNLP 2024-2025:

- **Bold**: Best result in each column/row (absolute winner)
- **Underline**: Second-best result
- State the convention explicitly in table caption or footnote

```latex
% In preamble
\newcommand{\first}[1]{\textbf{#1}}
\newcommand{\second}[1]{\underline{#1}}

% In table
GPT-4o & \first{82.3} & \second{79.1} & 76.4 \\
Claude & \second{81.7} & \first{80.2} & \first{78.9} \\
```

**Caption text**: "Best results per column in **bold**, second-best \underline{underlined}."

### Statistical Significance Markers

**Standard ACL convention:**

| Symbol | Meaning | Usage |
|--------|---------|-------|
| * | p < 0.05 | Significant vs. baseline |
| ** | p < 0.01 | Highly significant vs. baseline |
| *** | p < 0.001 | Very highly significant |
| dagger (†) | p < 0.05 | Significant vs. second comparison system |
| double-dagger (‡) | p < 0.01 | Highly significant vs. second comparison |

```latex
% Use with siunitx or manual
GPT-4o & 82.3$^{**}$ & 79.1$^{*}$ \\
Claude & 81.7$^{**}$ & 80.2$^{***}$ \\
```

**Footnote**: "Statistical significance vs. best baseline (paired bootstrap,
B=10000): * p<0.05, ** p<0.01, *** p<0.001."

### When to Use Heatmap Coloring vs. Plain Numbers

**Use heatmaps when:**
- Large tables (>= 8x8) where patterns are hard to see from numbers alone
- Showing correlation matrices or confusion matrices
- Comparing across many conditions (our adversarial transforms matrix)
- The relative magnitude matters more than exact values

**Use plain numbers when:**
- Small tables where exact values matter
- Main results tables (bold/underline suffices)
- Differences are small and color would exaggerate

**Hybrid approach (recommended for our paper):**
- Main results: plain numbers with bold/underline
- Adversarial transform heatmap: colored cells with numbers inside
- Error analysis: plain with significance markers

```latex
% Heatmap coloring with pgfplotstable or xcolor
\usepackage{colortbl}
\newcommand{\cellcolor}[1]{%
  \ifdim #1pt > 80pt \cellcolor{green!30}%
  \else\ifdim #1pt > 60pt \cellcolor{yellow!20}%
  \else \cellcolor{red!20}%
  \fi\fi
  #1}
```

### ACL 2024-2025 Best Paper Table Patterns Observed

Analysis of ACL 2024 best paper winners (MAGE, Aya, Mission Impossible, etc.) reveals:

1. **booktabs package universally used** -- `\toprule`, `\midrule`, `\bottomrule` (never `\hline`)
2. **No vertical lines** -- clean horizontal rules only
3. **Bold for best, underline for second-best** -- stated in caption
4. **Compact captions** -- describe what the table shows + conventions in 1-2 sentences
5. **Grouped columns with `\cmidrule`** -- e.g., grouping metrics or conditions
6. **Right-aligned numbers** -- use `S` column type from `siunitx` or `r`
7. **Consistent decimal places** -- typically 1 decimal for percentages, 2 for correlations
8. **Metric names abbreviated in headers** -- full names in caption or text
9. **Row grouping** -- separate model families with `\midrule` or `\cmidrule`
10. **Footnotes for significance** -- not inline explanations

---

## 5. What Reviewers Specifically Complain About

### From ARR Reviewer Guidelines (Official Codes)

**R1 - Data Presentation Issues:**
- p-hacking (running many tests, reporting only significant ones)
- Presenting "best" results from unknown number of trials
- Misleading statistics or cherry-picked metrics
- Not specifying whether results are mean, max, or single run

**R2 - Scope Overclaiming:**
- Claiming general understanding from narrow benchmarks
- "A few QA benchmarks != 'reasoning' or 'understanding'"

**M4 - Unmotivated Selection:**
- Model and benchmark choices must be "directly linked to the scope of claimed contributions"
- Reviewers flag when baselines seem chosen to make proposed method look good

### Top Reviewer Complaints (Empirical, from Meta-Reviews and Community Discussions)

1. **Missing baselines / unfair comparisons**
   - Not comparing against obvious SOTA
   - Using outdated baselines when newer ones exist
   - Comparing fine-tuned model against zero-shot
   - Different prompt templates for different models
   
   **Fix**: Include at least one strong open-source baseline and one proprietary SOTA.
   Use identical prompts/conditions.

2. **No error bars or confidence intervals**
   - Single-run results with no variance indication
   - Especially problematic for small test sets
   
   **Fix**: Report mean +/- std over 3-5 seeds, or bootstrap CIs.

3. **Too many metrics without clear takeaway**
   - Tables with 10+ metrics where reader can't determine winner
   - No primary metric identified
   
   **Fix**: Designate one primary metric, report others as secondary.
   Use bold/underline to guide the eye.

4. **Cherry-picked metrics**
   - Reporting only metrics where proposed method wins
   - Omitting standard metrics for the task
   
   **Fix**: Report ALL standard metrics. Discuss where method underperforms.

5. **Illegible or overwhelming tables**
   - Too many columns, tiny font, no visual hierarchy
   - Tables that span multiple pages without clear structure
   
   **Fix**: Split into focused subtables. Use appendix for full results.

6. **Missing ablations**
   - No evidence of which components contribute
   
   **Fix**: Include ablation table showing contribution of each component.

7. **Inconsistent formatting**
   - Different decimal places across tables
   - Inconsistent bold/underline conventions
   
   **Fix**: Use consistent formatting throughout. Define conventions once.

### What Reviewers Should NOT Demand (Per ARR H-codes)

- **H13**: Reviewers should not demand extra experiments beyond the paper's claims
- **H14**: Comparing to closed-source models only justified when directly relevant
- **H5**: Missing SOTA is not a weakness unless paper claims SOTA

---

## 6. Effect Sizes

### When to Use Which Effect Size

| Effect Size | Use Case | Scale | Interpretation |
|------------|----------|-------|----------------|
| Cohen's d | Continuous metrics, two models | Interval/ratio | 0.2 small, 0.5 medium, 0.8 large |
| Hedges' g | Same as Cohen's d, small samples (<30) | Interval/ratio | Same scale, bias-corrected |
| Cliff's delta | Ordinal data (MQM scores) | Ordinal | |delta|<0.147 negligible, <0.33 small, <0.474 medium, >=0.474 large |
| Glass's delta | When variances differ substantially | Interval/ratio | Uses control group SD |
| CLES (Common Language) | Probability one > other | Any | "In X% of cases, model A > model B" |

### For Our MQM Paper Specifically

- **Cliff's delta** for MQM severity comparisons (ordinal data)
- **Cohen's d** for composite MQM scores (treated as continuous)
- **CLES** for intuitive reporting: "GPT-4o produces higher-quality captions than
  Gemini in 73% of figure comparisons"

### Computing Effect Sizes

```python
def cohens_d(group1, group2):
    """Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def cliffs_delta(group1, group2):
    """Cliff's delta for ordinal data."""
    n1, n2 = len(group1), len(group2)
    more = sum(1 for x in group1 for y in group2 if x > y)
    less = sum(1 for x in group1 for y in group2 if x < y)
    return (more - less) / (n1 * n2)

def cles(group1, group2):
    """Common Language Effect Size."""
    n1, n2 = len(group1), len(group2)
    more = sum(1 for x in group1 for y in group2 if x > y)
    ties = sum(1 for x in group1 for y in group2 if x == y)
    return (more + 0.5 * ties) / (n1 * n2)
```

### Meaningful vs. Significant

A result can be:
- **Significant but not meaningful**: p < 0.01, but Cohen's d = 0.1 (tiny effect on 1000+ items)
- **Meaningful but not significant**: Cohen's d = 0.6, but p = 0.08 (underpowered study)
- **Both**: p < 0.01 AND Cohen's d > 0.5 (this is what you want)

**Always report both** statistical significance AND effect size. Dror et al. (2018) emphasizes:
"statistical significance differs from practical significance."

---

## 7. LaTeX Templates for Our Tables

### Main Results Table (11 Models x Metrics)

```latex
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{siunitx}
\sisetup{detect-weight=true, detect-inline-weight=math}

\begin{table*}[t]
\centering
\small
\caption{MQM evaluation of figure captions across 11 models and 4 judge LLMs.
Best results per column in \textbf{bold}, second-best \underline{underlined}.
Statistical significance vs.\ best baseline (paired bootstrap, $B$=10{,}000):
$^{*}$\,\textit{p}<0.05, $^{**}$\,\textit{p}<0.01.}
\label{tab:main-results}
\begin{tabular}{@{}l S[table-format=2.1] @{\,\scriptsize$\pm$\,} S[table-format=1.1]
                    S[table-format=2.1] @{\,\scriptsize$\pm$\,} S[table-format=1.1]
                    S[table-format=2.1] @{\,\scriptsize$\pm$\,} S[table-format=1.1]@{}}
\toprule
\textbf{Model} & \multicolumn{2}{c}{\textbf{Accuracy}} 
               & \multicolumn{2}{c}{\textbf{Fluency}}
               & \multicolumn{2}{c}{\textbf{MQM-Comp}} \\
\cmidrule(lr){2-3} \cmidrule(lr){4-5} \cmidrule(lr){6-7}
GPT-4o         & \bfseries 82.3 & 1.2 & \bfseries 91.2 & 0.8 & \bfseries 78.4 & 1.5 \\
Claude-3.5     & 81.7 & 1.4 & 90.8 & 0.9 & 77.1 & 1.3 \\
Gemini-1.5     & 79.2 & 1.8 & 88.4 & 1.1 & 74.6 & 1.7 \\
\midrule
\multicolumn{7}{l}{\textit{Open-source models}} \\
LLaVA-1.6      & 71.3 & 2.1 & 85.2 & 1.4 & 68.9 & 2.0 \\
\bottomrule
\end{tabular}
\end{table*}
```

### Compact CI Format (Parenthetical)

```latex
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Model} & \textbf{Acc.} & \textbf{95\% CI} & \textbf{$p$-val} & \textbf{$d$} \\
\midrule
GPT-4o   & \textbf{82.3} & (80.8, 83.9) & --      & --   \\
Claude   & \underline{81.7} & (80.1, 83.2) & 0.142   & 0.12 \\
Gemini   & 79.2 & (77.1, 81.4) & 0.003** & 0.41 \\
\bottomrule
\end{tabular}
```

### Adversarial Transforms Heatmap Table

```latex
\usepackage{colortbl}
\usepackage{xcolor}

% Define color gradient
\newcommand{\heatcell}[1]{%
  \ifdim #1 pt > 75pt%
    \cellcolor{green!25}#1%
  \else\ifdim #1 pt > 50pt%
    \cellcolor{yellow!20}#1%
  \else%
    \cellcolor{red!20}#1%
  \fi\fi%
}

\begin{table}[t]
\centering
\small
\caption{Model robustness under adversarial transforms
(MQM composite score). Color intensity indicates performance level.}
\begin{tabular}{@{}lccccc@{}}
\toprule
& \rotatebox{60}{Blur} & \rotatebox{60}{Crop} & \rotatebox{60}{Noise}
& \rotatebox{60}{Rotate} & \rotatebox{60}{Occlude} \\
\midrule
GPT-4o   & \heatcell{78.2} & \heatcell{72.1} & \heatcell{65.3} & \heatcell{80.1} & \heatcell{45.2} \\
Claude   & \heatcell{76.9} & \heatcell{74.5} & \heatcell{68.1} & \heatcell{79.3} & \heatcell{48.7} \\
\bottomrule
\end{tabular}
\end{table}
```

### IAA Reporting Table

```latex
\begin{table}[t]
\centering
\small
\caption{Inter-annotator agreement for MQM annotations.}
\begin{tabular}{@{}llcc@{}}
\toprule
\textbf{Dimension} & \textbf{Scale} & \textbf{Kripp.\ $\alpha$} & \textbf{ICC(2,1)} \\
\midrule
Error type     & Nominal & 0.72 & --   \\
Severity       & Ordinal & 0.68 & 0.71 \\
Overall MQM    & Interval & 0.74 & 0.78 \\
\midrule
\multicolumn{2}{l}{\textit{Judge agreement (LLM vs.\ human)}} \\
GPT-4o judge   & Interval & 0.65 & 0.69 \\
Claude judge   & Interval & 0.63 & 0.67 \\
\bottomrule
\end{tabular}
\end{table}
```

---

## 8. Comprehensive Checklist Before Submission

### Table Quality Checklist

- [ ] Uses `booktabs` (no `\hline`, no vertical rules)
- [ ] Bold = best, underline = second-best (stated in caption)
- [ ] Significance markers defined in caption footnote
- [ ] All numbers have consistent decimal places
- [ ] Mean +/- std OR 95% CI reported for main results
- [ ] Statistical test named (paired bootstrap, B=10000)
- [ ] Multiple comparisons correction applied (Holm-Bonferroni)
- [ ] Effect sizes reported (Cohen's d or Cliff's delta)
- [ ] IAA reported with appropriate metric (Krippendorff's alpha)
- [ ] Primary metric clearly identified
- [ ] Strong baselines included (both open and proprietary)
- [ ] Same evaluation conditions for all models
- [ ] Table fits in column width (or justified full-width)
- [ ] Readable font size (no smaller than `\small`)

### Statistical Reporting Checklist

- [ ] Number of bootstrap resamples stated (B=10,000)
- [ ] Confidence level stated (95%)
- [ ] Whether mean/median/max is reported
- [ ] Number of random seeds stated
- [ ] p-values: exact when > 0.001, "< 0.001" otherwise
- [ ] Effect sizes alongside p-values
- [ ] Practical significance discussed in text (not just statistical)
- [ ] Multiple comparisons correction method named

### Responsble NLP Checklist Items (ARR-Required)

- [ ] C1: Computational budget (GPU hours, parameters)
- [ ] C2: Hyperparameter search described
- [ ] C3: Error bars / CIs present; aggregation method stated
- [ ] C4: Package versions cited (evaluation tools)

---

## 9. Quick Reference Card

### For Each Table in the Paper

| Element | Format | Example |
|---------|--------|---------|
| Best result | `\textbf{82.3}` | **82.3** |
| Second best | `\underline{81.7}` | 81.7 (underlined) |
| With CI | `82.3 $\pm$ 1.2` | 82.3 +/- 1.2 |
| Significant | `82.3$^{**}$` | 82.3** |
| Sig + CI | `82.3$^{**}$ $\pm$ 1.2` | 82.3** +/- 1.2 |
| Not significant | `79.2` | 79.2 (no marker) |
| Effect size | `($d$=0.41)` | (d=0.41) |

### p-value Reporting

- p = 0.142 -> report as "0.142" (exact, not significant)
- p = 0.031 -> report as "0.031*"
- p = 0.004 -> report as "0.004**"
- p = 0.0002 -> report as "<0.001***"

### Multiple Comparisons (Holm-Bonferroni)

For k = 10 pairwise comparisons (11 models, vs. best):
1. Sort p-values ascending
2. Compare p_i against alpha / (k - i + 1)
3. Reject until first non-rejection, then stop

```python
from statsmodels.stats.multitest import multipletests

rejected, corrected_p, _, _ = multipletests(p_values, method='holm')
```

---

## 10. Key References to Cite

When justifying our statistical methodology in the paper:

1. **Dror, R., Baumer, G., Shlomov, S., & Reichart, R.** (2018). The Hitchhiker's Guide
   to Testing Statistical Significance in Natural Language Processing. ACL 2018.
   `\cite{dror-etal-2018-hitchhikers}` -- For test selection protocol.

2. **Dror, R. & Reichart, R.** (2018). Recommended Statistical Significance Tests for NLP
   Tasks. arXiv:1809.01448. -- Appendix with task-specific test recommendations.

3. **Berg-Kirkpatrick, T., Burkett, D., & Klein, D.** (2012). An Empirical Investigation
   of Statistical Significance in NLP. EMNLP 2012. -- For bootstrap methodology.

4. **Krippendorff, K.** (2011). Computing Krippendorff's Alpha-Reliability.
   -- For IAA methodology justification.

5. **Koehn, P.** (2004). Statistical Significance Tests for Machine Translation Evaluation.
   EMNLP 2004. -- For paired bootstrap in evaluation contexts.

---

## Summary of Actionable Decisions for Our Paper

1. **Bootstrap**: 10,000 resamples, BCa method, paired (same test figures)
2. **IAA**: Krippendorff's alpha (ordinal) for MQM severity, ICC(2,1) for composite scores
3. **Effect size**: Cliff's delta for ordinal MQM, Cohen's d for continuous
4. **Correction**: Holm-Bonferroni for all pairwise model comparisons
5. **Tables**: booktabs, bold/underline, mean +/- std, significance markers in superscript
6. **Report**: Exact p-values, effect sizes, state test name and parameters in caption
7. **Max columns**: 8-10 in main table, overflow to appendix
8. **Heatmaps**: Use for adversarial transform matrix, plain for main results
