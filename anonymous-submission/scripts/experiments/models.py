"""Shared model calling utilities for all experiment scripts."""

from __future__ import annotations

import base64
import time
import logging
from pathlib import Path

from config import (
    MODELS, TEMPERATURE, MAX_TOKENS, AZURE_API_VERSION,
    OPENROUTER_BASE_URL,
    get_azure_endpoint, get_azure_api_key, get_openrouter_api_key,
)

logger = logging.getLogger(__name__)


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def retry(func, max_retries=3, backoff=2.0):
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= backoff


def call_vlm(model_name: str, system_prompt: str, image_path: Path,
             user_text: str = "", temperature: float = TEMPERATURE) -> str:
    """Send image + text to a VLM and return the response text."""
    cfg = MODELS[model_name]
    b64 = encode_image(image_path)
    max_tok = cfg.get("max_tokens", MAX_TOKENS)

    user_content = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
    ]
    if user_text:
        user_content.append({"type": "text", "text": user_text})

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    def _call():
        if cfg["backend"] == "azure":
            from openai import AzureOpenAI
            client = AzureOpenAI(
                azure_endpoint=get_azure_endpoint(),
                api_key=get_azure_api_key(),
                api_version=AZURE_API_VERSION,
            )
            token_param = "max_completion_tokens" if any(
                v in cfg["model_id"] for v in ["gpt-5", "gpt-4.1"]
            ) else "max_tokens"
            response = client.chat.completions.create(
                model=cfg["model_id"],
                messages=messages,
                temperature=temperature,
                **{token_param: max_tok},
            )
        else:
            from openai import OpenAI
            client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=get_openrouter_api_key())
            response = client.chat.completions.create(
                model=cfg["model_id"],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tok,
            )
        return response.choices[0].message.content.strip()

    return retry(_call)


def call_llm(model_name: str, system_prompt: str, user_text: str,
             temperature: float = TEMPERATURE, json_mode: bool = False) -> str:
    """Send text-only prompt to an LLM and return the response text."""
    cfg = MODELS[model_name]
    max_tok = cfg.get("max_tokens", MAX_TOKENS)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]

    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    def _call():
        if cfg["backend"] == "azure":
            from openai import AzureOpenAI
            client = AzureOpenAI(
                azure_endpoint=get_azure_endpoint(),
                api_key=get_azure_api_key(),
                api_version=AZURE_API_VERSION,
            )
            token_param = "max_completion_tokens" if any(
                v in cfg["model_id"] for v in ["gpt-5", "gpt-4.1"]
            ) else "max_tokens"
            response = client.chat.completions.create(
                model=cfg["model_id"],
                messages=messages,
                temperature=temperature,
                **{token_param: max_tok},
                **kwargs,
            )
        else:
            from openai import OpenAI
            client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=get_openrouter_api_key())
            response = client.chat.completions.create(
                model=cfg["model_id"],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tok,
                **kwargs,
            )
        return response.choices[0].message.content.strip()

    return retry(_call)
