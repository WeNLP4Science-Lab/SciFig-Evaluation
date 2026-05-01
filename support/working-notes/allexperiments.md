# All Experiments

## Overview

45 adversarial figures × 12 generator models × 5 experiment types.

**Generator Models (12):**
| # | Model | Backend | Size |
|---|-------|---------|------|
| 1 | gpt-5.2 | Azure | Frontier |
| 2 | phi-4-multimodal | Azure | 14B |
| 3 | gemini-3.1-pro | OpenRouter | Frontier |
| 4 | gemma3-4b-it | OpenRouter | 4B |
| 5 | gemma3-12b-it | OpenRouter | 12B |
| 6 | gemma3-27b-it | OpenRouter | 27B |
| 7 | qwen3-vl-8b | OpenRouter | 8B |
| 8 | qwen3-vl-30b-a3b | OpenRouter | 30B (3B active) |
| 9 | qwen3-vl-32b | OpenRouter | 32B |
| 10 | qwen3-vl-235b-a22b | OpenRouter | 235B (22B active) |
| 11 | llama4-scout | OpenRouter | 17B×16E |
| 12 | llama4-maverick | OpenRouter | 17B×128E |

**Judge Models (for evaluation):**
| # | Model | Backend |
|---|-------|---------|
| 1 | gpt-4o | Azure |
| 2 | gpt-5.4-mini | Azure |

---

## Experiment 1: Questions (Prompt 1)

**Script:** `scripts/experiments/run_questions.py --prompt 1`
**Output:** `output/experiments/questions/{model}/{subfolder}/{fig_key}.json`
**Calls:** 12 models × 45 figures = **540 calls**

Sends 5 questions per figure with the original image:

| # | Question Type | Source | What it tests |
|---|---|---|---|
| 1 | Capability Q1 | `benchmarks/capability/native/{lang}.json` | Hard value reading, comparison, computation |
| 2 | Capability Q2 | same | Hard counting, trend analysis |
| 3 | Capability Q3 | same | Hard cross-series comparison |
| 4 | Hallucination — Inexist | `benchmarks/adversarial/hallucination/native/{lang}.json` | Does model describe a non-existent chart element? |
| 5 | Prompt Reverse — TRUE | `benchmarks/adversarial/prompt_reverse/native/{lang}.json` | Does model confirm a true visual fact? |

**Metrics derived:** Capability accuracy, Admittance (inexist), Resistance (prompt reverse consistency)

---

## Experiment 2: Questions (Prompt 2)

**Script:** `scripts/experiments/run_questions.py --prompt 2`
**Output:** appends to same file as Prompt 1
**Calls:** 12 models × 45 figures = **540 calls**

Sends 5 questions per figure with the original image:

| # | Question Type | Source | What it tests |
|---|---|---|---|
| 1 | Capability Q4 | `benchmarks/capability/native/{lang}.json` | Hard computation, trend analysis |
| 2 | Capability Q5 | same | Hard comparison, value reading |
| 3 | Hallucination — Contra | `benchmarks/adversarial/hallucination/native/{lang}.json` | Does model accept a false premise or correct it? |
| 4 | Hallucination — Unanswerable | same | Does model admit chart can't answer, or fabricate? |
| 5 | Prompt Reverse — FALSE | `benchmarks/adversarial/prompt_reverse/native/{lang}.json` | Does model reject a false visual fact? |

**Metrics derived:** Capability accuracy, Resistance (contra + prompt reverse), Admittance (unanswerable)

---

## Experiment 3: Transform Descriptions (Image Only)

**Script:** `scripts/experiments/run_transforms.py`
**Output:** `output/experiments/transforms/{model}/{transform}/{subfolder}/{fig_key}.json`
**Calls:** 12 models × 10 conditions × 45 figures = **5,400 calls**

Sends each image with the standard description prompt but **NO caption and NO paper title** — pure visual understanding. Model produces a free-form description from the image alone.

| # | Condition | Image Used | What it tests |
|---|---|---|---|
| 1 | original | `original.png` (clean) | Baseline visual description (no caption) |
| 2 | jpeg_compression | Heavy JPEG artifacts (quality=15) | Robustness to compression |
| 3 | noise | Gaussian noise (sigma=30) | Robustness to visual noise |
| 4 | grayscale | Removes all color information | Color dependency |
| 5 | aspect_ratio | Horizontal stretch (1.2x) | Geometric distortion robustness |
| 6 | low_contrast | Contrast reduced by 50% | Robustness to faded images |
| 7 | rotation | 30-degree rotation | Orientation robustness |
| 8 | axis_blurred | Bottom 15%, left 15%, top 12% blurred | Text reading honesty (Admittance) |
| 9 | selective_blur | Single in-chart element blurred | Element-level honesty + inference (Admittance + Inductance) |
| 10 | blurred_in_paper | Figure region blurred on paper page | Context reliance when figure is unreadable |

