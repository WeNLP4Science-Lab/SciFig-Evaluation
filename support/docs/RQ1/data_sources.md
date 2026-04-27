# Data Sources for RQ1

Where each piece of data lives in the repo and how to access it.

## Evaluation Results

### V2 Atomic MQM (LLM Judges)
- **Path**: `output/evaluation/atomic_mqm_v2/{judge}/{model}/{subfolder}/{fig_key}.json`
- **Judges**: `azure/gpt-4o`, `azure/mistral-large-3`
- **Models**: 13 models (see below)
- **Figures**: 120 total (45 adversarial subset completing first, then full 120)
- **Fields per file**: `figure_key`, `subfolder`, `model_name`, `judge_model`, `num_atoms`, `errors[]`, `error_count`, `mqm_score`, `total_penalty`, `atom_coverage`
- **Script**: `atomic_mqm/evaluator_v2.py`

### Human Evaluation
- **Raw export**: `HumanEval/project-15-at-2026-04-27-01-32-eea32bfb.json`
- **Model mapping**: `HumanEval/structuring_label_studio_export/model_alias_pools.json`
- **Structured output**: `HumanEval/structuring_label_studio_export/structured_output/annotations_structured.json`
- **Processed results**: `HumanEval/human_eval_results.json`
- **Script**: `HumanEval/structuring_label_studio_export/process_label_studio_export.py`
- **Coverage**: 4 models (gpt-5.2, qwen3-vl-30b-a3b, qwen3-vl-8b, gemma3-27b-it) x 30 English figures x 3 annotators

### Cross-Lingual Evaluation
- **Path**: `output/evaluation/crosslingual/{judge}/{model}/{language}/{fig_key}.json`
- **Atoms**: `atomic_mqm/atoms_crosslingual/{fig_key}_{lang}.json`
- **Coverage**: 13 parallel figures x 4 languages (BG, CN, DE, EN)
- **Script**: `atomic_mqm/evaluator_crosslingual.py`

### Prompt Ablation — C2 (English Prompt)
- **Descriptions**: `output/experiments/transforms_english_prompt/{model}/{fig_key}.json`
- **Evaluation**: Uses same evaluator_v2 pointed at these transforms
- **Script**: `scripts/experiments/run_transforms_english_prompt.py`

### Prompt Ablation — C2' (English Instruction, Native Output)
- **Descriptions**: `output/experiments/transforms_english_instruction_native_output/{model}/{fig_key}.json`
- **Script**: `scripts/experiments/run_transforms_english_instruction_native_output.py`

### Chain-of-Thought
- **Descriptions**: `scripts/experiments/cot/output/`
- **Evaluation**: `scripts/experiments/cot/evaluate_all_cot.py`

---

## Atom Checklists

### Main Atoms (120 figures)
- **Path**: `atomic_mqm/atoms/{fig_key}.json`
- **Fields**: `figure_key`, `figure_type`, `subfolder`, `language`, `reference_description`, `atoms[]`
- **Each atom**: `id`, `severity` (critical/important/minor), `value`
- **Total**: 2,252 atoms across 120 figures

### Cross-Lingual Atoms (25 parallel figures)
- **Path**: `atomic_mqm/atoms_crosslingual/{fig_key}_{lang}.json`
- **Languages**: bg, cn, de, en
- **Total**: 88 files

---

## Model Descriptions (Generations)

### Original Descriptions
- **Transforms**: `output/experiments/transforms/{model}/original/{subfolder}/{fig_key}.json`
- **Generation**: `output/generation/{model}/{subfolder}/{fig_key}.json`
- **Priority**: Evaluator checks transforms first, falls back to generation

### 13 Models
| Our Name | API/Router Name | Type |
|----------|----------------|------|
| gpt-5.2 | azure/gpt-5.2 | Proprietary |
| gemini-3.1-pro | google/gemini-3.1-pro | Proprietary |
| claude-opus-4.6 | anthropic/claude-opus-4-6 | Proprietary |
| qwen3-vl-235b-a22b | qwen/qwen3-vl-235b-a22b | Open |
| qwen3-vl-32b | qwen/qwen3-vl-32b | Open |
| qwen3-vl-30b-a3b | qwen/qwen3-vl-30b-a3b | Open |
| qwen3-vl-8b | qwen/qwen3-vl-8b | Open |
| llama4-maverick | meta-llama/llama-4-maverick | Open |
| llama4-scout | meta-llama/llama-4-scout | Open |
| gemma3-27b-it | google/gemma-3-27b-it | Open |
| gemma3-12b-it | google/gemma-3-12b-it | Open |
| gemma3-4b-it | google/gemma-3-4b-it | Open |
| phi-4-multimodal | microsoft/phi-4-multimodal | Open |

---

## Ground Truth

- **Path**: `Dataset/groundtruth/{subfolder}/{fig_key}.json`
- **Subfolders**: `english_only`, `bulgarian_only`, `chinese_only`, `german_only`, `multi_language`
- **Fields**: `figure_key`, `figure_type`, `annotations[]` (each with `annotation`, `annotation_language`)

## Figures (Images)

- **Path**: `Dataset/figures/{subfolder}/{fig_key}.png`
- **Same subfolders as groundtruth**

---

## Analysis Scripts

| Script | Purpose |
|--------|---------|
| `scripts/analysis/export_final_results.py` | Aggregate all results into `final_results.json` |
| `scripts/analysis/export_adversarial_results.py` | Adversarial subset aggregation |
| `scripts/analysis/plot_rq1_results.py` | TO BE CREATED — all RQ1 charts |

---

## Key Computed Values Already Known

### Human Eval (from processing)
- GPT-5.2: MQM 97.0 (n=40)
- qwen3-vl-8b: MQM 76.2 (n=39)
- qwen3-vl-30b-a3b: MQM 76.2 (n=40)
- gemma3-27b-it: MQM 59.9 (n=40)
- IAA: mean diff 7.6, median 6.4, 69% within 10 pts

### LLM Judges (partial, 3 models complete on 120 figures)
- GPT-4o judge: GPT-5.2=72.0, Gemini=70.4, Claude=67.7
- Mistral judge: GPT-5.2=79.0, Gemini=74.9, Claude=75.2

### Judge Severity Split
- Mistral: 26-31% Major
- GPT-4o: 69-71% Major
