"""Core MQM evaluation logic — LLM-as-judge for figure annotation quality.

Uses the MQM (Multidimensional Quality Metrics) framework from the project's
human evaluation guidelines. Supports three judge configurations:

  Reference-free: image + generation prompt + caption + model output (no groundtruth)
  Reference-only: groundtruth annotation + model output (no image)
  Reference-with-image: image + groundtruth annotation + model output
"""

import base64
import json
import os
import re
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from evaluation.judge_backends import resolve_backend, get_openai_compat_client, get_vertex_client

logger = logging.getLogger(__name__)

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
        "Incorrect Axis or Legend Interpretation",
        "Incorrect Visual Attribute Mapping",
        "Incorrect Structural Description",
    },
    "Completeness": {
        "Missing Chart Purpose",
        "Missing Axis Description",
        "Missing Visual Features",
        "Hallucinated Content",
        "Unwanted Interpretation",
    },
    "Clarity and Readability": {
        "Ambiguous Description",
        "Over-Generalization",
        "Overly Verbose Description",
        "Poor Sentence Structure",
    },
}

_MQM_ERROR_CATEGORIES = """\
## MQM Error Categories

### Accuracy Errors
- **Incorrect Numerical Value**: Reports incorrect numbers, percentages, or quantities. Example: Reporting "60%" when the plot shows approximately "45%".
- **Incorrect Axis or Legend Interpretation**: Incorrectly describes axis labels, units, or legend information. Example: Stating that the x-axis represents temperature when it represents time.
- **Incorrect Visual Attribute Mapping**: Assigns incorrect category names, series, values, marker shapes, or labels to visual elements such as bars, lines, pie segments, or datasets. Example: Assigning the blue bar to Method A when it corresponds to Method B.
- **Incorrect Structural Description**: Misrepresents the structural organization of the chart. Example: Describing grouped bars as stacked, reporting 5 slices when 4 exist, or misstating axis orientation.

### Completeness Errors
- **Missing Chart Purpose**: The description does not state what the chart represents based on visible labels or title.
- **Missing Axis Description**: Omits essential axis information such as axis labels, units, scale type, value range, or tick intervals.
- **Missing Visual Features**: Misses visual and stylistic features such as grouped/stacked structure, legend presence, sorting or ordering, or visual emphasis (highlighted bar, exploded slice).
- **Hallucinated Content**: Introduces information or visual elements that do not exist in the figure. Example: Stating that the chart contains five categories when only four are present.
- **Unwanted Interpretation**: Includes interpretation or inference beyond what is explicitly shown in the figure, introduces comparisons not explicitly indicated in the chart, or uses subjective or evaluative language (e.g., "significant increase").

### Clarity and Readability Errors
- **Ambiguous Description**: Contains vague or unclear references. Example: Using phrases such as "this increases significantly" without specifying the subject.
- **Over-Generalization**: Oversimplifies or exaggerates visual information. Example: Claiming that all methods perform similarly despite visible variation.
- **Overly Verbose Description**: Contains unnecessary repetition or excessive detail that does not add informational value.
- **Poor Sentence Structure**: Contains grammatical errors or awkward phrasing that reduces readability.

## Severity Levels
- **Major**: Errors that make the description factually unusable or misleading, or significantly degrade usability or scientific correctness.
- **Minor**: Stylistic or readability issues that do not affect the core factual meaning of the annotation."""

# Sub-types where the error refers to MISSING information (no text span to highlight)
NON_ANNOTATABLE_SUB_TYPES = {
    "Missing Chart Purpose",
    "Missing Axis Description",
    "Missing Visual Features",
}

_MQM_OUTPUT_FORMAT = """\
## Output Format
Return a JSON object with this exact structure:
{
  "errors": [
    {
      "category": "Accuracy",
      "sub_type": "Incorrect Numerical Value",
      "severity": "Major",
      "text_span": "with a final value of 60%",
      "evidence": "Description says 60% but figure shows approximately 45%"
    },
    {
      "category": "Completeness",
      "sub_type": "Missing Axis Description",
      "severity": "Major",
      "text_span": null,
      "evidence": "The description does not mention the y-axis units (percentage)"
    }
  ]
}

## text_span rules
- For errors about INCORRECT or UNWANTED content (Accuracy errors, Hallucinated Content, Unwanted Interpretation, all Clarity errors): set "text_span" to the EXACT substring from the machine-generated description that contains the error. Copy it verbatim — do not paraphrase.
- For errors about MISSING content (Missing Chart Purpose, Missing Axis Description, Missing Visual Features): set "text_span" to null, since there is no text to highlight.

If there are no errors, return: {"errors": []}
Return ONLY the JSON object. No extra text."""

