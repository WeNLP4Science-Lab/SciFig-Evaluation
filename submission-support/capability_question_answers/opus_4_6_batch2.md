## fig_051
- **counting**: 3 bars have average performance within 1 unit of 52: Standard (~52), FactTune (~52), and ClInGS (w/) (~53).
- **computation**: The difference between ClInGS's average (59) and the average of the other four methods (~52) is approximately 7.
- **comparison**: No, ClInGS (~59) is not more than twice FactTune (~52), since twice 52 is 104.
- **pattern_analysis**: No, the bar heights do not follow a monotonic pattern; they fluctuate across methods with ClInGS being the tallest.

## fig_052
- **counting**: 6 bars exceed 100 in popularity, all located in the Basketball category (3 models x 2 conditions visible above 100).
- **computation**: The difference between the Acc=0 & GT Ans (~30) and Acc=1 & GT Ans (~50) segments for ChatGPT in Songs is approximately 20.
- **comparison**: ChatGPT has the smallest difference between Acc=0 & GT Ans and Acc=0 & Gene Ans in the Songs category.
- **pattern_analysis**: Yes, popularity increases monotonically from Movies to Songs to Basketball for all AI models.

## fig_053
- **counting**: 3 bars represent GLUE performance greater than 88: the large model bars for LoRA, S5-model, and Adaptor.
- **computation**: The percentage increase from base (~87) to large (~89) for S5-model is approximately 2.3%.
- **comparison**: Prefix shows the smallest performance gap between base and large RoBERTa models (about 1 unit difference).
- **pattern_analysis**: Yes, the large model consistently outperforms the base model across all fine-tuning methods.

## fig_054
- **counting**: 7 models have Trustworthiness scores above 50%: gpt-4o-mini (88.8%), Qwen2.5-7B (71.8%), gpt-4o (54.6%), Qwen2.5-14B (63.8%), internlm3 (65.4%), glm-4 (55.2%), gpt-4.1-nano (58.2%).
- **computation**: The total of all models with Understanding above 50% is approximately 525.5% (98.0+91.7+87.1+71.2+68.6+55.6+53.3).
- **comparison**: Yes, gpt-4o-2024-11-20 (98.0%) is more than three times Mistral-Nemo-Instruct-2407 (2.4%), since 3 x 2.4 = 7.2%.
- **pattern_analysis**: No, the highlighted dark blue models (GPT models) do not consistently outperform all other models across all three metrics.

## fig_055
- **counting**: 4 bars are taller than the green bar (~0.35) in GPT4o: the orange bars for Gemini (~0.60), GPT4o (~0.58), Sonnet (~0.52), and the green bar for Sonnet is not taller -- actually 3 bars: orange Gemini, orange GPT4o, orange Sonnet.
- **computation**: The percentage difference between Structured prompt + oracle (0.60) and Structured prompt + predicted (0.35) for Gemini is approximately 71.4%.
- **comparison**: The Gemini oracle bar (0.60) equals exactly 1.2 times the Sonnet oracle bar (0.50), so it is not strictly more than 1.2 times.
- **pattern_analysis**: No, the differences between orange and green bars are not consistent: large gap for Gemini (~0.25), smaller for GPT4o (~0.12), and moderate for Sonnet (~0.10).

## fig_056
- **counting**: 4 bars are positioned entirely to the left of the red dashed line at Pass@1 = 0.82 (the bars at 0.0-0.2, 0.2-0.4, 0.4-0.6, and 0.6-0.8).
- **computation**: The difference between the tallest bar (76.2%) and the shortest bar (3.4%) is 72.8 percentage points.
- **comparison**: Yes, 76.2% is more than six times 11.2% (6 x 11.2 = 67.2%).
- **pattern_analysis**: The distribution is heavily right-skewed, with 76.2% of data concentrated in the 0.8-1.0 range.

## fig_057
- **counting**: 3 bars have Shapley values greater than 40: mBERT (~59), XLM-R (~55), and chLSTM (~79) in category T.
- **computation**: The percentage difference between chLSTM (~79) and XLM-R (~55) in category T is approximately 43.6%.
- **comparison**: XLM-R has a slightly higher Shapley value than mBERT in category L1, by approximately 2 units.
- **pattern_analysis**: Yes, there is approximate symmetry between left-side and right-side categories, with both showing consistently low values below 15.

