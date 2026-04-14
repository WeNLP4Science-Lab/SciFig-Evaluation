# Causes of poor VLM / MLLM performance on charts & figures

This note synthesizes **how prior work attributes failures** (what goes wrong and *why*, at the level each paper argues). It is a companion to `mustread.md` (curated list + intersections) and `references.md` (URLs).

**Important caveat:** Most claims are **behavioral** (ablations, taxonomies, error rates) or **light mechanistic** (probes on a few models). Few papers establish **neural-level causality** across all VLMs. When writing SciFig-Evaluation, match the strength of your evidence to your wording (“consistent with”, “suggests”, “we hypothesize”).

---

## 1. How to read “causes” in this literature

| Evidence style | What it supports | Examples |
|----------------|------------------|----------|
| **Ablations** (remove image, strip context, oracle inputs) | Which **information pathway** drives answers | See or Recall; FUGU (oracle coordinates) |
| **Taxonomies / error typing** | **Surface forms** of failure (hallucination type, misleader type) | ChartHal; Misviz; CHOCOLATE |
| **Controlled stress** (noise, blur, occlusion) | **When** performance breaks; sometimes **which perturbation class** | CHAOS; CHART NOISe; DIQ-H |
| **Probing / patching / latent readout** | **Where** in the stack signal is lost or distorted | FUGU |
| **Task decomposition** (reasoning type, encoding channel) | **Which subskills** fail | ChartMuseum; EncQA; CharXiv (desc vs reasoning) |
| **Consistency tests** | **Process reliability**, not single-shot accuracy | PRIN; CHART NOISe (prompt-reverse) |

---

## 2. Cause families (with papers and claims)

### 2.1 Vision–language **fusion / hand-off** loss

