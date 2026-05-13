"""Configuration for the capability question generation pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# ── Paths ──
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "dataset"
FIGURES_DIR = DATASET_DIR / "figures"
GROUNDTRUTH_DIR = DATASET_DIR / "groundtruth"
FINAL_OUTPUT_DIR = DATASET_DIR / "capability_questions"
PROMPTS_DIR = Path(__file__).parent / "prompts"

# Results (intermediate artifacts)
RESULTS_DIR = PROJECT_ROOT / "results" / "capability_generation"
GENERATION_DIR = RESULTS_DIR / "generation"
VALIDATION_DIR = RESULTS_DIR / "validation"

# ── Azure OpenAI ──
AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_API_VERSION = "2024-12-01-preview"

# ── OpenRouter (fallback for Mistral) ──
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# ── Models ──
GENERATOR_MODEL = "gpt-4o"                        # question generation (Azure)
VALIDATOR_MODEL = "mistralai/mistral-large-2512"   # validation (OpenRouter)
VALIDATOR_BACKEND = "openrouter"                   # "azure" or "openrouter"

# ── Generation settings ──
TEMPERATURE = 0
MAX_TOKENS = 2048
CATEGORIES = ["counting", "computation", "comparison", "pattern_analysis"]
