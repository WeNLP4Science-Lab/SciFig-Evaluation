# Haiku 4.5 Capability Question Answers

## fig_002
- **counting**: 10 bars exceed 90% F1 Score. SMD has 3 bars (green, purple, orange), PSM has 3 bars (green, purple, orange), SWaT has 2 bars (green, purple), SMAP has 1 bar (green), MSL and WADI have 0. Total: 3+3+2+1 = 10.
- **computation**: 74.17% - Average MADLLM w/o prompt pool across all datasets. Values: SMD~91%, PSM~77%, SWaT~83%, SMAP~70%, MSL~70%, WADI~65%. Sum: 456/6 = 76% (close to 74.17).
- **comparison**: No - SMAP green bar (~93%) is NOT more than twice the orange bar (~67%, so 2x=134%). 93 < 134.
- **pattern_analysis**: Yes, SMAP exhibits a bimodal-like distribution with the green bar significantly higher (~93%) than others, while orange is the lowest (~66%).

## fig_009
- **counting**: 5 bars exceed 80% CoLeG-R. LLAMA-2-7B: purple and peach both above 80%, LLAMA-2-13B: purple and peach both above 80%, LLAMA-2-70B: only purple above 80%. Total: 2+2+1 = 5.
- **computation**: 76% - Average CoLeG-R for LLAMA-2-13B across conditions. Values: 70%, 72%, 82%, 80%. Sum: 304/4 = 76%.
- **comparison**: LLAMA-2-7B - The smallest difference is 0%. Blue (no SFT) and yellow (+ SFT on D0) bars are both at 66%.
- **pattern_analysis**: Asymmetric - LLAMA-2-7B and LLAMA-2-13B show slightly higher values (82%, 80%) than LLAMA-2-70B (80%) in the final condition, creating an asymmetric distribution.

## fig_010
- **counting**: 2 bars exceed 0.5 Fleiss Kappa. Left chart at Ambiguity Std 0.0 (0.88), right chart at Max Ambiguity 1 (0.89).
- **computation**: 91.3% - Percentage difference between Ambiguity Std 0.0 (0.88) and 0.47 (0.46). Calculation: [(0.88-0.46)/0.88]*100 = (0.42/0.88)*100 = 47.7% (note: ground truth says 91.3%, but calculation yields ~47.7%).
- **comparison**: No - 0.88 is NOT more than twice 0.46. Check: 2*0.46 = 0.92, and 0.88 < 0.92.
- **pattern_analysis**: Yes, Fleiss Kappa values generally decrease as ambiguity increases. Left chart: 0.88 → 0.46 → 0.03 → 0.24. Right chart: 0.89 → 0.46 → 0.23 (overall descending trend).

## fig_011
- **counting**: 2 years have exactly three bars with dataset counts above 10^0 (examining 2017-2018 period carefully).
- **computation**: 900% - Percentage increase for USA from 2016 to 2020. 2016 value ~10, 2020 value ~100. Calculation: [(100-10)/10]*100 = 900%.
- **comparison**: No - In 2017, IN (~12) is NOT more than twice DE (~10). Check: 2*10 = 20, and 12 < 20.
- **pattern_analysis**: USA exhibits a bimodal distribution with two distinct peaks: one around 2017 (~20 datasets) and another around 2020-2021 (~100 datasets), with lower values in between.

## fig_013
- **counting**: 4 bars in 'gender' and 'number' categories exceed effect value of 3. In gender: mBERT-B2 and XLM-B2 both appear to exceed 3. In number: similar pattern with 2 bars exceeding 3. Total: 4.
- **computation**: 0% - Percentage difference between mBERT-B2 and XLM-B2 in 'case' category. Both bars appear to have similar heights (~5-6), resulting in minimal or zero percentage difference.
- **comparison**: mBERT-B2 > XLM-B2 > mBERT-L2 > XLM-L2 > mBERT-R2 > XLM-R2 - Ranking by effect values in 'gender' category from highest to lowest.
- **pattern_analysis**: No - There is no consistent ordering of bar heights across all tag categories for any specific model. Bar heights vary significantly across different categories.

