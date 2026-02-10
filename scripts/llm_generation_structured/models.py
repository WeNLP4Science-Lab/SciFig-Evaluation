"""LLM model abstractions for structured figure description generation.

Same architecture as llm_generation/models.py but requests JSON output
containing both a description paragraph and a structured breakdown.
"""

import base64
import json
import os
import re
import time
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class FigureAnnotator(ABC):
    """Abstract base class for structured LLM-based figure annotators."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...

    @property
    @abstractmethod
    def router_model_id(self) -> str:
        ...

    @abstractmethod
    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> dict:
        """Generate a structured description of a scientific figure.

        Returns:
            dict with "description" (str) and "breakdown" (dict) keys.
        """
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


def _extract_json(text: str) -> dict:
    """Extract JSON from model response, handling markdown fences."""
    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown code fences
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from model response: {text[:200]}...")


# ---------------------------------------------------------------------------
# GPT-4o-mini via OpenRouter (structured output)
# ---------------------------------------------------------------------------

class GPT4oMiniAnnotator(FigureAnnotator):
    """GPT-4o-mini via OpenRouter — structured output."""

    def __init__(self, max_tokens: int = 2048):
        self.max_tokens = max_tokens

    @property
    def model_name(self) -> str:
        return "gpt-4o-mini"

    @property
    def router_model_id(self) -> str:
        return "openai/gpt-4o-mini"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> dict:
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
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content.strip()
            return _extract_json(raw)

        return _retry(_call)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

MODEL_REGISTRY: dict[str, type[FigureAnnotator]] = {
    "gpt-4o-mini": GPT4oMiniAnnotator,
}


def get_annotator(model_name: str, **kwargs) -> FigureAnnotator:
    if model_name not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY.keys()))
        raise ValueError(f"Unknown model {model_name!r}. Available: {available}")
    return MODEL_REGISTRY[model_name](**kwargs)
