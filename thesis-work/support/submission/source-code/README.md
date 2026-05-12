# SciFig-Eval: Source Code

**MSc Artificial Intelligence Thesis — University of Aberdeen, 2026**

Paul Osemudiame Oamen

## Contents

This archive contains the source code for the SciFig-Eval project:

- `scripts/` — All Python scripts for generation, evaluation, experiments, and results computation
- `HumanEval/` — Label Studio exports and human evaluation data
- `atomic_mqm/` — Atomic MQM decomposition checklists and scoring configuration
- `adversarial_experiments/` — Adversarial probe benchmarks and sample manifests
- `Dataset/groundtruth/` — JSON annotations for all 1,005 figures
- `dashboard/` — React + Vite + Tailwind interactive dashboard source code

## Items on GitHub (excluded due to size)

The following are available in the full repository but excluded from this archive due to file size:

- `Dataset/figures/` — 1,005 PNG figure images (~80MB)
- `output/` — All model generation outputs, evaluation results, and experiment data (~476MB)
- `dashboard/public/` — Exported dashboard data and figure images (~200MB)

## Full Repository

The complete repository, including all figures, outputs, and evaluation data, is publicly available at:

**https://github.com/WeNLP4Science-Lab/SciFig-Evaluation**

## Dashboard

Live dashboard: https://victorious-glacier-00483810f.2.azurestaticapps.net

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install openai google-genai python-dotenv numpy matplotlib scipy seaborn
```

Create a `.env` file with API credentials (see Appendix B of the thesis for details).
