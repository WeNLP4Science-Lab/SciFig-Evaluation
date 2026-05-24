# Capability Question Answers - Batch 4 (fig_151 to fig_200)

## fig_151
- No intersections occur between attn_residual and ffn_residual lines.
- Average max activation difference between attn_output and ffn_output (layers 20-23) is approximately 40.
- FFN_residual shows greater increase than attn_residual between layers 20-23.
- Both attn_residual and ffn_residual exhibit quadratic-like growth, with ffn_residual reaching higher values.

## fig_152
- 9 data points located at exact cost values of 2, 5, and 10 across all lines.
- Difference between 2-Model and 3-Model Ensemble at cost 5 represents approximately 0.0625 (6.25%) of 3-Model score.
- 3-Model Ensemble and 2-Model Ensemble show smallest gap between costs 0 and 5.
- Yellow line decreases much faster (25 points) than blue (5 points) and red (3 points) between costs 0-5.

## fig_153
- 2 data points on Initial Accuracy line exceed 0.5 (at x=13 and x=15).
- Maximum Final Accuracy (0.9) minus maximum Initial Accuracy (0.55) equals 0.35.
- Difference at x=13 (0.35) is smaller than at x=15 (0.4) between the two lines.
- Largest error bar variability occurs at x=13 with Final Accuracy bars slightly larger than Initial.

## fig_154
- 2 intersections occur between blue line (Inconsistency-CE-MP) and other lines.
- Difference between Consistency-CE and Inconsistency-CE-MP at AL 6 is 2 BLEU, representing 0.071 (7.1%) fraction.
- Consistency-Bi (28) is not more than twice Consistency-CE (23) at AL=3.
- Consistency-Bi (red line) shows consistent upward trend without inflection points.

## fig_155
- 4 data points on Vanilla line have loss below 2.55.
- Percentage reduction in loss for SepLLM compared to Vanilla at 0.90 TFLOPs is approximately 2.72%.
- SepLLM loss (2.47) at 1.23 TFLOPs is less than 1.28 times Vanilla (3.20).
- Vanilla and SepLLM lines converge at approximately 1.23e9 TFLOPs.

## fig_156
- 1 intersection occurs between tiny AdaLoRA_int4 and tiny int4 lines around epoch 3.
- Difference in WER reduction from epoch 0-6: tiny int4 (31) minus tiny int8 (23) equals 3 units.
- Tiny AdaLoRA_int8 experienced larger absolute WER reduction (~28) than tiny full (~6).
- Tiny int4 and tiny int8 converge at epoch 4 with approximate WER value of 40.

## fig_157
- 4 bars across both models exceed count of 30 (RR and WW for GPT3.5, RR for Mistral 7B).
- Percentage difference in RR count between GPT3.5 (120) and Mistral 7B (110) is approximately 9.09%.
- RR for GPT3.5 (120) is more than twice WW for Mistral 7B (30), which is 60.
- Type1 and Type2 bar heights show consistent 10-point difference, indicating convergence pattern.

## fig_158
- 3 data points located at x=200 (one for each line: accuracy, confidence, alignment).
- Sum of confidence values (1.6) minus sum of alignment values (1.1) equals 0.5.
- Alignment (0.7) is not more than twice accuracy (0.55) at x=200.
- Accuracy line exhibits non-monotonic trend with initial decrease, then increase, then slight decrease.

## fig_159
- 3 data points on Vanilla line exceed loss value of 2.60.
- Ratio of TFLOPs for SepLLM to Vanilla reaching loss 2.5 is exactly 1.28.
- Loss reduction comparison at green dashed line shows SepLLM (0.22) achieves greater reduction than Vanilla (0.25).
- SepLLM decreases faster than Vanilla between TFLOPs 0.25 and 0.75.

