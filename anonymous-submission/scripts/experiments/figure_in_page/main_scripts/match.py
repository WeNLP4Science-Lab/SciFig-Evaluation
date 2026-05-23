"""Locate a reference figure crop on a rendered PDF page."""

from __future__ import annotations

import logging
from typing import Iterable

import cv2
import fitz
import numpy as np

from blur_figure_in_page.detect import _intersection_area, _pdf_rect_to_pixels, detect_figure_bboxes
from blur_figure_in_page.types import BBox, MatchHypothesis, MatchResult

logger = logging.getLogger(__name__)

DEFAULT_SCALE_MIN = 0.25
DEFAULT_SCALE_MAX = 2.5
DEFAULT_SCALE_STEP_COARSE = 0.05
DEFAULT_SCALE_STEP_FINE = 0.02
DEFAULT_ROI_SCALE_STEP = 0.1
_FINE_REFINE_RADIUS = 0.1
_COARSE_TOP_K = 3
_MIN_TEMPLATE_SIZE = 16
_REFINE_METHODS = frozenset({"roi", "embedded", "embedded_ncc"})
DEFAULT_REFINE_MIN_SCORE = 0.5


def _iter_scales(scale_min: float, scale_max: float, step: float) -> list[float]:
    """Inclusive scale values from scale_min to scale_max."""
    if step <= 0 or scale_max < scale_min:
        return [scale_min]
    scales: list[float] = []
    s = scale_min
    while s <= scale_max + 1e-9:
        scales.append(round(s, 4))
        s += step
    return scales


def _to_gray(bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)


