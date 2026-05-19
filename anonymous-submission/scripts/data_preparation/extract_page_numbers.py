"""
Extract PDF page numbers for each figure using combined matching:
  1. Caption text search on PDF pages
  2. Figure number text search (e.g., "Figure 4")
  3. Image template matching as tiebreaker

Reads:  dataset/groundtruth/*.json
        dataset/figures/*.png
        thesis-work/Dataset/groundtruth/ (for original figure_filename with Figure number)
        .temp/FigureSense-Data-Bank/ (source PDFs)

Writes: updates dataset/groundtruth/*.json with "pdf_page" field

Usage:
    python extract_page_numbers.py --limit 5
    python extract_page_numbers.py
    python extract_page_numbers.py --figures fig_001 fig_010
"""

from __future__ import annotations

import json
import argparse
import re
import sys
from pathlib import Path

import fitz  # pymupdf
import cv2
import numpy as np

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parent
GROUNDTRUTH_DIR = PROJECT_ROOT / "dataset" / "groundtruth"
FIGURES_DIR = PROJECT_ROOT / "dataset" / "figures"
THESIS_GT_EN = REPO_ROOT / "thesis-work" / "Dataset" / "groundtruth" / "english_only"
THESIS_GT_MULTI = REPO_ROOT / "thesis-work" / "Dataset" / "groundtruth" / "multi_language"
PDF_BASE = REPO_ROOT / ".temp" / "FigureSense-Data-Bank"


def find_pdf(arxiv_id: str) -> Path | None:
    for batch_dir in sorted(PDF_BASE.glob("Batch-*")):
        pdf_dir = batch_dir / "downloaded_pdfs"
        if not pdf_dir.exists():
            continue
        for pdf_file in pdf_dir.glob("*.pdf"):
            if arxiv_id in pdf_file.name:
                return pdf_file
    return None


def get_figure_number(original_file: str) -> str | None:
    """Get the Figure number from the thesis groundtruth's figure_filename field."""
    for gt_dir in [THESIS_GT_EN, THESIS_GT_MULTI]:
        path = gt_dir / original_file
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            filename = data.get("figure_filename", "")
            # Extract FigureN from e.g. "007_2502.06703v1_Figure1.png"
            match = re.search(r'Figure(\d+)', filename)
            if match:
                return match.group(1)
    return None


def search_text_on_pages(doc: fitz.Document, search_text: str) -> list[tuple[int, int]]:
    """Search for text on each page. Returns [(page_num, match_count), ...]."""
    results = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        # Count occurrences (case-insensitive)
        count = text.lower().count(search_text.lower())
        if count > 0:
            results.append((page_num + 1, count))  # 1-indexed
    return results


def image_match_score(fig_path: Path, doc: fitz.Document, page_num: int) -> float:
    """Compute template match score for a figure against a specific page."""
    fig = cv2.imread(str(fig_path))
    if fig is None:
        return 0.0
    fig_gray = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)

    page = doc[page_num - 1]  # 0-indexed
    mat = fitz.Matrix(150 / 72, 150 / 72)
    pix = page.get_pixmap(matrix=mat)
    page_img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n == 4:
        page_gray = cv2.cvtColor(page_img, cv2.COLOR_RGBA2GRAY)
    elif pix.n == 3:
        page_gray = cv2.cvtColor(page_img, cv2.COLOR_RGB2GRAY)
    else:
        page_gray = page_img

    fig_h, fig_w = fig_gray.shape[:2]
    page_h, page_w = page_gray.shape[:2]

    # Scale figure to fit within page
    if fig_h >= page_h or fig_w >= page_w:
        scale = min(page_h / fig_h, page_w / fig_w) * 0.8
        if scale < 0.1:
            return 0.0
        fig_gray = cv2.resize(fig_gray, None, fx=scale, fy=scale)

    fh, fw = fig_gray.shape[:2]
    if fh >= page_h or fw >= page_w:
        return 0.0

    result = cv2.matchTemplate(page_gray, fig_gray, cv2.TM_CCOEFF_NORMED)
    return float(result.max())


