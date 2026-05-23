"""Pipeline for fig_* page images with single-figure adversarial blur."""

from __future__ import annotations

import logging
from pathlib import Path

import cv2

from blur_figure_in_page.blur import blur_region
from blur_figure_in_page.match import (
    default_padding_px,
    locate_figure_on_page,
)
from blur_figure_in_page.render import render_page_bgr
from blur_figure_in_page.trim import TrimInfo, trim_reference_margins
from blur_figure_in_page.types import BBox, EnglishFigurePageResult, MatchResult

logger = logging.getLogger(__name__)

_EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent


def resolve_figure_paths(
    figure_id: str,
    base_dir: Path | None = None,
) -> dict[str, Path]:
    """Standard paths for PDF, reference figure, and generated page images."""
    root = base_dir or _EXPERIMENT_ROOT
    return {
        "pdf": root / "paper_pdfs" / f"{figure_id}_paper.pdf",
        "figure": root / "english_only_figures" / f"{figure_id}.png",
        "page_image": root / "generated" / f"{figure_id}_page.png",
        "adversarial_image": root / "generated" / f"{figure_id}_page_adverserial.png",
    }


def process_figure_page(
    figure_id: str,
    page_number: int,
    *,
    base_dir: Path | None = None,
    dpi: int = 200,
    match_threshold: float = 0.6,
    min_score_margin: float = 0.05,
    min_figure_area_px: int = 10_000,
    blur_kernel: int = 75,
    padding_px: int | None = None,
    scale_min: float = 0.25,
    scale_max: float = 2.5,
    scale_step_coarse: float = 0.05,
    scale_step_fine: float = 0.02,
    roi_scale_step: float = 0.1,
    trim_keep_margin_px: int = 8,
    refine_min_score: float = 0.5,
) -> EnglishFigurePageResult:
    """
    Render a paper page and optionally blur only the target figure region.

    Writes ``generated/{figure_id}_page.png`` always. Writes
    ``generated/{figure_id}_page_adverserial.png`` only when the reference
    figure is located with sufficient confidence.

    Args:
        figure_id: Dataset figure key (e.g. ``fig_040``).
        page_number: 1-based PDF page index.
        base_dir: Experiment root containing input/output folders.
        dpi: Render resolution (default 200).
        match_threshold: Minimum score to accept a match.
        min_score_margin: Required gap between top-1 and top-2 scores.
        min_figure_area_px: Minimum embedded image area for candidate detection.
        blur_kernel: Gaussian blur kernel size for the adversarial image.
        padding_px: Extra pixels around matched bbox; auto if None.
        scale_min: Minimum reference scale for template/ROI search.
        scale_max: Maximum reference scale for template/ROI search.
        scale_step_coarse: Coarse template scale step.
        scale_step_fine: Fine template refinement step.
        roi_scale_step: Scale step for ROI candidate matching.
        trim_keep_margin_px: Pixels kept around trimmed reference content edges.
        refine_min_score: Minimum template score for in-rect bbox refinement.

    Returns:
        EnglishFigurePageResult with paths and match metadata.

    Raises:
        FileNotFoundError: If PDF or reference PNG is missing.
        ValueError: If reference image cannot be read.
    """
    paths = resolve_figure_paths(figure_id, base_dir)

    if not paths["pdf"].is_file():
        raise FileNotFoundError(f"PDF not found: {paths['pdf']}")
    if not paths["figure"].is_file():
        raise FileNotFoundError(f"Reference figure not found: {paths['figure']}")

    paths["page_image"].parent.mkdir(parents=True, exist_ok=True)

    reference_bgr = cv2.imread(str(paths["figure"]))
    if reference_bgr is None:
        raise ValueError(f"Could not read reference image: {paths['figure']}")

    trimmed_bgr, trim_info = trim_reference_margins(
        reference_bgr, keep_margin_px=trim_keep_margin_px
    )
    _log_trim_info(figure_id, trim_info)

    page_bgr, page, doc = render_page_bgr(paths["pdf"], page_number, dpi=dpi)
    try:
        cv2.imwrite(str(paths["page_image"]), page_bgr)

        match = locate_figure_on_page(
            page_bgr,
            page,
            doc,
            trimmed_bgr,
            dpi=dpi,
            min_figure_area_px=min_figure_area_px,
            match_threshold=match_threshold,
            min_score_margin=min_score_margin,
            scale_min=scale_min,
            scale_max=scale_max,
            scale_step_coarse=scale_step_coarse,
            scale_step_fine=scale_step_fine,
            roi_scale_step=roi_scale_step,
            refine_min_score=refine_min_score,
        )

        if not match.found or match.bbox is None:
            _log_match_failure(figure_id, page_number, match)
            return EnglishFigurePageResult(
                figure_key=figure_id,
                page_number=page_number,
                page_image_path=paths["page_image"],
                adversarial_image_path=None,
                match_found=False,
                match_score=match.best.score if match.best else None,
                second_best_score=match.second_best.score if match.second_best else None,
                match_method=match.best.method if match.best else None,
                bbox_used=None,
                failure_reason=match.failure_reason,
            )

        h, w = page_bgr.shape[:2]
        pad = padding_px if padding_px is not None else default_padding_px(w, h)
        blur_bbox = match.bbox.expand(pad, w, h)

        adversarial_bgr = page_bgr.copy()
        blur_region(adversarial_bgr, blur_bbox, kernel=blur_kernel)
        cv2.imwrite(str(paths["adversarial_image"]), adversarial_bgr)

        _log_match_success(figure_id, page_number, match, blur_bbox)

        return EnglishFigurePageResult(
            figure_key=figure_id,
            page_number=page_number,
            page_image_path=paths["page_image"],
            adversarial_image_path=paths["adversarial_image"],
            match_found=True,
            match_score=match.best.score if match.best else None,
            second_best_score=match.second_best.score if match.second_best else None,
            match_method=match.best.method if match.best else None,
            bbox_used=blur_bbox,
            failure_reason=None,
        )
    finally:
        doc.close()


