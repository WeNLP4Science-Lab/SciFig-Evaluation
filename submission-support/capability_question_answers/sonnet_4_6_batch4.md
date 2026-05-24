# Capability Question Answers — Batch 4 (fig_151–fig_200)
Model: claude-sonnet-4-6

---

## fig_151
- **counting**: The 'attn_residual' (orange dotted) and 'ffn_residual' (red solid) lines never cross; there are 0 intersections.
- **computation**: attn_output averages ~50 and ffn_output averages ~104 across layers 20–23, giving a difference of approximately 54.
- **comparison**: 'ffn_residual' shows a greater increase between layers 20 and 23, rising from ~200 to ~380 versus 'attn_residual' rising from ~150 to ~250.
- **pattern_analysis**: Both 'attn_residual' and 'ffn_residual' exhibit quadratic-like growth, but 'ffn_residual' grows faster and reaches a higher maximum (~380) compared to 'attn_residual' (~250).

---

## fig_152
- **counting**: There are 9 data points at cost values 2, 5, and 10 across all three lines (3 lines × 3 cost values).
- **computation**: At cost 5, 2-Model Ensemble scores ~87 and 3-Model Ensemble scores ~80; the difference is ~7, which is 7/80 ≈ 0.0875 of the 3-Model Ensemble's score.
- **comparison**: Between costs 0 and 5, the 3-Model Ensemble and 2-Model Ensemble show the smallest gap, as both lines remain closest to each other throughout.
- **pattern_analysis**: The yellow (GPT-4) line decreases at a much faster rate than the blue and red lines between costs 0 and 5, dropping ~25 points while the others drop only ~5–7 points.

---

## fig_153
- **counting**: 2 data points on the 'Initial Accuracy' line exceed 0.5 (at x=13 and x=5 approximately, visible as the two highest green markers).
- **computation**: Maximum 'Final Accuracy' is ~0.90 and maximum 'Initial Accuracy' is ~0.55, giving a difference of approximately 0.35.
- **comparison**: The difference at x=13 (~0.35) is slightly smaller than the difference at x=15 (~0.40), so the difference at x=13 is smaller than at x=15.
- **pattern_analysis**: The largest error bars for both lines occur at x=13, with 'Final Accuracy' showing slightly larger error bars than 'Initial Accuracy' at that point.

---

## fig_154
- **counting**: The blue line (Inconsistency-CE-MP) intersects 2 other lines across the plot (the Consistency-CE line and the Inconsistency-CE line near AL 3–5).
- **computation**: At AL 6, Consistency-CE scores ~30 and Inconsistency-CE-MP scores ~28; the difference is 2, and 2/28 ≈ 0.071 of the Inconsistency-CE-MP score.
- **comparison**: At AL=3, Consistency-Bi scores ~28, which is not more than twice Consistency-CE's score of ~23 (twice would be 46); the answer is No.
- **pattern_analysis**: Consistency-Bi (red line with star markers) shows a consistent upward trend without inflection points, while other lines intersect or change relative positions.

---

## fig_155
- **counting**: The 'Vanilla' (purple) line has 4 data points with loss values below 2.55.
- **computation**: At ~0.90 TFLOPs, both Vanilla and SepLLM are approximately 2.50, so the percentage reduction is near 0%; the 1.28× annotation indicates SepLLM reaches 2.50 loss at ~0.78× the TFLOPs Vanilla needs.
- **comparison**: At 1.23 TFLOPs, SepLLM loss (~2.47) is less than 1.28 times Vanilla's loss (~2.50), so Yes, the condition is satisfied.
- **pattern_analysis**: The two lines converge toward a similar loss value at approximately 1.23×10⁹ TFLOPs, where SepLLM achieves ~2.47 and Vanilla achieves ~2.50.

---

## fig_156
- **counting**: The 'tiny AdaLoRA_int4' and 'tiny int4' lines intersect once, at approximately epoch 3.
- **computation**: 'tiny int4' reduces from ~69 to ~40 (reduction 29); 'tiny int8' reduces from ~60 to ~37 (reduction 23); the difference is approximately 6.
- **comparison**: 'tiny AdaLoRA_int8' experienced a larger absolute reduction (from ~60 to ~32 = 28 units) versus 'tiny full' (from ~29 to ~23 = 6 units).
- **pattern_analysis**: 'tiny int4' and 'tiny int8' converge at approximately epoch 4, with a WER value of around 40.

---

