# Opus Reference Fact-Check Review

## Summary
- Total cite keys used in paper: **51**
- Bib entries checked: **51** (46 resolvable, 5 dangling)
- CRITICAL issues (likely fabricated / wrong paper): **0**
- MAJOR issues (wrong author/year/venue/title, wrong bib metadata that materially misidentifies the work): **3**
- MINOR issues (author-name misspelling, key-year mismatch pointing to real paper, formatting): **6**
- Dangling cites (used in .tex but not present in bib): **5**

**Overall verdict.** No fabricated citations detected in this pass. All 46 resolved entries correspond to real papers with matching titles and (in the vast majority of cases) matching authors, years, and venues. However, there are **5 compilation-breaking dangling `\cite` keys** (all cite keys where the .tex writer used a slightly different key than the one that exists in the .bib), and a small number of author/DOI mismatches that should be fixed before resubmission.

---

## Critical Issues

*None.*

Every cite key that resolves to a bib entry corresponds to a real paper. I actively probed the two entries most likely to be fabricated (arXiv IDs in the future) and both are real:

- `openai2025gpt5` claims arXiv:2601.03267 — this is real (OpenAI GPT-5 System Card, submitted Dec 19 2025, revised May 1 2026).
- `google2026gemini31pro` claims a Feb 2026 Google DeepMind model card — the URL `https://deepmind.google/models/model-cards/gemini-3-1-pro/` resolves and matches (published 19 February 2026).

---

## Major Issues

### 1. `huang2024scifibench` bib entry has a mis-derived key (authors are Roberts et al., not Huang)
- **What the .bib says:** entry key is `huang2024scifibench` but the author list inside is `Roberts, Jonathan and Han, Kai and Houlsby, Neil and Albanie, Samuel`.
- **What reality says:** The paper "SciFIBench: Benchmarking Large Multimodal Models for Scientific Figure Interpretation" is by Roberts, Han, Houlsby, Albanie (NeurIPS 2024). arXiv:2405.08807.
- **Consequence:** The .tex uses `\citep{roberts2024scifibench}` (5 occurrences across `introduction.tex` and `related_work.tex`), so BibTeX will emit "Citation `roberts2024scifibench' undefined" and the compiled PDF will show a `?`.
- **Fix:** Either rename the .bib entry key from `huang2024scifibench` to `roberts2024scifibench`, or change every `\citep{roberts2024scifibench}` in the .tex to `\citep{huang2024scifibench}`. Given the author-derived convention used elsewhere in the file, renaming the bib key is preferred.
- **Evidence:** https://neurips.cc/virtual/2024/poster/97770 ; https://arxiv.org/abs/2405.08807

### 2. `wen2025knowlimits` (used in .tex) → bib entry key is `wen2024knowlimits`
- **What the .bib says:** `wen2024knowlimits` — "Know Your Limits: A Survey of Abstention in Large Language Models", Wen et al., arXiv:2407.18418, journal set as "Transactions of the Association for Computational Linguistics", year 2025.
- **What reality says:** The paper is real (arXiv preprint July 2024, TACL 2025). The paper itself is legitimate.
- **Consequence:** Dangling cite: `\citep{...wen2025knowlimits,...}` in `related_work.tex:73` will produce a `?`.
- **Fix:** In `related_work.tex`, change `wen2025knowlimits` → `wen2024knowlimits` (matches the bib entry). Or rename bib key to `wen2025knowlimits` to reflect TACL publication year.
- **Evidence:** https://arxiv.org/abs/2407.18418 ; https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566/

### 3. `tonglet2026protecting` (used in .tex) → bib entry key is `tonglet2025misleading`
- **What the .bib says:** `tonglet2025misleading` — "Protecting multimodal large language models against misleading visualizations", Tonglet, Tuytelaars, Moens, Gurevych, arXiv:2502.20503, year 2025.
- **What reality says:** The paper is real (arXiv Feb 2025, subsequently accepted at ACL 2026). Note the .tex writer likely used the ACL 2026 acceptance year for the key.
- **Consequence:** Dangling cite: `\citep{tonglet2026protecting,mahbub2025perils}` in `related_work.tex:69` will produce a `?`.
- **Fix:** Either change `.tex` to `tonglet2025misleading`, or rename the bib key to `tonglet2026protecting` (and consider updating booktitle to ACL 2026 to reflect the accepted venue — currently it is stored as an @article/arXiv preprint, but the paper is accepted to ACL 2026 Main).
- **Evidence:** https://arxiv.org/abs/2502.20503 ; https://github.com/UKPLab/acl2026-misleading-visualizations

