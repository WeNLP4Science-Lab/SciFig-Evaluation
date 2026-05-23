"""Trim uniform outer margins from reference figure images."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class TrimInfo:
    """Metadata from trimming outer margins off a reference image."""

    original_width: int
    original_height: int
    trimmed_width: int
    trimmed_height: int
    stripped_top: int
    stripped_bottom: int
    stripped_left: int
    stripped_right: int
    trimmed: bool


def _pixel_is_background(
    pixel: np.ndarray,
    *,
    bg_threshold: int,
    alpha_threshold: int,
) -> bool:
    if pixel.shape[0] >= 4 and pixel[3] <= alpha_threshold:
        return True
    bgr = pixel[:3]
    return bool(np.all(bgr >= bg_threshold))


def _strip_is_background(
    strip: np.ndarray,
    *,
    bg_threshold: int,
    max_bg_std: float,
    alpha_threshold: int,
) -> bool:
    """True if an entire row or column strip is removable background."""
    flat = strip.reshape(-1, strip.shape[-1])
    if all(
        _pixel_is_background(p, bg_threshold=bg_threshold, alpha_threshold=alpha_threshold)
        for p in flat
    ):
        return True

    bgr = flat[:, :3].astype(np.float64)
    return bool(bgr.mean() >= bg_threshold and bgr.std() < max_bg_std)


def trim_reference_margins(
    bgr: np.ndarray,
    *,
    bg_threshold: int = 248,
    max_bg_std: float = 8.0,
    alpha_threshold: int = 10,
    keep_margin_px: int = 8,
    min_content_px: int = 16,
) -> tuple[np.ndarray, TrimInfo]:
    """
    Asymmetrically remove uniform outer margins, then expand by keep_margin_px.

    Peels each edge independently (no centered-figure assumption). The
    keep-margin expands the content box outward so edge lines stay visible.
    """
    h, w = bgr.shape[:2]
    if h == 0 or w == 0:
        info = TrimInfo(w, h, w, h, 0, 0, 0, 0, trimmed=False)
        return bgr.copy(), info

    top = 0
    while top < h and _strip_is_background(
        bgr[top, :],
        bg_threshold=bg_threshold,
        max_bg_std=max_bg_std,
        alpha_threshold=alpha_threshold,
    ):
        top += 1

    bottom = h
    while bottom > top and _strip_is_background(
        bgr[bottom - 1, :],
        bg_threshold=bg_threshold,
        max_bg_std=max_bg_std,
        alpha_threshold=alpha_threshold,
    ):
        bottom -= 1

    left = 0
    while left < w and _strip_is_background(
        bgr[top:bottom, left],
        bg_threshold=bg_threshold,
        max_bg_std=max_bg_std,
        alpha_threshold=alpha_threshold,
    ):
        left += 1

    right = w
    while right > left and _strip_is_background(
        bgr[top:bottom, right - 1],
        bg_threshold=bg_threshold,
        max_bg_std=max_bg_std,
        alpha_threshold=alpha_threshold,
    ):
        right -= 1

    content_h = bottom - top
    content_w = right - left
    if content_h < min_content_px or content_w < min_content_px:
        info = TrimInfo(w, h, w, h, 0, 0, 0, 0, trimmed=False)
        return bgr.copy(), info

    y0 = max(0, top - keep_margin_px)
    y1 = min(h, bottom + keep_margin_px)
    x0 = max(0, left - keep_margin_px)
    x1 = min(w, right + keep_margin_px)

    cropped = bgr[y0:y1, x0:x1].copy()
    info = TrimInfo(
        original_width=w,
        original_height=h,
        trimmed_width=x1 - x0,
        trimmed_height=y1 - y0,
        stripped_top=y0,
        stripped_bottom=h - y1,
        stripped_left=x0,
        stripped_right=w - x1,
        trimmed=(y0, y1, x0, x1) != (0, h, 0, w),
    )
    return cropped, info


def load_trimmed_reference(
    path: str | Path,
    **trim_kwargs,
) -> tuple[np.ndarray, TrimInfo]:
    """Load a reference PNG and trim outer margins."""
    path = Path(path)
    bgr = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if bgr is None:
        raise ValueError(f"Could not read image: {path}")
    if bgr.ndim == 2:
        bgr = cv2.cvtColor(bgr, cv2.COLOR_GRAY2BGR)
    elif bgr.shape[2] == 4:
        bgr = cv2.cvtColor(bgr, cv2.COLOR_BGRA2BGR)
    return trim_reference_margins(bgr, **trim_kwargs)