## fig_157
- **counting**: 4 bars have a count greater than 30: RR and WW for GPT3.5, and RR for Mistral 7B (WW for Mistral 7B is ~30, borderline).
- **computation**: RR for GPT3.5 is ~122 and for Mistral 7B is ~115; the absolute difference is ~7, and (7/115)×100 ≈ 6.1%.
- **comparison**: RR for GPT3.5 (~122) is more than twice WW for Mistral 7B (~30), since 2×30=60 < 122; Yes.
- **pattern_analysis**: The heights for Type1 and Type2 bars remain similarly spaced across both models, showing a roughly parallel (convergent in relative terms) pattern.

---

## fig_158
- **counting**: There are 3 data points at x=200, one for each line (Accuracy, Confidence, Alignment).
- **computation**: Confidence at 50 (~0.8) + at 200 (~0.8) = 1.6; Alignment at 50 (~0.4) + at 200 (~0.75) = 1.15; difference ≈ 0.45.
- **comparison**: At x=200, alignment (~0.75) is NOT more than twice accuracy (~0.55), since 2×0.55=1.10 > 0.75; the answer is No.
- **pattern_analysis**: Accuracy (blue line) exhibits a non-monotonic trend, dropping initially then rising then leveling off, unlike Confidence and Alignment which increase more monotonically.

---

## fig_159
- **counting**: The 'Vanilla' (purple) line has 3 data points above loss 2.60.
- **computation**: Vanilla reaches loss 2.50 at ~1.28×10⁹ TFLOPs and SepLLM at ~1.00×10⁹; the ratio is 1.28/1.00 = 1.28.
- **comparison**: At the green dashed line intercepts, both lines reach 2.50 loss; SepLLM achieves this at fewer TFLOPs, meaning SepLLM achieves an equal or greater reduction relative to its starting point.
- **pattern_analysis**: From 0.25 to 0.75 TFLOPs, 'SepLLM' decreases at a faster rate than 'Vanilla', as shown by the steeper slope of the red line in that interval.

---

## fig_160
- **counting**: 6 data points across all models exceed perplexity 30 (Vicuna-7B has all 6 points above 30, LLaMA1-7B and LLaMA1-13B none exceed 30 in this figure; Vicuna-7B values range ~34–41).
- **computation**: Vicuna-7B perplexity drops from ~41 at M=3 to ~33 at M=7; percentage decrease = (41−33)/41 × 100 ≈ 19.5%.
- **comparison**: At M=3, LLaMA1-13B perplexity (~20) is less than half of Vicuna-7B perplexity (~41/2=20.5); Yes.
- **pattern_analysis**: LLaMA1-13B and LLaMA1-7B both exhibit convergence as M increases, stabilizing near ~17 and ~25 respectively at M=8.

---

## fig_161
- **counting**: The 'SepLLM' line crosses the green dashed horizontal line at loss=2.50 exactly 1 time.
- **computation**: At 50,000s, Vanilla−SepLLM ≈ 0.02; at 150,000s ≈ 0.03; average difference ≈ 0.025.
- **comparison**: At 250,000 seconds, SepLLM achieves ~2.49 loss, which is ~0.01 lower than Vanilla's ~2.50.
- **pattern_analysis**: The two methods are closest around 200,000 seconds training time, after which SepLLM continues to decrease slightly more steeply than Vanilla.

---

## fig_162
- **counting**: 4 data points exceed a Harmful with Refusal Ratio of 0.4: red line at 512 (~0.42) and 1024 (~0.52), orange line at 512 (~0.42), and green line at 512 (~0.37 — borderline, but visually at or just below 0.40).
- **computation**: Qwen2-VL-7B on MMSafetyBench values at 128, 256, 512, 1024 are ~0.245, 0.27, 0.42, 0.52; average = (0.245+0.27+0.42+0.52)/4 ≈ 0.364.
- **comparison**: At 1024, red line (~0.52) vs green line (~0.38); 1.5×0.38=0.57 > 0.52, so No, the red line is not more than 1.5× the green line.
- **pattern_analysis**: The green line (LLaVA-1.5-7B on MMSafetyBench) shows the fastest rate of increase between sample sizes 128 and 256, rising from ~0.065 to ~0.22.

---

## fig_163
- **counting**: The blue line maintains accuracy above 0.95 at all 7 tick markers on the x-axis (0.91 through 0.98).
- **computation**: Green line at x=0.93 is ~0.20 and at x=0.98 is ~0.91; percentage difference = (0.91−0.20)/0.20 × 100 ≈ 355%.
- **comparison**: Between x=0.95 and x=0.96, the blue line shows the smallest change in accuracy, remaining nearly constant near 1.0.
- **pattern_analysis**: The green and orange lines converge most closely around x=0.95, where their accuracy values are nearest to each other.

