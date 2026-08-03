# Bibliography Summary — `references.bib`

Category groupings for entries in the paper's bibliography. Kept here in Markdown so `references.bib` and `custom.bib` stay comment-free (BibTeX will treat `%`-prefixed lines as comments, but we prefer to keep operational notes out of the LaTeX source entirely).

For issues that were **corrected** using the thesis `.bbl` and issues that were **raised but NOT fixed** (needing manual arXiv verification), see [`bibliography-audit.md`](./bibliography-audit.md).

---

## Paper motivation references
Recent surveys and multi-modal-science papers cited in the introduction to motivate the setting.

- `yan2025multimodalscience`
- `zhang2025scimage`
- `greisinger2026tikzilla`
- `Eger2025TransformingSW`
- `zhang2025scientificllms` *(note: key stem is `zhang…` but the actual first author is Hu, Ming — cited as-is in `sections/introduction.tex`)*

## Model references (the 8 evaluated VLMs + judge)
- `openai2025gpt5` — GPT-5
- `openai2024gpt4o` — GPT-4o (judge)
- `google2026gemini31pro` — Gemini 3.1 Pro
- `abouelenin2025phi4` — Phi-4 Multimodal
- `meta2025llama4` — Llama 4 Maverick
- `qwen2025qwen3vl` — Qwen3-VL family (235B / 30B / 8B)
- `gemma2025gemma3` — Gemma-3-27B-IT
- `mistral2025large3` — Mistral Large 3 (used in the probe-designer ablation and judge robustness check)

## Psychology foundations
Classical citations for the analysis narrative (presupposition, heuristics, pragmatics).

- `loftus1975leading`
- `tversky1974judgment`
- `grice1975logic`
- `sharma2024sycophancy` *(note: thesis has this as `sharma2023sycophancy`, 2023 arXiv; see audit)*

## Chart and figure benchmarks
Related-work benchmarks compared in Table 1 and discussed in Section 2.

- `kahou2018figureqa`
- `methani2020plotqa`
- `masry2022chartqa`
- `xu2024chartbench` *(note: journal field is malformed — see audit)*
- `li2023scigraphqa`
- `wang2024charxiv` — CharXiv
- `huang2024scifibench` — SciFIBench (Roberts et al.)
- `tang2025chartmuseum` — ChartMuseum
- `zhu2024multichartqa` — MultiChartQA
- `masry2025chartqapro` — ChartQAPro
- `mukherjee2025encqa` — EncQA
- `lu2024mathvista`
- `yue2024mmmu`

## VLM hallucination
Related work on hallucination and factuality in vision-language models.

- `rohrbach2018object`
- `li2023pope`
- `guan2024hallusionbench`
- `sun2024aligning`
- `bai2024hallucination`
- `huang2024chocolate`
- `cui2025charthal`
- `moured2025chaos`
- `shin2025losing` — CHART-NOISe
- `tonglet2025misleading` — Tonglet's *Protecting multimodal LLMs against misleading visualizations* *(distinct paper from thesis's Tonglet reference — see audit)*
- `chartdeception2025` — Mahbub et al., "Perils of Chart Deception"

## Evaluation methodology
Metrics, honesty/abstention/sycophancy work, LLM-as-judge, calibration.

- `lommel2014multidimensional` — MQM framework (canonical entry lives here; **duplicate entry in `custom.bib` must be removed** — see audit)
- `freitag2021experts`
- `zheng2023judging` — LLM-as-judge
- `chern2024behonest`
- `wen2024knowlimits`
- `wei2024simpleqa`
- `ren2024selective` — Srinivasan et al., "Selective 'Selective Prediction'"
- `fanous2025syceval` — SycEval
- `kadavath2022language` — calibration

## Deployment and real-world references
Blog posts, product pages, and regulatory references cited in the introduction's broader-applicability paragraph.

- `googlelens2025`
- `medgemma2025`
- `morganstanley2026`
- `anthropicclauderesearch2026`
- `google2024gemini_deepresearch`
- `beede2020human` — Google Health / diabetic retinopathy CHI paper
- `nhtsa2024teslafsd` — NHTSA Tesla FSD investigation

## Reproducibility
- `krippendorff2011computing` — Krippendorff's alpha reliability

---

## `custom.bib`

`custom.bib` currently contains the seven ACL LaTeX template placeholder entries (`Aho:72`, `APA:83`, `Chandra:81`, `andrew2007scalable`, `Gusfield:97`, `rasooli-tetrault-2015`, `Ando2005`) plus one duplicate of `lommel2014multidimensional` that should be removed to avoid a BibTeX conflict. See `bibliography-audit.md` for details.

The template placeholders are safe to leave if unused — BibTeX only pulls entries actually cited in the `.tex` files.
