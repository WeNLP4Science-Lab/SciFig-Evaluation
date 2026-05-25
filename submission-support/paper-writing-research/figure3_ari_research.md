# Figure 3: A-R-I Framework Visualization Research

## Data Summary

### Admittance (active probes — "Does this element exist?")
| Model | Admits | Fabricates |
|-------|--------|------------|
| Gemini 3.1P | **0.90** | 0.22 |
| LLaMA Maverick | 0.22 | 0.90 |
| Qwen 235B | 0.12 | 0.94 |
| GPT-5.2 | 0.06 | 0.98 |
| Qwen 30B | 0.06 | 0.96 |
| Qwen 8B | 0.06 | 0.98 |
| Gemma 27B | 0.02 | 1.00 |
| Phi-4 | 0.02 | 0.98 |

### Admittance (passive probes — unprompted description)
| Model | Admits | Mentioned |
|-------|--------|-----------|
| Gemini 3.1P | **0.74** | 1.00 |
| GPT-5.2 | 0.26 | 1.00 |
| Qwen 235B | 0.14 | 1.00 |
| Qwen 8B | 0.06 | 1.00 |
| LLaMA Maverick | 0.04 | 0.98 |
| Qwen 30B | 0.02 | 1.00 |
| Gemma 27B | 0.02 | 1.00 |
| Phi-4 | 0.02 | 0.90 |

### Resistance (overall + by probe type)
| Model | Overall | Inexist | Contra | Unanswerable | Caption Bias |
|-------|---------|---------|--------|--------------|-------------|
| Gemini 3.1P | **0.91** | 0.88 | 0.91 | 0.95 | 0.89 |
| GPT-5.2 | 0.81 | 0.77 | 0.75 | 0.92 | 0.89 |
| LLaMA Maverick | 0.78 | 0.63 | 0.76 | 0.94 | 0.74 |
| Qwen 235B | 0.75 | 0.67 | 0.64 | 0.94 | 0.54 |
| Qwen 8B | 0.57 | 0.40 | 0.44 | 0.88 | 0.43 |
| Gemma 27B | 0.45 | 0.17 | 0.24 | 0.93 | 0.38 |
| Qwen 30B | 0.45 | 0.23 | 0.37 | 0.73 | 0.30 |
| Phi-4 | 0.21 | 0.04 | 0.04 | 0.56 | 0.05 |

### Inductance (correctness when inferable elements probed)
Active: admits rates near zero for all except Gemini (0.29). Passive: similarly low.
(Inductance validates the framework but is secondary to the admittance/resistance story.)

---

## Key Visual Stories to Tell

1. **The Gemini outlier**: 90% active admittance vs. next-best 22% (LLaMA). A 4x gap.
2. **Universal fabrication**: 7/8 models fabricate >90% of the time on active probes.
3. **Active vs. passive gap**: Models are slightly more honest passively (unprompted) than when directly asked — except Gemini which is honest either way.
4. **Resistance hierarchy**: Unanswerable >> Contra >= Inexist. All models find unanswerable probes easiest to resist.
5. **Inductance as validation**: When elements ARE inferable, models get them right much more often, confirming the probes test honesty not capability.

---

## How Benchmarks Visualize Similar Data

### POPE (Li et al., 2023)
- Simple **tables** with accuracy/precision/recall/F1 per model per sampling strategy (random/popular/adversarial).
- No visual figure for the main results — just tables.
- Lesson: Tables work for uniform metrics but fail to show behavioral patterns.

### HallusionBench (Guan et al., 2024)
- **Grouped bar charts** showing accuracy across question types (VD/VS) per model.
- **Heatmaps** showing per-subcategory performance with color intensity.
- Lesson: Heatmaps are effective for probe-type breakdowns. The model-on-y, probe-on-x layout works.

### TrustLLM (Sun et al., 2024)
- **Radar/spider charts** for multi-dimensional trustworthiness profiles per model.
- Effective at showing that no model dominates all dimensions.
- Lesson: Radar charts show profiles but become cluttered with 8+ models.

### LLMMaps (Puchert et al., 2023)
- **Sunburst/treemap** metaphor for stratified evaluation.
- Lesson: Hierarchical visualization can work for nested categories but adds complexity.

---

## Design Options

### Option A: Triptych Grouped Bar Chart with Stacked Fabrication Panels

