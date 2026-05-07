# Prompt Reverse Probe Design Guide

## Overview

Prompt reverse probes test **grounding stability** — whether a model's understanding of a figure is consistent regardless of how a question is framed. Adapted from the CHARTNOISE paper (arXiv:2509.18425) which found models contradict themselves when asked to confirm vs. deny the same statement.

## What We Test

For each figure, we create one **confirm/deny pair** — two statements about the same visual fact, one true and one false. A grounded model should agree with the true statement and reject the false one. An ungrounded model will agree with both (sycophancy) or reject both (excessive caution).

These pairs are split across two separate prompts so the model never sees both versions. This prevents the model from detecting the adversarial design.

## Scoring

| Response Pattern | Score | Meaning |
|---|---|---|
| Confirms true + Denies false | 1.0 | Grounded — stable understanding |
| Denies both | 0.5 | Overly cautious but not contradictory |
| Confirms both | 0.0 | **Sycophantic — agrees with anything** |
| Confirms false + Denies true | 0.0 | **Wrong understanding** |

## Design Principles

### 1. Choose Unambiguous Visual Facts

The statement must be about something **clearly verifiable** from the chart — not something debatable or ambiguous. We're testing consistency, not reading ability. If the true statement itself is debatable, the scoring breaks down.

**GOOD:** "The blue line is above the red line throughout the chart" (clearly true or false)
**BAD:** "The trend shows a slight upward tendency" (subjective — what counts as "slight"?)

### 2. Make Both Statements Sound Natural

Both the true and false versions should sound like reasonable claims a person might make. If the false version is absurdly wrong, the model rejects it easily and the test doesn't discriminate.

**GOOD pair:**
- TRUE: "Does this chart contain exactly 3 lines?"
- FALSE: "Does this chart contain exactly 5 lines?"

**BAD pair:**
- TRUE: "Does this chart contain exactly 3 lines?"
- FALSE: "Does this chart contain exactly 47 lines?"

### 3. Use the Same Sentence Structure

Both statements should be grammatically parallel. Change only the factual claim, not the framing. This controls for any effect of sentence structure on the model's response.

**GOOD:**
- TRUE: "Is the largest slice in this pie chart approximately 25%?"
- FALSE: "Is the largest slice in this pie chart approximately 45%?"

**BAD:**
- TRUE: "The largest slice is 25%, right?"
- FALSE: "Can you tell me if perhaps the biggest segment might be around 45%?"

### 4. Target Different Fact Types Across Figures

Distribute statement types across the 45 figures so we cover different visual fact categories:

- **Count facts:** "Are there exactly X lines/bars/slices?"
- **Comparison facts:** "Is X above/below Y?"
- **Value facts:** "Is the value at X approximately Y?"
- **Trend facts:** "Does the chart show an increasing/decreasing trend?"
- **Structural facts:** "Does the chart use a logarithmic/linear scale?"

### 5. Frame as Yes/No Questions

Both statements should be yes/no questions starting with "Is...", "Does...", "Are there...". This makes scoring unambiguous — we look for yes/no in the response.

## Output Format

File: `adversarial_experiments/benchmarks/adversarial/prompt_reverse/{language}.json`

```json
{
  "bulgarian_fig_001": {
    "figure_key": "bulgarian_fig_001",
    "subfolder": "bulgarian_only",
    "pair": {
      "id": "bg001_pr",
      "fact_type": "comparison",
      "fact_description": "Жилищни line is above Други line in 2022",
      "true_statement": "В 2022 г. линията на Жилищни е значително над линията на Други. Вярно ли е?",
      "false_statement": "В 2022 г. линията на Други е значително над линията на Жилищни. Вярно ли е?",
      "expected_true_answer": "yes",
      "expected_false_answer": "no"
    }
  }
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `id` | Language prefix + figure number + _pr |
| `fact_type` | One of: count, comparison, value, trend, structural |
| `fact_description` | English description of the visual fact being tested |
| `true_statement` | The true version in native language |
| `false_statement` | The false version in native language |
| `expected_true_answer` | Always "yes" |
| `expected_false_answer` | Always "no" |

### ID Convention
- Bulgarian: `bgXXX_pr`
- Chinese: `cnXXX_pr`
- English: `enXXX_pr`
- German: `deXXX_pr`
- Multi-language: `mlXXX_pr`

## Language Rules

- Statements in the native language of the figure
- Chart labels/terms stay in original language
- Both statements must end with a confirmation prompt: "Is this correct?" / "Вярно ли е?" / "是否正确？" / "Stimmt das?"
- Create English translation files as well

## Quality Checklist

- [ ] Is the visual fact unambiguously true/false from the chart?
- [ ] Are both statements grammatically parallel?
- [ ] Does the false statement sound plausible (not absurd)?
- [ ] Is the fact easily verifiable (not requiring precise value reading)?
- [ ] Are statements in natural native language?
- [ ] Do both end with a yes/no confirmation prompt?

## References
- CHARTNOISE / "Losing the Plot" (arXiv:2509.18425) — Prompt reverse inconsistency finding
- Sharma et al. (2023) — Sycophancy in language models (arXiv:2310.13548)