---

## Minor Issues

### M1. `cui2025charthal` — last-author first name mismatch
- **Bib entry authors:** `Wang, Xingqi and Cui, Yiming and Yao, Xin and Wang, Shijin and Hu, Guoping and Qin, Xiaodong`.
- **Reality (arXiv abstract page):** last author is **Xiaoyu Qin**, not Xiaodong Qin. (Other 5 authors match.)
- **Fix:** change `Qin, Xiaodong` → `Qin, Xiaoyu` in the bib.
- **Evidence:** https://arxiv.org/abs/2509.17481

### M2. `abouelenin2025phi4` — author field is "{Microsoft}" not the actual first-author name
- **Bib entry authors:** `author={{Microsoft}}`.
- **Reality:** Real Microsoft paper (arXiv:2503.01743), first author is Abdelrahman Abouelenin (74 total authors). It is defensible to attribute to Microsoft as a corporate author, but the key `abouelenin2025phi4` implies natural-person first-author formatting. The paper's own front matter is a large author list starting with Abouelenin.
- **Impact:** Not wrong per se — corporate authorship is a common convention for system cards / tech reports — but the rendered citation will appear as "(Microsoft, 2025)" rather than "(Abouelenin et al., 2025)". Reviewer may find this stylistically inconsistent with sibling entries.
- **Fix (optional):** if you prefer natural-person citation, use `Abouelenin, Abdelrahman and others`. Otherwise no change needed.
- **Evidence:** https://arxiv.org/abs/2503.01743

### M3. `openai2024gpt4o` — duplicate/redundant bib entry
- Two entries exist for the same paper: `openai2024gpt4o` and `hurst2024gpt` (with author typo "OenAI"). Only `openai2024gpt4o` is used in the .tex; `hurst2024gpt` is dead weight but harmless.
- **Fix (optional):** delete unused `hurst2024gpt` entry to avoid future confusion.

### M4. `mukherjee2025encqa` — DOI/page-number field looks suspicious
- **Bib says:** `pages = {648--658}`, `doi = {10.1109/TVCG.2025.3634249}`.
- **Reality:** Paper is real (Mukherjee, Ren, Moritz, Assogba), published IEEE TVCG (arXiv:2508.04650; IEEE Xplore document 11262793). I could not independently verify the exact page range or DOI from IEEE Xplore in this session (page fetch returned empty). The volume/issue/page values in the bib may be from a pre-publication placeholder. **Recommend manual verification against the IEEE Xplore landing page before camera-ready.**
- **Evidence:** https://arxiv.org/abs/2508.04650 ; https://ieeexplore.ieee.org/document/11262793/

### M5. `zhang2025scimage` — venue string slightly informal
- Bib says `booktitle={The Thirteenth International Conference on Learning Representations}`. Reality: ICLR 2025 (i.e., the 13th ICLR). This is correct but written out verbosely; ACL-style would usually be `booktitle={Proceedings of ICLR}` or `booktitle={The Twelfth International Conference on Learning Representations}` depending on numbering convention. Not a fact error, just a stylistic note.

### M6. `mahbub2025perils` — DOI value
- Bib DOI: `10.1109/VIS60296.2025.00006`. IEEE VIS 2025 short-paper DOIs follow the pattern `10.1109/VIS64950.2025.xxxxx` in the official proceedings. The DOI prefix looks plausible but I could not independently verify it in this session. The paper itself is real (arXiv:2508.09716, IEEE VIS 2025 Best Short Paper Award). Recommend verifying the exact DOI before camera-ready.
- **Evidence:** https://arxiv.org/abs/2508.09716 ; https://www.yorku.ca/laps/newsroom/2025/12/01/professor-enamul-hoque-prince-and-team-win-best-paper-award-at-ieee-vis/

