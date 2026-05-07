# Chinese Atom Review

## Figures with Issues

### chinese_fig_012
- **Issue**: Minor completeness gap -- groundtruth contains the claim "从epoch=2起F1值为约0.82" for FLAT method, which is not captured as a separate atom. The atom only captures "epoch = 2：F1 ≈ 0.78". The groundtruth itself is internally inconsistent (0.82 vs 0.78 for the same epoch), but the initial FLAT value claim is unatomized.
- **Fix needed**: Add an atom for the FLAT initial value claim, e.g. `{"id": "flat_initial_f1", "severity": "important", "value": "从epoch=2起F1值为约0.82"}`, or add a `note` field documenting the groundtruth internal inconsistency (similar to chinese_fig_069/070/119 pattern).

### chinese_fig_014
- **Issue**: Language fidelity / fabrication -- atom `chart_type` has value "折线图" but the groundtruth annotation text says "图表展示了不同参数..." not "折线图展示了...". The word "折线图" does not appear anywhere in the groundtruth annotation. This is a fabricated atom value inferred from the metadata figure_type ("Line Plot") rather than quoted from the annotation text.
- **Fix needed**: Change `chart_type` value from "折线图" to "图表" to match the groundtruth wording (consistent with the approach used in chinese_fig_039, chinese_fig_133, chinese_fig_140 which all faithfully use "图表" when that is what the groundtruth says). Alternatively, if "折线图" is preferred for evaluation accuracy, add a `note` field explaining the deviation from groundtruth wording.

### chinese_fig_039
- **Issue**: Atom `chart_type` has value "图表" which is generic. The groundtruth text itself uses "该图表展示了..." so this is faithful, but the figure is clearly a line chart with two lines and markers. Other line chart atoms in this set use "线图" or "折线图".
- **Fix needed**: Consider changing `chart_type` value to "线图" for consistency with other Chinese line chart atoms (e.g., chinese_fig_035, chinese_fig_015). Low priority since the groundtruth wording is generic.

### chinese_fig_133
- **Issue**: Same as chinese_fig_039 -- atom `chart_type` has value "图表" (generic) rather than "线图" or "折线图". Faithful to groundtruth wording "这个图表展示了..." but inconsistent with other line chart atoms in the set.
- **Fix needed**: Consider changing to "线图" or "折线图" for consistency. Low priority.

### chinese_fig_140
- **Issue**: Same as chinese_fig_039/133 -- atom `chart_type` has value "图表" matching the groundtruth's generic wording. Inconsistent with other line chart atoms.
- **Fix needed**: Consider changing to "线图" for consistency. Low priority.

## Figures Passing

### chinese_fig_004
- Type: bar_chart | Atoms: 12 | Status: PASS

### chinese_fig_009
- Type: bar_chart | Atoms: 23 | Status: PASS

### chinese_fig_010
- Type: pie_chart | Atoms: 16 | Status: PASS

### chinese_fig_013
- Type: pie_chart | Atoms: 16 | Status: PASS

### chinese_fig_015
- Type: line_plot | Atoms: 18 | Status: PASS

### chinese_fig_019
- Type: bar_chart | Atoms: 13 | Status: PASS

### chinese_fig_035
- Type: line_plot | Atoms: 24 | Status: PASS

### chinese_fig_042
- Type: bar_chart | Atoms: 22 | Status: PASS

### chinese_fig_045
- Type: bar_chart | Atoms: 20 | Status: PASS

### chinese_fig_046
- Type: line_plot | Atoms: 28 | Status: PASS

### chinese_fig_053
- Type: bar_chart | Atoms: 15 | Status: PASS

### chinese_fig_061
- Type: bar_chart | Atoms: 15 | Status: PASS

### chinese_fig_069
- Type: pie_chart | Atoms: 24 | Status: PASS (note field documents groundtruth anomaly: left pie claims 10 categories but lists 8)

### chinese_fig_070
- Type: pie_chart | Atoms: 28 | Status: PASS (note field documents groundtruth anomaly: left pie claims 8 slices but lists 6, right pie percentages sum to 84.07%)

### chinese_fig_071
- Type: bar_chart | Atoms: 17 | Status: PASS

### chinese_fig_072
- Type: bar_chart | Atoms: 17 | Status: PASS

### chinese_fig_077
- Type: bar_chart | Atoms: 27 | Status: PASS

### chinese_fig_094
- Type: pie_chart | Atoms: 11 | Status: PASS

### chinese_fig_116
- Type: pie_chart | Atoms: 10 | Status: PASS

### chinese_fig_119
- Type: pie_chart | Atoms: 13 | Status: PASS (note field documents groundtruth anomaly: claims 7 slices but lists 8, percentages sum to 132.5%)

### chinese_fig_120
- Type: pie_chart | Atoms: 11 | Status: PASS

### chinese_fig_126
- Type: pie_chart | Atoms: 19 | Status: PASS

### chinese_fig_152
- Type: line_plot | Atoms: 18 | Status: PASS

### chinese_fig_154
- Type: line_plot | Atoms: 17 | Status: PASS

### chinese_fig_158
- Type: pie_chart | Atoms: 10 | Status: PASS

## Summary
- Total: 30
- Passing: 25
- Issues: 5 (1 completeness gap, 1 language fidelity/fabrication, 3 low-priority consistency items)

### Validation Details

**Completeness**: All groundtruth claims are atomized across all 30 files, with one minor exception (chinese_fig_012 FLAT initial value). Groundtruth anomalies in 3 files (069, 070, 119) are properly documented with `note` fields.

**Language Fidelity**: All atom values are in Chinese except where English terms (COVID-19, BLEU, F1, FLAT, lattice, OURS, Teacher, Self-Training, PST, TextCNN, etc.) appear identically in the Chinese groundtruth annotations. One exception: chinese_fig_014 uses "折线图" as chart_type but the groundtruth text says "图表" -- this is a fabricated value not present in the annotation text.

**Severity Validity**: All severity values are valid (critical/important/minor). Consistent pattern: critical for chart type/purpose/axis labels/series names; important for ranges/data values/trends; minor for colors/markers/styles/legend/ordering.

**JSON Validity**: All 30 files are valid, well-formed JSON.

**Value Types**: All atom values are strings (no booleans or numbers).

**Field Compliance**: All files contain only allowed fields (figure_key, figure_type, subfolder, language, reference_description, atoms). Three files use the optional `note` field (069, 070, 119). No extra fields detected.

**No Fabricated Atoms**: No atoms claim information not present in the groundtruth, with one borderline case: chinese_fig_014's chart_type value "折线图" is inferred from metadata rather than quoted from the annotation text.
