# English + Multi-Language Atom Review

## Figures with Issues

### english_fig_019
- **Issue**: Bad sentence split at sent_6/sent_7. sent_6 is `"Under Not Abusive slice, the next layer has \"Other."` and sent_7 starts `"\"Political\", \"Religious\"..."`. The split occurs mid-list at a period that follows `"Other"` in the GT text, creating a fragment that appears cut off.
- **Fix needed**: Merge sent_6 and sent_7 into a single atom to preserve the full sentence: `"Under Not Abusive slice, the next layer has \"Other. \"Political\", \"Religious\", \"Sexist\" and \"Racial\", with other having a bigger slice and followed by rest, and small slices for \"Sexist\" and \"Racial\"."`.

### english_fig_080
- **Issue**: Truncated atom value in `english_fig_080_bar_items_listed`. Value ends with `\"unperturbed` -- missing the closing escaped quote and period. GT text has `"unperturbed."` with closing punctuation.
- **Fix needed**: Fix value to end with `\"unperturbed.\"` to match the GT text.

### english_fig_131
- **Issue**: Fabricated atom `english_fig_131_legend_present` with value `"legend: not present"`. The groundtruth annotation does not mention a legend at all. This atom asserts information not derivable from the groundtruth text.
- **Fix needed**: Remove the `english_fig_131_legend_present` atom.

## Figures Passing

### english_fig_001
- Type: Pie Chart | Atoms: 10 | Status: PASS

### english_fig_002
- Type: Pie Chart | Atoms: 9 | Status: PASS

### english_fig_003
- Type: Line Plot | Atoms: 34 | Status: PASS

### english_fig_004
- Type: Line Plot | Atoms: 30 | Status: PASS

### english_fig_005
- Type: Line Plot | Atoms: 29 | Status: PASS

### english_fig_006
- Type: Line Plot | Atoms: 19 | Status: PASS

### english_fig_009
- Type: Pie Chart | Atoms: 5 | Status: PASS

### english_fig_011
- Type: Pie Chart | Atoms: 10 | Status: PASS

### english_fig_017
- Type: Pie Chart | Atoms: 6 | Status: PASS

### english_fig_023
- Type: Pie Chart | Atoms: 9 | Status: PASS

### english_fig_026
- Type: Pie Chart | Atoms: 16 | Status: PASS

### english_fig_029
- Type: Line Plot | Atoms: 28 | Status: PASS

### english_fig_031
- Type: Bar Chart | Atoms: 17 | Status: PASS

### english_fig_033
- Type: Line Plot | Atoms: 27 | Status: PASS

### english_fig_038
- Type: Line Plot | Atoms: 32 | Status: PASS

### english_fig_047
- Type: Bar Chart | Atoms: 16 | Status: PASS

### english_fig_050
- Type: Bar Chart | Atoms: 14 | Status: PASS

### english_fig_057
- Type: Line Plot | Atoms: 35 | Status: PASS

### english_fig_060
- Type: Line Plot | Atoms: 24 | Status: PASS

### english_fig_075
- Type: Bar Chart | Atoms: 17 | Status: PASS

### english_fig_085
- Type: Bar Chart | Atoms: 17 | Status: PASS

### english_fig_103
- Type: Bar Chart | Atoms: 15 | Status: PASS

### english_fig_109
- Type: Pie Chart | Atoms: 10 | Status: PASS

### english_fig_111
- Type: Bar Chart | Atoms: 13 | Status: PASS

### english_fig_120
- Type: Bar Chart | Atoms: 15 | Status: PASS

### english_fig_136
- Type: Bar Chart | Atoms: 10 | Status: PASS

### english_fig_171
- Type: Line Plot | Atoms: 27 | Status: PASS

### multi_fig_002
- Type: Bar Chart | Atoms: 14 | Status: PASS

### multi_fig_004
- Type: Pie Chart | Atoms: 8 | Status: PASS

### multi_fig_006
- Type: Line Plot | Atoms: 18 | Status: PASS

### multi_fig_007
- Type: Line Plot | Atoms: 20 | Status: PASS

### multi_fig_009
- Type: Line Plot | Atoms: 28 | Status: PASS

### multi_fig_041
- Type: Bar Chart | Atoms: 14 | Status: PASS

### multi_fig_045
- Type: Pie Chart | Atoms: 10 | Status: PASS

### multi_fig_054
- Type: Bar Chart | Atoms: 20 | Status: PASS

### multi_fig_111
- Type: Pie Chart | Atoms: 10 | Status: PASS

## Summary

- Total: 39
- Passing: 36
- Issues: 3

### Issues Breakdown

1. **Bad sentence split** (1 file): english_fig_019 sent_6/sent_7 splits mid-list at a period within a quoted label, creating a fragment.
2. **Truncated atom value** (1 file): english_fig_080 `bar_items_listed` is missing the closing escaped quote on `"unperturbed"`.
3. **Fabricated atom** (1 file): english_fig_131 `legend_present` asserts "legend: not present" when the groundtruth does not mention a legend.

### Validation Notes

- All 39 files have valid JSON structure.
- All 39 files have exactly the correct top-level fields: figure_key, figure_type, subfolder, language, reference_description, atoms. No extra or missing fields.
- All reference_descriptions match their corresponding English groundtruth annotation exactly.
- All figure_type values match the groundtruth.
- All atom values are strings (no booleans or numbers).
- All severity values are valid (critical/important/minor).
- All sentence-level atoms faithfully reproduce exact substrings of the reference_description.
- Structural decomposition atoms (line series, axis range, line color, element count, etc.) are present across most Line Plot and Bar Chart files and correctly decompose information from the groundtruth. These are intentional and not flagged as issues per review guidelines.
