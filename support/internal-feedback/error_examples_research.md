# MQM Error Examples Research — Landscape Appendix Table

Concrete error examples extracted from atomic MQM evaluation outputs.
Judge: `azure/gpt-4o` unless noted otherwise. All examples from English figures.

---

## 1. Incorrect Numerical Value

### Example 1a — gemini-3.1-pro on english_fig_001
- **Figure**: english_fig_001 (Pie Chart — AttentionInfluence clustering)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "The left chart contains 22 total slices (6 inner and 16 outer)."
- **Ground truth**: The left chart has 6 inner slices and 15 outer slices, totaling 21 slices.
- **Atom**: english_fig_001_sent_1

### Example 1b — gemma3-27b-it on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemma3-27b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "'Health & Medicine' (pink, approximately 22%)"
- **Ground truth**: The FineWeb-Edu Classifier chart shows Health & Medicine as 19%, not 22%.
- **Atom**: english_fig_001_sent_6

### Example 1c — gemma3-12b-it on english_fig_005
- **Figure**: english_fig_005 (Line Plot)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/mistral-large-3
- **Model said**: "begins at approximately 0.36 at x = 2^0"
- **Ground truth**: The Llama-3B line starts around 0.42, not 0.36.

### Example 1d — gemma3-12b-it on english_fig_003
- **Figure**: english_fig_003 (Line Plot — quantized pruning)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "starts at approximately -2% at Layer1-4 and declines to approximately -13% at Layer29-32"
- **Ground truth**: The yellow line (LB-Avg of 2x tokens, 8-bit) starts near 0% and maintains a consistent trend near 0% across all layers — it does not decline to -13%.

### Example 1e — gemini-3.1-pro on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: gpt-4o (ref+img)
- **Model said**: "materials (pink, 2%)"
- **Ground truth**: Materials (pink) is 3%, not 2%.

---

## 2. Fabrication / Hallucination

### Example 2a — gemma3-12b-it on english_fig_031
- **Figure**: english_fig_031 (Bar Chart)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "visual emphasis is applied to certain bars denoted by a small icon, such as a circle, triangle, or square"
- **Ground truth**: The figure does not show any visual emphasis icons like circles, triangles, or squares.

### Example 2b — qwen3-vl-30b-a3b on english_fig_004
- **Figure**: english_fig_004 (Line Plot)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "when applying layer-wise quantized pruning using the SnapKV method, with a KV cache budget of 1/64"
- **Ground truth**: The figure does not mention SnapKV, quantized pruning, or KV cache budget. Entirely fabricated terminology.

### Example 2c — gemma3-12b-it on english_fig_120
- **Figure**: english_fig_120 (Bar Chart)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "Three sets of bars are displayed for each method; each set is differentiated by color: orange, light blue, and gray"
- **Ground truth**: The figure only shows two sets of bars (light blue and light orange). There are no gray bars.

### Example 2d — llama4-scout on english_fig_019
- **Figure**: english_fig_019 (Pie Chart)
- **Model**: llama4-scout
- **Severity**: Major
- **Judge**: gpt-4o (ref+img)
- **Model said**: "There are percentage labels inside some of the slices"
- **Ground truth**: There are no percentage labels inside the slices.

### Example 2e — gemma3-4b-it on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemma3-4b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "The slices appear to be ordered from largest to smallest in terms of their angular size."
- **Ground truth**: The slices are not ordered from largest to smallest; they are arranged by category.

### Example 2f — gemini-3.1-pro on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/mistral-large-3
- **Model said**: "and a small cyan slice labeled with an ellipsis (...)"
- **Ground truth**: There is no cyan slice or ellipsis in the FineWeb-Edu Classifier chart.

### Example 2g — gemma3-12b-it on english_fig_002
- **Figure**: english_fig_002 (Pie Chart)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/mistral-large-3
- **Model said**: "includes a legend identifying each category"
- **Ground truth**: The figure does not contain a legend.

---

## 3. Omission (Missing Visual Features / Missing Chart Purpose / Missing Axis Description)

### Example 3a — gemma3-27b-it on english_fig_001 (Missing Visual Features)
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemma3-27b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: [nothing — omitted entirely]
- **What was missed**: The description does not mention the AttentionInfluence chart at all (one of the two main pie charts in the figure).
- **Atom**: english_fig_001_sent_1

### Example 3b — qwen3-vl-30b-a3b on english_fig_033 (Missing Visual Features)
- **Figure**: english_fig_033 (Line Plot)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: [nothing — omitted]
- **What was missed**: The description does not mention the red line with triangular markers representing "IKE" — one of six methods in the figure.

### Example 3c — qwen3-vl-30b-a3b on english_fig_029 (Missing Axis Description)
- **Figure**: english_fig_029 (Line Plot)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: [nothing — omitted]
- **What was missed**: The description does not mention the x-axis label "Number of Frames".

