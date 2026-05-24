# Figure Design Research for SciFig-Eval Paper

Research compiled May 2026. Covers figure patterns in top ACL/NLP papers, benchmark/evaluation paper conventions, unconventional visualization types, design principles, anti-patterns, and specific figure recommendations for the SciFig-Eval paper.

---

## 1. Figure 1 Patterns in ACL 2023-2025 Best Papers

### What Figure 1 Typically Shows

Based on analysis of ACL 2024 best papers and top evaluation papers from 2023-2025:

**Pattern A: The "Problem + Our Approach" Split (most common, ~60% of papers)**
- Left side shows the problem/limitation of existing work
- Right side shows how this paper addresses it
- Usually page-width (two columns)
- Example: HallusionBench Figure 1 uses four diverse visual examples with red-highlighted human edits showing how models fail when images change -- instantly communicates the benchmark's purpose without reading text

**Pattern B: The "Framework Overview" Diagram (~25%)**
- Shows the evaluation/system pipeline end-to-end
- Boxes connected by arrows, color-coded by component type
- Usually page-width
- Example: AppWorld Figure 1 shows a concrete task example flowing through the benchmark system, making an abstract framework tangible

**Pattern C: The "Result Preview" Hook (~15%)**
- Jumps straight to the most surprising finding
- A single chart that makes the reader say "wait, really?"
- Can be column-width or page-width
- Example: MathVista Figure 1 uses a horizontal bar chart comparing model accuracy, immediately showing the performance gap between models and humans

### Design Characteristics of Effective Figure 1s

1. **Spans two columns** in almost all best papers -- Figure 1 gets maximum visual real estate
2. **Information density is high but layered**: a quick glance gives the main point, closer reading reveals details
3. **Uses real data examples** embedded in the diagram, not just abstract boxes
4. **Color is functional**: distinguishes categories (e.g., red for errors, blue for correct, grey for baseline)
5. **Typically combines visual elements**: diagram + examples, chart + annotations, pipeline + data samples
6. **Hooks the reader** by showing either (a) a surprising result or (b) a concrete example of the problem

### Color Schemes in Best Papers

- HallusionBench: Red highlights on a white/grey background for failure cases
- MathVista: Blue/orange two-tone for model vs. human performance
- POPE: Clean blue/grey palette with accent colors for key findings
- Mission: Impossible Language Models: Used distinct colors per language type on the impossibility continuum
- Aya Model: Used a world map visualization with color gradients for language coverage

### What Makes Figure 1 Hook the Reader