## fig_058
- **counting**: 3 Correct bars have heights greater than 0.5: at shots 0 (~0.61), 1 (~0.61), and 2 (~0.55).
- **computation**: The total Correct bar heights sum to approximately 2.53 and total Incorrect to approximately 0.60, giving a ratio of about 4.2.
- **comparison**: The Correct category shows a smaller difference between shots 3 and 4 (~0.25) compared to the Incorrect category (~0.22), so they are similar.
- **pattern_analysis**: The pattern is asymmetric; the gap between Correct and Incorrect bars is large for shots 0-1, moderate for shots 2-3, and small for shot 4.

## fig_059
- **counting**: 2 models have Correct segment values greater than 0.90: EEVE-Korean-10.8B-v1.0 (0.96) and RedWhale (0.96).
- **computation**: The percentage difference in Correct between Llama-3-Open-Ko-8B (0.88) and EEVE-Korean-10.8B-v1.0 (0.96) is approximately 9.09%.
- **comparison**: Yes, the Correct segment of Llama-3-Open-Ko-8B is approximately 8.33% smaller than EEVE-Korean's, which is less than 10%.
- **pattern_analysis**: Yes, the ordering is consistent: EEVE-Korean and RedWhale tie at 0.96 Correct, both higher than Llama-3-Open-Ko-8B at 0.88.

## fig_060
- **counting**: 2 bars appear to be exactly at the 90% threshold: the purple and orange bars in SMD are near 90%.
- **computation**: The average F1 Score for MADLLM (green bars) across all datasets is approximately (93+98+91+93+92)/5 = 93.4%.
- **comparison**: Yes, MADLLM's F1 Score in SMAP (~93%) is more than twice the difference between the purple (~90%) and orange (~90%) bars (difference ~0).
- **pattern_analysis**: No, the green bars do not follow a monotonic pattern; they peak at PSM (~98%) then drop for SWaT (~91%).

## fig_061
- **counting**: 3 bars have entropy values between 4.9 and 5.1: the Direct Command bars for GPT-4 (~5.05), Claude (~4.95), and the Source Info bar for GPT-4 (~5.22) is too high, so only 2 bars are in range.
- **computation**: The percentage difference between Baseline (~4.67) and Direct Command (~4.95) for Claude is approximately 6%.
- **comparison**: No, GPT-4 Direct Command (~5.05) is not more than twice Llama Baseline (~4.55), since 2 x 4.55 = 9.1.
- **pattern_analysis**: No, there is no symmetry; Baseline values are consistently lower than both Source Info and Direct Command values across all models.

## fig_062
- **counting**: 3 observation probability groups have at least one bar with height between 0 and 1 (positive values): 0.4, 0.7, and 0.9 have small positive Lexical Signal bars.
- **computation**: The total sum of Lexical Signal bars across all observation probabilities is approximately 0 + 0.5 + 2.0 + 1.8 + 1.5 = 5.8.
- **comparison**: No, the Lexical Signal bar at 0.5 (~2.0) is not more than twice the absolute value of the Inferred Frames bar (~2.0); they are approximately equal.
- **pattern_analysis**: No, the Inferred Frames values do not follow a monotonic pattern; they fluctuate across observation probabilities.

## fig_063
- **counting**: 3 categories have accuracy above 85%: CoT (91.19%), CCoT (88.50%), and CoUT (88.40%).
- **computation**: The percentage difference between CoT (91.19%) and CoD (80.89%) is approximately 12.73%.
- **comparison**: CoUT has the smallest difference between its accuracy (88.40%) and token count (354.46), with a gap of 266.06.
- **pattern_analysis**: No, there is no consistent ordering; CoT has the highest token count and accuracy, but CoD has the second-highest token count yet the lowest accuracy.

## fig_064
- **counting**: 2 categories have Partially (yellow) bars exceeding 20 conversations: Academic Collaboration (~30) and Journalism (~48).
- **computation**: The difference between the average No (~5.75) and average Partially (~26.25) values across all categories is 20.5.
- **comparison**: Yes, the Yes bar for Academic Funding (~65) is more than twice the Yes bar for Recruitment (~40).
- **pattern_analysis**: Academic Funding is the category where the Yes bar is consistently and significantly longer than both Partially and No bars.

