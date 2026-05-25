# VLM Performance & Usage Statistics (2025-2026)

> Research compiled May 2026. Every fact below includes its source.
> Items marked [VERIFIED-WEBFETCH] were retrieved and confirmed via web fetch during this research session.
> Items marked [TRAINING-KNOWLEDGE] come from model training data and should be independently verified before citation.

---

## Part 1: VLM Benchmark Performance

### Qwen2.5-VL-72B-Instruct [VERIFIED-WEBFETCH]
Source: https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct

| Benchmark | Score |
|-----------|-------|
| MMMU (val) | 70.2 |
| MMMU_Pro | 51.1 |
| MathVista (mini) | 74.8 |
| ChartQA (test) | 89.5 |
| DocVQA (val) | 96.4 |
| AI2D (test) | 88.4 |
| OCRBench | 885 |
| MMStar | 70.8 |
| MMVet_turbo | 76.19 |
| HallusionBench | 55.16 |
| MMBench_DEV_EN_V11 | 88.0 |
| MathVision (full) | 38.1 |
| ScreenSpot | 87.1 |
| ScreenSpot Pro | 43.6 |

### Llama 4 Maverick (17B active / 400B total MoE) [VERIFIED-WEBFETCH]
Source: https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct

| Benchmark | Llama 4 Scout | Llama 4 Maverick | Llama 3.1 405B |
|-----------|--------------|-----------------|----------------|
| MMMU | 69.4 | 73.4 | — |
| MMMU Pro | — | 59.6 | 52.2 |
| MathVista | — | 73.7 | 70.7 |
| ChartQA | — | 90.0 | 88.8 |
| DocVQA (test) | — | 94.4 | 94.4 |

Architecture: Mixture-of-Experts, 1M context, up to 5 input images.
Training: ~22 trillion tokens (cutoff August 2024).

### InternVL3-78B [VERIFIED-WEBFETCH]
Source: https://arxiv.org/abs/2504.10479

- MMMU: **72.2** (state-of-the-art among open-source MLLMs)
- Described as "highly competitive with leading proprietary models, including ChatGPT-4o, Claude 3.5 Sonnet, and Gemini 2.5 Pro"
- Full benchmark tables are in the paper PDF (scores shown as images on HuggingFace card)

### Phi-4-Multimodal-Instruct (Microsoft) [VERIFIED-WEBFETCH]
Source: https://huggingface.co/microsoft/Phi-4-multimodal-instruct

| Benchmark | Phi-4-multimodal |
|-----------|-----------------|
| MMMU | 55.1 |
| MMMU-Pro (std/vision) | 38.5 |
| MathVista (testmini) | 62.4 |
| AI2D | 82.3 |
| ChartQA | 81.4 |
| DocVQA | 93.2 |
| InfoVQA | 72.7 |
| TextVQA (val) | 75.6 |
| OCR Bench | 84.4 |
| BLINK | 61.3 |
| ScienceQA Visual | 97.5 |

Speech-Vision Multimodal (voice + image input):

| Benchmark | Phi-4-multimodal | Gemini-2.0-Flash | Gemini-2.0-Flash-Lite | Gemini-1.5-Pro |
|-----------|-----------------|-----------------|----------------------|----------------|
| s_AI2D | 68.9 | 69.4 | 62.0 | 67.7 |
| s_ChartQA | 69.0 | 51.3 | 35.5 | 46.9 |
| s_DocVQA | 87.3 | 80.3 | 76.0 | 78.2 |
| s_InfoVQA | 63.7 | 63.6 | 59.4 | 66.1 |
| **Average** | **72.2** | **66.2** | **58.2** | **64.7** |

Open ASR Leaderboard: #1 with 6.14% WER (as of March 4, 2025).

### Gemma 3 27B (Google) [VERIFIED-WEBFETCH]
Source: https://huggingface.co/google/gemma-3-27b-it

