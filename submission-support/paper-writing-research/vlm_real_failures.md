# Documented Real-World Vision AI / VLM Failures

Compiled for paper motivation and related-work sections. All entries have verifiable sources.

---

## 1. Medical AI Failures

### 1a. GPT-4V on Radiology Images (2024)

**Finding:** GPT-4V scored 81.5% on text-only radiology questions but only 47.8% on image-based questions -- nearly a coin flip.

**Details:** Study used 386 retired ACR Diagnostic Radiology In-Training Exam questions. GPT-4V showed a tendency to overdiagnose abnormalities (sensitivity 78%, specificity 32.3%). Free-text diagnostic reports had only 36.5% accuracy. Critically, the model frequently arrived at correct final answers through *incorrect* image interpretations -- in one case describing a nonexistent hepatic lesion while missing an obvious left adrenal gland lesion, yet still selecting the right multiple-choice answer.

**Citation:** Hayden N, Gilbert S, Poisson LM, Griffith B, Klochko C. Performance of GPT-4 with Vision on Text- and Image-based ACR Diagnostic Radiology In-Training Examination Questions. *Radiology*. 2024 Sep. DOI: 10.1148/radiol.240153

**Source:** https://pubs.rsna.org/doi/10.1148/radiol.240153

### 1b. Hidden Flaws Behind Expert-Level Accuracy (2024)

**Finding:** GPT-4V presents flawed rationales in 35.5% of cases where it makes correct final choices, most prominently in image comprehension.

**Citation:** Published in *npj Digital Medicine*, 2024.

**Source:** https://www.nature.com/articles/s41746-024-01185-7

### 1c. FDA Recalls of AI-Enabled Medical Devices

**Finding:** As of November 2024, 60 AI-enabled devices had accumulated 182 recorded recall events. 109 devices were recalled for diagnostic or measurement errors. About 43% of all recalls occurred within one year of FDA authorization. 92% of recalled AI devices came from publicly traded companies. The vast majority of recalled devices had not undergone clinical trials before clearance.

**Details:** Causes included imaging software that mislabeled healthy organs as diseased and infusion systems delivering inaccurate medication doses.

**Sources:**
- https://www.healthcare-brew.com/stories/2025/09/03/recalled-ai-enabled-medical-devices-public-companies
- https://pubmed.ncbi.nlm.nih.gov/40844774/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12274014/

---

## 2. Autonomous Driving Vision Failures

### 2a. NHTSA EA26002: Tesla FSD Reduced-Visibility Crashes (2026)

**Finding:** NHTSA escalated its investigation of Tesla FSD to Engineering Analysis (EA26002) on March 18, 2026, covering 3.2 million vehicles. The investigation found that FSD's degradation detection system fails to warn drivers when cameras are blinded by sun glare, fog, dust, or other airborne particles.

**Details:** Nine crashes documented in the docket: one fatal pedestrian crash, at least two confirmed injury crashes, six additional under review. Tesla removed radar in mid-2021 against the advice of its own engineers who warned cameras alone would be vulnerable to environmental interference. A fatal crash involving FSD and reduced visibility occurred November 28, 2023; Tesla submitted the required SGO report seven months late (June 27, 2024).

**Sources:**
- https://electrek.co/2026/03/19/nhtsa-upgrades-tesla-fsd-visibility-investigation-3-2-million-vehicles/
- https://static.nhtsa.gov/odi/inv/2026/INOA-EA26002-10023.pdf
- https://www.ainvest.com/news/nhtsa-upgrades-tesla-fsd-probe-engineering-analysis-visibility-failures-recall-catalyst-2604/

### 2b. Uber ATG Fatal Crash -- Elaine Herzberg (2018)

**Finding:** On March 18, 2018, a self-driving Uber test vehicle struck and killed pedestrian Elaine Herzberg in Tempe, Arizona. The vision system failed to correctly classify her.

**Details:** Radar first detected Herzberg ~6 seconds before impact, followed by lidar. However, the self-driving system could not classify an object as a pedestrian unless they were near a crosswalk. For 5 seconds, the system alternated between classifying her as a vehicle, a bike, and an unknown object. The 4.7-second perception-reaction time allowed the car to travel 250 feet before any response. Automated braking was disabled.

**Citation:** NTSB Investigation Report.

**Sources:**
- https://spectrum.ieee.org/ntsb-investigation-into-deadly-uber-selfdriving-car-crash-reveals-lax-attitude-toward-safety
- https://en.wikipedia.org/wiki/Death_of_Elaine_Herzberg

### 2c. Cruise Robotaxi Pedestrian Dragging (2023)

**Finding:** On October 2, 2023, a Cruise robotaxi ran over a pedestrian who had been knocked into its path by a hit-and-run driver. The vehicle's detection system failed to detect a person was underneath it, and the vehicle then attempted to pull over, dragging the woman over 20 feet.

**Details:** Cruise filed a false report to NHTSA omitting the dragging. The company was fined $500,000 by the DOJ. California DMV suspended Cruise's autonomous vehicle permits.

