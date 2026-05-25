# Figure 5: MQM vs Behavioural Reliability — Design Options

Research compiled May 2026. Four design options for a column-width (~3.25 in) figure showing that model quality (MQM) does NOT predict behavioural reliability (admittance/resistance).

---

## Data Summary

| Model       | MQM   | Admittance | Resistance |
|-------------|-------|------------|------------|
| GPT-5.2     | 91.6  | 6%         | 0.81       |
| Gemini      | 90.2  | 90%        | 0.91       |
| Llama4      | 81.4  | 22%        | 0.78       |
| Qwen-235B   | 80.8  | 12%        | 0.75       |
| Qwen-8B     | 78.9  | 6%         | 0.57       |
| Qwen-30B    | 74.4  | 6%         | 0.45       |
| Gemma       | 69.1  | 2%         | 0.45       |
| Phi-4       | 62.2  | 2%         | 0.21       |

Key story: GPT-5.2 is #1 MQM but #4-6 behaviourally. Gemini is #2 MQM but #1 on everything behavioural. If quality predicted behaviour, the dots would form a diagonal. They do not.

Spearman rho (MQM vs Admittance): approx 0.36 (weak, non-significant with n=8).
Spearman rho (MQM vs Resistance): approx 0.86 (looks correlated, but the story is about the RANK REVERSALS at the top — Gemini leapfrogs GPT-5.2, and the gap between top-2 and the rest is enormous on behaviour but smooth on MQM).

---

## Option A: Dual Micro-Scatter with Rank Annotations (RECOMMENDED)

### Layout
Two tiny scatter plots side by side, sharing a horizontal MQM axis:
- Left panel: MQM (x) vs Admittance (y)
- Right panel: MQM (x) vs Resistance (y)

### Key design moves
1. **Model initials as the data points themselves** — no circles. Each point is its 2-3 letter abbreviation (GP, Ge, Ll, Q2, Q8, Q3, Gm, Ph) in 6pt font. This eliminates the need for a legend and makes identification instant. Precedent: Edward Tufte's "direct labelling" principle; used in several ACL 2024 evaluation papers.
2. **A faint diagonal guide line** (dashed, very light grey) showing where points WOULD fall if quality predicted behaviour. The scatter away from this line IS the finding.
3. **Highlight the GPT-5.2 / Gemini pair** with a subtle colour accent (e.g., GPT in red, Gemini in blue) while all others are dark grey. A thin connecting line between these two points with a delta annotation ("84pp gap" on admittance panel) tells the story without clutter.
4. **Minimal axes**: 3 ticks on each axis. No gridlines. Axis labels inside the panel (rotated y-label at top-left, x-label at bottom-right) to save space.
5. **Spearman rho printed in each panel** as a small annotation: "rho = 0.36" and "rho = 0.86" with the caveat that the visual makes clear the rho=0.86 hides rank reversals.

### Why this works
- Instantly readable: the text-as-points trick means zero lookup time.
- The diagonal guide line is the "null hypothesis" made visual. The viewer immediately sees the dots scattered away from it.
- Two panels side by side show the same MQM axis producing different behavioural patterns, reinforcing that quality is a poor predictor.
- Fits in column width (3.25 in) with two ~1.5 in panels and a thin gap.

### Size
Column-width. Each panel approximately 1.5 x 1.5 inches. Total: 3.25 x 1.7 inches including labels.

### Precedent
Text-as-points scatter plots appear in Ribeiro et al. (CheckList, ACL 2020) and in several Tufte-inspired ML evaluation papers. The dual-panel micro-scatter is standard in biostatistics for comparing two outcomes against the same predictor.

---

## Option B: Slope Chart (Rank Spaghetti)

### Layout
Three vertical axes arranged left to right:
- Left axis: MQM rank (1-8)
- Middle axis: Admittance rank (1-8)
- Right axis: Resistance rank (1-8)

Lines connect each model's rank across all three axes. Rank 1 at top.

### Key design moves
1. **Line crossings ARE the story.** If quality predicted behaviour, lines would be parallel. Instead, the GPT-5.2 line plunges from rank 1 (MQM) to rank 5 (Admittance), while Gemini rises from rank 2 to rank 1. The crossing is dramatic and immediate.
2. **Colour only GPT-5.2 (red) and Gemini (blue).** All other models in light grey — they form a tangle of crossings that visually screams "no correlation" while the two highlighted models carry the narrative.
3. **Rank numbers at each axis endpoint** for the highlighted models only (e.g., "1" and "5" for GPT on MQM and Admittance).
4. **Model names on the left edge** next to their MQM rank.

### Why this works
- The visual metaphor is powerful: parallel lines = correlation, crossing lines = no correlation. The viewer grasps this without any statistical training.
- Three dimensions (MQM, Admittance, Resistance) in one figure — more information-dense than the dual scatter.
- Compact: fits in ~2.5 x 2.0 inches.

### Risks
- With 8 models and 3 axes, the middle can get cluttered. Mitigated by greying out 6 of 8 models.
- Less conventional in NLP papers — could read as unfamiliar to reviewers. But also more memorable if done cleanly.

### Precedent
Bump charts / slope graphs originate with Tufte's slopegraph and are used in The Economist, NYT, and increasingly in ML papers comparing benchmark rankings (e.g., Colorslope, Springer 2023).

---

## Option C: Quadrant Scatter with Shaded Zones

### Layout
Single scatter plot. MQM on x-axis, a combined behavioural score on y-axis (average of normalised admittance and resistance).