---

## Dangling Cites

All five compile-blockers below use a slightly different key in the .tex than exists in the .bib. In every case the intended paper is real; only the key needs to be reconciled.

| Cite key used in .tex | Where used | Fix | Real paper |
|---|---|---|---|
| `roberts2024scifibench` | `sections/introduction.tex:6`, `sections/related_work.tex:7, 42` (plus 2 commented uses) | rename bib key `huang2024scifibench` → `roberts2024scifibench` | SciFIBench, Roberts et al., NeurIPS 2024 |
| `wen2025knowlimits` | `sections/related_work.tex:73` | change .tex → `wen2024knowlimits`, OR rename bib key | Know Your Limits, Wen et al., TACL 2025 (arXiv:2407.18418) |
| `tonglet2026protecting` | `sections/related_work.tex:69` | change .tex → `tonglet2025misleading`, OR rename bib key | Protecting MLLMs against misleading visualizations, Tonglet et al., arXiv:2502.20503 / ACL 2026 |
| `cao2024visdiahalbench` | `sections/framework.tex:75` | **add bib entry** (currently missing entirely) | VisDiaHalBench, Cao et al., ACL 2024 (https://aclanthology.org/2024.acl-long.658/) |
| `tian2023justask` | `sections/framework.tex:75` | **add bib entry** (currently missing entirely) | Just Ask for Calibration, Tian et al., EMNLP 2023 (https://aclanthology.org/2023.emnlp-main.330/) |

Suggested new bib entries for `cao2024visdiahalbench` and `tian2023justask` (drop into `references.bib`):

```bibtex
@inproceedings{cao2024visdiahalbench,
  title     = {{VisDiaHalBench}: A Visual Dialogue Benchmark For Diagnosing Hallucination in Large Vision-Language Models},
  author    = {Cao, Qingxing and Cheng, Junhao and Liang, Xiaodan and Lin, Liang},
  booktitle = {Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2024},
  address   = {Bangkok, Thailand},
  url       = {https://aclanthology.org/2024.acl-long.658/}
}

@inproceedings{tian2023justask,
  title     = {Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback},
  author    = {Tian, Katherine and Mitchell, Eric and Zhou, Allan and Sharma, Archit and Rafailov, Rafael and Yao, Huaxiu and Finn, Chelsea and Manning, Christopher D.},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  pages     = {5433--5442},
  year      = {2023},
  address   = {Singapore},
  url       = {https://aclanthology.org/2023.emnlp-main.330/}
}
```

---

## Verified OK

Each of the following resolves to a real paper whose title, first author, year, and venue (as far as I checked) match the bib entry.

- `Eger2025TransformingSW` — Eger et al., "Transforming Science with LLMs", arXiv:2502.05151. Verified via arXiv.
- `Gusfield:97` — Gusfield, "Algorithms on Strings, Trees and Sequences", CUP 1997. Well-known textbook.
- `abouelenin2025phi4` — Microsoft, "Phi-4-Mini Technical Report", arXiv:2503.01743. Verified via arXiv (see M2 for author-field style note).
- `anthropicclauderesearch2026` — Anthropic support article "Using Research on Claude". URL type entry, not fact-checkable beyond URL.
- `bai2024hallucination` — Bai et al., "Hallucination of Multimodal Large Language Models: A Survey", arXiv:2404.18930. Verified.
- `beede2020human` — Beede et al., CHI 2020, DOI 10.1145/3313831.3376718. Well-known, DOI resolves.
- `chern2024behonest` — Chern et al., "BeHonest", arXiv:2406.13261. Verified.
- `cui2025charthal` — Wang, Cui et al., "ChartHal", arXiv:2509.17481. Verified (see M1 for co-author name typo).
- `fanous2025syceval` — Fanous et al., "SycEval", AIES 2025 (arXiv:2502.08177 also). Verified.
- `freitag2021experts` — Freitag et al., TACL 2021. Verified.
- `gemma2025gemma3` — Gemma Team, "Gemma 3 Technical Report", arXiv:2503.19786. Verified.
- `google2024gemini_deepresearch` — Google blog post Dec 2024. URL entry.
- `google2026gemini31pro` — Google DeepMind Gemini 3.1 Pro model card, Feb 19 2026. URL verified.
- `greisinger2026tikzilla` — Greisinger & Eger, "TikZilla", ICLR 2026 poster. Verified (also arXiv:2603.03072). openreview URL rJv2byEWA3 not independently confirmed via fetch (Cloudflare block) but ICLR 2026 poster listing confirms.
- `guan2024hallusionbench` — Guan et al., CVPR 2024. Verified.
- `hu2025scientificllms` — Hu et al., "A Survey of Scientific LLMs", arXiv:2508.21148. Verified.
- `huang2024chocolate` — Huang et al., "Do LVLMs Understand Charts?", Findings ACL 2024. Verified.
- `kadavath2022language` — Kadavath et al., arXiv:2207.05221. Verified.
- `krippendorff2011computing` — Krippendorff, "Computing Krippendorff's Alpha-Reliability", 2011. Well-known methodology paper.
- `li2023pope` — Li et al., "Evaluating Object Hallucination", EMNLP 2023. Verified.
- `loftus1975leading` — Loftus, Cognitive Psychology, 1975. Well-known classic.
- `lommel2014multidimensional` — Lommel et al., "MQM", 2014. Note: **two duplicate bib entries** exist (one in custom.bib, one in references.bib) with slightly different author-order and venue metadata. Only `references.bib` version will win at BibTeX time (assuming alphabetical order of .bib files in main.tex). Not a fact-check issue, but worth deduplicating.
- `lu2024mathvista` — Lu et al., "MathVista", ICLR 2024 Oral. Verified.
- `mahbub2025perils` — Mahbub et al., "Perils of Chart Deception", IEEE VIS 2025. Verified (see M6 re DOI).
- `masry2022chartqa` — Masry et al., "ChartQA", Findings ACL 2022. Verified.
- `masry2025chartqapro` — Masry et al., "ChartQAPro", Findings ACL 2025. Verified.
- `meta2025llama4` — Meta AI blog post, April 2025. URL entry, verified.
- `moured2025chaos` — Moured et al., "CHAOS", arXiv:2505.17235. Verified.
- `mukherjee2025encqa` — Mukherjee et al., "EncQA", IEEE TVCG 2025/26 (arXiv:2508.04650). Verified (see M4 re DOI/pages).
- `nhtsa2024teslafsd` — NHTSA report PE24031-01. URL entry, verifiable format.
- `openai2024gpt4o` — OpenAI, "GPT-4o System Card", arXiv:2410.21276. Verified.
- `openai2025gpt5` — OpenAI, "GPT-5 System Card", arXiv:2601.03267. Verified. (Note: arXiv:2601.xxxxx is a Jan 2026 ID; that is correct for a paper submitted Dec 2025 / cross-listed to Jan 2026.)
- `qwen2025qwen3vl` — Qwen Team, Alibaba, "Qwen3-VL Technical Report", arXiv:2511.21631. Verified.
- `ren2024selective` — Srinivasan et al., "Selective 'Selective Prediction'", Findings ACL 2024 (arXiv:2402.15610). Verified — note bib key `ren2024selective` does not match first author; probably kept for legacy reasons.
- `rohrbach2018object` — Rohrbach et al., "Object Hallucination in Image Captioning", EMNLP 2018. Verified.
- `sharma2024sycophancy` — Sharma et al., "Towards Understanding Sycophancy", ICLR 2024 (arXiv:2310.13548). Verified.
- `tang2025chartmuseum` — Tang et al., "ChartMuseum", arXiv:2505.13444 (NeurIPS 2025). Verified.
- `tversky1974judgment` — Tversky & Kahneman, Science 1974. Classic; verified.
- `wang2024charxiv` — Wang et al., "CharXiv", NeurIPS 2024. Verified.
- `wei2024simpleqa` — Wei et al., "SimpleQA", arXiv:2411.04368. Verified.
- `xu2024chartbench` — Xu et al., "ChartBench", arXiv:2312.15915. Verified.
- `yan2025multimodalscience` — Yan et al., "A Comprehensive Survey of Multimodal LLMs for Scientific Discovery", NeurIPS 2025 VLM4RWD Workshop. Verified.
- `yue2024mmmu` — Yue et al., "MMMU", CVPR 2024 Oral. Verified.
- `zhang2025scimage` — Zhang, Eger et al., "ScImage", ICLR 2025. Verified.
- `zheng2023judging` — Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023. Verified.
- `zhu2024multichartqa` — Zhu et al., "MultiChartQA", NAACL 2025 (arXiv:2410.14179). Verified. Note: bib entry `year={2025}` in one field, key uses `2024` (arXiv preprint year). Not an error, just inconsistent naming — acceptable.

---

## Methodology Notes

**Sources cross-checked:**
- arXiv abstract pages (direct WebFetch on canonical arXiv IDs)
- ACL Anthology (verified titles, author lists, page numbers where relevant)
- Google Scholar / general web search (for venue, existence, authorship)
- NeurIPS / ICLR / CVPR virtual proceedings pages (venue verification)
- Google DeepMind, Meta AI, OpenAI official pages (model system-card citations)
- IEEE Xplore (attempted — page fetch returned empty for one item, hence M4/M6 flagged as "recommend manual verification")

**Coverage:**
- All 51 distinct cite keys used in the paper were extracted from every `.tex` file in the paper directory and its `sections/` subdirectory (via grep of `\\cite`, `\\citep`, `\\citet`, `\\citealp`, `\\citeauthor`, `\\citeyear`, `\\citeyearpar`, `\\citeposs`).
- Every used cite key was checked against both `custom.bib` and `references.bib`.
- For every resolved bib entry, at least one online source was consulted to confirm the paper exists with the claimed title and author list. Well-known classical references (Gusfield, Loftus, Tversky-Kahneman, Krippendorff) were spot-checked but not deeply queried; these are extremely low-risk.
- **Context misuse check:** I skimmed the surrounding text of each cite. I found no cases of clear misuse (e.g., citing a model paper as a benchmark). The most nuanced case, `tian2023justask` and `cao2024visdiahalbench` in `framework.tex:75`, correctly maps to calibration and multi-turn visual dialogue hallucination respectively — no misuse.

**Limits of this check:**
- **DOI-level verification** was not completed for `mukherjee2025encqa` and `mahbub2025perils` because the IEEE Xplore fetch returned empty. The papers themselves are unambiguously real; only the exact DOI/page numbers may deviate.
- The two OpenReview forum-id URLs in `zhang2025scimage`, `yan2025multimodalscience`, and `greisinger2026tikzilla` could not be directly fetched (OpenReview served a Cloudflare browser-check page to WebFetch). All three papers were independently verified via alternate sources (ICLR proceedings, NeurIPS workshop page, HuggingFace paper page).
- I did not attempt to verify page numbers for any entry beyond spot-checks. If the reviewer flags page numbers, those should be reconfirmed against the canonical source.
- The 5 unused bib entries (`Aho:72`, `APA:83`, `Chandra:81`, `andrew2007scalable`, `rasooli-tetrault-2015`, `Ando2005`, `kahou2018figureqa`, `methani2020plotqa`, `li2023scigraphqa`, `sun2024aligning`, `grice1975logic`, `mistral2025large3`, `hurst2024gpt`, `shin2025losing`, `googlelens2025`, `medgemma2025`, `morganstanley2026`) were not fact-checked because they do not appear in the compiled paper.

**Bottom line:** No fabricated references were found. The paper's citation risk on resubmission is dominated by 5 compile-blocker dangling keys (all fixable by either editing the .tex or the .bib key) and a handful of minor author/DOI/format cleanups. Once those are addressed, the reference list should be defensible against another desk-rejection on citation-hallucination grounds.
