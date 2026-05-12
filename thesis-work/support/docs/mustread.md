# Must-read: close papers for SciFig-Evaluation

Curated papers that most directly overlap with this project: **multilingual scientific figures**, **open-ended description vs QA**, **hallucination and calibration**, **caption/context vs vision**, **robustness**, **misleading charts**, and **evaluation design**. Each entry has a short summary, a **key finding**, and how it **intersects** with `contributions.md`.

For a broader survey, see `research.md`. For a compact bibliography list, see `references.md`. For **synthesized “why” claims** (failure causes, evidence types, master table), see `cause.md`.

---

## Benchmarks and tasks (real charts, scientific figures, QA)

### CharXiv — Wang et al., NeurIPS 2024 (Datasets & Benchmarks)

- **Link:** https://arxiv.org/abs/2406.18521 · **Project:** https://charxiv.github.io/ · **Code:** https://github.com/princeton-nlp/CharXiv  
- **Summary:** ~2.3k **real** charts from arXiv with expert **descriptive** vs **reasoning** questions; shows a large gap between model and human performance, especially on reasoning; includes stress tests where easy benchmarks overstate competence.  
- **Key finding:** Reasoning on natural paper charts is much harder than descriptive probes; small distribution shifts hurt models a lot.  
- **SciFig intersection:** Same “**real paper charts**” motivation and **desc vs reasoning** split; SciFig pushes **multilingual open-ended description**, **MQM multi-judge**, and **adversarial** layers rather than English-only short-form QA.

### SciFIBench — Roberts et al., NeurIPS 2024

- **Link:** https://arxiv.org/abs/2405.08807 · **Code:** https://github.com/jonathan-roberts1/SciFIBench  
- **Summary:** Benchmarks LLMs on **scientific figure interpretation** (interpretation-style tasks on publication figures).  
- **Key finding:** Scientific figures remain challenging for LLMs even when the task is structured as interpretation/benchmark items.  
- **SciFig intersection:** Closest **“scientific figures”** neighbor; differentiate with **generative description**, **human references**, **MQM**, **four languages**, and **admittance / resistance** probes.

### ChartQAPro — Masry et al., ACL 2025 Findings

- **Link:** https://arxiv.org/abs/2504.05506 · **Anthology:** https://aclanthology.org/2025.findings-acl.978/ · **Code:** https://github.com/vis-nlp/chartqapro  
- **Summary:** Diverse real-world charts (infographics, dashboards, etc.) with harder question types including **unanswerable** and conversational items; strong models still drop sharply vs older ChartQA.  
- **Key finding:** Saturation on ChartQA hides weakness; diversity and unanswerable items expose brittleness.  
- **SciFig intersection:** Overlaps **unanswerable / hallucination** themes with SciFig **A1**; SciFig transfers similar ideas to **long-form description** and **judge-based** scoring.

### ChartMuseum — Tang et al., NeurIPS 2025 (D&B)

- **Link:** https://arxiv.org/abs/2505.13444 · **OpenReview:** https://openreview.net/forum?id=qLdX6TA19s · **Code:** https://github.com/Liyan06/ChartMuseum  
- **Summary:** ~1.16k expert QA pairs on real charts, labeled by **reasoning type** (text-heavy vs **visual** vs synthesis); humans stay high while best models stay far below, with large drops on **visual**-primary questions.  
- **Key finding:** Models that look capable on aggregate chart QA can still **fail when the task truly requires visual reasoning** rather than reading chart text.  
- **SciFig intersection:** Supports **F5 (genuine visual reading)** and **A2 (caption vs vision)**; SciFig tests this via **description**, **wrong caption**, and **page context**, not only typed QA.

### ChartQA — Masry et al., ACL 2022 Findings

- **Link:** https://arxiv.org/abs/2203.10244 · **Anthology:** https://aclanthology.org/2022.findings-acl.177/  
- **Summary:** Standard **chart QA** on real charts with relaxed numeric matching; human vs augmented subsets differ in difficulty.  
- **Key finding:** Chart QA needs both **perception** and **logical** steps; easy subsets inflate scores.  
- **SciFig intersection:** Foundational **chart** task; SciFig is **not** replacing Chart QA but complements it with **open-ended multilingual scientific figure** evaluation.

