# Writing Voice Guide: Sentence-Level Craft for ACL-Quality Prose

This guide is derived from close reading of ACL 2024 best papers (Mission: Impossible Language Models; Causal Estimation of Memorisation Profiles; Aya Model), EMNLP best papers, and widely praised NLP papers (FActScore, MT-Bench/Chatbot Arena, Observational Scaling Laws, Same Task More Tokens). Every pattern below is grounded in how award-winning authors actually write.

---

## 1. The Voice We Want

**Precise. Vivid. Confident. Surprising.**

The target voice sits at the intersection of:
- A scientist who respects their reader's intelligence
- A writer who refuses to bore
- A colleague explaining a genuinely interesting finding over coffee

It is NOT:
- A student trying to sound smart
- A bureaucrat covering all bases
- A press release overselling results

The calibration: **write as if your reader is an expert who is busy and skeptical but curious.** Every sentence must earn its place.

---

## 2. Banned Phrases and Better Alternatives

| # | Banned | Why it fails | Use instead |
|---|--------|-------------|-------------|
| 1 | "It is worth noting that..." | Throat-clearing; adds nothing | Just state the thing. |
| 2 | "Interestingly, ..." | Tells the reader what to feel | Let the finding speak. If it is interesting, the reader will notice. |
| 3 | "Surprisingly, ..." | Same problem. Also: if you expected it, why is it surprising? | State the result, then explain why it defies expectation. |
| 4 | "As can be seen from Table X..." | Points at a table instead of saying something | "Table X reveals that..." or better: state the finding, cite the table parenthetically. |
| 5 | "We can observe that..." | Passive filler | Cut entirely. State the observation. |
| 6 | "It is important to note..." | If it were important, you would not need to announce it | Delete the phrase; keep the content. |
| 7 | "In order to" | Three words doing the work of one | "To" |
| 8 | "A number of" | Vague | Give the actual number, or say "several" / "many" with specificity. |
| 9 | "Due to the fact that" | Five-word "because" | "Because" |
| 10 | "It should be mentioned that..." | Nobody asked you to mention it; just say it | Delete. |
| 11 | "Relatively" / "Fairly" / "Somewhat" | Generic hedging that conveys nothing | Quantify ("by 3 points"), specify a comparison, or commit to the claim. |
| 12 | "Utilize" | Pompous synonym for "use" | "Use" |
| 13 | "Methodology" (when you mean "method") | Methodology is the study of methods | "Method" or "approach" |
| 14 | "Novel" (in your own paper) | Let reviewers decide novelty | "We propose..." is sufficient. The work speaks for itself. |
| 15 | "State-of-the-art" (as an adjective) | Overused to the point of meaninglessness | Name the specific system you outperform and by how much. |
| 16 | "Leverage" | Corporate jargon | "Use" or "exploit" or "build on" |
| 17 | "Aforementioned" | Legalistic | "This" / "these" / rephrase |
| 18 | "Conduct experiments" | Nobody "conducts" experiments outside grant proposals | "We evaluate..." / "We test..." / "We measure..." |
| 19 | "Existing works" (as a mass noun) | Grammatically awkward, imprecise | "Prior work" (singular, conventional) or name the specific papers |
| 20 | "To the best of our knowledge" | Defensive and often wrong | If the claim is true, state it. If uncertain, say "No prior work has X" and let reviewers correct you. |

---

## 3. Before/After Transformations

### 3.1 The Dead Opening

**Before:** "In recent years, large language models have attracted significant attention from the research community due to their impressive performance on a wide range of natural language processing tasks."

**After:** "Large language models can now write code, summarize legal briefs, and pass medical licensing exams -- yet they fail at tasks any five-year-old handles effortlessly."

*Why it works:* Concrete specifics replace vague gestures. The contrast creates tension. The reader wants to know what those tasks are.

### 3.2 The Table Narrator

**Before:** "As can be seen from Table 3, our model achieves a score of 78.2, which is higher than the baseline score of 71.4."

