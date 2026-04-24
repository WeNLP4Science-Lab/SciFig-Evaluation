# Atomic MQM — Checklist-Based Figure Description Evaluation

## Problem
The standard MQM evaluation asks a judge to "find errors" in an open-ended way. This leads to:
- Missed completeness errors (judge doesn't flag all missing elements)
- A completely wrong description (wrong figure) can score 61/100
- Inconsistent scoring across figures with different complexity
- Scores don't normalize by figure complexity — a 5-atom figure can never reach 0

## Solution
Replace open-ended error finding with a **pre-defined checklist of atomic truths** per figure. The judge verifies each atom systematically, producing standard MQM errors with a normalized scoring formula that guarantees the full 0-100 range regardless of atom count.

## What is an Atom?
The smallest verifiable claim about a figure, extracted verbatim from the groundtruth annotation. Examples:
- "The x-axis label is 'Number of completions (k)'"
- "The x-axis uses a logarithmic scale"
- "There are 4 lines in the plot"
- "The blue solid line starts at approximately 0.42"

## Atom Severity Levels

Each atom has a severity that determines how much errors against it are penalized:

- **Critical**: Chart type, purpose, axis labels, data series names — defines what the chart IS
- **Important**: Values, ranges, scale types — defines what the chart SHOWS
- **Minor**: Colors, styles, tick intervals, markers — defines how the chart LOOKS

**The atom severity caps the error severity.** A minor atom can never produce a Major error. A critical atom can produce a Minor error if only partially wrong.

| Atom Severity | Complete miss/wrong | Partial miss/slightly off |
|---------------|--------------------|--------------------------| 
| Critical      | Major error        | Minor error              |
| Important     | Major error        | Minor error              |
| Minor         | Minor error        | Minor error              |

## Evaluation Process

The judge receives: **image + atom checklist + reference description + model description**.

### Step 1: Accuracy Check (atoms + image)
For each atom, check if the model description mentions it AND gets it right. If mentioned but wrong, flag an Accuracy error:

| Sub-type | Description |
|----------|-------------|
| Incorrect Numerical Value | Wrong numbers, percentages, quantities |
| Incorrect Axis or Legend Interpretation | Wrong axis labels, units, legend info |
| Incorrect Visual Attribute Mapping | Wrong color, series name, attribute assignment |
| Incorrect Structural Description | Wrong structure (grouped vs stacked, wrong count) |

### Step 2: Completeness Check (atoms)
For each atom, check if the model description covers this information at all. If missing, flag a Completeness error:

| Sub-type | Description |
|----------|-------------|
| Missing Chart Purpose | Chart purpose/title not stated |
| Missing Axis Description | Axis labels, units, scale, range, ticks omitted |
| Missing Visual Features | Data series, colors, values, legend, structure omitted |

Each missing atom is flagged as a **separate** error. Partially covered atoms get a Minor severity; completely missing atoms get severity based on atom severity (see table above).

### Step 3: Hallucination Check (atoms + image)
Check for claims NOT covered by any atom:

| Sub-type | Description |
|----------|-------------|
| Hallucinated Content | Introduces visual elements or data that don't exist |
| Unwanted Interpretation | Adds inference or subjective language beyond what is shown |

Hallucinations are not linked to any atom. The judge assigns Major or Minor severity based on how misleading the fabrication is.

### Step 4: Clarity Check (reference description)
Compare model description against reference for readability:

| Sub-type | Description |
|----------|-------------|
| Ambiguous Description | Vague or unclear references |
| Over-Generalization | Oversimplifies or exaggerates visual information |
| Overly Verbose Description | Unnecessary repetition or excessive detail |
| Poor Sentence Structure | Grammar errors or awkward phrasing |

Clarity only meaningfully affects the score when accuracy and completeness are good — if the description is already wrong, clarity penalties don't matter (score is capped at 0).

## Error Output Format

Same standard MQM format, with an additional `atom_id` field:

```json
{
  "errors": [
    {
      "category": "Accuracy",
      "sub_type": "Incorrect Numerical Value",
      "severity": "Major",
      "text_span": "with a final value of 60%",
      "evidence": "Atom says 45% but description says 60%",
      "atom_id": "fig_001_sent_3"
    },
    {
      "category": "Completeness",
      "sub_type": "Missing Axis Description",
      "severity": "Major",
      "text_span": null,
      "evidence": "The description does not mention the y-axis units",
      "atom_id": "fig_001_yaxis_label"
    },
    {
      "category": "Completeness",
      "sub_type": "Hallucinated Content",
      "severity": "Major",
      "text_span": "there are six distinct clusters",
      "evidence": "Figure shows four clusters, not six",
      "atom_id": null
    }
  ]
}
```

- `atom_id`: links to the specific atom for accuracy/completeness errors; `null` for hallucinations and clarity errors
- `text_span`: exact substring from model description for incorrect/hallucinated/clarity errors; `null` for missing content

## Scoring

### MQM Weights (from guidelines Table 2)

| Error Category          | Major Weight | Minor Weight |
|-------------------------|-------------|-------------|
| Accuracy                | 5.0         | 2.0         |
| Completeness            | 3.5         | 1.5         |
| Clarity and Readability | 2.0         | 1.0         |

### Normalized MQM Formula

```
max_possible_penalty = num_atoms × 5.0

MQM = max(0, 100 - (Σ all_penalties / max_possible_penalty) × 100)
```

Where:
- `Σ all_penalties` = sum of weights for all errors (accuracy + completeness + hallucination + clarity)
- `max_possible_penalty` = worst case if every atom had an Accuracy/Major error (the highest per-atom penalty)
- `num_atoms` = number of atoms in the figure's checklist

### Why normalize?

Without normalization, `MQM = max(0, 100 - Σ penalties)` depends on atom count:
- A 5-atom figure with everything wrong: `100 - 25 = 75` (should be 0)
- A 46-atom figure with everything wrong: `100 - 230 = 0`

With normalization:
- A 5-atom figure with everything wrong: `100 - (25/25) × 100 = 0`
- A 46-atom figure with everything wrong: `100 - (230/230) × 100 = 0`
- Both correctly score 0.

### Hallucination and clarity in the formula

Hallucinations and clarity errors add to `Σ all_penalties` but are NOT part of `max_possible_penalty`. This means:
- A model can exceed the max penalty (e.g., all atoms wrong AND hallucinations), but the score is clamped at 0
- A model with all atoms correct but heavy hallucination still gets penalized
- Clarity errors only move the needle when accuracy and completeness are good — otherwise the score is already at or near 0

### Atom Coverage Metrics

In addition to the MQM score, atom-level metrics are computed from atom_id-linked errors:

- **Atom Accuracy** = atoms with no accuracy error / total atoms
- **Atom Completeness** = atoms mentioned (no completeness error) / total atoms

These provide interpretable per-dimension scores alongside the composite MQM.

## Dataset

- **120 figures** across 4 languages (30 Bulgarian, 30 Chinese, 39 English+Multi, 21 German)
- **2,252 atoms** total, extracted verbatim from groundtruth annotations
- Atoms reviewed and validated per language with automated review agents

## File Structure
```
atomic_mqm/
├── README.md              (this file)
├── judge_prompt.txt       (judge system prompt)
├── evaluator.py           (evaluation script)
├── atoms/                 (120 atom files, one per figure)
│   ├── bulgarian_fig_001.json
│   ├── chinese_fig_004.json
│   ├── english_fig_002.json
│   ├── german_fig_001.json
│   └── ...
└── reviews/               (validation reports per language)
    ├── review_bulgarian.md
    ├── review_chinese.md
    ├── review_english.md
    └── review_german.md
```

## Usage

```bash
# Evaluate one model with one judge
python3 atomic_mqm/evaluator.py gpt-5.2 --judge azure/gpt-4o --workers 4

# Filter to one subfolder
python3 atomic_mqm/evaluator.py gpt-5.2 --judge azure/gpt-4o --subfolder english_only

# Evaluate all models
python3 atomic_mqm/evaluator.py --all --judge azure/gpt-4o --workers 4
```

Output: `output/evaluation/atomic_mqm/{judge}/{model}/{subfolder}/{fig_key}.json`