## fig_160
- 6 data points across all models exceed perplexity 30 (all from Vicuna-7B).
- Vicuna-7B perplexity decreases from 41.0 to 33.0 (M=3 to M=7), representing 19.51% reduction.
- LLAMA1-13B perplexity (20.0) at M=3 is less than half of Vicuna-7B (20.5).
- LLAMA1-13B and LLAMA1-7B converge toward ~20.0 and ~36.0 respectively at M=8.

## fig_161
- SepLLM line crosses green dashed horizontal line at loss 2.50 exactly once.
- Average loss difference between Vanilla and SepLLM at 50k and 150k seconds is approximately 0.03.
- SepLLM achieves lower loss (2.49) than Vanilla (2.50) at 250k seconds by approximately 0.01.
- Two methods show closest loss values at approximately 200k seconds, then SepLLM diverges downward.

## fig_162
- 4 data points have Harmful with Refusal Ratio greater than 0.4.
- Average Harmful with Refusal Ratio for Qwen2-VL-7B on MMSafetyBench is 0.4025.
- Red line (0.52) is not more than 1.5 times green line (0.37) at 1024; 0.52 < 0.555.
- Green line shows fastest rate of increase (0.17) between sample sizes 128 and 256.

## fig_163
- 7 x-axis tick markers have blue line accuracy above 0.95 (nearly constant at 0.99).
- Percentage difference for green line from x=0.93 (0.20) to x=0.98 (0.90) is approximately 350%.
- Blue line shows smallest change in accuracy between x=0.95 and x=0.96.
- Green and orange lines show convergence pattern, most apparent around x=0.95.

## fig_164
- 8 data points exceed 50% performance (7 from red line, 1 from purple line).
- Recall increases 300% from 70m (10%) to 7.0B (40%) model size.
- Precision shows smallest change between model sizes 1.0B and 1.4B.
- Metrics diverge with 40 percentage point gap between Precision (80%) and Recall (40%) at 7.0B.

## fig_165
- 5 data points with minFDE20 below 20 (all on blue TrajCL line).
- Average minFDE20 for LoRA 16 across all ratios is 22.6.
- Gap between TrajICL and FT (2.0) is larger than gap between LoRA 16 and LoRA 64 (0.2) at ratio 0.4.
- TrajICL exhibits consistent downward trend across entire Ratio axis.

## fig_166
- 14 layers have all three lines below sparsity ratio of 0.1 (layers 10-23).
- Orange dotted line sparsity decreases from 0.8 to 0.1 (layers 0-5), representing 87.5% decrease.
- Orange dotted line (0.1) at layer 20 is more than twice green dash-dot line (0.05).
- Green dash-dot line decreases more rapidly than orange dotted line between layers 0-5.

## fig_167
- 9 temperature points have LUFFY line accuracy above 75.0.
- On-policy RL accuracy increases 19.05% from temperature 0.1 (63.0) to 0.8 (75.0).
- LUFFY (81.0) is not more than twice On-policy RL (75.0), as 150.0 is the threshold.
- All lines show closest convergence at temperature 0.8 with accuracies around 75.0.

## fig_168
- 1 data point located at exact accuracy boundary of 40%.
- Percentage difference between Ours (54%) and PLLaVA (DP 8) (42%) at 30 frames is 12%.
- PLLaVA (DP 8) shows largest accuracy decrease of approximately 7% between 10 and 60 frames.
- PLLaVA (DP 8) shows steepest rate of decline in accuracy as frame count increases.

## fig_169
- 3 data points on orange line have perplexity below Full Cache PPL reference line (4.4).
- Percentage decrease in perplexity from 5% to 40% recent sequence ratio is approximately 6.52%.
- GPU memory ratio is closer to Full Cache GPU Mem reference line at 100% ratio.
- Blue line (GPU Mem. Ratio) increases faster than orange line (Perplexity) between 80%-100% ratio.

## fig_170
- 1 data point located exactly at accuracy threshold of 55 (Squared Exponential at 250 demos).
- Percentage increase for Squared Exponential from 0 (52) to 250 (55) demonstrations is 5.77%.
- Squared Exponential (55) is not more than twice LLmA-2-chat-7B (43), threshold is 86.
- Greatest accuracy divergence occurs at 250 demonstrations with largest spread between models.

