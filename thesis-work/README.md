# SciFig-Eval

**A Multilingual Benchmark and Behavioural Framework for Evaluating Vision-Language Models on Scientific Figures**

*MSc Artificial Intelligence Thesis, University of Aberdeen, 2026*

Paul Osemudiame Oamen | Supervisor: Dr Wei Zhao

---

## Overview

SciFig-Eval is a multilingual evaluation framework for assessing how well vision-language models (VLMs) comprehend scientific figures. Unlike existing benchmarks that measure extraction accuracy through closed-form QA, SciFig-Eval evaluates **description quality** through open-ended generation and **behavioural reliability** through adversarial probes.

The framework introduces the **Admittance-Resistance-Inductance (A-R-I)** behavioural model, which decomposes figure-reading trustworthiness into three axes:

- **Admittance** — epistemic honesty when content is unreadable
- **Resistance** — robustness to false or unsupported premises
- **Inductance** — contextual reasoning from partial evidence

## Key Numbers

| Metric | Value |
|--------|-------|
| Scientific figures | 1,005 |
| Research papers | 349 |
| Languages | 4 (English, Bulgarian, Chinese, German) |
| Expert annotations | 1,411 |
| Atomic fact checklists | 2,252 |
| Capability questions | 630 |
| Models evaluated | 13 (6 families, 4B-235B+) |
| LLM judges | 2 (GPT-4o, Mistral Large 3) |
| Total evaluations | 2,966 |
| Human ICC | .91 |

## Architecture

```
Dataset/                          # 1,005 figures + groundtruth annotations
  figures/                        # PNG images (5 language subfolders)
  groundtruth/                    # JSON annotations
adversarial_experiments/          # 45-figure adversarial subset
  benchmarks/                     # Probes: hallucination, caption bias, prompt reverse, capability
  samples.json                    # Sample manifest
atomic_mqm/                       # Atomic MQM decompositions (120 figures)
scripts/
  llm_generation/                 # Model abstraction layer + generation runners
    models.py                     # FigureAnnotator classes + factory
    run.py                        # Main generation entry point
  evaluation/                     # MQM judge pipeline
    mqm_evaluator.py              # Core scoring + judge prompts
    evaluate_reference_free.py    # Judge A: image only
    evaluate_reference_with_image.py  # Judge C: image + groundtruth
  experiments/                    # Adversarial experiment runners
    run_transforms.py             # 9 visual transforms
    run_prompt_reverse.py         # Prompt reversal probes
    run_caption_bias.py           # Caption bias probes
    run_questions.py              # Capability questions
    run_active_admittance.py      # Active admittance probes
    run_inductance.py             # Inductance reasoning probes
  evaluation-results/             # Results computation + plotting
    rq1/                          # Leaderboard, error analysis, cross-lingual
    rq2/                          # Degradation under transforms
    rq3/                          # Capability question accuracy
    rq4/                          # A-R-I behavioural scores
output/                           # All generated artefacts
  generation/                     # Model descriptions
  evaluation/                     # Judge scores
  experiments/                    # Adversarial experiment results
  evaluation-results/             # Computed tables + plots
dashboard/                        # React + Vite + Tailwind interactive UI
HumanEval/                        # Label Studio exports + human evaluation
```

## Pipeline

The evaluation pipeline operates in three stages:

**Stage 1: Generation** — Each of 13 models generates descriptions for all 1,005 figures across 5 language subfolders.

**Stage 2: MQM Evaluation** — Two LLM judges (GPT-4o, Mistral Large 3) independently score each description under three configurations (reference-free, reference-only, reference-with-image).

**Stage 3: Results** — Aggregation scripts compute bootstrap CIs, pairwise significance tests, per-language breakdowns, and generate all thesis tables and plots.

## Models Evaluated

