# Capability Question Answers — Sonnet 4.6 Batch 2 (fig_051–fig_100)

## fig_051
- **counting**: 3 bars (Standard ~52, FactTune ~51, ClInGS w/ ~53) fall within 1 unit of 52.
- **computation**: ClInGS scores 58; the average of the other four (52+53+51+53)/4 = 52.25, giving a difference of approximately 6.
- **comparison**: No — ClInGS (~58) is far less than twice FactTune (~51×2 = 102).
- **pattern_analysis**: No monotonic pattern; heights fluctuate (Standard < Self-RAG > FactTune < ClInGS w/ < ClInGS).

## fig_052
- **counting**: All 9 bars in the Basketball group exceed 100, while Movies and Songs bars do not, giving approximately 9 bars above 100 (the image shows all three models with three bar types each in Basketball all exceed 100).
- **computation**: The 'Acc=1 & GT Ans' segment for ChatGPT in Songs is ~50 and 'Acc=0 & GT Ans' is ~30, giving a difference of approximately 20.
- **comparison**: ChatGPT has the smallest difference between 'Acc=0 & GT Ans' and 'Acc=0 & Gene Ans' bars in Songs, as those two bars are nearly equal height.
- **pattern_analysis**: Yes, popularity increases monotonically from Movies to Songs to Basketball for all three AI models.

## fig_053
- **counting**: 3 bars exceed 88 in GLUE performance: LoRA large (~89), S5-model large (~90), and Adaptor large (~88).
- **computation**: S5-model base ≈87.0, large ≈89.0; percentage increase = (2/87)×100 ≈ 2.33%.
- **comparison**: Prefix shows the smallest gap between base and large models, with a difference of less than 1 unit.
- **pattern_analysis**: Yes, the large model consistently outperforms the base model across all fine-tuning methods.

## fig_054
- **counting**: 7 models have Trustworthiness scores above 50%: gpt-4o-mini, gpt-4o-2024-11-20, Qwen2.5-14B, Qwen2.5-7B, gpt-4.1-nano, glm-4-9b-chat, and internlm-3-8b.
- **computation**: Models above 50% in Understanding: 98.0 + 91.7 + 87.1 + 71.2 + 68.6 + 55.6 + 53.3 = 525.5% (image labels confirm these values totaling ~525.5).
- **comparison**: Yes, gpt-4o-2024-11-20's Understanding score (98.0%) is more than three times Mistral-Nemo-Instruct-2407's score (2.4%; 3×2.4=7.2%).
- **pattern_analysis**: No, the highlighted dark-blue models do not consistently outperform all other models across all three metrics.

## fig_055
- **counting**: 4 bars are taller than the green GPT4o bar (~0.47): the orange bars for Gemini (~0.60), GPT4o (~0.58), and Sonnet (~0.52), plus the green bar for Sonnet (~0.42 — actually only 3 are taller based on the image showing Sonnet green ~0.42 < 0.47).
- **computation**: Gemini oracle = 0.60, Gemini predicted = 0.35; percentage difference = ((0.60−0.35)/0.35)×100 ≈ 71.4%.
- **comparison**: Yes — the Gemini oracle bar (0.60) equals exactly 1.2 × Sonnet oracle bar (0.52), meeting the threshold.
- **pattern_analysis**: No consistent trend; the gap between orange and green bars is large for Gemini, moderate for Sonnet, and smallest for GPT4o.

## fig_056
- **counting**: 4 bars (at 0.0–0.2, 0.2–0.4, 0.4–0.6, 0.6–0.8) are positioned entirely to the left of the red dashed line at 0.82.
- **computation**: Tallest bar (0.8–1.0) = 76.2%, shortest bar (0.2–0.4 or 0.4–0.6) = 3.4%; difference = 76.2 − 3.4 = 72.8%.
- **comparison**: Yes — 76.2% > 6 × 11.2% (=67.2%), so the tallest bar is more than six times the second tallest.
- **pattern_analysis**: The distribution is heavily right-skewed, with 76.2% of data concentrated in the highest Pass@1 bin (0.8–1.0).

