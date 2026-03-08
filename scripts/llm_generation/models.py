"""LLM model abstractions for figure description generation.

Each model implements the FigureAnnotator interface. To add a new model,
subclass FigureAnnotator and implement annotate_figure() and model_name.

GPT-5.2 routes through OpenRouter; Gemini 3.1 Pro uses Vertex AI directly.
"""

import base64
import os
import time
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class FigureAnnotator(ABC):
    """Abstract base class for LLM-based figure annotators."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...

    @property
    @abstractmethod
    def router_model_id(self) -> str:
        ...

    @abstractmethod
    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_name={self.model_name!r})"


def _encode_image_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _retry(func, max_retries: int = 3, backoff: float = 2.0):
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                raise
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= backoff


def _get_openrouter_client():
    from openai import OpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY environment variable is not set.")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def _get_vertex_client():
    from google import genai

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    if not project:
        raise EnvironmentError(
            "GOOGLE_CLOUD_PROJECT environment variable is not set. "
            "Set it to your GCP project ID."
        )
    return genai.Client(vertexai=True, project=project, location=location)


# ---------------------------------------------------------------------------
# GPT-5.2 via OpenRouter
# ---------------------------------------------------------------------------

class GPT52Annotator(FigureAnnotator):
    """GPT-5.2 via OpenRouter."""

    def __init__(self, max_tokens: int = 2048):
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return "gpt-5.2"

    @property
    def router_model_id(self) -> str:
        return "openai/gpt-5.2"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        client = _get_openrouter_client()
        b64 = _encode_image_base64(image_path)

        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        user_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            },
            {
                "type": "text",
                "text": user_text,
            },
        ]

        def _call():
            response = client.chat.completions.create(
                model=self.router_model_id,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()

        return _retry(_call)


# ---------------------------------------------------------------------------
# Gemini 3.1 Pro via Vertex AI
# ---------------------------------------------------------------------------

class Gemini31ProAnnotator(FigureAnnotator):
    """Gemini 3.1 Pro Preview via Vertex AI."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return "gemini-3.1-pro"

    @property
    def router_model_id(self) -> str:
        return "gemini-3.1-pro-preview"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        from google.genai import types

        client = _get_vertex_client()

        image_bytes = image_path.read_bytes()
        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        contents = [
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            user_text,
        ]

        def _call():
            response = client.models.generate_content(
                model=self.router_model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=self.max_tokens,
                ),
            )
            return response.text.strip()

        return _retry(_call)


# ---------------------------------------------------------------------------
# Llama 4 Maverick via OpenRouter
# ---------------------------------------------------------------------------

class Llama4MaverickAnnotator(FigureAnnotator):
    """Llama 4 Maverick via OpenRouter."""

    def __init__(self, max_tokens: int = 2048):
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return "llama4-maverick"

    @property
    def router_model_id(self) -> str:
        return "meta-llama/llama-4-maverick-17b-128e-instruct"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        client = _get_openrouter_client()
        b64 = _encode_image_base64(image_path)

        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        user_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            },
            {
                "type": "text",
                "text": user_text,
            },
        ]

        def _call():
            response = client.chat.completions.create(
                model=self.router_model_id,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()

        return _retry(_call)


# ---------------------------------------------------------------------------
# Generic OpenRouter annotator (for models that follow the standard pattern)
# ---------------------------------------------------------------------------

class OpenRouterAnnotator(FigureAnnotator):
    """Generic annotator for any model available via OpenRouter."""

    def __init__(self, name: str, router_id: str, max_tokens: int = 2048):
        self._model_name = name
        self._router_model_id = router_id
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def router_model_id(self) -> str:
        return self._router_model_id

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        client = _get_openrouter_client()
        b64 = _encode_image_base64(image_path)

        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        user_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            },
            {
                "type": "text",
                "text": user_text,
            },
        ]

        def _call():
            response = client.chat.completions.create(
                model=self.router_model_id,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()

        return _retry(_call)


def _openrouter_factory(name: str, router_id: str):
    """Create a factory function for an OpenRouter model."""
    def factory(**kwargs):
        return OpenRouterAnnotator(name, router_id, **kwargs)
    return factory


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

MODEL_REGISTRY: dict[str, type[FigureAnnotator]] = {
    "gpt-5.2": GPT52Annotator,
    "gemini-3.1-pro": Gemini31ProAnnotator,
    "llama4-maverick": Llama4MaverickAnnotator,
}

# Additional OpenRouter models (using generic annotator)
OPENROUTER_MODELS = {
    "qwen3-vl-8b": "qwen/qwen3-vl-8b-instruct",
    "qwen3-vl-30b-a3b": "qwen/qwen3-vl-30b-a3b-instruct",
    "qwen3-vl-235b-a22b": "qwen/qwen3-vl-235b-a22b-instruct",
    "llama4-scout": "meta-llama/llama-4-scout",
    "gemma3-4b-it": "google/gemma-3-4b-it",
    "gemma3-12b-it": "google/gemma-3-12b-it",
    # Temporary OpenRouter fallbacks (normally these run on Vertex AI)
    "qwen3-vl-32b-or": "qwen/qwen3-vl-32b-instruct",
    "gemma3-27b-it-or": "google/gemma-3-27b-it",
}


def _get_all_models() -> dict:
    """Merge all model registries."""
    all_models = dict(MODEL_REGISTRY)
    # Add generic OpenRouter models
    for name, router_id in OPENROUTER_MODELS.items():
        all_models[name] = _openrouter_factory(name, router_id)
    try:
        from llm_generation.models_opensource import OPENSOURCE_MODEL_REGISTRY
        all_models.update(OPENSOURCE_MODEL_REGISTRY)
    except ImportError:
        pass
    return all_models


def get_annotator(model_name: str, **kwargs) -> FigureAnnotator:
    all_models = _get_all_models()
    if model_name not in all_models:
        available = ", ".join(sorted(all_models.keys()))
        raise ValueError(f"Unknown model {model_name!r}. Available: {available}")
    return all_models[model_name](**kwargs)
