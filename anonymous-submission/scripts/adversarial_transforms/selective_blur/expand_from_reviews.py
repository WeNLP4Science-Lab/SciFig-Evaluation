"""
Expand admittance and inductance blur sets from dashboard reviews.

Reads reviews from /tmp/tempmay2026admittance.json and /tmp/tempmay2026inductance.json.
For approved reviews: uses existing identification targets.
For rejected reviews with new targets: uses reviewer's new blur target + question.

Performs OCR matching, blur application, and probe file updates.

Usage:
    python expand_from_reviews.py --dry-run     # preview only
    python expand_from_reviews.py               # apply blurs
"""

import json
import argparse
import cv2
import numpy as np
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = PROJECT_ROOT / "dataset"
FIGURES_DIR = DATASET_DIR / "figures"
ADVERSARIAL_DIR = DATASET_DIR / "adversarial"
ADMITTANCE_DIR = ADVERSARIAL_DIR / "admittance"
INDUCTANCE_DIR = ADVERSARIAL_DIR / "inductance"
PROBES_DIR = ADVERSARIAL_DIR / "probes"
OCR_DIR = PROJECT_ROOT / "results" / "tasks" / "adversarial_transforms" / "selective_blur" / "ocr_results"
IDENTIFICATIONS_DIR = PROJECT_ROOT / "results" / "tasks" / "adversarial_transforms" / "selective_blur" / "identifications"
REGIONS_PATH = ADVERSARIAL_DIR / "regions.json"

# Blur settings
BLUR_KERNEL = 75
BLUR_GRAY_BLEND = 0.7


def _normalize(s):
    s = s.lower().strip()
    s = s.replace('l', '1').replace('o', '0')
    s = ''.join(c for c in s if c.isalnum())
    return s


def _similarity(a, b):
    if not a or not b:
        return 0.0
    a_norm, b_norm = _normalize(a), _normalize(b)
    if a_norm == b_norm:
        return 1.0
    if a_norm in b_norm or b_norm in a_norm:
        return min(len(a_norm), len(b_norm)) / max(len(a_norm), len(b_norm))
    common = sum(1 for c in a_norm if c in b_norm)
    return common / max(len(a_norm), len(b_norm))


def find_bbox(ocr_texts, target_text):
    target_lower = target_text.lower().strip()
    target_norm = _normalize(target_text)

    for t in ocr_texts:
        if t["text"].lower().strip() == target_lower:
            return t["bbox"]

    for t in ocr_texts:
        if _normalize(t["text"]) == target_norm:
            return t["bbox"]

    scored = []
    for t in ocr_texts:
        sim = _similarity(target_text, t["text"])
        if sim >= 0.5:
            scored.append((t, sim))

    if scored:
        scored.sort(key=lambda x: (x[1], -abs(len(x[0]["text"]) - len(target_text))), reverse=True)
        return scored[0][0]["bbox"]

    return None


