# Bulgarian C1 vs C2' Comparison: GPT-5.2 Descriptions

**Evaluator**: Independent manual assessment (no judge scores used)  
**C1**: Bulgarian prompt -> Bulgarian output  
**C2'**: English prompt (with instruction to respond in Bulgarian) -> Bulgarian output  
**Model**: GPT-5.2, original (untransformed) figures  
**Figures evaluated**: 9 (all available in both directories)

---

## Per-Figure Comparison

| Figure | Type | Winner | Rationale |
|--------|------|--------|-----------|
| bulgarian_fig_001 | Line Plot | **Tie (slight C1 edge)** | Both report identical numerical values for all 3 series across 11 years. C1 adds slightly more trend narrative (identifies local maximum at 2014, lowest at 2022 for the administrative line). C2' is equally accurate but marginally less detailed in trend commentary. |
| bulgarian_fig_014 | Bar Chart | **C2' wins** | C2' provides approximate bar-height values for all 12 months across all 3 years (36 values total). C1 only samples a handful of representative values ("approximately 80-81,000 at VIII", "approximately 128,000 at XII"). Against the image, C2's values are reasonably accurate. Substantial completeness advantage for C2'. |
| bulgarian_fig_021 | Horizontal Bar | **Tie** | Both list the same 13 categories, same percentage values for labeled bars (2%, 3%, 5%, 9%, 10%, 13%), same color coding (blue/red). Both correctly note the longest red bars lack visible percentage labels. C2' maps colors to specific categories slightly more explicitly, but the difference is marginal. |
| bulgarian_fig_036 | Line Plot (dual panel) | **Tie** | Both describe panels A and B with essentially identical numerical approximations (278, 266, 271, 240, ~197 for panel A; 1.5%, 0.85%, 0.75%, 1.3%, 2.3% for panel B). Same structural details about axes, markers, line color. Both misread the Y-axis label identically ("летгодни" vs what appears in the image as "леплодни"). |
| bulgarian_fig_038 | Donut Charts | **C1 wins (slight)** | Both correctly report all sector percentages and absolute values for all 3 donut charts. Key difference: C1 preserves the original English titles from the image ("Number of enterprises", "Number of persons employed", "Turnover"), while C2' translates these into Bulgarian. Since the image actually uses English titles, C1 is more faithful to the source. |
| bulgarian_fig_048 | Grouped Bar | **Tie** | Both describe the same 7 countries, same year range (2013-2022), same axis structure, same approximate value ranges per country. Nearly interchangeable descriptions with no meaningful accuracy or completeness difference. |
| bulgarian_fig_095 | Pie Chart | **Tie (slight C2' edge)** | Both identify 5 categories with identical counts (10, 24, 25, 8, 20) and computed percentages (~11%, 28%, 29%, 9%, 23%). Same color assignments. C2' adds a brief visual-size ranking observation ("Visually the largest segments are green and orange, followed by purple, blue, and red") which is a minor completeness gain. |
| bulgarian_fig_103 | Line Plot | **Tie** | Both describe 4 economic sectors with same approximate value ranges, same trajectory descriptions, and both note x-axis labels are unreadable. C2' gives marginally more specific trajectory details for the yellow (trade) line, but the difference is negligible. |
| bulgarian_fig_272 | Pie Chart | **Tie** | Both identify 4 sectors with identical percentages (3%, 23%, 51%, 23%), same full-text category labels, same color assignments, same observations about legend placement and no exploded sectors. Essentially equivalent. |

---

## Summary Statistics

| Outcome | Count | Figures |
|---------|-------|---------|
| **C1 wins** | 1 | fig_038 |
| **C2' wins** | 1 | fig_014 |
| **Tie** | 7 | fig_001, fig_021, fig_036, fig_048, fig_095, fig_103, fig_272 |

- C1 wins: 1/9 (11%)
- C2' wins: 1/9 (11%)
- Ties: 7/9 (78%)

---

## Key Patterns Observed

### 1. Numerical accuracy is equivalent
Both conditions produce descriptions with the same numerical values. Where figures have explicit data labels (fig_001's line values, fig_095's counts, fig_272's percentages), both C1 and C2' extract them identically. Where values must be estimated from bar heights or line positions (fig_014, fig_048), both give very similar approximations.

### 2. Structural descriptions are equivalent
Both conditions correctly identify chart type, axis labels, legend contents, color assignments, number of series/categories, and scale ranges. No systematic structural errors in either condition.

### 3. Completeness is mostly equivalent with isolated exceptions
The one clear C2' advantage was fig_014, where C2' exhaustively listed approximate values for all 36 bar-month-year combinations while C1 sampled only a few. This appears to be an instance of C2' being more systematic rather than a language-instruction effect, since both conditions produce exhaustive value listings in other figures (e.g., fig_001).

### 4. Label fidelity differs slightly
C1 (Bulgarian prompt) tends to preserve original image labels as-is, including when they are in English (fig_038). C2' (English prompt, Bulgarian output) tends to translate image labels into Bulgarian. This means C1 is slightly more faithful to source images that contain English text, while C2' may be slightly more readable for a Bulgarian audience.

### 5. Trend commentary shows minor variation
C1 occasionally provides marginally richer trend narrative (e.g., fig_001 identifying local maxima/minima). C2' occasionally adds brief visual-ordering observations (e.g., fig_095). These differences are minor and not systematic.

---

## Conclusion: Does the English Instruction Degrade Quality?

**No.** The English instruction (C2') does not produce measurably degraded descriptions compared to the Bulgarian instruction (C1). Across 9 figures:

- **Accuracy**: No systematic accuracy differences. Both conditions extract the same numerical values, identify the same chart elements, and make the same (correct or incorrect) readings of axis labels.
- **Completeness**: One isolated case favored C2' (fig_014's exhaustive bar values); one isolated case slightly favored C1 (fig_038's label fidelity). No pattern of degradation.
- **Clarity**: Both conditions produce well-structured, unambiguous Bulgarian descriptions. The Bulgarian output quality is not affected by the language of the instruction prompt.
- **Language quality**: The Bulgarian text in C2' does not exhibit translation artifacts, awkward phrasing, or code-switching that might indicate degradation from English-language prompting.

The only observable difference is a minor tendency for C2' to translate English labels from the image into Bulgarian, whereas C1 preserves them verbatim. This is a stylistic difference rather than a quality degradation.
