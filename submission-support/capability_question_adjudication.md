# Capability Question Adjudication: AI vs Human Comparison

Comparison of capability question answers across 3 AI adjudicators (Opus 4.6, Sonnet 4.6, Haiku 4.5) and human annotators for the sampled 100 figures.

## Methodology

- **Numeric answers**: Fuzzy match with 10% tolerance
- **Yes/No answers**: Exact match
- **Descriptive/text answers**: Skipped (too subjective for automated comparison)
- **GPT-5.2 ground truth** shown for reference where available

## Summary

| Category | Count | Description |
|----------|-------|-------------|
| **A** — Consensus | 82 | AI models agree with at least 1 human annotator |
| **B** — AI-only consensus | 74 | AI models agree with each other but disagree with ALL humans |
| **C** — AI disagreement | 36 | AI models disagree with each other |
| **D** — No human data | 0 | No human annotation available for comparison |
| **Skipped** | 208 | Descriptive answers or insufficient AI coverage |
| **Total comparable** | 192 | (A + B + C) |
| **Total** | 400 | All figure x category pairs |

### Agreement Rates (comparable cases only)

- AI-Human consensus rate: **42.7%** (82/192)
- AI-only consensus (disagree with humans): **38.5%** (74/192)
- AI internal disagreement: **18.8%** (36/192)

### Breakdown by Question Type

| Question Type | A (Consensus) | B (AI-only) | C (AI disagree) | D (No human) | Skipped |
|--------------|---------------|-------------|-----------------|--------------|---------|
| counting | 27 | 31 | 2 | 0 | 40 |
| computation | 6 | 29 | 24 | 0 | 41 |
| comparison | 25 | 12 | 3 | 0 | 60 |
| pattern_analysis | 24 | 2 | 7 | 0 | 67 |

---

## Category B: AI Models Agree But Disagree with ALL Humans

These cases warrant manual review — the AI adjudicators converged on an answer that differs from every human annotator.

