# SciFig-Eval Master Writing Guide

Every writing agent MUST follow this guide. Read it completely before writing.

---

## Core Framing

The paper evaluates VLMs across three dimensions of increasing demand:

1. **Perception** — can the model see and describe a scientific figure? (baseline MQM, transforms)
2. **Reasoning** — can the model think about what it sees? (capability questions, inductance inference)
3. **Behaviour** — how does the model act under uncertainty and deception? (A-R-I framework)

The central finding is that models performing equally on perception and reasoning diverge sharply on behaviour. The highest-scoring model on description quality fabricates answers 94% of the time when it cannot see.

**Behaviour under challenge** encompasses two types:
- **Uncertainty** — the model cannot fully see (blur, degradation). Tests admittance and inductance.
- **Deception** — the model receives false information (caption bias, resistance probes). Tests resistance.

The A-R-I framework organises the behavioural dimensions:
- **Admittance** = behaviour under uncertainty (does the model acknowledge what it cannot see?)
- **Resistance** = behaviour under deception (does the model push back on false premises and misleading captions?)
- **Inductance** = reasoning under uncertainty (can the model infer missing information from context?)

---

## Writing Voice

### The Standard
Every sentence must tell the reader something new, change how they think, or move them forward. If it does none of these, delete it.

### Tone
Precise, vivid, confident. Not arrogant, not hedging. Academic rigour with readable prose. The reader should feel the author has thought deeply, not just run experiments.

### Punchline Technique
Lead with the finding. Deliver the number. Then explain what it means.

**Bad:** "We observe that GPT-5.2 achieves a high MQM score of 91.6 but has a low admittance rate of 6%, which suggests that quality and behavioural reliability may be distinct."

**Good:** "GPT-5.2 produces the highest-quality descriptions in our evaluation (MQM 91.6) yet fabricates answers for elements it cannot see 94% of the time, with nothing in its output to distinguish the fabrication from genuine analysis."

### Number Embedding
Numbers should land, not float. Always contextualise.

**Bad:** "Gemini achieves an admittance rate of 90%."

**Good:** "Gemini acknowledges visual uncertainty in 90% of cases. No other model exceeds 22%."

The second number (22%) makes the first meaningful. Comparison is context.

### Contrast Technique
The paper's power comes from contrasts. Use them:

**Bad:** "GPT-5.2 has high quality. Gemini has high admittance."

**Good:** "GPT-5.2 and Gemini score within 1.4 MQM points of each other on description quality, yet their admittance rates differ by 84 percentage points."

### Sentence Length
Mix short and long. Short sentences deliver punchlines. Long sentences build context. Never three long sentences in a row.

---

## Banned Phrases (use alternatives)

| Banned | Use Instead |
|---|---|
| It is worth noting that | [delete, just state it] |
| Interestingly, ... | [delete the word, the finding speaks for itself] |
| As can be seen from Table X | [lead with finding, cite table parenthetically] |
| We can observe that | [state the observation directly] |
| It should be noted | [delete] |
| In order to | to |
| A large number of | many / [specific number] |
| Due to the fact that | because |
| In the context of | in / for |
| Prior to | before |
| At the present time | now / currently |
| It is important to | [delete, just say it] |
| We believe that | [state it as finding with evidence] |
| To the best of our knowledge | [verify, then state directly] |
| State-of-the-art | [specify which task/metric] |
| Significantly | [only with a statistical test, otherwise use "substantially"] |
| Relatively | [compared to what? be specific] |
| Arguably | [don't argue, show evidence] |
| --- (emdash) | [rewrite as two sentences or use comma/parentheses] |
| : (colon before explanation) | [rewrite as flowing sentence] |

---

## Terminology (strict consistency)

| Concept | Use This | NOT This |
|---|---|---|
| Our benchmark | \textsc{SciFig-Eval} | SciFig, SciFig-Evaluation, the benchmark |
| Three dimensions | perception, reasoning, behaviour | quality, reliability, competence |
| Evaluation metric | MQM score | quality score, description score |
| Chart types | bar chart, line plot, pie chart | bar graph, line chart, pie graph |
| Image degradation | transform | perturbation, corruption, augmentation |
| Poisoned caption | modified caption | fake caption, wrong caption |
| Model honesty | admittance | honesty, transparency |
| Pushing back on lies | resistance | robustness (reserve for transforms) |
| Inferring from context | inductance | inference (too generic) |
| The framework | A-R-I framework | ARI, A.R.I. |
| Hallucination probes | resistance probes | hallucination tests |
| Model gives answer despite blur | fabrication | hallucination, guessing |
| Model acknowledges blur | admission | acknowledgment |
| Types of challenge | uncertainty and deception | adversarial (too broad) |

---

## Model Names

| Short Name | Full Name | Type |
|---|---|---|
| GPT-5.2 | GPT-5.2 (Azure) | Commercial, closed |
| Gemini | Gemini 3.1 Pro | Commercial, closed |
| Llama 4 | Llama 4 Maverick 17B-128E | Open-weight, MoE |
| Qwen-235B | Qwen3-VL-235B-A22B | Open-weight, MoE (22B active) |
| Qwen-30B | Qwen3-VL-30B-A3B | Open-weight, MoE (3B active) |
| Qwen-8B | Qwen3-VL-8B | Open-weight, dense |
| Gemma | Gemma3-27B-IT | Open-weight, dense |
| Phi-4 | Phi-4-Multimodal | Commercial, small |

---

## Numbers and Statistics

- MQM scores: one decimal (91.6)
- Resistance/bias scores: two decimals (0.89)
- Percentages in text: "89%" not "0.89" (except in formal definitions)
- Bootstrap CIs: subscript/superscript in tables, brackets in text "91.6 [90.4, 92.8]"
- Always include sample size for key claims: "(n=250)" or "across 100 figures"
- Significance: report p-value and effect size together
- No "significantly" without a statistical test

---

## Formatting Rules

- No emdashes (---) anywhere
- No colons before explanations or lists
- \textsc{SciFig-Eval} for benchmark name
- \emph{} only for first use of a technical term
- Bold best result in tables, underline second best
- Use ~ (non-breaking space) before \ref and \cite
- Cross-reference: \S\ref{sec:label}, Table~\ref{tab:label}, Figure~\ref{fig:label}
- Contributions as \begin{enumerate} list

---

## Section Length Targets (8 pages)

| Section | Pages | Words |
|---|---|---|
| Introduction | 1.25 | ~750 |
| Related Work | 0.75 | ~450 |
| Framework (inc. Dataset) | 2.0 | ~1200 |
| Results | 2.5 | ~1500 |
| Analysis | 0.75 | ~450 |
| Conclusion | 0.5 | ~300 |
| Limitations + Ethics | 0.25 | ~150 |
| **Total** | **8.0** | **~4800** |

---

## Anti-Pattern Checklist

Before submitting any paragraph, check:
1. Does the first sentence state a finding or claim (not setup)?
2. Is every number contextualised (compared to something)?
3. Are there three long sentences in a row? (break one up)
4. Does every table reference include analysis (not just "see Table X")?
5. Are there any banned phrases?
6. Any emdashes or colons before explanations?
7. Is terminology consistent with this guide?
8. Does the paragraph tell the reader something new?