**Core idea:** The **vision encoder** may contain usable information about the chart, but the **answer path** (often the language model conditioned on visual tokens) **fails to use or preserve** fine-grained values (e.g. coordinates, small marks).

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **FUGU** ([arXiv:2510.21740](https://arxiv.org/abs/2510.21740)) | Many errors arise at **vision → language transfer**, not because the vision tower has *no* usable signal. **Correct coordinates can be read from vision latents** while final answers are wrong. Supplying **oracle coordinates** helps **few-point** tasks. | **Probing / patching** on three VLMs; controlled scatter-plot tasks. |
| **FUGU** (second claim) | **Many-point / aggregate statistics** tasks: oracle coordinates can **hurt**; bottleneck differs from single-point readout. | Same suite; suggests **aggregation / reasoning over many marks** as an additional limit. |
| **FUGU** (third claim) | **Fine-tuning** on the suite **does not** reach ceiling → residual **architectural** limits for reliable visualization QA. | Training experiment. |

**SciFig hook:** Pairs with **selective blur**, **MQM deltas under degradation**, and **admittance** (“fabricates values vs admits unreadable”) without requiring you to run linear probes unless you choose to.

---

### 2.2 **Text shortcuts**, **parametric recall**, and **weak relational grounding**

**Core idea:** Models answer from **question text, options, titles, or world knowledge**, not from reading the plot—so multimodal benchmarks **overcredit** “understanding.”

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **See or Recall** ([arXiv:2504.09809](https://arxiv.org/abs/2504.09809)) | Substantial **correct** answers **without the image**; **context** in the question triggers **recall**; **MC option structure** can support answers with **almost no task content** (“inner bias”). | **2×2 ablations**: see / no-see × recall / no-recall; VLATforge **non-factual** counterfactuals; 30-run stability. |
| **ARO** ([arXiv:2210.01936](https://arxiv.org/abs/2210.01936)) | VLMs often behave like **bags of words**, underusing **order and relational** structure in images. | Relational vs attribute probes on VLMs (broader than charts, but cited for **shortcut** narrative). |
| **ChartMuseum** ([arXiv:2505.13444](https://arxiv.org/abs/2505.13444)) | Large drops on **visual-primary** vs **text-primary** questions at similar aggregate difficulty → models lean on **textual** chart content when they can. | **Reasoning-type labels** + accuracy breakdowns + qualitative errors. |

**SciFig hook:** **Caption-only vs image+caption vs wrong-caption** and **no-image description** baselines align directly with this family.

---

### 2.3 **OCR**, **script**, **language**, and **tokenization**

**Core idea:** Chart text is **small, dense, non-Latin, or translated**; reading the figure is **harder than answering English MCQ** on simplified charts.

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **PolyChartQA** ([arXiv:2507.11939](https://arxiv.org/abs/2507.11939)) | Large **English vs other-language** gaps; error analysis highlights **OCR** and **language bias**; instruction tuning **reduces** gap. | Multilingual re-rendered charts + per-language / cross-lingual tables + sampled human QA on subset. |

**SciFig hook:** Your **four languages** and **MQM** across languages test overlapping **reading** stress; cite PolyChartQA for **chart QA** multilingual evidence, not identical task.

---

### 2.4 **Reasoning depth**, **compositionality**, and **multi-source integration**

**Core idea:** Models can pass **shallow** or **single-hop** questions but fail **multi-step reasoning**, **cross-element** synthesis, or **multi-chart** integration.

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **CharXiv** ([arXiv:2406.18521](https://arxiv.org/abs/2406.18521)) | **Reasoning** questions on real arXiv charts are **much harder** than **descriptive** ones; **stress tests** show **large drops** vs easy chart benchmarks. | Human-curated Q; descriptive vs reasoning splits; stress variants. |
| **PlotQA** ([arXiv:1909.00997](https://arxiv.org/abs/1909.00997)) | **Reasoning / data** questions much harder than **structural** items on scientific-style plots. | Accuracy by question category (classic result). |
| **MultiChartQA** ([arXiv:2410.14179](https://arxiv.org/abs/2410.14179)) | Single-chart benchmarks miss failures requiring **multiple charts** and **composed** reasoning. | Multi-chart benchmark design + model–human gaps. |

**SciFig hook:** Your **capability suite** (computation, counting, cross-panel, open-ended reasoning) maps here.

---

### 2.5 **Hallucination**, **overconfident language**, and **unanswerable items**

**Core idea:** The **language decoder** produces **fluent, specific, wrong** content; models **answer** when they should **abstain**.

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **ChartHal** ([arXiv:2509.17481](https://arxiv.org/abs/2509.17481)) | Hallucination on chart QA is **severe** and **structured** by **scenario type** (e.g. irrelevant, non-existent, contradictory). | Taxonomy + human-validated items + binary scoring. |
| **CHOCOLATE** ([arXiv:2312.10160](https://arxiv.org/abs/2312.10160)) | Chart **captioning** shows **systematic factual errors** analyzable by type. | Error analysis + correction-oriented discussion (LVLM caption setting). |
| **HallusionBench** ([arXiv:2310.14566](https://arxiv.org/abs/2310.14566)) | “Hallucination” **entangles** **vision mistakes** and **language-side** over-generation; needs **disentangled** diagnostics. | Diagnostic suite design. |
| **ChartQAPro** ([arXiv:2504.05506](https://arxiv.org/abs/2504.05506)) | **Diverse** charts + **unanswerable** and conversational QAs **break** saturation on ChartQA. | Benchmark design + model drops + paper discussion. |

**SciFig hook:** **A1 hallucination probes**, **admittance**, **misleading false alarms**; **MQM** for **long-form** faithfulness.

---

### 2.6 **Robustness**, **degradation**, and **inconsistency**

**Core idea:** Under **noise**, **occlusion**, or **reframed prompts**, models **collapse** or **contradict** themselves—even if clean-image accuracy looks good.

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **CHAOS** ([arXiv:2505.17235](https://arxiv.org/abs/2505.17235)) | MLLMs are **systematically sensitive** to **visual and textual** chart perturbations. | Many perturbation types × chart tasks. |
| **CHART NOISe** (“Losing the Plot”) ([arXiv:2509.18425](https://arxiv.org/abs/2509.18425)) | **Corruption + occlusion** + hard MC; **prompt-reverse** reveals **inconsistency**. | Benchmark + SOTA model evaluation. |
| **DIQ-H** ([arXiv:2512.03992](https://arxiv.org/abs/2512.03992)) | **Hallucination** behavior under **image degradation** (persistence / shift). | Degradation-focused study (see paper for exact setup). |
| **PRIN** ([arXiv:2504.01282](https://arxiv.org/abs/2504.01282)) | **Prompt-reverse inconsistency**: conflicting judgments on same candidates under “which are correct?” vs “which are incorrect?” | Defines phenomenon + experiments (general LLM; cited by chart robustness work). |

**SciFig hook:** **A3**, **A4**, **resistance** metrics; tie **MQM drop** to transform type.

---

### 2.7 **Which visual encodings are hard** (channel-level)

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **EncQA** ([arXiv:2508.04650](https://arxiv.org/abs/2508.04650)) | Difficulty is **channel-dependent** (position, length, color, etc.); models are not uniformly strong across encodings. | Channel-structured chart QA benchmark + analysis. |

**SciFig hook:** Use to **motivate** subtypes in descriptive vs reasoning probes (e.g. **length vs angle vs text-dense legend**).

---

### 2.8 **Misleading graphics** and **literacy vs deception**

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **Pandey & Ottley (VLAT + CALVI)** ([arXiv:2503.16632](https://arxiv.org/abs/2503.16632)) | VLMs can score OK on **basic** literacy yet **fail misleading-visualization** items vs humans. | Standardized tests + model comparison. |
| **Misviz** ([arXiv:2508.21675](https://arxiv.org/abs/2508.21675)) | **Typing misleaders** + large benchmark; detection remains hard. | Dataset + baseline analysis. |
| **Perils of Chart Deception** ([arXiv:2508.09716](https://arxiv.org/abs/2508.09716)) | VLMs are **misled** by **specific deceptive design patterns** (taxonomy of tactics). | Taxonomy + behavioral eval. |

**SciFig hook:** **A5** misleading detection + **false alarms** on correct scientific figures.

---

### 2.9 **Evaluation & judgment artifacts** (why *measured* performance misleads)

| Paper | Claim | Evidence / nuance |
|-------|--------|-------------------|
| **Chart-to-Experience** ([arXiv:2505.17374](https://arxiv.org/abs/2505.17374)) | MLLMs are **less sensitive** than humans to subtle chart issues → **human–model sensitivity mismatch** in evaluation. | Human vs model comparison framing. |
| **Chart-to-Text** ([arXiv:2203.06486](https://arxiv.org/abs/2203.06486)) | Early chart summarization: **fluency ≠ faithfulness**; factual and trend errors. | Automatic + human analysis (ACL 2022). |

**SciFig hook:** Justifies **multi-judge MQM**, **human subset**, and **admittance** as first-class—not only accuracy.

---

### 2.10 **Benchmark-centric** papers (gap first; “why” lighter)

These papers **establish difficulty and splits**; their “cause” story is often **implicit** (task is hard, data diverse) rather than a single mechanism.

| Paper | Main contribution relative to “causes” |
|-------|----------------------------------------|
| **SciFIBench** ([arXiv:2405.08807](https://arxiv.org/abs/2405.08807)) | Scientific **figure interpretation** is hard for LLMs on benchmark tasks. |
| **ChartQA** ([arXiv:2203.10244](https://arxiv.org/abs/2203.10244)) | Real chart QA needs **vision + logic**; subset difficulty differs. |
| **CharXiv** | Also provides **stress tests** → partial mechanistic story (§2.4). |

---

## 3. Meta: **MQM** is not a “VLM failure cause”

**MQM** (Lommel et al., 2014; see translation-QA literature) is a **rubric for describing errors** (types, severity). It does not assert *why* a VLM failed neurally—it helps you **operationalize causes** in **human or judge** protocols. SciFig’s use of MQM-style scoring is **attribution infrastructure**, not a competing biological claim to FUGU.

---

## 4. Master table: paper → attributed causes → evidence type

| Paper | Primary attributed cause(s) | Evidence type |
|-------|------------------------------|----------------|
| FUGU | Fusion/hand-off; multi-point aggregation; architectural ceiling | Probing / patching / oracle / finetune |
| See or Recall | Recall from text; MC bias; evaluation overestimates “seeing” | Ablations + counterfactual data |
| ARO | Bag-of-words / weak relational use of vision | Behavioral probes |
| ChartMuseum | Textual vs visual reasoning imbalance | Reasoning-type labels + errors |
| CharXiv | Reasoning harder than description; distribution shift | Splits + stress tests |
| PlotQA | Reasoning ≫ structure | Category accuracies |
| MultiChartQA | Multi-chart composition | Task design + gaps |
| ChartHal | Typed hallucination scenarios | Taxonomy + dataset |
| CHOCOLATE | Caption factual errors | Error analysis |
| HallusionBench | Entangled vision vs language failures | Diagnostic suite |
| ChartQAPro | Saturation hides weakness; unanswerable breaks models | Benchmark + results |
| PolyChartQA | OCR / language bias; English pivot effects | Multilingual eval + error buckets |
| CHAOS | Perturbation-specific fragility | Many corruptions |
| CHART NOISe | Noise + inconsistency under framing | Corruption + prompt-reverse |
| PRIN | Self-inconsistency across prompt polarity | Controlled LLM tests |
| EncQA | Channel-dependent difficulty | Structured QA by channel |
| Pandey & Ottley | Misleading viz harder than basic literacy | Standardized tests |
| Misviz | Misleader categories hard to detect | Typology + benchmark |
| Perils of Chart Deception | Deceptive design misleads VLMs | Taxonomy + eval |
| DIQ-H | Hallucination under degradation | Degradation experiments |
| Chart-to-Experience | Eval sensitivity mismatch | Human vs model framing |
| Chart-to-Text | Fluency vs faithfulness | Human + automatic eval |
| SciFIBench / ChartQA | Task is objectively hard / diverse | Benchmark scores |

---

## 5. Using this file in SciFig-Evaluation writing

1. **One subsection** in related work: “**Hypotheses about failure**” organized by **cause family** (this doc §2), not by paper name dump.  
2. **Methods / analysis**: map your **probes** (caption, blur, reverse, misleading) to **families** so readers see **which prior hypothesis** you test.  
3. **Discussion**: if results align with **hand-off** (FUGU-like), say **behaviorally consistent** with fusion loss unless you ran probes.  
4. Keep **PolyChartQA** and **See or Recall** distinct: **multilingual QA pipeline** vs **VisQA recall on fixed benchmarks**.

---

## 6. Related files

- `support/docs/mustread.md` — curated papers + SciFig intersection blurbs  
- `support/docs/references.md` — compact link list  
- `support/docs/research.md` — broader survey  
- `support/docs/contributions.md` — SciFig claims (F1–F5, A1–A5, admittance/resistance)

When adding new papers to this repo, append a row to **§4** and a short bullet under the best **§2** family.
