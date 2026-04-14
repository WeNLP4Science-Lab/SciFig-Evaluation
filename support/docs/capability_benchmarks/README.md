# Capability Benchmarks

## Overview

Measuring legitimate figure understanding performance at varying difficulty levels. These are not adversarial — they test what models can genuinely do when given clear, undegraded inputs.

See also: [Adversarial Testing](../adversarial_testing/README.md) for deliberate manipulation experiments.

---

## B1. Descriptive (Reading)
**Doc:** [descriptive.md](descriptive.md)

Can the model accurately read and extract information directly visible in the figure?

| Subtype | Status | GPT-5.2 |
|---------|--------|---------|
| D1. Numerical value reading | ✅ Done | 100% |
| D2. Chart element identification (CharXiv templates) | ✅ Done | 78% |
| D3. Other subtypes | ⬜ Planned | — |

## B2. Reasoning (Thinking)
**Doc:** [reasoning.md](reasoning.md)

Can the model think about chart data — compute, compare, count, infer?

| Subtype | Status | GPT-5.2 |
|---------|--------|---------|
| R1. Numerical computation (medium/hard) | ✅ Done | 78% |
| R2. Visual counting (single + cross-panel) | ✅ Done | 44-61% |
| R3. Open-ended reasoning | ✅ Done | 89% |
| R4. Cross-panel reasoning | ✅ Done | 89-94% |
| R5. Other subtypes | ⬜ Planned | — |

## B3. In-Paper Page Context
**Doc:** [in_paper_context.md](in_paper_context.md)

Can the model describe a figure on a real paper page with surrounding text/tables?

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| Clean vs in-paper (GPT-5.2) | ✅ Done | Minimal drop |
| Multi-model (7 models) | ✅ Done | Gemma fails, others handle well |

---

## GPT-5.2 Difficulty Ladder

```
DESCRIPTIVE:
  Value reading (labeled):         100%  █████████████████████████
  Chart element ID (CharXiv):       78%  ████████████████████

REASONING:
  Open-ended reasoning:             89%  ██████████████████████
  Cross-panel open reasoning:     89-94% ██████████████████████
  Numerical computation:            78%  ████████████████████
  Cross-panel counting:             61%  ███████████████
  Single-panel counting:            44%  ███████████
```

**Key insight:** The model's weakness is not reasoning itself (89%) but **precise visual counting** (44%). The bottleneck is extracting and enumerating visual elements, not thinking about them.
