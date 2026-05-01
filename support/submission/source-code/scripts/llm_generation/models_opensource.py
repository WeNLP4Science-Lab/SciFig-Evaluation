"""Open-source LLM model abstractions for figure description generation.

Models deployed on Vertex AI Model Garden (vLLM endpoints) or via OpenRouter.
Each model implements the FigureAnnotator interface from models.py.
"""

import os
import logging
from pathlib import Path

import google.auth
import google.auth.transport.requests
import requests as http_requests

from llm_generation.models import (
    FigureAnnotator,
    _encode_image_base64,
    _retry,
)

logger = logging.getLogger(__name__)


def _get_vertex_predict_url(endpoint_id: str, dedicated_dns: str, region: str, project: str) -> str:
    """Build the Vertex AI predict URL for a dedicated Model Garden endpoint."""
    return (
        f"https://{dedicated_dns}/v1/"
        f"projects/{project}/locations/{region}/endpoints/{endpoint_id}:predict"
    )


def _get_gcp_token() -> str:
    """Get a fresh GCP access token via ADC."""
    credentials, _ = google.auth.default()
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


# ---------------------------------------------------------------------------
# Gemma 3 27B-IT via Vertex AI Model Garden
# ---------------------------------------------------------------------------

class Gemma3Annotator(FigureAnnotator):
    """Gemma 3 27B-IT via Vertex AI Model Garden (vLLM endpoint)."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.endpoint_id = os.environ.get("VERTEX_ENDPOINT_GEMMA3")
        self.dedicated_dns = os.environ.get("VERTEX_ENDPOINT_GEMMA3_DNS")
        self.region = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")
        self.project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.endpoint_id or not self.dedicated_dns:
            raise EnvironmentError(
                "VERTEX_ENDPOINT_GEMMA3 and VERTEX_ENDPOINT_GEMMA3_DNS must be set. "
                "VERTEX_ENDPOINT_GEMMA3=endpoint ID, "
                "VERTEX_ENDPOINT_GEMMA3_DNS=dedicatedEndpointDns value."
            )
        if not self.project:
            raise EnvironmentError(
                "GOOGLE_CLOUD_PROJECT environment variable is not set."
            )

    @property
    def model_name(self) -> str:
        return "gemma3-27b-it"

    @property
    def router_model_id(self) -> str:
        return "google/gemma-3-27b-it"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        b64 = _encode_image_base64(image_path)
        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        url = _get_vertex_predict_url(self.endpoint_id, self.dedicated_dns, self.region, self.project)

        payload = {
            "instances": [
                {
                    "@requestFormat": "chatCompletions",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{b64}"},
                                },
                                {
                                    "type": "text",
                                    "text": user_text,
                                },
                            ],
                        },
                    ],
                    "max_tokens": self.max_tokens,
                }
            ]
        }

        def _call():
            token = _get_gcp_token()
            resp = http_requests.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            # Vertex AI wraps the chat completion in "predictions"
            pred = data.get("predictions", {})
            choices = pred.get("choices", [])
            if choices:
                return choices[0]["message"]["content"].strip()
            raise ValueError(f"Unexpected response format: {data}")

        return _retry(_call)


# ---------------------------------------------------------------------------
# Qwen3-VL 32B via Vertex AI Model Garden
# ---------------------------------------------------------------------------

class Qwen3VLAnnotator(FigureAnnotator):
    """Qwen3-VL 32B Instruct via Vertex AI Model Garden (vLLM endpoint)."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.endpoint_id = os.environ.get("VERTEX_ENDPOINT_QWEN3_VL")
        self.dedicated_dns = os.environ.get("VERTEX_ENDPOINT_QWEN3_VL_DNS")
        self.region = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")
        self.project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.endpoint_id or not self.dedicated_dns:
            raise EnvironmentError(
                "VERTEX_ENDPOINT_QWEN3_VL and VERTEX_ENDPOINT_QWEN3_VL_DNS must be set."
            )
        if not self.project:
            raise EnvironmentError(
                "GOOGLE_CLOUD_PROJECT environment variable is not set."
            )

    @property
    def model_name(self) -> str:
        return "qwen3-vl-32b"

    @property
    def router_model_id(self) -> str:
        return "qwen/qwen3-vl-32b-instruct"

    def annotate_figure(self, prompt: str, image_path: Path, caption: str, paper_title: str = "") -> str:
        b64 = _encode_image_base64(image_path)
        user_text = f"Paper: {paper_title}\nCaption: {caption}" if paper_title else f"Caption: {caption}"

        url = _get_vertex_predict_url(self.endpoint_id, self.dedicated_dns, self.region, self.project)

        payload = {
            "instances": [
                {
                    "@requestFormat": "chatCompletions",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{b64}"},
                                },
                                {
                                    "type": "text",
                                    "text": user_text,
                                },
                            ],
                        },
                    ],
                    "max_tokens": self.max_tokens,
                }
            ]
        }

        def _call():
            token = _get_gcp_token()
            resp = http_requests.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            pred = data.get("predictions", {})
            choices = pred.get("choices", [])
            if choices:
                return choices[0]["message"]["content"].strip()
            raise ValueError(f"Unexpected response format: {data}")

        return _retry(_call)


# ---------------------------------------------------------------------------
# Registry (open-source models only)
# ---------------------------------------------------------------------------

OPENSOURCE_MODEL_REGISTRY: dict[str, type[FigureAnnotator]] = {
    "gemma3-27b-it": Gemma3Annotator,
    "qwen3-vl-32b": Qwen3VLAnnotator,
}