**All conditions are image-only** (no caption, no paper title) so that:
- Transform degradation is measured purely against visual reading ability
- Caption can't help the model "cheat" on degraded images
- Admittance is cleanly measured (model can't infer from caption what blurred text says)
- The `original` condition serves as the image-only baseline

**Metrics derived:** MQM quality degradation per transform, Admittance (axis_blurred, selective_blur, blurred_in_paper), Inductance (selective_blur on inferable elements)

**Comparisons:**
- `original` (this experiment) vs `output/generation/{model}/` (baseline with caption) → measures caption dependency
- `original` vs each transform → measures degradation impact
- Across models per transform → identifies which models are most/least robust

---

## Experiment 4: Caption Bias — Modified Caption

**Script:** `scripts/experiments/run_caption_bias.py --condition modified_caption`
**Output:** `output/experiments/caption_bias/modified_caption/{model}/{subfolder}/{fig_key}.json`
**Calls:** 12 models × 45 figures = **540 calls**

Sends original image + subtly poisoned caption (70% correct, 30% false). The modified captions use psychology-informed strategies:
- Anchoring with plausible wrong numbers (20-40% off actual)
- Peripheral misinformation (poison secondary details, keep main trend correct)
- Loaded verbs and trend mischaracterization
- Domain-appropriate framing

**Source:** `benchmarks/adversarial/caption_bias/{lang}.json`

**Metrics derived:** Resistance (does model follow image or caption?). Compare description claims against:
- Ground truth (from original image) — visual-evidence-aligned claims
- Modified caption errors — caption-influenced claims
- R = visual-aligned / (visual-aligned + caption-influenced)

---

## ~~Experiment 5: Caption Bias — Image Only~~ (Merged into Experiment 3)

The image-only baseline is now the `original` condition in Experiment 3 (Transform Descriptions). No separate run needed — the `original` transform sends the clean image with no caption, producing the same output.

**Comparisons enabled:**
- `transforms/original/` vs `generation/` (baseline with caption) → caption dependency
- `transforms/original/` vs `caption_bias/modified_caption/` → caption influence magnitude

---

## Call Summary

| Experiment | Per Model | × 12 Models | Status |
|---|---|---|---|
| Questions Prompt 1 | 45 | 540 | GPT-5.2, Qwen-235B, Gemini done |
| Questions Prompt 2 | 45 | 540 | GPT-5.2, Qwen-235B, Gemini done |
| Transform descriptions (10 conditions) | 450 | 5,400 | Not started |
| Caption bias (modified caption) | 45 | 540 | Not started |
| **Total** | **585** | **7,020** | |

---

## Evaluation Pipeline

After generation, responses are scored:

| Evaluation | Script | Judge | What it scores |
|---|---|---|---|
| Hallucination probes | `scripts/experiments/evaluate_hallucination.py` | gpt-4o | inexist/contra/unanswerable scores (0, 0.5, 1.0) |
| Transform descriptions | MQM evaluator (existing) | gpt-4o / gemini-2.5-pro | Quality degradation per transform |
| Caption bias | TBD | gpt-4o | Claims matching image vs. caption |
| Capability questions | TBD | gpt-4o or rule-based | Answer correctness |
| Prompt reverse | Rule-based | N/A | yes/no consistency across true/false pairs |

---

## Derived Metrics (from all experiments)

| Metric | Definition | Source Experiments |
|---|---|---|
| **Admittance (A)** | Does model acknowledge when it can't see/read something? | Axis blur, selective blur, blurred_in_paper, inexist probes, unanswerable probes |
| **Resistance (R)** | Does model stay faithful to image when given misleading context? | Caption bias (modified), contra probes, prompt reverse pairs |
| **Inductance (L)** | Does model correctly infer missing info from visual context? | Selective blur (inferable), axis blur (patterned scales), in-paper context |

---

## Output Structure

```
output/experiments/
├── questions/{model}/{subfolder}/{fig_key}.json
│   └── Contains both prompt1 and prompt2 responses with parsed answers
├── transforms/{model}/{transform}/{subfolder}/{fig_key}.json
│   └── Free-form description of transformed image
├── caption_bias/
│   ├── modified_caption/{model}/{subfolder}/{fig_key}.json
│   └── image_only/{model}/{subfolder}/{fig_key}.json
└── evaluation/
    └── hallucination/{judge}/{model}/{subfolder}/{fig_key}.json
        └── Judge scores per probe (0, 0.5, 1.0) with reasoning
```

---

## Benchmark Data Sources

```
adversarial_experiments/benchmarks/
├── capability/                          # 225 questions (5 per figure)
│   ├── native/{bulgarian,chinese,english,german,multi_language}.json
│   └── english/{same files — translations}
├── adversarial/
│   ├── hallucination/                   # 135 probes (3 per figure: inexist + contra + unanswerable)
│   │   ├── native/{5 language files}
│   │   └── english/{5 language files}
│   ├── caption_bias/                    # 45 modified captions (1 per figure)
│   │   └── {bulgarian,chinese,english,german,multi_language}.json
│   └── prompt_reverse/                  # 45 confirm/deny pairs (1 pair per figure)
│       ├── native/{5 language files}
│       └── english/{5 language files}
└── references.md                        # 77 cross-disciplinary references
```