## fig_065
- **counting**: 3 years have orange bars (2+ languages) between 10 and 30 datasets: 2018 is low (~2), so only 2019 (~8) and 2020 (~22) qualify, plus 2021 (~10).
- **computation**: In 2020, the ratio of 1-language (~100) to 2+-language (~22) datasets is approximately 4.5.
- **comparison**: The 1-language category experienced a greater absolute increase from 2016 to 2020 (~87 vs ~22).
- **pattern_analysis**: The growth patterns diverge; blue bars grow much faster than orange bars, with the gap widening significantly after 2017.

## fig_066
- **counting**: 4 years have blue bars exceeding 50 datasets: 2019 (~47 is close), 2020 (~87), and 2021 (~113) clearly exceed 50; 2018 (~30) does not. So 2 years clearly exceed 50.
- **computation**: The percentage increase from 2018 (total ~50) to 2021 (total ~160) is approximately 220%.
- **comparison**: The 1-source category (blue) experienced a greater absolute increase from 2016 to 2021 (~103 vs ~45).
- **pattern_analysis**: The blue bars show a mostly monotonic increase from 2012 to 2021, with a drop in 2022 (likely incomplete data).

## fig_067
- **counting**: 2 bars are within 0.05 of the zero line: XLM-R in hidden:[100] ReLU (~0.03) and XLM-R in hidden:[50] linear (~-0.05).
- **computation**: The ratio of XLM-R (0.21) to mBERT (0.09) in hidden:[] linear is approximately 2.33.
- **comparison**: Yes, the mBERT bar in hidden:[50] linear (~-0.05) is more than twice the XLM-R bar in absolute terms (|-0.05| vs |-0.05|); actually mBERT is ~-0.05 and XLM-R ~-0.05, they appear similar.
- **pattern_analysis**: No, XLM-R's bar heights are non-monotonic, going from negative to positive to near-zero to negative across categories.

## fig_068
- **counting**: 6 bars have accuracy greater than or equal to 0.6: Davinci-003 Deductive and Mix, ChatGPT Deductive and Mix, BARD Deductive and Mix.
- **computation**: The percentage difference between Davinci-003 Deductive (~0.8) and ChatGPT Inductive (~0.2) is approximately 300%.
- **comparison**: No, Davinci-003's Mix accuracy (~0.8) is not more than twice ChatGPT's Mix accuracy (~0.6).
- **pattern_analysis**: No, there is no symmetry; Inductive accuracy is consistently lower than Abductive accuracy across all models.

## fig_069
- **counting**: 8 bars have values greater than 0.7: all 6 SOLAR-10.7B-v1.0 bars (all at 1.00) plus KoBEST-CP RedWhale (0.71) and KoBEST-CP EEVE (0.74).
- **computation**: The percentage difference between RedWhale (0.57) and EEVE-Korean (0.61) AVG is approximately 7.02%.
- **comparison**: Ranked by descending difference: PT-EVAL (0.58), KoBEST-HS (0.46), KoBEST-BQ (0.44), KoBEST-SN (0.27), KoBEST-CP (0.26).
- **pattern_analysis**: Non-monotonic pattern; RedWhale values rise from PT-EVAL (0.42) to KoBEST-CP (0.71), drop at KoBEST-HS (0.50), rise at KoBEST-SN (0.69).

## fig_070
- **counting**: 5 bars have values greater than 80: TA-SQL Precision (91.24), DIN-SQL few-shot Precision (92.31), DIN-SQL zero-shot Precision (88.89), TA-SQL F1 (80.40), DIN-SQL few-shot F1 (81.08).
- **computation**: The percentage increase in Recall from DIN-SQL zero-shot to TA-SQL zero-shot is 13.09%, and from TA-SQL to DIN-SQL few-shot is 0.54%; the difference is 12.55%.
- **comparison**: No, the F1 Score of DIN-SQL few-shot (81.08) is not more than twice the Recall of DIN-SQL zero-shot (63.58), since 63.58 x 2 = 127.16.
- **pattern_analysis**: Yes, the Precision bars exhibit a monotonic increase: 88.89, 91.24, 92.31 from left to right.