def _resize_pair(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Resize b to match a's spatial dimensions."""
    if a.shape == b.shape:
        return a, b
    resized = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
    return a, resized


def _ssim(gray_a: np.ndarray, gray_b: np.ndarray) -> float:
    """Simplified SSIM for same-shape grayscale images."""
    a, b = _resize_pair(gray_a, gray_b)
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    mu_a = a.mean()
    mu_b = b.mean()
    sigma_a_sq = ((a - mu_a) ** 2).mean()
    sigma_b_sq = ((b - mu_b) ** 2).mean()
    sigma_ab = ((a - mu_a) * (b - mu_b)).mean()
    num = (2 * mu_a * mu_b + c1) * (2 * sigma_ab + c2)
    den = (mu_a**2 + mu_b**2 + c1) * (sigma_a_sq + sigma_b_sq + c2)
    if den == 0:
        return 0.0
    return float(np.clip(num / den, -1.0, 1.0))


def _ncc_peak(gray_search: np.ndarray, gray_template: np.ndarray) -> float:
    """Max normalized cross-correlation; template must fit inside search region."""
    th, tw = gray_template.shape[:2]
    sh, sw = gray_search.shape[:2]
    if th > sh or tw > sw or th < 2 or tw < 2:
        return 0.0
    result = cv2.matchTemplate(gray_search, gray_template, cv2.TM_CCOEFF_NORMED)
    return float(result.max()) if result.size else 0.0


def _compare_images(bgr_a: np.ndarray, bgr_b: np.ndarray) -> tuple[float, float]:
    """
    Return (ncc, ssim) using both resize orientations (a→b and b→a).

    Helps when reference and embedded image differ in resolution or aspect.
    """
    gray_a = _to_gray(bgr_a)
    gray_b = _to_gray(bgr_b)

    ga, gb = _resize_pair(gray_a, gray_b)
    ncc_ab = _ncc_peak(ga, gb)
    ssim_ab = _ssim(ga, gb)

    gb_search, ga_templ = _resize_pair(gray_b, gray_a)
    ncc_ba = _ncc_peak(gb_search, ga_templ)
    ssim_ba = _ssim(gb_search, ga_templ)

    return max(ncc_ab, ncc_ba), max(ssim_ab, ssim_ba)


def _roi_score_multiscale(
    page_gray: np.ndarray,
    ref_gray: np.ndarray,
    bbox: BBox,
    *,
    scale_min: float,
    scale_max: float,
    roi_scale_step: float,
) -> float:
    """Best NCC over multiple reference scales inside a candidate ROI."""
    h, w = page_gray.shape[:2]
    clipped = bbox.clamp(w, h)
    if clipped.area == 0:
        return 0.0

    roi = page_gray[clipped.y0 : clipped.y1, clipped.x0 : clipped.x1]
    rh, rw = ref_gray.shape[:2]
    best = 0.0

    for scale in _iter_scales(scale_min, scale_max, roi_scale_step):
        tw = max(_MIN_TEMPLATE_SIZE, int(rw * scale))
        th = max(_MIN_TEMPLATE_SIZE, int(rh * scale))
        if th > roi.shape[0] or tw > roi.shape[1]:
            continue
        templ = cv2.resize(ref_gray, (tw, th), interpolation=cv2.INTER_AREA)
        best = max(best, _ncc_peak(roi, templ))

    return best


def _decode_xref(doc: fitz.Document, xref: int) -> np.ndarray | None:
    try:
        info = doc.extract_image(xref)
        buf = np.frombuffer(info["image"], dtype=np.uint8)
        decoded = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        return decoded
    except (ValueError, RuntimeError):
        return None


def _embedded_entries(
    doc: fitz.Document,
    page: fitz.Page,
    ref_bgr: np.ndarray,
    *,
    dpi: int,
    image_width: int,
    image_height: int,
) -> list[tuple[float, BBox, str]]:
    """Score each embedded image xref; return (score, bbox, method tag)."""
    scale = dpi / 72.0
    entries: list[tuple[float, BBox, str]] = []
    seen_xrefs: set[int] = set()

    for img_info in page.get_images(full=True):
        xref = img_info[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)

        embedded = _decode_xref(doc, xref)
        if embedded is None:
            continue

        ncc, ssim = _compare_images(embedded, ref_bgr)
        score = max(ncc, ssim)
        method = "embedded" if ssim >= ncc else "embedded_ncc"
        if score <= 0:
            continue

        try:
            rects = page.get_image_rects(xref)
        except (ValueError, RuntimeError):
            continue
        for rect in rects:
            bbox = _pdf_rect_to_pixels(rect, scale).clamp(image_width, image_height)
            if bbox.area > 0:
                entries.append((score, bbox, method))

    return entries


def _hypothesis_from_candidate(
    page_gray: np.ndarray,
    ref_gray: np.ndarray,
    candidate: BBox,
    embedded: list[tuple[float, BBox, str]],
    *,
    scale_min: float,
    scale_max: float,
    roi_scale_step: float,
) -> MatchHypothesis:
    roi = _roi_score_multiscale(
        page_gray,
        ref_gray,
        candidate,
        scale_min=scale_min,
        scale_max=scale_max,
        roi_scale_step=roi_scale_step,
    )
    best_score = roi
    method = "roi"

    for emb_score, emb_bbox, emb_method in embedded:
        if _intersection_area(candidate, emb_bbox) == 0:
            continue
        if emb_score > best_score:
            best_score = emb_score
            method = emb_method

    return MatchHypothesis(score=best_score, bbox=candidate, method=method)


def _template_peak_at_scale(
    page_gray: np.ndarray,
    ref_gray: np.ndarray,
    scale: float,
    image_width: int,
    image_height: int,
) -> tuple[float, BBox | None]:
    rh, rw = ref_gray.shape[:2]
    tw = max(_MIN_TEMPLATE_SIZE, int(rw * scale))
    th = max(_MIN_TEMPLATE_SIZE, int(rh * scale))
    if th > page_gray.shape[0] or tw > page_gray.shape[1]:
        return 0.0, None

    templ = cv2.resize(ref_gray, (tw, th), interpolation=cv2.INTER_AREA)
    result = cv2.matchTemplate(page_gray, templ, cv2.TM_CCOEFF_NORMED)
    _, peak, _, peak_loc = cv2.minMaxLoc(result)
    x0, y0 = peak_loc
    bbox = BBox(x0, y0, x0 + tw, y0 + th).clamp(image_width, image_height)
    return float(peak), bbox if bbox.area > 0 else None


def _coarse_fine_template_hypothesis(
    page_gray: np.ndarray,
    ref_gray: np.ndarray,
    image_width: int,
    image_height: int,
    *,
    scale_min: float,
    scale_max: float,
    scale_step_coarse: float,
    scale_step_fine: float,
) -> MatchHypothesis | None:
    """Coarse scale sweep, refine top-K coarse peaks, return global best."""
    coarse_results: list[tuple[float, float, BBox]] = []

    for scale in _iter_scales(scale_min, scale_max, scale_step_coarse):
        peak, bbox = _template_peak_at_scale(
            page_gray, ref_gray, scale, image_width, image_height
        )
        if bbox is not None and peak > 0:
            coarse_results.append((peak, scale, bbox))

    if not coarse_results:
        return None

    coarse_results.sort(key=lambda x: x[0], reverse=True)
    top_scales = {s for _, s, _ in coarse_results[:_COARSE_TOP_K]}

    best_score = -1.0
    best_bbox: BBox | None = None

    for coarse_scale in top_scales:
        refine_min = max(scale_min, coarse_scale - _FINE_REFINE_RADIUS)
        refine_max = min(scale_max, coarse_scale + _FINE_REFINE_RADIUS)
        for scale in _iter_scales(refine_min, refine_max, scale_step_fine):
            peak, bbox = _template_peak_at_scale(
                page_gray, ref_gray, scale, image_width, image_height
            )
            if peak > best_score and bbox is not None:
                best_score = peak
                best_bbox = bbox

    if best_bbox is None:
        return None
    return MatchHypothesis(score=best_score, bbox=best_bbox, method="template")


def refine_bbox_in_rect(
    page_gray: np.ndarray,
    trimmed_ref_gray: np.ndarray,
    coarse_bbox: BBox,
    *,
    scale_min: float,
    scale_max: float,
    scale_step_coarse: float,
    scale_step_fine: float,
    refine_min_score: float = DEFAULT_REFINE_MIN_SCORE,
) -> BBox | None:
    """
    Locate trimmed reference inside a coarse placement rect via template match.

    Returns a tight page-space bbox, or None if refinement score is too low.
    """
    h, w = page_gray.shape[:2]
    clipped = coarse_bbox.clamp(w, h)
    if clipped.area == 0:
        return None

    roi = page_gray[clipped.y0 : clipped.y1, clipped.x0 : clipped.x1]
    roi_h, roi_w = roi.shape[:2]
    hypothesis = _coarse_fine_template_hypothesis(
        roi,
        trimmed_ref_gray,
        roi_w,
        roi_h,
        scale_min=scale_min,
        scale_max=scale_max,
        scale_step_coarse=scale_step_coarse,
        scale_step_fine=scale_step_fine,
    )
    if hypothesis is None or hypothesis.score < refine_min_score:
        return None

    tight = hypothesis.bbox
    return BBox(
        clipped.x0 + tight.x0,
        clipped.y0 + tight.y0,
        clipped.x0 + tight.x1,
        clipped.y0 + tight.y1,
    ).clamp(w, h)


def _apply_tight_bbox_refinement(
    match: MatchResult,
    page_gray: np.ndarray,
    ref_gray: np.ndarray,
    *,
    scale_min: float,
    scale_max: float,
    scale_step_coarse: float,
    scale_step_fine: float,
    refine_min_score: float,
) -> MatchResult:
    if not match.found or match.bbox is None or match.best is None:
        return match
    if match.best.method not in _REFINE_METHODS:
        return match

    coarse = match.bbox
    tight = refine_bbox_in_rect(
        page_gray,
        ref_gray,
        coarse,
        scale_min=scale_min,
        scale_max=scale_max,
        scale_step_coarse=scale_step_coarse,
        scale_step_fine=scale_step_fine,
        refine_min_score=refine_min_score,
    )
    if tight is None or tight.area == 0:
        logger.debug(
            "Tight bbox refine skipped for %s (coarse area=%s)",
            match.best.method,
            coarse.area,
        )
        return match

    logger.debug(
        "Tight bbox refine: %s coarse area=%s -> tight area=%s",
        match.best.method,
        coarse.area,
        tight.area,
    )
    return MatchResult(
        found=True,
        bbox=tight,
        best=match.best,
        second_best=match.second_best,
        failure_reason=None,
    )


def _ranked_hypotheses(hypotheses: Iterable[MatchHypothesis]) -> list[MatchHypothesis]:
    return sorted(hypotheses, key=lambda h: h.score, reverse=True)


def _resolve_match(
    ranked: list[MatchHypothesis],
    *,
    match_threshold: float,
    min_score_margin: float,
) -> MatchResult:
    if not ranked:
        return MatchResult(
            found=False,
            bbox=None,
            best=None,
            second_best=None,
            failure_reason="below_threshold",
        )

    best = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None

    if best.score < match_threshold:
        return MatchResult(
            found=False,
            bbox=None,
            best=best,
            second_best=second,
            failure_reason="below_threshold",
        )

    if second is not None and (best.score - second.score) < min_score_margin:
        return MatchResult(
            found=False,
            bbox=None,
            best=best,
            second_best=second,
            failure_reason="ambiguous",
        )

    return MatchResult(
        found=True,
        bbox=best.bbox,
        best=best,
        second_best=second,
        failure_reason=None,
    )


def locate_figure_on_page(
    page_bgr: np.ndarray,
    page: fitz.Page,
    doc: fitz.Document,
    reference_bgr: np.ndarray,
    *,
    dpi: int = 200,
    min_figure_area_px: int = 10_000,
    match_threshold: float = 0.6,
    min_score_margin: float = 0.05,
    scale_min: float = DEFAULT_SCALE_MIN,
    scale_max: float = DEFAULT_SCALE_MAX,
    scale_step_coarse: float = DEFAULT_SCALE_STEP_COARSE,
    scale_step_fine: float = DEFAULT_SCALE_STEP_FINE,
    roi_scale_step: float = DEFAULT_ROI_SCALE_STEP,
    refine_min_score: float = DEFAULT_REFINE_MIN_SCORE,
) -> MatchResult:
    """
    Find where the reference figure appears on a rendered page.

    Combines PyMuPDF placement candidates (multi-scale ROI), embedded-image
    similarity, and coarse-to-fine multi-scale template matching (default
    scale range 0.25x–2.5x).
    """
    h, w = page_bgr.shape[:2]
    page_gray = _to_gray(page_bgr)
    ref_gray = _to_gray(reference_bgr)

    embedded = _embedded_entries(
        doc, page, reference_bgr, dpi=dpi, image_width=w, image_height=h
    )

    hypotheses: list[MatchHypothesis] = []

    candidates = detect_figure_bboxes(
        page,
        image_width=w,
        image_height=h,
        dpi=dpi,
        min_figure_area_px=min_figure_area_px,
    )

    if candidates:
        for candidate in candidates:
            hypotheses.append(
                _hypothesis_from_candidate(
                    page_gray,
                    ref_gray,
                    candidate,
                    embedded,
                    scale_min=scale_min,
                    scale_max=scale_max,
                    roi_scale_step=roi_scale_step,
                )
            )
    else:
        for score, bbox, method in embedded:
            hypotheses.append(MatchHypothesis(score=score, bbox=bbox, method=method))

    template = _coarse_fine_template_hypothesis(
        page_gray,
        ref_gray,
        w,
        h,
        scale_min=scale_min,
        scale_max=scale_max,
        scale_step_coarse=scale_step_coarse,
        scale_step_fine=scale_step_fine,
    )
    if template is not None:
        hypotheses.append(template)

    ranked = _ranked_hypotheses(hypotheses)
    match = _resolve_match(
        ranked, match_threshold=match_threshold, min_score_margin=min_score_margin
    )
    return _apply_tight_bbox_refinement(
        match,
        page_gray,
        ref_gray,
        scale_min=scale_min,
        scale_max=scale_max,
        scale_step_coarse=scale_step_coarse,
        scale_step_fine=scale_step_fine,
        refine_min_score=refine_min_score,
    )


def default_padding_px(image_width: int, image_height: int, *, fraction: float = 0.01) -> int:
    return max(4, int(min(image_width, image_height) * fraction))
