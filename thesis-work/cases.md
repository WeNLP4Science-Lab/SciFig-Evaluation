# Real-World VLM Deployments and AI Failure Cases

Research compiled for thesis presentation context.

---

## 1. Consumer VLM Deployments

### Google Lens
- 1.5B monthly users, 100B+ visual searches/year (2025)
- 99.8% OCR accuracy on handwriting, translates 120+ languages
- Circle to Search launched Jan 2024 with Samsung Galaxy S24
- Desktop Chrome integration Aug 2024
- Source: Google Lens Guide 2025, Google business blog

### Apple Intelligence
- On-device VLM: ViT-g 1B-parameter vision backbone
- Trained on 10B image-text pairs, 175M interleaved documents (550M images)
- Visual Intelligence identifies objects, extracts calendar events, Image Wand
- iOS 18.1 Oct 2024, iOS 18.2 Dec 2024
- Source: Apple Foundation Models Tech Report 2025

### Samsung Galaxy AI
- Circle to Search, AI Visual Search, Generative Edit, Photo Assist
- Jan 2024 with Galaxy S24; expanded to S23, S22, Fold/Flip
- Galaxy S25 (Jan 2025) deepened Gemini integration
- Source: Galaxy AI Wikipedia

### Microsoft Copilot Vision
- AI that views your screen/browser/camera and answers questions
- Oct 2024 Copilot Labs (Pro); 2025 rolled out free in US
- No images retained or logged; deleted when session ends
- Source: Microsoft Copilot blog Dec 2024

### Meta AI (Instagram, WhatsApp, Messenger)
- Powered by Llama 4 (MoE) and Llama 3.2 Vision (11B/90B)
- Image analysis, visual coding, image generation, animation
- Llama 3 integration Apr 2024; Llama 3.2 Vision Sep 2024; Llama 4 2025
- Source: Meta AI blog

### Amazon Rufus + Lens Live
- AI shopping assistant with visual search
- 250M+ customers, monthly users up 149%, interactions up 210% YoY
- Identifies items in context (style, material, proportions)
- Source: Amazon Rufus features page

### Snapchat AI
- AI Lenses from text prompts, visual search with Amazon integration
- AI-generated captions and Lens suggestions for Memories
- Source: Snap SPS 2024

---

## 2. Enterprise/Professional VLM Deployments

### Microsoft 365 Copilot
- Excel: analyzes data, generates charts, PivotTables, trend detection
- PowerPoint: "Explain this" for contextual explanations of slides
- Image interpretation in documents rolled out Dec 2025
- Source: Microsoft 365 Copilot Release Notes

### Bloomberg Terminal AI
- BloombergGPT: 50B-parameter model trained on 363B financial tokens
- AI-generated earnings call summaries, news insights
- Jan 2024 launch; mobile and Vision Pro versions Jul 2024
- Source: Bloomberg AI Summaries

### Salesforce Einstein Vision
- Image classification and recognition in CRM
- Einstein Trust Layer prevents sensitive data from entering LLMs
- Ongoing since 2017; expanded 2024-2025 with generative AI
- Source: Salesforce Einstein Guide 2024

### Adobe Firefly + Sensei
- Firefly generates images trained on 300M+ licensed assets
- Sensei: ML-powered insights across Adobe suite
- New video and audio models Feb 2025
- Source: Adobe Sensei

### Figma AI
- AI for design workflows: generating assets, first drafts, layout exploration
- 85% of designers say learning AI is essential (Figma 2025 AI Report)
- 33% use AI for design asset generation
- Source: Figma 2025 AI Report

---

## 3. Healthcare/Medical VLM Deployments

### FDA-Approved AI Landscape
- 950 total AI/ML devices authorized by FDA (mid-2025)
- 723 (76%) are radiology devices
- Top: GE HealthCare (115), Siemens (86), Philips (48), Canon (41), Aidoc (30)
- Source: FDA AI-Enabled Medical Devices

### Aidoc (Radiology Triage)
- 30 FDA-cleared AI tools for radiology
- Jan 2026: first comprehensive foundation model AI detecting multiple conditions from single abdominal CT
- 150+ US health systems, 1,600+ hospitals worldwide
- FDA Breakthrough Device Designation
- Source: Aidoc press release, STAT News

### Viz.ai (Stroke Detection)
- FDA-approved automatic stroke identification on CT angiography
- 13 cleared algorithms for stroke and neurocritical care
- Patients reach treatment ~66 minutes faster
- 1,600+ hospitals
- Source: AI in Radiology 2025