## fig_071
- **counting**: 2 segments have values equal to 2.9: EEVE-Korean Partially Correct (2.9) and RedWhale Incorrect (2.9).
- **computation**: The percentage difference in Correct responses between EEVE-Korean (92.9) and RedWhale (95.7) is approximately 3.01%.
- **comparison**: RedWhale has a larger gap (95.7 - 2.9 = 92.8) than EEVE-Korean (92.9 - 4.3 = 88.6), meaning EEVE-Korean has the smaller gap.
- **pattern_analysis**: Yes, the ordering is consistent: Correct > Partially Correct > Incorrect for both models.

## fig_072
- **counting**: 1 bar is within 5% of the highest accuracy (~62%): LaSQuE (syn2real) at approximately 58%.
- **computation**: The percentage difference between LaSQuE syn2real+curriculum (~62%) and RoBERTa w/o Exp. (~46%) is approximately 34.8%.
- **comparison**: LaSQuE (mean) and LaSQuE have the smallest gap in accuracy, both near 41-42%.
- **pattern_analysis**: Neither monotonic increasing nor decreasing; bars fluctuate with a dip at LaSQuE (mean)/LaSQuE before rising again.

## fig_073
- **counting**: 3 models have at least one metric below 0.6: Single-task_baseline, Baseline_with_Adaptive_Dropout, and Supervised_SimCSE (all have Sentiment Acc. below 0.6).
- **computation**: The percentage increase in STS Correlation from Single-task_baseline (~0.50) to Supervised_SimCSE (~0.81) is approximately 62%.
- **comparison**: Baseline_with_Adaptive_Dropout has the smallest difference between Sentiment Accuracy (~0.52) and Paraphrase Accuracy (~0.78).
- **pattern_analysis**: No, the ordering of the three metrics is not consistent across all models; e.g., STS Corr. is lowest for Single-task_baseline but highest for Supervised_SimCSE.

## fig_074
- **counting**: 4 linguistic families have bars exceeding 20 tasks: IE-Slavic (~79), IE-Romance (~47), IE-Germanic (~43), and Uralic (~20).
- **computation**: The difference between the IE average (~37.5) and non-IE average (~12.5) is approximately 25.
- **comparison**: Yes, IE-Slavic (~79) is more than twice the combined Semitic (~8) and Turkic (~5) total of 13.
- **pattern_analysis**: There are sharp drops between IE-Slavic and IE-Romance, and between Uralic and IE-Baltic, rather than a gradual decline.

## fig_075
- **counting**: 2 models have runtime greater than 200 seconds: DeepSeek (365) and Claude (243).
- **computation**: The total runtime of all models is 77 + 190 + 365 + 172 + 243 = 1047 seconds, which exceeds twice DeepSeek (730).
- **comparison**: ChatGPT (190 seconds) has the runtime closest to LLaMA (172 seconds), and its runtime is higher.
- **pattern_analysis**: The distribution is asymmetric; DeepSeek at 365s is a clear outlier among the light blue LLM bars.

## fig_076
- **counting**: 3 bars have heights above 10^19 FLOPs: Full FT, TAG, and LoRA.
- **computation**: The ratio of Full FT (~6x10^19) to Ours (~3x10^18) FLOPs is approximately 20.
- **comparison**: Yes, Full FT (~6x10^19) has more than ten times the FLOPs of Ours (~3x10^18).
- **pattern_analysis**: The distribution follows a generally decreasing pattern from Full FT to QLoRA, but Ours breaks the monotonic trend by being slightly higher than QLoRA.

## fig_077
- **counting**: 3 categories have Not Attempted bars above 50%: SFT (57.5%), DPO Stage 1 (79.8%), and Final (81.1%).
- **computation**: The difference in Correct performance between Base (6.8%) and Final (3.0%) is 3.8 percentage points.
- **comparison**: No, the increase in Not Attempted from DPO Stage 1 to Final (1.3%) is not more than twice the decrease in Incorrect (1.6%).
- **pattern_analysis**: The Not Attempted percentages increase monotonically across all four stages: 3.2% to 57.5% to 79.8% to 81.1%.

## fig_078
- **counting**: 2 bars in Without Context have heights within 2 units: Standard (~45) and CInGS (w/) (~47).
- **computation**: The total difference between With Context (56+57+60=173) and Without Context (45+47+44=136) is 37.
- **comparison**: No, CInGS With Context (60) is not more than 1.5 times its Without Context value (44), since 44 x 1.5 = 66 > 60.
- **pattern_analysis**: Yes, the With Context bars increase monotonically: Standard (56) < CInGS (w/) (57) < CInGS (60).

