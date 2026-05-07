# German Atom Review

## Figures with Issues

### german_fig_001
- **Issue**: Atom `purple_line_start` has value "Die lilane Linie fängt in 2016 bei 0 an" but groundtruth text reads "Die lilane Linie fängt in 2016 bei 0 and und steigt bis 2020 auf 2000 an". The groundtruth has a typo "bei 0 and und" -- the atom silently corrects "and" to "an" instead of preserving the original text exactly.
- **Fix needed**: Change atom value to "Die lilane Linie fängt in 2016 bei 0 and" or "Die lilane Linie fängt in 2016 bei 0 and und" to match the groundtruth verbatim.

### german_fig_002
- **Issue 1**: Missing atom for blue line intermediate dip. The groundtruth says "Danach fällt sie kurz und steigt dann bis Ende 2023 auf 350" but there is no atom for "Danach fällt sie kurz" -- only the rise to 350 is captured.
- **Issue 2**: Atom `legend_blue_line` has value "die blaue Linie als \"Importe (linke Skala)\"" but groundtruth text reads "dir blaue Linie als \"Importe (linke Skala)\"". The groundtruth typo "dir" was silently corrected to "die".
- **Fix needed**: (1) Add an atom for "Danach fällt sie kurz" to cover the blue line dip. (2) Change atom value to preserve groundtruth typo "dir" instead of correcting it.

## Figures Passing

### german_fig_001
- Type: line_plot | Atoms: 29 | Status: PASS (except issue above)

### german_fig_004
- Type: line_plot | Atoms: 40 | Status: PASS

### german_fig_009
- Type: bar_chart | Atoms: 26 | Status: PASS

### german_fig_011
- Type: line_plot | Atoms: 23 | Status: PASS

### german_fig_012
- Type: line_plot | Atoms: 19 | Status: PASS

### german_fig_015
- Type: bar_chart | Atoms: 19 | Status: PASS

### german_fig_016
- Type: line_plot | Atoms: 17 | Status: PASS

### german_fig_018
- Type: bar_chart | Atoms: 16 | Status: PASS

### german_fig_022
- Type: bar_chart | Atoms: 27 | Status: PASS

### german_fig_023
- Type: bar_chart | Atoms: 26 | Status: PASS

### german_fig_024
- Type: line_plot | Atoms: 33 | Status: PASS

### german_fig_033
- Type: line_plot | Atoms: 29 | Status: PASS

### german_fig_039
- Type: bar_chart | Atoms: 14 | Status: PASS

### german_fig_042
- Type: bar_chart | Atoms: 16 | Status: PASS

### german_fig_051
- Type: line_plot | Atoms: 20 | Status: PASS

### german_fig_057
- Type: pie_chart | Atoms: 43 | Status: PASS

### german_fig_060
- Type: line_plot | Atoms: 25 | Status: PASS

### german_fig_070
- Type: bar_chart | Atoms: 31 | Status: PASS

### german_fig_082
- Type: bar_chart | Atoms: 33 | Status: PASS

### german_fig_085
- Type: bar_chart | Atoms: 25 | Status: PASS

## Summary
- Total: 21
- Passing: 19
- Issues: 2
- Issue breakdown:
  - german_fig_001: 1 atom silently corrects a groundtruth typo ("and" -> "an")
  - german_fig_002: 1 missing atom for blue line dip + 1 atom silently corrects groundtruth typo ("dir" -> "die")
- All 21 files have valid JSON structure
- All 21 files use German text exclusively (no English translations)
- All atom values are strings (no booleans or numbers)
- All severities are valid (critical/important/minor)
- No fabricated atoms found -- every atom value traces back to the groundtruth text
- Groundtruth typos preserved correctly in most atoms (e.g., "Durchschnitee" in fig_022, "19.59" in fig_039, "neun Kategorien" listing only 8 in fig_085, double "die die" in fig_051)
- Completeness is strong across all files -- groundtruth content is well-decomposed into atoms
- Previously flagged issue (german_fig_024 fabricated `marker_shape` atom) has been resolved and is no longer present