| Model | Family | Parameters | Backend |
|-------|--------|------------|---------|
| GPT-5.2 | OpenAI | undisclosed | Azure |
| Gemini 3.1 Pro | Google | undisclosed | OpenRouter |
| Claude Opus 4.6 | Anthropic | undisclosed | OpenRouter |
| Qwen3-VL 235B | Alibaba | 235B/22B | OpenRouter |
| Qwen3-VL 32B | Alibaba | 32B | OpenRouter |
| Qwen3-VL 30B | Alibaba | 30B/3B | OpenRouter |
| Qwen3-VL 8B | Alibaba | 8B | OpenRouter |
| LLaMA-4 Maverick | Meta | 400B+ | OpenRouter |
| LLaMA-4 Scout | Meta | 109B | OpenRouter |
| Gemma-3 27B | Google | 27B | OpenRouter |
| Gemma-3 12B | Google | 12B | OpenRouter |
| Gemma-3 4B | Google | 4B | OpenRouter |
| Phi-4 Multimodal | Microsoft | 14B | Azure |

## Key Findings

- **GPT-5.2** leads on description quality (75.5 MQM) but scores only .56 on resistance to false premises
- **Gemini 3.1 Pro** is the only model maintaining top-tier standing across accuracy, comprehension, and behavioural trustworthiness
- **Gemma family** fabricates with near-zero admittance regardless of scale
- **Numerical precision** accounts for 30.6% of all errors
- **Description and comprehension** appear to be partially dissociated capabilities
- **Cross-lingual performance** comparisons are unreliable without controlling for figure complexity

## Quick Start

```bash
# Clone and install
git clone https://github.com/WeNLP4Science-Lab/SciFig-Evaluation.git
cd SciFig-Evaluation
python3 -m venv .venv && source .venv/bin/activate
pip install openai google-genai python-dotenv numpy matplotlib scipy seaborn

# Configure API credentials
cp .env.example .env  # Edit with your API keys

# Generate descriptions
python3 scripts/llm_generation/run.py gpt-5.2 --workers 4

# Run MQM evaluation
python3 scripts/evaluation/evaluate_reference_free.py gpt-5.2 --judge azure/gpt-4o

# Run adversarial experiments
python3 scripts/experiments/run_prompt_reverse.py gpt-5.2 --workers 4
python3 scripts/experiments/run_transforms.py gpt-5.2 --workers 4

# Compute results
python3 scripts/evaluation-results/rq1/compute_leaderboard.py
python3 scripts/evaluation-results/rq4/compute_ari.py

# Launch dashboard
cd dashboard && npm install && npm run dev
```

## Dashboard

Interactive exploration of all results, figures, and evaluations:

**Live:** https://victorious-glacier-00483810f.2.azurestaticapps.net

Three tabs: **Dataset** (browse figures, annotations, probes), **Evaluation** (MQM scores, transform comparisons), **Results** (leaderboards, analytics, cross-model charts).

## Environment Variables

| Variable | Required by | Description |
|----------|-------------|-------------|
| `OPENROUTER_API_KEY` | OpenRouter models | API key |
| `AZURE_OPENAI_ENDPOINT` | Azure models | Azure OpenAI resource URL |
| `AZURE_OPENAI_API_KEY` | Azure models | Azure OpenAI API key |
| `GCP_PROJECT` | Vertex AI | Google Cloud project ID |

All API calls use `temperature=0` for deterministic, reproducible outputs.

## Citation

```bibtex
@mastersthesis{oamen2026scifigeval,
  author  = {Oamen, Paul Osemudiame},
  title   = {SciFig-Eval: A Multilingual Benchmark and Behavioural Framework
             for Evaluating Vision-Language Models on Scientific Figures},
  school  = {University of Aberdeen},
  year    = {2026},
  type    = {MSc Thesis},
  department = {Department of Computing Science}
}
```

## License

This project is part of academic research at the University of Aberdeen. Dataset figures are sourced from publicly available scientific papers under fair-use provisions for research purposes.