## fig_079
- **counting**: 3 bars are within 0.00010 of 0.00300: Remove Spacing NESAC (0.00311), Remove Spacing SESHA (0.00306), and Americanisms SESHA (0.00302).
- **computation**: The total absolute difference in WER between NESAC and SESHA across all categories sums to approximately 0.00049.
- **comparison**: In no category is the NESAC ft model bar less than half the height of the SESHA ft model bar, as all values are relatively close.
- **pattern_analysis**: No, the NESAC ft model values do not follow a monotonic pattern; they fluctuate from Normalised (0.00334) down to Dates (0.00257).

## fig_080
- **counting**: 2 categories have at least one bar above 85%: Movies (Llama3 ~89%, Qwen2 ~90%) and Songs (Qwen2 ~90%).
- **computation**: The average ratio for Llama3 across all categories is approximately (89+84+67)/3 = 80%.
- **comparison**: No, Llama3's ratio (67%) in Basketball is not more than twice Qwen2's ratio (58%), since 58 x 2 = 116.
- **pattern_analysis**: No, Qwen2 ratios do not follow a monotonic pattern: 90% (Movies), 90% (Songs), 58% (Basketball).

## fig_081
- **counting**: 1 frequency category has at least one bar with Macro F-score above 0.8: High (RECA: 0.837, GAIT_GAT: 0.877).
- **computation**: The total difference in Macro F-scores between GAIT_GAT and RECA across all categories is 0.04 + 0.071 + 0.110 = 0.221.
- **comparison**: The High frequency category has the smallest absolute difference (0.04) between RECA (0.837) and GAIT_GAT (0.877).
- **pattern_analysis**: The difference between GAIT_GAT and RECA increases as frequency decreases: 0.04 (High), 0.071 (Medium), 0.110 (Low).

## fig_082
- **counting**: 3 bars have accuracy greater than 0.6: Davinci-003 Classification (~0.8), ChatGPT Classification (~0.8), and BARD Classification (~0.6).
- **computation**: The percentage difference between Davinci-003 (~0.4) and BARD (~0.4) for Generation is 0%.
- **comparison**: Yes, ChatGPT Classification accuracy (~0.8) is more than three times its Generation accuracy (~0.2).
- **pattern_analysis**: No, there is no symmetry; Classification accuracy is significantly higher than Generation accuracy for all models.

## fig_083
- **counting**: 2 bars across all distributions are taller than the tallest bar in Bottleneck: the tallest bars in Decreasing and Increasing distributions.
- **computation**: The average height across all bars in all five distributions is approximately 3 units.
- **comparison**: Decreasing > Increasing > Uniform > Spindle > Bottleneck in terms of total bar height, though Spindle and Increasing are close.
- **pattern_analysis**: Bottleneck features a bimodal pattern with shorter bars in the middle and taller bars at both ends.

## fig_084
- **counting**: 3 bars have heights below 50,000: labels 0 (~8,000), 4 (~5,000), and 5 (negligible).
- **computation**: The ratio of label 1 (~475,000) to total tweets (~990,000) is approximately 0.48.
- **comparison**: No, label 1 (~475,000) is not more than twice label 2 (~415,000), since 415,000 x 2 = 830,000.
- **pattern_analysis**: No, the distribution is asymmetric around label 2; labels 1 and 2 dominate while others are much smaller.

## fig_085
- **counting**: 2 bars are within 5% of the 65% mark: MMAU for Audio-Reasoner (~63%) and MMAU for Qwen-2.5-Omni (~65%).
- **computation**: The average MMAU (~60%) minus the average MMAR (~37%) gives a percentage difference of approximately 38%.
- **comparison**: Yes, MMAU in Audio-Reasoner (~63%) is more than twice MMAR in the same category (~37%).
- **pattern_analysis**: No, the differences between MMAU and MMAR are asymmetric: ~20% (Qwen2-Audio), ~26% (Audio-Reasoner), ~9% (Qwen-2.5-Omni).

## fig_086
- **counting**: 4 categories have token counts greater than 1000: Administrative (6472), Non-fiction (1889), News (10584), and Science (1626).
- **computation**: The difference between the IE-like group average (Administrative 6472, Religion 652, Non-fiction 1889 = avg 3004.3) and the other group average (Fiction 387, Law 354, Science 1626 = avg 789) is approximately 2215.
- **comparison**: Yes, News (10584) is more than twice the combined Religion (652) and Blogs (32) total of 684.
- **pattern_analysis**: Yes, the distribution is right-skewed, with News and Administrative having much higher values than most other categories.

