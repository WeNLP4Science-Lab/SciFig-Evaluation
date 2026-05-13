"""
Stage 3: Select best question per category and finalize dataset.

For each figure + category:
  - From accepted candidates, pick the one rated hardest
  - If none accepted, write to review queue
  - Write clean output to dataset/capability_questions/

Reads from:  results/capability_generation/validation/
Writes to:   dataset/capability_questions/  (final)
             results/capability_generation/review/  (flagged)
             results/capability_generation/report.json

Usage:
    python filter.py
    python filter.py --dry-run
"""

from __future__ import annotations

import json
import argparse
from collections import Counter

from config import VALIDATION_DIR, FINAL_OUTPUT_DIR, RESULTS_DIR, CATEGORIES


REVIEW_DIR = RESULTS_DIR / "review"
DIFFICULTY_RANK = {"very_hard": 2, "hard": 1}


def select_best(candidates: list[dict]) -> tuple[dict | None, list[dict]]:
    """From validated candidates, pick best accepted one. Return (selected, rejected)."""
    accepted = [c for c in candidates if c.get("validation", {}).get("overall") == "ACCEPT"]
    rejected = [c for c in candidates if c.get("validation", {}).get("overall") != "ACCEPT"]

    if not accepted:
        return None, candidates

    # Sort by difficulty (very_hard > hard), take first
    accepted.sort(
        key=lambda c: DIFFICULTY_RANK.get(c.get("validation", {}).get("difficulty", ""), 0),
        reverse=True,
    )
    selected = accepted[0]
    return selected, rejected


def clean_question(q: dict) -> dict:
    """Strip validation metadata for final dataset output."""
    return {k: v for k, v in q.items() if k != "validation"}


def process_figure(data: dict) -> tuple[dict, dict]:
    """Process one figure. Returns (final_output, review_output)."""
    final = {
        "figure_id": data["figure_id"],
        "figure_type": data.get("figure_type", ""),
        "generator_model": data.get("generator_model", ""),
        "questions": [],
    }
    review = {
        "figure_id": data["figure_id"],
        "questions": [],
    }

    for cat in CATEGORIES:
        candidates = data.get("categories", {}).get(cat, [])
        selected, rejected = select_best(candidates)

        if selected:
            q = clean_question(selected)
            q["difficulty"] = selected.get("validation", {}).get("difficulty", "hard")
            final["questions"].append(q)
        else:
            # All rejected — add to review with rejection reasons
            for c in rejected:
                rq = {**c}
                rq["rejection_reasons"] = [
                    f"{k}: {v.get('reason', '')}"
                    for k, v in c.get("validation", {}).items()
                    if isinstance(v, dict) and v.get("verdict") == "FAIL"
                ]
                review["questions"].append(rq)

    return final, review


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not VALIDATION_DIR.exists():
        print(f"No validated data at {VALIDATION_DIR}. Run validate.py first.")
        return

    all_data = []
    for p in sorted(VALIDATION_DIR.glob("*.json")):
        with open(p) as f:
            all_data.append(json.load(f))

    if not all_data:
        print("No validated files found.")
        return

    print(f"Selecting best questions from {len(all_data)} figures")
    print("-" * 60)

    finals, reviews = [], []
    accepted_by_cat = Counter()
    review_by_cat = Counter()

    for data in all_data:
        final, review = process_figure(data)
        finals.append(final)
        if review.get("questions"):
            reviews.append(review)
        for q in final.get("questions", []):
            accepted_by_cat[q["category"]] += 1
        for q in review.get("questions", []):
            review_by_cat[q.get("category", "?")] += 1

    total_accepted = sum(len(f.get("questions", [])) for f in finals)
    total_review = sum(len(r.get("questions", [])) for r in reviews)
    figures_complete = sum(1 for f in finals if len(f.get("questions", [])) == len(CATEGORIES))
    figures_incomplete = len(all_data) - figures_complete

    report = {
        "total_figures": len(all_data),
        "figures_with_all_categories": figures_complete,
        "figures_needing_review": figures_incomplete,
        "total_questions_accepted": total_accepted,
        "total_questions_for_review": total_review,
        "accepted_by_category": dict(accepted_by_cat),
        "review_by_category": dict(review_by_cat),
    }

    print(f"\nResults:")
    print(f"  Figures complete (all 4 categories): {figures_complete}/{len(all_data)}")
    print(f"  Figures needing review:              {figures_incomplete}")
    print(f"  Questions accepted:                  {total_accepted}")
    print(f"  Questions for review:                {total_review}")
    print(f"\nAccepted by category:")
    for cat in CATEGORIES:
        a = accepted_by_cat.get(cat, 0)
        r = review_by_cat.get(cat, 0)
        print(f"  {cat}: {a} accepted, {r} for review")

    if not args.dry_run:
        FINAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        REVIEW_DIR.mkdir(parents=True, exist_ok=True)

        for f in finals:
            if f.get("questions"):
                with open(FINAL_OUTPUT_DIR / f"{f['figure_id']}.json", "w") as fh:
                    json.dump(f, fh, indent=2)

        for r in reviews:
            if r.get("questions"):
                with open(REVIEW_DIR / f"{r['figure_id']}.json", "w") as fh:
                    json.dump(r, fh, indent=2)

        with open(RESULTS_DIR / "report.json", "w") as fh:
            json.dump(report, fh, indent=2)

        print(f"\nFinal dataset: {FINAL_OUTPUT_DIR}")
        print(f"Review queue:  {REVIEW_DIR}")
        print(f"Report:        {RESULTS_DIR / 'report.json'}")
    else:
        print("\n(dry run)")


if __name__ == "__main__":
    main()
