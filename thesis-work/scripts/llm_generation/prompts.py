"""Prompt loading and selection for figure description generation."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Maps figure_type values (from groundtruth) to prompt filenames
FIGURE_TYPE_TO_FILE = {
    "Line Plot": "line_plot.txt",
    "Bar Chart": "bar_chart.txt",
    "Pie Chart": "pie_chart.txt",
}

DEFAULT_PROMPT_FILE = "default.txt"

# Maps annotation_language / paper_language to translated prompt subdirectory
LANGUAGE_TO_DIR = {
    "Bulgarian": "translated/bulgarian",
    "Chinese": "translated/chinese",
    "German": "translated/german",
}


def load_prompts() -> dict[tuple[str, str], str]:
    """Load all prompts into a (language, figure_type) -> prompt_text mapping.

    English prompts are loaded from the top-level prompts/ directory.
    Translated prompts are loaded from prompts/translated/<language>/.
    Falls back gracefully if a translated prompt file is missing.

    Returns:
        Dictionary mapping (language, figure_type) to prompt string.
    """
    prompts = {}

    # Load English prompts (top-level)
    for figure_type, filename in FIGURE_TYPE_TO_FILE.items():
        path = PROMPTS_DIR / filename
        if path.exists():
            prompts[("English", figure_type)] = path.read_text(encoding="utf-8")

    # English default
    default_path = PROMPTS_DIR / DEFAULT_PROMPT_FILE
    if default_path.exists():
        prompts[("English", "Default")] = default_path.read_text(encoding="utf-8")

    # Load translated prompts
    for language, subdir in LANGUAGE_TO_DIR.items():
        lang_dir = PROMPTS_DIR / subdir
        if not lang_dir.exists():
            continue
        for figure_type, filename in FIGURE_TYPE_TO_FILE.items():
            path = lang_dir / filename
            if path.exists():
                prompts[(language, figure_type)] = path.read_text(encoding="utf-8")
        default_path = lang_dir / DEFAULT_PROMPT_FILE
        if default_path.exists():
            prompts[(language, "Default")] = default_path.read_text(encoding="utf-8")

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

    Raises:
        ValueError: If no prompt can be found at all (shouldn't happen if
                    English prompts are present).
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