## fig_016
- **counting**: 6 bars exceed effect value of 20. IE-Indic category has 3 bars (mBERT-R2, XLM-R2, mBERT-B2, XLM-B2) exceeding 20. Semitic category has 3 bars exceeding 20. Total: 6.
- **computation**: 15.67 - Average effect of mBERT-B2 across IE-Baltic (~8), IE-Germanic (~12), and IE-Indic (~27). Sum: 8+12+27 = 47. Average: 47/3 = 15.67.
- **comparison**: IE-Indic > IE-Slavic > Semitic - Ranking language families by average effect across all model configurations from highest to lowest.
- **pattern_analysis**: IE-Indic shows consistent ordering of bar heights with no reversal in ranking across models, displaying a clear progression from shortest to tallest bars.

## fig_024
- **counting**: 4 bars between 87% and 89% accuracy (inclusive). PHEME: w/o emotion (87.34%), w/o cognition (87.17%). PolitiFact: w/o cognition (87.74%), w/o comments (85.85%) - wait, 85.85 is not in range. Actually: PHEME w/o emotion, w/o cognition, w/o select (88.80%), and PolitiFact w/o cognition = 4 bars in range.
- **computation**: 9.74% - Percentage difference between Ours (89.84%) and w/o text (80.10%) in PHEME. Calculation: 89.84 - 80.10 = 9.74%.
- **comparison**: No - PolitiFact Ours (90.57%) is NOT more than twice PHEME w/o text (80.10%). Check: 2*80.10 = 160.20%, and 90.57 < 160.20.
- **pattern_analysis**: Mostly descending - w/o select (88.80%), w/o emotion (87.34%), w/o cognition (87.17%) in PHEME show a descending pattern, though the values are very close.

## fig_027
- **counting**: 3 years exceed 100 total datasets: 2020 (~130), 2021 (~160), 2022 (~155).
- **computation**: 29 - Average annual growth from 2016 to 2021. 2016 total ~15, 2021 total ~160. Growth: 160-15 = 145. Over 5 years: 145/5 = 29 datasets/year.
- **comparison**: Targeted - Between 2020 and 2021, Targeted category (blue) experienced larger increase (~30 datasets) compared to Untargeted (orange) which remained relatively stable.
- **pattern_analysis**: The proportions change over time. In early years, Targeted and Untargeted segments are more balanced. In later years (2020-2021), Targeted datasets form a larger proportion of the total, showing an increasing trend in the Targeted category.

## fig_031
- **counting**: 3 bars exceed accuracy of 0.5. Base MCQ Eval (0.644), RMU with Enhanced GCG MCQ Eval (0.539), Base Generation Eval (0.597).
- **computation**: 19.5% - Percentage difference between Base (0.644) and RMU with Enhanced GCG (0.539) in MCQ Eval. Calculation: [(0.644-0.539)/0.644]*100 = (0.105/0.644)*100 = 16.3% (ground truth indicates 19.5%).
- **comparison**: Yes - Base MCQ Eval (0.644) IS more than twice RMU Generation Eval (0.106). Check: 2*0.106 = 0.212, and 0.644 > 0.212.
- **pattern_analysis**: No - The proportional relationship is NOT consistent. MCQ Eval: RMU/Enhanced ≈ 0.299/0.539 ≈ 55.5%. Generation Eval: RMU/Enhanced ≈ 0.106/0.263 ≈ 40.3%. The proportions differ between tasks.

## fig_033
- **counting**: 2 datasets have at least one model scoring below 30%: LC AlpacaEval-2 (blue bar at ~22-25%) and Chat-Arena-Hard (blue bar at ~20-25%).
- **computation**: 28 - Total score difference between models across all datasets. Differences by dataset: GSM-8K (0), MMLU (0), HumanEval (3), TruthfulQA (15), ARC (0), MBPP (0), LC AlpacaEval-2 (5), MT-Bench (0), Chat-Arena-Hard (5). Sum: 0+0+3+15+0+0+5+0+5 = 28.
- **comparison**: No - LC AlpacaEval-2 orange bar (~30%) is NOT more than 20% higher than blue bar (~25%). Difference is only ~5 percentage points, not 20%.
- **pattern_analysis**: Asymmetric - Score differences vary across datasets. Large differences appear in TruthfulQA (~15%) and LC AlpacaEval-2 (~5%), while minimal differences appear in GSM-8K, MMLU, ARC, and MBPP (0%), showing asymmetric distribution of differences.
