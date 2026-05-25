# Figure 2: Model Performance Degradation Across Conditions -- Design Research

## 1. Data Summary

### Raw MQM Scores (from all_statistics.json transform_mqm)

| Model | baseline | original | noise | low_contrast | rotation | in_paper | in_paper_blur | caption_bias | admittance_blur | inductance_blur |
|-------|----------|----------|-------|-------------|----------|----------|---------------|-------------|-----------------|-----------------|
| GPT-5.2 | 91.6 | 89.6 | 91.3 | 87.0 | 70.2 | 77.8 | 13.3 | 91.3 | 81.7 | 88.9 |
| Gemini 3.1 Pro | 90.2 | 89.3 | 90.2 | 85.1 | 72.0 | 83.8 | 8.4 | 91.3 | 84.6 | 86.8 |
| Llama4 Maverick | 81.4 | 82.0 | 81.0 | 75.9 | 60.6 | 63.0 | 30.9 | 84.8 | 70.5 | 78.9 |
| Qwen3-VL-235B | 80.8 | 82.6 | 82.1 | 77.8 | 65.3 | 77.2 | 22.9 | 83.4 | 71.0 | 79.0 |
| Qwen3-VL-30B | 74.4 | 77.3 | 74.3 | 75.7 | 58.2 | 68.3 | 24.3 | 78.3 | 67.5 | 74.7 |
| Qwen3-VL-8B | 78.9 | 78.5 | 80.1 | 76.0 | 61.9 | 72.9 | 25.8 | 83.0 | 71.5 | 74.8 |
| Gemma3-27B | 69.1 | 60.9 | 62.2 | 61.5 | 49.8 | 35.4 | 25.3 | 70.9 | 58.3 | 59.6 |
| Phi-4 | 62.2 | 59.5 | 61.3 | 64.7 | 43.7 | 31.3 | 17.7 | 61.7 | 56.6 | 59.4 |

### Key Patterns in the Data

1. **Minimal degradation**: noise, caption_bias, inductance_blur -- scores stay near baseline. Noise and caption bias are "easy" perturbations.
2. **Moderate degradation**: low_contrast, admittance_blur, original (slightly lower due to subset) -- 5-15 point drops for most models.
3. **Severe degradation**: rotation (~20-30 point drops), in_paper (~10-30 point drops, devastating for weaker models).
4. **Catastrophic collapse**: in_paper_blur -- ALL models drop to 8-31 range. This is the "nuke" condition.
5. **Rank reversals**: Gemini overtakes GPT-5.2 under in_paper and rotation. Llama4 overtakes GPT-5.2 under in_paper_blur (30.9 vs 13.3!). Phi-4 overtakes Gemma3 under low_contrast.
6. **Caption bias paradox**: Models actually IMPROVE slightly with biased captions, revealing caption dependence.
7. **The top-2 gap**: GPT-5.2 and Gemini form a clear top tier, ~10 points above the pack at baseline, and this gap narrows under stress.
8. **Sample sizes vary**: baseline=250, most transforms=~100, selective blurs=~50.

### Logical Condition Groupings

- **Reference**: baseline (n=250)
- **Perceptual transforms**: noise, low_contrast, rotation (n~100 each)
- **Contextual transforms**: original (no caption), in_paper (with surrounding text), caption_bias (n~100 each)
- **Selective blur (adversarial)**: in_paper_blur, admittance_blur, inductance_blur (n=50-100)


---

## 2. How Top Papers Visualize This

### ImageNet-C / Robustness Benchmarks
- **Radar/spider charts** per corruption category, with models overlaid -- effective for 4-5 models, cluttered beyond that.
- **Bar charts grouped by corruption type**, models as grouped bars -- the most common but space-hungry approach.
- **Heatmaps** (model x corruption) with color = error rate -- used in RobustART, comprehensive ImageNet robustness studies.
- **mCE tables** with a single summary metric per model -- clean but hides the per-condition story.

### HELM Benchmark
- Uses **grouped tables with cell coloring** (best/worst highlighted). Also uses **radar plots** for capability profiles.

### TextFlint (ACL 2021)
- **Grouped bar charts** with transformation types on x-axis, models as bars within each group.

### Brittlebench (2026)
- Rank-shift analysis: shows how perturbations change relative model ordering -- directly relevant to our rank reversal finding.