---

## fig_164
- **counting**: 8 data points across all lines have average performance above 50%: Precision (red) has 7 points above 50%, and F1-score (purple) has 1 point above 50% at 7.0B.
- **computation**: Recall at 70m (~10%) to 7.0B (~45%); percentage increase = (45−10)/10 × 100 = 350%.
- **comparison**: Between 1.0B and 1.4B, Precision (red line) shows the smallest change, remaining nearly flat.
- **pattern_analysis**: The metrics diverge as model size increases; at 7.0B, the gap between Precision (~78%) and Recall (~45%) is approximately 33 percentage points.

---

## fig_165
- **counting**: TrajICL (blue line) is the only method with values below 20, with approximately 7 data points below 20 (from ratio 0.1 onwards it stays below 21).
- **computation**: LoRA 16 values across 5 ratio points are approximately 22.9, 22.8, 22.4, 22.2, 22.1; average ≈ 22.48.
- **comparison**: At Ratio 0.4, TrajICL (~19.3) vs FT gap (~21.0−19.3=1.7) is larger than LoRA 16 (~22.4) vs LoRA 64 (~22.5) gap (~0.1); Yes, the TrajICL–FT gap is larger.
- **pattern_analysis**: TrajICL (blue line) exhibits a consistent downward trend across the entire range of the Ratio axis, decreasing from ~20.5 at 0.1 to ~18.1 at 1.0.

---

## fig_166
- **counting**: All three lines are below 0.1 from approximately layer 10 onwards, giving about 14 layers (layers 10–23) where all three are below 0.1.
- **computation**: Orange dotted line at layer 0 is ~0.83 and at layer 5 is ~0.10; percentage decrease = (0.83−0.10)/0.83 × 100 ≈ 87.9%.
- **comparison**: At layer 20, orange dotted (~0.06) is approximately twice green dash-dot (~0.02–0.03); Yes, it is more than twice.
- **pattern_analysis**: The green dash-dot line decreases more rapidly than the orange dotted line between layers 0 and 5, dropping from ~0.83 to near 0 faster.

---

## fig_167
- **counting**: The LUFFY (red star) line has accuracy above 75.0 at all 10 temperature points shown (0.1 through 1.0); approximately 9–10 points exceed 75.0.
- **computation**: On-policy RL at temperature 0.1 is ~63 and peaks at temperature 0.8 at ~75; percentage increase = (75−63)/63 × 100 ≈ 19.0%.
- **comparison**: At temperature 0.8, LUFFY (~81) is not more than twice On-policy RL (~75), since 2×75=150 > 81; No.
- **pattern_analysis**: All three lines show closest convergence near temperature 0.8, where On-policy RL peaks (~75), SFT recovers (~74), and LUFFY is ~81.

---

## fig_168
- **counting**: 1 data point is located at approximately 40% accuracy, on the orange line (PLLaVA DP 8) at the rightmost frame count.
- **computation**: At 30 frames, Ours (Dynamic Seg) scores ~54% and PLLaVA (DP 8) scores ~43%; difference ≈ 11%.
- **comparison**: Between 10 and 60 frames, PLLaVA (DP 8) shows the largest decrease, dropping from ~45% to ~39.5%, a decrease of ~5.5%.
- **pattern_analysis**: PLLaVA (DP 8) (orange line) shows the steepest rate of decline in accuracy as the number of frames increases.

---

## fig_169
- **counting**: 3 data points on the orange (Perplexity) line fall below the red dashed Full Cache PPL line (~4.38), at approximately 20%, 30%, and 40% recent sequence ratio.
- **computation**: Perplexity at 5% is ~4.60 and at 40% is ~4.30; percentage decrease = (4.60−4.30)/4.60 × 100 ≈ 6.5%.
- **comparison**: At 100% recent sequence ratio, both metrics equal their reference lines; the GPU memory ratio aligns perfectly with Full Cache GPU Mem, while perplexity equals Full Cache PPL.
- **pattern_analysis**: Between 80% and 100% recent sequence ratio, the blue line (GPU Mem. Ratio) increases at a much faster rate than the orange line (Perplexity).

---

