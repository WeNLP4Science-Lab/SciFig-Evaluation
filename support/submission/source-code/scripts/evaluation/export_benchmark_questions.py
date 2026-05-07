#!/usr/bin/env python3
"""
Merge all benchmark question files into a single JSON for the dashboard.

Reads from adversarial_experiments/benchmarks/capability/{native,english}/
and writes a merged file to dashboard/public/data/capability_questions.json.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "adversarial_experiments" / "benchmarks" / "capability"
OUTPUT_PATH = ROOT / "dashboard" / "public" / "data" / "capability_questions.json"

SUBFOLDER_TO_LANGUAGE = {
    "bulgarian_only": "bulgarian",
    "chinese_only": "chinese",
    "english_only": "english",
    "german_only": "german",
    "multi_language": "english",
}

# Single-language native files: language name -> filename
SINGLE_LANG_FILES = ["bulgarian", "chinese", "english", "german"]

# Multi-language variant suffixes
MULTI_LANG_SUFFIXES = {"bg": "multi_language_bg", "cn": "multi_language_cn", "de": "multi_language_de", "en": "multi_language_en"}


def _fix_internal_quotes(content: str) -> str:
    """Fix unescaped ASCII quotes inside JSON string values.

    Some benchmark files contain Bulgarian „..." or Chinese \u201c...\u201d
    quotation marks that were saved as plain ASCII double-quotes, which
    breaks the JSON parser.  This function escapes those internal quotes
    while leaving the structural JSON quotes intact.
    """
    fixed_lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        # Only process lines that look like JSON string key-value pairs
        m = re.match(r'^("(?:question|expected_answer)":\s*)"(.*)"(,?)$', stripped)
        if m:
            prefix, value, trailing = m.group(1), m.group(2), m.group(3)
            # Escape any unescaped internal double-quotes in the value
            escaped_value = value.replace('\\"', '\x00').replace('"', '\\"').replace('\x00', '\\"')
            indent = line[: len(line) - len(line.lstrip())]
            fixed_lines.append(f'{indent}{prefix}"{escaped_value}"{trailing}')
        else:
            fixed_lines.append(line)
    return "\n".join(fixed_lines)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try fixing internal quote issues and retry
        fixed = _fix_internal_quotes(content)
        return json.loads(fixed)


def main():
    merged: dict = {}

    # --- Process single-language files (bulgarian, chinese, english, german) ---
    for lang in SINGLE_LANG_FILES:
        native_path = BENCH_DIR / "native" / f"{lang}.json"
        english_path = BENCH_DIR / "english" / f"{lang}.json"

        native_data = load_json(native_path) if native_path.exists() else {}
        english_data = load_json(english_path) if english_path.exists() else {}

        # Collect all figure keys from both files
        all_keys = set(native_data.keys()) | set(english_data.keys())

        for fig_key in all_keys:
            native_entry = native_data.get(fig_key, {})
            english_entry = english_data.get(fig_key, {})

            subfolder = native_entry.get("subfolder") or english_entry.get("subfolder", "")
            native_language = SUBFOLDER_TO_LANGUAGE.get(subfolder, lang)

            merged[fig_key] = {
                "figure_key": fig_key,
                "subfolder": subfolder,
                "native_language": native_language,
                "questions_native": native_entry.get("questions", []),
                "questions_english": english_entry.get("questions", []),
            }

    # --- Process multi_language files ---
    native_multi = load_json(BENCH_DIR / "native" / "multi_language.json")
    english_multi = load_json(BENCH_DIR / "english" / "multi_language.json")

    # Load translated variants
    multi_variants = {}
    for suffix, filename in MULTI_LANG_SUFFIXES.items():
        path = BENCH_DIR / "native" / f"{filename}.json"
        if path.exists():
            multi_variants[suffix] = load_json(path)
        else:
            multi_variants[suffix] = {}

    all_multi_keys = set(native_multi.keys()) | set(english_multi.keys())
    for fig_key in all_multi_keys:
        native_entry = native_multi.get(fig_key, {})
        english_entry = english_multi.get(fig_key, {})

        subfolder = native_entry.get("subfolder") or english_entry.get("subfolder", "")
        native_language = SUBFOLDER_TO_LANGUAGE.get(subfolder, "english")

        entry = {
            "figure_key": fig_key,
            "subfolder": subfolder,
            "native_language": native_language,
            "questions_native": native_entry.get("questions", []),
            "questions_english": english_entry.get("questions", []),
        }

        # Add translated variants
        for suffix, variant_data in multi_variants.items():
            if fig_key in variant_data:
                entry[f"questions_{suffix}"] = variant_data[fig_key].get("questions", [])

        merged[fig_key] = entry

    # Sort by figure key for deterministic output
    merged = dict(sorted(merged.items()))

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    # Summary
    total_figures = len(merged)
    total_questions = sum(
        len(v.get("questions_native", []))
        + len(v.get("questions_english", []))
        + len(v.get("questions_bg", []))
        + len(v.get("questions_cn", []))
        + len(v.get("questions_de", []))
        for v in merged.values()
    )
    print(f"Merged {total_figures} figures with {total_questions} total questions")
    print(f"Output written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
