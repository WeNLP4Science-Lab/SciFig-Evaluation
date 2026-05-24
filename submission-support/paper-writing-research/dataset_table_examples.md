# Dataset Table Design Patterns from Top Benchmark Papers

Research compiled from ACL, EMNLP, CVPR, ICLR 2023-2025 benchmark/evaluation papers.

---

## 1. HallusionBench (Guan et al., CVPR 2024) -- 346 images, 1129 questions

### Table 1: Benchmark Comparison (the "context" table)
- **Purpose:** Positions HallusionBench among existing VL benchmarks
- **Rows:** 9 benchmarks (Lynx-Bench, SciGraphQA, MathVista, MME, POPE, M-HalDetect, GAVIE, Bingo, HallusionBench)
- **Columns:** Benchmarks | Visual Format | # Total QA | # H-Edited QA | # Total Img. | # H-Edited Img. | Control Pair? | Purpose
- **Key pattern:** Comparison table as the FIRST table. Makes a small dataset (346 images) look significant by showing unique properties (human-edited, control pairs) that no other benchmark has.
- **Trick:** The "Control Pair?" and "Purpose" columns highlight what others lack, not just raw scale.

### Table 2: Correctness Leaderboard
- 15 models x 6 metrics (qAcc, fAcc, Easy/Hard/All accuracy)
- Shows model parameters alongside results

### Table 3: Analytical Evaluation
- 15 models x 8 diagnostic metrics (bias, consistency, language/vision diagnosis)
- Decomposes failures into interpretable categories

**Actionable insight:** With a small dataset, lead with a COMPARISON table showing qualitative uniqueness, not raw numbers. Show what dimensions you cover that others don't. Evaluation scale (model count x metrics) goes in separate results tables.

---

## 2. POPE (Li et al., EMNLP 2023) -- 500 images, 9000 questions

### Evaluation Setup (not a traditional dataset table)
- **Structure:** 3 sampling strategies (Random, Popular, Adversarial) x 500 images
- **Per strategy:** 1500 Yes + 1500 No questions = 3000 per strategy
- **Total:** 9000 question-answer pairs across 3 evaluation settings
- **Key pattern:** POPE does NOT have a complex dataset statistics table. Instead, the method IS the contribution -- the three sampling strategies are explained in prose and via figures, not a table.
- **Evaluation scale:** Results tables show 6+ models x 3 strategies x 3 metrics (Accuracy, Precision, Recall, F1)

**Actionable insight:** When the method/protocol is the contribution (not the raw data), explain the evaluation design through clear figures and prose rather than forcing it into a statistics table. The results tables implicitly convey scale through rows (models) x columns (conditions).

---

## 3. ChartQA (Masry et al., ACL Findings 2022) -- 4,804 charts, 32,701 questions

### Table 2: Dataset Statistics (per split)
- **Rows:** ChartQA-H (Human), ChartQA-M (Machine) -- just 2 main rows
- **Columns:** Split (Train/Val/Test) with sub-columns for # Charts and # QA pairs
- **ChartQA-H:** Train 3,699 charts / 7,398 QA | Val 480 / 960 | Test 625 / 1,250
- **ChartQA-M:** Larger numbers for machine-generated
- **Total human-written: 9,608 | Total machine-generated: 23,111**

### Table 3: Number of Charts from Each Source
- Rows: Different web sources (Statista, Pew, OECD, OWID, etc.)
- Shows provenance and diversity of data sources

**Actionable insight:** Separate human-curated vs. machine-generated clearly. Show train/val/test splits with both chart count AND question count (multiplier effect). Source diversity table adds perceived comprehensiveness.

---

## 4. MathVista (Lu et al., ICLR 2024) -- 6,141 examples from 31 sources

### Table 1: Key Statistics (the "dashboard" table)
- **Structure:** Simple 2-column table: Statistic | Number
- **13 rows of statistics:**
  - Total questions: 6,141
  - Multiple-choice questions: 3,392 (55.2%)
  - Free-form questions: 2,749 (44.8%)
  - Questions with annotations: 5,261 (85.6%)
  - Questions newly annotated: 736 (12.0%)
  - Unique images: 5,487
  - Unique questions: 4,746
  - Unique answers: 1,464
  - Source datasets: 31
  - Visual context classes: 19
  - Avg question length: 15.6
  - Avg answer length: 1.2
  - Avg choice number: 3.4

### Table 3: Mathematical Reasoning Type Breakdown
- 7 rows: Arithmetic (34.1%), Statistical (30.5%), Algebraic (28.5%), Geometry (23.3%), Numeric Common Sense (14.0%), Scientific (10.7%), Logical (3.8%)
- Note: percentages sum to >100% because examples can have multiple reasoning types

