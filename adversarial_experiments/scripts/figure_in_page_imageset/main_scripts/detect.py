"""Detect raster figure regions on a rendered PDF page."""

from __future__ import annotations

import fitz

from blur_figure_in_page.types import BBox


def _pdf_rect_to_pixels(rect: fitz.Rect, scale: float) -> BBox:
    return BBox(
        x0=int(round(rect.x0 * scale)),
        y0=int(round(rect.y0 * scale)),
        x1=int(round(rect.x1 * scale)),
        y1=int(round(rect.y1 * scale)),
    )


def _intersection_area(a: BBox, b: BBox) -> int:
    x0 = max(a.x0, b.x0)
    y0 = max(a.y0, b.y0)
    x1 = min(a.x1, b.x1)
    y1 = min(a.y1, b.y1)
    if x1 <= x0 or y1 <= y0:
        return 0
    return (x1 - x0) * (y1 - y0)


def _merge_overlapping(bboxes: list[BBox], *, iou_threshold: float = 0.3) -> list[BBox]:
    """Merge boxes that overlap significantly (union on merge)."""
    if not bboxes:
        return []

    merged: list[BBox] = []
    for box in sorted(bboxes, key=lambda b: b.area, reverse=True):
        absorbed = False
        for i, existing in enumerate(merged):
            inter = _intersection_area(box, existing)
            if inter == 0:
                continue
            union_area = box.area + existing.area - inter
            iou = inter / union_area if union_area > 0 else 0.0
            if iou >= iou_threshold or inter >= 0.5 * min(box.area, existing.area):
                merged[i] = BBox(
                    x0=min(existing.x0, box.x0),
                    y0=min(existing.y0, box.y0),
                    x1=max(existing.x1, box.x1),
                    y1=max(existing.y1, box.y1),
                )
                absorbed = True
                break
        if not absorbed:
            merged.append(box)
    return merged


def detect_figure_bboxes(
    page: fitz.Page,
    *,
    image_width: int,
    image_height: int,
    dpi: int,
    min_figure_area_px: int = 10_000,
) -> list[BBox]:
    """
    Find embedded raster image placements on a page.

    Uses PyMuPDF image xref rects mapped to pixel coordinates at the given dpi.
    """
    scale = dpi / 72.0
    candidates: list[BBox] = []

    for img_info in page.get_images(full=True):
        xref = img_info[0]
        try:
            rects = page.get_image_rects(xref)
        except (ValueError, RuntimeError):
            continue
        for rect in rects:
            bbox = _pdf_rect_to_pixels(rect, scale).clamp(image_width, image_height)
            if bbox.area >= min_figure_area_px:
                candidates.append(bbox)

    return _merge_overlapping(candidates)


def resolve_figure_bboxes(
    page: fitz.Page,
    *,
    image_width: int,
    image_height: int,
    dpi: int,
    figure_bboxes: list[BBox] | None,
    min_figure_area_px: int,
) -> list[BBox]:
    """
    Return bboxes to blur: caller override or automatic detection.
    """
    if figure_bboxes is not None:
        return [
            b.clamp(image_width, image_height)
            for b in figure_bboxes
            if b.clamp(image_width, image_height).area > 0
        ]

    return detect_figure_bboxes(
        page,
        image_width=image_width,
        image_height=image_height,
        dpi=dpi,
        min_figure_area_px=min_figure_area_px,
    )