## fig_171
- 4 data points exceed NPMI threshold of 0.40 (all on blue NIPS line).
- Percentage increase for NIPS from weight 0.5 (0.40) to peak 1.5 (0.41) is 2.5%.
- NIPS (0.41) at weight 1.5 is more than twice IMDB (0.20), since 0.41 > 0.40.
- NIPS dataset exhibits non-monotonic trend, increasing then decreasing as weight increases.

## fig_172
- 3 data points on Confidence line fall within 0.01 of maximum 1.00.
- Difference between maximum Confidence (0.97) and minimum Accuracy (0.65) is 0.32.
- Confidence (0.93) at popularity 5 is not more than twice Accuracy (0.65), threshold is 1.30.
- Accuracy shows fastest rate of increase (0.13 per 10 units) between popularity 15-25.

## fig_173
- 1 intersection occurs between Consistency (wait-1) and Inconsistency (wait-9) lines at x≈9.
- BLEU score for Consistency: wait-1 increases 16.67% from x=0 (24) to x=20 (28).
- Consistency: wait-1 increases by 2 units (more than twice the 0.5 unit increase for Inconsistency) between x=15-20.
- Consistency: wait-1 increases sharply while Inconsistency: wait-9 remains flat between x=15-20.

## fig_174
- 2 data points exceed Missing Step threshold of 0.855 (one on each line).
- Average Missing Step for 0-CoT across all x-values is 0.8518.
- 0-CoT (0.844) is not less than half of CoRe (0.424) at x=4.
- Two methods diverge as x increases, with maximum divergence at x=4.

## fig_175
- 2 data points on Confidence line fall within 0.05 of 0.9.
- Difference in rate of change between Confidence (0.01125) and Accuracy (0.02) is approximately 0.01.
- Confidence (0.95) is not more than twice Accuracy (0.7) at popularity 25; 1.4 is threshold.
- Lines diverge as popularity increases, with Confidence widening gap after popularity 15.0.

## fig_176
- 4 x-axis positions show overlapping shaded areas between MATTER and w/o material lines.
- Average Macro-F1 Score for w/o material information across 0.6-1.4 tokens is 51.25%.
- MATTER (51%) is not more than twice w/o material (48%) at x=1.4.
- Two lines come closest at approximately x=1.2, then diverge overall.

## fig_177
- 3 lines have at least one data point below 0.9 minFDE20 (TrajICL, FT, LoRA 16).
- FT method shows 18.95% decrease in minFDE20 from ratio 0.0 (0.96) to 1.0 (0.78).
- FT shows largest absolute decrease (~0.12) between ratios 0.2 and 0.8.
- FT demonstrates steepest rate of decrease between ratios 0.0 and 0.4.

## fig_178
- 5 data points have ROUGE-1 score ≥30 (3 from MBart+AdaLoRA, 2 from T5+AdaLoRA).
- ROUGE-1 increases 540% for MBart+AdaLoRA from log r=0 (5) to log r=4 (32).
- MBart+AdaLoRA at x=4 (32) is more than twice MBart+LoRA at x=2 (3).
- MBart+AdaLoRA shows fastest rate of increase from log r=0 to log r=4 across all methods.

## fig_179
- 2 intersections occur between language lines (blue-orange and green-orange).
- Percentage difference in vocabulary between Japanese (3100) and Korean (2900) at 500 iterations is 6.9%.
- Difference between Korean (2900) and Spanish (3000) at 500 iterations is exactly 100 (not greater).
- All language lines exhibit linear trends relative to gray reference line.

## fig_180
- 6 data points exceed 0.98 across all lines (3 green, 2 red, 1 blue).
- Difference between maximum confidence (0.99) and minimum alignment (0.92) is 0.07.
- Alignment (0.94) at popularity 20 is closer to Accuracy (0.96) than Confidence (0.975).
- Blue line (Accuracy) shows fastest rate of increase between popularity 15-25.

