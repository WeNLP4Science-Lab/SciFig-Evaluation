"""Quick script to ask 3 models the same question on the ORIGINAL (unblurred) multi_fig_004."""

import json
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from llm_generation.models import get_annotator

IMAGE = str(ROOT / "adversarial_experiments/figures/multi_language/multi_fig_004/original.png")
QUESTION = "Which character category in the outer ring is positioned between Movie Characters and Novel Characters?"
OUTPUT_DIR = ROOT / "output" / "quick_original_check"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["gpt-5.2", "claude-opus-4.6", "gemini-3.1-pro"]

for model_name in MODELS:
    out_file = OUTPUT_DIR / f"{model_name}.json"
    if out_file.exists():
        print(f"[SKIP] {model_name} — already exists")
        d = json.load(open(out_file))
        print(f"  Answer: {d['answer']}\n")
        continue

    print(f"[RUN] {model_name}...")
    try:
        annotator = get_annotator(model_name)
        prompt = f"Look at this scientific figure carefully and answer the following question:\n\n{QUESTION}\n\nProvide a direct, concise answer."
        answer = annotator.annotate_figure(
            prompt=prompt,
            image_path=IMAGE,
            caption="",
            paper_title=""
        )
        result = {
            "model": model_name,
            "question": QUESTION,
            "image": "original (unblurred)",
            "answer": answer
        }
        json.dump(result, open(out_file, "w"), indent=2)
        print(f"  Answer: {answer}\n")
    except Exception as e:
        print(f"  ERROR: {e}\n")

print("Done.")
