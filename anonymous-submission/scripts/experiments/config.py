"""Shared configuration for all ACL experiments.

Models (8): Gemini 3.1, GPT-5.2, Llama 4, Qwen 235B, Qwen 30B, Qwen 8B, Gemma 27B, Phi 5
Routing:    GPT-5.2 + Phi-5 on Azure; all others on OpenRouter
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# ── Paths ──
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "dataset"
FIGURES_DIR = DATASET_DIR / "figures"
GROUNDTRUTH_DIR = DATASET_DIR / "groundtruth"
ADVERSARIAL_DIR = DATASET_DIR / "adversarial"

RESULTS_DIR = PROJECT_ROOT / "results"
DESCRIPTIONS_DIR = RESULTS_DIR / "generation" / "description_tasks" / "baseline_descriptions"

# Prior generation outputs (1,005-figure dataset, for import into 250-figure subset)
PRIOR_ROOT = Path(__file__).resolve().parents[3] / "thesis-work"
PRIOR_GENERATION_DIR = PRIOR_ROOT / "output" / "generation"
PRIOR_EXPERIMENTS_DIR = PRIOR_ROOT / "output" / "experiments"

# ── Prompts ──
PROMPTS_DIR = Path(__file__).parent / "prompts"

# ── Azure OpenAI (lazy-loaded for scripts that don't need API access) ──
AZURE_API_VERSION = "2024-12-01-preview"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_azure_endpoint():
    return os.environ["AZURE_OPENAI_ENDPOINT"]


def get_azure_api_key():
    return os.environ["AZURE_OPENAI_API_KEY"]


def get_openrouter_api_key():
    return os.environ.get("OPENROUTER_API_KEY", "")

# ── Generation settings ──
TEMPERATURE = 0
MAX_TOKENS = 2048

# ── Model definitions ──
# Each model: (display_name, backend, model_id, thesis_dir_name)
# backend: "azure" or "openrouter"
MODELS = {
    "gemini-3.1-pro": {
        "backend": "openrouter",
        "model_id": "google/gemini-3.1-pro-preview",
        "thesis_name": "gemini-3.1-pro",
        "max_tokens": 16000,
    },
    "gpt-5.2": {
        "backend": "azure",
        "model_id": "gpt-5-2",
        "thesis_name": "gpt-5.2",
    },
    "llama4-maverick": {
        "backend": "openrouter",
        "model_id": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "thesis_name": "llama4-maverick",
    },
    "qwen3-vl-235b-a22b": {
        "backend": "openrouter",
        "model_id": "qwen/qwen3-vl-235b-a22b-instruct",
        "thesis_name": "qwen3-vl-235b-a22b",
    },
    "qwen3-vl-30b-a3b": {
        "backend": "openrouter",
        "model_id": "qwen/qwen3-vl-30b-a3b-instruct",
        "thesis_name": "qwen3-vl-30b-a3b",
    },
    "qwen3-vl-8b": {
        "backend": "openrouter",
        "model_id": "qwen/qwen3-vl-8b-instruct",
        "thesis_name": "qwen3-vl-8b",
    },
    "gemma3-27b-it": {
        "backend": "openrouter",
        "model_id": "google/gemma-3-27b-it",
        "thesis_name": "gemma3-27b-it",
    },
    "phi-4-multimodal": {
        "backend": "azure",
        "model_id": "phi-4-multimodal",
        "thesis_name": None,  # no prior outputs
    },
}

# ── ACL-to-thesis figure mapping ──
def load_figure_mapping() -> dict[str, str]:
    """Return {acl_fig_id: thesis_fig_key} for all 250 figures."""
    import json
    mapping = {}
    for gt_file in sorted(GROUNDTRUTH_DIR.glob("*.json")):
        fig_id = gt_file.stem
        with open(gt_file) as f:
            data = json.load(f)
        orig = data.get("original_file", "")
        if orig:
            mapping[fig_id] = orig.replace(".json", "")
    return mapping


def get_thesis_subfolder(thesis_key: str) -> str:
    """Return the thesis subfolder for a given thesis figure key."""
    if thesis_key.startswith("english_"):
        return "english_only"
    elif thesis_key.startswith("multi_"):
        return "multi_language"
    elif thesis_key.startswith("bulgarian_"):
        return "bulgarian_only"
    elif thesis_key.startswith("chinese_"):
        return "chinese_only"
    elif thesis_key.startswith("german_"):
        return "german_only"
    return "english_only"