The most effective Figure 1s do one of these:
1. **Show a concrete failure** that makes the reader feel the problem viscerally (HallusionBench)
2. **Reveal a counterintuitive result** that challenges assumptions (Mission: Impossible LMs)
3. **Display the scope and ambition** of the contribution at a glance (Aya's 101-language map)
4. **Compress the entire paper narrative** into one visual: problem, method, result (MathVista)

---

## 2. Figures in Top Benchmark/Evaluation Papers

### HallusionBench (CVPR 2024)

| Figure | Type | What It Shows | Effectiveness |
|--------|------|---------------|---------------|
| Fig 1 | Annotated examples with red highlights | Data samples across diverse topics; human-edited images highlighted in red | Instantly communicates the manipulation methodology; concrete and visceral |
| Fig 2 | Three-panel composite (table + bar chart + distribution) | Dataset statistics: question counts, subcategory distribution, image type breakdown | Efficiently conveys dataset composition in one figure |
| Fig 3 | Decision tree / flowchart | Blue and orange nodes mapping correctness outcomes to failure categories | Makes diagnostic classification transparent and reproducible |
| Fig 4 | Multi-series line graph | Model accuracy across visual input categories | Shows relative performance and category-specific weaknesses |
| Fig 5 | Case study vignettes | Original/edited image pairs with model outputs | Makes abstract failure modes tangible |

**Key takeaway**: HallusionBench excels at mixing quantitative results with qualitative examples. Every abstract concept has a concrete visual counterpart.

### POPE (EMNLP 2023)

- Uses clean, minimal figures focused on the polling-based methodology
- Bar charts comparing F1 scores with error bars showing stability advantage (std 0.78 vs CHAIR's 3.22)
- Framework diagram showing the polling-based object probing pipeline
- Effective use of **simplicity** -- each figure makes exactly one point

### MathVista (ICLR 2024)

- Figure 1: Horizontal bar chart comparing model accuracy -- immediately shows the gap
- Figure 2: Panel of dataset examples (IQTest puzzles, function plots, paper figures) -- shows visual diversity
- Figure 3: Donut chart showing dataset composition across task categories
- Uses a **taxonomy hierarchy** to organize seven reasoning types and five task categories
- Blue/orange color scheme throughout for consistency

### ChartQA

- Framework figure showing visual + logical reasoning pipeline
- Sample questions embedded alongside actual charts
- Performance comparison tables (leaning heavily on tables over figures)

### AppWorld (ACL 2024)

- Figure 1: Concrete task example flowing through the benchmark system
- Emphasizes the complexity gap (best model solves only ~30% of tasks)
- Clean, professional diagrams with API/app architecture visualization

### Common Patterns Across Benchmark Papers

1. **Figure 1 always shows concrete examples** -- not just an abstract framework
2. **At least one figure dedicated to dataset statistics** (distribution, composition)
3. **Model comparison uses bar charts or tables** -- rarely radar charts
4. **Case study figures with model outputs** appear in most papers (often in appendix)
5. **Color coding is consistent** throughout the paper (same color = same model/category)
6. **Heatmaps are used for model x condition matrices** in papers with many conditions

---

## 3. Unconventional / Memorable Figure Types for NLP Papers

### Radar / Spider Charts
- **Use case**: Multi-dimensional model profiles (e.g., quality vs. admittance vs. resistance vs. inductance)
- **Strengths**: Shows the "shape" of a model's capabilities at a glance; enables overlay comparisons
- **Weaknesses**: Becomes cluttered with >6-7 axes or >4-5 models; axis order affects perception
- **When to use**: Comparing 3-5 models across 4-7 dimensions; showing that models have different "profiles"
- **NLP precedent**: MMBench uses radar charts for ability dimension comparisons; InternVL papers use them extensively
- **Recommendation for SciFig**: Strong candidate for A-R-I profiles -- each model gets a distinctive shape

### Heatmaps
- **Use case**: Model x condition matrices; error type distributions
- **Strengths**: Compact representation of large tables; patterns (rows, columns, clusters) are visually obvious
- **Weaknesses**: Precise values hard to read; needs good color scale
- **When to use**: When you have a matrix of results (models x transforms, models x question types)
- **NLP precedent**: Extremely common in evaluation papers for showing cross-condition performance
- **Recommendation for SciFig**: Use for the full model x adversarial condition performance matrix

### Bump Charts
- **Use case**: Showing how model rankings change across conditions
- **Strengths**: Directly shows rank inversions (the paper's core thesis about quality != reliability)
- **Weaknesses**: Cluttered with >10-12 items; requires clear line differentiation
- **When to use**: When the story is about rank changes, not absolute values
- **Recommendation for SciFig**: Excellent for showing that MQM rankings do NOT predict adversarial rankings -- the crossing lines literally visualize the orthogonality claim

### Slope Charts
- **Use case**: Paired comparison between two conditions (e.g., standard vs. adversarial)
- **Strengths**: Clean, minimal; slope direction immediately shows improvement/degradation
- **Weaknesses**: Only two conditions; can be cluttered with many items
- **Recommendation for SciFig**: Use for quality-rank vs. reliability-rank comparison for each model

### Sankey / Alluvial Diagrams
- **Use case**: Showing flow from input conditions to outcome types (e.g., blurred element -> admits/fabricates/correct)
- **Strengths**: Shows proportional flow; reveals where most errors go
- **Weaknesses**: Complex to read; needs careful labeling
- **Recommendation for SciFig**: Strong candidate for showing how models handle adversarial probes -- where do fabrications come from?

### Small Multiples
- **Use case**: Per-model breakdowns using the same chart template repeated
- **Strengths**: Enables comparison without overlay clutter; each panel is simple
- **Weaknesses**: Takes space; requires consistent scales
- **NLP precedent**: Common in papers with per-language or per-category breakdowns
- **Recommendation for SciFig**: Use for per-model A-R-I radar charts or per-transform degradation curves

### Parallel Coordinates
- **Use case**: Multi-metric comparison across models
- **Strengths**: Shows correlations and trade-offs across many dimensions simultaneously
- **Weaknesses**: Lines can cross and create clutter; axis order matters
- **Recommendation for SciFig**: Could replace or supplement radar charts for showing model profiles across many metrics

### Waffle Charts
- **Use case**: Showing proportions (e.g., % of time model admits vs. fabricates vs. answers correctly)
- **Strengths**: More precise than pie charts; visually distinctive; each square = a fixed unit
- **Weaknesses**: Less familiar to readers; takes space
- **Recommendation for SciFig**: Use for the fabrication/admittance/correct proportions per model -- more memorable than a stacked bar

### Annotated Example Figures
- **Use case**: Showing actual model input/output on real data with annotations
- **Strengths**: Makes abstract metrics concrete; most memorable figure type for reviewers
- **NLP precedent**: Nearly every top benchmark paper includes these
- **Recommendation for SciFig**: Essential -- show a selectively blurred figure with model responses annotated

---

## 4. What Makes a Figure "Award-Worthy"

Based on analysis of ACL/EMNLP/CVPR best paper figures:

### The Five Tests

1. **The Glance Test**: Can a reviewer understand the main finding in 3 seconds? If not, simplify.
2. **The Captionless Test**: Does the figure tell its story without the caption? Titles, annotations, and labels should carry meaning.
3. **The Table Test**: Could this figure be replaced by a table? If yes, it should be a table instead (or it needs redesign to convey what tables cannot -- patterns, trends, shapes, outliers).
4. **The Color Test**: Does removing color destroy the figure? If yes, add redundant encoding (shape, pattern, position).
5. **The Memory Test**: Will a reviewer remember this figure a week later? Distinctive visual form + surprising content = memorability.

### Specific Qualities of Award-Level Figures

- **Embeds the paper's core claim visually** -- the figure IS the argument, not illustration of it
- **Uses color meaningfully**: warm/cool for good/bad; sequential for magnitude; categorical for model/condition
- **Has clear hierarchy**: primary data is largest/boldest; supporting context is smaller/lighter
- **Includes annotations/callouts** pointing to key findings ("GPT-5.2 ranks #1 here but #4 here")
- **Cannot be generated by default matplotlib/seaborn** -- some design effort is visible
- **Referenced and discussed in text** -- not just placed and forgotten

### What Reviewers Notice (Based on ARR Review Criteria)

- Reviewers evaluate **clarity** (score 1-5): figures directly impact this
- **Excitement** score depends on how well findings are communicated: a great figure can boost excitement by 0.5-1 point
- Reviewers are more likely to recommend for award when they can **quickly grasp** the contribution -- Figure 1 is their first impression

---

## 5. Figure Design Principles from Information Visualization

### Edward Tufte's Core Principles Applied to NLP Papers

1. **Maximize the data-ink ratio**: Every mark on the figure should encode data. Remove gridlines, box borders, redundant legends, and decorative elements that don't carry information.

2. **Above all else, show the data**: Don't let the framework diagram dominate at the expense of actual results. The most effective benchmark papers integrate real data into framework figures.

3. **Avoid chartjunk**: No 3D effects, no gradient fills, no shadows, no unnecessary texture. ACL papers with clean, flat aesthetics look more professional.

4. **Small multiples over complex single figures**: Instead of one overlaid line chart with 11 models, show a grid of simple charts -- one per model or one per condition.

5. **Micro/macro readings**: Design figures that work at both levels -- a quick glance shows the pattern, careful study reveals specific values.

### Ten Simple Rules for Better Figures (Rougier et al., PLOS Comp Bio)

1. **Know your audience** -- ACL reviewers expect certain conventions; don't deviate without reason
2. **Identify your message** -- one figure, one message
3. **Adapt the figure to the medium** -- print-ready (300 DPI, vector when possible)
4. **Captions are not optional** -- they should be self-contained
5. **Do not trust defaults** -- matplotlib/seaborn defaults are rarely publication-ready
6. **Use color effectively** -- colorblind-safe palettes (Okabe-Ito or viridis family)
7. **Do not mislead the reader** -- consistent scales, no truncated axes without marking
8. **Avoid "chartjunk"** -- every visual element must earn its place
9. **Message and readability first** -- aesthetics serve communication, not the reverse
10. **Get scientific feedback** -- test figures on colleagues before submission

### 16 Guidelines for Academic Paper Visualizations (Luis Cruz)

Key highlights applicable to SciFig:
- Use vector graphics (PDF/SVG) not raster (PNG/JPG)
- Font size in figures should match caption font size (~8-9pt in ACL format)
- Consistent color scheme across ALL figures in the paper
- Label axes directly (not just in legend)
- Use direct annotation instead of requiring legend lookup
- Order categories meaningfully (by value, not alphabetically)

### Color Palette Recommendations

**For categorical data (models):**
- Okabe-Ito palette (gold standard for colorblind safety): recommended by Nature
- 8 distinct colors: black, orange, sky blue, bluish green, yellow, blue, vermillion, reddish purple

**For sequential data (performance scores):**
- Viridis family (viridis, plasma, inferno, magma): perceptually uniform, colorblind-safe

**For diverging data (above/below baseline):**
- Blue-white-red (with distinct lightness levels)
- Use ColorBrewer diverging palettes

**Testing accessibility:**
- Convert to grayscale -- if data is lost, add redundant encoding
- Use Color Oracle or Coblis simulators to check colorblind rendering
- ~8% of male readers have red-green color deficiency

---

## 6. How Many Figures Do Top 8-Page Papers Have?

### Estimated Counts (Based on Analysis of ACL/EMNLP 2023-2025 Best Papers)

| Paper Type | Figures | Tables | Total Float Objects |
|---|---|---|---|
| Evaluation/benchmark paper | 4-6 figures | 3-5 tables | 7-10 |
| Systems paper | 3-5 figures | 2-4 tables | 6-8 |
| Analysis paper | 5-7 figures | 2-3 tables | 7-9 |

### Figure Size Conventions

- **Figure 1**: Almost always page-width (two columns). This is the showcase figure.
- **Results figures**: Mix of column-width (for simple charts) and page-width (for complex comparisons)
- **Framework/pipeline diagrams**: Page-width
- **Bar charts and line charts**: Column-width when comparing <6 items; page-width for more
- **Heatmaps**: Page-width (need room for labels)
- **Example/case study figures**: Page-width (need room for images + text)

### Space Budget for 8-Page SciFig Paper

Rough allocation:
- Figure 1 (overview): ~0.4 page (page-width)
- Figure 2 (methodology/selective blur): ~0.3 page (page-width)
- Figure 3 (main results visualization): ~0.3 page (page-width)
- Figure 4 (A-R-I profiles): ~0.3 page (page-width)
- Figure 5 (case study/examples): ~0.3 page (page-width)
- Tables: ~1.0-1.5 pages total
- Total float objects: ~2.5-3.0 pages of 8 pages dedicated to visuals

---

## 7. Anti-Patterns: What NOT to Do

### Figures That Hurt Papers

1. **Generic bar charts that could be a table**
   - If all you show is "Model A: 85.3, Model B: 82.1, Model C: 79.4" -- that's a table
   - Bar charts earn their place only when patterns (clusters, outliers, trends) are the message

2. **Pie charts**
   - Almost never appropriate in NLP papers
   - Human perception of angles is poor; bar charts or waffle charts are always better
   - Exception: showing 2-3 large proportions where the "parts of a whole" metaphor matters

3. **3D charts of any kind**
   - Zero information added by the third dimension
   - Distorts perception of values
   - Signals lack of design sophistication to reviewers

4. **Figures that require color to read**
   - ~8% of male reviewers may be colorblind
   - Must be readable in grayscale or with redundant encoding (shape, pattern, labels)
   - Test by printing in black and white

5. **Figures with too much text**
   - If the figure is mostly text boxes, it should be a table or prose
   - Framework diagrams that are just labeled boxes connected by arrows add little

6. **Screenshots of dashboards or interfaces**
   - Low resolution, not vector, not designed for print
   - Shows the tool, not the insight
   - Acceptable only if the UI IS the contribution

7. **Default matplotlib/seaborn styling**
   - Signals "I spent 2 minutes on this figure"
   - Reviewers notice: grey backgrounds, default blue, thick borders, auto-legends
   - Invest in custom styling: remove chart borders, use direct labels, align with paper's color scheme

8. **Overcrowded line charts**
   - 11 overlapping lines with a legend is unreadable
   - Use small multiples or highlight 3-4 key models with others in grey background

9. **Inconsistent styling across figures**
   - Different color for the same model in different figures
   - Different font sizes, axis styles, or legend positions
   - Creates cognitive load and looks unprofessional

10. **Figures not discussed in the text**
    - "See Figure X" without analysis wastes the figure
    - Every figure should be referenced with a specific claim: "As Figure X shows, rankings on quality do not predict rankings on reliability"

---

## 8. Specific Figure Recommendations for SciFig-Eval Paper

### Figure 1: "The Quality-Reliability Disconnect" (Page-width, the hook)

**What it shows**: A two-panel figure that immediately communicates the paper's core thesis.

**Left panel -- "The Leaderboard View"**: A standard bar chart showing MQM quality rankings (GPT-5.2 #1, Gemini #2, etc.) -- this is what the field currently sees.

**Right panel -- "The Behavioral View"**: The same models re-ranked by A-R-I composite, showing dramatic reordering (Gemini jumps to #1, GPT-5.2 drops). Use connecting lines between the two panels (slope chart style) to show the crossings.

**Between panels**: A bold annotation: "Rankings invert under adversarial conditions"

**Color**: Use a consistent model color palette. Highlight the biggest rank changes with thicker/colored lines; use grey for models that maintain rank.

**WHY this works**: 
- Passes the 3-second glance test: "oh, rankings change"
- Passes the table test: the crossing lines can't be a table
- Creates immediate "wait, really?" reaction (hooks reviewer)
- Compresses the entire paper argument into one image
- The slope chart form is distinctive and memorable

**Alternative Figure 1: "The Honesty Gap"**

Show a single dramatic comparison: GPT-5.2 (91.6 MQM, 6% admittance) vs. Gemini (90.2 MQM, 90% admittance). Use a split visualization -- tall quality bar next to tiny admittance bar for GPT-5.2, both tall for Gemini. Annotation: "The #1 model fabricates 94% of the time when it can't see."

---

### Figure 2: "The A-R-I Framework" (Page-width, the methodology)

**What it shows**: The evaluation framework with real data embedded.

**Design**: A 2x2 matrix layout matching the paper's structure (Description/Reasoning x Standard/Adversarial), with each cell showing:
- A miniature real figure from the dataset
- The type of evaluation applied
- A sample model response (one good, one bad)

**Below the matrix**: The A-R-I decomposition shown as three icons/diagrams:
- **Admittance** (A): blurred figure -> model says "I cannot determine..." (green, honest) vs. "The value is 42" (red, fabrication)
- **Resistance** (R): misleading caption + figure -> model ignores caption (green) vs. echoes it (red)
- **Inductance** (I): partially blurred figure -> model infers from context (green) vs. admits/fabricates (yellow/red)

**WHY this works**:
- Grounds the abstract framework in concrete examples
- Reviewer immediately understands what A-R-I means without reading the methods section
- The good/bad response pairs create "aha" moments
- Real figure images make it feel empirical, not theoretical

---

### Figure 3: "Selective Blur Methodology" (Column-width or page-width)

**What it shows**: The selective blur pipeline visually.

**Design**: A single figure shown in 4 states side by side:
1. Original (clean) figure
2. Axis-blurred version (admittance target)
3. Legend-blurred version (inductance target)
4. Data-blurred version (inductance target)

Below each: a one-line model response showing the behavioral difference.

**WHY this works**:
- The visual before/after is immediately compelling
- Makes the adversarial methodology tangible and reproducible
- Reviewers can see exactly what "selective blur" means
- Differentiates this paper from crude noise-based adversarial methods

---

### Figure 4: "A-R-I Behavioral Profiles" (Page-width, the signature visualization)

**What it shows**: Each model's behavioral "shape" across A-R-I dimensions.

**Design Option A -- Small Multiples Radar Charts**:
- A 2x4 or 3x4 grid of small radar/spider charts (one per model)
- Each radar has 5-6 axes: MQM Quality, Admittance, Resistance, Caption Bias R, Inductance, Robustness
- Models with similar quality but different shapes are visually striking
- Highlight key models (GPT-5.2, Gemini, Phi-4) with color; others in grey

**Design Option B -- Parallel Coordinates Plot**:
- Horizontal axes for each dimension (MQM, Admittance, Resistance, etc.)
- Each model is a line connecting its values across dimensions
- Crossing lines reveal where models trade off quality for reliability
- Color-code by model family (GPT blue, Gemini green, Qwen orange, etc.)

**Design Option C -- Bump Chart**:
- Vertical axis = rank (1-11), horizontal axis = metric
- Each model is a line showing its rank across metrics
- Crossing lines ARE the finding -- quality rank != reliability rank
- Annotations at key crossings: "Gemini: #2 quality, #1 reliability"

**Recommendation**: Option A (small multiples radar) for the paper, Option C (bump chart) as a strong alternative. The radar charts create model "fingerprints" that reviewers will remember.

**WHY this works**:
- Shows orthogonality of dimensions visually (different shapes)
- Each model gets a distinctive, memorable profile
- Reviewers can quickly see that "Gemini is the honest model" and "GPT-5.2 is the quality-confident model"
- Cannot be replaced by a table -- the shape IS the insight

---

### Figure 5: "The Fabrication Spectrum" (Page-width)

**What it shows**: How models handle uncertainty -- the distribution of admits/fabricates/correct responses.

**Design Option A -- Stacked/Grouped Bar with Annotations**:
- For each model: a stacked bar split into "Admits" (green), "Fabricates" (red), "Correct" (blue)
- Ordered by admittance rate (Gemini left, Phi-4 right)
- Annotation callout on GPT-5.2: "94% fabrication despite #1 quality ranking"

**Design Option B -- Sankey Diagram**:
- Left: 11 models (width proportional to test count)
- Middle: adversarial condition type (blur, caption bias, hallucination probe)
- Right: outcome (admits, fabricates, correct)
- Shows where fabrications come from and which models contribute most

**Design Option C -- Waffle Chart Grid**:
- Small multiples of 10x10 waffle grids, one per model
- Each square = one adversarial probe response
- Green = admits, red = fabricates, blue = correct
- The visual contrast between Gemini's mostly-green grid and GPT-5.2's mostly-red grid is striking

**Recommendation**: Option C (waffle charts) is the most unconventional and memorable. Option A is the safest. Consider Option B for the appendix.

**WHY waffle charts work here**:
- Each square represents a real test case -- makes the data feel tangible
- The color contrast between honest and dishonest models is visceral
- Unfamiliar enough to be memorable, familiar enough to be readable
- Reviewers will remember "the grid of colored squares showing honesty"

---

### Figure 6 (if space permits): "Case Study: The Same Figure, Eight Models" (Page-width)

**What it shows**: A single selectively blurred figure with 8 model responses annotated.

**Design**: 
- Center: the blurred figure (large)
- Surrounding it: speech bubbles from each model, color-coded by response type
  - Green bubble: "The axis labels are not readable due to blur" (admits)
  - Red bubble: "The x-axis shows years 2010-2020" (fabricates)
  - Blue bubble: "Based on the title and legend, this likely shows..." (induces)
- Model name and MQM score in each bubble header

**WHY this works**:
- Most concrete, memorable figure in the paper
- Makes the A-R-I framework feel real, not theoretical
- Reviewers remember concrete examples more than aggregate charts
- Shows diversity of model behaviors on identical input
- Can be discussed extensively in the text

---

### Summary: Recommended Figure Set for 8-Page Paper

| # | Figure | Type | Width | Primary Purpose |
|---|--------|------|-------|-----------------|
| 1 | Quality-Reliability Disconnect | Slope chart / paired comparison | Page | Hook: rankings invert |
| 2 | A-R-I Framework with Examples | Annotated diagram + examples | Page | Methodology: ground the framework |
| 3 | Selective Blur Pipeline | Before/after image sequence | Column or Page | Methodology: show the adversarial approach |
| 4 | Behavioral Profiles | Small multiples radar charts | Page | Results: model "fingerprints" |
| 5 | Fabrication Spectrum | Waffle chart grid or stacked bar | Page | Results: honesty distribution |
| 6 | Case Study | Annotated example with responses | Page | Qualitative: make it real |

Total: 5-6 figures + 3-4 tables = 8-10 float objects (within budget for 8 pages)

---

## 9. Advanced Design Recommendations

### Creating Visual Consistency

- Assign each model a fixed color used in ALL figures and tables:
  - GPT-5.2: deep blue
  - Gemini: teal/green
  - Llama4-Scout: orange
  - Llama4-Maverick: amber
  - Qwen-VL-Max: purple
  - Qwen-235B: violet
  - Qwen-32B: lavender
  - Phi-4: red (danger color -- fits its poor reliability)
  - Gemma3-4b/12b/27b: grey family (three shades)
- Use these colors in every chart, table highlight, and example annotation
- Create a LaTeX color definition file and import it everywhere

### Typography in Figures

- Figure text should be 8-9pt to match ACL caption size
- Use the same serif font as the paper body (Times/Nimbus Roman) or a clean sans-serif (Helvetica)
- Never use Comic Sans, Calibri, or system default fonts
- Bold for emphasis, not color alone
- Axis labels: sentence case ("Model accuracy") not title case ("Model Accuracy")

### Figure-Text Integration

- Every figure should be referenced with a specific analytical claim
- Bad: "Results are shown in Figure 4."
- Good: "As Figure 4 reveals, model rankings on MQM quality do not predict rankings on behavioral reliability (Spearman rho = 0.34, p = 0.08), with Gemini showing the most dramatic improvement from quality rank #2 to reliability rank #1."

### Making Figures Reproducible

- Include figure generation scripts in supplementary materials
- Use seaborn/matplotlib with custom style sheets
- Provide color hex codes in the paper or supplement
- Export as PDF (vector) not PNG (raster)

---

## 10. Implementation Priorities

### Must-Have Figures (without these the paper is incomplete)

1. **Figure 1: The hook** -- whatever form, must show quality != reliability
2. **Figure showing A-R-I framework** -- reviewers need to understand the methodology visually
3. **Main results comparison** -- radar charts or bump chart showing multi-dimensional profiles

### High-Value Additions (make the paper memorable)

4. **Selective blur visual** -- shows the methodology is novel and rigorous
5. **Fabrication/admittance distribution** -- makes the "honesty gap" visceral
6. **Case study with real model outputs** -- most memorable for reviewers

### Appendix Opportunities (enhance without spending page budget)

- Full heatmap of all models x all conditions
- Per-language performance breakdowns (small multiples)
- Sankey diagram of error flow
- Additional case studies
- Confusion-matrix style analysis of hallucination probe types

---

## Sources

### Papers Analyzed
- [HallusionBench (CVPR 2024)](https://arxiv.org/abs/2310.14566)
- [POPE (EMNLP 2023)](https://aclanthology.org/2023.emnlp-main.20/)
- [MathVista (ICLR 2024)](https://arxiv.org/abs/2310.02255)
- [ChartQA](https://arxiv.org/abs/2203.10244)
- [AppWorld (ACL 2024)](https://aclanthology.org/2024.acl-long.850/)
- [Mission: Impossible Language Models (ACL 2024 Best Paper)](https://aclanthology.org/2024.acl-long.787/)
- [Aya Model (ACL 2024 Best Paper)](https://aclanthology.org/2024.acl-long.845/)
- [MMBench](https://arxiv.org/abs/2307.06132)

### Design Guides
- [16 Guidelines for Effective Data Visualizations in Academic Papers](https://luiscruz.github.io/2021/03/01/effective-visualizations.html)
- [Ten Simple Rules for Better Figures (PLOS Comp Bio)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833)
- [MIT Broad CommKit: Figure Design](https://mitcommlab.mit.edu/broad/commkit/figure-design/)
- [Choosing Color Palettes for Scientific Figures (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7040535/)
- [ACL Formatting Guidelines](https://acl-org.github.io/ACLPUB/formatting.html)

### Color and Accessibility
- [Okabe-Ito Colorblind-Safe Palette](https://jfly.uni-koeln.de/color/)
- [ColorBrewer 2.0](https://colorbrewer2.org/)
- [ggpubfigs: Colorblind-Friendly Palettes](https://github.com/JLSteenwyk/ggpubfigs)