**After:** "Our model scores 78.2, a 6.8-point gain over the strongest baseline (Table 3) -- roughly the gap between GPT-3.5 and GPT-4 on this benchmark."

*Why it works:* The finding leads. The table is evidence, not the subject. The comparison gives the number meaning.

### 3.3 The Hedge That Hedges Nothing

**Before:** "The results somewhat suggest that the model may have relatively limited capability in handling certain types of complex reasoning tasks."

**After:** "The model fails on 3 of 5 compositional reasoning tasks, succeeding only when the reasoning chain is two steps or shorter."

*Why it works:* Precision replaces vagueness. The reader now knows exactly what the limitation is.

### 3.4 The Buried Punchline

**Before:** "We performed experiments across multiple settings and found that the performance of the model varied depending on the type of input used, with some inputs leading to better results than others."

**After:** "Performance hinges on input type: structured prompts yield 82% accuracy, while free-form queries drop to 54% -- a gap wider than the difference between our best and worst models."

*Why it works:* The finding is front-loaded. Numbers are embedded naturally. The comparison makes the gap tangible.

### 3.5 The "We Did Things" Paragraph

**Before:** "We first preprocessed the data. We then split it into training and test sets. We trained the model using the training set. We evaluated the model on the test set."

**After:** "We train on 10K examples and evaluate on a held-out set of 2K, using identical preprocessing to Chen et al. (2023) to ensure comparability."

*Why it works:* One sentence replaces four. The reader learns what matters (scale, comparability) and skips what does not (the obvious).

### 3.6 The Overclaim

**Before:** "Our novel framework significantly outperforms all existing state-of-the-art methods, demonstrating the superiority of our approach."

**After:** "Our approach outperforms the previous best system by 4.2 F1 points on MMLU and 7.1 on HellaSwag, though the gap narrows on multilingual benchmarks (Table 4)."

*Why it works:* Specific numbers replace superlatives. Acknowledging where the gap narrows builds trust and preempts reviewer objections.

### 3.7 The Passive Fog

**Before:** "It was found that the errors were predominantly caused by misalignment between the generated output and the expected format, which was observed across multiple experimental configurations."

**After:** "Format mismatches cause 63% of errors, a pattern consistent across all five configurations we test."

*Why it works:* Active voice. A number. One sentence instead of a paragraph.

### 3.8 The "Interestingly" Crutch

**Before:** "Interestingly, we observe that smaller models sometimes outperform larger models on this particular task."

**After:** "Smaller models outperform their larger counterparts on 3 of 7 tasks -- all three involving short-context reasoning, where the larger model's additional capacity appears to offer no advantage."

*Why it works:* Instead of labeling the finding as interesting, the sentence explains *why* it happens, which is what actually makes it interesting.

### 3.9 The Empty Transition

**Before:** "Furthermore, we also investigate the impact of different hyperparameter settings on the overall performance of our proposed method."

**After:** "Does the gain survive hyperparameter variation? We sweep learning rate across three orders of magnitude and find that performance remains within 2 points of the optimum for rates between 1e-4 and 1e-3."

*Why it works:* A question creates forward momentum. The answer is specific and self-contained.

### 3.10 The Generic Conclusion

**Before:** "In this paper, we have presented a comprehensive study of X. Our results demonstrate that our approach achieves competitive performance. We hope that our work will inspire future research in this important area."

**After:** "The gap between human and machine performance on figure interpretation is not closing -- it is shifting. Models now match humans on extraction but fall behind on inference, suggesting that the next frontier is not better vision but better reasoning."

*Why it works:* A genuine insight replaces a template. The reader leaves with something to think about.

### 3.11 The Number Dump

**Before:** "The accuracy was 87.3%, the precision was 84.1%, the recall was 89.7%, and the F1 score was 86.8%."

**After:** "The system achieves 86.8 F1, with recall (89.7%) outpacing precision (84.1%) -- a tradeoff we deliberately accept because missed captions cost more than false positives in downstream evaluation."

*Why it works:* Lead with the headline metric. Give supporting numbers in parentheses. Explain *why the pattern matters*.