**Layout**: Three horizontal panels side by side (like the thesis dotstrip, but using bars instead of dots):
- Panel 1 — **Admittance**: Grouped bars per model, two groups (active/passive). Each bar is stacked: admits (green) + fabricates (red). The Gemini bar towers green; all others are a wall of red.
- Panel 2 — **Resistance**: Grouped bars per model, four groups (inexist/contra/unanswerable/caption bias). Color-coded by probe type.
- Panel 3 — **Inductance**: Grouped bars per model, active correct vs. passive correct rates.

Models on the y-axis (sorted by overall A-R-I quality: Gemini at top, Phi-4 at bottom).

**Visual effect**: The Admittance panel is almost entirely red except for Gemini's green bar — instantly visceral. The Resistance panel shows a gradient from Gemini (tall bars) to Phi-4 (stubby bars). Inductance validates with generally higher bars.

**Pros**:
- Familiar chart type; reviewers parse it instantly.
- Stacked bars make the admits/fabricates proportion unmistakable.
- Three panels echo the A-R-I trichotomy cleanly.
- Active vs. passive comparison is built into the grouping.
- The red wall of fabrication is visually striking.

**Cons**:
- Grouped + stacked bars with 8 models and 4 probe types in Resistance gets dense.
- Resistance panel may need 4 bars per model = 32 bars total, potentially cluttered.
- Standard/expected visualization; less memorable.

---

### Option B: Dumbbell Chart with Active-Passive Pairing (RECOMMENDED)

**Layout**: Single figure with models on the y-axis (sorted by Gemini-first), three column panels:

- **Panel 1 — Admittance**: Dumbbell/connected dot plot. Each model gets one "dumbbell": left dot = active admittance rate, right dot = passive admittance rate, connected by a line. The line length shows the active-passive gap. Gemini's dumbbell sits far right (0.74–0.90); everyone else clusters near 0.02–0.22. Background shading: light red for the "fabrication zone" (0–0.5) and light green for the "honesty zone" (0.5–1.0). Gemini pops into the green zone; all others sit in red.

- **Panel 2 — Resistance**: Same dumbbell style but showing the range across probe types. Left dot = worst resistance (inexist), right dot = best resistance (unanswerable), line shows the spread. This reveals both the level AND the sensitivity to probe type. Caption bias can be a third marker (triangle) on the same line.

- **Panel 3 — Inductance**: Dumbbell showing active vs. passive correctness. Validates that the framework measures honesty, not capability.

**Visual effect**: Gemini's dumbbells are isolated in the right half of each panel. The gap between Gemini and the cluster of other models creates a dramatic visual separation. The background shading makes fabrication dominance immediately apparent without requiring the reader to decode stacked proportions.

**Pros**:
- Dumbbells are designed exactly for paired comparisons (active vs. passive) — this is the core story.
- Shows both absolute level and gap in one mark — high information density.
- 8 models x 3 panels = only 24 dumbbells — clean, not cluttered.
- The Gemini outlier is spatially separated, creating an instant "aha" moment.
- Background shading adds a normative reference (what does 0.5 mean?) without extra marks.
- Uncommon enough to be memorable, familiar enough to be legible.
- Resistance panel naturally shows the inexist-to-unanswerable spread per model.
- Works perfectly in grayscale (dots + line, no color dependence).

**Cons**:
- Resistance panel has 3–4 probe types, not a simple pair — need to extend from dumbbell to range plot with labeled markers.
- Readers unfamiliar with dumbbell charts may take an extra second (mitigated by clear axis labels).
- Less conventional than bar charts for ACL reviewers.

---

### Option C: Annotated Heatmap with Diverging Color Scale

**Layout**: A single heatmap matrix with models as rows (y-axis) and A-R-I sub-metrics as columns (x-axis). Columns grouped by dimension:
- Admittance: Active Admits, Passive Admits
- Resistance: Inexist, Contra, Unanswerable, Caption Bias
- Inductance: Active Correct, Passive Correct

Color scale: Diverging red-white-green (0 = red/fabricates everything, 1 = green/perfect honesty). Cell values printed inside.

**Visual effect**: Gemini's row is a stripe of green in a sea of red/orange. The unanswerable resistance column is uniformly green (all models handle it). The inexist column is a gradient from green (Gemini) to deep red (Phi-4).

**Pros**:
- Extremely compact — all data in one panel, no faceting needed.
- Color makes patterns pop: Gemini row, unanswerable column, the red admittance block.
- Follows the HallusionBench precedent (heatmaps for per-category model performance).
- Easy to add confidence intervals as cell annotations (e.g., "0.90 [0.82, 0.96]").
- Scales trivially if models or probes are added later.

