# German Prompt vs English Prompt Comparison (GPT-5.2)

Comparison of C1 (German prompt, German output) vs C2' (English prompt, German output) for all 9 German figures with descriptions in both conditions.

## Per-Figure Comparisons

---

### german_fig_001 -- Line Plot (Policy Indices 2016-2024)

**Figure**: Three-line time series showing Wirtschaftspolitik insgesamt, Finanzpolitik (left axis, 0-1000), and Handelspolitik (right axis, 0-9000) from 2016 to ~2025.

| Dimension | C1 (German prompt) | C2' (English prompt) | Verdict |
|-----------|-------------------|---------------------|---------|
| Accuracy | x-axis described as 2016-2024; detailed numerical ranges for all three lines accurate. End-of-series spike values correct (~700 for black/blue, ~8000-8500 for purple). | x-axis described as 2016-2025 (more accurate -- data visibly extends past 2024). End values: ~700 for black, ~650-700 for blue, ~8500-9000 for purple. The 8500-9000 range for Handelspolitik is slightly more accurate than C1's 8000-8500. | C2' slightly better |
| Completeness | Describes all three lines with detailed trajectory. Mentions dual y-axes, tick intervals, colors, line styles. | Same coverage. Slightly more concise but captures the same elements. Explicitly notes "ohne Marker" (no markers). | Equivalent |
| Clarity | Very detailed, reads like a continuous paragraph. Dense but thorough. | Slightly better organized with clearer separation of line descriptions. | C2' slightly better |

**Winner: C2' (slight edge)**

---

### german_fig_002 -- Combo Chart (Imports/Exports + Trade Balance)

**Figure**: Blue line (Importe), purple line (Exporte) on left axis, light blue bars (Saldo) on right axis, 2020-2023.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Import start ~200, dip to ~165, peak ~290, end ~340. Export start ~135, dip ~90, peak ~180. Saldo range -50 to -180. All accurate. Right y-axis -200 to 400 -- correct. | Very similar values. Import end ~345 (C1: ~340 -- both reasonable). Saldo initial values -20 to -60 (C1: -50 to -80). Looking at the image, C2's initial saldo values may be slightly more accurate. | Equivalent |
| Completeness | Detailed trajectory descriptions for both lines and bars. Notes all axis scales and labels. | Slightly more concise but covers the same structural elements. | Equivalent |
| Clarity | Long single paragraph, dense. | Better structured with clearer separation of data series. | C2' slightly better |

**Winner: C2' (marginal)**

---

### german_fig_022 -- Grouped Bar Chart (Economic Indicators by Decade)

**Figure**: Four grouped bars per decade (2000er, 2010er, 2020er) showing Welt-BIP, Welthandel, Exporte Deutschland, Industrieproduktion Deutschland. Values labeled on bars.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | All numerical values correct (3.9, 5.4, 5.3, 1.0 / 3.7, 4.8, 5.0, 2.2 / 2.7, 2.3, 0.4, -1.5). Colors correctly identified. | Identical numerical values. Same color descriptions. | Equivalent |
| Completeness | Notes scale range, negative bar, color coding, bar order, data labels. | Same coverage. Additionally notes "nicht gestapelt" (not stacked) which is a useful clarification. Notes label placement for negative bar. | C2' slightly better |
| Clarity | Well structured. | Very well structured. Opens by identifying chart type as "gruppiertes Balkendiagramm" (grouped bar chart) which is more precise than C1's "Balkendiagramm". | C2' slightly better |

**Winner: C2' (slight edge)**

---

### german_fig_023 -- Stacked Bar Charts (Government Expenditure % of GDP, 1991-2023)

**Figure**: Two side-by-side stacked bar charts showing Bund/Laender/Gemeinden as % of GDP with a total line and Bahnreform annotation.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Left chart: total 3.0+ at start, 2.2-2.6 in 2000s, back to ~3.0 -- accurate. Right chart: total curve 0.7-0.8 initially, near 0 in 2000s, spike ~0.5 in 2020s -- accurate. Segment ranges reasonable. | Left chart: total 3.2-3.3 at start, 2.2-2.4 mid-2000s -- more precise. Individual segments: Bund 0.5-1.0, Laender 0.6-0.9, Gemeinden 0.7-1.7. Right chart: Bund -0.1 to 0.2, Laender 0.1-0.3, Gemeinden up to 0.6-0.7 early, total -0.2 to 0.8 -- more granular and accurate. | C2' better |
| Completeness | Describes both sub-charts, Bahnreform annotation, stacking order. Mentions year labeling style (schraeg/slanted). | Same coverage, combines description into single flowing paragraph. Mentions stacking order, Bahnreform, year labels. | Equivalent |
| Clarity | Clearly separated into left and right chart descriptions. | Single long paragraph but still readable. | C1 slightly better |

