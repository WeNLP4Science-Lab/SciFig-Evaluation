"""Shared types for page figure blur pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BBox:
    """Axis-aligned box in pixel coordinates (top-left origin, OpenCV convention)."""

    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def width(self) -> int:
        return self.x1 - self.x0

    @property
    def height(self) -> int:
        return self.y1 - self.y0

    @property
    def area(self) -> int:
        return max(0, self.width) * max(0, self.height)

    def clamp(self, max_width: int, max_height: int) -> BBox:
        """Clip to image bounds [0, max_width) x [0, max_height)."""
        x0 = max(0, min(self.x0, max_width))
        y0 = max(0, min(self.y0, max_height))
        x1 = max(0, min(self.x1, max_width))
        y1 = max(0, min(self.y1, max_height))
        if x1 <= x0 or y1 <= y0:
            return BBox(0, 0, 0, 0)
        return BBox(x0, y0, x1, y1)

    def expand(self, padding_px: int, max_width: int, max_height: int) -> BBox:
        """Grow bbox by padding on all sides, then clamp to image bounds."""
        return BBox(
            self.x0 - padding_px,
            self.y0 - padding_px,
            self.x1 + padding_px,
            self.y1 + padding_px,
        ).clamp(max_width, max_height)


@dataclass(frozen=True)
class PageBlurResult:
    """Paths and metadata from processing one PDF page."""

    original_path: Path
    blurred_path: Path
    page_number: int
    dpi: int
    bboxes_used: tuple[BBox, ...]
    figures_found: int


@dataclass(frozen=True)
class MatchHypothesis:
    """One candidate location for the reference figure on a page."""

    score: float
    bbox: BBox
    method: str  # "roi" | "embedded" | "template"


@dataclass(frozen=True)
class MatchResult:
    """Outcome of locating a reference figure on a rendered page."""

    found: bool
    bbox: BBox | None
    best: MatchHypothesis | None
    second_best: MatchHypothesis | None
    failure_reason: str | None  # "below_threshold" | "ambiguous" | None


@dataclass(frozen=True)
class EnglishFigurePageResult:
    """Paths and match metadata for one english_fig_* page export."""

    figure_key: str
    page_number: int
    page_image_path: Path
    adversarial_image_path: Path | None
    match_found: bool
    match_score: float | None
    second_best_score: float | None
    match_method: str | None
    bbox_used: BBox | None
    failure_reason: str | None