### PlotQA — Methani et al., WACV 2020

- **Link:** https://arxiv.org/abs/1909.00997  
- **Summary:** Large-scale QA over **scientific-style** plots (World Bank–style data); heavy emphasis on **numerical reasoning** over plots.  
- **Key finding:** Reasoning and data questions are much harder than shallow structure questions.  
- **SciFig intersection:** Aligns with **capability suite** (numerical reading, computation) on **plot-like** figures; SciFig adds **language**, **description**, and **behavioral** metrics.

### MultiChartQA — Zhu et al., NAACL 2025 (arXiv 2410.14179)

- **Link:** https://arxiv.org/abs/2410.14179  
- **Summary:** Benchmark where answers require **integrating multiple charts** (parallel, comparative, sequential reasoning).  
- **Key finding:** Single-chart benchmarks miss a major failure mode: **cross-chart** reasoning.  
- **SciFig intersection:** Relates to **cross-panel** / in-paper context in your capability suite; multi-chart is a different axis than multilingual description but same “**compositionality**” spirit.

---

## Hallucination, captioning, and factuality

### ChartHal — Wang et al., 2025

- **Link:** https://arxiv.org/abs/2509.17481 · **Code:** https://github.com/ymcui/ChartHal  
- **Summary:** **Fine-grained hallucination** taxonomy for **chart QA** (irrelevant, non-existent, contradictory, etc.) with human-validated samples; strong models still score poorly on hallucination-heavy items.  
- **Key finding:** Hallucination on charts is **systematic** and **taxonomy-organized**, not rare noise.  
- **SciFig intersection:** Direct overlap with **A1**; SciFig adds **admittance** explicitly and applies probes to **generated descriptions** with **MQM**.

### CHOCOLATE — Huang et al., ACL Findings 2024

- **Link:** https://arxiv.org/abs/2312.10160 · **Code:** https://github.com/khuangaf/CHOCOLATE  
- **Summary:** Studies **factual errors** in **chart captioning** with LVLM analysis and correction-oriented discussion.  
- **Key finding:** Models produce **fluent but factually wrong** chart captions; errors are structured enough to analyze.  
- **SciFig intersection:** Same **generative** risk as SciFig descriptions; motivates **MQM**, multiple judges, and hallucination probes beyond a single BLEU/ROUGE score.

### HallusionBench — Guan et al., 2023

- **Link:** https://arxiv.org/abs/2310.14566  
- **Summary:** Diagnostic suite for **entangled** hallucination and **visual illusion** in LVLMs.  
- **Key finding:** “Hallucination” mixes **vision failures** and **language over-generation**; disentangling helps evaluation.  
- **SciFig intersection:** Conceptual backup for separating **fabrication** vs **honest uncertainty** (admittance) under ambiguous or degraded inputs.

---

## Vision vs text, recall, and bottlenecks

### See or Recall — Li et al., 2025

- **Link:** https://arxiv.org/abs/2504.09809  
- **Summary:** **No-image** baselines on visualization QA: models often answer correctly **without seeing the chart**, implying **parametric recall** and inflated “multimodal” scores.  
- **Key finding:** Many VisQA items are solvable from **language-side priors** alone; need **sanity checks** to know if vision matters.  
- **SciFig intersection:** Core support for **F1 / F2** (caption bias, parametric memory); SciFig should report **no-image / caption-only** baselines for **description**, not only QA.

### ARO — Yuksekgonul et al., 2022

- **Link:** https://arxiv.org/abs/2210.01936  
- **Summary:** Shows when VLMs behave like **bags of words** and underuse **order and relation** in images.  
- **Key finding:** **Textual shortcuts** can dominate unless benchmarks force relational grounding.  
- **SciFig intersection:** Mechanism story for **wrong-caption** and **page-text injection** failures (**resistance**).

### FUGU — Tartaglini et al., “Diagnosing Bottlenecks in Data Visualization Understanding by VLMs,” 2025