# ---------------------------------------------------------------------------
# Reference-free (image + generation prompt + caption + model output, no groundtruth)
# ---------------------------------------------------------------------------
JUDGE_A_PROMPT = f"""\
You are an expert evaluator assessing the quality of a machine-generated scientific figure description.

## Your Task
Examine the provided figure image carefully. You are also given the GENERATION PROMPT that was used to instruct the model — this defines what the description should cover. Evaluate the machine-generated description against WHAT YOU ACTUALLY SEE in the figure AND whether it fulfills the requirements of the generation prompt. Identify ALL errors.

{_MQM_ERROR_CATEGORIES}

## Instructions
1. Examine the figure image thoroughly — note axes, labels, data series, values, colors, legends, trends.
2. Read the generation prompt to understand what the model was asked to describe.
3. Read the machine-generated description.
4. Compare each claim in the description against what you see in the figure (for Accuracy).
5. Check whether the description covers everything the generation prompt requested (for Completeness). If the prompt asks for specific elements (e.g., axes, legend, colors, values) and the description omits them, flag as a Completeness error.
6. Identify ALL errors. Be thorough but fair — minor approximations in numerical values are acceptable.
7. For each error, classify by category, sub_type, and severity, and provide specific evidence.

{_MQM_OUTPUT_FORMAT}"""

# ---------------------------------------------------------------------------
# Reference-only (groundtruth + model output, no image)
# ---------------------------------------------------------------------------
JUDGE_B_PROMPT = f"""\
You are an expert evaluator assessing the quality of a machine-generated scientific figure description.

## Your Task
You are given a REFERENCE description written by a human expert and a MACHINE-GENERATED description of the same scientific figure. Compare the machine-generated description against the reference to identify errors.

Use the reference as the source of truth for what the figure contains, since you do not have access to the image.

{_MQM_ERROR_CATEGORIES}

## Instructions
1. Read the reference description carefully — it tells you what the figure actually shows.
2. Read the machine-generated description.
3. Compare each claim in the machine-generated description against the reference.
4. Any claim that contradicts the reference is an Accuracy error.
5. Any important information present in the reference but missing from the machine output is a Completeness error.
6. Any information in the machine output that is NOT mentioned in the reference should be flagged as Hallucinated Content (it may be fabricated since you cannot verify it visually).
7. Assess clarity and readability of the machine-generated description on its own merits.
8. For each error, classify by category, sub_type, and severity, and provide specific evidence.

{_MQM_OUTPUT_FORMAT}"""

# ---------------------------------------------------------------------------
# Reference-with-image (image + groundtruth + model output)
# ---------------------------------------------------------------------------
JUDGE_C_PROMPT = f"""\
You are an expert evaluator assessing the quality of a machine-generated scientific figure description.

## Your Task
You are given the FIGURE IMAGE, a REFERENCE description written by a human expert, and a MACHINE-GENERATED description. Use BOTH the image and the reference to evaluate the machine-generated description. Identify ALL errors.

The image is the primary source of truth. The reference description provides additional context about what a human expert considered important to mention.

{_MQM_ERROR_CATEGORIES}

## Instructions
1. Examine the figure image thoroughly — note axes, labels, data series, values, colors, legends, trends.
2. Read the reference description to understand what a human expert highlighted.
3. Read the machine-generated description.
4. Compare each claim in the machine-generated description against BOTH the image and the reference.
5. Identify ALL errors. Be thorough but fair — minor approximations in numerical values are acceptable.
6. Use the image to verify factual claims. Use the reference to identify important omissions.
7. For each error, classify by category, sub_type, and severity, and provide specific evidence.

{_MQM_OUTPUT_FORMAT}"""

# Keep backward compatibility
MQM_JUDGE_PROMPT = JUDGE_A_PROMPT




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

        # Handle text_span
        text_span = err.get("text_span")
        if text_span is not None:
            text_span = str(text_span).strip() if text_span else None
        # Force null for non-annotatable sub-types
        if sub in NON_ANNOTATABLE_SUB_TYPES:
            text_span = None

        validated.append({
            "category": cat,
            "sub_type": sub,
            "severity": sev,
            "weight": MQM_WEIGHTS.get((cat, sev), 0.0),
            "text_span": text_span,
            "evidence": err.get("evidence", ""),
        })
    return validated


def _build_context_text(annotation: str, caption: str = "", paper_title: str = "",
                        figure_type: str = "", reference: str = "",
                        generation_prompt: str = "") -> str:
    """Build the user-facing context text for the judge."""
    parts = []
    if paper_title:
        parts.append(f"Paper: {paper_title}")
    if caption:
        parts.append(f"Caption: {caption}")
    if figure_type:
        parts.append(f"Figure type: {figure_type}")
    if generation_prompt:
        parts.append(f"\n--- Generation prompt (given to the model) ---\n{generation_prompt}")
    if reference:
        parts.append(f"\n--- Reference description (human expert) ---\n{reference}")
    parts.append(f"\n--- Machine-generated description to evaluate ---\n{annotation}")
    return "\n".join(parts)


