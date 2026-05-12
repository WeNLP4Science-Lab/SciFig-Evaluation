"""Extract PDF pages containing specific figures for adversarial in-context testing.

Uses three strategies to find the correct page:
1. Text search for figure labels (e.g., "Figure 4", "图 4", "Abbildung 4")
2. Embedded image matching (aspect ratio + size comparison)
3. Visual pixel matching (render pages at low res and compare)

Usage:
    python3 scripts/extract_figure_pages.py
"""

import io
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ADV_DATASET = ROOT / "adversarial_dataset"

FIGURE_PATTERNS = {
    "english_only": ["Figure {n}", "Fig. {n}", "Fig {n}"],
    "chinese_only": ["图 {n}", "图{n}", "Figure {n}", "Fig. {n}"],
    "german_only": ["Abbildung {n}", "Abb. {n}", "Figure {n}", "Fig. {n}"],
    "bulgarian_only": ["Фигура {n}", "Фиг. {n}", "Figure {n}"],
    "multi_language": ["Figure {n}", "Fig. {n}", "Fig {n}"],
}


def extract_figure_number(figure_filename):
    match = re.search(r'[Ff]ig(?:ure)?(\d+)', figure_filename)
    return match.group(1) if match else ""


def strategy_text_search(pdf_path, fig_num, subfolder):
    """Strategy 1: Search for figure label in PDF text."""
    patterns = FIGURE_PATTERNS.get(subfolder, FIGURE_PATTERNS["english_only"])
    search_terms = [p.format(n=fig_num) for p in patterns]

    doc = fitz.open(str(pdf_path))
    best_page = None
    best_count = 0

    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        for term in search_terms:
            count = text.lower().count(term.lower())
            if count > best_count:
                best_count = count
                best_page = page_num

    doc.close()
    return best_page


def strategy_image_match(pdf_path, fig_path):
    """Strategy 2: Match embedded images by aspect ratio and size."""
    our_fig = Image.open(fig_path).convert("RGB")
    our_aspect = our_fig.size[0] / our_fig.size[1]
    our_pixels = our_fig.size[0] * our_fig.size[1]

    doc = fitz.open(str(pdf_path))
    best_page = None
    best_score = 0

    for page_num in range(len(doc)):
        for img_info in doc[page_num].get_images(full=True):
            try:
                base = doc.extract_image(img_info[0])
                img = Image.open(io.BytesIO(base["image"])).convert("RGB")
                img_aspect = img.size[0] / img.size[1]
                img_pixels = img.size[0] * img.size[1]

                aspect_diff = abs(our_aspect - img_aspect) / max(our_aspect, 0.01)
                size_ratio = min(our_pixels, img_pixels) / max(our_pixels, img_pixels)

                if aspect_diff < 0.3 and size_ratio > 0.05:
                    score = (1 - aspect_diff) * size_ratio
                    if score > best_score:
                        best_score = score
                        best_page = page_num
            except Exception:
                continue

    doc.close()
    return best_page if best_score > 0.1 else None


def strategy_visual_match(pdf_path, fig_path):
    """Strategy 3: Render pages at low res and look for visual similarity."""
    our_fig = np.array(Image.open(fig_path).convert("RGB").resize((100, 100)))

    doc = fitz.open(str(pdf_path))
    best_page = None
    best_score = 0

    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
        page_img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

        # Slide a window roughly the figure's aspect ratio across the page
        pw, ph = page_img.size
        our_w, our_h = Image.open(fig_path).size
        aspect = our_w / our_h
        win_h = ph // 3
        win_w = int(win_h * aspect)
        if win_w > pw:
            win_w = pw
            win_h = int(win_w / aspect)

        for y in range(0, ph - win_h, win_h // 2):
            for x in range(0, pw - win_w, win_w // 2):
                crop = page_img.crop((x, y, x + win_w, y + win_h))
                crop_arr = np.array(crop.resize((100, 100)))
                # Normalized cross-correlation
                diff = np.mean(np.abs(crop_arr.astype(float) - our_fig.astype(float)))
                similarity = 1 - (diff / 255)
                if similarity > best_score:
                    best_score = similarity
                    best_page = page_num

    doc.close()
    return best_page if best_score > 0.6 else None


def render_page(pdf_path, page_num, dpi=200):
    doc = fitz.open(str(pdf_path))
    scale = dpi / 72
    pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(scale, scale))
    png_bytes = pix.tobytes("png")
    doc.close()
    return png_bytes


def main():
    found = 0
    not_found = 0
    no_pdf = 0
    methods = {"text": 0, "image": 0, "visual": 0, "failed": 0}

    for subfolder_dir in sorted(ADV_DATASET.iterdir()):
        if not subfolder_dir.is_dir():
            continue
        subfolder = subfolder_dir.name

        for fig_dir in sorted(subfolder_dir.iterdir()):
            if not fig_dir.is_dir():
                continue
            fig_key = fig_dir.name

            pdfs = list(fig_dir.glob("paper_*.pdf"))
            if not pdfs:
                no_pdf += 1
                continue

            pdf_path = pdfs[0]
            out_path = fig_dir / f"page_{fig_key}.png"

            # Always re-extract to fix bad ones
            gt_path = fig_dir / f"{fig_key}.json"
            if not gt_path.exists():
                continue
            with open(gt_path) as f:
                gt = json.load(f)

            fig_filename = gt.get("figure_filename", "")
            fig_num = extract_figure_number(fig_filename)
            fig_path = fig_dir / f"{fig_key}.png"

            if not fig_num or not fig_path.exists():
                print(f"  SKIP {fig_key}: no figure number or image")
                not_found += 1
                continue

            page_num = None
            method = "failed"

            # Strategy 1: Text search
            page_num = strategy_text_search(pdf_path, fig_num, subfolder)
            if page_num is not None:
                method = "text"
            else:
                # Strategy 2: Image matching
                page_num = strategy_image_match(pdf_path, fig_path)
                if page_num is not None:
                    method = "image"
                else:
                    # Strategy 3: Visual matching
                    page_num = strategy_visual_match(pdf_path, fig_path)
                    if page_num is not None:
                        method = "visual"

            if page_num is None:
                print(f"  FAIL {fig_key}: could not find figure in PDF")
                not_found += 1
                methods["failed"] += 1
                continue

            png_bytes = render_page(pdf_path, page_num)
            with open(out_path, "wb") as f:
                f.write(png_bytes)

            found += 1
            methods[method] += 1
            print(f"  OK {subfolder}/{fig_key}: page {page_num + 1} [{method}] ({len(png_bytes) // 1024}KB)")

    print(f"\nDone. Extracted: {found}, Not found: {not_found}, No PDF: {no_pdf}")
    print(f"Methods: text={methods['text']}, image={methods['image']}, visual={methods['visual']}, failed={methods['failed']}")


if __name__ == "__main__":
    main()
