"""
Render PDF pages and produce figure-blurred variants for adversarial evaluation.

- ``process_page``: render any PDF page; blur all embedded raster figures.
- ``process_figure_page``: fig_* workflow with single-figure localization.

Page numbers are 1-based. Vector-only figures are not detected automatically.
"""

from blur_figure_in_page.english_pipeline import (
    process_english_figure_page,
    process_figure_page,
    resolve_english_paths,
    resolve_figure_paths,
)
from blur_figure_in_page.match import locate_figure_on_page
from blur_figure_in_page.pipeline import process_page
from blur_figure_in_page.trim import TrimInfo, load_trimmed_reference, trim_reference_margins
from blur_figure_in_page.types import (
    BBox,
    EnglishFigurePageResult,
    MatchHypothesis,
    MatchResult,
    PageBlurResult,
)

__all__ = [
    "BBox",
    "EnglishFigurePageResult",
    "MatchHypothesis",
    "MatchResult",
    "PageBlurResult",
    "TrimInfo",
    "locate_figure_on_page",
    "load_trimmed_reference",
    "process_english_figure_page",
    "process_figure_page",
    "process_page",
    "resolve_english_paths",
    "resolve_figure_paths",
    "trim_reference_margins",
]