def apply_blur(image_path, bbox, output_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return False

    x1, y1 = bbox["x_min"], bbox["y_min"]
    x2, y2 = bbox["x_max"], bbox["y_max"]

    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return False

    roi = img[y1:y2, x1:x2]

    if BLUR_GRAY_BLEND > 0:
        gray_mask = np.full_like(roi, 200)
        roi = cv2.addWeighted(roi, 1 - BLUR_GRAY_BLEND, gray_mask, BLUR_GRAY_BLEND, 0)

    kernel = BLUR_KERNEL if BLUR_KERNEL % 2 == 1 else BLUR_KERNEL + 1
    blurred = cv2.GaussianBlur(roi, (kernel, kernel), 0)
    img[y1:y2, x1:x2] = blurred

    cv2.imwrite(str(output_path), img)
    return True


def process_review(review, probe_type, dry_run=False):
    """Process a single review entry."""
    fig_id = review["figure_id"]
    status = review["status"]
    new_target = review.get("new_blur_target", "")
    new_question = review.get("new_question", "")
    notes = review.get("notes", "")

    # Load OCR
    ocr_path = OCR_DIR / f"{fig_id}.json"
    if not ocr_path.exists():
        return {"fig_id": fig_id, "status": "skip", "reason": "no_ocr"}

    with open(ocr_path) as f:
        ocr_data = json.load(f)
    ocr_texts = ocr_data.get("texts", [])

    # Load existing probe
    probe_path = PROBES_DIR / f"{fig_id}.json"
    if probe_path.exists():
        with open(probe_path) as f:
            probe = json.load(f)
    else:
        probe = {"figure_id": fig_id, "selective_blur": {}}

    # Load existing identifications for approved reviews
    id_path = IDENTIFICATIONS_DIR / f"{fig_id}.json"

    # Determine blur target and question
    if status == "approved":
        # Use existing identification
        if id_path.exists():
            with open(id_path) as f:
                identification = json.load(f)
            candidates = identification.get(f"{probe_type}_candidates", [])
            if not candidates:
                return {"fig_id": fig_id, "status": "skip", "reason": "no_candidates"}
            # Use top candidate
            target_text = candidates[0].get("selected_text", "")
            question = candidates[0].get("question", "")
        else:
            return {"fig_id": fig_id, "status": "skip", "reason": "no_identification"}
    elif status == "rejected" and new_target:
        # Use reviewer's new target
        target_text = new_target
        question = new_question if new_question else ""
    else:
        return {"fig_id": fig_id, "status": "skip", "reason": "rejected_no_target"}

    if not target_text:
        return {"fig_id": fig_id, "status": "skip", "reason": "empty_target"}

    # Find OCR bbox
    bbox = find_bbox(ocr_texts, target_text)
    if not bbox:
        return {"fig_id": fig_id, "status": "fail", "reason": f"no_bbox_match for '{target_text}'"}

    # Output paths
    if probe_type == "admittance":
        out_dir = ADMITTANCE_DIR
    else:
        out_dir = INDUCTANCE_DIR

    out_path = out_dir / f"{fig_id}.png"
    fig_path = FIGURES_DIR / f"{fig_id}.png"

    if not fig_path.exists():
        return {"fig_id": fig_id, "status": "skip", "reason": "no_figure"}

    if dry_run:
        return {
            "fig_id": fig_id,
            "status": "would_process",
            "target": target_text,
            "question": question[:80],
            "bbox": bbox,
        }

    # Apply blur
    success = apply_blur(fig_path, bbox, out_path)
    if not success:
        return {"fig_id": fig_id, "status": "fail", "reason": "blur_failed"}

    # Update probe file
    probe["selective_blur"][probe_type] = {
        "blurred_text": target_text,
        "question": question,
        "status": "confirmed",
        "reviewer_notes": notes,
    }

    # Save OCR texts in probe for reference
    probe["ocr_texts"] = [t["text"] for t in ocr_texts]

    with open(probe_path, "w") as f:
        json.dump(probe, f, indent=2)

    return {"fig_id": fig_id, "status": "success", "target": target_text}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Ensure output dirs exist
    ADMITTANCE_DIR.mkdir(parents=True, exist_ok=True)
    INDUCTANCE_DIR.mkdir(parents=True, exist_ok=True)

    # Load locked figures
    adm_confirmed = DATASET_DIR / "admittance_confirmed.json"
    ind_confirmed = DATASET_DIR / "inductance_confirmed.json"
    locked_adm = set(json.load(open(adm_confirmed))) if adm_confirmed.exists() else set()
    locked_ind = set(json.load(open(ind_confirmed))) if ind_confirmed.exists() else set()

    # Load reviews
    with open("/tmp/tempmay2026admittance.json") as f:
        adm_reviews = json.load(f)
    with open("/tmp/tempmay2026inductance.json") as f:
        ind_reviews = json.load(f)

    # Process admittance
    print("=== ADMITTANCE ===")
    adm_results = {"success": 0, "fail": 0, "skip": 0, "would_process": 0}
    for review in adm_reviews:
        if review["figure_id"] in locked_adm:
            continue
        result = process_review(review, "admittance", dry_run=args.dry_run)
        adm_results[result["status"]] = adm_results.get(result["status"], 0) + 1
        if result["status"] in ("fail", "would_process"):
            print(f"  {result}")
    print(f"  Results: {adm_results}")

    # Process inductance
    print("\n=== INDUCTANCE ===")
    ind_results = {"success": 0, "fail": 0, "skip": 0, "would_process": 0}
    for review in ind_reviews:
        if review["figure_id"] in locked_ind:
            continue
        result = process_review(review, "inductance", dry_run=args.dry_run)
        ind_results[result["status"]] = ind_results.get(result["status"], 0) + 1
        if result["status"] in ("fail", "would_process"):
            print(f"  {result}")
    print(f"  Results: {ind_results}")

    if not args.dry_run:
        # Count final totals
        adm_count = len(list(ADMITTANCE_DIR.glob("*.png")))
        ind_count = len(list(INDUCTANCE_DIR.glob("*.png")))
        print(f"\n=== FINAL TOTALS ===")
        print(f"Admittance blurred images: {adm_count}")
        print(f"Inductance blurred images: {ind_count}")


if __name__ == "__main__":
    main()