def _run_judge(client, judge_model: str, system_prompt: str,
               user_content, max_tokens: int = 2048) -> dict:
    """Call the judge LLM and return validated MQM result."""
    def _call():
        # Newer models (GPT-5.x+) use max_completion_tokens instead of max_tokens
        token_param = "max_completion_tokens" if any(v in judge_model for v in ["gpt-5", "gpt-4.1"]) else "max_tokens"
        response = client.chat.completions.create(
            model=judge_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            **{token_param: max_tokens},
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


def _run_judge_gemini(judge_model: str, system_prompt: str,
                      user_content_parts, backend_config: dict,
                      max_tokens: int = 32768) -> dict:
    """Call a Gemini model via Vertex AI and return validated MQM result."""
    from google.genai import types

    client = get_vertex_client(backend_config, judge_model)

    def _call():
        config_kwargs = {
            "system_instruction": system_prompt,
            "max_output_tokens": max_tokens,
            "response_mime_type": "application/json",
        }
        # Thinking models (2.5 Pro, etc.) need a thinking config to avoid truncation
        if "2.5" in judge_model or "2-5" in judge_model:
            config_kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_budget=4096,
            )
        response = client.models.generate_content(
            model=judge_model,
            contents=user_content_parts,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        raw = response.text.strip()
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


def _get_judge_result(judge_model: str, system_prompt: str, text_content: str,
                      image_path=None, max_tokens: int = 2048) -> dict:
    """Unified judge dispatcher. Routes to the correct backend."""
    backend_type, backend_config, model_id = resolve_backend(judge_model)

    if backend_type == "openai_compat":
        client = get_openai_compat_client(backend_config)
        user_content = []
        if image_path:
            b64 = _encode_image(image_path)
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
            })
        user_content.append({"type": "text", "text": text_content})
        return _run_judge(client, model_id, system_prompt, user_content, max_tokens)

    elif backend_type == "vertex_ai":
        from google.genai import types
        parts = []
        if image_path:
            parts.append(types.Part.from_bytes(
                data=Path(image_path).read_bytes(), mime_type="image/png",
            ))
        parts.append(text_content)
        # Vertex AI / Gemini needs higher token budget (thinking tokens are separate)
        return _run_judge_gemini(model_id, system_prompt, parts, backend_config, max_tokens=8192)

    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


# ---------------------------------------------------------------------------
# Reference-free
# ---------------------------------------------------------------------------

def evaluate_annotation(
    image_path: Path,
    annotation: str,
    caption: str,
    paper_title: str = "",
    figure_type: str = "",
    generation_prompt: str = "",
    judge_model: str = "openai/gpt-4o-mini",
    max_tokens: int = 2048,
) -> dict:
    """Reference-free — evaluate annotation against the figure image + generation prompt."""
    user_text = _build_context_text(annotation, caption, paper_title, figure_type,
                                    generation_prompt=generation_prompt)
    return _get_judge_result(judge_model, JUDGE_A_PROMPT, user_text,
                             image_path=image_path, max_tokens=max_tokens)


# Alias for backward compatibility
evaluate_judge_a = evaluate_annotation


# ---------------------------------------------------------------------------
# Reference-only (no image)
# ---------------------------------------------------------------------------

def evaluate_judge_b(
    annotation: str,
    reference: str,
    caption: str,
    paper_title: str = "",
    figure_type: str = "",
    judge_model: str = "openai/gpt-4o-mini",
    max_tokens: int = 2048,
) -> dict:
    """Reference-only — evaluate annotation against the reference (no image)."""
    user_text = _build_context_text(annotation, caption, paper_title, figure_type, reference)
    return _get_judge_result(judge_model, JUDGE_B_PROMPT, user_text,
                             max_tokens=max_tokens)


# ---------------------------------------------------------------------------
# Reference-with-image (image + reference)
# ---------------------------------------------------------------------------

def evaluate_judge_c(
    image_path: Path,
    annotation: str,
    reference: str,
    caption: str,
    paper_title: str = "",
    figure_type: str = "",
    judge_model: str = "openai/gpt-4o-mini",
    max_tokens: int = 2048,
) -> dict:
    """Reference-with-image — evaluate annotation against both the image and reference."""
    user_text = _build_context_text(annotation, caption, paper_title, figure_type, reference)
    return _get_judge_result(judge_model, JUDGE_C_PROMPT, user_text,
                             image_path=image_path, max_tokens=max_tokens)