## fig_087
- **counting**: 7 Turn IDs have both LLaMA-7B and T5-small bars above 0.5: Turn IDs 0, 2, 4, 6, 8, 10, and possibly 14.
- **computation**: The percentage difference between LLaMA-7B (~0.83) and T5-small (~0.61) at Turn ID 6 is approximately 36%.
- **comparison**: Yes, T5-small's lowest score between Turn IDs 12-24 occurs at Turn ID 24 (~0.30), which is less than half of LLaMA-7B at Turn ID 24 (~0.65).
- **pattern_analysis**: The performance gap between LLaMA-7B and T5-small generally widens as Turn ID increases, not narrows.

## fig_088
- **counting**: 4 bars have accuracy above the 30% Random Choice threshold: Audio and Noise bars for both Audio-Reasoner and Qwen-2.5-Omni.
- **computation**: The total accuracy difference between Audio and Noise conditions across all models is approximately 10+6+20 = 36%.
- **comparison**: Yes, Qwen-2.5-Omni Audio accuracy (~57%) is more than 1.5 times Qwen2-Audio-Instruct Audio accuracy (~30%).
- **pattern_analysis**: The Audio condition accuracy consistently increases across the three models from ~30% to ~37% to ~57%.

## fig_089
- **counting**: 2 bars have accuracy within the range 0.65 to 0.75: VADER (~0.70) and TextBlob (~0.67).
- **computation**: The percentage increase from TextBlob (~0.67) to ChatGPT (~0.92) is approximately 37.3%.
- **comparison**: Yes, ChatGPT (0.92) is more than 1.3 times TextBlob (0.67), since 0.67 x 1.3 = 0.871.
- **pattern_analysis**: No, the distribution is asymmetric; ChatGPT is much taller than VADER and TextBlob, which are similar in height.

## fig_090
- **counting**: 4 bars have execution accuracy greater than 50: NatSQL Simple (60.21), TA-SQL Simple (63.14), NatSQL Total (51.35), TA-SQL Total (56.19).
- **computation**: The percentage difference in execution accuracy between NatSQL (39.64) and TA-SQL (48.60) for Moderate is approximately 22.6%.
- **comparison**: Ranked by difference from smallest to largest: Simple (2.93), Challenging (3.79), Total (4.84), Moderate (8.96).
- **pattern_analysis**: The gap increases from Simple (2.93) to Moderate (8.96) then decreases at Challenging (3.79), showing a non-monotonic pattern.

## fig_091
- **counting**: 2 bars have accuracy greater than 0.5: ChatGPT in both Emoji Tweets (~0.67) and Overall Tweet (~0.65).
- **computation**: The percentage increase from TEXTBLOB (~0.30) to ChatGPT (~0.67) in Emoji Tweets is approximately 123%.
- **comparison**: Yes, ChatGPT's Overall Tweet accuracy (~0.65) is more than 1.5 times TEXTBLOB's (~0.38), since 0.38 x 1.5 = 0.57.
- **pattern_analysis**: TEXTBLOB shows a monotonic increase from Emoji Tweets (~0.30) to Overall Tweet (~0.38); ChatGPT remains roughly constant.

## fig_092
- **counting**: 3 blue bars have Recall@10 values below 0.3: -critiquing (~0.29), -scoring (~0.17), and -ranking (~0.23).
- **computation**: The difference between the sum of blue bars (0.29+0.17+0.23=0.69) and the orange bar (0.35) is approximately 0.34.
- **comparison**: Yes, Ours (0.35) is more than twice -scoring (0.17), since 0.17 x 2 = 0.34.
- **pattern_analysis**: No, the distribution is non-monotonic; heights go from 0.35 (Ours) to 0.29 (-critiquing) to 0.17 (-scoring) to 0.23 (-ranking).

## fig_093
- **counting**: 4 categories have more than 100K sentences: Administrative (525K), Non-fiction (190K), News (902K), and Science (110K).
- **computation**: The ratio of News (902K) to combined Religion (50K) and Law (23K) is 902/73 = approximately 12.36.
- **comparison**: No, Administrative (525K) is not more than five times Science (110K), since 5 x 110 = 550K > 525K.
- **pattern_analysis**: News (902K) nearly matches the combined total of all other categories (935K), showing strong dominance but not exceeding it.