### 3.12 The Motivation Paragraph

**Before:** "Evaluating the quality of automatically generated figure descriptions is an important problem. Previous methods have several limitations. Therefore, we propose a new method."

**After:** "Current evaluation metrics reward fluency but ignore faithfulness: a caption that eloquently describes the wrong trend scores higher than a terse but accurate one. We design an evaluation that penalizes hallucination proportionally to its severity."

*Why it works:* A concrete failure case motivates the work more than an abstract claim of importance.

### 3.13 The Related Work Throat-Clear

**Before:** "Several previous works have studied this problem. Smith et al. (2020) proposed X. Jones et al. (2021) extended this by Y. Our work differs from these approaches in several important ways."

**After:** "Smith et al. (2020) and Jones et al. (2021) evaluate on single-panel figures only; we extend to multi-panel layouts where spatial reasoning compounds the challenge."

*Why it works:* One sentence positions the work relative to prior art without a literature review in miniature.

### 3.14 The Weak Claim with "Suggests"

**Before:** "This result suggests that there might potentially be some form of relationship between model size and caption quality."

**After:** "Caption quality scales with model size up to 13B parameters, then plateaus (r = 0.91 below 13B, r = 0.12 above)."

*Why it works:* The correlation coefficient does the hedging. The plateau is the finding.

---

## 4. How to Write Punchlines That Land

A punchline is the sentence that delivers the finding. Best-paper authors treat it like the last line of a joke: everything before it is setup.

**Technique 1: Concrete, then abstract.**
> "GPT-4 identifies 92% of bar chart trends but only 31% of scatter plot correlations -- a gap that reveals not a vision deficit but a reasoning one."

The numbers are the concrete. The clause after the dash is the abstract meaning. The reader gets both.

**Technique 2: The reversal.**
> "Contra claims by Chomsky and others that LLMs cannot possibly inform our understanding of human language, we argue there is great value in treating LLMs as a comparative system for language learning." (Kallini et al., ACL 2024 Best Paper)

State the conventional wisdom, then reverse it. The "contra" does the work.

**Technique 3: The question answered.**
> "A fundamental question arises: If an LLM possesses the ability to self-correct, why doesn't it simply offer the correct answer in its initial attempt?" (Huang et al.)

Pose a question the reader is already thinking. Then answer it with data.

**Technique 4: The named phenomenon.**
> "We note the presence of a 'seesaw phenomenon', where certain capabilities exhibit improvement while a few others clearly regress."

Naming a pattern makes it real. It gives the community a handle to grab.

**Technique 5: The scale anchor.**
> "Standard finetuning achieves 29.79% on AlpacaEval, which rises to 64.69% using noisy embeddings." (NEFTune)

A more-than-doubling needs no adjective. The numbers are the punchline.

**Technique 6: The implication sentence.**
> "The observed drop in performance with varying input lengths remains unexplained." (Same Task, More Tokens)

Sometimes the punchline is what you *cannot* explain. Admitting a mystery is more memorable than claiming you solved everything.

---

## 5. How to Make Numbers Sing

### Rule 1: Lead with the headline number, support with context.
Bad: "The precision was 84.1% and the recall was 89.7% and the F1 was 86.8%."
Good: "The system achieves 86.8 F1, driven by high recall (89.7%) at modest cost to precision."

### Rule 2: Give numbers meaning through comparison.
Bad: "Our model reduces the KV cache by 93.3%."
Good: "Our model reduces the KV cache by 93.3%, shrinking a 32GB footprint to 2.1GB -- enough to fit on a single consumer GPU."

### Rule 3: Use ratios and multiples for large differences.
Bad: "The test set has 81 times more tests than the original."
Good: "EvalPlus extends the test suite by 81x." (Clean, punchy, from the actual paper.)

### Rule 4: Embed numbers in causal sentences.
Bad: "Accuracy was 0.92 at 1K tokens and 0.68 at 3K tokens."
Good: "Accuracy drops from 0.92 to 0.68 by 3,000 tokens -- a 26-percentage-point decline on the same underlying task, well within the model's stated context window." (Same Task, More Tokens, adapted)