def find_page(fig_id: str, gt: dict, fig_path: Path, doc: fitz.Document) -> tuple[int | None, dict]:
    """Find page using combined signals. Returns (page_number, debug_info)."""
    debug = {"signals": {}}

    # Signal 1: Caption text search
    caption = gt.get("caption", "")
    caption_pages = []
    if caption and len(caption) > 15:
        # Use first 60 chars of caption to avoid truncation issues
        search_caption = caption[:60].strip()
        caption_pages = search_text_on_pages(doc, search_caption)
        debug["signals"]["caption"] = {
            "search": search_caption[:40],
            "pages": caption_pages,
        }

    # Signal 2: Figure number search
    original_file = gt.get("original_file", "")
    fig_num = get_figure_number(original_file) if original_file else None
    fignum_pages = []
    if fig_num:
        # Search for "Figure N" with common patterns
        for pattern in [f"Figure {fig_num}", f"Fig. {fig_num}", f"Figure{fig_num}"]:
            matches = search_text_on_pages(doc, pattern)
            if matches:
                fignum_pages.extend(matches)
                break
        debug["signals"]["figure_number"] = {
            "search": f"Figure {fig_num}",
            "pages": fignum_pages,
        }

    # Combine signals
    page_scores: dict[int, float] = {}

    # Caption matches get weight 3
    for page, count in caption_pages:
        page_scores[page] = page_scores.get(page, 0) + 3.0

    # Figure number matches get weight 2 (but only first occurrence,
    # since "Figure N" appears in references too)
    if fignum_pages:
        # The first occurrence is most likely the actual figure
        first_fignum_page = fignum_pages[0][0]
        page_scores[first_fignum_page] = page_scores.get(first_fignum_page, 0) + 2.0

    # If we have candidates, use image matching as tiebreaker
    if page_scores:
        for page in page_scores:
            img_score = image_match_score(fig_path, doc, page)
            page_scores[page] += img_score
            debug["signals"].setdefault("image_scores", {})[str(page)] = round(img_score, 4)

        best_page = max(page_scores, key=lambda p: page_scores[p])
        debug["page_scores"] = {str(k): round(v, 4) for k, v in page_scores.items()}
        debug["method"] = "combined"
        return best_page, debug

    # Fallback: pure image matching across all pages
    best_page = None
    best_score = 0.0
    for page_num in range(1, len(doc) + 1):
        score = image_match_score(fig_path, doc, page_num)
        if score > best_score:
            best_score = score
            best_page = page_num

    debug["signals"]["image_fallback"] = {"best_page": best_page, "score": round(best_score, 4)}
    debug["method"] = "image_fallback"
    return best_page if best_score >= 0.15 else None, debug


def get_figure_ids(limit: int | None = None, figures: list[str] | None = None) -> list[str]:
    if figures:
        return figures
    all_ids = sorted(p.stem for p in GROUNDTRUTH_DIR.glob("*.json"))
    return all_ids[:limit] if limit else all_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--figures", nargs="+")
    parser.add_argument("--force", action="store_true", help="Overwrite existing pdf_page")
    args = parser.parse_args()

    fig_ids = get_figure_ids(args.limit, args.figures)

    print(f"Extracting page numbers for {len(fig_ids)} figures")
    print(f"PDF source: {PDF_BASE}")
    print("-" * 60)

    found, skipped, no_pdf, failed = 0, 0, 0, 0

    for i, fig_id in enumerate(fig_ids, 1):
        gt_path = GROUNDTRUTH_DIR / f"{fig_id}.json"
        fig_path = FIGURES_DIR / f"{fig_id}.png"

        with open(gt_path) as f:
            gt = json.load(f)

        if "pdf_page" in gt and not args.force:
            skipped += 1
            continue

        arxiv_id = gt.get("arxiv_id", "")
        pdf_path = find_pdf(arxiv_id)
        if not pdf_path:
            no_pdf += 1
            print(f"  {fig_id}: PDF not found for {arxiv_id}")
            continue

        doc = fitz.open(str(pdf_path))
        page, debug = find_page(fig_id, gt, fig_path, doc)
        doc.close()

        if page:
            gt["pdf_page"] = page
            with open(gt_path, "w") as f:
                json.dump(gt, f, indent=2)
            found += 1
            method = debug.get("method", "?")
            print(f"  {fig_id}: page {page} ({method})")
        else:
            failed += 1
            print(f"  {fig_id}: FAILED to find page")

        if i % 25 == 0:
            print(f"  [{i}/{len(fig_ids)}] {found} found, {skipped} skipped, {no_pdf} no PDF, {failed} failed")

    print("-" * 60)
    print(f"Done. {found} found, {skipped} skipped, {no_pdf} no PDF, {failed} failed.")


if __name__ == "__main__":
    main()