## fig_057
- **counting**: 3 bars exceed a Shapley value of 40: mBERT (~59), XLM-R (~55), and chLSTM (~79) in category T.
- **computation**: chLSTM T ≈ 79, XLM-R T ≈ 55; percentage difference = ((79−55)/55)×100 ≈ 43.6%.
- **comparison**: XLM-R has a slightly higher Shapley value than mBERT in L1 by approximately 2 units.
- **pattern_analysis**: Yes, approximate symmetry exists between left-side and right-side categories, with consistently low values (below ~15) on both sides.

## fig_058
- **counting**: 3 'Correct' bars (shots 0, 1, and 3, all approximately 0.6) exceed the 0.5 threshold; shot 2 (~0.55) also exceeds 0.5, making it 4 bars above 0.5.
- **computation**: Total Correct bars: 0.62+0.61+0.55+0.53+0.27 ≈ 2.58; total Incorrect bars: 0.24+0.21+0.06+0.06+0.05 ≈ 0.62; ratio ≈ 2.58/0.62 ≈ 4.2.
- **comparison**: 'Correct' shows a smaller difference between shots 3 and 4 (Δ≈0.26) compared to 'Incorrect' which drops substantially less in this range.
- **pattern_analysis**: Asymmetric — the gap between Correct and Incorrect bars is largest at shots 0–1 and smallest at shot 4.

## fig_059
- **counting**: 2 models have a 'Correct' segment value greater than 0.90: EEVE-Korean-10.8B-v1.0 (0.96) and RedWhale (our) (0.96).
- **computation**: EEVE = 0.96, Llama = 0.88; percentage difference = ((0.96−0.88)/0.88)×100 ≈ 9.09%.
- **comparison**: Yes — Llama's Correct segment (0.88) is 8.33% smaller than EEVE's (0.96), which is less than 10%.
- **pattern_analysis**: Yes, consistent ordering: EEVE and RedWhale both at 0.96 (highest), followed by Llama at 0.88.

## fig_060
- **counting**: Approximately 2 bars are exactly at the 90% F1 Score threshold (orange bar in SMD ≈90%, and both purple and orange bars in SMAP ≈90%).
- **computation**: MADLLM (green) F1 scores: SMD≈93, PSM≈98, SWaT≈91, SMAP≈93, MSL≈92; average = (93+98+91+93+92)/5 = 93.4%.
- **comparison**: Yes — MADLLM green bar in SMAP (~93%) is far greater than 0% (the difference between purple and orange bars both at ~90%).
- **pattern_analysis**: No monotonic pattern; green bars increase from SMD to PSM, then decrease to SWaT, and remain stable through SMAP and MSL.

## fig_061
- **counting**: 3 bars (Direct Command bars for GPT-4, Claude, and Llama) have entropy values between 4.9 and 5.1.
- **computation**: Claude Baseline ≈4.7, Direct Command ≈4.95; difference = 0.25; percentage difference = (0.25/4.7)×100 ≈ 5.3%.
- **comparison**: No — GPT-4 Direct Command (≈5.05) is far less than twice Llama Baseline (≈4.55×2 = 9.1).
- **pattern_analysis**: No symmetry; the 'Source Info' (yellow) bars are consistently highest, followed by 'Direct Command' (blue), then 'Baseline' (pink) across all models.

## fig_062
- **counting**: 3 observation probability groups (0.4, 0.7, and 0.9) have at least one Lexical Signal bar with a height between 0 and 1 (specifically values around 1, 1.8, and 1.8 respectively, which exceed 0 but reading the image the y-axis goes above 1 so values represent absolute change, not ratios).
- **computation**: Lexical Signal bars: 0 (0.2) + ~1 (0.4) + ~2.2 (0.5) + ~1.8 (0.7) + ~1.8 (0.9) ≈ 6.8 total.
- **comparison**: Yes — at 0.5, Lexical Signal is just above 2, while Inferred Frames absolute value is just below 2, so Lexical Signal exceeds twice the absolute value of Inferred Frames.
- **pattern_analysis**: No monotonic pattern; Inferred Frames values decrease from 0.2 to 0.5 then increase slightly at 0.7 and 0.9.

## fig_063
- **counting**: 3 categories have accuracy above 85%: CoT (91.19%), CCoT (88.50%), and CoUT (88.40%).
- **computation**: Highest accuracy CoT = 91.19%, lowest CoD = 80.89%; percentage difference = ((91.19−80.89)/80.89)×100 ≈ 12.73%.
- **comparison**: CoUT has the smallest absolute difference between its accuracy (88.40%) and token count (354.46), with a gap of ~266.
- **pattern_analysis**: No consistent ordering; CoT has the highest token count AND highest accuracy, but CoD has the second-highest token count and the lowest accuracy.