## fig_181
- 3 keywords have ASR above 0.8 for end line (purple): stunning, beautifully, and one other.
- Random line shows 200% increase in ASR from cf (0.2) to beautiful (0.6).
- Random line shows smallest increase (~0.05) between gorgeous and wonderful.
- Random line (orange) exhibits non-monotonic pattern with increases and decreases.

## fig_182
- 2 words (bb and mb) have all three lines with ASR below 0.5.
- Random line shows 500% increase in ASR from bb (0.1) to beautiful (0.6).
- Beautifully shows smallest difference in ASR between start and end lines.
- All three lines converge most closely at beautifully with approximate ASR value of 0.9.

## fig_183
- 3 peaks (local maxima) visible in purple line (Regularization Loss) shaded region.
- Reconstruction Loss decreases 88.75% from step 0 (7.8) to step 1000 (0.8).
- Peak value of Regularization Loss (exceeds 6.0) exceeds twice starting Task Loss (3.0) between steps 0-200.
- Regularization Loss shows most pronounced oscillations, most evident between 0-200 steps.

## fig_184
- 7 data points have AUC ≥95% (blue:2, orange:2, green:1, magenta:1, yellow:1).
- Average AUC at N=10 across all datasets is 96.4%.
- Light blue and yellow lines show smallest AUC difference between N=15-20.
- Green line with star markers shows slowest and most consistent increase across entire N range.

## fig_185
- 5 epochs have BLEU score above 0.1 for Members with near-duplicates (1.0-3.0).
- Members with near-duplicates shows 140% BLEU increase from epoch 1 (0.15) to epoch 3 (0.36).
- Members with near-duplicates (0.36) at epoch 3.0 is more than five times Held-out data (0.03).
- Steepest rate of increase for Members with near-duplicates occurs between epochs 1 and 2.

## fig_186
- 3 lines have at least one minADE20 value below 0.60 (FT, LoRA 16, LoRA 64).
- Average minADE20 for LoRA 16 across all ratios is 0.67.
- FT shows largest absolute decrease (0.16) in minADE20 between ratios 0.0 and 1.0.
- TrajICL exhibits non-monotonic trend with fluctuations across ratio range.

## fig_187
- 6 data points have BLEU score ≥26 (3 from red line, 2 from purple, 1 from blue).
- Average BLEU score for Inconsistency-CE-MP across all AL values is 24.17.
- Ranking at AL 3: Consistency-Bi > Inconsistency-CE-MP > Inconsistency-CE > Consistency-CE.
- Consistency-CE line shows non-monotonic trend with direction change between AL 0-1.

## fig_188
- 1 data point on NDCG@50 (Ours) line falls within 0.01 of constant ReFICR value (0.155).
- Total difference between Recall@50 (Ours) and (ReFICR) summed across all x-values is 0.1.
- Recall@50 (Ours) at x=5 (0.48) exceeds twice NDCG@50 (ReFICR) (0.31).
- Recall@50 and NDCG@50 (Ours) show greatest convergence rate at x=2.

## fig_189
- 1 x-axis position where minFDE_20 values are equal for ST-ES and Random lines (x≈4).
- ST-ES method shows 12.5% decrease in minFDE_20 from 0 examples (0.24) to 4 examples (0.21).
- Random method does not achieve lower minFDE_20 than ST-ES between x=2 and x=8.
- ST-ES shows decreasing trend (0-4), then slight upward curve (4-8).

## fig_190
- 2 times Linear method's training accuracy drops below 0.6 after epoch 200.
- Ratio of C³A_b=128/2 (0.8) to LoRA_T=1 (0.64) training accuracy at epoch 50 is 1.25.
- Linear does not increase more than twice LoRA_T=1 between epochs 300-400.
- C³A_b=128/2 exhibits most consistent trend after epoch 100 with no visible fluctuations.