- **Link:** https://arxiv.org/abs/2510.21740 · **Code:** https://github.com/cogtoolslab/fugu  
- **Summary:** Controlled **scatter-plot** task suite with interventions; argues a major bottleneck is **vision–language hand-off**, not “vision can’t see” or “LM can’t do math” alone.  
- **Key finding:** Errors cluster at the **interface** between visual encoding and language reasoning.  
- **SciFig intersection:** Complements **selective blur** and **degradation** probes: failures may reflect **information loss at fusion**, not only OCR.

---

## Robustness, noise, and inconsistency

### “Losing the Plot” / CHART NOISe — Shin et al., 2025

- **Link:** https://arxiv.org/abs/2509.18425  
- **Summary:** Chart QA under **corruption, occlusion**, and difficult MC; uses **prompt-reverse** style checks (confirm vs deny) to reveal **self-inconsistency**.  
- **Key finding:** Clean-chart benchmarks **hide** sharp degradation under realistic imperfection and inconsistent answering.  
- **SciFig intersection:** Overlaps **A3** and **A4**; SciFig extends to **multilingual scientific figures** and ties degradation to **MQM deltas** and **resistance**.

### CHAOS — Moured et al., 2025

- **Link:** https://arxiv.org/abs/2505.17235 · **Data:** https://huggingface.co/datasets/omoured/CHAOS  
- **Summary:** **Robustness** benchmark with many **visual and textual perturbations** on chart tasks (e.g. ChartQA, chart2text-style settings in their evaluation).  
- **Key finding:** MLLMs are **systematically sensitive** to realistic chart noise.  
- **SciFig intersection:** Same stress axis as **A3**; useful citation for “**robustness is a first-class evaluation dimension**.”

### PRIN — Ahn & Yin, 2025

- **Link:** https://arxiv.org/abs/2504.01282  
- **Summary:** Defines **prompt-reverse inconsistency**: models disagree when asked which answers are “correct” vs “incorrect” for the same candidates.  
- **Key finding:** A distinct **trust** failure mode beyond sampling noise or paraphrase.  
- **SciFig intersection:** Theoretical basis for **A4**; CHART NOISe applies similar ideas in the chart domain.

---

## Misleading charts and visualization literacy

### Benchmarking VLMs on VLAT + CALVI — Pandey & Ottley, EuroVis / CGF 2025

- **Link:** https://arxiv.org/abs/2503.16632  
- **Summary:** Evaluates GPT-class VLMs on **standard visualization literacy** (VLAT) vs **critical** items about **misleading** design (CALVI).  
- **Key finding:** Models can look decent on **basic** chart reading yet **fail misleading-detection** tasks relative to humans.  
- **SciFig intersection:** Aligns with **A5** (misleading detection and **false alarms** on honest figures).

### Misviz — Tonglet et al., 2025

- **Link:** https://arxiv.org/abs/2508.21675 · **Project:** https://ukplab.github.io/arxiv2025-misviz/  
- **Summary:** Large benchmark for **detecting** misleading real-world visualizations and **typing** violation categories.  
- **Key finding:** Automated detection remains **hard** for both classical and MLLM baselines at scale.  
- **SciFig intersection:** Broader **misinformation chart** line; SciFig focuses on **scientific figure** context and **generative** behavior (inventing problems vs refusing).

### “The Perils of Chart Deception” — 2025

- **Link:** https://arxiv.org/abs/2508.09716  
- **Summary:** Taxonomy of **deceptive chart designs** and evaluation of how VLMs are **misled** in interpretation.  
- **Key finding:** Many VLMs **track deceptive visual cues** similarly to human viewers (i.e., they are fooled).  
- **SciFig intersection:** Same **trust** theme as **A5**; useful when discussing **axis / aspect / dual-axis** style manipulations vs SciFig’s **false-alarm** probe.

---

## Multilingual chart understanding

### PolyChartQA — Xu et al., 2025 (arXiv v2 Jan 2026)