**Sources:**
- https://www.justice.gov/usao-ndca/pr/cruise-admits-submitting-false-report-influence-federal-investigation-and-agrees-pay
- https://www.nbcbayarea.com/news/local/san-francisco/cruise-admits-filing-false-report-robotaxi-dragged-san-francisco-pedestrian/3710410/

---

## 3. The "Jagged Frontier" -- Stanford HAI AI Index 2026

**Finding:** The same frontier model that wins gold-medal-level scores at the International Mathematical Olympiad reads analog clocks correctly only 50.1% of the time (vs. 90.1% for humans on ClockBench). Top models came within 0.4 percentage points of the best human expert on MMMU (multimodal benchmark with diagrams, charts, tables, equations).

**Key quote for paper:** "Headline benchmark scores are a poor proxy for performance on the specific task your system needs to complete. This is not a temporary limitation pending the next model release -- it is a structural characteristic of current architectures."

**Citation:** Stanford Institute for Human-Centered Artificial Intelligence. The 2026 AI Index Report. April 2026.

**Sources:**
- https://hai.stanford.edu/ai-index/2026-ai-index-report
- https://hai.stanford.edu/ai-index/2026-ai-index-report/technical-performance
- https://www.rdworldonline.com/stanford-hai-2026-ai-index-ai-posts-gains-in-science-and-medicine-while-often-struggling-to-read-a-clock/

---

## 4. VLM Chart Reading Failures (Academic Studies)

### 4a. ChartHal: Hallucination in Chart Understanding

**Finding:** State-of-the-art LVLMs suffer from severe hallucinations on charts. Proprietary models GPT-5 and o4-mini achieved only 34.46% and 22.79% accuracy respectively on chart hallucination benchmarks. Taxonomy covers value fabrication, trend misinterpretation, and other failure modes.

**Source:** https://arxiv.org/pdf/2509.17481

### 4b. CHART NOISe: VLM Responses Degrade on Imperfect Charts

**Finding:** VLMs exhibit systematic hallucination patterns including value fabrication and trend misinterpretation under degraded chart conditions (corruptions, occlusions).

**Source:** https://arxiv.org/pdf/2509.18425

### 4c. GPT-4V Foundation Model Assessment in Radiology (Radiology, 2024)

**Finding:** GPT-4V reliably identified imaging modality and anatomic region but could not safely detect, classify, or rule out abnormalities on single MRI, CT, and radiographic images. Tendency to overdiagnose (specificity 32.3%).

**Citation:** Published in *Radiology*, 2024. DOI: 10.1148/radiol.240955

**Source:** https://pubs.rsna.org/doi/full/10.1148/radiol.240955

---

## 5. Summary Table for Paper Use

| Domain | Incident/Study | Key Metric | Source |
|--------|---------------|------------|--------|
| Medical imaging | GPT-4V on radiology exams | 47.8% accuracy on image questions vs 81.5% text-only | Hayden et al., Radiology 2024 |
| Medical imaging | GPT-4V hidden flaws | 35.5% correct answers from wrong reasoning | npj Digital Medicine 2024 |
| Medical devices | FDA AI device recalls | 182 recall events across 60 devices | Healthcare Brew / PubMed 2025 |
| Autonomous driving | Tesla FSD visibility | 9 crashes, 1 fatal; cameras blinded by glare/fog | NHTSA EA26002, 2026 |
| Autonomous driving | Uber ATG fatal crash | 5 sec misclassification cycle; pedestrian killed | NTSB 2018 |
| Autonomous driving | Cruise dragging | Failed to detect person under vehicle | DOJ 2024 |
| Multimodal reasoning | Stanford AI Index | 50.1% on analog clocks vs near-expert on MMMU | Stanford HAI 2026 |
| Chart understanding | ChartHal benchmark | GPT-5: 34.46% accuracy on chart hallucination | arXiv 2025 |
| Chart understanding | CHART NOISe | Value fabrication under degraded conditions | arXiv 2025 |

---

## Suggested Paper Framing

These incidents collectively demonstrate that:

1. **Vision AI failures are not hypothetical** -- they have caused deaths (Uber, Tesla), injuries (Cruise), and diagnostic errors (FDA recalls).

2. **Overconfidence is the critical failure mode** -- systems that cannot express uncertainty (e.g., Tesla FSD not warning drivers when cameras are degraded) cause the worst outcomes.

3. **The jagged frontier means benchmark scores mislead** -- a model near expert-level on MMMU but at chance on analog clocks shows that aggregate benchmarks mask dangerous capability gaps.

4. **Chart/figure understanding is particularly brittle** -- ChartHal and CHART NOISe show that even frontier models hallucinate chart values, fabricate trends, and degrade sharply under visual noise.

5. **Our work directly addresses this gap** -- by evaluating VLMs on scientific figures under controlled degradation (selective blur), we measure exactly the kind of capability cliff that the Stanford AI Index warns about.
