#!/usr/bin/env python3
"""Helper to write autoagent capability answer JSON files."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QUESTIONS_DIR = ROOT / "anonymous-submission" / "dataset" / "capability_questions"
OUTPUT_DIR = Path(__file__).resolve().parent


def write_figure(fig_id: str, answers: list[dict]) -> Path:
    q_path = QUESTIONS_DIR / f"{fig_id}.json"
    with open(q_path) as f:
        meta = json.load(f)

    questions = meta.get("questions", [])
    if len(answers) != len(questions):
        raise ValueError(f"{fig_id}: expected {len(questions)} answers, got {len(answers)}")

    out_answers = []
    for q, a in zip(questions, answers):
        out_answers.append(
            {
                "category": q["category"],
                "question": q["question"],
                "answer": a["answer"],
                "answer_type": q["answer_type"],
                "reasoning": a["reasoning"],
            }
        )

    payload = {
        "figure_id": fig_id,
        "figure_type": meta.get("figure_type"),
        "model": "autoagent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "answers": out_answers,
    }

    out_path = OUTPUT_DIR / f"{fig_id}.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return out_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python _write_answer.py fig_004 '<json answers list>'")
        raise SystemExit(1)
    fig_id = sys.argv[1]
    answers = json.loads(sys.argv[2])
    path = write_figure(fig_id, answers)
    print(path)
