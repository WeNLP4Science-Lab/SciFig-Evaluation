# Presentation Data — Verified Sources

All numbers used in the presentation slides with verification status.

---

## Slide 1.1 — VLMs deployed everywhere

| Example | Stat | Status | Source |
|---------|------|--------|--------|
| Google Lens | 20B visual searches/month | VERIFIED | Google blog Oct 2024 |
| MedGemma | 81% match radiologist quality | VERIFIED | MedGemma Tech Report arxiv:2507.05201 |
| Morgan Stanley AI | 98% advisor adoption | VERIFIED | CDO Magazine, OpenAI case study |
| ChatGPT Vision | GPT-4o/5 reading images at scale | VERIFIED | General knowledge |
| Gemini in Workspace | Reading images in Gmail, Docs, Slides | VERIFIED | Google Workspace announcements |
| Meta AI Vision | Llama 4 across 3B+ users | VERIFIED | Meta AI blog |

---

## Slide 1.2 — Scientific research

| Example | Stat | Status | Source |
|---------|------|--------|--------|
| Claude for Research | Paper completed in 2 weeks | VERIFIED | Anthropic blog, Harvard Crimson. Nuance: physicist spent 50-60 hours overseeing, 270 sessions. Claude fabricated some results. |
| OpenAI Deep Research | Cited reports from hundreds of sources | VERIFIED | OpenAI docs |
| Gemini Deep Research | Multimodal research with inline charts | VERIFIED | Google blog Dec 2025 |
| SciSpace | Interprets figures in 200M+ papers | VERIFIED (corrected from 280M) | SciSpace papers page |
| Sakana AI Scientist | Autonomous end-to-end research agent | VERIFIED | Published in Nature. Caveat: 42% of experiments failed. |
| ICLR 2026 | 21% of peer reviews AI-written | VERIFIED | Pangram Labs report |

---

## Slide 1.3b — Frontier benchmark scores

| Benchmark | Score | Model | Status | Source |
|-----------|-------|-------|--------|--------|
| MATH-500 | 96% | Gemini 3 Pro | VERIFIED (o1=94.8%, Gemini 3 Pro=96.4%) | BenchLM |
| GPQA Diamond | 94% | Multiple frontier models | VERIFIED (Claude Mythos 94.6%, Gemini 3.1 Pro 94.3%) | Artificial Analysis |
| HumanEval | 94% | Claude Opus 4 / Kimi K2 | VERIFIED (94.5%) | LLM Stats |
| MMLU | 91% | OpenAI o1 (91.8%), GPT-5 (92.5%) | VERIFIED | LLM Stats |
| SWE-bench | 81% | Claude Opus 4.5 (80.9%) | VERIFIED | LLM Stats. Caveat: contamination concerns. |

---

## Slide 1.4 — Benchmark comparison table

### Original paper results (what the authors tested)

| Benchmark | Year | Best in paper | Score | Top models tested |
|-----------|------|---------------|-------|-------------------|
| ChartQA | 2022 | VL-T5 (pretrained) | 51.8% | T5, TaPas, VL-T5, VisionTaPas |
| CharXiv | 2024 | Claude 3.5 Sonnet | 60.2% (reasoning) | GPT-4o (47.1%), Gemini 1.5 Pro (43.3%), InternVL V2.0 (38.9%) |
| MMMU | 2024 | Gemini Ultra | 59.4% | GPT-4V (55.7%), LLaVA-1.5-13B (36.4%), Qwen-VL (35.9%) |
| PlotQA | 2020 | Authors' hybrid model | 22.5% | SAN-VQA (<8%), BAN (<1%), LoRRA (<1%) |
| SciFIBench | 2024 | GPT-4o | 75.4% (fig-to-cap) | Gemini 1.5 Pro (74.0%), Gemini 1.5 Flash (74.4%), Claude 3 Opus (59.8%) |
| PolyChartQA | 2025 | Gemini-2.5-Pro | 68.5% (avg all langs) | GPT-4o (50.9%), Qwen2.5-VL-7B (53.8%) |
| ChartMuseum | 2025 | Gemini-2.5-Pro | 63.0% | Claude-3.7-Sonnet (61.7%), o4-mini (61.5%), GPT-4o (42.2%). Human: 93% |

### Current leaderboard (2026)

| Benchmark | Current #1 | Score | Source |
|-----------|-----------|-------|--------|
| ChartQA | Claude 3.5 Sonnet | 90.8% | llm-stats.com |
| CharXiv-R | Claude Mythos Preview | 93.2% | llm-stats.com |
| MMMU | Qwen3.6 Plus | 86.0% | llm-stats.com |
| PlotQA | No active leaderboard | — | Papers With Code shut down Jul 2025 |
| SciFIBench | GPT-4o | 73.8% | No updated leaderboard since NeurIPS 2024 |
| PolyChartQA | Gemini-2.5-Pro | 68.5% | From paper, no public leaderboard |
| ChartMuseum | Gemini-2.5-Pro | 63.0% | chartmuseum-leaderboard.github.io |

### Key observations
- ChartQA went from 51.8% (2022) to 90.8% (2026) — near saturated
- CharXiv went from 60.2% (2024) to 93.2% (2026) — rapid improvement
- MMMU went from 59.4% (2024) to 86.0% (2026) — significant but not saturated
- PlotQA baseline was 22.5% (2020), no reliable current SOTA
- ChartMuseum: even best model (63%) is 30 points below human (93%)
- All benchmarks are closed-form QA, English-only (except PolyChartQA), no behavioural testing

---

## Slide 1.6 — Tesla NHTSA case

| Claim | Status | Source |
|-------|--------|--------|
| NHTSA Investigation EA26002 | VERIFIED | NHTSA official investigation |
| "Did not provide alerts when camera performance had deteriorated" | VERIFIED | NHTSA finding |
| 9 crashes, 1 fatality | VERIFIED | NHTSA report |
| 3.2M vehicles under investigation | VERIFIED | Electrek, NHTSA upgrade to Engineering Analysis |

---

## Slide 5 — multi_fig_004 model responses

| Model | Response | Source |
|-------|----------|--------|
| GPT-5.2 | "Anime Characters." | Our experiment: output/experiments/active_admittance/gpt-5.2/multi_language/multi_fig_004.json |
| Claude Opus 4.6 | "TV Characters (partially visible as 'aracters')" | Our experiment: same path, claude-opus-4.6 |
| Gemini 3.1 Pro | "The label is partially obscured. Only 'aracters' is visible." | Our experiment: same path, gemini-3.1-pro |

---

## Notes on Claude Mythos

- VERIFIED as real. Released April 8, 2026 as "Claude Mythos Preview"
- Limited release under Project Glasswing for cybersecurity
- NOT publicly available to general users
- Leads CharXiv-R (93.2%), SWE-bench Verified (93.9%), GPQA Diamond (94.6%)
- Source: red.anthropic.com, Fortune, AISI evaluation
- We should NOT use Claude Mythos in our "top models" column since it's not generally available
