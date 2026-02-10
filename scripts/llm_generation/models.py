"""LLM model abstractions for figure description generation.

Each model implements the FigureAnnotator interface. To add a new model,
subclass FigureAnnotator and implement annotate_figure() and model_name.

All models route through OpenRouter (https://openrouter.ai).
Set the OPENROUTER_API_KEY environment variable before use.
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
        """Short identifier for this model (used in filenames and logs)."""
        ...

    @property
    @abstractmethod
    def router_model_id(self) -> str:
        """OpenRouter model identifier (e.g. 'openai/gpt-4o-mini')."""
        ...

    @abstractmethod
    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        """Generate a text description of a scientific figure.

        Args:
            prompt: The system/instruction prompt for figure description.
            image_path: Path to the figure image file (PNG).
            caption: The original figure caption from the paper.
            paper_title: Title of the source paper (provides context).

        Returns:
            Generated figure description as a string.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_name={self.model_name!r})"


def _encode_image_base64(image_path: Path) -> str:
    """Read an image file and return its base64-encoded string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _retry(func, max_retries: int = 3, backoff: float = 2.0):
    """Simple retry wrapper with exponential backoff."""
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
    """Create an OpenAI client pointed at OpenRouter."""
    from openai import OpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY environment variable is not set.")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


# ---------------------------------------------------------------------------
# GPT-4o-mini via OpenRouter
# ---------------------------------------------------------------------------

class GPT4oMiniAnnotator(FigureAnnotator):
    """GPT-4o-mini via OpenRouter."""

    def __init__(self, max_tokens: int = 1024):
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return "gpt-4o-mini"

    @property
    def router_model_id(self) -> str:
        return "openai/gpt-4o-mini"

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
# Registry — maps model_name strings to annotator classes
# ---------------------------------------------------------------------------

MODEL_REGISTRY: dict[str, type[FigureAnnotator]] = {
    "gpt-4o-mini": GPT4oMiniAnnotator,
}


def get_annotator(model_name: str, **kwargs) -> FigureAnnotator:
    """Instantiate an annotator by model name.

    Args:
        model_name: Key from MODEL_REGISTRY (e.g. "gpt-4o-mini").
        **kwargs: Passed to the annotator constructor.

    Returns:
        An instance of the requested FigureAnnotator.

    Raises:
        ValueError: If model_name is not in the registry.
    """
    if model_name not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY.keys()))
        raise ValueError(f"Unknown model {model_name!r}. Available: {available}")
    return MODEL_REGISTRY[model_name](**kwargs)
