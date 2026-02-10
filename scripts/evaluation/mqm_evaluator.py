"""Core MQM evaluation logic — LLM-as-judge for figure annotation quality.

Uses the MQM (Multidimensional Quality Metrics) framework from the project's
human evaluation guidelines. An LLM judge examines the figure image and
evaluates the model-generated annotation against it.

This module is shared by both evaluate_unstructured.py and evaluate_structured.py.
"""

import base64
import json
import os
import re
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# MQM weights from the guidelines (Table 2)
MQM_WEIGHTS = {
    ("Accuracy", "Major"): 5.0,
    ("Accuracy", "Minor"): 2.0,
    ("Completeness", "Major"): 3.5,
    ("Completeness", "Minor"): 1.5,
    ("Clarity and Readability", "Major"): 2.0,
    ("Clarity and Readability", "Minor"): 1.0,
}

VALID_CATEGORIES = {"Accuracy", "Completeness", "Clarity and Readability"}
VALID_SEVERITIES = {"Major", "Minor"}
VALID_SUB_TYPES = {
    "Accuracy": {
        "Incorrect Numerical Value",
        "Incorrect Trend Interpretation",
        "Incorrect Axis or Legend Interpretation",
        "Incorrect Label Mapping",
    },
    "Completeness": {
        "Missing Key Information",
        "Hallucinated Content",
    },
    "Clarity and Readability": {
        "Ambiguous Description",
        "Missing Takeaway",
        "Over-Generalization",
        "Overly Verbose Description",
        "Poor Sentence Structure",
    },
}

MQM_JUDGE_PROMPT = """\
You are an expert evaluator assessing the quality of a machine-generated scientific figure description.

## Your Task
Examine the provided figure image carefully. Then evaluate the machine-generated description against WHAT YOU ACTUALLY SEE in the figure. Identify ALL errors.

## MQM Error Categories

### Accuracy Errors
- **Incorrect Numerical Value**: Reports incorrect numbers, percentages, or quantities.
- **Incorrect Trend Interpretation**: Misrepresents the overall pattern or direction of data.
- **Incorrect Axis or Legend Interpretation**: Incorrectly describes axis labels, units, or legend.
- **Incorrect Label Mapping**: Assigns wrong category names to visual elements (bars, lines, pie segments).

### Completeness Errors
- **Missing Key Information**: Omits essential elements (major data points, axis labels, units, key categories).
- **Hallucinated Content**: Introduces information or visual elements that do not exist in the figure.

### Clarity and Readability Errors
- **Ambiguous Description**: Contains vague or unclear references.
- **Missing Takeaway**: Fails to summarize the main pattern or insight.
- **Over-Generalization**: Oversimplifies or exaggerates visual information.
- **Overly Verbose Description**: Unnecessary repetition or excessive detail.
- **Poor Sentence Structure**: Grammatical errors or awkward phrasing.

## Severity Levels
- **Major**: Makes the description factually unusable or misleading, or significantly degrades scientific correctness.
- **Minor**: Stylistic or readability issues that do not affect core factual meaning.

## Instructions
1. Examine the figure image thoroughly — note axes, labels, data series, values, colors, legends, trends.
2. Read the machine-generated description.
3. Compare each claim in the description against what you see in the figure.
4. Identify ALL errors. Be thorough but fair — minor approximations in numerical values are acceptable.
5. For each error, classify by category, sub_type, and severity, and provide specific evidence.

## Output Format
Return a JSON object with this exact structure:
{
  "errors": [
    {
      "category": "Accuracy",
      "sub_type": "Incorrect Numerical Value",
      "severity": "Major",
      "evidence": "Description says 60% but figure shows approximately 45%"
    }
  ]
}

If there are no errors, return: {"errors": []}
Return ONLY the JSON object. No extra text."""


def _get_client():
    from openai import OpenAI
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY environment variable is not set.")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def _encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from judge response: {text[:300]}...")


def _retry(func, max_retries: int = 3, backoff: float = 2.0):
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


def compute_mqm_score(errors: list[dict]) -> tuple[float, float]:
    """Compute MQM score from a list of errors.

    Returns:
        (mqm_score, total_penalty) where mqm_score = max(0, 100 - total_penalty)
    """
    total_penalty = 0.0
    for err in errors:
        cat = err.get("category", "")
        sev = err.get("severity", "")
        weight = MQM_WEIGHTS.get((cat, sev), 0.0)
        total_penalty += weight
    mqm_score = max(0.0, 100.0 - total_penalty)
    return mqm_score, total_penalty


def validate_errors(errors: list[dict]) -> list[dict]:
    """Normalize and validate error entries from the LLM judge."""
    validated = []
    for err in errors:
        cat = err.get("category", "")
        sub = err.get("sub_type", "")
        sev = err.get("severity", "")

        # Normalize category
        if cat not in VALID_CATEGORIES:
            for valid_cat in VALID_CATEGORIES:
                if valid_cat.lower() in cat.lower():
                    cat = valid_cat
                    break

        # Normalize severity
        if sev not in VALID_SEVERITIES:
            sev = "Minor"  # default to Minor if unclear

        validated.append({
            "category": cat,
            "sub_type": sub,
            "severity": sev,
            "weight": MQM_WEIGHTS.get((cat, sev), 0.0),
            "evidence": err.get("evidence", ""),
        })
    return validated


def evaluate_annotation(
    image_path: Path,
    annotation: str,
    caption: str,
    paper_title: str = "",
    figure_type: str = "",
    judge_model: str = "openai/gpt-4o-mini",
    max_tokens: int = 2048,
) -> dict:
    """Evaluate a single annotation against its figure using MQM.

    Args:
        image_path: Path to the figure image.
        annotation: The model-generated description to evaluate.
        caption: Original figure caption from the paper.
        paper_title: Title of the source paper.
        figure_type: Type of figure (Line Plot, Bar Chart, etc.).
        judge_model: OpenRouter model ID for the judge.
        max_tokens: Max tokens for judge response.

    Returns:
        dict with errors, mqm_score, total_penalty.
    """
    client = _get_client()
    b64 = _encode_image(image_path)

    context_parts = []
    if paper_title:
        context_parts.append(f"Paper: {paper_title}")
    if caption:
        context_parts.append(f"Caption: {caption}")
    if figure_type:
        context_parts.append(f"Figure type: {figure_type}")
    context_parts.append(f"\n--- Machine-generated description to evaluate ---\n{annotation}")
    user_text = "\n".join(context_parts)

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
            model=judge_model,
            messages=[
                {"role": "system", "content": MQM_JUDGE_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content.strip()
        return _extract_json(raw)

    result = _retry(_call)
    errors = validate_errors(result.get("errors", []))
    mqm_score, total_penalty = compute_mqm_score(errors)

    return {
        "errors": errors,
        "mqm_score": round(mqm_score, 2),
        "total_penalty": round(total_penalty, 2),
        "error_count": len(errors),
        "judge_model": judge_model,
    }