### Example 3d — qwen3-vl-30b-a3b on english_fig_029 (Missing Chart Purpose)
- **Figure**: english_fig_029 (Line Plot)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: [nothing — omitted]
- **What was missed**: The description does not mention that the plot illustrates accuracy percentage as a function of the number of frames across four different methods.

### Example 3e — gemini-3.1-pro on english_fig_003 (Missing Chart Purpose)
- **Figure**: english_fig_003 (Line Plot)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: gpt-4o (ref+img)
- **Model said**: [nothing — omitted]
- **What was missed**: The description does not mention the purpose of illustrating quantized pruning on Llama-3-8B-Instruct.

---

## 4. Incorrect Label/Legend

### Example 4a — qwen3-vl-30b-a3b on english_fig_120
- **Figure**: english_fig_120 (Bar Chart)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "a light blue bar representing the average score ('Avg') and an orange bar representing the score for a subset ('Avg_sub')"
- **Ground truth**: The legend labels are "AvgObj" and "AvgSub", not "Avg" and "Avg_sub".

### Example 4b — qwen3-vl-30b-a3b on english_fig_120
- **Figure**: english_fig_120 (Bar Chart)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "A dashed blue line at 64.71 represents the 'Base Avg_6by' baseline, and a dashed yellow line at 37.91 represents the 'Base Avg_5by'"
- **Ground truth**: The dashed lines are labeled "Base AvgObj" and "Base AvgSub", not "Base Avg_6by" and "Base Avg_5by".

### Example 4c — gemma3-27b-it on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemma3-27b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "'Education' (yellow, approximately 38%)"
- **Ground truth**: Education is green, not yellow. (Combines label-color mapping error.)
- **Atom**: english_fig_001_sent_6

### Example 4d — gemini-3.1-pro on english_fig_001
- **Figure**: english_fig_001 (Pie Chart)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "cyan Fin & Law 3"
- **Ground truth**: The "Fin & Law" category is blue, not cyan.

### Example 4e — gemini-3.1-pro on english_fig_002
- **Figure**: english_fig_002 (Pie Chart)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: gpt-4o (ref+img)
- **Model said**: "a light blue slice representing Universal Quantifiers (29.07%)"
- **Ground truth**: Universal Quantifiers is light grey, not light blue.

### Example 4f — gemma3-12b-it on english_fig_006
- **Figure**: english_fig_006 (Line Plot)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "with tick labels incrementing by 1"
- **Ground truth**: The x-axis tick labels increment by powers of two, not by 1.

### Example 4g — gemini-3.1-pro on english_fig_029
- **Figure**: english_fig_029 (Line Plot)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "features a linear scale encompassing a data range from 8 to 64"
- **Ground truth**: The x-axis range is from 10 to 60, not 8 to 64.

---

## 5. Incorrect Trend/Relationship

### Example 5a — gemini-3.1-pro on english_fig_006
- **Figure**: english_fig_006 (Line Plot)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "remains flat to 2^1"
- **Ground truth**: The green line shows a consistent upward trend from (1, 0.42) to (256, 0.6) without a flat segment.

### Example 5b — gemma3-12b-it on english_fig_003
- **Figure**: english_fig_003 (Line Plot — layer groupings)
- **Model**: gemma3-12b-it
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "begins at approximately -1% at Layer1-4, decreases to approximately -15% at Layer29-32"
- **Ground truth**: The dark blue line (RULER4k of 1x tokens, 16-bit) starts near -2%, drops to -15% at Layer13-20, then increases back to around -2% at Layer29-32. The model describes a monotonic decrease when the line actually recovers.

### Example 5c — qwen3-vl-30b-a3b on english_fig_171
- **Figure**: english_fig_171 (Line Plot — training rewards)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "The Llama-On-Policy-Easy (teal line) and Llama-LUFFY-Easy (red line) models show similar trends"
- **Ground truth**: The trends are not similar; Llama-LUFFY-Easy achieves higher rewards and exhibits more variability.

### Example 5d — qwen3-vl-32b on english_fig_006
- **Figure**: english_fig_006 (Line Plot)
- **Model**: qwen3-vl-32b
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "Both lines show a positive trend, with the dark blue line consistently achieving higher accuracy than the light green line across all values of k."
- **Ground truth**: The description oversimplifies — there are four lines in the plot, not two. The relationship between lines is more nuanced.

### Example 5e — qwen3-vl-235b-a22b on english_fig_033
- **Figure**: english_fig_033 (Line Plot — co-occurrence vs accuracy)
- **Model**: qwen3-vl-235b-a22b
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "all methods generally show an upward trend in accuracy"
- **Ground truth**: The Base method plateaus at higher co-occurrence levels, contradicting a "general upward trend."

### Example 5f — gemini-3.1-pro on english_fig_038
- **Figure**: english_fig_038 (Line Plot — training loss)
- **Model**: gemini-3.1-pro
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "rapidly declines through the axis break to roughly 0.25 by 10k steps"
- **Ground truth**: The red line does not reach 0.25 by 10k steps; it decreases hyperbolically but remains above 0.4.

