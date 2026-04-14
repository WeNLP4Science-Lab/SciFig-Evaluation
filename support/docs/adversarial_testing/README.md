# Adversarial Testing Strategies

## Overview

Deliberately challenging scenarios designed to expose model weaknesses, biases, and failure modes. These go beyond standard evaluation — they test what happens when inputs are degraded, misleading, or designed to trigger fabrication.

See also: [Capability Benchmarks](../capability_benchmarks/README.md) for non-adversarial performance measurement.

---

## A1. Hallucination Probing
**Doc:** [hallucination_probing.md](hallucination_probing.md)

Ask about things that are absent, incorrect, or irrelevant to test if the model fabricates information. Framework adapted from ChartHal (arXiv:2509.17481).

| Category | Status | Key Finding |
|----------|--------|-------------|
| Inexist (absent elements) | ✅ Done | GPT-5.2: 48% hallucination. Qwen-235b: 7% |
| Contra (wrong premise) | ⬜ Planned | Does model correct false statements or accept them? |
| Irrel (unrelated questions) | ⬜ Planned | Can model say "chart doesn't show this"? |
| Normal (control) | ⬜ Planned | Baseline correct answers |

## A2. Caption & Context Bias
**Doc:** [caption_context_bias.md](caption_context_bias.md)

Tests whether models rely on text context instead of reading figures.

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Caption ablation | ✅ Done | Image-only (82.3) > image+caption (78.6) |
| Caption mismatch | ✅ Done | GPT-5.2 mostly ignores wrong captions |
| No-image baseline | ✅ Done | Model scores 78.0 without image (refusals/fabrications) |

## A3. Visual Degradation & Text Removal
**Doc:** [visual_degradation.md](visual_degradation.md)

Tests robustness to image quality changes and text obfuscation.

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Image transforms (5 types) | ✅ Done | GPT-5.2 resilient. Gemma: grayscale devastating |
| Axis blur | ✅ Done | Honesty: GPT-5.2 67%, all others 0-11% |
| Single-label blur | ✅ Done | GPT-5.2 infers from pattern (not memorizing) |
| Legend/title blur | ✅ Done | GPT-5.2 genuinely reads — doesn't fabricate |

## A4. Figure-Blurred Page & Misplaced Figure

Included in [visual_degradation.md](visual_degradation.md) (sections 5 and 6).

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Figure-blurred page | ✅ Done | Only GPT-5.2 admits "obscured". Gemma describes table as chart. |
| Misplaced figure (wrong page) | ✅ Done | Only Gemma gets influenced by surrounding text. |

**Note:** In-paper page context (correct page, no manipulation) is a capability benchmark, not adversarial. See [../capability_benchmarks/in_paper_context.md](../capability_benchmarks/in_paper_context.md).

---

## A4. Prompt Reverse Inconsistency
**Doc:** [prompt_reverse.md](prompt_reverse.md)

Ask the model to confirm then deny the same claim about a figure. Tests grounding stability.

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Confirm/deny pairs | ⬜ Planned | Does the model agree with contradictory statements? |

## A5. Admittance × Resistance Probes
**Doc:** [admittance_resistance_probes.md](admittance_resistance_probes.md)

Targeted probes to independently measure and separate admittance and resistance into four quadrants.

| Probe | What it measures | Status |
|-------|-----------------|--------|
| Probe A (admittance-only) | Degraded visual + direct question — does model admit? | ⬜ Planned |
| Probe B (resistance-only) | Clear image + misleading context — does model ignore? | ⬜ Planned |
| Probe C (combined) | Degraded visual + misleading context — which quadrant? | ⬜ Planned |

Goal: Plot each model on a 2D scatter (x=resistance, y=admittance) to visualize model behaviors.

## A6. Misleading Chart Detection
**Doc:** [misleading_detection.md](misleading_detection.md)

Ask "Is anything misleading about this chart?" on normal, correct charts. Tests if models invent fake problems.

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Normal charts — misleading detection | ⬜ Planned | Literature: all models max at 30% on CALVI |

---

## Cross-Model Findings

| Finding | Evidence |
|---------|----------|
| **Model family > model size** | Qwen-8b (14% hallu) beats Gemma-27b (81%) |
| **GPT-5.2 hallucinates more than expected** | 48% on absent elements — worse than Qwen and LLaMA |
| **Only frontier models admit uncertainty** | GPT-5.2 says "not visible". All others fabricate. |
| **Gemma is consistently worst** | 81-85% hallucination, mixes page text, fabricates axes |
| **Captions hurt more than help** | Image-only outperforms image+caption by 3.7 points |
| **IEMOCAP "5 slices" bias** | Multiple models say 5 instead of 6 — training data override |

## References
- ChartHal (arXiv:2509.17481) — Hallucination probing framework
- See or Recall (arXiv:2504.09809) — Caption/memory bias testing
- Co-Attack (ACM MM 2022) — Gradient-based attacks (cited, not used)
- Paredes La Torre (arXiv:2603.16960) — CLIP spectral attack (cited, not used)
- Ren et al. (s44230-026-00141-w) — VLM vulnerability taxonomy (cited, not used)
