# Potential Inductance Probes — To Review

## Current 5 (finalized)
1. **bg095** — Count vs % trap. Sum=87 not 100. Naive: 34%, Correct: 39%
2. **en009** — Color gradient mapping. Naive: 7%, Correct: 5%
3. **ml002** — Log scale gap interpretation. Correct: 80% sparsity
4. **en166** — Knowledge crosswords student/professor debate. Compute success rates from 2x2
5. **en213** — Professor claims model getting worse. Precision actually doubles (7%→16%)

## Candidates to verify (from agent search)

### Simpson's Paradox
6. **multi_fig_065** — Qwen2 wins 2/3 categories (Movies 91%, Songs 90%) but Llama3 wins overall average (82.7 vs 79.3). Qwen2 catastrophic Basketball drop (57%) offsets narrow wins. Q: "Qwen2 leads in Movies and Songs. If you average across all three domains, does Qwen2 still rank first?"

### Metric Choice Changes Ranking  
7. **multi_fig_005** — Win/Tie/Lose stacked bars. Student says GPT4o best (Win=56%), professor says Claude best (Lose=24% lowest). Computing Win+Tie: Doubao wins 78% vs Claude 76% vs GPT4o 74%. Neither debater right. Q: "If we define success as Win+Tie, which model has highest success rate?"

### Oracle vs Realistic Ranking Reversal
8. **english_fig_130** — Gemini/GPT4o tie at 0.60 F1 with oracle labels. Excluding oracle (unrealistic): Sonnet wins realistic average (0.375 vs 0.35 vs 0.325). Q: "Excluding oracle condition, which model performs best on average under realistic conditions?"

### Convergence Attribution
9. **multi_fig_053** — Correct vs Incorrect branching ratio gap narrows 0-4 shots. Looks like convergence but Correct collapsed 37.5% while Incorrect only dropped 25%. Q: "Which category changed more and by what percentage?"

### Differential Recovery
10. **multi_fig_030** — Enhanced GCG recovers 69.6% of MCQ gap but only 32.0% of Generation gap. Looks like "helps both" but very asymmetric. Q: "What percentage of the base performance gap does Enhanced GCG recover for each task?"

## Dropped (too simple/observable)
- de007 (additive decomposition — just arithmetic)
- de030 (multiplicative index — just arithmetic)
- bg202 (derive total from count/percentage — one division)
- cn095 (chain computation across pies — just multiplication)
- en046 (incremental gains — just subtraction)
- multi_fig_031 (different eval formats — visible from chart)
- en188 (tree search non-monotonic — visible from chart)
- en047 (SFT scaling diminishing returns — visible)
- multi_fig_177 (ranking inversion — visible from crossing lines)

## Design Strategies (from references.md)
- Contradiction probes (chart shows X, computation reveals not-X)
- Simpson's Paradox (aggregate vs subgroup reversal)
- Counterfactual ("if we exclude X, does conclusion change?")
- Hypothesis testing with competing claims (student vs professor)
- Deception detection ("is this chart misleading?")
