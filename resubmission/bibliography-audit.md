# Bibliography Audit Report

Verified `resubmission/6a143a4c382eafd7ee52e0c7/references.bib` and `custom.bib` against thesis `.bbl` at `thesis-work/support/thesis/main/abdnthesis.bbl` (source of truth from the signed thesis).

**Rule:** entries verifiable against the thesis `.bbl` were fixed. Entries NOT in the thesis are listed below as needing manual verification against arXiv/DOI — DO NOT edit them without live source verification.

---

## Provenance of the hallucinated citations

- **Origin:** Ananya Mukherjee's initial bulk Overleaf upload, commit `b32d25f` on 2026-05-25 17:17 UTC. Six entries had fabricated author metadata under clean base keys (`Huang, Jonathan and others` for SciFIBench, `Fanous, Anthony and others` for SycEval, etc.). This is what was submitted and got desk-rejected on 2026-07-30.
- **Wei's cleanup:** commit `c209b50` on 2026-08-02 (post desk-reject) by Wei Zhao (`andyweizhao1@gmail.com`) added correct entries under the base keys and renamed the fabricated originals to `_wrong` suffixes as audit markers.
- **This branch:** deletes the `_wrong` audit markers now that provenance is documented, plus applies other thesis-verified corrections.

---

## ✅ Applied (thesis-verified)

Every fix below uses the thesis `.bbl` as the source of truth.

### Deleted 6 hallucinated audit markers
- `huang2024scifibench_wrong`, `tang2025chartmuseum_wrong`, `chen2025multichartqa_wrong`, `pandey2025perils_wrong`, `ren2024selective_wrong`, `fanous2025syceval_wrong`

The correct siblings under the base keys (already matching the thesis) remain and continue to serve any `.tex` citations.

### Fixed wrong first-author entries
| Key | Was | Now (from thesis) |
|---|---|---|
| `cui2025charthal` | "Cui, Yiming and others" | Wang, X.; Cui, Y.; Yao, X.; Wang, S.; Hu, G.; Qin, X. |
| `chern2024behonest` | "Chern, Ethan and others" | Chern, S.; Hu, Z.; Yang, Y.; Chern, E.; Guo, Y.; Jin, J.; Wang, B.; Liu, P. |

### Fixed truncated `and others` → thesis-verified full author lists
- `abouelenin2025phi4` → {Microsoft Research} (institutional, as in thesis)
- `qwen2025qwen3vl` → {Qwen Team, Alibaba} (as in thesis)
- `guan2024hallusionbench` → full 12-author list + CVPR venue + pages 14375–14385
- `huang2024chocolate` → full 8-author list + arXiv:2312.10160
- `moured2025chaos` → full 7-author list
- `wen2024knowlimits` → full 7-author list + TACL venue + year 2025
- `wei2024simpleqa` → full 8-author list + correct title "Measuring Short-Form Factuality…"
- `yue2024mmmu` → full 22-author list
- `kadavath2022language` → 10 named authors + `@article` (was `@inproceedings` with `booktitle=arXiv…`)

### Metadata alignments (thesis-verified)
- `openai2025gpt5` title → "OpenAI GPT-5 System Card"; `@article` with `journal=arXiv...`
- `google2026gemini31pro` title casing + Feb date + "Google DeepMind model card" note
- `google2024gemini_deepresearch` full title "Try Deep Research and Our New Experimental Model in Gemini" + correct blog URL + December 2024 date
- `rohrbach2018object` added arXiv:1809.02156

---

## ⚠️ Raised (NOT fixed — need manual verification against arXiv/DOI)

These entries are cited in the paper but are NOT present in the thesis `.bbl`. Each needs manual verification against the live source. **Do not edit these based on memory or LLM output** — that is what caused the desk rejection.

### Team's own recent papers (verify against OpenReview)
- `yan2025multimodalscience` — NeurIPS 2025 VLM4RWD workshop; OpenReview `HSz1Kr5BeC`
- `zhang2025scimage` — ICLR 2025; OpenReview `ugyqNEOjoU`
- `greisinger2026tikzilla` — ICLR 2026; OpenReview `rJv2byEWA3`
- `Eger2025TransformingSW` — arXiv 2502.05151
- `zhang2025scientificllms` — arXiv 2508.21148. Author list ends `and others`; **note key stem is misleading — first author is Hu, Ming, not Zhang**. Key preserved because cited in intro (`\citep{zhang2025scientificllms}`)

### Model cards / blog posts (verify URL)
- `openai2024gpt4o` — arXiv 2410.21276
- `mistral2025large3` — https://mistral.ai/news/mistral-3
- `googlelens2025` — Google blog URL
- `medgemma2025` — Google Research blog URL
- `morganstanley2026` — OpenAI blog URL
- `anthropicclauderesearch2026` — Anthropic support URL

### Prior work (verify against arXiv/DOI)
- `loftus1975leading` — Cognitive Psychology 7(4):560–572 (classical, verify volume/pages)
- `tversky1974judgment` — Science 185(4157):1124–1131 (classical, verify)
- `krippendorff2011computing` — Departmental Papers (ASC)
- `beede2020human` — CHI 2020, DOI 10.1145/3313831.3376718
- `nhtsa2024teslafsd` — NHTSA URL
- `sharma2024sycophancy` — has 11 named + `and others`; verify. Note: thesis has `sharma2023sycophancy` (2023 arXiv, not 2024 ICLR)
- `li2023pope` — arXiv ID needed
- `li2023scigraphqa` — verify EMNLP 2023 or arXiv only
- `sun2024aligning` — 10 named + `and others`; verify full list
- `bai2024hallucination` — has `Bai, Zechen and others`; verify full author list against arXiv:2404.18930
- `lu2024mathvista` — has "Lu, Pan and others"; verify full list. Canonical arXiv 2310.02255, ICLR 2024
- `xu2024chartbench` — `journal` field is malformed: `"URL https://arxiv. org/abs/2312.15915"` (space in "arxiv. org"). Should be `journal={arXiv preprint arXiv:2312.15915}`. **Content is defensibly real** but the format is broken.
- `grice1975logic` — venue field is `journal={Syntax and Semantics}` but "Syntax and Semantics 3: Speech Acts" is a book chapter. Entry should be `@incollection` with `booktitle` (verify).
- `tonglet2025misleading` — arXiv 2502.20503, "Protecting multimodal LLMs against misleading visualizations". **Distinct from thesis's `tonglet2025misviz`** (arXiv:2508.21675, "Is this chart lying to me?"). Both are real Tonglet et al. papers. Verify this is the one intended.

---

## ⚠️ Raised (custom.bib)

- **DUPLICATE:** `lommel2014multidimensional` exists in BOTH `references.bib` and `custom.bib` with different metadata. This is a BibTeX compilation conflict (duplicate key). One must be removed. Not touching either here per "raise, don't fix" — recommend keeping the references.bib version (matches thesis's Lommel/Uszkoreit/Burchardt in Tradumàtica) and removing the custom.bib version.
- The remaining 7 entries in custom.bib (`Aho:72`, `APA:83`, `Chandra:81`, `andrew2007scalable`, `Gusfield:97`, `rasooli-tetrault-2015`, `Ando2005`) are ACL template placeholders. Only remove if unused.

---

## Summary of counts

- **Total in `references.bib`:** ~64 entries
- **Deleted (hallucinated audit markers):** 6
- **Corrected (thesis-verified):** 14
- **Raised (need manual verification, not touched):** ~24 in references.bib + 1 duplicate in custom.bib