**Winner: C2' (accuracy edge outweighs clarity)**

---

### german_fig_033 -- Line Plot (Employment Rate by Migration Background)

**Figure**: Four lines (ohne Migrationshintergrund, in Deutschland geboren, zugewandert bis 2009, zugewandert seit 2010) showing employment rate vs age (20-70).

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Black line: ~60% at 20, peaks ~90%, drops to few % at 70. Gray: ~53% at 20, drops similarly. Light blue: ~35% at 20, spike to ~upper 70% at 22. Dark blue: ~40% at 20, dip to under 40% mid-50s, 0% late 60s. All match the image well. | Black: ~60% at 20, 80-85% late 20s, 85-88% plateau, single digits at 70. Gray: ~55% at 20, 70-85% range. Light blue: ~35% at 20, spike to ~75% at 22, 60-75% range. Dark blue: ~38-40% at 20, trough ~38% at 53, high ~70% at 58. More precise trough/peak locations. | C2' slightly better |
| Completeness | Covers all 4 lines with trajectories. Notes markers (Punktmarkierungen). | Same coverage. Notes "runde Marker" (round markers) -- more specific. | C2' slightly better |
| Clarity | Four numbered descriptions, well organized. | Four named descriptions, well organized. | Equivalent |

**Winner: C2' (slight edge)**

---

### german_fig_042 -- Horizontal Stacked Bar Chart (Defense Spending % GDP by EU Country)

**Figure**: 21 EU countries with horizontal stacked bars (blue = increase 2021-2024, green = spending 2021), plus reference markers.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Lists all 21 countries in correct order. Provides detailed segment values for top countries. Correctly identifies colors and legend labels. **BUT the description is truncated** -- cuts off mid-sentence at "Niederlande ca. 1,35 + 0," missing the bottom 7-8 countries. | Lists fewer specific values but covers the full range (Poland to Spain). Correctly identifies stacking order, colors, reference markers. Provides example values for Poland (~2.2+1.9), Estland (~2.0+1.5), Luxembourg (~0.5+0.8), Spain (~1.0+0.2-0.3). | C2' better |
| Completeness | Truncated -- incomplete output. Missing ~40% of countries. | Complete description covering full chart. Mentions reference markers with explanation. | C2' clearly better |
| Clarity | Would have been good if complete. | Well structured, uses examples rather than exhaustive listing. | C2' better |

**Winner: C2' (C1 truncated)**

---

### german_fig_051 -- Dual Line Plot (IMF Fiscal Index + Debt Ratios)

**Figure**: Two side-by-side plots: left shows IMF Fiskalindex (0-2.5) + Schuldenquote Gesamtstaat (60-120), right shows IMF Fiskalindex (-0.5-2.0) + Schuldenquote Zentralstaat (30-70). Each has blue and purple lines plus triangle markers.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Left plot well described. Right plot **also truncated** -- cuts off at "2010 einen sprunghaften Anstieg bis etwa 1,0" without completing. | Both plots fully described with detailed numerical values. Left plot: blue line trajectory accurate. Triangle markers described with step-wise values. Right plot: complete description including both lines and both sets of triangles. | C2' better |
| Completeness | Left plot complete; right plot truncated (missing ~50% of right panel description). | Both panels fully covered including all 4 data series per panel. | C2' clearly better |
| Clarity | Structured as separate paragraphs per panel. Good when not truncated. | Single flowing description, well organized by panel. | Equivalent |

**Winner: C2' (C1 truncated)**

---

### german_fig_057 -- Donut/Ring Chart (Municipal Enterprise Shares 2014 vs 2021)

**Figure**: Double-ring donut chart with inner ring (2014) and outer ring (2021) showing 14 categories of municipal enterprise types.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | Correctly identifies 14 segments. All percentage values accurate for both rings (e.g., Uebrige 38.1%/31.1%, Wasserversorgung 8.8%/11.8%). Colors mostly correct. Correctly says inner=2014, outer=2021. | Says "13 Kategorien" -- actually there are 14 (it separately mentions Gasversorgung as an additional one, so effectively 14 but the count is stated as 13). All percentage values accurate. Inner/outer year assignment correct. | C1 slightly better |
| Completeness | Lists all 14 categories with both 2014 and 2021 values in order. Notes clockwise arrangement starting from Kultur. | Lists categories but in less systematic order. Describes outer ring first, then inner ring. Covers all values. | C1 slightly better |
| Clarity | Well organized: outer ring then inner ring, each with full enumeration. Notes placement of labels. | Adequate but slightly less systematic. The count error (13 vs 14) is confusing. | C1 better |