## fig_170
- **counting**: 1 data point is located exactly at the accuracy threshold of 55 (Squared Exponential at 250 demonstrations).
- **computation**: Squared Exponential at 0 demonstrations is ~52 and at 250 demonstrations is ~55.5; percentage increase ≈ (55.5−52)/52 × 100 ≈ 6.7%.
- **comparison**: At 250 demonstrations, Squared Exponential (~55) is not more than twice LLaMA-2-chat-7B (~43), since 2×43=86 > 55; No.
- **pattern_analysis**: The greatest divergence among all models occurs at 250 demonstrations, where Squared Exponential peaks above 55 while LLaMA-2-chat-7B remains flat at ~43.

---

## fig_171
- **counting**: The NIPS (blue) line has 4 data points above NPMI 0.40 (at weights 0.5, 1.0, 1.5, 2.0).
- **computation**: NIPS at weight 0.5 is ~0.400 and at peak (weight 1.0–1.5) is ~0.410; percentage increase ≈ (0.410−0.400)/0.400 × 100 ≈ 2.5%.
- **comparison**: At weight 1.5, NIPS (~0.410) is more than twice IMDB (~0.195), since 2×0.195=0.390 < 0.410; Yes.
- **pattern_analysis**: NIPS (blue line) exhibits a non-monotonic trend, increasing from weight 0.5, peaking around weight 1.0–1.5, then decreasing slightly through weight 3.0.

---

## fig_172
- **counting**: The Confidence (green) line has 3 data points within 0.01 of the maximum value (≥0.99), at Question Popularity ~17, ~20, and ~26.
- **computation**: Maximum Confidence is ~0.98 at x=26; minimum Accuracy is ~0.60 at x=5; difference ≈ 0.38.
- **comparison**: At Question Popularity 5, Confidence (~0.93) is not more than twice Accuracy (~0.60), since 2×0.60=1.20 > 0.93; No.
- **pattern_analysis**: Between Question Popularity 15 and 25, Accuracy (blue) shows the fastest rate of increase, rising from ~0.72 to ~0.88, while Alignment increases gradually and Confidence remains nearly steady.

---

## fig_173
- **counting**: The two lines intersect at 1 x-value, around x=9 (gold prefix length ~9).
- **computation**: Consistency: wait-1 at x=0 is ~24.7 and at x=20 is ~28; percentage increase ≈ (28−24.7)/24.7 × 100 ≈ 13.4%.
- **comparison**: Between x=15 and x=20, Consistency: wait-1 increases by ~2 (26→28) while Inconsistency: wait-9 increases by ~0.5 (25.5→26); Yes, the wait-1 increase is more than twice the wait-9 increase.
- **pattern_analysis**: From x=15 to x=20, Consistency: wait-1 increases sharply (~2 BLEU points) while Inconsistency: wait-9 remains nearly flat around 26 BLEU.

---

## fig_174
- **counting**: 2 data points have Missing Step values greater than 0.855: one on 0-CoT and one on CoRe, both at x=0 (~0.859).
- **computation**: 0-CoT values at x=0,1,2,3,4 are ~0.859, 0.854, 0.850, 0.847, 0.844; average ≈ 0.8508.
- **comparison**: At x=4, 0-CoT (~0.844) is not less than half of CoRe (~0.848), since half of 0.848=0.424 < 0.844; No.
- **pattern_analysis**: The two methods diverge as x increases; 0-CoT continues to decrease while CoRe levels off, with the divergence most pronounced at x=4.

---

## fig_175
- **counting**: The Confidence (green) line has 2 data points within 0.05 of 0.9 (between 0.85 and 0.95), at approximately question popularity 5 and 6.
- **computation**: Confidence rate = (0.94−0.72)/20=0.011; Accuracy rate = (0.71−0.21)/20=0.025; difference ≈ 0.014.
- **comparison**: At question popularity 25, Confidence (~0.94) is not more than twice Accuracy (~0.71), since 2×0.71=1.42 > 0.94; No.
- **pattern_analysis**: As question popularity increases, all three lines rise but Confidence (green) diverges upward from Accuracy and Alignment, with the gap widening most noticeably after popularity ~10.

---

## fig_176
- **counting**: The shaded areas of the two lines overlap at approximately 4 x-axis positions (around 0.7, 0.8, 0.9, and 1.0 tokens).
- **computation**: MATTER (ours) average across roughly 4 visible key points (~55, 57, 56, 53) ≈ 55.25%; w/o material information at same points (~52.5, 53, 53, 48) ≈ 51.6%.
- **comparison**: At x=1.4, MATTER (~51%) is not more than twice w/o material information (~48%), since 2×48=96 > 51; No.
- **pattern_analysis**: The two lines diverge overall, with the closest approach occurring near x=1.2–1.3 tokens where the gap between them narrows before widening again at x=1.5.

