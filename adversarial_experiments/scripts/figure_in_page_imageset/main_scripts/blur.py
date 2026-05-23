"""Blur figure regions on a page image."""

from __future__ import annotations

import cv2
import numpy as np

from blur_figure_in_page.types import BBox


def _odd_kernel(kernel: int) -> int:
    k = max(3, kernel)
    return k if k % 2 == 1 else k + 1


def _effective_kernel(roi_height: int, roi_width: int, requested: int) -> int:
    """
    Scale blur kernel to ROI size so large figures are not left partially legible.

    Capped at the largest odd kernel OpenCV allows for the ROI dimensions.
    """
    limit = min(roi_height, roi_width)
    if limit < 3:
        return 3
    max_k = limit if limit % 2 == 1 else limit - 1
    # At least requested kernel, up to ~half the shorter ROI side
    target = max(requested, min(roi_height, roi_width) // 2)
    return _odd_kernel(min(target, max_k))


def _pixelate(roi: np.ndarray, *, blocks: int = 16) -> np.ndarray:
    """Downscale then nearest-neighbor upscale to destroy fine structure."""
    h, w = roi.shape[:2]
    scale = max(blocks, 2) / max(w, h)
    bw = max(2, int(w * scale))
    bh = max(2, int(h * scale))
    small = cv2.resize(roi, (bw, bh), interpolation=cv2.INTER_AREA)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def blur_region(
    img: np.ndarray,
    bbox: BBox,
    *,
    kernel: int = 75,
    gray_value: int = 200,
    blend_roi_weight: float = 0.3,
    blur_passes: int = 2,
    pixelate_blocks: int = 20,
) -> None:
    """
    Heavily obliterate a rectangular region in-place.

    Pipeline (aligned with auto-gen_adversarial_blur_data.py, strengthened for
    large figure areas):

    1. Blend ROI toward flat gray to kill contrast
    2. Pixelate (downscale / upscale)
    3. Adaptive Gaussian blur (kernel scales with ROI size)
    4. Repeat blur passes
    5. Final gray blend so edges and text do not remain readable
    """
    h, w = img.shape[:2]
    clipped = bbox.clamp(w, h)
    if clipped.area == 0:
        return

    x0, y0, x1, y1 = clipped.x0, clipped.y0, clipped.x1, clipped.y1
    roi = img[y0:y1, x0:x1].copy()
    rh, rw = roi.shape[:2]

    gray_mask = np.full_like(roi, gray_value)
    gray_weight = 1.0 - blend_roi_weight
    roi = cv2.addWeighted(roi, blend_roi_weight, gray_mask, gray_weight, 0)

    roi = _pixelate(roi, blocks=pixelate_blocks)

    k = _effective_kernel(rh, rw, kernel)
    for _ in range(max(1, blur_passes)):
        roi = cv2.GaussianBlur(roi, (k, k), 0)

    roi = cv2.addWeighted(roi, 0.15, gray_mask, 0.85, 0)

    img[y0:y1, x0:x1] = roi


def blur_regions(
    img: np.ndarray,
    bboxes: list[BBox],
    *,
    kernel: int = 75,
) -> None:
    """Blur each bbox region in-place on img."""
    for bbox in bboxes:
        blur_region(img, bbox, kernel=kernel)