# Backward-compatible aliases
resolve_english_paths = resolve_figure_paths
process_english_figure_page = process_figure_page


def _log_trim_info(figure_id: str, trim_info: TrimInfo) -> None:
    if not trim_info.trimmed:
        logger.debug("%s: reference trim skipped (no margins removed)", figure_id)
        return
    logger.debug(
        "%s: reference trimmed %dx%d -> %dx%d (strip T/B/L/R=%d/%d/%d/%d)",
        figure_id,
        trim_info.original_width,
        trim_info.original_height,
        trim_info.trimmed_width,
        trim_info.trimmed_height,
        trim_info.stripped_top,
        trim_info.stripped_bottom,
        trim_info.stripped_left,
        trim_info.stripped_right,
    )


def _log_match_success(
    figure_id: str,
    page_number: int,
    match: MatchResult,
    blur_bbox: BBox,
) -> None:
    second = match.second_best.score if match.second_best else None
    logger.info(
        "%s page %s: match score=%.3f method=%s second=%s bbox=%s",
        figure_id,
        page_number,
        match.best.score if match.best else 0.0,
        match.best.method if match.best else "?",
        f"{second:.3f}" if second is not None else "n/a",
        blur_bbox,
    )


def _log_match_failure(figure_id: str, page_number: int, match: MatchResult) -> None:
    best = match.best
    second = match.second_best
    margin = (best.score - second.score) if best and second else None
    logger.warning(
        "%s page %s: match failed (%s) best=%.3f (%s) second=%s margin=%s",
        figure_id,
        page_number,
        match.failure_reason,
        best.score if best else 0.0,
        best.method if best else "?",
        f"{second.score:.3f} ({second.method})" if second else "n/a",
        f"{margin:.3f}" if margin is not None else "n/a",
    )