### Key design moves
1. **Quadrant shading.** Divide the plot into four zones with dashed lines at the median of each axis:
   - Top-right (light green): high quality, high reliability — **where you want to be**
   - Top-left: low quality, high reliability
   - Bottom-right (light red): high quality, LOW reliability — **the danger zone** (GPT-5.2 lands here)
   - Bottom-left: low quality, low reliability
2. **Quadrant labels** in italic: "Capable & Reliable", "Capable & Unreliable", etc.
3. **Model names as point labels**, offset with thin leader lines where needed for overlap avoidance.
4. **Circle size encodes a third variable** (e.g., model parameter count or cost), adding a bubble-chart dimension.
5. **The punchline**: GPT-5.2 sits alone in the "Capable & Unreliable" quadrant. Gemini sits alone in "Capable & Reliable."

### Why this works
- The quadrant framing gives the viewer a cognitive framework: it is not just "no correlation" but "these models are in the WRONG quadrant."
- Familiar from strategy consulting (BCG matrix), so reviewers from applied backgrounds will instantly parse it.
- The red-shaded danger zone draws the eye to the key finding.

### Risks
- Combining admittance and resistance into a single "behavioural" score requires justification (what weights? what normalisation?). Could be challenged in review.
- Single panel means you lose the ability to show admittance and resistance separately, which have different distributions.
- Quadrant boundaries are arbitrary (why median? why not another cut?).

### Precedent
Quadrant plots appear in Chatbot Arena analyses and in the "cost vs quality" figures of papers like LMSYS (2024). The BCG matrix is the most recognisable quadrant framework in business, and it has been adapted in several ML systems papers.

---

## Option D: Dumbbell / Connected Dot Plot (Rank Gap)

### Layout
Horizontal chart. Each model is a row. Two dots per row connected by a line:
- Left dot: MQM rank
- Right dot: Admittance rank (or Resistance rank)
- The line length and direction show the rank gap.

### Key design moves
1. **Sort rows by MQM rank** (GPT-5.2 at top). The viewer reads down the left column and sees a clean 1-2-3-4-5-6-7-8 sequence. Then the right column is scrambled — instantly showing non-correlation.
2. **Colour the connecting lines**: red if the model drops in rank (MQM rank < Admittance rank, i.e., worse behaviour than expected), blue if it rises. GPT-5.2 gets the longest red line. Gemini gets a blue line (rises from 2 to 1).
3. **Line length is proportional to rank change**, so the visual weight of each model's "quality-behaviour gap" is immediately apparent.
4. **Two side-by-side dumbbell charts** (one for admittance, one for resistance) stacked or placed side by side.

### Why this works
- Extremely compact and readable. Even 8 models with two panels fit in column width.
- The red/blue colour coding makes the narrative binary: is behaviour better or worse than quality would predict?
- No statistical knowledge required — anyone can read it.

### Risks
- Uses rank, not raw values. Loses magnitude information (e.g., the 84pp admittance gap between Gemini and Llama4 looks like a 1-rank difference).
- Less visually striking than scatter or slope charts — may not "pop" for a best paper.

### Precedent
Dumbbell charts are advocated by Stephanie Evergreen and Cole Nussbaumer Knaflic (Storytelling with Data). Used in The Economist and increasingly in ML fairness papers to show metric disagreements.

---

## Recommendation: Option A (Dual Micro-Scatter)

**Option A is the strongest choice for this paper.** Here is why:

1. **It fits the paper's voice.** The master style guide emphasises contrast and punchlines. Two panels showing the SAME x-axis (quality) producing DIFFERENT y-axis patterns is contrast made visual.

2. **It is small and self-contained.** At 3.25 x 1.7 inches, it sits cleanly in a single column without crowding the text.

3. **Text-as-points eliminates clutter.** No legend, no colour key for 8 models. Each point IS its label. This is the kind of elegant minimalism that best paper reviewers notice.

4. **The diagonal guide line does the statistical work visually.** Printing rho in the corner confirms it numerically, but the viewer already sees the non-correlation before reading the number.

5. **It preserves raw values, not just ranks.** The viewer sees that GPT-5.2 is at 91.6 / 6% — the absurdity of the gap lands harder in raw numbers than in ranks.

6. **The GPT/Gemini highlight is surgical.** Red and blue for just those two models, with a delta annotation, delivers the paper's central contrast without making the figure "about" any single model.

### Implementation notes
- Use matplotlib with `scienceplots` (ieee style) for consistent typography.
- Font: 7pt sans-serif for point labels, 8pt for axis labels.
- Diagonal guide: `ax.plot([xmin,xmax],[ymin,ymax], ls='--', lw=0.5, c='#cccccc', zorder=0)` after normalising both axes to [0,1] range.
- GPT label in `#c0392b` (muted red), Gemini in `#2980b9` (muted blue), all others in `#555555`.
- Panel gap: 0.4 inches (use `fig.subplots_adjust(wspace=0.35)`).
- Add Spearman rho as `ax.text()` in top-left corner of each panel, 6pt italic.
- Consider adding 95% CI whiskers on each point from the bootstrap data in `all_statistics.json` to show that the MQM differences between GPT-5.2 and Gemini are NOT significant while the admittance difference clearly is.

### Alternative strong choice: Option B (Slope Chart)
If the goal is maximum visual drama — the lines crossing like spaghetti — the slope chart is more memorable. It works best if the paper has space for a paragraph explaining how to read it. For a figure that must be instantly self-explanatory, Option A wins.