### Key Insight from Literature
The most impactful visualizations in top papers are **not the most complex**. They succeed by:
1. Having a clear "takeaway" visible in 5 seconds
2. Using redundant encoding (position + color + annotation)
3. Grouping conditions semantically rather than alphabetically
4. Highlighting 2-3 key findings with callouts/annotations


---

## 3. Design Options

### Option A: Enhanced Slope Chart (Thesis-Style, Improved)

**Description**: Line chart with conditions on x-axis (grouped with vertical separators), MQM on y-axis. Top 3 models (GPT-5.2, Gemini, Llama4/Qwen3-235B) in distinct colors with markers. Bottom 4-5 models in thin grey lines. Annotations at key points.

**Layout**:
```
Y-axis: MQM Score (0-100)
X-axis: baseline | noise low_c rotation | original in_paper caption_bias | adm_blur ind_blur in_paper_blur
         [ref]   [---perceptual---]      [-----contextual-----]           [----selective blur----]
```

- Vertical dashed separators between groups
- Group labels above x-axis
- Annotations: "Rank reversal" arrow at in_paper_blur, "Caption improves scores" at caption_bias
- Model names at right edge of lines (like the thesis figure)
- Confidence interval bands (translucent) for highlighted models

**Pros**:
- Directly shows trajectories -- the reader's eye follows the "story" left to right
- Familiar to NLP audience (line charts are standard)
- Naturally reveals rank reversals where lines cross
- Can show confidence bands without clutter (only for 2-3 models)
- Proven design: thesis version already works well

**Cons**:
- 10 conditions on x-axis is a lot -- labels will be cramped in a single-column figure
- in_paper_blur collapse (scores drop to 8-31) compresses the rest of the y-axis
- 8 lines can still be cluttered even with grey treatment
- Doesn't handle different sample sizes visually

**Improvements over thesis version**:
- Add group separators and labels
- Order conditions by severity within each group
- Use 95% CI bands (not just lines) for top models
- Add n= counts below x-axis labels
- Consider log-scale or broken y-axis to handle the in_paper_blur collapse


### Option B: Heatmap (Models x Conditions)

**Description**: 8 rows (models, ordered by baseline performance) x 10 columns (conditions, grouped). Color = MQM score using a diverging colormap (dark green = 90+, white = 60, red = <30). Cell values printed inside.

**Layout**:
```
                    Reference  |  Perceptual        |  Contextual              |  Selective Blur
                    baseline   |  noise  low_c rot  |  original in_paper cap   |  adm  ind  in_paper_blur
GPT-5.2            [91.6]     |  [91.3] [87.0][70.2]| [89.6]  [77.8]  [91.3] | [81.7][88.9] [13.3]
Gemini 3.1 Pro     [90.2]     |  ...
...
Phi-4              [62.2]     |  ...
```

**Pros**:
- Extremely compact -- fits a full-width single-column figure easily
- Color immediately reveals the "hot spots" of failure (in_paper_blur column is solid red)
- Natural for readers familiar with leaderboard tables
- Easy to add annotations (asterisks for significant drops, borders for rank reversals)
- Handles different sample sizes gracefully (just note n in column header)
- No clutter problem at all -- each cell is independent

**Cons**:
- Doesn't show trajectories or trends as naturally as a line chart
- Harder to see rank reversals (need to compare cells vertically)
- Color perception varies across readers; must be grayscale-readable (ACL requirement)
- Less "visual impact" than a line chart -- feels more like a table

**Design details**:
- Use `RdYlGn` or custom diverging colormap
- Print values in each cell (white text on dark cells, black on light)
- Bold the highest value in each column
- Add row-level sparkline or delta column on the right showing overall degradation
- Consider adding a "delta from baseline" version as a companion


### Option C: Grouped Dumbbell/Lollipop Chart

**Description**: Y-axis = models (8 rows). For each model, show a horizontal dumbbell: left dot = worst condition score, right dot = baseline score, line connecting them. Color-code the dots by condition. Optionally show individual condition dots along the line.

**Alternative framing**: One row per model. Show baseline as a vertical reference line. Plot each condition as a dot, color-coded by group (perceptual/contextual/selective blur). Distance from baseline = degradation.

