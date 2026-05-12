# Charts for RQ1

## Global Design Specs

```python
import matplotlib.pyplot as plt
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.linewidth': 0.8,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.format': 'pdf',
})
```

- **Palette**: Paul Tol colorblind-safe: `['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']`
- **Sequential**: viridis or cividis
- **Diverging**: RdYlGn (centered on median)
- **Output**: PDF for thesis, PNG 300 DPI for dashboard
- **Sizes**: Single-column = 3.25", double-column = 6.75"
- **Font minimum**: 8pt

---

## MAIN TEXT FIGURES (3-4)

---

### Figure 1: Heatmap — Model x Language

**Location**: Main text, Page 1 (companion to Table 1)
**Type**: Annotated heatmap
**Size**: Double-column (6.75")

**Layout**:
- Rows: 13 models grouped by family
- Columns: EN, BG, CN, DE, Multi, Overall
- Cell values: MQM score (1 decimal)
- Colormap: RdYlGn diverging, centered on median (~70)

**Implementation**: `seaborn.heatmap(annot=True, fmt='.1f', cmap='RdYlGn', center=70)`
**Bold**: Best score per column in cell text

---

### Figure 2: Scatter — Human vs LLM Judge Correlation

**Location**: Main text, Page 3 (companion to Table 2)
**Type**: Two-panel scatter plot
**Size**: Double-column (6.75")

**Panel A**: Human MQM (x) vs GPT-4o MQM (y)
**Panel B**: Human MQM (x) vs Mistral MQM (y)

**Elements**:
- One point per (figure, model) pair — ~120 points per panel
- Color by model (4 colors from Paul Tol palette)
- Dashed grey y=x identity line
- Solid regression line per panel
- Text box: "rho = 0.XX, p < 0.001"
- Legend for model colors

**Key visual**: Points below y=x line = judge harsher than human

---

### Figure 3: Stacked Bar — Error Type Proportions

**Location**: Main text, Page 4
**Type**: Horizontal 100% stacked bar chart
**Size**: Double-column (6.75")

**Y-axis**: 13 models sorted by total errors
**X-axis**: Proportion 0-100%
**Segments** (6, using paired light/dark colors):
- Accuracy/Major (dark red #CC3311)
- Accuracy/Minor (light red #EE6677)
- Completeness/Major (dark blue #004488)
- Completeness/Minor (light blue #4477AA)
- Clarity/Major (dark grey #666666)
- Clarity/Minor (light grey #BBBBBB)

**Annotations**: Total error count at end of each bar
**Legend**: Below chart, single row

---

### Figure 4 (optional): Scaling Plot

**Location**: Main text, Page 5 (if space permits; otherwise Appendix)
**Type**: Line chart with markers
**Size**: Single-column (3.25")

**X-axis**: Parameter count (log scale)
**Y-axis**: MQM score (0-100)
**Lines**: One per model family (Qwen, Gemma), connecting by size
**Markers**: Individual models as labeled dots
**Separate markers**: Proprietary models on the right (no param count, use rightmost position)

---

## APPENDIX FIGURES (7)

---

### Figure A.1: Scaling Plot
(If not used in main text — same spec as Figure 4 above)

### Figure A.2: IAA Box Plot — Annotator Variability
**Type**: Box + strip plot
**X-axis**: 4 human-evaluated models
**Y-axis**: MQM score
**Elements**: Box per model, overlay strip points colored by annotator (Judge 1 vs Judge 13)
**Size**: Single-column

### Figure A.3: Violin Plot — Score Distributions
**Type**: Violin plot
**X-axis**: 13 models sorted by median
**Y-axis**: MQM score (0-100)
**Elements**: Violin with inner box, white dot for mean
**Size**: Double-column

### Figure A.4: Slope Chart — Language Performance Gap
**Type**: Slope chart
**Layout**: Left=EN score, right columns=BG/CN/DE scores, lines connecting per model
**Color**: By model family
**Size**: Single-column

### Figure A.5: Radar Chart — Model Capability Profiles
**Type**: Radar / spider chart
**Axes**: EN, BG, CN, DE, Atom Accuracy, Atom Completeness
**Layout**: 2 panels — proprietary models | best open-source models
**Size**: Double-column

### Figure A.6: Ablation Delta Chart
**Type**: Diverging horizontal bar (lollipop)
**Y-axis**: Ablation conditions (C2, C2', CCoT)
**X-axis**: Delta MQM from C1 baseline (centered at 0)
**Color**: Green = positive, Red = negative
**Size**: Single-column

### Figure A.7: Cross-Lingual Controlled Bar Chart
**Type**: Grouped bar chart
**X-axis**: Models
**Y-axis**: MQM score
**Bars**: EN, BG, CN, DE (4 per model), error bars from 95% CI
**Data**: 13 parallel figures only
**Size**: Double-column

---

## Output Locations

- PDF: `thesis/main/figures/rq1/` (for LaTeX inclusion)
- PNG: `support/docs/RQ1/plots/` (for review)
- Generation script: `scripts/analysis/plot_rq1_results.py`

## Implementation Priority

1. Figure 1 (Heatmap) — needed for Page 1
2. Figure 2 (Scatter) — needed for Page 3
3. Figure 3 (Stacked bar) — needed for Page 4
4. Figure 4 (Scaling) — optional for Page 5
5. Appendix figures — after main text is drafted