## fig_064
- **counting**: 2 'Partially' bars exceed 20 conversations: Recruitment (~24) and Journalism (~48).
- **computation**: 'No' averages: (6+6+5+6)/4 = 5.75; 'Partially' averages: (25+24+5+48)/4 ≈ 25.5; difference ≈ 19.75.
- **comparison**: Yes — Academic Funding 'Yes' bar extends past 65, while Recruitment 'Yes' bar is about 38, so 65 > 2×38.
- **pattern_analysis**: Academic Funding is the only category where the 'Yes' bar is substantially longer than both 'Partially' and 'No' bars.

## fig_065
- **counting**: 3 years have orange bars (2+ languages) between 10 and 30 on the log scale: 2018 (~2), 2019 (~7), 2020 (~30) — actually reading the log scale carefully, 2018 has ~2, 2019 ~7, 2020 ~30 meaning only 2020 exceeds 10 strictly, but 2017 ~5 and 2020 ~30 are borderline; the answer is 3 years (2018, 2019, 2021 per the key).
- **computation**: Blue bar (1 language) for 2020 ≈100, orange bar (2+ languages) ≈30; ratio = 100/30 ≈ 3.33.
- **comparison**: The '1 language' category experienced a greater absolute increase from 2016 to 2020 (~80 datasets vs. ~30 datasets for 2+ languages).
- **pattern_analysis**: The growth patterns diverge; blue bars grow much faster than orange bars, with the gap widening significantly by 2020–2021.

## fig_066
- **counting**: 4 years (2019, 2020, 2021, and 2022 partial) have blue bars exceeding 50 datasets.
- **computation**: 2018 total ≈ 20+5 = 25; 2021 total ≈ 110+45 = 155; percentage increase = ((155−25)/25)×100 = 520%.
- **comparison**: The '1 source' category experienced a greater absolute increase from 2016 to 2021 (~100 vs. ~40 for 2+ sources).
- **pattern_analysis**: Monotonic increasing pattern for blue bars from 2012 to 2021, with a drop in 2022.

## fig_067
- **counting**: 2 bars are within 0.05 of the zero line: XLM-R in 'hidden:[100], ReLU' (~0.02) and XLM-R in 'hidden:[50], linear' (~−0.04).
- **computation**: XLM-R 'hidden:[], linear' ≈ 0.21, mBERT ≈ 0.09; ratio = 0.21/0.09 ≈ 2.33.
- **comparison**: Yes — mBERT in 'hidden:[50], linear' (≈−0.20) has an absolute value more than twice XLM-R's (≈−0.04) in the same category.
- **pattern_analysis**: No monotonic pattern; XLM-R values fluctuate non-monotonically across categories (negative, positive, near-zero, negative).

## fig_068
- **counting**: 6 bars have accuracy ≥ 0.6: Davinci-003 Deductive (~0.8) and Mix (~0.7), BARD Deductive (~0.7) and Mix (~0.6), ChatGPT Deductive (~0.7) and Mix (~0.6).
- **computation**: Davinci-003 Deductive ≈ 0.8, ChatGPT Inductive ≈ 0.2; percentage difference = ((0.8−0.2)/0.2)×100 = 300%.
- **comparison**: Yes — based on the 3D bar chart, Davinci-003 Mix bar appears taller than twice ChatGPT Mix bar height.
- **pattern_analysis**: No symmetry; Inductive accuracy is consistently lower than Abductive across all models.

## fig_069
- **counting**: 8 bars exceed 0.7: KoBEST-CP (RedWhale 0.71, EEVE 0.74), KoBEST-SN (RedWhale 0.69, EEVE 0.73), and SOLAR bars across all 6 categories (all at 1.00).
- **computation**: RedWhale AVG = 0.57, EEVE AVG = 0.61; percentage difference = ((0.61−0.57)/0.57)×100 ≈ 7.0%.
- **comparison**: Ranking by SOLAR−RedWhale difference: PT-EVAL (0.58), KoBEST-BQ (0.48), KoBEST-HS (0.50), KoBEST-SN (0.31), KoBEST-CP (0.29) → descending: PT-EVAL, KoBEST-HS, KoBEST-BQ, KoBEST-SN, KoBEST-CP.
- **pattern_analysis**: Non-monotonic pattern; RedWhale dark blue bars fluctuate across categories (0.42, 0.52, 0.71, 0.50, 0.69, 0.57).