| Figure | Category | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 | Human Answers | GPT-5.2 GT |
|--------|----------|----------|------------|-----------|---------------|------------|
| fig_002 | comparison | No. For SMAP, green (MADLLM) bar is ~93% and orange (MADLLM  | No. SMAP green bar is approximately 93%, and orange bar is a | No - SMAP green bar (~93%) is NOT more than twice the orange | Ananya: yes; John: yes | Yes |
| fig_011 | comparison | No. In 2017, IN (green) bar appears to be roughly 1 (right a | No. In 2017, IN bar is slightly above 10^1 (~12–13), and DE  | No - In 2017, IN (~12) is NOT more than twice DE (~10). Chec | Bana: Yes; John: Yes | No |
| fig_011 | computation | Approximately 900%. USA in 2016 is roughly 6-7 datasets. USA | ~900%. USA in 2016 ~6 datasets; USA in 2020 ~35–40 datasets. | 900% - Percentage increase for USA from 2016 to 2020. 2016 v | Bana: 401.19%; John: Eyeballing it should be about a 60% incr | 900 |
| fig_011 | counting | 2. Looking at each year and counting bars above 10^0 (i.e.,  | 2. Years where exactly three bars extend above the 10^0 (=1) | 2 years have exactly three bars with dataset counts above 10 | Bana: 0; John: 0 | 2 |
| fig_013 | computation | Approximately 0%. In the case category, mBERT-B2 and XLM-B2  | 0%. In the case category, mBERT-B2 reads ~12 and XLM-B2 read | 0% - Percentage difference between mBERT-B2 and XLM-B2 in 'c | Bana: 7.7%; John: Can't say the graph isn't that detailed | 0 |
| fig_013 | counting | 4. In the gender category, mBERT-B2 (~4.5) and XLM-B2 (~3.3) | 4. In the gender category: mBERT-B2 bar reads ~4.2 and XLM-B | 4 bars in 'gender' and 'number' categories exceed effect val | Bana: 10; John: I cant tell, the graph isn't that detail | 4 |
| fig_016 | counting | 6. Looking at bars above 20: IE-Indic has mBERT-L2 (~1), XLM | 6. Bars above 20: IE-Indic has mBERT-R2 (~20.5), XLM-R2 (~18 | 6 bars exceed effect value of 20. IE-Indic category has 3 ba | Bana: 12; John: 3 | 6 |
| fig_024 | computation | 9.74 percentage points. Ours PHEME = 89.84%, w/o text PHEME  | 9.74 percentage points difference (or ~12.14% relative diffe | 9.74% - Percentage difference between Ours (89.84%) and w/o  | Benedict: 11.4629; Wei: 12.16% | 12.14 |
| fig_027 | counting | 3. Years with total datasets exceeding 100: 2020 (~130), 202 | 3. Years with total datasets exceeding 100: 2020 (~130), 202 | 3 years exceed 100 total datasets: 2020 (~130), 2021 (~160), | Benedict: 2; Wei: 2 | 3 |
| fig_031 | comparison | Yes. Base MCQ Eval = 0.644. RMU Generation Eval = 0.106. Twi | Yes. Base in MCQ Eval = 0.644. RMU in Generation Eval = 0.10 | Yes - Base MCQ Eval (0.644) IS more than twice RMU Generatio | Wei: No | Yes |
| fig_031 | pattern_analysis | No, the proportional relationship is not consistent. In MCQ  | No, the proportional relationship is not consistent. In MCQ  | No - The proportional relationship is NOT consistent. MCQ Ev | Wei: Yes, they are both less than half of the | No, the proportional relationship changes: RMU is approximat |
| fig_033 | comparison | No. For LC AlpacaEval-2, blue bar is ~23% and orange bar is  | No. LC AlpacaEval-2: blue bar ~23%, orange bar ~31%. Differe | No - LC AlpacaEval-2 orange bar (~30%) is NOT more than 20%  | Wei: Yes | No |
| fig_034 | counting | 1 text type category (Narrative) has both bars below 90: Ope | - | 1 | Wei: Open has 4 and Cons. has 1 | 1 |
| fig_037 | counting | 4 mBERT bars have task counts less than 5: IE-Germanic (~4), | - | 4 | Wei: 10 | 4 |
| fig_038 | comparison | Yes, the Correct bar at 0 shots (~0.72) is more than twice t | - | Yes, the 'Correct' value at 0 shots (approximately 0.7) is m | Wei: No | Yes, the 'Correct' value at 0 shots (approximately 0.7) is m |
| fig_038 | counting | 2 categories have Correct-Incorrect difference greater than  | - | 2 | Wei: 0 | 2 |
| fig_042 | counting | 6 bars have height greater than 20: NoR QA for 2WikiMQA (29) | - | 6 | Benedict: 5 | 6 |
| fig_045 | counting | 3 bars have a Demonstration (blue) segment taller than 500 t | - | 3 | Benedict: 1 | 3 |
| fig_051 | computation | The difference between ClInGS's average (59) and the average | ClInGS scores 58; the average of the other four (52+53+51+53 | - | Benedict: 150 | 6 |
| fig_051 | counting | 3 bars have average performance within 1 unit of 52: Standar | 3 bars (Standard ~52, FactTune ~51, ClInGS w/ ~53) fall with | - | Benedict: 4 | 3 |
| fig_057 | computation | The percentage difference between chLSTM (~79) and XLM-R (~5 | chLSTM T ≈ 79, XLM-R T ≈ 55; percentage difference = ((79−55 | - | Anthony: 35.82% | 33.33 |
| fig_061 | computation | The percentage difference between Baseline (~4.67) and Direc | Claude Baseline ≈4.7, Direct Command ≈4.95; difference = 0.2 | - | Anthony: 8.69% | 10% |
| fig_061 | counting | 3 bars have entropy values between 4.9 and 5.1: the Direct C | 3 bars (Direct Command bars for GPT-4, Claude, and Llama) ha | - | Anthony: 7 | 3 |
| fig_061 | pattern_analysis | No, there is no symmetry; Baseline values are consistently l | No symmetry; the 'Source Info' (yellow) bars are consistentl | - | Anthony: Yes | No, there is asymmetry; the 'Baseline' values are consistent |
| fig_063 | computation | The percentage difference between CoT (91.19%) and CoD (80.8 | Highest accuracy CoT = 91.19%, lowest CoD = 80.89%; percenta | - | Anthony: 11.97 | 12.73 |
| fig_064 | comparison | Yes, the Yes bar for Academic Funding (~65) is more than twi | Yes — Academic Funding 'Yes' bar extends past 65, while Recr | - | Anthony: No | Yes |
| fig_064 | computation | The difference between the average No (~5.75) and average Pa | 'No' averages: (6+6+5+6)/4 = 5.75; 'Partially' averages: (25 | - | Anthony: 82 | 18.25 |
| fig_064 | counting | 2 categories have Partially (yellow) bars exceeding 20 conve | 2 'Partially' bars exceed 20 conversations: Recruitment (~24 | - | Anthony: 3 | 2 |
| fig_067 | computation | The ratio of XLM-R (0.21) to mBERT (0.09) in hidden:[] linea | XLM-R 'hidden:[], linear' ≈ 0.21, mBERT ≈ 0.09; ratio = 0.21 | - | Anthony: 93.3% | 2.33 |
| fig_069 | computation | The percentage difference between RedWhale (0.57) and EEVE-K | RedWhale AVG = 0.57, EEVE AVG = 0.61; percentage difference  | - | Anthony: 6.5% | 6.56 |
| fig_069 | counting | 8 bars have values greater than 0.7: all 6 SOLAR-10.7B-v1.0  | 8 bars exceed 0.7: KoBEST-CP (RedWhale 0.71, EEVE 0.74), KoB | - | Anthony: 9 | 8 |
| fig_073 | computation | The percentage increase in STS Correlation from Single-task_ | Single-task_baseline STS Corr. ≈ 0.50, Supervised_SimCSE STS | - | Dan: 81.3% | 50 |
| fig_073 | counting | 3 models have at least one metric below 0.6: Single-task_bas | 3 models have at least one metric below 0.6: Single-task_bas | - | Dan: 2 | 3 |
| fig_075 | computation | The total runtime of all models is 77 + 190 + 365 + 172 + 24 | Total runtime = 77+190+365+172+243 = 1047 seconds; twice Dee | - | Dan: The total runtime is 1027 and that is ov | 1047 |
| fig_079 | counting | 3 bars are within 0.00010 of 0.00300: Remove Spacing NESAC ( | 3 bars fall within 0.00010 of 0.00300: Remove Spacing NESAC  | - | Dan: 2 | 3 |
| fig_080 | computation | The average ratio for Llama3 across all categories is approx | Llama3 values: Movies ~90%, Songs ~84%, Basketball ~67%; ave | - | Dan: 81% | 80.33 |
| fig_083 | computation | The average height across all bars in all five distributions | Average bar height across all five distributions is approxim | - | Dan: 2.5 | 3 |
| fig_090 | computation | The percentage difference in execution accuracy between NatS | NatSQL Moderate = 39.64, TA-SQL Moderate = 48.60; percentage | - | Dan: 22.6% | 22.6 |
| fig_092 | computation | The difference between the sum of blue bars (0.29+0.17+0.23= | Sum of blue bars ≈ 0.29+0.17+0.24 = 0.70; orange bar 'Ours'  | - | Bana: 0.34 | 0.33 |
| fig_098 | comparison | Yes, (0,90] (~600) is more than 1.1 times (90,180] (~567), s | Yes — (0,90] (~601) appears greater than 1.1 × (90,180] (~56 | - | Bana: No | Yes |
| fig_098 | computation | The percentage difference between (0,90] (~600) and (360,450 | (0,90] ≈ 600, (360,450] ≈ 590; percentage difference = ((600 | - | Bana: 1.67% | Approximately 9.09 |
| fig_098 | counting | 1 bar has error bars extending below 500: the (0,90] group,  | 1 bar — (0,90] — has an error bar extending below 500. | - | Bana: 0 | 1 |
| fig_102 | computation | The average training loss of ChemLLaMA Medium 20M between st | The average training loss for ChemLLaMA Medium 20M between s | - | Ananya: 0.05; John: graph isn't detailed enough for that val | 0.02 |
| fig_102 | counting | 5 lines have training loss below 0.1 at the 440k step. | 5 lines (ChemBART Small, ChemBART Medium, ChemBERTa Medium,  | - | Ananya: 6; John: 3 | 5 |
| fig_103 | counting | 4 data points have MRR@10 greater than 35.5, from the DPR w/ | 4 data points exceed MRR@10 = 35.5: DPR w/ top-1 has 2 point | - | Ananya: 16; John: 2 | 4 |
| fig_104 | computation | The average relative change for RULER4k of 1x tokens,16-bit  | The average relative change for RULER4k 1×tokens,16-bit acro | - | Ananya: -10.375%; John: Not detailed enough | -12.0 |
| fig_105 | computation | The percentage decrease in Ex1 Validation Loss from step 0 t | The percentage decrease in Ex1 Validation Loss from step 0 ( | - | Ananya: 36% | 72.73 |
| fig_109 | comparison | Yes, ROME's accuracy increase (~10%) from 10^1 to 10^3 is mo | Yes — ROME increases by ~8 percentage points (75%→83%) and B | - | Bana: No | Yes, ROME's accuracy increased by approximately 8%, which is |
| fig_113 | computation | The percentage difference between SepLLM (n=64) and SepLLM ( | The percentage difference in loss ratio between SepLLM (n=64 | - | Bana: 1.16; John: 1% | 1 |
| fig_113 | counting | 1 intersection occurs between the red (SepLLM n=64, H/T) and | 1 intersection: the red line (SepLLM n=64, H/T) crosses the  | - | Bana: 0; John: None | 1 |
| fig_122 | comparison | For w/o Attention, Precision (64.06) is closer to F1-score ( | For w/o Attention, Precision (64.06) is closer to F1-score ( | - | Benedict: F1-score value; Wei: F1-score | F1-score |
| fig_122 | computation | The percentage difference in Recall between Full model (65.7 | The percentage difference in Recall between Full model (65.7 | - | Benedict: 9.7911%; Wei: 15.77% | 13.96 |
| fig_123 | comparison | At all three time points (50k, 150k, 250k seconds), Vanilla  | At all three time points (50k, 150k, 250k seconds), Vanilla  | - | Benedict: Vanilla(at 50,000), SepLLM(at 50,000),Va; Wei: 2.62, 2.61, 2.545, 2.53, 2.50, 2.49 | At 50,000 seconds: Vanilla > SepLLM. At 150,000 seconds: Van |
| fig_123 | counting | 8 circular markers on the SepLLM (red) line are below the lo | 8 circular markers on the red SepLLM line fall below loss 2. | - | Benedict: 7; Wei: 7 | 8 |
| fig_125 | counting | 4 lines cross the y-axis value of 5.0: Intent, Translation,  | 4 lines cross y=5.0: Intent (orange), Translation (purple),  | - | Benedict: 6; Wei: 6 | 4 |
| fig_126 | computation | The percentage difference in accuracy between GPT-4o (31.1%) | The percentage difference between GPT-4o (31.1%) and Claude- | - | Benedict: 43.4442; Wei: 55.5% | 55.5 |
| fig_126 | counting | 3 data points have accuracy above 30%: GPT-4o at widths 3 (2 | 3 data points exceed 30% accuracy: GPT-4o at tree width 5 (3 | - | Benedict: 2; Wei: 2 | 3 |
| fig_130 | counting | The line in the top plot crosses the c-a-s dashed line 2 tim | The black solid line in the top plot crosses the 'c-a-s' das | - | Benedict: 8; Wei: 8 | 2 |
| fig_136 | computation | The ratio of maximum Delta Accuracy (~0.28 at 0.86) to minim | The ratio of maximum Δ Accuracy (~0.29 at 0.86) to minimum Δ | - | Wei: 5.8 | 3.0 |
| fig_136 | counting | 6 data points on the Initial Accuracy (green) line have accu | 6 data points on the green Initial Accuracy line exceed 0.8, | - | Wei: 9 | 6 |
| fig_137 | computation | The percentage difference between attn_residual (~1400) and  | The percentage difference between attn_residual (~1400) and  | - | Wei: 100% | 40 |
| fig_137 | counting | 4 layers (0, 1, 2, and 3) have all four lines at a maximum a | 4 layers (0, 1, 2, 3) have all four lines at a maximum activ | - | Wei: 5 | 4 |
| fig_138 | computation | The average difference between Final Accuracy and Initial Ac | The average difference between Final Accuracy and Initial Ac | - | Wei: 0.25 | 0.35 |
| fig_138 | counting | 5 data points on the Initial Accuracy (green) line have erro | 5 data points on the green Initial Accuracy line have error  | - | Wei: 6 | 5 |
| fig_139 | comparison | Yes, the random line at Estadio (~0.93) is more than twice t | Yes — at 'Estadio' the random (orange) line is ~0.93 and at  | - | Wei: No | Yes |
| fig_139 | counting | 2 intersections occur between the random (orange) and end (p | 2 intersections occur between the 'random' and 'end' lines:  | - | Wei: 3 | 2 |
| fig_142 | computation | The percentage increase in hidden state mean before gate fro | Hidden state mean before gate increases from ~0.05 at layer  | - | Benedict: 46900% | 9500 |
| fig_142 | counting | 1 layer (layer 0) has all three lines below 0.1. | 1 layer (layer 0) has all three lines below 0.1. | - | Benedict: 4 | 1 |
| fig_144 | counting | 2 lines peak at K=32: TACRED (blue) and TACRED-Revisit (oran | 2 lines reach their peak Micro F1 at K=32: TACRED (blue, ~30 | - | Benedict: 3 | 2 |
| fig_145 | computation | The difference between peak Library Documentation (~33 at x= | Peak of Library Documentation (~32 at x=500 or 800) minus lo | - | Benedict: 9 | 9 |
| fig_145 | counting | 1 intersection occurs, where StackOverflow posts (yellow) cr | 1 intersection: StackOverflow posts (yellow) crosses Github  | - | Benedict: 4 | 1 |
| fig_147 | comparison | No, at step 60,000, Ex1 (~0.41) is not more than 1.1 times E | No — at step 60,000 Ex1 is ~0.41 and Ex2 is ~0.385; 1.1×0.38 | - | Benedict: yes | No |
| fig_147 | computation | The percentage increase in Ex1 Accuracy from step 0 (~0.09)  | Ex1 Accuracy rises from ~0.095 at step 0 to ~0.395 at step 1 | - | Benedict: 300% | 300 |
| fig_147 | counting | 5 data points on the Ex1 Accuracy line have accuracy above 0 | 5 data points on Ex1 Accuracy (blue line) are above 0.35: at | - | Benedict: 10 | 5 |

---

## Category C: AI Models Disagree with Each Other

These cases show where the AI adjudicators gave conflicting answers.

| Figure | Category | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 | Disagreeing Pairs | Human Answers | GPT-5.2 GT |
|--------|----------|----------|------------|-----------|-------------------|---------------|------------|
| fig_002 | pattern_analysis | Yes, the SMAP dataset shows a pattern where the green bar (M | No clear bimodal distribution. SMAP shows one dominant bar ( | Yes, SMAP exhibits a bimodal-like distribution with the gree | opus vs sonnet, sonnet vs haiku | Ananya: Yes, in SWaT dataset green & p; John: No | Yes, the SMAP dataset exhibits a bimodal distribution, where |
| fig_009 | pattern_analysis | The distribution is asymmetric. For the +SFT on D0,D1,D2 con | Asymmetric. The +SFT on D0, D1, D2 (pink) bars are: LLaMA-2- | Asymmetric - LLAMA-2-7B and LLAMA-2-13B show slightly higher | opus vs haiku, sonnet vs haiku | Bana: asymmetric | The performance distribution is asymmetric, with LLAMA-2-7B  |
| fig_010 | computation | Approximately 47.7%. The percentage difference between Ambig | 91.3%. Ambiguity Std 0.0 = 0.88, Ambiguity Std 0.47 = 0.46.  | 91.3% - Percentage difference between Ambiguity Std 0.0 (0.8 | opus vs sonnet, opus vs haiku | Bana: 47.73; John: 0.42 | 91.3 |
| fig_024 | counting | 3. Bars with accuracy between 87% and 89% inclusive: PHEME:  | 3. Bars between 87% and 89% inclusive: PHEME: w/o emotion =  | 4 bars between 87% and 89% accuracy (inclusive). PHEME: w/o  | opus vs haiku, sonnet vs haiku | Benedict: 4; Wei: 4 | 4 |
| fig_024 | pattern_analysis | Yes, they do form a descending pattern in the PHEME dataset. | No. The values are: w/o select = 88.80%, w/o emotion = 87.34 | Mostly descending - w/o select (88.80%), w/o emotion (87.34% | opus vs sonnet | Benedict: Yes; Wei: Yes | No |
| fig_031 | computation | Approximately 16.3%. Base MCQ Eval = 0.644, RMU with Enhance | 19.5%. Base MCQ Eval = 0.644, RMU with Enhanced GCG MCQ Eval | 19.5% - Percentage difference between Base (0.644) and RMU w | opus vs sonnet, opus vs haiku | Wei: 19.48% | 19.5 |
| fig_033 | computation | Approximately 35. Differences per dataset: GSM-8K (80 vs 81, | ~35. Reading approximate scores: GSM-8K (blue 80, orange 80, | 28 - Total score difference between models across all datase | opus vs haiku, sonnet vs haiku | Wei: 45% | 35 |
| fig_034 | comparison | No, Cons. in Expository (130) is not more than twice Open in | - | Yes | opus vs haiku | Wei: No | Yes |
| fig_034 | computation | The percentage difference between Cons. (130) and Open (62)  | - | 109.68 | opus vs haiku | Wei: 109.68% | 109.68 |
| fig_037 | computation | In IE-Slavic, same (~28) as a percentage of total (mBERT ~12 | - | 50 | opus vs haiku | Wei: 35% | 50 |
| fig_038 | computation | Total difference across all shots: (0.31) + (0.30) + (0.28)  | - | 1.55 | opus vs haiku | Wei: 1.3 | 1.55 |
| fig_042 | computation | The percentage difference between OneR QA (27) and IRCoT QA  | - | 17.39 | opus vs haiku | Benedict: 19.6078 | 17.39 |
| fig_043 | computation | If Filters and Veracity Explanation doubled (each from 1 to  | - | 23 | opus vs haiku | Benedict: 23 | 23 |
| fig_045 | computation | The percentage decrease from 0 shots (6393) to 3 shots (6393 | - | 16.27 | opus vs haiku | Benedict: 16.2678 | 16.27 |
| fig_052 | computation | The difference between the Acc=0 & GT Ans (~30) and Acc=1 &  | The 'Acc=1 & GT Ans' segment for ChatGPT in Songs is ~50 and | - | opus vs sonnet | Benedict: 14 | 20 |
| fig_052 | counting | 6 bars exceed 100 in popularity, all located in the Basketba | All 9 bars in the Basketball group exceed 100, while Movies  | - | opus vs sonnet | Benedict: 8 | 6 |
| fig_053 | computation | The percentage increase from base (~87) to large (~89) for S | S5-model base ≈87.0, large ≈89.0; percentage increase = (2/8 | - | opus vs sonnet | Anthony: 2.29% | 2.33 |
| fig_074 | computation | The difference between the IE average (~37.5) and non-IE ave | IE average: (79+47+44+17+15+12)/6 ≈ 35.7; non-IE average: (2 | - | opus vs sonnet | Dan: 21.4 | 25.0 |
| fig_079 | computation | The total absolute difference in WER between NESAC and SESHA | Summing absolute differences per category: |0.00334−0.00323| | - | opus vs sonnet | Dan: 0.00165 | 0.00049 |
| fig_085 | computation | The average MMAU (~60%) minus the average MMAR (~37%) gives  | MMAU average: (50+61+65)/3 ≈ 58.7%; MMAR average: (30+37+57) | - | opus vs sonnet | Dan: 23.33% | 30 |
| fig_091 | computation | The percentage increase from TEXTBLOB (~0.30) to ChatGPT (~0 | ChatGPT Emoji Tweets ≈ 0.68, TEXTBLOB ≈ 0.33; percentage inc | - | opus vs sonnet | Dan: 116.67% | 116.67 |
| fig_103 | computation | The percentage increase in MRR@10 for DPR w/ top-1 from S=2  | The percentage increase for DPR w/ top-1 from S=2 to S=10 is | - | opus vs sonnet | Ananya: S=2: ~34.7 S=10: ~36.4  % incr; John: 10.61% | 5.5 |
| fig_109 | computation | The difference between the ACC ranges of MEMIT and IKE is ap | The ACC range for MEMIT (78%−70% = 8%) minus ACC range for I | - | opus vs sonnet | Bana: 1 | 3 |
| fig_112 | computation | The percentage decrease in Vanilla loss from 0 to 140,000 it | Vanilla decreases from ~3.42 to ~2.45, a percentage decrease | - | opus vs sonnet | Bana: undefined; John: No image | 28.26 |
| fig_113 | comparison | SepLLM (n=64, H) has a slightly higher loss ratio by approxi | At 5e8 TFLOPs, SepLLM (n=64, H) is slightly above 100% and S | - | opus vs sonnet | Bana: At 5e8 they have identical los; John: 1,5% | SepLLM (n=64, H) has a higher loss ratio by approximately 0. |
| fig_115 | computation | The pink line (en&bn) drops by approximately 0.08 from layer | The pink line drops from ~0.13 at Layer 6 to ~0.05 at Layer  | - | opus vs sonnet | Bana: Similarity for the pink line (; John: No image | The pink line drops by 0.08, and the green line drops by 0.1 |
| fig_122 | pattern_analysis | Recall demonstrates the steepest overall decline from Full m | Recall demonstrates the steepest overall decline from Full m | - | opus vs sonnet | Benedict: Recall; Wei: Recall. F1-score declines slig | Recall demonstrates the steepest overall decline, dropping f |
| fig_123 | computation | The average loss reduction per 50,000 seconds for SepLLM is  | SepLLM reduces loss from ~2.75 to ~2.48 over 250,000 s; aver | - | opus vs sonnet | Benedict: 0.052; Wei: 0.056 | 0.057 |
| fig_124 | computation | The difference in rate of ACC increase per logarithmic step  | IKE rate ≈ (69−64)/3 = 1.67%/step; MEND rate ≈ (73−66)/3 = 2 | - | opus vs sonnet | Benedict: 0.5; Wei: 2.1% | 1.5 |
| fig_125 | computation | The percentage increase in Intent from 2^9 (~3.8) to 2^20 (~ | Intent increases from ~3.7 at 2⁹ to ~6.0 at 2²⁰, a percentag | - | opus vs sonnet | Benedict: 62.1622; Wei: 58% | 62.16 |
| fig_126 | comparison | GPT-4o shows a greater increase of 5.5% (28.9 to 34.4) betwe | Between widths 3 and 5, GPT-4o increases by +5.5 points (28. | - | opus vs sonnet | Benedict: GPT-4o. It increases by 5.5; Wei: GPT-4o with 9% | GPT-4o shows a greater increase in accuracy, with an increas |
| fig_136 | pattern_analysis | The Initial Accuracy (green) line exhibits a non-monotonic t | The green line (Initial Accuracy) exhibits a non-monotonic t | - | opus vs sonnet | Wei: orange dashed line | The green line (Initial Accuracy) exhibits a non-monotonic t |
| fig_139 | computation | The average ASR for the start line across all categories is  | The average ASR for the 'start' (green) line across all 8 ca | - | opus vs sonnet | Wei: 0.81 | 0.78 |
| fig_144 | computation | The percentage difference between SemEval (~51%) and TACRED  | At K=64, SemEval is ~52% and TACRED is ~29.5%; percentage di | - | opus vs sonnet | Benedict: 58.5366% | 25 |
| fig_144 | pattern_analysis | Re-TACRED shows the fastest rate of increase between K=8 and | Re-TACRED (green line) shows the fastest rate of increase in | - | opus vs sonnet | Benedict: Re-TACRED | Re-TACRED |
| fig_145 | pattern_analysis | StackOverflow posts (yellow) exhibits a strongly non-monoton | The red line (Library Documentation) exhibits a non-monotoni | - | opus vs sonnet | Benedict: Library documentation. X = 800 | The red line (Library Documentation) exhibits a non-monotoni |

---

## Category A: Consensus Cases (AI + Human Agreement)

These cases show strong agreement. Listed for completeness.

| Figure | Category | AI Answer (representative) | Matching Human |
|--------|----------|---------------------------|----------------|
| fig_002 | computation | Approximately 74.2%. MADLLM w/o prompt pool (blue bars): SMD | Ananya |
| fig_002 | counting | 10. Bars above 90%: SMD has 3 (green ~93, purple ~92, orange | Ananya, John |
| fig_009 | comparison | LLAMA-2-7B has the smallest difference (approximately 0%). T | Bana, John |
| fig_009 | computation | Approximately 76%. LLaMA-2-13B values: no SFT ~70, +SFT on D | Bana, John |
| fig_009 | counting | 5. Bars above 80%: LLaMA-2-7B has purple (~81) and peach (~8 | John |
| fig_010 | comparison | No. Ambiguity Std 0.0 has value 0.88. Max Ambiguity 2 has va | Bana, John |
| fig_010 | counting | 2. In the left chart, only the bar at Ambiguity Std 0.0 (val | Bana, John |
| fig_010 | pattern_analysis | Yes, the Fleiss Kappa values generally decrease as ambiguity | John |
| fig_013 | comparison | mBERT-B2 > XLM-B2 > mBERT-L2 > XLM-L2 > mBERT-R2 > XLM-R2. I | John |
| fig_013 | pattern_analysis | No, there is no consistent ordering of bar heights across al | John |
| fig_016 | computation | Approximately 15.7%. mBERT-B2 values: IE-Baltic ~5, IE-Germa | Bana, John |
| fig_024 | comparison | No. Ours PolitiFact = 90.57%. w/o text PHEME = 80.10%. Twice | Benedict, Wei |
| fig_027 | computation | Approximately 29 datasets/year. Total in 2016 ~14, total in  | Benedict, Wei |
| fig_027 | pattern_analysis | The proportions change over time. In earlier years (2012-201 | Wei |
| fig_031 | counting | 3. Bars with accuracy > 0.5: Base in MCQ Eval (0.644), Base  | Wei |
| fig_033 | counting | 2. Datasets with at least one model scoring below 30%: LC Al | Wei |
| fig_043 | counting | 4 criteria have >= 3 participants: Relevant FCs (6), FC Summ | Benedict |
| fig_043 | pattern_analysis | Yes, the bar heights follow a monotonic non-increasing patte | Benedict |
| fig_045 | comparison | No, the total for 3 shots (~5353) is not more than twice the | Benedict |
| fig_051 | comparison | No, ClInGS (~59) is not more than twice FactTune (~52), sinc | Benedict |
| fig_051 | pattern_analysis | No, the bar heights do not follow a monotonic pattern; they  | Benedict |
| fig_052 | pattern_analysis | Yes, popularity increases monotonically from Movies to Songs | Benedict |
| fig_053 | comparison | Prefix shows the smallest performance gap between base and l | Anthony |
| fig_053 | counting | 3 bars represent GLUE performance greater than 88: the large | Anthony |
| fig_053 | pattern_analysis | Yes, the large model consistently outperforms the base model | Anthony |
| fig_057 | comparison | XLM-R has a slightly higher Shapley value than mBERT in cate | Anthony |
| fig_057 | counting | 3 bars have Shapley values greater than 40: mBERT (~59), XLM | Anthony |
| fig_057 | pattern_analysis | Yes, there is approximate symmetry between left-side and rig | Anthony |
| fig_061 | comparison | No, GPT-4 Direct Command (~5.05) is not more than twice Llam | Anthony |
| fig_063 | counting | 3 categories have accuracy above 85%: CoT (91.19%), CCoT (88 | Anthony |
| fig_063 | pattern_analysis | No, there is no consistent ordering; CoT has the highest tok | Anthony |
| fig_067 | comparison | Yes, the mBERT bar in hidden:[50] linear (~-0.05) is more th | Anthony |
| fig_067 | counting | 2 bars are within 0.05 of the zero line: XLM-R in hidden:[10 | Anthony |
| fig_067 | pattern_analysis | No, XLM-R's bar heights are non-monotonic, going from negati | Anthony |
| fig_069 | pattern_analysis | Non-monotonic pattern; RedWhale values rise from PT-EVAL (0. | Anthony |
| fig_073 | pattern_analysis | No, the ordering of the three metrics is not consistent acro | Dan |
| fig_074 | comparison | Yes, IE-Slavic (~79) is more than twice the combined Semitic | Dan |
| fig_074 | counting | 4 linguistic families have bars exceeding 20 tasks: IE-Slavi | Dan |
| fig_075 | counting | 2 models have runtime greater than 200 seconds: DeepSeek (36 | Dan |
| fig_079 | pattern_analysis | No, the NESAC ft model values do not follow a monotonic patt | Dan |
| fig_080 | comparison | No, Llama3's ratio (67%) in Basketball is not more than twic | Dan |
| fig_080 | counting | 2 categories have at least one bar above 85%: Movies (Llama3 | Dan |
| fig_080 | pattern_analysis | No, Qwen2 ratios do not follow a monotonic pattern: 90% (Mov | Dan |
| fig_083 | counting | 2 bars across all distributions are taller than the tallest  | Dan |
| fig_085 | comparison | Yes, MMAU in Audio-Reasoner (~63%) is more than twice MMAR i | Dan |
| fig_085 | counting | 2 bars are within 5% of the 65% mark: MMAU for Audio-Reasone | Dan |
| fig_090 | counting | 4 bars have execution accuracy greater than 50: NatSQL Simpl | Dan |
| fig_091 | comparison | Yes, ChatGPT's Overall Tweet accuracy (~0.65) is more than 1 | Dan |
| fig_091 | counting | 2 bars have accuracy greater than 0.5: ChatGPT in both Emoji | Dan |
| fig_092 | comparison | Yes, Ours (0.35) is more than twice -scoring (0.17), since 0 | Bana |
| fig_092 | counting | 3 blue bars have Recall@10 values below 0.3: -critiquing (~0 | Bana |
| fig_092 | pattern_analysis | No, the distribution is non-monotonic; heights go from 0.35  | Bana |
| fig_094 | computation | The ratio of Other in Ours (7.7%) to Other in Standard (25.3 | Bana |
| fig_094 | counting | 3 segments across both bars represent percentages greater th | Bana |
| fig_094 | pattern_analysis | Yes, the Ours bar shows a monotonic decrease from left to ri | Bana |
| fig_101 | comparison | No, SepLLM (n=64, H/T) at iteration 40,000 has a loss of app | Ananya, John |
| fig_101 | computation | The difference in loss reduction is approximately 0.10 (SepL | Ananya |
| fig_101 | counting | 5 lines cross the loss value of 2.8 (Vanilla, StrmLLM n=64,  | John |
| fig_102 | comparison | ChemLLaMA Medium 20M decreases more steeply between step 0 a | John |
| fig_102 | pattern_analysis | ChemBERTa Small 20M shows the slowest rate of decrease betwe | Ananya, John |
| fig_103 | comparison | No, the MRR@10 of DPR w/ top-1 at x=10 (~36.5) does not exce | Ananya, John |
| fig_103 | pattern_analysis | DPR w/ top-1 demonstrates the fastest rate of increase betwe | Ananya |
| fig_104 | comparison | RULER4k of 1x tokens,16-bit shows a larger recovery from Lay | Ananya, John |
| fig_104 | counting | 2 lines dip below -10%: RULER4k of 1x tokens,16-bit (to ~-25 | Ananya, John |
| fig_104 | pattern_analysis | RULER4k of 1x tokens,16-bit (dark blue) exhibits the most pr | Ananya |
| fig_105 | comparison | Yes, the initial Ex1 Validation Loss (~11) is more than twic | Ananya, John |
| fig_105 | counting | 4 data points have loss values greater than 6x10^0, from the | John |
| fig_109 | counting | 3 methods achieve at least 75% ACC at 10^3: ROME (~85%), MEN | Bana |
| fig_112 | comparison | No, StrmLLM (n=64) at 80,000 (~2.68) is not more than twice  | Bana, John |
| fig_112 | counting | 2 lines have final loss below 2.5 at 140,000 iterations: Sep | Bana |
| fig_113 | pattern_analysis | SepLLM (n=64, H/T) (red line) shows the fastest initial incr | Bana, John |
| fig_115 | counting | 1 intersection occurs between the green (en&el) and pink (en | Bana |
| fig_122 | counting | 5 data points have values above 64%: Precision at Full model | Benedict, Wei |
| fig_123 | pattern_analysis | SepLLM decreases faster than Vanilla in the first 50,000 sec | Benedict |
| fig_124 | comparison | No, ROME (~72%) at 10^1 is not more than twice Base (~61%). | Benedict, Wei |
| fig_124 | counting | 4 lines cross the 70% threshold: ROME, MEND, MEMIT, and IKE. | Benedict, Wei |
| fig_125 | comparison | No, Code (~5.8) at 2^20 is not more than twice Summary (~5.8 | Benedict, Wei |
| fig_126 | pattern_analysis | GPT-4o exhibits a faster rate of change between widths 3 and | Benedict, Wei |
| fig_130 | comparison | No, the ratio of the peak c to w+a+s in the bottom plot is n | Benedict, Wei |
| fig_137 | pattern_analysis | The attn_output (blue dashed) line remains flat near zero ac | Wei |
| fig_144 | comparison | Yes, Re-TACRED at K=32 (~50.5%) is more than twice TACRED at | Benedict |
| fig_147 | pattern_analysis | Ex1 Accuracy increases more sharply than Ex2 Accuracy during | Benedict |

---

## Category D: No Human Annotation Available

Total: 0 figure x category pairs had no human annotation for comparison.

---

## Skipped Cases

Total: 208 cases skipped.

| Reason | Count |
|--------|-------|
| only 1 AI answers | 160 |
| AI-human not comparable (descriptive) | 30 |
| all descriptive | 18 |