---

## fig_177
- **counting**: 3 lines (TrajICL, FT, and LoRA 16) have at least one data point with minFDE20 below 0.9.
- **computation**: FT at ratio 0.1 is ~1.09 and at ratio 1.0 is ~0.76; percentage decrease = (1.09−0.76)/1.09 × 100 ≈ 30.3%.
- **comparison**: Between ratios 0.2 and 0.8, FT shows the largest absolute decrease, dropping from ~0.99 to ~0.83 (change of ~0.16).
- **pattern_analysis**: FT (green line) shows the steepest rate of decrease in minFDE20 between ratios 0.0 and 0.4, dropping rapidly from ~1.09 to ~0.90.

---

## fig_178
- **counting**: 5 data points across all lines have ROUGE-1 ≥ 30: MBart + AdaLoRA has 3 points (at log r = 4, 5, 6+) and T5 + AdaLoRA has 2 points (at log r = 8, 9).
- **computation**: MBart + AdaLoRA at log r=0 is ~5 and at log r=4 is ~32; percentage increase = (32−5)/5 × 100 = 540%.
- **comparison**: MBart + AdaLoRA at x=4 (~32) is more than twice MBart + LoRA at x=2 (~3), since 2×3=6 < 32; Yes.
- **pattern_analysis**: MBart + AdaLoRA demonstrates the fastest rate of increase between log r=0 and log r=4, rising sharply from ~5 to ~32 while other methods show smaller, steadier changes.

---

## fig_179
- **counting**: The language lines intersect each other at approximately 2 points (Spanish crosses Korean once, and Japanese crosses Korean once, both early in training).
- **computation**: Japanese at 500 iterations is ~3150 and Korean is ~2900; percentage difference = (3150−2900)/2900 × 100 ≈ 8.6%.
- **comparison**: At 500 iterations, Korean (~2900) and Spanish (~3150) differ by ~250, which is greater than 100; No, the difference is not less than 100 — the difference exceeds 100.
- **pattern_analysis**: All three language lines exhibit approximately linear trends, sub-linear relative to the gray 1:1 reference line, with no visible non-linear deviations.

---

## fig_180
- **counting**: 6 data points across all three lines exceed 0.98: green (Confidence) has 3, red (Alignment) has ~2, and blue (Accuracy) has ~1.
- **computation**: Maximum Confidence is ~0.99 at popularity 55; minimum Alignment is ~0.92 at popularity 15; difference ≈ 0.07.
- **comparison**: At question popularity 20, Alignment (~0.94) is closer to Accuracy (~0.96) than to Confidence (~0.975), with differences of 0.02 vs 0.035 respectively.
- **pattern_analysis**: Between question popularities 15 and 25, the blue line (Accuracy) demonstrates the fastest rate of increase, rising steeply from ~0.895 to ~0.96.

---

## fig_181
- **counting**: The 'end' (purple) line has 3 keywords with ASR above 0.8: 'brilliant', 'stunning', and 'beautifully'.
- **computation**: 'random' line at 'cf' is ~0.20 and at 'beautiful' is ~0.60; percentage increase = (0.60−0.20)/0.20 × 100 = 200%.
- **comparison**: Between 'gorgeous' and 'wonderful', the 'random' line shows the smallest increase in ASR (~0.05 versus ~0.10 for 'start').
- **pattern_analysis**: The 'random' (orange/cross) line demonstrates a non-monotonic pattern, dropping sharply from 'mb' to 'cf' before increasing again from 'cf' to 'beautiful'.

---

## fig_182
- **counting**: At 'bb' and 'mb', all three lines (start, random, end) have ASR values below 0.5; 2 words meet this criterion.
- **computation**: 'random' at 'bb' is ~0.10 and at 'beautiful' is ~0.60; percentage increase = (0.60−0.10)/0.10 × 100 = 500%.
- **comparison**: The 'start' and 'end' lines show the smallest difference in ASR values at 'beautifully', where both are near 0.90–0.92.
- **pattern_analysis**: All three lines converge most closely at 'beautifully', with an approximate ASR value of ~0.90 for all three.

---

