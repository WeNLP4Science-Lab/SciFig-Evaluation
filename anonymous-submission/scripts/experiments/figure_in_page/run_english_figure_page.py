"""
Batch-generate page and adversarial images from figure_metadata.csv.

Usage (from this directory):
    python run_english_figure_page.py              # all figures
    python run_english_figure_page.py --all
    python run_english_figure_page.py --limit 5    # first 5 rows only
    python run_english_figure_page.py fig_040      # one figure (page from CSV)
    python run_english_figure_page.py fig_040 25    # one figure, page override
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

from blur_figure_in_page import process_figure_page, resolve_figure_paths

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

_EXPERIMENT_ROOT = Path(__file__).resolve().parent
_METADATA_CSV = _EXPERIMENT_ROOT / "figure_metadata.csv"
_SUMMARY_CSV = _EXPERIMENT_ROOT / "generated" / "batch_summary.csv"
_PROGRESS_EVERY = 25

_SUMMARY_FIELDS = [
    "figure_id",
    "pdf_page",
    "status",
    "match_score",
    "second_best_score",
    "page_image",
    "adversarial_image",
    "message",
]


def load_metadata(csv_path: Path) -> list[dict[str, str]]:
    """Load figure_id and pdf_page rows from metadata CSV."""
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            figure_id = (row.get("figure_id") or "").strip()
            pdf_page = (row.get("pdf_page") or "").strip()
            if not figure_id or not pdf_page:
                continue
            try:
                int(pdf_page)
            except ValueError:
                logger.warning("Skipping %s: invalid pdf_page %r", figure_id, pdf_page)
                continue
            rows.append({"figure_id": figure_id, "pdf_page": pdf_page})
    return rows


def lookup_page(metadata: list[dict[str, str]], figure_id: str) -> int | None:
    for row in metadata:
        if row["figure_id"] == figure_id:
            return int(row["pdf_page"])
    return None


def result_row(
    figure_id: str,
    pdf_page: int,
    status: str,
    *,
    match_score: float | None = None,
    second_best_score: float | None = None,
    page_image: str = "",
    adversarial_image: str = "",
    message: str = "",
) -> dict[str, str]:
    return {
        "figure_id": figure_id,
        "pdf_page": str(pdf_page),
        "status": status,
        "match_score": "" if match_score is None else f"{match_score:.6f}",
        "second_best_score": "" if second_best_score is None else f"{second_best_score:.6f}",
        "page_image": page_image,
        "adversarial_image": adversarial_image,
        "message": message,
    }


def process_one(
    figure_id: str,
    page_number: int,
    base_dir: Path,
    **match_kwargs,
) -> dict[str, str]:
    paths = resolve_figure_paths(figure_id, base_dir)

    if not paths["pdf"].is_file():
        logger.warning("%s: missing PDF %s", figure_id, paths["pdf"])
        return result_row(
            figure_id, page_number, "missing_pdf", message=str(paths["pdf"])
        )
    if not paths["figure"].is_file():
        logger.warning("%s: missing figure %s", figure_id, paths["figure"])
        return result_row(
            figure_id, page_number, "missing_figure", message=str(paths["figure"])
        )

    try:
        outcome = process_figure_page(
            figure_id, page_number, base_dir=base_dir, **match_kwargs
        )
    except Exception as exc:
        logger.exception("%s: unexpected error", figure_id)
        return result_row(figure_id, page_number, "error", message=str(exc))

    if outcome.match_found:
        return result_row(
            figure_id,
            page_number,
            "ok",
            match_score=outcome.match_score,
            second_best_score=outcome.second_best_score,
            page_image=str(outcome.page_image_path),
            adversarial_image=str(outcome.adversarial_image_path or ""),
            message=outcome.match_method or "",
        )

    return result_row(
        figure_id,
        page_number,
        "match_failed",
        match_score=outcome.match_score,
        second_best_score=outcome.second_best_score,
        page_image=str(outcome.page_image_path),
        message=outcome.failure_reason or "",
    )


def write_summary(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def run_batch(
    metadata: list[dict[str, str]],
    *,
    base_dir: Path,
    limit: int | None = None,
    **match_kwargs,
) -> list[dict[str, str]]:
    rows = metadata[:limit] if limit is not None else metadata
    results: list[dict[str, str]] = []
    total = len(rows)

    for i, row in enumerate(rows, start=1):
        figure_id = row["figure_id"]
        page_number = int(row["pdf_page"])
        results.append(process_one(figure_id, page_number, base_dir, **match_kwargs))

        if i % _PROGRESS_EVERY == 0 or i == total:
            logger.info("Progress: %s / %s", i, total)

    return results


def print_counts(results: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    for row in results:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    logger.info(
        "Finished: %s total | ok=%s match_failed=%s missing_pdf=%s "
        "missing_figure=%s error=%s",
        len(results),
        counts.get("ok", 0),
        counts.get("match_failed", 0),
        counts.get("missing_pdf", 0),
        counts.get("missing_figure", 0),
        counts.get("error", 0),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate page images from figure_metadata.csv")
    parser.add_argument(
        "figure_id",
        nargs="?",
        help="Process one figure (e.g. fig_040). Omit to run batch.",
    )
    parser.add_argument(
        "page_number",
        nargs="?",
        type=int,
        help="Optional page override for single-figure mode.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run batch over all metadata rows (default when figure_id omitted).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N metadata rows (batch mode).",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=_METADATA_CSV,
        help="Path to figure_metadata.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=_SUMMARY_CSV,
        help="Path for batch summary CSV output",
    )
    parser.add_argument(
        "--scale-min",
        type=float,
        default=0.25,
        help="Minimum reference scale for figure matching (default 0.25)",
    )
    parser.add_argument(
        "--scale-max",
        type=float,
        default=2.5,
        help="Maximum reference scale for figure matching (default 2.5)",
    )
    return parser.parse_args(argv)


def _match_kwargs_from_args(args: argparse.Namespace) -> dict:
    return {
        "scale_min": args.scale_min,
        "scale_max": args.scale_max,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    base_dir = _EXPERIMENT_ROOT

    if not args.metadata.is_file():
        logger.error("Metadata CSV not found: %s", args.metadata)
        return 1

    metadata = load_metadata(args.metadata)
    if not metadata:
        logger.error("No valid rows in %s", args.metadata)
        return 1

    match_kwargs = _match_kwargs_from_args(args)

    if args.figure_id:
        figure_id = args.figure_id
        if args.page_number is not None:
            page_number = args.page_number
        else:
            page = lookup_page(metadata, figure_id)
            if page is None:
                logger.error("figure_id %s not found in metadata", figure_id)
                return 1
            page_number = page

        row = process_one(figure_id, page_number, base_dir, **match_kwargs)
        print(f"figure_id: {row['figure_id']}")
        print(f"pdf_page: {row['pdf_page']}")
        print(f"status: {row['status']}")
        print(f"match_score: {row['match_score']}")
        print(f"second_best_score: {row['second_best_score']}")
        print(f"page_image: {row['page_image']}")
        print(f"adversarial_image: {row['adversarial_image']}")
        print(f"message: {row['message']}")
        return 0 if row["status"] in ("ok", "match_failed") else 1

    results = run_batch(metadata, base_dir=base_dir, limit=args.limit, **match_kwargs)
    write_summary(results, args.summary)
    print_counts(results)
    logger.info("Summary written to %s", args.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