---

## 6. Clarity/Fluency

### Example 6a — Ambiguous Description — qwen3-vl-30b-a3b on english_fig_009
- **Figure**: english_fig_009 (Nested Pie Chart)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "dark light blue for Max: 1, medium light blue for Max: 2, and very light blue for Max: 3."
- **Problem**: Uses unclear terminology ("dark light blue", "medium light blue") that would confuse readers.

### Example 6b — Poor Sentence Structure — llama4-scout on english_fig_120
- **Figure**: english_fig_120 (Bar Chart)
- **Model**: llama4-scout
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "with an additional annotation of 37.91 for DEITA's red bar and 64.71 for DEITA's blue bar."
- **Problem**: The phrasing incorrectly associates reference line values with specific bars, creating ambiguity.

### Example 6c — Poor Sentence Structure — phi-4-multimodal on english_fig_075
- **Figure**: english_fig_075 (Bar Chart)
- **Model**: phi-4-multimodal
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "The bar chart is designed to compare the effect size of different classifiers"
- **Problem**: Awkward phrasing; "effect size" is not explicitly defined and could be clearer.

### Example 6d — Overly Verbose — gpt-5.2 on english_fig_029
- **Figure**: english_fig_029 (Line Plot)
- **Model**: gpt-5.2
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "stays near 53.8--53.9% at 32 frames and about 53.7--53.8% at 64 frames"
- **Problem**: Excessive detail about minor variations (0.1% differences) that are not visually distinguishable in the plot.

### Example 6e — Overly Verbose — gpt-5.2 on english_fig_033
- **Figure**: english_fig_033 (Line Plot)
- **Model**: gpt-5.2
- **Severity**: Minor
- **Judge**: azure/gpt-4o
- **Model said**: "The Base series is a black solid line with circular markers, increasing from about 38.4% at the smallest co-occurrence value..."
- **Problem**: Provides excessive numerical detail for each data point, unnecessary for understanding the overall trend.

### Example 6f — Unwanted Interpretation — qwen3-vl-30b-a3b on english_fig_011
- **Figure**: english_fig_011 (Pie Chart — stimulus types)
- **Model**: qwen3-vl-30b-a3b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "illustrates the distribution of various input stimulus material types provided by journalists to large language models (LLMs) in the context of WildChat conversations matched to online articles"
- **Problem**: Introduces interpretation about journalists, LLMs, and WildChat conversations not supported by the figure.

### Example 6g — Unwanted Interpretation — qwen3-vl-235b-a22b on english_fig_026
- **Figure**: english_fig_026 (Pie/Bar Chart — language distribution)
- **Model**: qwen3-vl-235b-a22b
- **Severity**: Major
- **Judge**: azure/gpt-4o
- **Model said**: "The visual emphasizes the dominance of English and Spanish, with the remaining languages contributing relatively minor shares."
- **Problem**: Introduces subjective interpretation about "dominance" not explicitly shown in the figure.

---

## Summary of Models and Error Distribution

| Error Sub-type | Models with examples | Best example for table |
|---|---|---|
| Incorrect Numerical Value | gemini-3.1-pro, gemma3-27b-it, gemma3-12b-it | 1b (22% vs 19%) or 1e (2% vs 3%) |
| Fabrication/Hallucination | gemma3-12b-it, qwen3-vl-30b-a3b, llama4-scout, gemma3-4b-it, gemini-3.1-pro | 2b (SnapKV fabrication) or 2a (fabricated icons) |
| Omission | gemma3-27b-it, qwen3-vl-30b-a3b, gemini-3.1-pro | 3a (entire chart omitted) |
| Incorrect Label/Legend | qwen3-vl-30b-a3b, gemma3-27b-it, gemini-3.1-pro, gemma3-12b-it | 4a (AvgObj/AvgSub misread) or 4c (yellow vs green) |
| Incorrect Trend/Relationship | gemini-3.1-pro, gemma3-12b-it, qwen3-vl-30b-a3b, qwen3-vl-32b, qwen3-vl-235b-a22b | 5b (monotonic decrease vs recovery) |
| Clarity/Fluency | qwen3-vl-30b-a3b, llama4-scout, phi-4-multimodal, gpt-5.2, qwen3-vl-235b-a22b | 6a ("dark light blue") or 6d (0.1% precision) |

## Notes for Appendix Table Construction

- All errors sourced from `output/evaluation/atomic_mqm/azure/gpt-4o/` and `output/evaluation/reference_with_image/gpt-4o/`.
- Ground truth descriptions in `Dataset/groundtruth/english_only/`.
- Atom checklists in `atomic_mqm/atoms/`.
- For the landscape table, recommend picking one clear example per sub-type that is short enough to fit in a table cell (max ~40 words per cell).
- Recommended picks for conciseness: 1e, 2a, 3b, 4c, 5a, 6a.