## fig_094
- **counting**: 3 segments across both bars represent percentages greater than 30%: Ours Context (60.6%), Ours Generated Response (31.7%), and Standard Generated Response (51.1%).
- **computation**: The ratio of Other in Ours (7.7%) to Other in Standard (25.3%) is approximately 0.304.
- **comparison**: Context has the larger percentage difference between Ours (60.6%) and Standard (23.6%), a gap of 37% vs 19.4% for Generated Response.
- **pattern_analysis**: Yes, the Ours bar shows a monotonic decrease from left to right: 60.6% > 31.7% > 7.7%.

## fig_095
- **counting**: 8 bars across both charts are taller (less negative) than the bar at layer 5 in XLM-R (~-2): mBERT layers 5-12 and concat are all less negative.
- **computation**: The difference in total percent point difference between mBERT and XLM-R for layers 0-5 is approximately 15 points.
- **comparison**: Yes, mBERT layer 3 (~-5) has a larger absolute value than twice mBERT layer 9 (~0), so its magnitude is more than twice.
- **pattern_analysis**: Both distributions are asymmetric, with larger negative values concentrated in lower layers (0-5) and near-zero values in higher layers (6-12).

## fig_096
- **counting**: 2 bars have GPU memory usage greater than 20 GB: Full FT (~72 GB) and MTL-FT (~40 GB).
- **computation**: The ratio of MTL-FT (~40 GB) to combined TAG (~22 GB) and LoRA (~22 GB) is approximately 40/44 = 0.91.
- **comparison**: Yes, Full FT (~72 GB) is more than three times QLoRA (~13 GB), since 13 x 3 = 39 GB.
- **pattern_analysis**: The orange bars show a generally decreasing pattern from Full FT to QLoRA, but not strictly bimodal.

## fig_097
- **counting**: 1 m-value has both purple and yellow bars below 26.0: m=6 (Fine-to-Coarse ~25.95, Uniform ~24.4).
- **computation**: The total difference in MAP@10 between Fine-to-Coarse and Uniform summed across all m-values is approximately 1.55+2.0+0.7+1.3+2.0 = 7.55.
- **comparison**: The smallest gap between the two strategies occurs at m=8, with a difference of approximately 0.7.
- **pattern_analysis**: The Uniform strategy distribution is unimodal with a peak at m=8 (~25.6) and values decreasing on either side.

## fig_098
- **counting**: 1 bar has error bars extending below 500: the (0,90] group, whose lower error bar reaches near 500.
- **computation**: The percentage difference between (0,90] (~600) and (360,450] (~590) is approximately 1.7%.
- **comparison**: Yes, (0,90] (~600) is more than 1.1 times (90,180] (~567), since 567 x 1.1 = 623.7, actually no -- 600 < 623.7.
- **pattern_analysis**: The distribution shows approximate symmetry, with higher values at the extremes (0,90] and (360,450] and a dip in the middle groups.

## fig_099
- **counting**: 1 bar has a height within 0.01 of 0.12: the -ranking bar at approximately 0.12.
- **computation**: The ratio of -critiquing (0.19) to combined -scoring (0.075) and -ranking (0.12) is 0.19/0.195 = approximately 0.97.
- **comparison**: Ours (~0.21) and -critiquing (~0.19) have the smallest difference at approximately 0.02.
- **pattern_analysis**: No, the heights are non-monotonic: they decrease from Ours to -scoring then increase to -ranking.

## fig_100
- **counting**: 1 intersection occurs between the teal and red lines in the Easy Training Set plot, around step 100-150.
- **computation**: Llama-LUFFY-Easy increases from approximately 0.0 to 0.4 over 500 steps, but percentage increase is undefined from a zero baseline.
- **comparison**: Ranked by final rewards at step 500: Llama-LUFFY-Easy (~0.40) > Llama-On-Policy-Easy (~0.35) > Llama-LUFFY-Hard (~0.20) > Llama-On-Policy-Hard (~0.0).
- **pattern_analysis**: Yes, Llama-On-Policy-Hard exhibits an inflection point around step 100 where rewards briefly increase then sharply decrease to near zero.