| Benchmark | Score |
|-----------|-------|
| MMMU (pt) | 56.1 |
| ChartQA | 76.3 |
| DocVQA (val) | 85.6 |
| AI2D | 79.0 |
| RealWorldQA | 53.9 |
| TextVQA (val) | 68.6 |
| VQAv2 | 72.9 |
| BLINK | 39.6 |
| CountBenchQA | 68.0 |
| TallyQA | 54.3 |

### Pixtral Large (Mistral) [VERIFIED-WEBFETCH]
Source: https://mistral.ai/news/pixtral-large

- MathVista: **69.4%** ("outperforming all other models" per Mistral's claim)
- Surpasses GPT-4o and Gemini-1.5 Pro on ChartQA and DocVQA (exact numbers not given on page)

### Pixtral 12B (Mistral) [VERIFIED-WEBFETCH]
Source: https://mistral.ai/news/pixtral-12b

| Benchmark | Pixtral 12B | GPT-4o | Claude 3.5 Sonnet | Gemini-1.5 Flash |
|-----------|------------|--------|-------------------|-----------------|
| MMMU (CoT) | 52.5 | 68.6 | 68.0 | — |
| ChartQA (CoT) | 81.8 | 85.1 | — | 78.0 |
| DocVQA (ANLS) | 90.7 | — | 90.3 | — |
| MathVista (CoT) | 58.0 | — | — | — |
| VQAv2 | 78.6 | — | — | — |

Note: Pixtral 12B "no longer maintained and has been replaced by more powerful models" per Mistral.

### Cross-Model Benchmark Summary Table

Best scores per benchmark (from verified sources above):

| Benchmark | Best Score | Model |
|-----------|-----------|-------|
| MMMU | 73.4 | Llama 4 Maverick |
| MMMU (open-source) | 72.2 | InternVL3-78B |
| MathVista | 74.8 | Qwen2.5-VL-72B |
| ChartQA | 90.0 | Llama 4 Maverick |
| DocVQA | 96.4 | Qwen2.5-VL-72B |
| AI2D | 88.4 | Qwen2.5-VL-72B |
| OCRBench | 885 | Qwen2.5-VL-72B |

**Key observation for SciFig paper:** Even the best models score only ~90% on ChartQA and ~70-75% on MMMU, confirming that chart/figure understanding remains a challenging frontier.

---

## Part 2: VLM-Specific Usage Statistics

### IMPORTANT CAVEAT
**No verified web sources were found during this research session that provide concrete statistics about vision-specific feature usage rates, image upload percentages, or multimodal vs. text-only API call ratios.** The following are from training knowledge and require independent verification:

#### [TRAINING-KNOWLEDGE — verify before citing]

- **OpenAI**: As of early 2025, OpenAI reported ~400M weekly active ChatGPT users. No public breakdown of vision vs. text usage has been officially released.
- **Be My Eyes**: Partnered with OpenAI for "Be My AI" using GPT-4V. The app has ~700,000 registered users (blind/low-vision) and ~7 million volunteers. No public statistics on the number of AI-powered image description sessions have been released.
- **GitHub Copilot**: Visual/image features were not a primary modality as of early 2025; Copilot remained predominantly code-text focused.
- **Multimodal API adoption**: No official figures from OpenAI, Google, or Anthropic on what percentage of API calls include image inputs.

**Bottom line for the paper:** You can cite the benchmark scores above to demonstrate model capabilities, but claims about real-world vision adoption rates lack verifiable public sources. The gap between benchmark capability and documented real-world vision usage is itself a finding worth noting.

---

## Part 3: Real-World VLM Vision Applications

### Verified Deployments [TRAINING-KNOWLEDGE — verify before citing]

1. **Be My AI (Be My Eyes + OpenAI)**
   - Uses GPT-4V/GPT-4o to describe images for blind users
   - Source: https://www.bemyeyes.com/blog/announcing-be-my-ai
   - ~700K registered blind/low-vision users
   - Launched as beta in late 2023, general availability 2024

2. **Google Lens / Google Search Visual**
   - Multimodal search integrated with Gemini models
   - Source: Google I/O 2024 keynote
   - Billions of visual searches per month (Google's claim, not independently verified)

3. **Adobe Acrobat AI Assistant**
   - Uses VLMs to understand document layouts, charts, figures in PDFs
   - Source: Adobe blog, March 2024

4. **Microsoft Copilot Vision (Edge browser)**
   - Announced December 2024, uses GPT-4o to interpret what's on screen
   - Source: Microsoft blog

5. **Medical Imaging**
   - No major VLM-based system has received FDA clearance for primary diagnosis as of early 2025
   - Traditional deep learning systems (not foundation-model VLMs) dominate: e.g., IDx-DR for diabetic retinopathy (FDA cleared 2018)
   - Research: Med-PaLM M (Google, 2023) showed expert-level performance on medical VQA but is not deployed clinically
   - Source: https://arxiv.org/abs/2307.14334

6. **Tesla Vision (Autopilot/FSD)**
   - Tesla uses vision-only (no LiDAR/radar since 2022) for Autopilot
   - This is traditional computer vision / CNNs, NOT foundation-model VLMs
   - Source: Tesla AI Day presentations

---

## Part 4: Known VLM Vision Failures

### Chart/Figure Understanding Failures

1. **"Unraveling the Truth: Do VLMs really Understand Charts?"** [VERIFIED-WEBFETCH]
   - Source: https://arxiv.org/abs/2407.11229
   - Finding: VLMs show "significant performance variations based on question and chart types"
   - Models struggle when the same data appears in different visual formats
   - Complexity sensitivity: varying ability across chart types and question difficulty

2. **"MMC: Advancing Multimodal Chart Understanding with Large-scale Instruction Tuning"** [VERIFIED-WEBFETCH]
   - Source: https://arxiv.org/abs/2311.10774
   - Key finding: "Extensive experiments on MMC-Benchmark reveal the limitations of existing LMMs on correctly interpreting charts, even for the most recent GPT-4V model"
   - Created 600K instruction-tuning instances to address these failures

3. **ChartQA Performance Gap**
   - Even the best model (Llama 4 Maverick) scores only 90.0% on ChartQA
   - Smaller models like Gemma 3 27B score only 76.3%
   - This confirms that chart understanding remains substantially unsolved

4. **Counting and Numerical Reasoning**
   - Qwen2.5-VL-72B scores only 55.16 on HallusionBench
   - Gemma 3 27B scores only 68.0 on CountBenchQA
   - MathVision (full) scores remain low: Qwen2.5-VL-72B at 38.1

### Relevance to SciFig-Evaluation

These failures directly support the SciFig project's premise:
- Best ChartQA accuracy is ~90% — meaning ~10% of chart questions are answered incorrectly even by frontier models
- HallusionBench scores in the 50s indicate substantial hallucination on visual inputs
- MathVision scores below 40 show that complex mathematical figure reasoning remains very weak
- The consistency/robustness finding (arxiv 2407.11229) is directly relevant: models give different answers when the same data is presented in different chart formats

---

## Notes on Sources Not Retrieved

The following sources were attempted but could not be fetched (permission denied or dynamic content):
- OpenCompass multimodal leaderboard (dynamic JavaScript rendering)
- LMSYS Chatbot Arena Vision leaderboard (dynamic JavaScript rendering)
- Papers With Code SOTA pages for ChartQA, MMMU, DocVQA, MathVista (permission denied)
- OpenAI GPT-4o system card and blog posts (permission denied)
- Anthropic Claude 3 family, Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude 4 announcements (permission denied)
- Google Gemini 2.0/2.5 blog posts (permission denied)
- NHTSA autonomous vehicle safety statistics (permission denied)
- Be My Eyes blog (permission denied)

**Recommendation:** Manually visit these URLs to fill in:
- GPT-4o scores on MMMU (~69.1), ChartQA (~85.7), DocVQA (~92.8)
- Claude 3.5 Sonnet scores on MMMU (~68.3)
- Gemini 2.0/2.5 Pro scores
- LMSYS Vision Arena Elo rankings
- OpenCompass comprehensive comparison table
