"""LLM model abstractions for figure description generation.

Each model implements the FigureAnnotator interface. To add a new model,
subclass FigureAnnotator and implement annotate_figure() and model_name.

All models expect:
    - API keys via environment variables (never hardcoded)
    - A text prompt and a local image path
    - Return a string description
"""

import base64
import os
import time
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)


class FigureAnnotator(ABC):
    """Abstract base class for LLM-based figure annotators."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Short identifier for this model (used in filenames and logs)."""
        ...

    @abstractmethod
    def annotate_figure(self, prompt: str, image_path: Path, caption: str) -> str:
        """Generate a text description of a scientific figure.

        Args:
            prompt: The system/instruction prompt for figure description.
            image_path: Path to the figure image file (PNG).
            caption: The original figure caption from the paper.

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


# ---------------------------------------------------------------------------
# GPT-4o-mini (OpenAI) — quick test model
# ---------------------------------------------------------------------------

class GPT4oMiniAnnotator(FigureAnnotator):
    """OpenAI GPT-4o-mini annotator."""

    def __init__(self, max_tokens: int = 1024):
        self.max_tokens = max_tokens
        self._api_key = os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

    @property
    def model_name(self) -> str:
        return "gpt-4o-mini"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self._api_key)
        b64 = _encode_image_base64(image_path)

        user_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            },
            {
                "type": "text",
                "text": f"Caption: {caption}",
            },
        ]

        def _call():
            response = client.chat.completions.create(
                model="gpt-4o-mini",
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
