# Comment / TODO Fixes — Resubmission

Inventory of all `\todo{}` notes, hidden `%\todo{}` markers, `\am{}` edit markers, and commented-out text blocks in the paper source. Grouped by fix approach so each group can be tackled on its own branch.

Source: `resubmission/6a143a4c382eafd7ee52e0c7/sections/*.tex` and `main.tex`.

---

## Group A — Quick clarifications and one-line fixes

Small textual/terminological fixes. Each resolvable by a one-sentence rewrite or missing reference/definition. Estimated effort: <30 min total.

### A1. `sections/analysis.tex:7` — Fig. 4 never referenced
```
\todo{SE: Fig. 4 never referenced? - PAUL}
```
Steffen flags that Figure 4 is defined but never `\ref`'d anywhere. Either (a) add a `\ref{fig:...}` in the appropriate paragraph, or (b) remove Figure 4 if it's redundant.

### A2. `sections/results.tex:52` — What does "R" stand for?
```
Models fall along a caption dependency spectrum from visual independence to textual dependency (Table~\ref{tab:behavioral}, Cap.\ Bias~R - PAUL). 
\todo{SE: what does R stand for? [PAUL]} 
```
`R` = **Resistance** score (0–1 scale). Just clarify inline or in the caption of Table 4.

### A3. `sections/results.tex:65` — Symbol clarification
```
Caption bias resistance is unchanged at 0.89, while hallucination resistance differs only modestly (0.80 vs.\ 0.86, $\delta = -0.16$). 
\todo{SE: do you mean $\Delta$? Difference to what? - PAUL}
```
Was Cliff's $\delta$ effect size, not $\Delta$. Clarify what `-0.16` is a delta of (probably `\delta = 0.06` if it's the raw difference 0.86 − 0.80, or Cliff's δ effect size — needs verification).

---

## Group B — Content additions / restructures

These need actual new writing (paragraphs, examples, or reframing). Higher effort — likely need discussion before drafting.

### B1. `sections/analysis.tex:16` — Where does "caption" come from?
```
Instead, caption dependency appears tied to instruction tuning that encourages models to trust provided context over visual evidence. 
\todo{SE: I don't understand this. Where does caption come from? I thought you have figures with understanding questions? - NEEDS DISCUSSION}
```
Steffen doesn't understand the caption probe design. Need to add a sentence linking back to §3.2 (behavioural probes / caption-bias) so readers understand the caption is a modified probe input, not part of the question.

### B2. `sections/conclusion.tex:13` — Add examples, clarify setup
```
\todo{SE: I like the paper, but more examples would be helpful. It's often very dense, and some parts of the setup could be better illustrated, e.g., are there questions with answer choices? And models must choose the correct ones under blur, etc.? Also, I didn't understand what caption means here... PAUL}
```
Steffen's broader "add examples" concern. Overlaps with reviewer feedback that the setup is dense. Likely requires: (a) a compact example box in Section 3 showing an admittance probe + expected behaviour, (b) same caption-clarification as B1.

### B3. `sections/results.tex:38` — More examples + human construction details
```
\todo{SE: At some point we need more examples (of all these different cases --- full examples ideally). And also more details on human construction - PAUL}
```
Steffen wants more example probes (of admittance / resistance / inductance) and more detail on the human annotation pipeline. **Human annotation pipeline is a P1 rebuttal commitment already** (5 annotators / 600+ hours) — this can be addressed in the same paragraph.

---

## Group C — Cleanup (source hygiene, no content change)

Non-content clutter. Safe to do in a single pass.

### C1. Remove 4 hidden `%\todo{}` markers
- `sections/framework.tex` — 2 hidden TODOs
- `sections/introduction.tex` — 1 hidden TODO
- `sections/related_work.tex` — 1 hidden TODO (inline, mid-sentence — likely commented-out edit)

### C2. Remove ~65 commented-out old-version paragraphs

Files with `%`-prefixed old text kept as history:
| File | Approx count |
|---|---|
| `sections/abstract.tex` | 5 |
| `sections/conclusion.tex` | 11 |
| `sections/framework.tex` | 12 |
| `sections/introduction.tex` | 11 |
| `sections/related_work.tex` | 5 |
| `sections/evaluation_appendix.tex` | 8 |
| `main.tex` | 5 |
| Other files | 2–3 each |

These are old paragraph drafts that were replaced but not deleted. Not visible in the PDF but clutter the source.

### C3. Remove `todonotes` package once Group A + B are resolved

`main.tex:39`:
```
\usepackage[colorinlistoftodos,prependcaption,textsize=tiny]{todonotes}
```
After all `\todo{}` calls in Groups A + B are gone, this package (and any `\listoftodos` calls) can be removed. Reduces preamble load and any `\todo{...}` accidentally left in a `.tex` will fail-compile so we notice.

---

## Group D — `\am{}` marker audit (need macro definition check)

Ananya added text using `\am{...}` markers in 15 places. Before doing anything with these, need to check `main.tex` for the definition of `\am`:

- If `\am` is defined as `\newcommand{\am}[1]{#1}` (i.e., transparent — just displays the text) → nothing to do, they're integrated normal text
- If `\am` is defined as a colour/highlight or diff-review macro → decide whether to keep highlighted or "accept" by unwrapping

Locations:
- `sections/analysis.tex`: 8 uses
- `sections/conclusion.tex`: 3 uses
- `sections/framework.tex`: 2 uses
- `sections/dataset.tex`: 1 use
- `sections/introduction.tex`: 1 use
- `sections/related_work.tex`: 1 use

---

## Suggested execution order

| Order | Group | Branch name | Effort |
|---|---|---|---|
| 1 | **A — Quick clarifications** | `p1-comments-quick-clarifications` | Low, ~30 min |
| 2 | **D — `\am{}` audit** | `p1-comments-am-marker-audit` | Low — just inspect definition |
| 3 | **C — Cleanup** | `p1-comments-source-cleanup` | Medium, mechanical |
| 4 | **B — Content additions** | `p1-comments-content-additions` | High, needs discussion |

Do the low-risk ones first so the source is clean by the time we tackle the higher-effort B group.
