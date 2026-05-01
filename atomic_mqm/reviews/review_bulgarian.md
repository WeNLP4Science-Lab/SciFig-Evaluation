# Bulgarian Atom Review

## Figures with Issues

### bulgarian_fig_019
- **Issue**: reference_description field starts with Latin "C" (U+0043) instead of Cyrillic "С" (U+0421) -- "Cтълбовидната" vs "Стълбовидната". Atom values themselves are correct.
- **Fix needed**: Replace the leading Latin "C" in reference_description with Cyrillic "С".

### bulgarian_fig_021
- **Issue**: Category label atoms (category_1 through category_13) use severity "important", but equivalent category/label atoms in other files (fig_033, fig_035, fig_042) use severity "critical". This is an inconsistency across the Bulgarian atom set.
- **Fix needed**: Consider aligning severity to "critical" for category labels to match the pattern used in other Bulgarian atom files, or document the rationale for the difference.

## Figures Passing

### bulgarian_fig_001
- Type: line_plot | Atoms: 25 | Status: PASS

### bulgarian_fig_014
- Type: bar_chart | Atoms: 12 | Status: PASS

### bulgarian_fig_015
- Type: line_plot | Atoms: 16 | Status: PASS

### bulgarian_fig_031
- Type: line_plot | Atoms: 18 | Status: PASS

### bulgarian_fig_033
- Type: bar_chart | Atoms: 19 | Status: PASS

### bulgarian_fig_035
- Type: bar_chart | Atoms: 16 | Status: PASS

### bulgarian_fig_036
- Type: line_plot | Atoms: 18 | Status: PASS

### bulgarian_fig_038
- Type: pie_chart | Atoms: 22 | Status: PASS

### bulgarian_fig_042
- Type: bar_chart | Atoms: 20 | Status: PASS

### bulgarian_fig_048
- Type: bar_chart | Atoms: 15 | Status: PASS

### bulgarian_fig_049
- Type: line_plot | Atoms: 27 | Status: PASS

### bulgarian_fig_055
- Type: bar_chart | Atoms: 12 | Status: PASS

### bulgarian_fig_058
- Type: pie_chart | Atoms: 9 | Status: PASS

### bulgarian_fig_069
- Type: bar_chart | Atoms: 14 | Status: PASS

### bulgarian_fig_072
- Type: line_plot | Atoms: 21 | Status: PASS

### bulgarian_fig_073
- Type: bar_chart | Atoms: 15 | Status: PASS

### bulgarian_fig_087
- Type: pie_chart | Atoms: 9 | Status: PASS

### bulgarian_fig_088
- Type: line_plot | Atoms: 25 | Status: PASS

### bulgarian_fig_095
- Type: pie_chart | Atoms: 9 | Status: PASS

### bulgarian_fig_103
- Type: line_plot | Atoms: 15 | Status: PASS

### bulgarian_fig_119
- Type: line_plot | Atoms: 19 | Status: PASS

### bulgarian_fig_123
- Type: line_plot | Atoms: 14 | Status: PASS

### bulgarian_fig_130
- Type: pie_chart | Atoms: 11 | Status: PASS

### bulgarian_fig_140
- Type: pie_chart | Atoms: 11 | Status: PASS

### bulgarian_fig_162
- Type: pie_chart | Atoms: 8 | Status: PASS

### bulgarian_fig_250
- Type: pie_chart | Atoms: 10 | Status: PASS

### bulgarian_fig_255
- Type: pie_chart | Atoms: 11 | Status: PASS

### bulgarian_fig_272
- Type: pie_chart | Atoms: 8 | Status: PASS

## Summary
- Total: 30
- Passing: 28
- Issues: 2
- **Completeness**: All groundtruth sentences/claims are represented as atoms in all 30 files. No missing content.
- **Language fidelity**: All atom values are in Bulgarian, matching groundtruth text exactly. One mixed-script character found in reference_description of fig_019 (Latin C vs Cyrillic С), but atom values are unaffected.
- **Severity values**: All atoms use valid severities (critical/important/minor). One cross-file inconsistency noted in fig_021 where category labels use "important" while other files use "critical" for equivalent content.
- **JSON validity**: All 30 files parse correctly with well-formed JSON.
- **Value types**: All atom values are strings -- no booleans or numbers found.
- **Schema compliance**: All 30 files contain only the required fields: figure_key, figure_type, subfolder, language, reference_description, atoms. No extra fields (e.g., annotation_notes).
- **Fabricated atoms**: None detected. All atom values trace back to groundtruth annotation text.
- English terms in fig_038, fig_123, fig_255 are original figure labels from the charts, not translations.