### Rule 5: Round when precision does not matter; be exact when it does.
- "roughly 80% of the variance" is fine for a PCA summary.
- "4.2 F1 points" is necessary when reporting a benchmark delta.

### Rule 6: Use parenthetical numbers to avoid interrupting prose flow.
Good: "The agreement between GPT-4 and human experts reaches 85% (setup S2, without ties), on par with inter-annotator agreement."

### Rule 7: Never report a number without telling the reader whether it is good or bad.
Bad: "Human--machine agreement is 72%."
Good: "Human--machine agreement is 72%, close to the 78% ceiling set by inter-annotator agreement."

---

## 6. Sentence Templates (Natural, Not Formulaic)

These are *patterns*, not fill-in-the-blank forms. Vary them. Mix them. Never use the same one twice in a row.

### Opening Hooks
- "[Concrete capability] -- yet [concrete failure]."
- "[Entity] has claimed [X]. We test this claim."
- "[Practical problem] remains unsolved because [specific reason]."
- "The gap between [A] and [B] is not [expected thing] -- it is [surprising thing]."

### Presenting Findings
- "[System] achieves [number], a [delta]-point [gain/drop] over [baseline] ([citation])."
- "[Finding in plain English] ([number]; [statistical context])."
- "The effect holds across [conditions], with [metric] ranging from [low] to [high]."
- "[Number] of [total] [things] exhibit [pattern] -- all sharing [common property]."

### Explaining Why
- "This gap reflects not [obvious explanation] but [deeper one]."
- "The pattern breaks down when [condition], suggesting that [mechanism]."
- "Two factors explain this result: [factor 1] and [factor 2]."
- "[Finding] is consistent with [theory], which predicts that [implication]."

### Hedging with Strength
- "This pattern holds for [scope], though we cannot rule out [alternative]."
- "The correlation is strong (r = [value]) but causal claims require [what's missing]."
- "While we observe [X] consistently, [Y] warrants further investigation."
- "[X] outperforms [Y] on [N] of [M] benchmarks; the exceptions share [property]."

### Transitions Between Findings
- "Does this pattern extend to [related domain]?"
- "The picture changes for [different condition]."
- "A natural question is whether [next question]. [Answer]."
- "So far we have shown [X]. We now turn to [Y]."

### Closing Sentences
- "The frontier is not [what people think] -- it is [what your work shows]."
- "[Your finding] reframes the question from [old question] to [new question]."
- "If [your finding] generalizes, then [implication for the field]."
- "We release [artifact] to enable [what others can now do]."

---

## 7. Paragraph Architecture

### The Topic Sentence Rule
The first sentence of every paragraph should be readable in isolation and still convey the paragraph's point. Best-paper paragraphs pass the "skim test": reading only first sentences gives a coherent summary.

Good first sentences from award-winning papers:
- "Our core finding is that GPT-2 struggles to learn impossible languages when compared to English as a control." (Kallini et al.)
- "Commercially available LMs are riddled with errors." (FActScore)
- "The requirement of training models across many different scales has limited their use." (Observational Scaling Laws)

### The Build Pattern
1. **Claim** (first sentence)
2. **Evidence** (numbers, examples)
3. **Implication** (what it means)

Example:
> "Caption quality degrades sharply for figures containing more than four data series. Models averaging 91% accuracy on single-series charts drop to 58% on five-series charts (Table 3). The bottleneck is not visual -- models correctly identify all series in 94% of cases -- but inferential: they fail to compare trends across series."

### The Contrast Pattern
1. **Setup** (what you might expect)
2. **Reversal** (what actually happens)
3. **Explanation** (why)

Example:
> "Larger models should, in principle, handle longer inputs more effectively. In practice, accuracy drops from 0.92 to 0.68 by 3,000 tokens across all model sizes. The failure is architectural, not parametric: attention dilution affects large and small models alike."

---

## 8. Voice Calibration

