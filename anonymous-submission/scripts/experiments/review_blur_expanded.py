#!/usr/bin/env python3
"""Visual review of expanded admittance and inductance probes using GPT-4o vision.

Sends the ORIGINAL (unblurred) figure + probe details to GPT-4o to verify:
- Admittance: element is truly unrecoverable once blurred
- Inductance: element is truly inferable from remaining context

Usage:
    python review_blur_expanded.py --type admittance
    python review_blur_expanded.py --type inductance
    python review_blur_expanded.py --type both
"""

from __future__ import annotations
import json
import base64
import os
import argparse
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

ROOT = Path("/Users/thanksgiver/grace/projects/wenlp4science/SciFig-Evaluation")
ENV_PATH = ROOT / ".env"
PROBES_DIR = ROOT / "anonymous-submission/dataset/adversarial/probes"
FIGURES_DIR = ROOT / "anonymous-submission/dataset/figures"
ADMITTANCE_DIR = ROOT / "anonymous-submission/dataset/adversarial/admittance"
INDUCTANCE_DIR = ROOT / "anonymous-submission/dataset/adversarial/inductance"
OUTPUT_DIR = ROOT / "anonymous-submission/results/tasks/adversarial_transforms"

load_dotenv(ENV_PATH)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
)
MODEL = "gpt-4o"


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def review_admittance(fig_id: str) -> tuple[str, str | None]:
    probe_path = PROBES_DIR / f"{fig_id}.json"
    image_path = FIGURES_DIR / f"{fig_id}.png"

    if not probe_path.exists() or not image_path.exists():
        return "error", "missing files"

    probe = json.loads(probe_path.read_text())
    adm = probe.get("selective_blur", {}).get("admittance")
    if not adm:
        return "error", "no admittance probe"

    blurred_text = adm["blurred_text"]
    question = adm.get("question", "")

    b64 = encode_image(image_path)

    prompt = f"""Look at this scientific chart image. I need to verify an ADMITTANCE blur probe.

The plan is to blur (make unreadable) this element: "{blurred_text}"
Question that will be asked after blurring: "{question}"

Check these criteria:
A) Does "{blurred_text}" actually appear in this chart?
B) If "{blurred_text}" were blurred, would it be UNRECOVERABLE? It should NOT be inferable from axis patterns, colour matching, legends, or any other remaining visual context.
C) Is the question answerable from the chart, and does its answer depend on seeing "{blurred_text}"?
D) Is "{blurred_text}" a meaningful chart element (label, value, category) rather than a decoration or axis tick?

Reply with exactly: PASS or REJECT: [reason]"""

    resp = client.chat.completions.create(
        model=MODEL, temperature=0, max_tokens=300,
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
            {"type": "text", "text": prompt},
        ]}],
    )

    answer = resp.choices[0].message.content.strip()
    if answer.startswith("PASS"):
        return "pass", None
    elif answer.startswith("REJECT"):
        return "reject", answer.replace("REJECT:", "").replace("REJECT", "").strip()
    else:
        return "reject", f"Ambiguous: {answer[:200]}"


def review_inductance(fig_id: str) -> tuple[str, str | None]:
    probe_path = PROBES_DIR / f"{fig_id}.json"
    image_path = FIGURES_DIR / f"{fig_id}.png"

    if not probe_path.exists() or not image_path.exists():
        return "error", "missing files"

    probe = json.loads(probe_path.read_text())
    ind = probe.get("selective_blur", {}).get("inductance")
    if not ind:
        return "error", "no inductance probe"

    blurred_text = ind["blurred_text"]
    question = ind.get("question", "")

    b64 = encode_image(image_path)

    prompt = f"""Look at this scientific chart image. I need to verify an INDUCTANCE blur probe.

The plan is to blur (make unreadable) this element: "{blurred_text}"
Question that will be asked after blurring: "{question}"

Check these criteria:
A) Does "{blurred_text}" actually appear in this chart?
B) If "{blurred_text}" were blurred, could someone INFER the correct answer from remaining visual context? For example: a numeric value readable from axis gridlines, a label recoverable from colour matching with a legend, or a pattern continuation.
C) Is the question answerable from the chart, and does its answer depend on "{blurred_text}"?
D) Is the question well-formed and natural?

Reply with exactly: PASS or REJECT: [reason]"""

    resp = client.chat.completions.create(
        model=MODEL, temperature=0, max_tokens=300,
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
            {"type": "text", "text": prompt},
        ]}],
    )

    answer = resp.choices[0].message.content.strip()
    if answer.startswith("PASS"):
        return "pass", None
    elif answer.startswith("REJECT"):
        return "reject", answer.replace("REJECT:", "").replace("REJECT", "").strip()
    else:
        return "reject", f"Ambiguous: {answer[:200]}"


def run_review(probe_type: str):
    review_fn = review_admittance if probe_type == "admittance" else review_inductance
    blur_dir = ADMITTANCE_DIR if probe_type == "admittance" else INDUCTANCE_DIR
    output_path = OUTPUT_DIR / f"{probe_type}_expanded_review.json"

    # Get figures to review (those with blurred images)
    figures = sorted([f.stem for f in blur_dir.glob("*.png")])

    # Load locked (skip those)
    locked_path = ROOT / f"anonymous-submission/dataset/{probe_type}_confirmed.json"
    locked = set(json.load(open(locked_path))) if locked_path.exists() else set()

    candidates = [f for f in figures if f not in locked]
    print(f"\n=== {probe_type.upper()} REVIEW ===")
    print(f"Total blurred: {len(figures)}, locked: {len(locked)}, to review: {len(candidates)}")

    # Load existing results
    if output_path.exists():
        results = json.loads(output_path.read_text())
    else:
        results = {"passed": [], "rejected": [], "errors": []}

    already_done = set(results["passed"])
    already_done |= {r["fig_id"] for r in results["rejected"]}
    already_done |= set(results["errors"])

    remaining = [f for f in candidates if f not in already_done]
    print(f"Already done: {len(already_done)}, remaining: {len(remaining)}")

    for i, fig_id in enumerate(remaining, 1):
        try:
            verdict, reason = review_fn(fig_id)
            if verdict == "pass":
                results["passed"].append(fig_id)
            elif verdict == "reject":
                results["rejected"].append({"fig_id": fig_id, "reason": reason})
            else:
                results["errors"].append(fig_id)
        except Exception as e:
            results["errors"].append(fig_id)
            print(f"  ERROR {fig_id}: {e}")
            time.sleep(2)

        if i % 10 == 0 or i == len(remaining):
            results["summary"] = (
                f"{len(results['passed'])} passed, "
                f"{len(results['rejected'])} rejected, "
                f"{len(results['errors'])} errors"
            )
            output_path.write_text(json.dumps(results, indent=2))
            print(f"  [{i}/{len(remaining)}] {results['summary']}")

        time.sleep(0.3)  # rate limit

    print(f"\nDone. {results.get('summary', '')}")
    print(f"Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["admittance", "inductance", "both"], default="both")
    args = parser.parse_args()

    if args.type in ("admittance", "both"):
        run_review("admittance")
    if args.type in ("inductance", "both"):
        run_review("inductance")


if __name__ == "__main__":
    main()