### IDx-DR / LumineticsCore (Ophthalmology)
- First FDA-authorized AUTONOMOUS diagnostic AI (any field)
- Screens for diabetic retinopathy in primary care
- Sensitivity: 87.4%, Specificity: 89.5%
- No specialist needed for interpretation
- FDA cleared Apr 2018; renamed LumineticsCore 2023
- Source: FDA Authorization DEN180001

### Google DermAssist (Dermatology)
- Noninferior to dermatologists, superior to primary care physicians
- CE-marked Class I medical device in EU
- Integrated into Google Lens skin search in US
- Source: Journal of Visual Communication in Dermatology

### PathAI (Digital Pathology)
- AISight Dx platform for digital pathology
- FDA 510(k) clearance 2022, expanded 2025
- Labcorp expanded PathAI across US labs
- Quest Diagnostics acquired PathAI diagnostic lab for $100M (May 2024)
- Source: MedTech Dive

---

## 4. Scientific Research VLM Tools

### Anthropic Claude for Research
- Claude Opus 4.5 shows improvements in figure interpretation, computational biology
- Claude for Life Sciences (Oct 2025): connectors to Benchling, BioRender, PubMed, Scholar Gateway
- Harvard physicist Matthew Schwartz completed a theoretical physics paper in 2 weeks (replacing a year of grad work)
- BUT: Claude fabricated results and took mathematical shortcuts, requiring domain expertise to catch
- Source: anthropic.com/news/accelerating-scientific-research

### Google Deep Research
- Agentic research with Gemini
- Deep Research (speed) and Deep Research Max (comprehensiveness)
- Generates charts/infographics inline
- 46.4% on Humanity's Last Exam, 66.1% on DeepSearchQA
- Dec 2025 via Gemini API
- Axiom Bio uses it to accelerate drug discovery
- Source: Google blog

### OpenAI Deep Research
- Powered by o3 model, searches hundreds of sources
- Produces cited reports with tables and visualizations
- Feb 2025 for Pro; Apr 2025 expanded to Plus/Team/Enterprise
- Takes 5-30 minutes per task
- Acknowledged limitation: "Can sometimes hallucinate facts, has trouble distinguishing rumors from fact, and often fails to convey uncertainty accurately"
- Source: openai.com/index/introducing-deep-research

### Elicit
- Semantic search across 200M+ papers (Semantic Scholar + OpenAlex)
- Extracts key findings, synthesizes across studies
- Source: elicit.com

### Semantic Scholar
- AI-powered research tool by Allen Institute for AI
- 200M+ papers indexed
- Source: semanticscholar.org

### Consensus AI
- Search engine summarizing findings across scientific studies
- Struggles with contradictory evidence
- Source: consensus.app

### Sakana AI Scientist
- Released Aug 2024 to automate entire research lifecycle
- Source: sakana.ai

### Google AI Co-Scientist
- Built on Gemini, unveiled Feb 2025
- Hypothesis generation and evaluation
- Source: Google blog

---

## 5. Autonomous Systems

### Tesla FSD
- Vision-only (cameras, no LiDAR/radar)
- FSD v13: end-to-end neural networks trained on ~50B miles shadow-mode data/year
- Cortex cluster: 50,000 H100 GPUs (Jan 2025)
- Robotaxi pilot launched Jun 22, 2025 in Austin, Texas (10-20 vehicles)
- ~$400/vehicle for sensor suite
- FAILURES: At least 13 fatal crashes as of Apr 2024. Four in Jan 2024 alone in reduced visibility.
- Source: gearmusk.com, Contrary Research

### Waymo
- 29 cameras, 5 LiDARs, radar. ~$12.7K/vehicle sensor suite
- 71M rider-only miles through Mar 2025
- Phoenix, San Francisco, Los Angeles, Austin
- FAILURE: May 2025 recall of 1,200+ robotaxis — software failed to classify stationary objects (chains, gates, poles). 7+ crashes with clearly visible obstacles.
- Source: Contrary Research

### Figure AI (Humanoid Robotics)
- Three generations (Figure 01-03) with Helix vision-language-action models
- BMW Spartanburg pilot supported 30K+ vehicles
- Valued at $39B (late 2025)
- Source: Figure AI Wikipedia

### 1X Robotics
- NEO humanoid robot for general-purpose tasks
- Preorders open, 2026 deliveries
- Source: mikekalil.com