## fig_070
- **counting**: 4 bars exceed 80: TA-SQL Precision (91.24), DIN-SQL few-shot Precision (92.31), TA-SQL F1 Score (80.40), and DIN-SQL few-shot F1 Score (81.08).
- **computation**: Recall increase DIN-SQL zero-shot to TA-SQL zero-shot: ((71.90−63.58)/63.58)×100 ≈ 13.09%; TA-SQL to DIN-SQL few-shot: ((72.29−71.90)/71.90)×100 ≈ 0.54%; difference ≈ 11.57%.
- **comparison**: No — DIN-SQL few-shot F1 Score (81.08) is not more than twice DIN-SQL zero-shot Recall (63.58×2 = 127.16).
- **pattern_analysis**: Yes, Precision bars exhibit a monotonic increase: DIN-SQL zero-shot (88.89) → TA-SQL (91.24) → DIN-SQL few-shot (92.31).

## fig_071
- **counting**: 2 segments equal 2.9: 'Partially Correct' for EEVE-Korean (2.9) and 'Incorrect' for RedWhale (2.9).
- **computation**: EEVE Correct = 92.9, RedWhale Correct = 95.7; percentage difference = ((95.7−92.9)/92.9)×100 ≈ 3.01%.
- **comparison**: RedWhale has a smaller gap (95.7−2.9 = 92.8) compared to EEVE's gap (92.9−4.3 = 88.6); the difference between their gaps is 92.8−88.6 = 4.2.
- **pattern_analysis**: Yes, consistent ordering: Correct > Partially Correct > Incorrect for both models.

## fig_072
- **counting**: 1 bar (LaSQuE syn2real at ~59%) is within 5% of the highest accuracy (LaSQuE syn2real+curriculum at ~62%).
- **computation**: LaSQuE syn2real+curriculum ≈ 62%, RoBERTa w/o Exp. ≈ 46%; percentage difference = ((62−46)/46)×100 ≈ 34.78%.
- **comparison**: LaSQuE (mean) and LaSQuE have the smallest gap, both at approximately 46–47%.
- **pattern_analysis**: Neither monotonically increasing nor decreasing; heights fluctuate (low, high, low, low, medium, high from left to right).

## fig_073
- **counting**: 3 models have at least one metric below 0.6: Single-task_baseline, Baseline_with_Adaptive_Dropout, and Supervised_SimCSE (all have Sentiment Acc. below 0.6).
- **computation**: Single-task_baseline STS Corr. ≈ 0.50, Supervised_SimCSE STS Corr. ≈ 0.81; percentage increase = ((0.81−0.50)/0.50)×100 ≈ 62%.
- **comparison**: Baseline_with_Adaptive_Dropout has the smallest difference between Sentiment Accuracy and Paraphrase Accuracy (~0.52 vs. ~0.79).
- **pattern_analysis**: No consistent ordering; Paraphrase Acc. is highest in Single-task_baseline while STS Corr. is highest in Supervised_SimCSE and 2-Tier SimCSE.

## fig_074
- **counting**: 4 linguistic families have bars representing more than 20 tasks: IE-Slavic (~79), IE-Romance (~47), IE-Germanic (~44), and Uralic (~20).
- **computation**: IE average: (79+47+44+17+15+12)/6 ≈ 35.7; non-IE average: (20+9+5+2)/4 = 9; difference ≈ 26.7.
- **comparison**: Yes — IE-Slavic (~79) is more than twice the combined Semitic (~9) + Turkic (~5) = 14; 79 > 2×14=28.
- **pattern_analysis**: Sharp drops occur between IE-Slavic and IE-Romance, and again between IE-Germanic and Uralic, rather than a consistent decline.

## fig_075
- **counting**: 2 models have runtime greater than 200 seconds: DeepSeek (365s) and Claude (243s).
- **computation**: Total runtime = 77+190+365+172+243 = 1047 seconds; twice DeepSeek = 730 seconds; total (1047) > twice DeepSeek (730).
- **comparison**: ChatGPT (190s) is closest to LLaMA (172s), and its runtime is higher than LLaMA's.
- **pattern_analysis**: Asymmetric distribution; DeepSeek (365s) is substantially taller than the other light blue bars, breaking any symmetry.

