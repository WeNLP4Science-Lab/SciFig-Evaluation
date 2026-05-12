"""Prompt loading and selection for structured figure description generation.

Reuses the same base prompt files as llm_generation, but wraps them with
instructions to return JSON containing both a description paragraph and
a structured component breakdown.
"""

from pathlib import Path

# Reuse the same prompt files
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "llm_generation" / "prompts"

FIGURE_TYPE_TO_FILE = {
    "Line Plot": "line_plot.txt",
    "Bar Chart": "bar_chart.txt",
    "Pie Chart": "pie_chart.txt",
}

DEFAULT_PROMPT_FILE = "default.txt"

LANGUAGE_TO_DIR = {
    "Bulgarian": "translated/bulgarian",
    "Chinese": "translated/chinese",
    "German": "translated/german",
}

# Structured output schemas per figure type
STRUCTURED_SUFFIX = {
    "Line Plot": """

In addition to the paragraph description above, also provide a structured breakdown of the figure's key components.

Return your response as valid JSON with exactly this structure:
{
  "description": "<your single paragraph description>",
  "breakdown": {
    "figure_type_detected": "<what type of plot you see>",
    "x_axis": {"label": "<text>", "scale": "<linear or logarithmic>", "range": "<min to max>"},
    "y_axis": {"label": "<text>", "scale": "<linear or logarithmic>", "range": "<min to max>"},
    "num_lines": <integer>,
    "lines": [
      {"label": "<legend label>", "color": "<color>", "style": "<solid/dashed/dotted>", "trend": "<increasing/decreasing/stable/fluctuating>"}
    ],
    "has_legend": <true or false>,
    "legend_position": "<position or null>"
  }
}

Return ONLY the JSON object. No extra text before or after.""",

    "Bar Chart": """

In addition to the paragraph description above, also provide a structured breakdown of the figure's key components.

Return your response as valid JSON with exactly this structure:
{
  "description": "<your single paragraph description>",
  "breakdown": {
    "figure_type_detected": "<what type of chart you see>",
    "category_axis": {"label": "<text>", "categories": ["<cat1>", "<cat2>"]},
    "value_axis": {"label": "<text>", "scale": "<linear or logarithmic>", "range": "<min to max>"},
    "num_bars": <integer total number of individual bars>,
    "bars": [
      {"label": "<category>", "color": "<color>", "value": "<approximate value>"}
    ],
    "is_grouped": <true or false>,
    "is_stacked": <true or false>,
    "has_legend": <true or false>,
    "legend_position": "<position or null>"
  }
}

Return ONLY the JSON object. No extra text before or after.""",

    "Pie Chart": """

In addition to the paragraph description above, also provide a structured breakdown of the figure's key components.

Return your response as valid JSON with exactly this structure:
{
  "description": "<your single paragraph description>",
  "breakdown": {
    "figure_type_detected": "<what type of chart you see>",
    "num_slices": <integer>,
    "slices": [
      {"label": "<category>", "color": "<color>", "percentage": "<value as shown>"}
    ],
    "has_legend": <true or false>,
    "legend_position": "<position or null>",
    "labels_on_slices": <true or false>
  }
}

Return ONLY the JSON object. No extra text before or after.""",

    "Default": """

In addition to the paragraph description above, also provide a structured breakdown of the figure's key components.

Return your response as valid JSON with exactly this structure:
{
  "description": "<your single paragraph description>",
  "breakdown": {
    "figure_type_detected": "<what type of figure you see>",
    "x_axis": {"label": "<text or null>", "scale": "<type or null>", "range": "<min to max or null>"},
    "y_axis": {"label": "<text or null>", "scale": "<type or null>", "range": "<min to max or null>"},
    "num_visual_elements": <integer>,
    "has_legend": <true or false>,
    "legend_position": "<position or null>"
  }
}

Return ONLY the JSON object. No extra text before or after.""",
}


def load_prompts() -> dict[tuple[str, str], str]:
    """Load all prompts with structured output suffixes appended."""
    prompts = {}

    # Load English prompts
    for figure_type, filename in FIGURE_TYPE_TO_FILE.items():
        path = PROMPTS_DIR / filename
        if path.exists():
            base = path.read_text(encoding="utf-8")
            suffix = STRUCTURED_SUFFIX.get(figure_type, STRUCTURED_SUFFIX["Default"])
            prompts[("English", figure_type)] = base + suffix

    # English default
    default_path = PROMPTS_DIR / DEFAULT_PROMPT_FILE
    if default_path.exists():
        base = default_path.read_text(encoding="utf-8")
        prompts[("English", "Default")] = base + STRUCTURED_SUFFIX["Default"]

    # Load translated prompts
    for language, subdir in LANGUAGE_TO_DIR.items():
        lang_dir = PROMPTS_DIR / subdir
        if not lang_dir.exists():
            continue
        for figure_type, filename in FIGURE_TYPE_TO_FILE.items():
            path = lang_dir / filename
            if path.exists():
                base = path.read_text(encoding="utf-8")
                suffix = STRUCTURED_SUFFIX.get(figure_type, STRUCTURED_SUFFIX["Default"])
                prompts[(language, figure_type)] = base + suffix
        default_path = lang_dir / DEFAULT_PROMPT_FILE
        if default_path.exists():
            base = default_path.read_text(encoding="utf-8")
            prompts[(language, "Default")] = base + STRUCTURED_SUFFIX["Default"]

    return prompts


def get_prompt(
    prompts: dict[tuple[str, str], str],
    language: str,
    figure_type: str,
) -> str:
    """Select the best prompt for a given language and figure type.

    Fallback chain:
        1. (language, figure_type) — exact match
        2. (language, "Default") — language-specific default
        3. ("English", figure_type) — English prompt for that figure type
        4. ("English", "Default") — ultimate fallback
    """
    for key in [
        (language, figure_type),
        (language, "Default"),
        ("English", figure_type),
        ("English", "Default"),
    ]:
        if key in prompts:
            return prompts[key]

    raise ValueError(
        f"No prompt found for language={language!r}, figure_type={figure_type!r}. "
        "Ensure at least the English default prompt exists."
    )