**Winner: C1 (more accurate count, better organization)**

---

### german_fig_070 -- Grouped Bar Chart (Metal Import Shares DE vs EU)

**Figure**: Two side-by-side grouped bar charts (Deutschland, EU) showing % for Aluminium, Kupfer, Nickel across 2021-2023. All values labeled.

| Dimension | C1 | C2' | Verdict |
|-----------|-----|------|---------|
| Accuracy | All 18 values correct (DE: 3.6, 2.7, 1.0 / 8.3, 11.3, 2.2 / 25.1, 24.7, 11.4; EU: 3.2, 2.8, 1.7 / 4.4, 5.1, 1.3 / 24.3, 23.3, 14.6). Colors: blue, violet, light gray -- correct. | Identical values, all 18 correct. Same color descriptions. | Equivalent |
| Completeness | Describes both charts separately, each with full detail. Notes axis ranges, tick intervals, lack of sorting/highlighting. | Describes both charts together more efficiently. Notes same structural features. Additionally identifies chart as having two sub-panels upfront. | Equivalent |
| Clarity | Split into two paragraphs, one per chart. Systematic. | Single integrated description. More concise but equally clear. | C2' slightly better |

**Winner: C2' (marginal, better conciseness)**

---

## Summary Statistics

| Figure | Winner | Margin |
|--------|--------|--------|
| german_fig_001 | C2' | Slight |
| german_fig_002 | C2' | Marginal |
| german_fig_022 | C2' | Slight |
| german_fig_023 | C2' | Slight |
| german_fig_033 | C2' | Slight |
| german_fig_042 | C2' | Clear (C1 truncated) |
| german_fig_051 | C2' | Clear (C1 truncated) |
| german_fig_057 | C1 | Moderate |
| german_fig_070 | C2' | Marginal |

### Tally

- **C2' wins: 8 / 9** (89%)
- **C1 wins: 1 / 9** (11%)
- **Equivalent: 0 / 9**

### By margin (excluding truncation issues):
- C2' clear wins: 0 (the 2 "clear" wins are due to C1 truncation, not inherent quality)
- C2' slight/marginal wins: 6
- C1 moderate win: 1

## Key Patterns

### 1. Truncation Problem in C1
Two of the nine C1 descriptions (german_fig_042 and german_fig_051) are truncated mid-sentence. This is a significant data quality issue that may reflect a token-limit or output-handling problem specific to the German-prompt condition. The C2' condition produced complete outputs for the same figures. This alone accounts for 2 of the 8 C2' wins.

### 2. Structural Precision
C2' descriptions tend to open with a more precise chart-type identification (e.g., "gruppiertes Balkendiagramm" instead of just "Balkendiagramm"). This is a minor but consistent pattern suggesting the English instruction may encourage more systematic description structure.

### 3. Numerical Accuracy
When both descriptions are complete, numerical accuracy is nearly identical. Both conditions extract the same data values from labeled charts. For unlabeled values (estimated from visual position), C2' sometimes provides slightly tighter ranges (e.g., fig_001 Handelspolitik endpoint: C1 says 8000-8500, C2' says 8500-9000; the image suggests values closer to C2').

### 4. Conciseness vs Exhaustiveness
C1 descriptions tend to be more exhaustive (e.g., listing all 21 countries with individual values in fig_042), while C2' descriptions use a sampling strategy (listing a few representative examples). When the exhaustive approach works (fig_057), C1 is better. When it leads to truncation (fig_042), C2' wins by default.

### 5. German Language Quality
Both conditions produce fluent, natural German. There is no detectable "translationese" or awkwardness in C2' despite the English prompt. Technical vocabulary (Balkendiagramm, gestapelt, Tickmarken, etc.) is used correctly in both. The English instruction does not degrade German language quality.

### 6. Category Counting
C2' made one counting error (13 vs 14 categories in fig_057). C1 was correct. This is the only clear accuracy advantage for C1 across all figures.

## Conclusion

**English instruction does not degrade description quality for German figures.** In fact, C2' performs slightly better on average due to:
- More concise, better-organized descriptions
- No truncation issues (C1 had 2/9 truncated outputs)
- Marginally more precise visual estimates in some cases

The single C1 advantage (category count accuracy in fig_057) is outweighed by C2's consistency. However, when excluding the truncation artifacts, the quality difference between conditions is **small** -- most wins are marginal or slight. The truncation issue in C1 should be investigated as a potential pipeline bug rather than attributed to prompt language.

**Bottom line**: For GPT-5.2 on German scientific figures, prompting in English with a German output instruction produces descriptions that are at least as good as, and often marginally better than, prompting natively in German.
