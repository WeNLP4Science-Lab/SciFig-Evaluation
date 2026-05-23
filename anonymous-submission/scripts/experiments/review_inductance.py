#!/usr/bin/env python3
"""Visual review of 132 inductance probes using GPT-4o vision on Azure."""

from __future__ import annotations
import json
import base64
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

# --- paths ---
ROOT = Path("/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation")
ENV_PATH = ROOT / ".env"
CANDIDATES = ROOT / "anonymous-submission/results/tasks/adversarial_transforms/inductance_deep_review.json"
PROBES_DIR = ROOT / "anonymous-submission/dataset/adversarial/probes"
FIGURES_DIR = ROOT / "anonymous-submission/dataset/figures"
OUTPUT = ROOT / "anonymous-submission/results/tasks/adversarial_transforms/inductance_visual_review.json"

load_dotenv(ENV_PATH)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
)
MODEL = "gpt-4o"

# --- load candidates ---
candidates = json.loads(CANDIDATES.read_text())["passed"]
print(f"Loaded {len(candidates)} candidates")

# --- load existing results (skip-if-exists) ---
if OUTPUT.exists():
    results = json.loads(OUTPUT.read_text())
else:
    results = {"passed": [], "rejected": [], "errors": []}

already_done = set(results["passed"])
already_done |= {r["fig_id"] for r in results["rejected"]}
already_done |= set(results["errors"])

remaining = [f for f in candidates if f not in already_done]
print(f"Already done: {len(already_done)}, remaining: {len(remaining)}")


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def review_figure(fig_id: str) -> tuple[str, str | None]:
    """Returns ('pass', None) or ('reject', reason) or ('error', msg)."""
    probe_path = PROBES_DIR / f"{fig_id}.json"
    image_path = FIGURES_DIR / f"{fig_id}.png"

    if not probe_path.exists():
        return "error", f"probe file missing: {probe_path}"
    if not image_path.exists():
        return "error", f"image missing: {image_path}"

    probe = json.loads(probe_path.read_text())
    ind = probe["selective_blur"]["inductance"]
    blurred_text = ind["blurred_text"]
    question = ind["question"]
    candidate_type = ind.get("candidate_type", "unknown")

    b64 = encode_image(image_path)

    prompt = f"""Look at this scientific chart image. I need to verify an inductance probe for a blur experiment.

Blurred text: {blurred_text}
Question: {question}
Expected answer: {blurred_text}
Candidate type: {candidate_type}

Check these 4 things:
A) Is this a multi-panel figure with multiple separate charts? If yes, could the blur be on a different chart than the question refers to?
B) Would the answer to the question actually be '{blurred_text}'? The answer must be exactly the blurred text.
C) If the blurred text were hidden, could someone infer it from the remaining visible context? (numeric from axis sequence, text from naming pattern)
D) Is the question well-formed and natural?

Reply with exactly: PASS or REJECT: [reason]"""

    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    answer = resp.choices[0].message.content.strip()

    if answer.startswith("PASS"):
        return "pass", None
    elif answer.startswith("REJECT"):
        reason = answer.replace("REJECT:", "").replace("REJECT", "").strip()
        return "reject", reason
    else:
        # Ambiguous response – treat as rejection with the full text
        return "reject", f"Ambiguous GPT response: {answer}"


def save():
    results["summary"] = (
        f"{len(results['passed'])} passed, "
        f"{len(results['rejected'])} rejected, "
        f"{len(results['errors'])} errors"
    )
    OUTPUT.write_text(json.dumps(results, indent=2))


# --- main loop ---
for i, fig_id in enumerate(remaining, 1):
    try:
        verdict, reason = review_figure(fig_id)
        if verdict == "pass":
            results["passed"].append(fig_id)
        elif verdict == "reject":
            results["rejected"].append({"fig_id": fig_id, "reason": reason})
        else:
            results["errors"].append(fig_id)
    except Exception as e:
        results["errors"].append(fig_id)
        print(f"  ERROR {fig_id}: {e}")

    if i % 10 == 0 or i == len(remaining):
        save()
        print(f"[{i}/{len(remaining)}] {len(results['passed'])} pass, "
              f"{len(results['rejected'])} reject, {len(results['errors'])} err")

save()
print(f"\nDone. {results['summary']}")
print(f"Saved to {OUTPUT}")