## fig_183
- **counting**: The Regularization Loss (purple) line exhibits approximately 3 visible peaks in its shaded region, at roughly steps 50, 400, and 800.
- **computation**: Reconstruction Loss at step 0 is ~7.8 and at step 1000 is ~0.65; percentage decrease ≈ (7.8−0.65)/7.8 × 100 ≈ 91.7%.
- **comparison**: Task Loss starts at ~3.0 at step 0; Regularization Loss peaks between steps 0 and 200 at ~4.8, which exceeds 2×3.0=6.0? No — 4.8 < 6.0; actually No, the peak does not exceed twice the starting Task Loss.
- **pattern_analysis**: Regularization Loss (purple line) exhibits the most pronounced oscillations, with the largest peaks and troughs most evident between steps 0 and 200.

---

## fig_184
- **counting**: 7 data points across all lines have AUC ≥ 95%: blue at N=5 and N=10, orange at N=10 and N=15, green at N=15, yellow at N=10 (borderline), and magenta at N=10.
- **computation**: Average AUC at N=10 across 5 datasets: ~98, 97, 92, 96, 95; average = (98+97+92+96+95)/5 = 95.6%.
- **comparison**: Between N=15 and N=20, the blue line (circle markers) and orange/yellow line show the smallest difference in AUC values, remaining nearest to each other.
- **pattern_analysis**: The green line (star markers) shows the slowest and most consistent increase in AUC across the entire range of N, with a gradual, steady slope.

---

## fig_185
- **counting**: 5 epochs have BLEU score above 0.1 for 'Members with near-duplicates' (at epochs 1.0, 1.5, 2.0, 2.5, and 3.0).
- **computation**: 'Members with near-duplicates' at epoch 1 is ~0.15 and at epoch 3 is ~0.36; percentage increase = (0.36−0.15)/0.15 × 100 = 140%.
- **comparison**: At epoch 3.0, 'Members with near-duplicates' (~0.36) is more than five times 'Held-out data' (~0.035), since 5×0.035=0.175 < 0.36; Yes.
- **pattern_analysis**: The orange line ('Members with near-duplicates') exhibits the steepest rate of increase between epochs 1 and 2, where the BLEU score rises most sharply.

---

## fig_186
- **counting**: 3 lines have at least one data point below minADE20=0.60: FT (green), LoRA 16 (red, at ratio 1.0 borderline), and LoRA 64 (purple, at ratio 1.0 borderline).
- **computation**: LoRA 16 values across all ratios are approximately 0.745, 0.700, 0.670, 0.640, 0.615, 0.600; average ≈ 0.662.
- **comparison**: FT shows the largest absolute decrease in minADE20 between ratios 0.0 and 1.0, dropping from ~0.69 to ~0.52 (change of ~0.17).
- **pattern_analysis**: TrajICL (blue line) exhibits a non-monotonic trend, showing small fluctuations rather than a consistent decrease across the ratio range.

---

## fig_187
- **counting**: 6 data points across all lines have BLEU ≥ 26: Consistency-Bi (red) has 3, Inconsistency-CE-MP (blue) has 2, and Inconsistency-CE (dark purple) has 1.
- **computation**: Inconsistency-CE-MP BLEU values at AL 0.5, 1.5, 3, 5, 7 are approximately 20, 20, 22.7, 25, 27; average ≈ 22.9.
- **comparison**: At AL=3, ranked highest to lowest: Consistency-Bi (~25.5) > Inconsistency-CE-MP (~22.7) ≈ Inconsistency-CE (~22.7) > Consistency-CE (~20).
- **pattern_analysis**: Consistency-CE (light purple dashed) shows a non-monotonic trend with an initial steep rise from AL −0.5 to AL 0.5, followed by a slower but more linear increase.

---

## fig_188
- **counting**: 1 data point on 'NDCG@50 (Ours)' is within 0.01 of the NDCG@50 (ReFICR) constant value (~0.155), at x=1 (~0.16).
- **computation**: Recall@50 (Ours) sum at x=1–5 ≈ 0.35+0.43+0.47+0.48+0.49=2.22; Recall@50 (ReFICR) = 0.47×5=2.35; difference ≈ 0.13.
- **comparison**: Recall@50 (Ours) at x=5 (~0.49) is more than twice NDCG@50 (ReFICR) (~0.155), since 2×0.155=0.31 < 0.49; Yes.
- **pattern_analysis**: The greatest rate of convergence between 'Recall@50 (Ours)' and 'NDCG@50 (Ours)' occurs at x=2, where the Recall line rises steeply before leveling off.

---

