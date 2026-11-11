#!/usr/bin/env python3
"""Summarize the latest final review for each source item."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


DIMENSIONS = (
    "problem_correctness",
    "solution_correctness",
    "language_quality",
    "fusion_elegance",
)


def load_latest_final_reviews(path: Path) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            if not raw_line.strip():
                continue
            row = json.loads(raw_line)
            if row.get("review_status") != "final":
                continue
            source_id = str(row.get("source_id", "")).strip()
            if not source_id:
                continue
            previous = latest.get(source_id)
            if previous is None or str(row.get("review_time", "")) >= str(
                previous.get("review_time", "")
            ):
                latest[source_id] = row
    return latest


def summarize(reviews: dict[str, dict[str, Any]]) -> dict[str, Any]:
    averages: dict[str, float | None] = {}
    for dimension in DIMENSIONS:
        values = [
            row.get("scores", {}).get(dimension)
            for row in reviews.values()
            if isinstance(row.get("scores", {}).get(dimension), (int, float))
        ]
        averages[dimension] = round(mean(values), 2) if values else None

    return {
        "unique_final_reviews": len(reviews),
        "average_scores": averages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Review JSONL file")
    args = parser.parse_args()

    if not args.jsonl.is_file():
        parser.error(f"File not found: {args.jsonl}")

    reviews = load_latest_final_reviews(args.jsonl)
    print(json.dumps(summarize(reviews), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