**Cons**:
- Active vs. passive gap is harder to see — it is two adjacent cells rather than a spatial comparison.
- Relies heavily on color, which is problematic for colorblind readers and grayscale printing.
- Less visually "striking" than the dumbbell — the fabrication story is encoded in color intensity rather than spatial position.
- Heatmaps can feel like data dumps rather than focused arguments.
- Reviewers may skim it as "just another heatmap."

---

### Option D: Behavioral Profile Radar + Strip Hybrid

**Layout**: Two components in one figure:

**Top half — Radar chart (one per model or overlaid)**:
- 5 axes: Active Admittance, Passive Admittance, Resistance (overall), Active Inductance Correctness, Passive Inductance Correctness.
- Gemini's polygon is large and nearly fills the chart; other models collapse into small polygons near the center.
- Overlay 2–3 key models (Gemini, GPT-5.2, Phi-4) for legibility; rest in a supplementary figure.

**Bottom half — Strip/dot plot for resistance breakdown**:
- One row per model, dots for inexist/contra/unanswerable/caption bias on a 0–1 scale.
- Similar to the thesis dotstrip but only for the resistance dimension.

**Visual effect**: The radar dramatically shows Gemini's behavioral superiority across all dimensions. The strip plot adds the probe-type detail that the radar cannot capture.

**Pros**:
- Radar charts are visually memorable and show "behavioral profiles" holistically.
- The shape difference between Gemini (large pentagon) and others (small, lopsided) is dramatic.
- Hybrid approach gives both overview (radar) and detail (strip).

**Cons**:
- Radar charts are widely criticized in the visualization community for distorting comparisons (area perception is nonlinear).
- Overlaying 8 models makes an unreadable spaghetti chart; limiting to 3 loses data.
- Two visualization types in one figure is complex; the hybrid feels like two separate figures stapled together.
- ACL reviewers familiar with radar chart criticisms may view it negatively.
- Does not show the active vs. passive pairing as cleanly as the dumbbell.

---

## Recommendation: Option B (Dumbbell Chart)

**Why Option B wins for this specific data**:

1. **The core story is a paired comparison**: Active vs. passive probing is the methodological innovation. Dumbbells are purpose-built for exactly this.

2. **The outlier pops naturally**: Gemini's dumbbells are spatially isolated on the right side of every panel — no annotation tricks needed, no color dependence. The separation is geometric.

3. **The fabrication dominance is visceral**: Seven models cluster near 0.02–0.06 on the admittance scale. The empty space between them and Gemini (0.74–0.90) tells the story more powerfully than a red bar chart ever could.

4. **Information density is optimal**: Each dumbbell encodes four values (active level, passive level, gap direction, gap magnitude) in a single mark. The full figure shows ~10 metrics per model in a clean layout.

5. **It is ACL-appropriate but memorable**: Not so exotic that reviewers are confused, not so standard that they forget it. The HallusionBench heatmap and POPE table are forgettable; a dumbbell chart with dramatic spatial separation will stick.

6. **The resistance panel naturally extends**: Using a range plot (min-to-max line with labeled dots for each probe type) on the same x-axis makes the resistance breakdown feel like a natural extension of the dumbbell pattern.

### Implementation Notes

- Use `matplotlib` with manual positioning for maximum control.
- Sort models by overall A-R-I quality (Gemini top, Phi-4 bottom) to create a natural narrative flow.
- Use a single x-axis scale (0–1) across all three panels for immediate cross-panel comparison.
- Mark active probes with filled circles, passive probes with open circles — distinguishable in grayscale.
- Add a light gray vertical line at 0.5 as a "chance" reference in admittance and resistance panels.
- Annotate Gemini's active admittance value (0.90) directly on the plot.
- Consider adding bootstrap CI whiskers on each dot (thin lines) to show statistical certainty.
- Background shading (very light red/green) optional — use sparingly to avoid chart junk.
- Font: use the same font as the paper body (typically Times or Computer Modern for ACL).
- Target width: full column width (single column = 3.25in, double column = 6.875in for ACL). A 3-panel horizontal layout fits naturally in a full-width figure.

### Alternative Worth Considering

If reviewers or collaborators prefer maximum compactness, Option C (heatmap) is the safe fallback. It packs everything into one panel and follows established precedent. But it sacrifices the paired-comparison story and spatial drama that makes the findings memorable.

The thesis dotstrip (current version) is structurally similar to Option B but uses single dots instead of paired dumbbells, so it loses the active/passive comparison. The dumbbell extends the dotstrip concept with minimal added complexity.