**Layout** (dot strip variant):
```
GPT-5.2         |----o--o--------o------X-o-o-------|  baseline=91.6
                     ^  ^        ^      ^ ^ ^
                   rot low_c   in_pap  noise cap ind
                                       in_p_blur (at 13.3, far left)

Gemini 3.1 Pro  |---o--o---------o-----X-o-o-------|  baseline=90.2
...
```

**Pros**:
- Focuses on the KEY STORY: how far each model falls from its baseline
- Each model gets its own row -- no overlap or clutter
- Can cluster dots by condition group using color
- Outliers (in_paper_blur) are immediately visible as extreme leftward dots
- Shows both absolute level (x position) and degradation (distance from baseline)

**Cons**:
- Doesn't show condition-to-condition trajectories
- 10 dots per row may overlap if scores are similar
- Less familiar chart type -- some readers may need a moment to parse
- Doesn't naturally reveal rank reversals between models


### Option D: Two-Panel Composite (RECOMMENDED)

**Description**: Combine the best of Options A and B into a two-panel figure that tells two complementary stories.

**Panel (a) -- Slope chart (simplified)**:
- X-axis: 7 key conditions only (drop noise, original, inductance_blur which show minimal effect -- or keep all 10 if space permits in a full-width figure)
- Show only top 3 models in color (GPT-5.2, Gemini, Qwen3-235B), rest in grey
- Y-axis: MQM score
- Annotations at key crossover points
- Group separators
- This panel tells the TRAJECTORY story

**Panel (b) -- Delta heatmap**:
- 8 rows (models) x conditions columns
- Color = CHANGE from baseline (not absolute score)
- Green = improvement over baseline, white = no change, red = degradation
- This reveals: (1) caption_bias slightly improves some models, (2) in_paper_blur is universally catastrophic, (3) which models are most/least robust
- Print delta values in cells: "-4.6", "+1.2", "-78.3" etc.
- This panel tells the RELATIVE ROBUSTNESS story

**Layout**:
```
Full-width figure (7 inches), two panels side by side or stacked vertically.
If side-by-side: panel (a) = 4 inches, panel (b) = 3 inches
If stacked: each panel = 7 inches wide, total height ~4 inches
```

**Pros**:
- Two complementary views: trajectory (slope) + magnitude (heatmap)
- Slope chart shows the narrative; heatmap provides the reference
- Can simplify each panel (fewer conditions in slope, deltas in heatmap)
- Professional, publication-quality look
- Handles the "story" problem: reader first sees the slope for the big picture, then consults the heatmap for details
- The delta heatmap avoids the y-axis compression problem of the slope chart

**Cons**:
- Takes more space (but full-width figures are fine in ACL)
- Two panels = more for the reader to process
- Must ensure consistent condition ordering between panels


---

## 4. Specific Design Decisions

### X-axis ordering
**Recommendation**: Order by severity of degradation (mean across models), NOT alphabetically. This creates a natural "slope" in the line chart.

Severity order (from data, mean drop across all models):
1. caption_bias: +1.8 (actually improves!)
2. noise: -0.4
3. inductance_blur: -2.4
4. original: -4.1
5. low_contrast: -5.3
6. admittance_blur: -7.9
7. in_paper: -16.5
8. rotation: -19.2
9. in_paper_blur: -58.5

However, **grouping by type is better than strict severity order** because it tells a more coherent story. Within each group, order by severity.

**Recommended order**: baseline | noise, low_contrast, rotation | caption_bias, original, in_paper | inductance_blur, admittance_blur, in_paper_blur

### Absolute vs. delta scores
- **Slope chart**: Use ABSOLUTE scores. Readers need to see that GPT-5.2 starts at 91.6 and Phi-4 starts at 62.2.
- **Heatmap companion**: Use DELTA from baseline. This normalizes the comparison and reveals which models are most robust regardless of starting point.

### Single vs. multi-panel
- **Single-column figure**: Use heatmap (Option B) -- it's the only one that fits cleanly.
- **Full-width figure**: Use two-panel composite (Option D) -- this is the ACL best paper play.

### Handling different sample sizes
- Add n= in parentheses below condition labels on x-axis: "noise (n=98)", "adm_blur (n=50)"
- In heatmap: use column header annotation
- Consider showing wider confidence intervals for smaller n (the blur conditions with n=50 have wider CIs)
- Do NOT normalize by sample size -- the MQM means are already comparable


