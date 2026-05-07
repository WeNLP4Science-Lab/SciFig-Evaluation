# New MQM Approach: Atomic Truth Checklist

## Problem with Current MQM
- Judge finds errors in open-ended way — misses completeness errors
- A completely wrong description (wrong figure) can score 61/100 because judge only flags 9 errors instead of 20+
- No systematic checking of what's missing from groundtruth
- Penalty-based scoring means you need 20+ Major errors to reach 0

## Proposed Approach

### 1. Define Atomic Truths per Figure
Break each figure's groundtruth into the smallest verifiable units (atoms). Each atom is one fact that can be independently checked as correct, inaccurate, or missing.

### 2. Atom Templates by Figure Type

**Line Plot atoms:**
- Chart purpose/title
- X-axis label
- X-axis scale type (linear/log/etc.)
- X-axis value range
- X-axis units
- X-axis tick interval
- Y-axis label
- Y-axis scale type
- Y-axis value range
- Y-axis units
- Y-axis tick interval
- Per line (×N lines):
  - Line name/label
  - Line color
  - Line style (solid/dashed/dotted)
  - Marker shape
  - Start value (at first x point)
  - End value (at last x point)
  - Key peaks/valleys with values
- Legend presence and content
- Subplot structure (if multiple)
- Annotations/labels on data points

**Bar Chart atoms:**
- Chart purpose/title
- Category axis orientation (horizontal/vertical)
- Category axis label
- Category names (each is an atom)
- Value axis label
- Value axis scale type
- Value axis range
- Value axis units
- Per bar/group (×N):
  - Bar label
  - Bar color
  - Bar value
- Grouped/stacked structure description
- Sort order
- Visual emphasis (annotations, bold, etc.)

**Pie Chart atoms:**
- Chart purpose/title
- Total number of slices
- Per slice (×N):
  - Slice label
  - Slice color
  - Slice percentage/value
- Legend presence
- Labels inside/outside slices
- Ordering pattern
- Visual emphasis (exploded slices, etc.)

### 3. Scoring per Atom
Each atom scored independently:
- **Correct (C)** — model stated it accurately
- **Inaccurate (I)** — model mentioned but got wrong
- **Missing (M)** — model didn't mention at all
- **Hallucinated (H)** — model added something not in checklist
- **N/A** — atom doesn't apply to this figure

### 4. MQM Score Computation

**Accuracy** = C / (C + I)
**Completeness** = C / (C + M)
**Hallucination rate** = H / total_atoms_mentioned

**Overall MQM** = weighted combination:
- Accuracy weight: 0.5
- Completeness weight: 0.35
- Hallucination penalty: 0.15

Or keep penalty-based but now with exhaustive checking:
- Each Inaccurate atom = penalty (severity-weighted)
- Each Missing atom = penalty (severity-weighted)
- Each Hallucinated atom = penalty

### 5. Atom Severity Levels
Not all atoms are equal:
- **Critical**: chart purpose, axis labels, data series names — these define what the chart IS
- **Important**: values, ranges, scale types — these define what the chart SHOWS
- **Minor**: colors, styles, tick intervals — these define how the chart LOOKS

### 6. Implementation Plan
1. Define atom templates per figure type (3 types + default)
2. For each of 45 figures, fill template from groundtruth annotation
3. Human-verify extracted atoms
4. Judge receives: image + atom checklist + model description
5. Judge scores each atom as C/I/M/H
6. Compute MQM from atom scores

### 7. Advantages
- Exhaustive — nothing missed
- Reproducible — same checklist every time
- Comparable — same methodology across figures
- Interpretable — know exactly which atoms failed
- Judge's job is simpler — verify yes/no per atom, not "find all errors"

### 8. Estimated Effort
- ~30-50 atoms per figure
- 45 figures = ~1,500-2,000 atoms total
- Template approach reduces manual work — fill template, not write from scratch
- LLM can extract initial atoms from groundtruth text, human verifies
