#!/usr/bin/env python3
"""Small, privacy-safe demonstration of a structured human-review workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import streamlit as st


DIMENSIONS = {
    "problem_correctness": "Problem Correctness / 题目正确性",
    "solution_correctness": "Solution Correctness / 解答正确性",
    "language_quality": "Language Quality / 语言质量",
    "fusion_elegance": "Fusion Elegance / 融合优雅度",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--data", type=Path, default=Path("examples/demo_problems.jsonl"))
    args, _ = parser.parse_known_args()
    return args


@st.cache_data
def load_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            if raw_line.strip():
                rows.append(json.loads(raw_line))
    return rows


def main() -> None:
    st.set_page_config(page_title="Research Review Demo", layout="wide")
    st.title("Structured Human Review Demo")
    st.caption("匿名演示数据；不包含投稿论文或项目内部数据。")

    args = parse_args()
    rows = load_rows(args.data)
    if not rows:
        st.warning("No records found.")
        return

    index = st.sidebar.number_input(
        "Sample index", min_value=1, max_value=len(rows), value=1, step=1
    )
    row = rows[int(index) - 1]

    left, right = st.columns([3, 2])
    with left:
        st.subheader(str(row.get("id", f"sample-{index}")))
        st.markdown("#### Problem")
        st.write(row.get("problem", ""))
        st.markdown("#### Solution")
        st.write(row.get("solution", ""))
        st.markdown("#### Answer")
        st.write(row.get("answer", ""))

    with right:
        st.markdown("#### Scores")
        scores = {
            key: st.slider(label, 1, 5, 3, key=f"{index}-{key}")
            for key, label in DIMENSIONS.items()
        }
        comments = st.text_area("Comments / 评语", key=f"{index}-comments")
        st.info("演示模式不会写入磁盘。")
        st.json({"source_id": row.get("id"), "scores": scores, "comments": comments})


if __name__ == "__main__":
    main()