---

## 5. Tools and Styling

### Recommended stack
- **matplotlib** with custom rcParams for font sizes, line weights, and colors
- **No seaborn defaults** -- the seaborn "look" screams "student project." Use matplotlib directly with careful styling.
- Use `matplotlib.gridspec` for multi-panel layout
- Export as **PDF** (vector) for the paper, PNG at 600 DPI for reviews

### ACL figure requirements
- Figures must be readable in grayscale (use distinct line styles + markers, not just color)
- Single column width: ~3.3 inches / 8.4 cm
- Full width (two-column): ~7.0 inches / 17.8 cm
- Captions below figures, 10pt roman type
- Use Type 1 or TrueType fonts (matplotlib default is fine)

### Style specifications for the slope chart
```python
# rcParams
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette (colorblind-safe, grayscale-distinguishable)
HIGHLIGHT_COLORS = {
    'GPT-5.2': '#2171B5',        # Blue
    'Gemini 3.1 Pro': '#238B45', # Green
    'Qwen3-VL-235B': '#D94801',  # Orange
}
GREY = '#B0B0B0'
GREY_ALPHA = 0.4

# Line styles for grayscale fallback
LINE_STYLES = {
    'GPT-5.2': '-',
    'Gemini 3.1 Pro': '--',
    'Qwen3-VL-235B': '-.',
}

# Markers
MARKERS = {
    'GPT-5.2': 'o',
    'Gemini 3.1 Pro': 's',
    'Qwen3-VL-235B': '^',
}
```

### Style specifications for the heatmap
```python
# Custom diverging colormap for deltas
from matplotlib.colors import LinearSegmentedColormap
colors_delta = ['#B2182B', '#F4A582', '#FDDBC7', '#F7F7F7', '#D1E5F0', '#92C5DE', '#2166AC']
cmap_delta = LinearSegmentedColormap.from_list('delta', colors_delta, N=256)

# For absolute scores
colors_abs = ['#B2182B', '#F4A582', '#FFFFBF', '#A6D96A', '#1A9641']
cmap_abs = LinearSegmentedColormap.from_list('mqm', colors_abs, N=256)
```


---

## 6. Final Recommendation

### For an ACL best paper submission: Option D (Two-Panel Composite)

**Panel (a)**: Full-width slope chart, all 10 conditions grouped with vertical separators. Top 3 models (GPT-5.2 blue solid, Gemini green dashed, Qwen3-235B orange dash-dot) in color with markers and 95% CI bands. Remaining 5 models in thin grey lines (no markers). Model names at right edge. Two annotations: (1) "Rank reversal" at in_paper_blur where Llama4 > GPT-5.2, (2) "Caption bias improves scores" at caption_bias. X-axis labels rotated 30 degrees with n= counts.

**Panel (b)**: Delta-from-baseline heatmap, 8 rows x 9 columns (exclude baseline itself). Color = delta MQM. Values printed in cells. Row order matches y-axis order of panel (a) (by baseline performance). Column order matches panel (a) x-axis. This panel is compact -- can fit below or beside panel (a).

**Why this wins**:
1. The slope chart delivers the "wow" finding (catastrophic collapse under in_paper_blur, rank reversals) in a visually dramatic way
2. The heatmap delivers precision -- reviewers can check any model x condition cell
3. The delta encoding in the heatmap reveals that caption_bias is the only condition that improves scores (green cells) -- a finding that would be buried in absolute scores
4. The composite format signals "thorough analysis" to reviewers
5. Grayscale-safe: slope chart uses line styles + markers; heatmap prints values in cells

**Fallback**: If space is tight, use Option B (heatmap only) as a single-column figure. It's the most information-dense option and works well at small sizes.

### What to cut from the thesis version
The thesis slope chart (degradation_slope.png) is good but has issues:
1. Too many highlighted models (5-6 in color) -- reduce to 3
2. No condition grouping -- add vertical separators and group labels
3. No annotations -- add 2-3 callouts for key findings
4. No confidence intervals -- add CI bands for highlighted models
5. X-axis labels are plain -- add n= counts and rotate for readability
6. The y-axis range (40-90) doesn't accommodate in_paper_blur (8-31) well -- consider a broken y-axis or inset panel for the extreme condition
