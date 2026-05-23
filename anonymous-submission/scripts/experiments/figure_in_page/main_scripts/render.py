"""Render a PDF page to a BGR numpy array via PyMuPDF."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import cv2
import fitz
import numpy as np

if TYPE_CHECKING:
    pass


def render_page_bgr(
    pdf_path: str | Path,
    page_number: int,
    *,
    dpi: int = 150,
) -> tuple[np.ndarray, fitz.Page, fitz.Document]:
    """
    Render one PDF page to a BGR image.

    Args:
        pdf_path: Path to the PDF file.
        page_number: 1-based page index.
        dpi: Render resolution.

    Returns:
        (bgr_image, page, document). Caller must close document when done.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    if page_number < 1 or page_number > doc.page_count:
        doc.close()
        raise ValueError(
            f"page_number must be between 1 and {doc.page_count}, got {page_number}"
        )

    page = doc[page_number - 1]
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix, alpha=False)

    rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        rgb = cv2.cvtColor(rgb, cv2.COLOR_RGBA2RGB)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    return bgr, page, doc