- **Link:** https://arxiv.org/abs/2507.11939  
- **Summary:** **10 languages**, **~22.6k** test chart images and **~26k** QA pairs (plus a large train split): English seed charts are **decomposed** into JSON + code, **translated**, and **re-rendered** per language; evaluates **short-form chart QA** accuracy and cross-lingual conditions.  
- **Key finding:** Large **English vs non-English** gap; error analysis highlights **OCR** and **language bias**; multilingual **instruction tuning** helps a lot.  
- **SciFig intersection:** Same **multilingual** motivation; **different task** (re-rendered **QA** vs **natural paper figures** + **open description** + **MQM**). Cite carefully: **public artifact** for PolyChartQA itself was not clearly linked on arXiv at last check—verify before claiming “released dataset.”

---

## Encoding structure and “what makes items hard”

### EncQA — Apple, IEEE VIS 2025

- **Link:** https://arxiv.org/abs/2508.04650 · **Code:** https://github.com/apple/ml-encqa  
- **Summary:** Chart QA organized around **visual encoding channels** (e.g. position, length, color) to measure what skills break.  
- **Key finding:** Performance is **channel-dependent**; models are not uniformly “good at charts.”  
- **SciFig intersection:** Analytic lens for **capability suite** design and for explaining **which** degradations (blur legend vs blur data) hurt **which** skills.

---

## Human vs model sensitivity and degradation

### Chart-to-Experience — 2025

- **Link:** https://arxiv.org/abs/2505.17374  
- **Summary:** Argues MLLMs are **less sensitive** than human evaluators to subtle chart issues—**human–model sensitivity mismatch**.  
- **Key finding:** Automated or model-based grading can **miss** flaws humans care about (or vice versa).  
- **SciFig intersection:** Motivates **human subset**, **multiple judges**, and explicit **admittance** scoring—not only one automatic metric.

### DIQ-H — 2025 (hallucination under image degradation)

- **Link:** https://arxiv.org/abs/2512.03992  
- **Summary:** Studies how **hallucination** interacts with **degraded** images (persistence and failure modes).  
- **Key finding:** Degradation does not always reduce “confidence”; hallucinations can **persist or shift** form.  
- **SciFig intersection:** Pairs with **A3** and **admittance** (“**can’t see**” vs “**won’t admit**”).

---

## Chart summarization and long-form outputs (historical context)

### Chart-to-Text — Kantharaj et al., ACL 2022

- **Link:** https://arxiv.org/abs/2203.06486 · **Anthology:** https://aclanthology.org/2022.acl-long.277.pdf  
- **Summary:** Large benchmark for **chart summarization** / data-to-text; early work already noted **hallucination** and trend-misreporting in neural summaries.  
- **Key finding:** **Fluency ≠ faithfulness** for chart-generated text.  
- **SciFig intersection:** Precedent for **open-ended** chart-to-language evaluation; SciFig narrows to **scientific figures**, **multilingual references**, and **modern LVLM** probes.

---

## Evaluation methodology (for SciFig’s MQM story)

### MQM — Lommel et al., 2014 (framework)

- **Summary:** **Multidimensional Quality Metrics** framework from translation quality evaluation: error typologies, severity, and structured rater guidelines.  
- **SciFig intersection:** SciFig **adapts MQM** for figure-description quality and deltas under adversarial conditions; cite the original framework when describing judge training and error dimensions.

---

## Quick map: SciFig contribution → papers

| SciFig theme | Start here |
|--------------|------------|
| Real scientific charts + reasoning gap | CharXiv, SciFIBench, PlotQA |
| Open-ended / caption factuality | CHOCOLATE, Chart-to-Text |
| Hallucination taxonomy / unanswerable | ChartHal, ChartQAPro |
| Visual vs text reasoning | ChartMuseum, ARO, EncQA |
| No vision / recall | See or Recall |
| V–L bottleneck / interventions | FUGU |
| Noise, corruption, inconsistency | CHART NOISe, CHAOS, PRIN |
| Misleading charts | Pandey & Ottley (CALVI), Misviz, Perils of Chart Deception |
| Multilingual charts | PolyChartQA |
| Judge sensitivity / degradation | Chart-to-Experience, DIQ-H |

---

## Maintenance

When a paper gets a **camera-ready** version or **official code URL**, prefer **ACL Anthology** or **NeurIPS Proceedings** DOIs over arXiv in final citations, while keeping arXiv for preprints still in flux.
