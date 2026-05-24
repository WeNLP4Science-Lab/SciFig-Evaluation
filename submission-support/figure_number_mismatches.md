# Figure Number Mismatches

Comparison of groundtruth figure numbers against Opus 4.6 and Sonnet 4.6 readings from in-paper page images. 100 figures checked from sampled_100 (seed=42).

**Total mismatches: 36 / 100**

---

## 1. Agents Agree, Disagree with Groundtruth (5)

Both Opus and Sonnet identify the same figure number, which differs from our groundtruth. **These need fixing.**

| Figure | Groundtruth | Opus | Sonnet | Action |
|---|---|---|---|---|
| fig_048 | Figure 7 | Figure 6 | Figure 5 | Verify and fix |
| fig_098 | Figure 4 | Figure 5 | Figure 5 | Fix to Figure 5 |
| fig_195 | Figure 13 | Figure 10 | Figure 10 | Fix to Figure 10 |
| fig_196 | Figure 4 | Figure 3 | Figure 3 | Fix to Figure 3 |
| fig_197 | Figure 7 | Figure 5 | Figure 5 | Fix to Figure 5 |

---

## 2. Agents Disagree with Each Other (11)

Opus and Sonnet give different figure numbers. **Need manual verification.**

| Figure | Groundtruth | Opus | Sonnet | Notes |
|---|---|---|---|---|
| fig_038 | Figure 8 | Figure 8 | Figure 7 | Sonnet disagrees with GT+Opus |
| fig_042 | Figure 7 | Figure 7 | Figure 4 | Sonnet disagrees with GT+Opus |
| fig_043 | Figure 4 | Figure 4 | Figure 6 | Sonnet disagrees with GT+Opus |
| fig_045 | Figure 6 | Figure 6 | Figure 2 | Sonnet disagrees with GT+Opus |
| fig_046 | Figure 2 | Figure 2 | Figure 6 | Sonnet disagrees with GT+Opus |
| fig_050 | Figure 5 | Figure 5 | Figure 2 | Sonnet disagrees with GT+Opus |
| fig_051 | Figure 2 | Figure 2 | Figure 1 | Sonnet disagrees with GT+Opus |
| fig_080 | Figure 5 | Figure 4 | Figure 4 and Figure 5 | Opus disagrees, Sonnet ambiguous |
| fig_091 | Figure 1 | Figure 1 | Figure 2 | Sonnet disagrees with GT+Opus |
| fig_101 | Figure 5 | Figure 3 | Figure 5 (panel a) | Opus disagrees with GT+Sonnet |
| fig_217 | Figure 3 | Figure 5 | Figure 3 | Opus disagrees with GT+Sonnet |

---

## 3. Sub-panel Labels Missing or Different in Groundtruth (12)

Agents identify the parent figure number but GT has (or lacks) a sub-panel label. Not wrong, just different granularity.

| Figure | Groundtruth | Opus | Sonnet | Notes |
|---|---|---|---|---|
| fig_011 | Figure 6 | Figure 6 | Figure 6 | Opus notes it's 6(a), GT just says 6 |
| fig_109 | Figure 8 | Figure 8 | Figure 8 (panel a) | Sonnet adds panel detail |
| fig_112 | Figure 5 | Figure 3 | Figure 5 (panel a) | Opus wrong, Sonnet adds panel |
| fig_113 | Figure 5 | Figure 3 | Figure 5 (panel b) | Opus wrong, Sonnet adds panel |
| fig_123 | Figure 1 (right) | Figure 1 | Figure 1 | GT has extra position detail |
| fig_124 | Figure 8b | Figure 8 | Figure 8 | GT has sub-label, agents give parent |
| fig_126 | Figure 4 (right) | Figure 4 | Figure 4 | GT has extra position detail |
| fig_136 | Figure 16b | Figure 16 | Figure 16 | GT has sub-label, agents give parent |
| fig_137 | Figure 6 (row 1; left) | Figure 6 | Figure 6 | GT has position detail |
| fig_138 | Figure 16c | Figure 16 | Figure 16 | GT has sub-label, agents give parent |
| fig_139 | Figure 3d | Figure 3 | Figure 3 | GT has sub-label, agents give parent |
| fig_233 | Figure 6 | Figure 5 | Figure 6 | Opus disagrees, Sonnet matches GT |

---

## 4. Other Mismatches (8)

| Figure | Groundtruth | Opus | Sonnet | Notes |
|---|---|---|---|---|
| fig_002 | Figure 5 | N/A (no in-paper image) | Figure 5 | No in-paper image available |
| fig_053 | Figure 3 | N/A (no in-paper image) | N/A | No in-paper image available |
| fig_061 | Figure 5 | No explicit figure number | No explicit figure number | Appendix chart with no figure label |
| fig_090 | Figure 3 | Figure 3 | Figure 2 and Figure 3 | Sonnet sees multiple, Opus matches GT |
| fig_094 | Figure 7 | Figure 7 | Figure 6 and Figure 7 | Sonnet sees multiple, Opus matches GT |
| fig_104 | Figure 8 | Figure 7/8/9 | Figure 7 | Multi-figure page, agents differ |
| fig_105 | Figure 7 | Figure 7/8 | Figure 7 (left panel) | Opus ambiguous, Sonnet matches |
| fig_122 | Figure 3 | Figure 5 | Figure 3 | Opus disagrees, Sonnet matches GT |
| fig_223 | Figure 8 | Figure 5 | Figure 8 | Opus disagrees, Sonnet matches GT |

---

## Summary

| Category | Count | Action |
|---|---|---|
| Agents agree, GT wrong | 5 | Fix groundtruth |
| Agents disagree | 11 | Manual verification needed |
| Sub-panel label differences | 12 | Optional: add sub-labels to GT |
| Other | 8 | Case-by-case review |
| **Total mismatches** | **36** | |
| **Figures correct** | **64** | No action needed |
