#!/usr/bin/env python3
"""Export all benchmark data (capability, hallucination, prompt_reverse, caption_bias)
into a single JSON keyed by figure_key for the dashboard."""

import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BENCHMARKS = os.path.join(ROOT, 'adversarial_experiments', 'benchmarks')
OUTPUT = os.path.join(ROOT, 'dashboard', 'public', 'data', 'all_benchmarks.json')

SUBFOLDER_TO_LANG = {
    'bulgarian_only': 'bulgarian',
    'chinese_only': 'chinese',
    'english_only': 'english',
    'german_only': 'german',
    'multi_language': 'english',
}

LANG_FILES = ['bulgarian.json', 'chinese.json', 'english.json', 'german.json', 'multi_language.json']


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    merged: dict = {}

    # 1. Capability questions
    cap_dir = os.path.join(BENCHMARKS, 'capability', 'native')
    for fname in LANG_FILES:
        fpath = os.path.join(cap_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [skip] {fpath}")
            continue
        data = load_json(fpath)
        for fig_key, fig_data in data.items():
            subfolder = fig_data.get('subfolder', '')
            if fig_key not in merged:
                merged[fig_key] = {
                    'figure_key': fig_key,
                    'subfolder': subfolder,
                    'native_language': SUBFOLDER_TO_LANG.get(subfolder, 'english'),
                }
            merged[fig_key]['capability_questions'] = fig_data.get('questions', [])

    # 2. Hallucination probes
    hall_dir = os.path.join(BENCHMARKS, 'adversarial', 'hallucination', 'native')
    for fname in LANG_FILES:
        fpath = os.path.join(hall_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [skip] {fpath}")
            continue
        data = load_json(fpath)
        for fig_key, fig_data in data.items():
            subfolder = fig_data.get('subfolder', '')
            if fig_key not in merged:
                merged[fig_key] = {
                    'figure_key': fig_key,
                    'subfolder': subfolder,
                    'native_language': SUBFOLDER_TO_LANG.get(subfolder, 'english'),
                }
            merged[fig_key]['hallucination_probes'] = fig_data.get('probes', [])

    # 3. Prompt reverse pairs
    pr_dir = os.path.join(BENCHMARKS, 'adversarial', 'prompt_reverse', 'native')
    for fname in LANG_FILES:
        fpath = os.path.join(pr_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [skip] {fpath}")
            continue
        data = load_json(fpath)
        for fig_key, fig_data in data.items():
            subfolder = fig_data.get('subfolder', '')
            if fig_key not in merged:
                merged[fig_key] = {
                    'figure_key': fig_key,
                    'subfolder': subfolder,
                    'native_language': SUBFOLDER_TO_LANG.get(subfolder, 'english'),
                }
            pair = fig_data.get('pair', {})
            merged[fig_key]['prompt_reverse'] = {
                'true_statement': pair.get('true_statement', ''),
                'false_statement': pair.get('false_statement', ''),
                'fact_description': pair.get('fact_description', ''),
            }

    # 4. Caption bias
    cb_dir = os.path.join(BENCHMARKS, 'adversarial', 'caption_bias')
    for fname in LANG_FILES:
        fpath = os.path.join(cb_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [skip] {fpath}")
            continue
        data = load_json(fpath)
        for fig_key, fig_data in data.items():
            subfolder = fig_data.get('subfolder', '')
            if fig_key not in merged:
                merged[fig_key] = {
                    'figure_key': fig_key,
                    'subfolder': subfolder,
                    'native_language': SUBFOLDER_TO_LANG.get(subfolder, 'english'),
                }
            merged[fig_key]['caption_bias'] = {
                'original_caption': fig_data.get('original_caption', ''),
                'modified_caption': fig_data.get('modified_caption', ''),
                'modifications': fig_data.get('modifications', []),
            }

    print(f"Merged {len(merged)} figures")

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"Written to {OUTPUT}")

    # Upload to Azure Blob Storage
    print("Uploading to Azure Blob Storage...")
    result = subprocess.run(
        [
            'az', 'storage', 'blob', 'upload',
            '--account-name', 'scifigfigures',
            '--container-name', 'data',
            '--name', 'all_benchmarks.json',
            '--file', OUTPUT,
            '--overwrite',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("Upload successful")
    else:
        print(f"Upload failed: {result.stderr}")
        sys.exit(1)


if __name__ == '__main__':
    main()
