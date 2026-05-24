# VLM Deployment Statistics and Concrete Examples

Compiled: May 2026. All figures sourced from web searches; use citations for verification.

---

## 1. Scale of Scientific Publishing

- **5.14 million** scholarly articles published globally in 2024, a 2.06% increase from 2023 and a 22.78% cumulative increase over 5 years ([PublishingState.com](https://publishingstate.com/more-than-5-million-scholarly-articles-were-published-in-2024-and-here-are-more-interesting-facts/2025/))
- Since 1980, published scientific articles have increased **8-9% annually** ([phys.org](https://phys.org/news/2024-10-millions-discoveries-published-year-explosive.html))
- arXiv submission rate: **~24,000 articles/month** as of Nov 2024, reaching **~28,000/month by late 2025** with super-exponential growth ([arXiv blog](https://blog.arxiv.org/2025/08/12/a-year-in-review-arxiv-2024-annual-report-posted/); [Medium](https://lightcapai.medium.com/the-event-horizon-of-knowledge-why-3-million-arxiv-papers-are-a-warning-signal-48fc9b74fb33))
- arXiv milestones: 1M articles by end of 2014, 2M by end of 2021 ([Wikipedia](https://en.wikipedia.org/wiki/ArXiv))
- AI papers on arXiv doubling every **~23 months**

### Figures Per Paper
- Average data items (tables + figures) per paper increased from **7 +/- 3 in 1993** to **14 +/- 11 in 2013** ([biorxiv](https://www.biorxiv.org/content/10.1101/2022.05.06.490896.full.pdf))
- Life science papers in Nature: average **12.3 figures per paper** (range 7-16)
- Panels per figure increased from **2 +/- 1 (1993)** to **4 +/- 2 (2013)**, meaning figures themselves are growing more complex
- **Implication**: At 5M+ papers/year with ~10+ figures each, there are **50+ million scientific figures published annually** that require interpretation

---

## 2. Platform Scale and Adoption

### ChatGPT / OpenAI
- **900 million weekly active users** (Feb 2026), up from 400M in Feb 2025 and 300M in Dec 2024 ([DemandSage](https://www.demandsage.com/chatgpt-statistics/); [ALM Corp](https://almcorp.com/blog/chatgpt-900-million-weekly-active-users/))
- **50 million paying subscribers** across all tiers; **9 million paying business users** (4x increase from Sep 2025) ([TechnologyChecker](https://technologychecker.io/blog/chatgpt-statistics))
- Revenue: **$25B+ annualized** (Mar 2026), generating **$2B/month** ([Panto](https://www.getpanto.ai/blog/chatgpt-statistics))

### Google Gemini
- **750 million monthly active users** by Q4 2025 ([tech-insider.org](https://tech-insider.org/google-gemini-750-million-users-march-2026-updates/))
- **8 million+ Gemini Enterprise seats** across 2,800+ companies ([fatjoe](https://fatjoe.com/blog/google-gemini-stats/))
- **1 in 6 AI Mode queries are non-text** (voice or images), demonstrating multimodal usage at scale

### Claude / Anthropic
- **7.38 million monthly app users** (Jan 2026, up from 2.9M in Jan 2025) ([DemandSage](https://www.demandsage.com/claude-ai-statistics/))
- **300,000+ business customers** on the API; **25 billion+ API calls/month** (45% from enterprise) ([aibusinessweekly](https://aibusinessweekly.net/p/claude-ai-statistics))
- Anthropic winning **~70% of head-to-head enterprise deals** against OpenAI among new purchasers in 2026
- **$14B annualized revenue** (Feb 2026)

### Google NotebookLM
- **5 million+ monthly active users** by Q1 2024, with 300% US surge ([seosandwitch](https://seosandwitch.com/notebooklm-statistics/))
- Available in **150+ countries**; 120% quarter-over-quarter growth in Q4 2024
- **62% of users upload images** for analysis; users upload **9.7 documents/month** on average
- Now synthesizes sources into structured data tables for export

---

## 3. AI Research Tools (Scientific Workflow)

### Elicit
- Used by **over 2 million researchers** in academia and industry ([elicit.com](https://elicit.com/))
- Searches **138 million academic papers** and **545,000 clinical trials**
- Reported to cut systematic review timelines by up to **60%**

### Semantic Scholar
- Indexes **200+ million academic papers** ([semanticscholar.org](https://www.semanticscholar.org/))

### Consensus
- Built on **~200 million peer-reviewed papers** via Semantic Scholar

### Efficiency Gains Reported
- Paper discovery: 4 hours to 45 minutes (**85% reduction**)
- Duplicate removal: 2 hours to 15 minutes (**87% reduction**)
- Abstract screening: 8 hours to 3 hours (**62% reduction**)

---

## 4. Concrete Deployment Examples

### Document AI / PDF Extraction
- **VLM Run**: Production platform achieving **98% accuracy** in visual data extraction, outperforming Azure Doc AI, GPT-4o, and Gemini 2.5 Pro; handles **32+ concurrent requests** ([vlm.run](https://www.vlm.run/blog/fast-tracking-visual-ai-in-construction-using-vlm-run))
- **LlamaParse**: VLM-powered agentic OCR that understands layouts, interprets embedded charts/tables, with self-correction loops ([llamaindex](https://www.llamaindex.ai/glossary/vision-language-model))
- Enterprise pattern: OCR preprocessing + VLM for structural extraction and normalization (dates, currencies, entity linking)

### Accessibility
- **Be My Eyes**: 6.9 million volunteers serving 250M+ blind/low-vision people globally; "Be My AI" feature powered by GPT-4 Vision launched 2023; 19,000+ beta testers shaped the design ([bemyeyes.com](https://www.bemyeyes.com/); [OpenAI](https://openai.com/index/be-my-eyes/))
- MIT **VisText**: generates captions for complex charts/graphs, among the hardest image types for assistive tech
- AI can provide descriptions of charts, graphs, and images in reports and presentations for blind users

### Pharma and Finance
- **53% of pharma finance leaders** prioritizing AI and advanced analytics ([coherentsolutions](https://www.coherentsolutions.com/insights/artificial-intelligence-in-pharmaceuticals-and-biotechnology-current-trends-and-innovations))
- Global AI in pharma market: **$1.94B in 2025**, projected **$16.49B by 2034** (27% CAGR)
- **95% of life sciences companies** use SAP solutions; SAP S/4HANA 2025 has embedded AI for document processing
- Finance: LLM pipelines ingest corporate slides/PDFs, convert to embeddings for retrieval-augmented analysis

---

## 5. Market Size Data

### Document AI Market
- Document AI market: **$19.33B in 2025**, growing to **$31.82B in 2026** (64.6% CAGR) ([GII Research](https://www.giiresearch.com/report/tbrc1963327-document-artificial-intelligence-ai-global-market.html))
- Projected to reach **$232B by 2030** (64.3% CAGR)

### Intelligent Document Processing (IDP)
- IDP market valued at **$10.57B in 2025** (Fortune Business Insights), projected to **$91.02B by 2034** (26.2% CAGR) ([Fortune Business Insights](https://www.fortunebusinessinsights.com/intelligent-document-processing-market-108590))
- Alternative estimate: **$3.22B in 2025**, growing to **$43.92B by 2034** ([Precedence Research](https://www.precedenceresearch.com/intelligent-document-processing-market))
- North America holds **48.1% market share** in 2026; cloud-based revenue ~$2.56B

### Vision AI / VLM Market
- VLM market reached **$3.84B in 2025**, projected **26.95% CAGR through 2035** ([Datature](https://datature.io/blog/enterprise-vision-ai-adoption-report-2026))
- **40%+ of new VLM deployments** at the edge

---

## 6. Hallucination and Risk Evidence

### Chart-Specific Hallucination (ChartHal Benchmark)
- **ChartHal**: 1,062 human-validated samples for chart hallucination evaluation ([arxiv 2509.17481](https://arxiv.org/pdf/2509.17481))
- **GPT-5 achieves only 34.46% accuracy**; **o4-mini only 22.79%** on chart hallucination tasks
- Hallucination types: value fabrication, trend misinterpretation, entity confusion, reasoning hallucination, chart-to-table translation drift

### Degradation on Imperfect Charts (CHART NOISe)
- **"Losing the Plot"** (Sep 2025): evaluated GPT-4o, Claude Sonnet 4, Gemini 2.5 Pro ([arxiv 2509.18425](https://arxiv.org/abs/2509.18425))
- Found **sharp performance drops** under corruption or occlusion
- Models remain **overconfident in degraded settings**, generating plausible but unsupported explanations
- **Prompt reverse inconsistency**: models contradict themselves when asked to confirm vs. deny the same statement about a chart
- Chart-to-table translation risks **error propagation** from imperfect parsing

### Key Risk Finding
- Questions involving **information absent from or contradictory to charts** are especially likely to trigger hallucinations

---

## 7. AI in Peer Review

- **50%+ of researchers** have used AI tools while peer reviewing manuscripts (survey of 1,600 academics) ([Nature](https://www.nature.com/articles/d41586-025-04066-5))
- **~20% of ICLR 2025 reviews** classified as AI-generated ([Nature](https://www.nature.com/articles/d41586-025-03506-6))
- **~12% of Nature Communications reviews** classified as AI-generated
- **103 high-impact journals** updated AI policies for peer review between March-August 2025 ([Wiley](https://onlinelibrary.wiley.com/doi/10.1002/leap.2035?af=R))
- Medical field: among top 100 SJR journals, 78 provide AI guidance, **46 explicitly prohibit** its use in review
- AI-assisted reviews correlated with **boosted paper scores and acceptance rates** ([arxiv 2405.02150](https://arxiv.org/pdf/2405.02150))

---

## 8. VLM Research Trends

- Analysis of **26,104 accepted papers** from CVPR, ICLR, NeurIPS (2023-2025): VLM papers constitute **40.7% of ICLR 2025** ([chatpaper](https://chatpaper.com/paper/198465))
- Three phases of AI for science: Foundational Modules (2022-23), Closed-Loop Integration (2024), Scalability and Collaboration (2025+)
- GPT-5 lab experiment optimized a gene-editing protocol with **79x efficiency gain**

---

## Key Narrative Points for Paper Introduction

1. **Scale of the problem**: 5M+ papers/year x 10+ figures each = 50M+ figures annually needing interpretation, growing exponentially
2. **Massive deployment**: VLMs already used by 900M+ (ChatGPT) and 750M+ (Gemini) weekly/monthly users; vision features are core, not peripheral
3. **Real production tools exist**: VLM Run (98% accuracy), LlamaParse, NotebookLM (5M+ users uploading images), Be My Eyes (6.9M volunteers)
4. **But accuracy is dangerously low on charts**: GPT-5 scores only 34% on chart hallucination benchmarks; sharp degradation on imperfect/real-world charts
5. **Stakes are high**: 50%+ of peer reviewers use AI; 20% of major conference reviews are AI-generated; figures are central to scientific claims
6. **Market is massive**: Document AI is a $19-32B market growing 60%+ annually
7. **Gap**: Enormous deployment but inadequate evaluation of figure understanding fidelity -- this is where SciFig fills the need
