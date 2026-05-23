"""Orchestrate page render, figure detection, blur, and export."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import cv2

from blur_figure_in_page.blur import blur_regions
from blur_figure_in_page.detect import resolve_figure_bboxes
from blur_figure_in_page.render import render_page_bgr
from blur_figure_in_page.types import BBox, PageBlurResult

logger = logging.getLogger(__name__)


def _sanitize_stem(path: Path) -> str:
    stem = path.stem
    return re.sub(r'[<>:"/\\|?*]', "_", stem)[:200]


def process_page(
    pdf_path: str | Path,
    page_number: int,
    output_dir: str | Path,
    figure_bboxes: list[BBox] | None = None,
    *,
    dpi: int = 150,
    min_figure_area_px: int = 10_000,
    blur_kernel: int = 75,
) -> PageBlurResult:
    """
    Render a PDF page and write original + figures-blurred PNG variants.

    Args:
        pdf_path: Path to the PDF.
        page_number: 1-based page index.
        output_dir: Directory for output PNGs (created if missing).
        figure_bboxes: Optional pixel bboxes on the rendered image; replaces
            auto-detection when provided.
        dpi: Render resolution.
        min_figure_area_px: Minimum embedded image area for auto-detection.
        blur_kernel: Gaussian blur kernel size (odd integer applied internally).

    Returns:
        PageBlurResult with paths and metadata.
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    original_bgr, page, doc = render_page_bgr(pdf_path, page_number, dpi=dpi)
    try:
        h, w = original_bgr.shape[:2]
        bboxes = resolve_figure_bboxes(
            page,
            image_width=w,
            image_height=h,
            dpi=dpi,
            figure_bboxes=figure_bboxes,
            min_figure_area_px=min_figure_area_px,
        )

        if not bboxes:
            logger.warning(
                "No figure regions found on page %s of %s; blurred image equals original.",
                page_number,
                pdf_path.name,
            )

        blurred_bgr = original_bgr.copy()
        blur_regions(blurred_bgr, bboxes, kernel=blur_kernel)

        stem = _sanitize_stem(pdf_path)
        page_tag = f"page{page_number:03d}"
        original_path = output_dir / f"{stem}_{page_tag}_original.png"
        blurred_path = output_dir / f"{stem}_{page_tag}_figures_blurred.png"

        cv2.imwrite(str(original_path), original_bgr)
        cv2.imwrite(str(blurred_path), blurred_bgr)

        return PageBlurResult(
            original_path=original_path,
            blurred_path=blurred_path,
            page_number=page_number,
            dpi=dpi,
            bboxes_used=tuple(bboxes),
            figures_found=len(bboxes),
        )
    finally:
        doc.close()