## fig_191
- 3 data points exceed PPL threshold of 8.0 (one each on blue, orange, green lines at 2K).
- Percentage decrease for γ=0.25 from 2K (8.2) to 8K (7.82) is 4.88%.
- γ=0.25 shows largest absolute PPL decrease (0.38) between 2K and 8K context lengths.
- Three lines converge as context length increases; green lowest at 64K, then orange, then blue.

## fig_192
- 4 data points exceed Pass@1 Rate threshold of 50% (2 from each model).
- Percentage difference between Claude-3.5-Sonnet (87.1%) and GPT-4o (77.4%) at 20 steps is 12.5%.
- Ranking in ascending order: 6.5%, 19.4%, 32.3%, 38.7%, 77.4%, 87.1% (across 5-20 steps).
- Greatest divergence occurs at 5 reasoning steps with 12.9% difference between models.

## fig_193
- 6 data points exceed WER threshold of 35.0.
- Difference in WER reduction between small AdaLoRA_int4 (5.0) and small int8 (4.0) is 1.0.
- Small int8 WER at epoch 6 (26.0) is not less than half small int4 at epoch 2 (21.0).
- Small int4 configuration exhibits non-monotonic trend with peak at epoch 2.

## fig_194
- 4 paper numbers have time cost >10 seconds for w/o Pre-computation method.
- Time cost ratio for w/o Pre-computation to w Pre-computation at Paper 256 is approximately 35.
- W/o Pre-computation (35 seconds) at Paper 256 exceeds 10 times w Pre-computation.
- W/o Pre-computation shows significantly higher rate of change than w Pre-computation between papers 64-256.

## fig_195
- 3 data points exceed PPL threshold of 13.0 (1 on Only MoHD ATTN, 2 on MoHD ATTN+MLP).
- Only MoHD ATTN shows 26.1% increase in PPL from 100% (11.5) to 25% (14.5) parameters.
- Only MoHD ATTN shows largest increase (3.0) in PPL between 100%-25% parameter ratios.
- Only MoHD ATTN and MoHD ATTN+MLP diverge most significantly at 25% parameter ratio.

## fig_196
- 2 lines intersect once near training step 10,000.
- Difference in rate of change between SMoE and SimSMoE is 0.05 from steps 0-10,000.
- SMoE BPC (1.1) at step 50,000 is not less than 90% of SimSMoE (1.008).
- SimSMoE Validating declines faster than SMoE during initial 0-10,000 training steps.

## fig_197
- 7 data points exceed MRR@10 threshold of 35.0 (6 on red line).
- DPR w/ corpus expansion shows 4.64% increase in MRR@10 from S=2 (35.1) to S=10 (35.8).
- Corpus expansion increase (0.7) exceeds twice asymmetric expansion decrease (0.6).
- DPR w/ corpus expansion (red) and w/ asymmetric expansion (blue) lines diverge most.

## fig_198
- 2 lines intersect once around 20,000 training steps.
- Percentage difference in BPC between XMoE (1.25) and SimSMoE (1.27) at 10,000 steps is 1.57%.
- SimSMoE BPC (1.27) is not more than 1.5 times XMoE (1.875) at 10,000 steps.
- SimSMoE declines slightly faster than XMoE during first 20,000 training steps.

## fig_199
- 10 slices represent categories with percentages ≥10% across both pie charts.
- Total Health & Medicine in AttentionInfluence (22%) equals FineWeb-Edu Classifier (22%), difference is 0%.
- Infor tech (5%) is closest to Emerging tech (4%) in AttentionInfluence chart and higher.
- Education dominates both charts: 25% in AttentionInfluence vs 38% in FineWeb-Edu Classifier.

## fig_200
- 4 subcategories have exactly four slices in outermost layer of Not Abusive segment.
- Ratio of Negative slices under Abusive to Not Abusive categories is approximately 2.5.
- Negative slice under Sexist in Abusive category is more than twice Positive slice size.
- Political sub-category under Abusive consistently has largest Negative slice compared to other sentiments.
