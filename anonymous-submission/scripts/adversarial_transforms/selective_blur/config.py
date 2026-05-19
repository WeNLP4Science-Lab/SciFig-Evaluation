"""Configuration for selective blur pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[4] / ".env")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = PROJECT_ROOT / "dataset"
FIGURES_DIR = DATASET_DIR / "figures"
ADVERSARIAL_DIR = DATASET_DIR / "adversarial"
ADMITTANCE_DIR = ADVERSARIAL_DIR / "admittance"
INDUCTANCE_DIR = ADVERSARIAL_DIR / "inductance"
PROMPTS_DIR = Path(__file__).parent / "prompts"

# Results
RESULTS_DIR = PROJECT_ROOT / "results" / "adversarial_transforms" / "selective_blur"
OCR_DIR = RESULTS_DIR / "ocr_results"
IDENTIFICATIONS_DIR = RESULTS_DIR / "identifications"

# Azure OpenAI
AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_API_VERSION = "2024-12-01-preview"

# Model
MODEL = "gpt-4o"
TEMPERATURE = 0

# Blur settings
BLUR_KERNEL = 75  # must be odd
BLUR_GRAY_BLEND = 0.7  # 0 = no gray fill, 1 = full gray fill before blur