### Boston Dynamics Atlas
- All-electric Atlas introduced Apr 2024
- First application: part sequencing in automotive manufacturing
- 2025 pilot in automotive manufacturing
- Source: Boston Dynamics blog

### Cognex (Manufacturing QA)
- AI-based machine vision for automated inspection
- Edge learning + deep learning for defect detection
- High-speed production line inspection
- Source: cognex.com

### Drone Inspection AI
- Autonomous drones with real-time CV for infrastructure inspection
- Detect damaged insulators, corrosion, vegetation on power lines at 40 mph
- Exelon/BGE deployed autonomous drones 2024
- Source: Deloitte, Optelos

---

## 6. Confident-but-Wrong AI: Failures and Consequences

### The Confidence Paradox
- AI models are 34% MORE likely to use "definitely," "certainly," "without doubt" when generating INCORRECT information
- Global business losses from AI hallucinations: $67.4 billion in 2024
- 47% of enterprise AI users made at least one major business decision based on hallucinated content
- Source: suprmind.ai AI Hallucination Statistics Report 2026

### Medical AI Failures
- AI methods can confidently make predictions even when confidence is not warranted
- Overconfidence + absent uncertainty quantification has reinforced medical professional skepticism
- Study of 9 AI programs on 1,000 ER cases (1.7M+ responses): recommendations changed based on race, gender, sexuality, income — not actual health conditions
- ECRI ranked AI risks as #1 health technology hazard for 2025
- Misleading AI explanations significantly DEGRADED diagnostic accuracy; correct explanations offered no improvement over no-explanation controls
- Source: PMC, UCSF AI Bias Study

### Autonomous Vehicle Perception Failures
- Tesla FSD: 13+ fatal crashes (Apr 2024). Four in Jan 2024 in reduced visibility (sun glare, fog, dust)
- Waymo: May 2025 recall of 1,200+ robotaxis — failed to classify thin stationary objects
- Total: 5,202 autonomous vehicle accidents in US by Nov 2025; 7.4% injury, 1.2% fatality
- Source: Bloomberg, Craft Law Firm

### Financial AI Overconfidence
- Algorithms "misread" market → unwarranted sell-offs → cascading responses (2010 Flash Crash)
- IMF warning (Oct 2024): AI contributing to increased market volatility
- US Treasury (Dec 2024): AI defects could pose risks to financial stability
- Source: Lawfare

### Legal AI Hallucinations
- Stanford 2024: LLMs hallucinated in 75% of legal queries, inventing 120+ non-existent court cases
- Air Canada 2024: chatbot confidently gave wrong bereavement fare info; tribunal ruled company responsible
- 1,397 documented hallucination cases in legal contexts since 2023
- 160 cases of AI-generated pleadings with fabricated citations
- Source: damiencharlotin.com hallucinations database

### Boeing 737 MAX as AI Safety Analogy
Published in Radiology: Artificial Intelligence (PMC):
1. Safety systems can cause harm — MCAS was designed for safety but caused both crashes
2. Input quality matters — MCAS used only 1 of 2 angle-of-attack sensors
3. Transparency is essential — flight crews not told MCAS existed
4. Override must be possible — Boeing made override difficult
5. False confidence in safety — assumed existing frameworks would catch issues
- Source: PMC8017379

---

## 7. Regulatory Requirements for AI Transparency

### EU AI Act
- Transparency rules take effect Aug 2026
- High-risk AI must disclose AI involvement, limitations, provide human oversight
- Users must be informed when interacting with AI
- Source: euaiact.com

### FDA Guidelines (Jan 2025 draft)
- Requires: identification of AI use, class of model and limitations
- Must disclose development/validation datasets
- Must report statistical confidence level of predictions
- Risk-based approach to assess AI model credibility
- Source: FDA AI Guidance

### Georgetown CSET (Jun 2024)
- "Key Concepts in AI Safety: Reliable Uncertainty Quantification in Machine Learning"
- Enabling ML systems to "know what they don't know" is a critical open research problem
- Source: cset.georgetown.edu

### Calibration Problem
- Contemporary neural networks are consistently miscalibrated
- Yield excessively confident predictions inappropriate for safety-critical applications
- ICLR 2025: "Do LLMs Estimate Uncertainty Well?"
- KDD 2025: survey on uncertainty quantification and confidence calibration in LLMs
- Source: ICLR 2025, KDD survey arxiv:2503.15850