### Results Table: Massive multi-axis evaluation
- 47 rows (models grouped by type: baselines, LLMs, augmented LLMs, multimodal models, human)
- 13 columns: ALL + 5 task types (FQA, GPS, MWP, TQA, VQA) + 7 reasoning types

**Actionable insight:** The 2-column "Key Statistics" table is brilliant for making a modestly-sized dataset look rich. Including percentages, averages, and source counts in a single compact table conveys depth without needing massive raw numbers. The reasoning type breakdown with overlapping categories (>100% total) shows multi-dimensionality.

---

## 5. AppWorld (Trivedi et al., ACL 2024 Best Resource Paper) -- 750 tasks

### Benchmark Structure (multiple tables)
- **Scale metrics:** 9 apps, 457 APIs, ~100 simulated users, 60K lines of engine code
- **Task splits:** Train (105) | Dev (60) | Test-N (168) | Test-C (417) = 750 total
- **Task complexity stats:** Avg 1.8 apps per task (max 6), avg 9.5 APIs per task (max 26), avg 80+ lines of solution code
- **Comparison table:** Positions against other agent benchmarks on dimensions like: realistic environment, multi-app tasks, interactive execution, state-based evaluation

**Actionable insight:** AppWorld multiplies perceived scale by reporting: number of apps, number of APIs, number of users, lines of code, task complexity metrics. A 750-task benchmark sounds much bigger when you add "457 APIs" and "60K lines of engine code." Infrastructure scale complements task count.

---

## 6. Dolma (Soldaini et al., ACL 2024 Best Resource Paper) -- 3T tokens

### Table 1: Corpus At-a-Glance
- **Structure:** Source | Documents | Tokens (with LLaMA tokenizer)
- **Rows:** ~7 sources: Common Crawl (web), Semantic Scholar (scientific papers), GitHub (code), Project Gutenberg (books), Reddit (social media), Wikipedia + Wikibooks (encyclopedic)
- **Key numbers:** 200 TB raw text -> 11 TB curated -> 3T tokens
- **24 Common Crawl snapshots (2020-2023)**

**Actionable insight:** For corpus papers, show the pipeline compression: raw -> curated -> final. Multiple source categories with individual token counts. The "at-a-glance" framing makes a massive table feel approachable.

---

## 7. MMMU (Yue et al., CVPR 2024) -- 11,500 questions

### Dataset Taxonomy Table
- **Hierarchy:** 6 disciplines -> 30 subjects -> 183 subfields
- **Disciplines:** Art & Design, Business, Science, Health & Medicine, Humanities & Social Science, Tech & Engineering
- **Additional dimensions:** 30 image types, college-level difficulty
- **Splits:** dev (150) + validation (900) + test (10,500)

**Actionable insight:** Hierarchical taxonomy (discipline -> subject -> subfield) makes 11.5K questions span an impressive intellectual breadth. The 183 subfields number is more impressive than 11.5K questions.

---

## 8. MME (Fu et al., 2024) -- 14 subtasks

### No separate dataset statistics table
- **Structure:** Evaluation results ARE the main tables
- Table 1: 30 models x 7 perception subtasks (ACC and ACC+ per subtask)
- Table 2: 30 models x 7 cognition subtasks (ACC and ACC+ per subtask)
- The 14-subtask taxonomy is presented via figures and prose, not a statistics table

**Actionable insight:** When the benchmark is defined by evaluation dimensions rather than data volume, the results table IS the dataset table. 30 models x 14 subtasks x 2 metrics = 840 evaluation cells conveys scale.

---

## 9. FigureQA (Kahou et al., ICLR 2018) -- 100K+ images, 1M+ questions

### Dataset Split Table
- **Rows:** Training, Validation 1, Validation 2, Test 1, Test 2
- **Columns:** # Figures | # Questions
- Training: 100,000 figures / ~1.3M questions
- Each val/test: 20,000 figures / ~260K questions
- **5 figure types:** Line, dot-line, vertical bar, horizontal bar, pie chart
- **15 question templates**

**Actionable insight:** Multiple validation and test sets (with different color schemes) multiply the evaluation surface. Reporting both figure count AND question count (13x multiplier) makes scale obvious.

---

## 10. PlotQA (Methani et al., WACV 2020) -- 224K plots, 28.9M questions

### Comparison with Existing Datasets (Table 3)
- **Rows:** FigureQA, DVQA, PlotQA
- **Columns:** # Images | # QA pairs | Source | Answer type | # Unique answers | Real data? | Question length
- **Key differentiator:** Real-world data vs. synthetic, open vocabulary vs. fixed
- Shows orders of magnitude more questions (28.9M vs. 1M for FigureQA)

**Actionable insight:** The comparison table with both quantitative AND qualitative columns (real data?, answer type) lets you win on dimensions where you are strong.

---

## 11. Latxa (Etxaniz et al., ACL 2024 Best Resource Paper) -- Basque LLM

