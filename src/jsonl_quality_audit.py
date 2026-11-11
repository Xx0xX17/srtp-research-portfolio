#!/usr/bin/env python3
"""Audit a JSONL problem set without modifying the source file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ("id", "problem", "solution", "answer")
EMPTY_MARKERS = {"", "null", "none", "n/a", "not available"}


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in EMPTY_MARKERS


def audit(path: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    valid_rows = 0

    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue

            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                issues.append(
                    {
                        "line": line_number,
                        "id": None,
                        "problems": [f"JSON parse error: {exc.msg}"],
                    }
                )
                continue

            if not isinstance(row, dict):
                issues.append(
                    {
                        "line": line_number,
                        "id": None,
                        "problems": ["Top-level value is not an object"],
                    }
                )
                continue

            valid_rows += 1
            row_problems = [
                f"Missing or empty field: {field}"
                for field in REQUIRED_FIELDS
                if is_empty(row.get(field))
            ]
            if row_problems:
                issues.append(
                    {
                        "line": line_number,
                        "id": row.get("id"),
                        "problems": row_problems,
                    }
                )

    return {
        "file": path.name,
        "valid_json_objects": valid_rows,
        "rows_with_issues": len(issues),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="JSONL file to audit")
    args = parser.parse_args()

    if not args.jsonl.is_file():
        parser.error(f"File not found: {args.jsonl}")

    print(json.dumps(audit(args.jsonl), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