### Active vs. Passive
Use active voice by default. Use passive only when the actor is genuinely irrelevant:
- Active: "We train on 10K examples." (Default)
- Passive: "The dataset was annotated by three experts." (The experts are not the story; the annotations are.)

### "We" Usage
"We" is fine and expected in ACL papers. Use it for actions your team took:
- "We evaluate..." / "We find..." / "We release..."

Do NOT use "we" for universal statements:
- Bad: "We know that transformers use self-attention."
- Good: "Transformers use self-attention."

### Formality Level
Aim for **precise informality**. You can write "the model chokes on long inputs" in a blog post, but in a paper, write "the model's accuracy degrades sharply beyond 3K tokens." The informality is in the directness and concreteness, not in slang.

### Metaphors and Analogies
Use sparingly and only when they clarify:
- Good: "a seesaw phenomenon" (names a real tradeoff pattern)
- Good: "impossible languages lie on a continuum" (spatial metaphor that clarifies)
- Bad: "our framework is a Swiss Army knife for NLP" (vague, cliched)

---

## 9. Anti-Pattern Detection Checklist

Before submitting any paragraph, check for:

- [ ] Does any sentence start with "It is..." that could be rewritten in active voice?
- [ ] Does any sentence contain "interestingly," "surprisingly," "notably," or "importantly"?
- [ ] Does any sentence point at a table/figure without stating the finding? ("As shown in...")
- [ ] Do three or more consecutive sentences start with "We"?
- [ ] Does any sentence contain "somewhat," "relatively," or "fairly" without a specific comparison?
- [ ] Does any sentence use "utilize," "leverage," "novel," or "methodology" unnecessarily?
- [ ] Does any sentence announce that it will say something before saying it? ("It is worth noting...")
- [ ] Does the paragraph bury the finding after the method?
- [ ] Are numbers reported without context for what they mean?
- [ ] Does the conclusion merely restate the abstract?

---

## 10. Quick Reference: The Five Moves of a Strong Analytical Sentence

1. **Name the finding.** ("Accuracy drops by 26 points.")
2. **Anchor it.** ("...from 0.92 to 0.68 by 3K tokens.")
3. **Scope it.** ("...consistently across all five model families.")
4. **Explain it.** ("The failure stems from attention dilution, not parameter count.")
5. **Imply it.** ("Longer context windows alone will not solve this.")

Not every sentence needs all five. But the best analytical paragraphs hit all five within 2-3 sentences.

---

## 11. Tone Exemplars from Best Papers

**How to open with confidence (Kallini et al., ACL 2024 Best Paper):**
> "Chomsky and others have very directly claimed that large language models are equally capable of learning languages that are possible and impossible for humans to learn. However, there is very little published experimental evidence to support such a claim."

Two sentences. The first states a strong claim by a famous figure. The second quietly demolishes it. No hedging. No "it is worth noting." Just: here is the claim, here is the gap.

**How to admit uncertainty without weakness (Same Task, More Tokens):**
> "The observed drop in performance with varying input lengths remains unexplained; because of lack of access to many of the models, we suspect this direction will continue to be limited."

They do not pretend to know. They state the mystery and the practical barrier. This builds more trust than a forced explanation.

**How to deliver a number that matters (FActScore):**
> "Commercially available LMs are riddled with errors."

No number in this sentence -- but it follows paragraphs of precise percentages (ChatGPT at 58.3%, InstructGPT at 42.5%). The blunt summary *earns* its bluntness through prior precision.

**How to close with vision (Kallini et al.):**
> "Since we do find that real languages are more learnable by GPT-2, this leads us to wonder what inductive bias of GPT language models matches natural language."

Ends not with a claim but with a question -- the most powerful kind of close, because it gives the reader something to carry away.

---

## 12. Final Principle

The difference between a good paper and a best paper is not the findings -- it is whether the reader *feels* the findings. Every sentence should do one of three things:

1. **Tell the reader something they did not know.**
2. **Change how the reader thinks about something they did know.**
3. **Move the reader closer to the next thing they need to know.**

If a sentence does none of these, delete it.