### Evaluation Suite Table
- **4 evaluation datasets with individual statistics:**
  - EusProficiency: 5,169 questions (official language proficiency exams)
  - EusReading: 352 reading comprehension questions
  - EusTrivia: 1,715 trivia questions across 5 knowledge areas
  - EusExams: 16,774 questions from public examinations
- **Model family:** 7B to 70B parameters
- **Pretraining corpus:** 4.3M documents, 4.2B tokens

**Actionable insight:** Breaking evaluation into named sub-benchmarks with distinct purposes makes a moderate evaluation suite feel comprehensive. Each sub-benchmark has a clear, memorable name.

---

## 12. Aya Model (Ustun et al., ACL 2024 Best Paper) -- 101 languages

### Scale Through Coverage
- **99 languages evaluated** (double the previous state of the art)
- **513M instruction instances** through templating + augmentation across 114 languages
- **65 languages** with human-curated data

**Actionable insight:** For multilingual work, the NUMBER OF LANGUAGES is the headline metric, not the number of examples per language. Coverage breadth beats depth.

---

# Synthesis: Actionable Patterns for Our SciFig Paper

## Pattern 1: The Comparison Table (most common, most effective)
Used by: HallusionBench, PlotQA, ChartQA, AppWorld
- **Structure:** Your benchmark as the last row, existing benchmarks above
- **Include qualitative columns** (e.g., "Multilingual?", "Human annotations?", "MQM framework?") where you uniquely check the box
- **This is THE table to lead with** for a small-to-medium dataset

## Pattern 2: The Key Statistics Dashboard
Used by: MathVista
- **2-column table:** Statistic | Value
- **Include counts, percentages, averages, unique counts**
- **Works well for datasets with many facets** but modest raw numbers
- 10-15 rows of diverse statistics make any dataset look multidimensional

## Pattern 3: The Multi-Axis Breakdown
Used by: MMMU, MathVista, Latxa
- Show dataset along MULTIPLE taxonomic axes (figure type, language, model family, evaluation dimension)
- **Each axis is a separate small table or figure**
- Readers remember the DIMENSIONALITY, not the absolute count

## Pattern 4: The Multiplier Effect
Used by: FigureQA, PlotQA, ChartQA, our paper
- Report evaluation scale as: figures x models x judges x metrics
- **1,005 figures x 11 models x 4 judges = 44,220 evaluations** (our case)
- This is standard practice and expected

## Pattern 5: The Infrastructure/Complexity Metrics
Used by: AppWorld, Dolma
- Report supporting infrastructure scale (lines of code, APIs, pipeline stages)
- Show data curation pipeline: raw -> filtered -> final
- **For our paper:** Could show annotation pipeline stages, inter-annotator agreement, MQM rubric complexity

## Pattern 6: Named Sub-Benchmarks
Used by: Latxa, MMMU, MathVista
- Give distinct names to evaluation subsets
- Each sub-benchmark has its own purpose and statistics
- **For our paper:** Could name adversarial evaluation subsets (e.g., "SciFig-Blur", "SciFig-Adversarial")

## Recommended Table Design for Our Paper

### Option A: Comparison Table (Table 1)
```
Benchmark      | Figures | Models | Languages | Eval Framework | Human Annot. | Adversarial | Multilingual
ChartQA        | 4,804   | --     | 1         | Accuracy       | Partial      | No          | No
FigureQA       | 140K    | --     | 1         | Accuracy       | No           | No          | No
POPE           | 500     | 6+     | 1         | Yes/No Acc     | No           | Yes         | No
HallusionBench | 346     | 15     | 1         | Acc + Diag     | Yes          | No          | No
SciGraphQA     | 295K    | --     | 1         | Open-vocab     | No           | No          | No
SciFig (Ours)  | 1,005   | 11     | 4         | MQM (1-5)      | Yes          | Yes         | Yes
```

### Option B: Key Statistics Dashboard (Table 1)
```
Statistic                          | Value
Total scientific figures           | 1,005
Languages                          | 4 (EN, DE, ZH, JA)
Vision-language models evaluated   | 11
LLM judges                        | 4
MQM evaluation dimensions         | 5
Total model evaluations            | 44,220
Human-annotated subset             | X figures
Adversarial test figures           | 45
Adversarial transforms             | 7
Figure source domains              | N
Average caption length             | X tokens
Inter-annotator agreement          | X (Cohen's kappa)
```

### Recommended: Use BOTH
- **Table 1:** Comparison table (positions us in the landscape)
- **Table 2:** Key statistics dashboard (shows depth and rigor)
- **Evaluation scale** (44K evaluations) goes in either Table 2 or in prose in the experimental setup

This two-table approach follows HallusionBench (comparison first) + MathVista (statistics dashboard) patterns, which are the most effective for medium-sized benchmarks.
