"""Backend routing for LLM judge models.

Resolves a judge model identifier (e.g. "openai/gpt-4o-mini", "azure/gpt-4o",
"gemini-3.1-pro") to the correct backend and client configuration.

Configuration is loaded from judge_backends.json in the same directory.
"""

import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_CONFIG_PATH = Path(__file__).parent / "judge_backends.json"
_config = None


def _load_config():
    global _config
    if _config is None:
        with open(_CONFIG_PATH) as f:
            _config = json.load(f)
    return _config


def resolve_backend(judge_model: str) -> tuple:
    """Resolve a judge model string to (backend_type, backend_config, model_id).

    Routes are matched by prefix in order. The first match wins.
    If strip_prefix is true, the prefix is removed from the model_id
    passed to the API.
    """
    config = _load_config()

    for route in config["routes"]:
        prefix = route["prefix"]
        if prefix == "*" or judge_model.startswith(prefix):
            backend_name = route["backend"]
            backend_config = config["backends"][backend_name]
            model_id = judge_model[len(prefix):] if route.get("strip_prefix") else judge_model
            return backend_config["type"], backend_config, model_id

    raise ValueError(f"No backend route matched for judge model: {judge_model}")


def get_openai_compat_client(backend_config: dict):
    """Create an OpenAI-compatible client (works for OpenRouter and Azure)."""
    api_key = os.environ.get(backend_config["api_key_env"])
    if not api_key:
        raise EnvironmentError(
            f"{backend_config['api_key_env']} environment variable is not set."
        )

    if backend_config.get("azure"):
        from openai import AzureOpenAI
        endpoint = os.environ.get(backend_config["endpoint_env"])
        if not endpoint:
            raise EnvironmentError(
                f"{backend_config['endpoint_env']} environment variable is not set."
            )
        return AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=backend_config.get("api_version", "2024-12-01-preview"),
        )
    else:
        from openai import OpenAI
        return OpenAI(
            base_url=backend_config["base_url"],
            api_key=api_key,
        )


def get_vertex_client(backend_config: dict, model: str = ""):
    """Create a Google GenAI / Vertex AI client."""
    from google import genai
    project = os.environ.get(
        backend_config.get("project_env", ""),
        backend_config.get("project_default", ""),
    )
    location = backend_config.get("location", "us-central1")
    # Gemini 3+ preview models require location='global'
    if "preview" in model or "gemini-3" in model:
        location = "global"
    return genai.Client(vertexai=True, project=project, location=location)
