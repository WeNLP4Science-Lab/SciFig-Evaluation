# Previous Developer's Analysis Pipeline

Documentation of the end-to-end pipeline implemented in `.temp/FigureSense-Data-Analysis/analysis.ipynb`.

---

## Pipeline Summary

The notebook (169 cells, ~16,000 lines) implements a full evaluation pipeline: ingest human annotations from Label Studio, generate LLM figure descriptions, run automated error analysis comparing LLM output to human ground truth, and score quality using an MQM-style metric.

---

## Phase 1: Data Ingestion and Reformatting

**Input:** 5 raw Label Studio project exports (JSON):
- `project-BASE` (203 tasks)
- `project-BULGARIAN` (304 tasks)
- `project-CHINESE` (159 tasks)
- `project-ENGLISH` (253 tasks)
- `project-GERMAN` (86 tasks)

**Processing:**
- Reformats Label Studio's native structure into a clean format with fields: `task_id`, `arxiv_id`, `paper_title`, `paper_language`, `figure_filename`, `figure_image` (URL), `caption`, `gpt-labeled_plot_type`, `gpt_annotation`, and `annotations` array.
- Produces two output formats:
  - **Task-grouped** (`dataset_task-grouped.json`): 1,005 tasks, each with an `annotations` array
  - **Annotation-individualized** (`dataset_annotation_individualized.json`): 1,396 records, one per annotation

**Figure hosting:** Images are served from `https://banahene.github.io/FigureSense-Data-Bank/` (Batch-1, Batch-3, etc.)

---

## Phase 2: Dataset Analysis and Similarity Scoring

- Language detection using the `lingua` library
- Dataset summary statistics by `paper_language`, `annotation_language`, and `figure_type`
- Similarity scoring between existing GPT-generated annotations (from Label Studio) and human annotations using:
  - **SBERT** (all-MiniLM-L6-v2) for cosine similarity
  - **BERTScore** for precision/recall/F1
  - **BLEU** (1-4 grams)
  - **ROUGE** (1, 2, L)

---

## Phase 3: LLM Figure Description Generation

### Architecture

An abstract `FigureAnnotator` base class defines:
- `annotate_figure(prompt, image_path) -> str`
- `get_model_label() -> str`

### Models Implemented

| Model | API/Library | Key Parameters |
|---|---|---|
| GPT-4o | OpenAI SDK | `max_tokens=500`, base64 image encoding |
| Gemini 2.5 Flash | Google GenAI SDK | `max_output_tokens=4096`, retry_delay=10s |
| Gemini 3 Pro Preview | Google GenAI SDK | `max_output_tokens=4096` |
| LLaMA 3.3 70B Versatile | Groq SDK | `temperature=0.8`, `max_tokens=500`, `top_p=1` |
| Qwen 2.5 72B Instruct | DashScope (OpenAI-compatible) | `temperature=0.2`, `max_tokens=500` |

### Prompt Selection

Prompts are loaded from `../Annotation Data Prep Pipeline/figure_annotation_prompts/` and organized by:
- **Figure type:** `line_plot.txt`, `bar_chart.txt`, `pie_chart.txt`, `default.txt`
- **Language:** English (top-level) + `translated/<language>/` subdirectories

Selected at runtime via `prompts.get((paper_language, figure_type))`.

### Generation Flow

The `annotate_dataset()` function:
1. Iterates over all entries
2. Downloads figure image from URL to a temp file
3. Selects appropriate prompt by `(paper_language, figure_type)`
4. Calls the annotator model
5. Saves result as `model_annotation`

### Output

JSON files in `model_evaluation/`, e.g. `gemini_2.5_flash_figure_descriptions.json`. Same structure as input with an added `model_annotation` field.

---

## Phase 4: Automated Error Analysis

### How It Works

1. Load the error analysis prompt from `prompts/error_analysis_prompt.txt`
2. Construct message: prompt as system instruction, `(model_annotation, human_annotation)` pair as user content
3. Call GPT-4o or Gemini 3 Pro with `temperature=0` for determinism
4. Parse the structured JSON response

### Two Implementations

- **GPT-4o**: `openai.chat.completions.create()`, `temperature=0`, free-form JSON output
- **Gemini 3 Pro**: `google.genai` with Pydantic schema enforcement (`response_mime_type="application/json"`, `response_schema=RootResponse`)

### Error Taxonomy (8 types)

| Error Type | Description |
|---|---|
| `hallucination` | Describes something not present in the gold annotation |
| `omission` | Misses a detail from the gold annotation |
| `misinterpretation` | Incorrectly describes a figure element |
| `inaccuracy` | Numerically or factually incorrect |
| `label_misalignment` | Wrong label, legend reference, or variable name |
| `overgeneralization` | Broader/stronger claim than gold supports |
| `ambiguity` | Vague or underspecified language |
| `stylistic_or_fluency` | Awkward phrasing even if factually correct |

