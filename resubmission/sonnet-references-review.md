# Sonnet Reference Fact-Check Review

Paper: `resubmission/6a143a4c382eafd7ee52e0c7/` (main.tex + sections/*.tex, custom.bib + references.bib)

## Summary
- Total cite keys used in paper: 50
- Bib entries checked: 45 (50 used keys minus 5 confirmed dangling)
- CRITICAL issues (likely fabricated / wrong paper): 2
- MAJOR issues (wrong author/year/venue/title/duplicate/mismatched key): 5
- MINOR issues (formatting, page-range gaps, cosmetic mismatches): 6
- Dangling cites (used but not in bib): 5

Overall assessment: **No evidence of wholesale fabrication of non-existent papers.** Every citation traces to a real, findable work. The problems are almost all **bibliography hygiene bugs** — mismatched cite keys, a duplicate/conflicting entry, a wrong document behind a real URL, and missing bib entries for two real papers. Given the paper's prior desk-rejection for hallucinated citations, these bugs (especially the dangling cites and the `nhtsa2024teslafsd` content mismatch) are exactly the kind of thing that would read as fabrication to a skeptical reviewer doing a citation pass, even though the underlying works are real. All must be fixed before resubmission.

---

## Critical Issues

### 1. `nhtsa2024teslafsd` — cited document does not match its own title
- **What the .bib says:** `title={Information Request {PE24031-01}: {Tesla} Full Self-Driving Collisions in Reduced Roadway Visibility Conditions}`, howpublished URL `https://static.nhtsa.gov/odi/inv/2024/INIM-PE24031-27346.pdf`, Nov 2024.
- **What reality says:** The URL is real and does belong to NHTSA investigation PE24031 (opened Oct 17, 2024, which genuinely concerns Tesla FSD and reduced-visibility collisions). However, the specific PDF at that URL is an **Information Request letter dated November 5, 2024**, addressed to Tesla regarding **misleading social-media/"robotaxi" marketing claims** — not a report on visibility-related collisions. The title in the bib entry does not describe the actual content of the linked document.
- **Used in:** `sections/introduction.tex` (×3, in commented-out/optional text: "deployed vision systems in which high performance under expected conditions has coexisted with failures under degraded or unusual visual inputs~\citep{beede2020human,nhtsa2024teslafsd}").
- **Severity:** CRITICAL if this sentence/citation survives into the final PDF — it is citing a document for a claim the document doesn't make. Note: as of the current sections/introduction.tex, all three usages of this key are inside `%`-commented lines, so it may not currently render in the compiled PDF. **Verify whether this text is still commented out before submission; if it is ever uncommented, the citation must be replaced** with either (a) the actual PE24031 investigation-opening resume document, or (b) a source whose content matches the "collisions in reduced visibility" claim.
- **Evidence:** https://static.nhtsa.gov/odi/inv/2024/INIM-PE24031-27346.pdf (letter content re: marketing claims, not visibility collisions).

### 2. `lommel2014multidimensional` — duplicate bib key with two conflicting entries, one has a broken/wrong URL
- **What custom.bib says (Version A, line 71-80):** author order Lommel, Burchardt, Uszkoreit; venue "Proceedings of Translating and the Computer 36"; url `https://aclanthology.org/2014.tc-1.11`.
- **What references.bib says (Version B, line 248-256):** author order Lommel, Uszkoreit, Burchardt; venue "Tradumàtica" journal, issue 12, pp. 455–463, DOI `10.5565/rev/tradumatica.77`.
- **What reality says:** The real MQM paper is Lommel, Uszkoreit, Burchardt, "Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics," **Tradumàtica**, issue 12 (2014), pp. 455–463 — matching **Version B**. The ACL Anthology ID `2014.tc-1.11` cited in **Version A** resolves to a **completely different, unrelated paper** ("Improving fuzzy matching through syntactic knowledge" by Vanallemeersch & Vandeghinste). Version A's venue/URL attribution is wrong.
- **Used in:** `sections/related_work.tex` line 74 — `\citep{lommel2014multidimensional,freitag2021experts}`.
- **Severity:** CRITICAL for bibliography integrity — with two `@`-entries sharing one BibTeX key, compilation will silently pick whichever the compiler encounters first/last (order-dependent, fragile), and Version A's URL is factually wrong (points to an unrelated paper). **Fix: delete Version A from custom.bib entirely; keep only Version B (Tradumàtica, correct DOI) in references.bib.**
- **Evidence:** https://aclanthology.org/2014.tc-1.11 (wrong paper), https://ddd.uab.cat/pub/tradumatica/tradumatica_a2014n12/tradumatica_a2014n12p455.pdf (correct paper).

---

## Major Issues

### 3. Dangling cite `wen2025knowlimits` — key/year mismatch with bib entry `wen2024knowlimits`
- **What the .tex uses:** `\citep{...,wen2025knowlimits,...}` in `sections/related_work.tex` line 73.
- **What the .bib has:** key `wen2024knowlimits`, `year={2025}`, note `arXiv:2407.18418` — i.e., the bib entry's own year field already says 2025, but the key says 2024.
- **What reality says:** Real paper, "Know Your Limits: A Survey of Abstention in Large Language Models," Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang — genuinely published in **TACL**, `2025.tacl-1.26`, DOI `10.1162/tacl_a_00754` (arXiv:2407.18418 is the preprint). The 2025 TACL publication date is correct; the bib key's "2024" is what's wrong.
- **Fix:** Rename bib key from `wen2024knowlimits` to `wen2025knowlimits` (matching what the text already cites) and keep year=2025. Currently this is a **dangling reference** — LaTeX will not resolve `\citep{wen2025knowlimits}` and will produce a `??` or compile warning.
- **Evidence:** https://aclanthology.org/2025.tacl-1.26/

### 4. Dangling cite `tonglet2026protecting` — key mismatch with bib entry `tonglet2025misleading`
- **What the .tex uses:** `\citep{tonglet2026protecting,mahbub2025perils}` in `sections/related_work.tex` line 69.
- **What the .bib has:** key `tonglet2025misleading`, title "Protecting multimodal large language models against misleading visualizations," Tonglet, Tuytelaars, Moens, Gurevych, arXiv:2502.20503, year 2025.
- **What reality says:** The paper is real and the bib entry (title/authors/arXiv ID/year) is accurate. Only the cite key differs from what's used in text (`tonglet2026protecting` vs `tonglet2025misleading`), and the year "2026" embedded in the text's key doesn't match the actual 2025 arXiv submission.
- **Fix:** Rename bib key to `tonglet2026protecting` (or, better, correct the in-text key to `tonglet2025misleading` and fix the erroneous implied 2026 year). Currently dangling — will not resolve at compile time.
- **Evidence:** https://arxiv.org/abs/2502.20503

### 5. Dangling cite `roberts2024scifibench` — key mismatch with bib entry `huang2024scifibench`
- **What the .tex uses:** `\citep{roberts2024scifibench}` (5 occurrences across `related_work.tex` and `introduction.tex`).
- **What the .bib has:** key `huang2024scifibench`, author `{Roberts, Jonathan and Han, Kai and Houlsby, Neil and Albanie, Samuel}`.
- **What reality says:** Real paper, "SciFIBench: Benchmarking Large Multimodal Models for Scientific Figure Interpretation," Roberts, Han, Houlsby, Albanie, NeurIPS 2024 Datasets and Benchmarks Track (arXiv:2405.08807). Authors in the bib entry are correct — but the bib **key** falsely implies first author "Huang," who is not an author on this paper at all. The in-text key `roberts2024scifibench` is the semantically correct one.
- **Fix:** Rename bib key from `huang2024scifibench` to `roberts2024scifibench`. Currently dangling.
- **Evidence:** https://arxiv.org/abs/2405.08807, https://openreview.net/forum?id=HcLFNuQwy5

### 6. Dangling cite `tian2023justask` — real paper, no bib entry exists at all
- **What the .tex uses:** `\citep{tian2023justask}` in `sections/framework.tex` line 75, in the sentence "Other axes exist, such as confidence calibration \citep{tian2023justask}..."
- **What the .bib has:** Nothing — confirmed via exhaustive grep of both custom.bib and references.bib, this key has no entry anywhere.
- **What reality says:** The likely intended paper is Katherine Tian et al., "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback," EMNLP 2023 (arXiv:2305.14975) — title and topic (confidence calibration) match the citation context closely. Not fabricated in the sense of referring to a nonexistent work, but the bib entry is simply **missing**, which will produce a dangling-reference compile error.
- **Fix:** Add the bib entry for Tian et al. 2023 EMNLP ("Just Ask for Calibration...").
- **Evidence:** https://aclanthology.org/2023.emnlp-main.330/

### 7. Dangling cite `cao2024visdiahalbench` — real paper, no bib entry exists at all
- **What the .tex uses:** `\citep{cao2024visdiahalbench}` in `sections/framework.tex` line 75, same sentence: "...multi-turn visual-dialogue consistency \citep{cao2024visdiahalbench}."
- **What the .bib has:** Nothing — confirmed via exhaustive grep, no entry anywhere.
- **What reality says:** Likely intended paper: Qingxing Cao, Junhao Cheng, Xiaodan Liang, Liang Lin, "VisDiaHalBench: A Visual Dialogue Benchmark For Diagnosing Hallucination in Large Vision-Language Models," ACL 2024, pp. 12161–12176 — title matches the cite key almost exactly and the topic (multi-turn visual-dialogue hallucination) matches the citation context. Missing bib entry, not evidence the underlying claim is fabricated.
- **Fix:** Add the bib entry for Cao et al. 2024 ACL ("VisDiaHalBench...").
- **Evidence:** https://aclanthology.org/2024.acl-long.658/

---

## Minor Issues

### 8. `ren2024selective` — cite key names an author ("Ren") who is not on the paper
- Bib entry's actual authors are Srinivasan, Hessel, Gupta, Lin, Choi, Thomason, Chandu — real paper, Findings of ACL 2024, arXiv:2402.15610, title/venue verified correct. No "Ren" appears anywhere in the author list. This is present as a legitimate `@inproceedings` entry (not dangling — the key IS defined and DOES match what's cited in text), so it will compile fine, but the key is misleading and could look like a citation mix-up to a careful reviewer.
- Recommend renaming key to `srinivasan2024selective` for clarity, though this is cosmetic only.

### 9. `abouelenin2025phi4` — author field is `{Microsoft}` but citekey implies first author "Abouelenin"
- Real paper confirmed (arXiv:2503.01743, "Phi-4-Mini Technical Report"), true first author is Abdelrahman Abouelenin among 70+ Microsoft co-authors. The bib `author` field is compressed to just `{Microsoft}`, which is a stylistic simplification consistent with how other org-authored tech reports in this bib are formatted (e.g. `{OpenAI}`, `{Meta AI}`) — not a fabrication, just an internal inconsistency between key and author field. No action strictly required, but note this generates a citation like "(Microsoft, 2025)" — acceptable for a system-card citation style but worth confirming intentional.

### 10. `xu2024chartbench` — malformed `journal`/`volume` fields
- `journal={URL https://arxiv. org/abs/2312.15915}`, `volume={2}` — this is garbled auto-generated BibTeX (likely from a scraper), not evidence of fabrication. The paper is real (arXiv:2312.15915). Recommend cleaning up to use proper `eprint`/`archivePrefix` fields.

### 11. `openai2025gpt5` — arXiv ID / submission-date internal inconsistency
- Bib cites arXiv:2601.03267 (ID prefix "2601" implies January 2026 submission). One web source's fetched page showed a "Submitted on 19 Dec 2025" date, which is inconsistent with a 2601.xxxxx ID (a Dec 2025 submission would normally get a 2512.xxxxx ID). OpenAI does not have a strong historical practice of mirroring system cards to arXiv (they're normally hosted at cdn.openai.com). Content plausibly exists per multiple sources, but the ID/date inconsistency and unusual publication channel warrant a direct manual check of https://arxiv.org/abs/2601.03267 in a browser before submission, given this paper's history of citation problems.

### 12. `google2026gemini31pro` — single-source, dynamic vendor URL
- Model card page fetched successfully and content is internally consistent with the bib entry (Feb 2026, Google DeepMind), but this is a single, non-archival, mutable vendor webpage. Recommend the authors keep a locally archived copy (or Wayback Machine snapshot) since vendor model-card URLs are frequently overwritten or retired.

### 13. `mukherjee2025encqa` — unverified page range
- Paper confirmed real (IEEE TVCG, DOI 10.1109/TVCG.2025.3634249, arXiv:2508.04650) but the exact page range "648–658" in the bib could not be independently confirmed (IEEE Xplore page metadata unavailable during check). Low risk given everything else about the entry checks out; recommend a final manual check against the IEEE Xplore record before camera-ready.

---

## Dangling Cites

All confirmed via exhaustive grep of `custom.bib` and `references.bib` — these five keys are `\citep`'d in the .tex sources but have **zero matching `@...{key,` entries** in either bib file:

| Cite key | Used in | Status |
|---|---|---|
| `tonglet2026protecting` | `sections/related_work.tex` line 69 | Real paper exists under different bib key `tonglet2025misleading` (see Major Issue #4) — rename to fix |
| `wen2025knowlimits` | `sections/related_work.tex` line 73 | Real paper exists under different bib key `wen2024knowlimits` (see Major Issue #3) — rename to fix |
| `roberts2024scifibench` | `sections/related_work.tex` (×3), `sections/introduction.tex` (×2) | Real paper exists under different bib key `huang2024scifibench` (see Major Issue #5) — rename to fix |
| `tian2023justask` | `sections/framework.tex` line 75 | Real paper, bib entry never created (see Major Issue #6) — add entry |
| `cao2024visdiahalbench` | `sections/framework.tex` line 75 | Real paper, bib entry never created (see Major Issue #7) — add entry |

Note: `zhang2025scimage` initially appeared dangling under a naive single-line grep because its `@inproceedings{` and key are split across two lines in `references.bib` (lines 9-10). It IS present and correct — false alarm, included here only to document the check.

---

## Verified OK

The following cite keys were checked against arXiv, ACL Anthology, OpenReview, NeurIPS proceedings, IEEE Xplore, ACM DL, or official vendor pages, and their title/authors/year/venue match the paper's bib entries with no material discrepancy:

- `openai2024gpt4o` — GPT-4o System Card, arXiv:2410.21276
- `meta2025llama4` — Llama 4 Herd blog post, ai.meta.com
- `qwen2025qwen3vl` — Qwen3-VL Technical Report, arXiv:2511.21631
- `gemma2025gemma3` — Gemma 3 Technical Report, arXiv:2503.19786
- `anthropicclauderesearch2026` — Anthropic "Using Research on Claude" help article
- `google2024gemini_deepresearch` — Google blog, Dec 11 2024
- `beede2020human` — CHI 2020, DOI 10.1145/3313831.3376718
- `yan2025multimodalscience` — NeurIPS 2025 VLM4RWD workshop, OpenReview HSz1Kr5BeC
- `zhang2025scimage` — ICLR 2025, OpenReview ugyqNEOjoU
- `greisinger2026tikzilla` — ICLR 2026, OpenReview rJv2byEWA3
- `Eger2025TransformingSW` — arXiv:2502.05151
- `hu2025scientificllms` — arXiv:2508.21148
- `bai2024hallucination` — arXiv:2404.18930
- `guan2024hallusionbench` — CVPR 2024, DOI 10.1109/CVPR52733.2024.01363
- `rohrbach2018object` — EMNLP 2018, arXiv:1809.02156
- `li2023pope` — EMNLP 2023, DOI 10.18653/v1/2023.emnlp-main.20
- `cui2025charthal` — arXiv:2509.17481
- `moured2025chaos` — arXiv:2505.17235
- `mahbub2025perils` — IEEE VIS 2025, DOI 10.1109/VIS60296.2025.00006 (winner, VIS 2025 Best Short Paper)
- `masry2022chartqa` — Findings ACL 2022, DOI 10.18653/v1/2022.findings-acl.177
- `wang2024charxiv` — NeurIPS 2024 D&B Track
- `tang2025chartmuseum` — arXiv:2505.13444
- `lu2024mathvista` — ICLR 2024 Oral
- `yue2024mmmu` — CVPR 2024 Oral
- `masry2025chartqapro` — Findings ACL 2025, DOI 10.18653/v1/2025.findings-acl.978
- `zhu2024multichartqa` — NAACL 2025, arXiv:2410.14179
- `huang2024chocolate` — Findings ACL 2024, DOI 10.18653/v1/2024.findings-acl.41
- `freitag2021experts` — TACL vol.9 (2021), DOI 10.1162/tacl_a_00437
- `zheng2023judging` — NeurIPS 2023, arXiv:2306.05685
- `loftus1975leading` — Cognitive Psychology vol.7 (1975)
- `tversky1974judgment` — Science vol.185 (1974)
- `sharma2024sycophancy` — ICLR 2024, arXiv:2310.13548
- `chern2024behonest` — arXiv:2406.13261
- `wei2024simpleqa` — arXiv:2411.04368
- `fanous2025syceval` — AIES 2025, DOI 10.1609/aies.v8i1.36598, arXiv:2502.08177 (note: correct arXiv ID is 2502.08177, not a typo in the bib itself but flagged during verification)
- `kadavath2022language` — arXiv:2207.05221
- `krippendorff2011computing` — UPenn ASC departmental paper (2011)
- `lommel2014multidimensional` — real (Tradumàtica version, i.e. Version B only — see Critical Issue #2 for the duplicate/wrong-URL Version A)
- `xu2024chartbench` — real, arXiv:2312.15915 (see Minor Issue #10 for formatting)
- `mukherjee2025encqa` — real, IEEE TVCG (see Minor Issue #13 for page range)
- `abouelenin2025phi4` — real, arXiv:2503.01743 (see Minor Issue #9)
- `openai2025gpt5` — likely real but flagged for manual re-check (see Minor Issue #11)
- `google2026gemini31pro` — likely real but flagged for manual re-check (see Minor Issue #12)
- `roberts2024scifibench` / `huang2024scifibench` — real (see Major Issue #5)
- `wen2025knowlimits` / `wen2024knowlimits` — real (see Major Issue #3)
- `tonglet2026protecting` / `tonglet2025misleading` — real (see Major Issue #4)
- `ren2024selective` — real (see Minor Issue #8)

## Misuse-in-Context Check

Spot-checked how citations are used in surrounding prose for signs of mismatched claims (e.g., benchmark cited as a model, or a finding misattributed):
- `lommel2014multidimensional`, `freitag2021experts` — used to justify adapting MQM to figure descriptions; both are genuinely MQM/human-eval methodology papers. OK.
- `zheng2023judging` — used for "LLM-as-judge" methodology; matches (MT-Bench/Chatbot Arena paper is exactly this). OK.
- `krippendorff2011computing` — used for the 0.80 inter-annotator reliability threshold; matches (this is literally Krippendorff's own alpha methodology paper). OK.
- `sharma2024sycophancy` — used to explain RLHF-driven admittance asymmetry between passive/active questioning; topically consistent with the paper's actual finding (sycophancy toward implicit helpfulness pressure). OK, though somewhat loosely applied — reasonable interpretive use, not a factual misuse.
- `loftus1975leading`, `tversky1974judgment` — used as psychology analogies (leading questions / anchoring bias) for VLM probe design; both are the correct, canonical papers for these named effects. OK.
- No clear cases found where a citation's actual content contradicts or fails to support the claim it's attached to, aside from the `nhtsa2024teslafsd` document-title mismatch already flagged as Critical Issue #1.

---

## Methodology Notes

- **Sources cross-checked:** arXiv (abstract pages fetched directly), ACL Anthology, OpenReview, NeurIPS proceedings (proceedings.neurips.cc), IEEE Xplore / computer.org CSDL, ACM Digital Library, Google Scholar-style web search, official vendor pages/blogs (deepmind.google, ai.meta.com, blog.google, support.claude.com, static.nhtsa.gov), GitHub project pages, and DOI resolution.
- **Work was parallelized across 4 independent verification passes** (one per ~12-14 cite keys), each performing live web search and direct URL fetches rather than relying on background knowledge, specifically because this paper has a documented history of citation fabrication.
- **Could not fully verify:**
  - Exact page ranges for `wang2024charxiv` (113569–113697) and `mukherjee2025encqa` (648–658) — DOIs/venues confirmed correct, but page metadata wasn't independently retrievable from the sources checked (IEEE Xplore returned 504/blocked responses in one pass).
  - `mahbub2025perils` exact page range (6–10) — DOI and venue confirmed, IEEE Xplore page data not independently retrieved.
  - One 22nd/17th-author name spelling for `yue2024mmmu` (bib says "Ziyan Yang," one source rendered "Zhenzhu Yang") — likely an OCR/scrape artifact on one side; all other 21 authors, title, venue, and year fully match, so this is very low risk.
  - `openai2025gpt5` and `google2026gemini31pro` — both point to genuinely very-recent (near-future relative to model training data) releases; content was found via live web fetch and is internally plausible, but given (a) this paper's fabrication history and (b) an observed arXiv ID/submission-date inconsistency for `openai2025gpt5`, both are flagged for a final human check by opening the URLs directly in a browser immediately before submission.
- **Known limits:** Web-fetch tools can occasionally return stale, cached, or hallucinated content for very recent (2026) URLs; agents cross-checked with multiple independent sources where possible, but single-source vendor-page confirmations (model cards, blog posts) should be treated as lower-confidence than DOI/ACL-Anthology/arXiv-verified academic papers. No citation-management software (Zotero/BetterBibTeX) or CrossRef API batch lookup was used; all checks were manual web search/fetch per entry.