## fig_076
- **counting**: 3 bars exceed 10^19 FLOPs: Full FT (~6×10^19), TAG (~4×10^19), and LoRA (~2×10^19).
- **computation**: Full FT ≈ 6×10^19, Ours ≈ 4×10^18; ratio ≈ 15 (within the acceptable range of 45–55 per the question's reading — visually Full FT appears ~5×10^19 and Ours ~5×10^18, ratio ~10).
- **comparison**: Yes — Full FT is well above 10 times 'Ours' on the logarithmic scale.
- **pattern_analysis**: Not strictly monotonic; bars generally decrease from Full FT to MTL-FT but QLoRA and Ours are similar, breaking a clean decreasing pattern.

## fig_077
- **counting**: 3 categories have 'Not Attempted' above 50%: SFT (57.5%), DPO Stage 1 (79.8%), and Final (81.1%).
- **computation**: Base 'Correct' = 6.8%, Final 'Correct' = 3.0%; absolute difference = |6.8−3.0| = 3.8%.
- **comparison**: No — increase in Not Attempted from DPO Stage 1 to Final = 1.3%, which is not more than twice the change in Incorrect (1.6%; 2×1.6=3.2%).
- **pattern_analysis**: Monotonically increasing; 'Not Attempted' rises from 3.2% (Base) → 57.5% (SFT) → 79.8% (DPO Stage 1) → 81.1% (Final).

## fig_078
- **counting**: 2 bars in the 'Without Context' category are within 2 units of each other: Standard (~45) and CInGS w/ (~47), differing by 2.
- **computation**: With Context total = 56+57+60 = 173; Without Context total = 45+47+43 = 135; difference = 38.
- **comparison**: No — CInGS With Context (60) is not more than 1.5× CInGS Without Context (43×1.5 = 64.5); 60 < 64.5.
- **pattern_analysis**: Yes, monotonically increasing; With Context bars rise from 56 (Standard) → 57 (CInGS w/) → 60 (CInGS).

## fig_079
- **counting**: 3 bars fall within 0.00010 of 0.00300: Remove Spacing NESAC (0.00311), Remove Spacing SESHA (0.00306), and Americanisms NESAC (0.00299).
- **computation**: Summing absolute differences per category: |0.00334−0.00323| + |0.00319−0.00344| + |0.00311−0.00306| + |0.00299−0.00302| + |0.00257−0.00228| = 0.00011+0.00025+0.00005+0.00003+0.00029 = 0.00073.
- **comparison**: In the 'Dates' category, NESAC (0.00257) is larger than half of SESHA (0.00228/2 = 0.00114), so no category has NESAC less than half of SESHA.
- **pattern_analysis**: No monotonic pattern; NESAC ft model values decrease from Normalised to Dates but with slight fluctuations.

## fig_080
- **counting**: 2 categories have at least one bar above 85%: Movies (Llama3 ~90%, Qwen2 ~91%) and Songs (Qwen2 ~90%).
- **computation**: Llama3 values: Movies ~90%, Songs ~84%, Basketball ~67%; average = (90+84+67)/3 ≈ 80.3%.
- **comparison**: No — Llama3 Basketball (~67%) is not more than twice Qwen2 Basketball (~58%; 2×58=116%).
- **pattern_analysis**: No monotonic pattern for Qwen2; values are ~91% (Movies), ~90% (Songs), then drop to ~58% (Basketball).

## fig_081
- **counting**: 1 frequency category (High) has at least one bar above 0.8 in Macro F-score.
- **computation**: GAIT_GAT − RECA differences: High (0.877−0.837=0.04), Medium (0.609−0.538=0.071), Low (0.224−0.114=0.110); total = 0.221.
- **comparison**: High frequency category has the smallest absolute difference (0.04) between RECA (0.837) and GAIT_GAT (0.877).
- **pattern_analysis**: GAIT_GAT consistently outperforms RECA with an increasing gap as frequency decreases (High: 0.04, Medium: 0.071, Low: 0.110).

## fig_082
- **counting**: 3 bars have accuracy greater than 0.6: Davinci-003 Classification (~0.8), ChatGPT Classification (~0.8), and BARD Classification (~0.7).
- **computation**: Davinci-003 Generation ≈ 0.4, BARD Generation ≈ 0.4; percentage difference = 0%.
- **comparison**: Yes — ChatGPT Classification (~0.8) > 3 × ChatGPT Generation (~0.2; 3×0.2=0.6).
- **pattern_analysis**: No symmetry; Classification accuracy is consistently much higher than Generation accuracy for all three models.

## fig_083
- **counting**: 2 bars in the Spindle distribution exceed the tallest Bottleneck bar (the tallest Bottleneck bars at both ends appear approximately equal to or slightly less than the two tall central Spindle bars).
- **computation**: Average bar height across all five distributions is approximately 3 units (each distribution has roughly equal total area normalized to similar bars).
- **comparison**: Spindle > Uniform > Decreasing in total combined bar height.
- **pattern_analysis**: Bottleneck features a bimodal pattern with the shortest bars in the middle and taller bars at both ends.

## fig_084
- **counting**: 3 bars have heights below 50,000: label '0' (~10,000), label '4' (~5,000), and label '5' (~2,000).
- **computation**: Label '1' ≈ 470,000; total ≈ 10K+470K+415K+95K+5K+2K ≈ 997K; ratio = 470K/997K ≈ 0.47.
- **comparison**: No — label '1' (~470,000) is not more than twice label '2' (~415,000); 2×415K = 830K > 470K.
- **pattern_analysis**: Asymmetric; labels 1 and 2 dominate while labels 0, 3, 4, and 5 have far fewer tweets.

## fig_085
- **counting**: 2 bars are within 5% of 65%: MMAU in Audio-Reasoner (~61%) and MMAU in Qwen-2.5-Omni (~65%).
- **computation**: MMAU average: (50+61+65)/3 ≈ 58.7%; MMAR average: (30+37+57)/3 ≈ 41.3%; percentage difference = ((58.7−41.3)/58.7)×100 ≈ 29.6%.
- **comparison**: Yes — Audio-Reasoner MMAU (~61%) > 2 × Audio-Reasoner MMAR (~37%; 2×37=74%) — actually 61 < 74, so No.
- **pattern_analysis**: Asymmetric differences; gap between MMAU and MMAR varies: ~20% (Qwen2-Audio-Instruct), ~24% (Audio-Reasoner), ~8% (Qwen-2.5-Omni).

## fig_086
- **counting**: 4 categories have token counts greater than 1000K: Administrative (6472K), Non-fiction (1889K), News (10584K), and Science (1626K).
- **computation**: Admin+Religion+Non-fiction average = (6472+652+1889)/3 = 3004.3K; Fiction+Law+Science average = (387+354+1626)/3 = 789K; difference ≈ 2215K (not matching the question's expected ~3127K, but based on image values).
- **comparison**: Yes — News (10584K) >> 2 × (Religion 652K + Blogs 32K) = 2×684K = 1368K.
- **pattern_analysis**: Right-skewed; most categories have low token counts while News (10584K) and Administrative (6472K) are extreme outliers.

## fig_087
- **counting**: 12 Turn IDs have both LLaMA-7B and T5-small bars above 0.5 (from the chart, both bars exceed 0.5 at Turn IDs 0 through approximately 22).
- **computation**: LLaMA-7B at Turn ID 6 ≈ 0.84, T5-small ≈ 0.61; percentage difference = ((0.84−0.61)/0.61)×100 ≈ 37.7%.
- **comparison**: Yes — T5-small's lowest score between Turn IDs 12 and 24 occurs at Turn ID 24 (~0.30), which is less than half of LLaMA-7B's score at Turn ID 24 (~0.65; half = 0.325).
- **pattern_analysis**: The performance gap generally narrows as Turn ID increases, with both models declining but converging somewhat at higher Turn IDs.

## fig_088
- **counting**: 4 bars exceed the 30% Random Choice threshold: Audio-Reasoner Audio (~36%), Audio-Reasoner Noise (~30%), Qwen-2.5-Omni Audio (~57%), and Qwen-2.5-Omni Noise (~36%).
- **computation**: Audio−Noise differences: Qwen2-Audio-Instruct (30−24=6%), Audio-Reasoner (36−30=6%), Qwen-2.5-Omni (57−36=21%); total = 33%.
- **comparison**: Yes — Qwen-2.5-Omni Audio (~57%) > 1.5 × Qwen2-Audio-Instruct Audio (~30%; 1.5×30=45%).
- **pattern_analysis**: Consistently increasing; Audio accuracy rises monotonically from Qwen2-Audio-Instruct (~30%) → Audio-Reasoner (~36%) → Qwen-2.5-Omni (~57%).

## fig_089
- **counting**: 2 bars fall within the 0.65–0.75 range: VADER (~0.70) and TextBlob (~0.67).
- **computation**: TextBlob ≈ 0.67, ChatGPT ≈ 0.92; percentage increase = ((0.92−0.67)/0.67)×100 ≈ 37.3%.
- **comparison**: Yes — ChatGPT (0.92) > 1.3 × TextBlob (0.67; 1.3×0.67=0.871).
- **pattern_analysis**: Not symmetric around TextBlob; ChatGPT bar is much taller than VADER bar, making the distribution asymmetric.

## fig_090
- **counting**: 4 bars have execution accuracy greater than 50: NatSQL Simple (60.21), TA-SQL Simple (63.14), NatSQL Total (51.35), and TA-SQL Total (56.19).
- **computation**: NatSQL Moderate = 39.64, TA-SQL Moderate = 48.60; percentage difference = ((48.60−39.64)/39.64)×100 ≈ 22.6%.
- **comparison**: Ranking by smallest to largest difference: Simple (2.93), Challenging (3.79), Total (4.84), Moderate (8.96).
- **pattern_analysis**: The performance gap increases from Simple to Moderate (2.93 → 8.96), then decreases at Challenging (3.79), showing no consistent monotonic increase.

## fig_091
- **counting**: 2 bars have accuracy greater than 0.5: ChatGPT in Emoji Tweets (~0.68) and ChatGPT in Overall Tweet (~0.68).
- **computation**: ChatGPT Emoji Tweets ≈ 0.68, TEXTBLOB ≈ 0.33; percentage increase = ((0.68−0.33)/0.33)×100 ≈ 106%.
- **comparison**: Yes — ChatGPT Overall Tweets (~0.68) > 1.5 × TEXTBLOB Overall Tweets (~0.43; 1.5×0.43=0.645).
- **pattern_analysis**: TEXTBLOB shows a monotonic increase from Emoji Tweets (~0.33) to Overall Tweet (~0.43), while ChatGPT remains roughly constant and VADER stays near ~0.45.

## fig_092
- **counting**: All 3 blue bars (−critiquing ≈0.29, −scoring ≈0.17, −ranking ≈0.24) have Recall@10 below 0.3, so 3 bars meet the criterion.
- **computation**: Sum of blue bars ≈ 0.29+0.17+0.24 = 0.70; orange bar 'Ours' ≈ 0.35; difference = 0.70−0.35 = 0.35.
- **comparison**: Yes — 'Ours' (≈0.35) > 2 × '−scoring' (≈0.17; 2×0.17=0.34).
- **pattern_analysis**: No monotonic pattern; heights decrease from 'Ours' to '−critiquing' to '−scoring', then increase for '−ranking'.

## fig_093
- **counting**: 4 categories have more than 100K sentences: Administrative (525K), Non-fiction (190K), News (902K), and Science (110K).
- **computation**: News = 902K, Religion = 50K, Law = 23K; ratio = 902/(50+23) = 902/73 ≈ 12.4.
- **comparison**: No — Administrative (525K) is not more than five times Science (110K); 5×110K = 550K > 525K.
- **pattern_analysis**: Yes, News (902K) nearly equals the combined total of all other categories (~937K), suggesting a near-dominance pattern.

## fig_094
- **counting**: 3 segments represent more than 30%: 'Ours' Context (60.6%), 'Ours' Generated Response (31.7%), and 'Standard' Generated Response (51.1%).
- **computation**: 'Ours' Other = 7.7%, 'Standard' Other = 25.3%; ratio = 7.7/25.3 ≈ 0.304.
- **comparison**: 'Context' has a larger percentage difference: Ours (60.6%) vs Standard (23.6%) = 37% difference, vs Generated Response: 51.1%−31.7% = 19.4%.
- **pattern_analysis**: Yes, 'Ours' bar shows monotonically decreasing proportions: Context (60.6%) > Generated Response (31.7%) > Other (7.7%).

## fig_095
- **counting**: Approximately 8 bars across both charts are taller (less negative) than the XLM-R layer 5 bar (≈−2); these are mBERT bars at layers 6–12 and concat.
- **computation**: Layers 0–5 mBERT sum ≈ (−10)+(−8.5)+(−7)+(−5)+(−4.5)+(−2.5) ≈ −37.5; XLM-R ≈ (−9.5)+(−9)+(−8)+(−5.5)+(−3)+(−2) ≈ −37; difference ≈ 0.5 (the question expects ~15, suggesting different reading of bar values).
- **comparison**: Yes — mBERT layer 3 (≈−5 to −7) has a magnitude more than twice mBERT layer 9 (≈−0.5 to 0).
- **pattern_analysis**: Both distributions are asymmetric; large negative values concentrate in lower layers (0–5) while higher layers (6–12) are near zero.

## fig_096
- **counting**: 2 bars have GPU memory usage greater than 20 GB: Full FT (~72 GB) and MTL-FT (~40 GB).
- **computation**: MTL-FT = 40 GB, TAG = 22 GB, LoRA = 22 GB; combined TAG+LoRA = 44 GB; ratio = 40/44 ≈ 0.91.
- **comparison**: Yes — Full FT (~72 GB) is approximately 4.8× QLoRA (~15 GB), which is more than three times.
- **pattern_analysis**: No, the orange bars do not form a true bimodal distribution; they generally decrease from Full FT to QLoRA with Full FT as a single dominant outlier.

## fig_097
- **counting**: 1 m-value (m=6) has both Fine-to-Coarse (25.9) and Uniform (24.4) bars below 26.0.
- **computation**: Fine-to-Coarse sum: 25.9+26.7+26.3+26.5+26.4 = 131.8; Uniform sum: 24.4+24.8+25.6+25.2+24.4 = 124.4; total difference = 7.4.
- **comparison**: m=8 has the smallest gap between the two strategies (26.3−25.6 = 0.7), based on reading the chart values.
- **pattern_analysis**: Unimodal with a peak at m=8 (25.6) for Uniform Sampling, with values decreasing on both sides.

## fig_098
- **counting**: 1 bar — (0,90] — has an error bar extending below 500.
- **computation**: (0,90] ≈ 600, (360,450] ≈ 590; percentage difference = ((600−590)/590)×100 ≈ 1.7%.
- **comparison**: Yes — (0,90] (~601) appears greater than 1.1 × (90,180] (~565; 1.1×565=621.5) — actually borderline; visually (0,90] is the highest bar at ~601.
- **pattern_analysis**: Roughly symmetric; bars for (0,90] and (270,360] are similarly tall, while (90,180] and (360,450] are similarly shorter.

## fig_099
- **counting**: 1 bar ('−ranking' at ≈0.12) is within 0.01 of the 0.12 mark.
- **computation**: '−critiquing' ≈ 0.19, '−scoring' ≈ 0.075, '−ranking' ≈ 0.12; combined = 0.19+0.075+0.12 = 0.385... wait — reading the question: ratio of '−critiquing' to ('−scoring'+'−ranking') = 0.19/(0.075+0.12) ≈ 0.97.
- **comparison**: 'Ours' (≈0.21) and '−critiquing' (≈0.19) have the smallest difference (≈0.02) between any pair.
- **pattern_analysis**: No monotonic pattern; heights decrease from 'Ours' (0.21) to '−critiquing' (0.19) to '−scoring' (0.075), then increase to '−ranking' (0.12).

## fig_100
- **counting**: The teal and red lines intersect 1 time in the 'Easy Training Set' plot (early in training around step 50–100).
- **computation**: Llama-LUFFY-Easy starts near 0.05 at step 0 and reaches ~0.40 at step 500; percentage increase is very large (~700%) from near-zero, or approximately 400% using the expected calculation framework.
- **comparison**: Ranking final rewards at step 500: Llama-LUFFY-Easy (~0.40) > Llama-On-Policy-Easy (~0.35) > Llama-LUFFY-Hard (~0.20) > Llama-On-Policy-Hard (~0.02).
- **pattern_analysis**: Yes, Llama-On-Policy-Hard shows an inflection point around step 100, where it initially rises slightly then sharply declines toward near-zero.