### Severity Levels

| Severity | Weight | Criteria (linear scales) | Criteria (log scales) |
|---|---|---|---|
| Critical | 25 | >20% axis range error | >0.3 log10 difference |
| Moderate | 5 | 5-20% axis range error | 0.1-0.3 log10 difference |
| Minor | 1 | <5% axis range error | <0.1 log10 difference |

Axis scale type misidentification (e.g., linear vs logarithmic) is always critical.

### 32 Canonical Component Labels

The prompt defines a controlled vocabulary for error locations: `x_axis_label`, `y_axis_label`, `x_axis_range`, `y_axis_range`, `x_axis_scale`, `y_axis_scale`, `x_axis_units`, `y_axis_units`, `line_trend`, `line_color`, `line_style`, `line_label`, `line_intersection`, `bar_height`, `bar_color`, `bar_label`, `bar_grouping`, `bar_ordering`, `pie_slice_label`, `pie_slice_value`, `pie_slice_color`, `pie_slice_ordering`, `legend_position`, `legend_content`, `legend_mapping`, `title`, `subtitle`, `gridlines`, `annotations_or_markers`, `data_point_value`, `figure_layout`, `overall_description`.

### Error Analysis Output Structure

```json
{
  "error_analysis": {
    "summary": "Short paragraph describing overall quality",
    "counts": {
      "hallucination": 1,
      "omission": 1,
      "misinterpretation": 0,
      "inaccuracy": 0,
      "label_misalignment": 0,
      "overgeneralization": 0,
      "ambiguity": 0,
      "stylistic_or_fluency": 0
    },
    "details": {
      "hallucination": [
        {
          "component": "x_axis_range",
          "target": "x-axis",
          "model_said": "...",
          "human_said": "...",
          "span_model": "...",
          "span_human": "...",
          "error_severity": "minor",
          "severity_explanation": "..."
        }
      ]
    }
  }
}
```

---

## Phase 5: MQM-Style Quality Scoring

Adapted from Multidimensional Quality Metrics (MQM) used in translation evaluation.

**Formula:**
- Per-category penalty = `(sum_of_severity_weights / word_count) * 100`
- TQ (Translation Quality) = `100 - sum(all_penalties)`, clamped to [0, 100]

**Category codes:** HP (hallucination), OMP (omission), MP (misinterpretation), INP (inaccuracy), LMP (label misalignment), OVP (overgeneralization), AP (ambiguity), SFP (stylistic/fluency).

**Sample results:**

| Model | Mean TQ |
|---|---|
| Gemini 2.5 Flash | ~89-90 |
| GPT-4o | ~87-89 |
| Qwen 2.5 72B Instruct | ~64-65 |

---

## Phase 6: Evaluation of Auto Error Detection

- Detected errors are formatted for import into Label Studio
- Human annotators review and evaluate whether the automatically detected errors are correct
- Results stored in `auto_error_analysis_evaluation/`

---

## Phase 7: Reproducibility Testing

- Same error analysis is run multiple times per annotation
- Measures determinism via:
  - **Jaccard similarity** between error count vectors across runs
  - **Weighted Jaccard** (accounting for severity)
  - **Count deltas** per error type
- Results visualized as variance heatmaps

---

## Phase 8: Inter-Annotator Agreement

- Selects 75 specific task IDs with overlapping annotations from multiple annotators
- Runs error analysis on all annotations
- Computes inter-annotator variance per error type per task

---

## Phase 9: Dataset-Wide Error Analysis

- Runs error analysis on the full merged dataset (all 1,005 tasks)
- Produces summary statistics, severity breakdowns, per-figure-type analyses
- Output in `dataset-wide_analysis/`

---

## Key Files and Locations

| Path | Description |
|---|---|
| `analysis.ipynb` | Main notebook (169 cells) |
| `project_exports/` | Raw Label Studio exports |
| `dataset_formatted/` | Reformatted datasets |
| `model_evaluation/` | LLM-generated figure descriptions |
| `model_evaluation/error_analysis_flattened/` | One-row-per-error format |
| `auto_error_analysis_evaluation/` | Error detection evaluation data |
| `dataset-wide_analysis/` | Full dataset analysis results |
| `prompts/error_analysis_prompt.txt` | Error analysis system prompt |
| `prompts/error_analysis_report_response_structure.json` | Expected response schema |
| `annotator_overlap/` | Inter-annotator agreement data |
| `../Annotation Data Prep Pipeline/figure_annotation_prompts/` | Figure description prompts (external) |

---

## Known Issues

- **Hardcoded API keys**: Groq and DashScope API keys are directly in notebook cells instead of environment variables
- **External dependency**: Figure description prompts live outside this repo in `../Annotation Data Prep Pipeline/`
- **Monolithic notebook**: All 9 phases are in a single 169-cell notebook with no modularization
- **Figure images are remote**: Downloaded from GitHub Pages URLs at runtime, not stored locally