## fig_189
- **counting**: There is 1 x-axis position where ST-ES and Random have the same minFDE20 value, where the lines cross at approximately x=0 (they start nearly at the same value) — actually they appear to intersect around x=0.
- **computation**: ST-ES at 0 examples is ~0.243 and at 4 examples is ~0.207; percentage decrease = (0.243−0.207)/0.243 × 100 ≈ 14.8%.
- **comparison**: Between x=2 and x=8, the Random method does not achieve a lower minFDE20 value than ST-ES; No.
- **pattern_analysis**: The ST-ES line shows a rapid decreasing trend from x=0 to x=1, then stabilizes and fluctuates slightly between ~0.207–0.214 from x=1 to x=8.

---

## fig_190
- **counting**: The Linear method's training accuracy drops below 0.6 approximately 2 times after epoch 200 (visible dips around epoch 300–350).
- **computation**: C³A_b=128/2 at epoch 50 is ~0.95 and LoRA_r=1 at epoch 50 is ~0.55; ratio ≈ 0.95/0.55 ≈ 1.73.
- **comparison**: Between epochs 300 and 400, the 'Linear' method does not increase by more than twice the 'LoRA_r=1' increase; No.
- **pattern_analysis**: C³A_b=128/2 (pink/maroon line) exhibits the most consistent trend after epoch 100, stabilizing near 1.0 with minimal fluctuations.

---

## fig_191
- **counting**: 3 data points across all lines exceed PPL=8.0, one for each line (γ=0.25, 0.5, 0.75) at 2K evaluation context length.
- **computation**: γ=0.25 at 2K is ~8.20 and at 8K is ~7.84; percentage decrease = (8.20−7.84)/8.20 × 100 ≈ 4.4%.
- **comparison**: Between 2K and 8K, γ=0.75 (green) shows the largest absolute decrease, dropping from ~8.20 to ~7.74 (change of ~0.46).
- **pattern_analysis**: The three lines converge as evaluation context length increases; at 64K, green (γ=0.75) has the lowest PPL, followed by orange (γ=0.5), then blue (γ=0.25).

---

## fig_192
- **counting**: 4 data points exceed Pass@1 Rate of 50%: GPT-4o at 20 steps (77.4%) and 40 steps (83.9%), Claude-3.5-Sonnet at 20 steps (87.1%) and 40 steps (89.2%).
- **computation**: GPT-4o at 20 steps = 77.4%; Claude-3.5-Sonnet at 20 steps = 87.1%; percentage difference = (87.1−77.4)/77.4 × 100 ≈ 12.5%.
- **comparison**: Ascending order at 5, 10, 20 steps: 6.5% (GPT-4o@5), 19.4% (Claude@5), 32.3% (GPT-4o@10), 38.7% (Claude@10), 77.4% (GPT-4o@20), 87.1% (Claude@20).
- **pattern_analysis**: The largest divergence between the two models occurs at 5 reasoning steps, where the gap is 19.4%−6.5% = 12.9 percentage points.

---

## fig_193
- **counting**: 6 data points across all lines have WER > 35: small int4 has 3 points (epochs 1, 2, 3 visible above 35) and small AdaLoRA_int4 has ~2 points plus small int8 has 1 point at epoch 0.
- **computation**: small AdaLoRA_int4 reduces from ~35.8 to ~31.0 (−4.8); small int8 reduces from ~30.2 to ~25.1 (−5.1); difference ≈ 0.3.
- **comparison**: small int8 at epoch 6 (~25.1) is not less than half of small int4 at epoch 2 (~42); half of 42=21 < 25.1; No.
- **pattern_analysis**: The 'small int4' configuration (dashed orange circle line) exhibits a non-monotonic trend, rising from epoch 0 to a peak at epoch 2 (~42) before decreasing.

---

## fig_194
- **counting**: The 'w/o Pre-computation' (blue) line exceeds 10 seconds at Paper Numbers 32, 64, 128, and 256 — approximately 4 paper numbers.
- **computation**: At Paper Number 256, w/o Pre-computation is ~35s and w Pre-computation is ~1s; ratio ≈ 35.
- **comparison**: At Paper Number 256, w/o Pre-computation (~35s) is more than 10 times w Pre-computation (~1s); Yes.
- **pattern_analysis**: The 'w/o Pre-computation' rate of change rises sharply (exponentially) between Paper Numbers 64 and 256, while 'w Pre-computation' remains nearly constant near 0–1 second.

---

## fig_195
- **counting**: 3 data points exceed PPL=13.0: Only MoHD ATTN at 25% (~14.4), and MoHD ATTN + MLP at 25% (~13.2) and at 50% (~12.2 — borderline, just above 12.0 not 13.0).
- **computation**: Only MoHD ATTN at 100% is ~11.5 and at 25% is ~14.4; percentage increase = (14.4−11.5)/11.5 × 100 ≈ 25.2%.
- **comparison**: Between 100% and 25%, Only MoHD ATTN shows the largest increase in Eval PPL, rising ~2.9 points versus MoHD ATTN + MLP rising ~1.7 points.
- **pattern_analysis**: Only MoHD ATTN and MoHD ATTN + MLP diverge most significantly at 25% activated parameters ratio, where the gap between them is largest.

---

## fig_196
- **counting**: The SMoE and SimSMoE validating lines intersect 1 time, at approximately the 10,000 training step mark.
- **computation**: SimSMoE starts at ~2.20 and reaches ~1.25 at 10K (rate ~0.095/10K); SMoE starts at ~2.20 and reaches ~1.25 at 10K (similar rate); the difference in rates is very small, approximately 0.05.
- **comparison**: At 50,000 steps, SMoE BPC (~1.15) is NOT less than 90% of SimSMoE BPC (~1.12), since 0.9×1.12=1.008 < 1.15; No.
- **pattern_analysis**: SimSMoE Validating declines slightly faster than SMoE Validating during the initial training steps (0 to 10,000), converging to similar values thereafter.

---

## fig_197
- **counting**: 7 data points across all lines have MRR@10 > 35.0: DPR w/ corpus expansion (red) has 6 points above 35, and DPR w/ document expansion (green) has 1 point just above 35 at S=2.
- **computation**: DPR w/ corpus expansion at S=2 is ~35.2 and at S=10 is ~35.8; percentage increase = (35.8−35.2)/35.2 × 100 ≈ 1.7%.
- **comparison**: From x=2 to x=10, corpus expansion increases ~0.6 while asymmetric expansion decreases ~0.3; twice the decrease = 0.6; so the increase equals but does not strictly exceed twice the decrease — borderline Yes.
- **pattern_analysis**: DPR w/ corpus expansion (red) and DPR w/ asymmetric expansion (blue) diverge the most as the number of queries increases, with the red line rising and the blue line fluctuating downward.

---

## fig_198
- **counting**: The two lines (XMoE and SimSMoE) intersect 1 time, at approximately the 20,000 training step mark where SimSMoE crosses below XMoE.
- **computation**: XMoE at 10K is ~1.25 and SimSMoE at 10K is ~1.27; percentage difference = (1.27−1.25)/1.25 × 100 ≈ 1.6%.
- **comparison**: At 10,000 steps, SimSMoE BPC (~1.27) is not more than 1.5× XMoE BPC (~1.25), since 1.5×1.25=1.875 > 1.27; No.
- **pattern_analysis**: During the first 20,000 training steps, SimSMoE Validating declines slightly faster than XMoE Validating, with SimSMoE reaching lower BPC values before the two lines converge after ~20K steps.

---

## fig_199
- **counting**: 10 slices across both pie charts represent categories with percentages ≥ 10% (7 in AttentionInfluence and 6 in FineWeb-Edu, with some overlap in category names but counted across both charts).
- **computation**: Health & Medicine in AttentionInfluence totals Medical(6)+Nutrition(5)+Diseases(11)=22%; FineWeb-Edu shows Health & Medicine at 19%; difference = 22−19 = 3%.
- **comparison**: In the AttentionInfluence chart, 'Infor tech' (5%) is the subcategory closest to 'Emerging tech' (4%), and it is higher.
- **pattern_analysis**: 'Education' dominates both charts: 25% in AttentionInfluence (vs second-largest Health & Medicine at 22%) and 38% in FineWeb-Edu Classifier (vs second-largest History & Society and Science & Technology Education at 19% each).

---

## fig_200
- **counting**: In the 'Not Abusive' segment, 4 subcategories (Other, Political, Religious, and Racial) have exactly four slices in their outermost layer.
- **computation**: The ratio of 'Negative' slices under Abusive to 'Negative' slices under Not Abusive is approximately 2.5, based on the relative arc sizes visible in the chart.
- **comparison**: In the 'Abusive' category, the 'Negative' slice under 'Sexist' appears visually more than twice the size of the 'Positive' slice under 'Sexist'; Yes.
- **pattern_analysis**: 'Political' consistently has the largest 'Negative' slice compared to other sentiment slices within its layer under the 'Abusive' category.
