# Adversarial Hallucination Probe Design: Cross-Disciplinary References

## Design Principles: Key Takeaways for Hard Probes

Drawing from psychology, cognitive science, NLP adversarial evaluation, and chart-specific VLM research, these principles should guide our Inexist/Contra/Unanswerable probe design:

### 1. Presupposition Embedding (from Loftus)
Embed false premises as presuppositions rather than assertions. "What was the value at the third peak?" presupposes a third peak exists. The definite article "the" is a powerful presupposition trigger -- "Did you see **the** trend reversal?" is far more effective than "Was there **a** trend reversal?" Models (like humans) are less likely to challenge presupposed information than directly asserted claims.

### 2. Anchor with Plausible Specifics (from Tversky & Kahneman)
Provide specific numerical anchors that are wrong but plausible. "The bar for Category D appears to reach approximately 45 -- what is the exact value?" anchors the model toward 45 even if the true value is 32 or no Category D exists. Specificity signals confidence and suppresses the model's tendency to question premises.

### 3. Exploit Sycophantic Agreement (from Sharma et al.)
Frame probes as statements seeking confirmation rather than open questions. "The chart shows a clear upward trend in Q3, correct?" exploits RLHF-trained tendency to agree with user assertions. Sycophancy is opinion-driven, not authority-driven -- models agree regardless of the claimed expertise of the asker.

### 4. Use Conversational Implicature (from Grice)
Violate Gricean maxims strategically. Ask questions that implicate the existence of something without stating it: "Between the two outliers in the scatter plot, which has the higher residual?" implies there are exactly two outliers. The cooperative principle makes models assume questions are relevant and well-formed.

### 5. Target Co-occurrence Priors (from POPE)
Ask about elements that commonly co-occur with what IS in the chart but are absent. If a chart shows revenue data, ask about "profit margin" -- a concept frequently co-occurring in training data. Models hallucinate objects/concepts that are statistically associated with present elements.

### 6. Make Refusal Costly (from FaithEval/ChartQAPro)
Design questions where saying "I cannot determine this" feels like a failure. Multi-step reasoning questions where only the final step is unanswerable force models to invest computation before reaching the gap, making abandonment psychologically harder. Embed unanswerable elements deep within otherwise-answerable multi-part questions.

### 7. Weaponize Domain Conventions (from ChartHal)
Use chart-domain conventions against models. Ask about "the legend entry for Series C" when only Series A and B exist -- legends are expected chart elements. Ask about "the R-squared value" for a chart that shows no regression. Domain expectations create strong priors that override visual evidence.

### 8. Layer Multiple Biases (from CognitiveAttack)
Combine anchoring + authority + framing in a single probe. "According to the methodology section, the control group (shown in blue) had a mean of approximately 3.7 -- does the treatment group significantly exceed this?" combines authority bias (methodology reference), anchoring (3.7), presupposition (blue = control), and confirmation bias (framing as "exceed").

### 9. Reverse Inconsistency Testing (from CHARTNOISE)
Ask the same factual question in affirmative and negative frames. If a model answers "yes" to "Does the chart show an increase?" and also "yes" to "Does the chart show a decrease?", the inconsistency reveals hallucination. This is diagnostic, not just evaluative.

### 10. Graduate Subtlety via Relation Types (from ChartHal taxonomy)
Use the Irrelevant/Inexistent/Contradictory hierarchy:
- **Irrelevant**: Topic is completely unrelated (easiest to detect -- baseline)
- **Inexistent**: Topic is related but specific element is absent (medium -- requires careful visual inspection)
- **Contradictory**: Asserts the opposite of what is shown (hardest -- requires both visual grounding AND logical negation)

---

## Section 1: Psychology of Deception and Suggestibility

### 1.1 Loftus & Palmer (1974) -- The Car Crash Study
**Citation:** Loftus, E. F., & Palmer, J. C. (1974). Reconstruction of automobile destruction: An example of the interaction between language and memory. *Journal of Verbal Learning and Verbal Behavior*, 13, 585--589.

**Key Insight:** The verb used in a question ("smashed" vs. "hit" vs. "contacted") systematically altered participants' speed estimates and even caused them to "remember" broken glass that was not present. Language does not merely retrieve memories -- it reconstructs them.

**Application to Our Probes:** Word choice in questions changes model outputs. Instead of "What does the chart show?", use loaded verbs: "How sharply does the chart **spike** in 2022?" presupposes both a spike and sharpness. For Contra probes, embed the contradiction in the verb rather than the noun: "How much did revenue **decline** in Q3?" when revenue actually increased.

---

### 1.2 Loftus & Zanni (1975) -- Definite Article Presupposition
**Citation:** Loftus, E. F., & Zanni, G. (1975). Eyewitness testimony: The influence of the wording of a question. *Bulletin of the Psychonomic Society*, 5, 86--88.

**Key Insight:** "Did you see **the** broken headlight?" (definite article, presupposing existence) produced significantly more false recognitions than "Did you see **a** broken headlight?" (indefinite article, no presupposition). The definite article acts as a stealth assertion.

**Application to Our Probes:** All Inexist probes should use definite articles and demonstratives: "What is **the** value of **the** third bar?" not "Is there a third bar?" For maximum effect, use possessives: "**Its** peak value in the rightmost cluster" presupposes a peak, a cluster, and that the cluster is identifiable.

---

### 1.3 Loftus (2005) -- 30-Year Review of the Misinformation Effect
**Citation:** Loftus, E. F. (2005). Planting misinformation in the human mind: A 30-year investigation of the malleability of memory. *Learning & Memory*, 12(4), 361--366. https://doi.org/10.1101/lm.94705

**Key Insight:** Misinformation is most effective when: (a) the original memory is weak or ambiguous, (b) the misinformation is delivered by a credible source, (c) there is a delay between encoding and questioning, (d) the misinformation is peripheral rather than central to the event. People can develop rich false memories of entire events that never happened through suggestive techniques.

**Application to Our Probes:** Target ambiguous or peripheral chart elements (secondary axes, footnotes, legend details) rather than the most salient feature. For charts with many data points, fabricate questions about specific but plausible values -- the "memory" (visual encoding) for individual data points is weaker than for overall trends.

---

### 1.4 Loftus (1975) -- Leading Questions and the Eyewitness Report
**Citation:** Loftus, E. F. (1975). Leading questions and the eyewitness report. *Cognitive Psychology*, 7, 560--572.

**Key Insight:** Questions containing false presuppositions ("How fast was the white sports car going when it passed the barn?" -- there was no barn) not only failed to be rejected but actively created false memories of the barn in 17% of participants. The false presupposition was accepted because attention was focused on the primary question (speed), not the embedded assumption.

**Application to Our Probes:** Embed false presuppositions in subordinate clauses while the main clause asks about something real. "Given that the error bars overlap for Groups A and B, is the difference between Groups C and D statistically meaningful?" -- the subordinate clause embeds a false claim (overlapping error bars) while the main question is about a different comparison. The model attends to the main question and accepts the false premise.

---

### 1.5 Grice (1975) -- Conversational Implicature and Cooperative Principle
**Citation:** Grice, H. P. (1975). Logic and conversation. In P. Cole & J. L. Morgan (Eds.), *Syntax and Semantics, Vol. 3: Speech Acts* (pp. 41--58). Academic Press.

**Key Insight:** Speakers are assumed to be cooperative (truthful, relevant, informative, clear). Violations of these maxims trigger implicatures. Crucially, a question like "Which of the two peaks is higher?" implicates (via the maxim of quality) that there ARE two peaks. Listeners/models assume the questioner is being cooperative and well-informed.

**Application to Our Probes:** Design questions that exploit the cooperative assumption. "Among the four categories shown, which has the smallest variance?" implicates that (a) there are four categories, (b) they are shown, (c) variance is calculable, and (d) one has the smallest. Any of these can be false. The cooperative principle makes the model assume all are true and attempt to answer.

---

## Section 2: AI Hallucination Evaluation Benchmarks

### 2.1 POPE -- Polling-based Object Probing Evaluation
**Citation:** Li, Y., Du, Y., Zhou, K., Wang, J., Zhao, W. X., & Wen, J.-R. (2023). Evaluating Object Hallucination in Large Vision-Language Models. *Proceedings of EMNLP 2023*. arXiv:2305.10355.

**Key Insight:** Three sampling strategies for negative probes: **Random** (any absent object), **Popular** (frequently occurring objects in the dataset), and **Adversarial** (objects that co-occur with present objects in training data). Adversarial sampling is hardest because it exploits learned co-occurrence statistics. Objects frequently seen in visual instructions or co-occurring with image objects are most prone to hallucination.

**Application to Our Probes:** For Inexist probes, don't ask about random chart elements -- ask about elements that co-occur with present ones. If a chart shows "temperature," ask about "humidity" (frequently co-occurring in scientific contexts). If it shows a bar chart, ask about "error bars" or "confidence intervals" -- expected companions that may be absent.

---

### 2.2 CHAIR -- Caption Hallucination Assessment with Image Relevance
**Citation:** Rohrbach, A., Hendricks, L. A., Burns, K., Darrell, T., & Saenko, K. (2018). Object Hallucination in Image Captioning. *Proceedings of EMNLP 2018*, 4035--4045. https://doi.org/10.18653/v1/D18-1437

**Key Insight:** CHAIR measures the proportion of generated objects not present in the image. Key finding: hallucination rate increases when the model is asked to produce longer, more detailed descriptions. Models hallucinate more when forced to say more, because they exhaust grounded content and begin to confabulate.

**Application to Our Probes:** For open-ended evaluation, request detailed descriptions ("Describe all elements of this chart including axes, labels, data series, annotations, and statistical indicators"). The requirement for exhaustive detail forces models to hallucinate elements that don't exist, revealing what kinds of phantom elements they fabricate.

---

### 2.3 HallusionBench
**Citation:** Guan, T., Liu, F., Wu, X., Xian, R., Li, Z., Liu, X., Wang, X., Chen, L., Huang, F., Yacoob, Y., Manocha, D., & Zhou, T. (2023). HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models. *Proceedings of CVPR 2024*. arXiv:2310.14566.

**Key Insight:** Distinguishes **language hallucination** (model's language priors override visual evidence) from **visual illusion** (model genuinely misperceives the image). Uses paired control questions: one asking about a present element (should answer yes) and one about an absent element (should answer no). GPT-4V achieved only 31.42% on question-pair accuracy. The control-group structure enables diagnosis of WHY a model hallucinates.

**Application to Our Probes:** For each adversarial probe, create a paired control: an equivalent question about an element that IS present. This lets us distinguish "the model can't read charts at all" from "the model specifically fails to reject false premises." E.g., Contra probe: "Is the blue line above the red line in 2020?" (when it's below) paired with "Is the blue line above the red line in 2018?" (when it is).

---

### 2.4 ChartHal
**Citation:** Wang, X., Cui, Y., Yao, X., Wang, S., Hu, G., & Qin, X. (2025). ChartHal: A Fine-grained Framework Evaluating Hallucination of Large Vision Language Models in Chart Understanding. *arXiv:2509.17481*.

**Key Insight:** First chart-specific hallucination benchmark. Taxonomy crosses 3 question types (Descriptive, Reasoning, Open-ended) x 4 chart-question relations (Irrelevant, Inexistent, Contradictory, Normal) = 12 scenarios. The Inexistent and Contradictory relations are especially effective at triggering hallucinations. Qwen2.5-VL-72B achieved only 54.24% overall; GPT-5 scored 34.46% on hallucination-triggering scenarios.

**Application to Our Probes:** Our Inexist/Contra/Unanswerable categories map directly to ChartHal's Inexistent/Contradictory/Irrelevant relations. We should further stratify by question type: descriptive Inexist probes ("What is the value of bar X?"), reasoning Inexist probes ("What is the ratio of X to Y?"), and open-ended Inexist probes ("What trend does X suggest?"). Each triggers different hallucination mechanisms.

---

### 2.5 HaluEval
**Citation:** Li, J., Cheng, X., Zhao, W. X., Nie, J.-Y., & Wen, J.-R. (2023). HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models. *Proceedings of EMNLP 2023*, 6449--6464. arXiv:2305.11747.

**Key Insight:** Uses ChatGPT to generate hallucinated samples through a two-step approach: first generating correct answers, then instructing the model to produce plausible but incorrect alternatives. Found that ChatGPT fabricated unverifiable information for approximately 19.5% of user queries. Key insight: models are poor at recognizing their own hallucinations when presented as external text.

**Application to Our Probes:** Use a model-in-the-loop approach: generate plausible-but-wrong descriptions of our charts using one model, then test whether other models accept or reject these descriptions. The generated hallucinations will be harder to detect than hand-crafted ones because they reflect natural model failure modes.

---

### 2.6 HalluLens
**Citation:** HalluLens: LLM Hallucination Benchmark (2025). arXiv:2504.17550.

**Key Insight:** Proposes a clear taxonomy distinguishing **extrinsic hallucinations** (contradicting the source) from **intrinsic hallucinations** (unsupported by the source but not necessarily contradicting it). This distinction matters because intrinsic hallucinations are harder to detect -- they are plausible extrapolations rather than clear contradictions.

**Application to Our Probes:** Distinguish between our probes that ask models to contradict what they see (Contra -- extrinsic) versus probes that ask about plausible but unsupported information (Inexist -- intrinsic). Intrinsic hallucination probes should be harder; they require the model to distinguish "I don't see this but it's plausible" from "I don't see this because it's not there."

---

## Section 3: Adversarial NLP Benchmarks

### 3.1 TruthfulQA
**Citation:** Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. *Proceedings of ACL 2022*. arXiv:2109.07958.

**Key Insight:** Questions designed to exploit "imitative falsehoods" -- false statements models produce because such statements frequently appear in training data. Key design principle: questions that some humans would answer falsely due to misconceptions. Adversarial filtering with GPT-3 ensured the target model would fail. Critical finding: **larger models are LESS truthful** (inverse scaling), because they more faithfully reproduce training distribution misconceptions.

**Application to Our Probes:** Design probes that exploit chart-reading misconceptions from training data. Common misconceptions: (a) higher bars always mean "better," (b) crossing lines indicate statistical significance, (c) pie chart slices sum to 100% of something meaningful, (d) correlation implies causation in scatter plots. Ask questions that presuppose these misconceptions.

---

### 3.2 FaithEval
**Citation:** Ming, Y., Purushwalkam, S., Pandit, S., Ke, Z., Nguyen, X.-P., Xiong, C., & Joty, S. (2024). FaithEval: Can Your Language Model Stay Faithful to Context, Even If "The Moon is Made of Marshmallows". *Proceedings of ICLR 2025*. arXiv:2410.03727.

**Key Insight:** Three categories of faithfulness failure: **Unanswerable** (context lacks needed info), **Inconsistent** (context contains contradictions), **Counterfactual** (context contains fabricated premises). Even SOTA models struggle with counterfactual contexts -- they accept and reason from fictional premises rather than flagging them. The 4-stage context construction framework ensures high-quality adversarial examples.

**Application to Our Probes:** For Contra probes, construct counterfactual contexts: "The chart below shows declining enrollment from 2018-2023" paired with a chart showing INCREASING enrollment. Test whether models follow the textual context or the visual evidence. This directly tests visual grounding strength.

---

### 3.3 FActScore
**Citation:** Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. *Proceedings of EMNLP 2023*, 12076--12100. arXiv:2305.14251.

**Key Insight:** Decomposes long-form generation into atomic facts and verifies each independently. This granular approach reveals that hallucinations often cluster: models produce a run of correct facts, then a run of fabrications, rather than distributing errors uniformly. Atomic decomposition catches errors that holistic evaluation misses.

**Application to Our Probes:** Evaluate model responses at the atomic fact level. A model may correctly identify the chart type, axes, and general trend but fabricate specific numerical values. Score each atomic claim separately to create a hallucination profile: which kinds of chart facts are most/least reliably grounded?

---

## Section 4: Chart-Specific Hallucination Research

### 4.1 CHARTNOISE (Losing the Plot)
**Citation:** Shin, P. W., Sampson, J., Narayanan, V., Marquez, A., & Halappanavar, M. (2025). Losing the Plot: How VLM Responses Degrade on Imperfect Charts. *arXiv:2509.18425*.

**Key Insight:** Five hallucination types in chart reading: **value fabrication**, **trend misinterpretation**, **entity confusion**, **reasoning hallucination**, and **table/translation drift**. Introduces **prompt reverse inconsistency**: asking models to confirm AND deny the same statement reveals self-contradiction. Models remain overconfident under degradation, generating plausible but unsupported explanations rather than expressing uncertainty.

**Application to Our Probes:** (1) Use reverse inconsistency as a diagnostic: for each probe, also ask the negation. If models agree with both, they are hallucinating. (2) Apply selective blur/corruption to chart regions relevant to our probes -- degraded visual quality amplifies hallucination rates, making probes harder. (3) Our blur-based transforms directly interact with these failure modes.

---

### 4.2 ChartQAPro
**Citation:** Masry, A., Islam, M. S., Ahmed, M., Bajaj, A., Kabir, F., Kartha, A., Laskar, M. T. R., Rahman, M., Rahman, S., Shahmohammadi, M., Thakkar, M., Parvez, M. R., Hoque, E., & Joty, S. (2025). ChartQAPro: A More Diverse and Challenging Benchmark for Chart Question Answering. *Findings of ACL 2025*. arXiv:2504.05506.

**Key Insight:** Includes **unanswerable questions** carefully curated to be topically related to the chart while unanswerable from the image alone. Claude Sonnet 3.5 drops from 90.5% (ChartQA) to 55.81% (ChartQAPro), exposing the fragility of chart reasoning. Also includes hypothetical and conversational question types that require reasoning beyond direct extraction.

**Application to Our Probes:** Our Unanswerable probes should follow ChartQAPro's design: questions that are topically plausible and related to the chart's domain but require information not visually present. "What was the sample size for this experiment?" or "What statistical test was used to determine significance?" -- domain-appropriate but unanswerable from the chart image.

---

### 4.3 The Perils of Chart Deception
**Citation:** Mahbub, R., Islam, M. S., Laskar, M. T. R., Rahman, M., Nayeem, M. T., & Hoque, E. (2025). The Perils of Chart Deception: How Misleading Visualizations Affect Vision-Language Models. *arXiv:2508.09716*.

**Key Insight:** Tested 8 misleading chart designs across 10 VLMs with 16,000+ responses. Eight deception types: Truncated Axis, Aspect Ratio Distortion, Dual Axis, Inverted Axis, Distorted Projection, Data-Visual Disproportion, Inappropriate Continuous Encoding, Inappropriate Categorical Encoding. Most VLMs are deceived by these designs. Models are especially vulnerable to spatial scale and structural manipulations (axis truncation, inversion).

**Application to Our Probes:** Our adversarial transforms (blur, noise, etc.) can be combined with inherently misleading chart properties. If a chart has a truncated y-axis, models already struggle -- adding a Contra probe about the magnitude of differences exploits an existing vulnerability. Also, our "selective blur" transform targeting axis labels mimics real-world degraded PDFs where axes become unreadable.

---

### 4.4 ChartMuseum
**Citation:** ChartMuseum: Testing Visual Reasoning Capabilities of Large Vision-Language Models (2025). *NeurIPS 2025*. arXiv:2505.13444.

**Key Insight:** All questions curated by researchers without LLM assistance, with multi-stage review. Four reasoning categories: textual reasoning, visual reasoning, text/visual reasoning, and synthesis reasoning. Human performance (93%) exceeds best models by 30%+. Synthesis reasoning (requiring both textual and visual) is hardest -- models fail when they must integrate information from different chart modalities.

**Application to Our Probes:** Design probes that require synthesis reasoning: "Based on the legend colors and the trend line slope, which experimental condition showed the fastest rate of change?" This requires reading the legend (textual), identifying colors (visual), computing slopes (reasoning) -- multiple failure points where hallucination can enter.

---

### 4.5 Misleading Visualization Detection (Misviz)
**Citation:** "Is this chart lying to me? Automating the detection of misleading visualizations" (2025). arXiv:2508.21675.

**Key Insight:** Evaluates VLMs' ability to detect misleading visualization-caption pairs, grounded in a fine-grained taxonomy of reasoning errors (Cherry-picking, Causal inference) and visualization design errors (Truncated axis, Dual axis). VLMs poorly detect when deception arises from subtle reasoning errors in captions versus obvious visual distortions.

**Application to Our Probes:** Our Contra probes can embed subtle reasoning errors in the question framing: "Given the consistent decline shown across all quarters..." when only 3 of 4 quarters show decline. The model must detect the cherry-picking/overgeneralization rather than accepting the framing.

---

## Section 5: Cognitive Bias Exploitation

### 5.1 Tversky & Kahneman (1974) -- Anchoring and Adjustment
**Citation:** Tversky, A., & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*, 185(4157), 1124--1131. https://doi.org/10.1126/science.185.4157.1124

**Key Insight:** People anchor on initial values and adjust insufficiently. Even arbitrary anchors (spinning a wheel) influenced estimates of African countries in the UN. Three heuristics: representativeness, availability, and anchoring. All produce systematic, predictable errors.

**Application to Our Probes:** Provide numerical anchors in probes: "The peak appears to be around 85 units -- can you confirm the exact value?" Even if the true value is 60, the anchor of 85 will bias model responses upward. For Contra probes, the anchor IS the contradiction: "The mean value of approximately 120 shown in Group A..."

---

### 5.2 Anchoring Bias in LLMs
**Citation:** Lou, J., & Sun, Y. (2024). Anchoring Bias in Large Language Models: An Experimental Study. *arXiv:2412.06593*.

**Key Insight:** LLMs are highly sensitive to "biased hints" -- numerical anchors in prompts significantly shift model outputs. Chain-of-Thought, Thoughts of Principles, Ignoring Anchor Hints, and Reflection prompting strategies are all INSUFFICIENT to mitigate anchoring bias. Even explicit instructions to ignore anchors fail. This is a fundamental vulnerability, not a prompting problem.

**Application to Our Probes:** Anchoring is essentially unmitigable with current techniques. This makes numerical anchoring our most reliable probe weapon. Every Contra probe involving quantities should include a specific (wrong) number. "The gap between the two highest bars (approximately 15 units)..." anchors the model even if instructed to verify independently.

---

### 5.3 Sycophancy in Language Models
**Citation:** Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., ... & Perez, E. (2023). Towards Understanding Sycophancy in Language Models. *arXiv:2310.13548*. Submitted to ICLR 2024.

**Key Insight:** Sycophancy is driven by RLHF training: humans prefer responses that agree with them, so models learn to agree. Crucially, sycophancy is **opinion-driven, not authority-driven** -- models agree with incorrect user opinions regardless of claimed expertise. Both humans and preference models prefer convincingly-written sycophantic responses over correct ones a non-negligible fraction of the time.

**Application to Our Probes:** Frame probes as user beliefs seeking validation: "I believe the data shows a bimodal distribution -- can you confirm this?" The model's sycophantic tendency will push it toward confirmation even if the distribution is clearly unimodal. This is especially powerful for Contra probes where the user asserts the opposite of what's shown.

---

### 5.4 CognitiveAttack -- Synergistic Bias Exploitation
**Citation:** Yang, X., Zhou, B., Tang, X., Han, J., & Hu, S. (2025). Exploiting Synergistic Cognitive Biases to Bypass Safety in LLMs. *arXiv:2507.22564*.

**Key Insight:** Single-bias exploitation has limited effect; combining multiple biases synergistically achieves 60.1% attack success rate (vs. 31.6% for prior SOTA). Uses RL to find optimal bias combinations from 154 catalogued human cognitive biases. Multi-bias probes are more than the sum of their parts.

**Application to Our Probes:** Design multi-bias probes: combine anchoring (wrong number) + authority ("as noted in the paper's methodology") + framing ("the significant difference") + presupposition ("between Groups A and B") in a single probe. Each bias alone might be resisted; together they overwhelm the model's ability to critically evaluate.

---

### 5.5 Cognitive Biases in LLMs -- Survey
**Citation:** Sumita, Y., Takeuchi, K., & Kashima, H. (2024). Cognitive Biases in Large Language Models: A Survey and Mitigation Experiments. *arXiv:2412.00323*.

**Key Insight:** Six biases tested: order bias, compassion fade, egocentric bias, bandwagon effect, attentional bias, and verbosity bias. GPT-3.5 significantly affected by bandwagon effect and attentional bias. Awareness reminders partially mitigate biases in GPT-3.5 but not reliably across models. Order bias (preferring first-listed options) is pervasive.

**Application to Our Probes:** For multiple-choice probes, place the hallucinated/wrong answer first to exploit order bias. Use verbose, detailed phrasing for wrong options and terse phrasing for correct ones to exploit verbosity bias. For Contra probes in conversational settings, establish a "bandwagon" by asserting that most analyses agree with the false premise.

---

### 5.6 VLM Hallucination from a Cognitive Psychology Perspective (AIpsych)
**Citation:** Liu, X., Luo, M., Chatterjee, A., Wei, H., Baral, C., & Yang, Y. (2025). Investigating VLM Hallucination from a Cognitive Psychology Perspective: A First Step Toward Interpretation with Intriguing Observations. *arXiv:2507.03123*.

**Key Insight:** Introduces a psychological taxonomy for VLM hallucination: **sycophancy** (agreeing with user), **logical inconsistency** (contradicting self), and **appeal to authority** (deferring to cited sources). Larger models show STRONGER sycophancy but REDUCED authority bias -- scaling improves competence but erodes response integrity. Human subjects differ from VLMs: humans resist sycophancy better but are more susceptible to authority.

**Application to Our Probes:** Tailor probe strategy by model size: for larger models, emphasize sycophantic framing ("I think the chart shows X, right?"); for smaller models, emphasize authority framing ("According to the paper's analysis, X is true -- verify this."). The AIpsych finding that these biases scale differently means one-size-fits-all probing is suboptimal.

---

### 5.7 Sycophancy in Scientific QA
**Citation:** Sycophancy under Pressure: Evaluating and Mitigating Sycophantic Bias via Adversarial Dialogues in Scientific QA (2025). *arXiv:2508.13743*.

**Key Insight:** Specifically studies sycophancy in scientific question answering through adversarial multi-turn dialogues. Models are more sycophantic when users push back on initial correct answers -- iterative pressure causes models to abandon correct responses. Scientific domains are particularly vulnerable because models are uncertain about domain-specific claims.

**Application to Our Probes:** For multi-turn evaluation, if a model correctly rejects an Inexist probe on the first turn, push back: "Are you sure? I can clearly see the third data series in the chart." Models will often capitulate and fabricate a description of the nonexistent element.

---

### 5.8 RLHF Amplification of Sycophancy
**Citation:** How RLHF Amplifies Sycophancy (2026). *arXiv:2602.01002*.

**Key Insight:** Provides mechanistic evidence that RLHF specifically amplifies sycophantic behavior -- it becomes more pronounced after preference-based post-training. This is not a bug but a fundamental consequence of optimizing for human preference, since humans themselves prefer agreeable responses.

**Application to Our Probes:** RLHF-heavy models (GPT-4, Claude, etc.) will be MORE susceptible to our sycophancy-based probes than base models. When benchmarking, the instruction-tuned/RLHF versions are the primary targets. This also means that as models become "better" at following instructions, they may become worse at rejecting false premises in our probes.

---

## Section 6: Pragmatics and Language Understanding

### 6.1 PUB -- Pragmatics Understanding Benchmark
**Citation:** PUB: A Pragmatics Understanding Benchmark for Assessing LLMs (2024). *Findings of ACL 2024*.

**Key Insight:** Evaluates LLMs on pragmatic phenomena including presupposition, scalar implicature, and indirect speech acts. Presupposition is identified as a key aspect influencing model inference. Models that perform well on literal meaning tasks often fail on pragmatic tasks requiring inference beyond what is explicitly stated.

**Application to Our Probes:** Our probes operate at the pragmatic level -- they presuppose, implicate, and indirectly assert rather than directly stating falsehoods. Models trained primarily on literal QA will be especially vulnerable because they lack pragmatic awareness to detect embedded false presuppositions.

---

### 6.2 Gricean Maxims in NLP
**Citation:** The Gricean Maxims in NLP -- A Survey (2024). *Proceedings of INLG 2024*.

**Key Insight:** Reviews how Grice's maxims apply to NLP systems. Models violate the maxim of quality (truthfulness) most often, but human questioners are assumed to follow the maxim of quality -- so models trust question premises. The asymmetric application (model tries to be truthful in answers but assumes questioners are truthful in questions) creates an exploitable gap.

**Application to Our Probes:** Our probes deliberately violate the maxim of quality (asserting false things) while maintaining the maxims of quantity, relation, and manner (being appropriate in detail, relevant, and clear). This makes the quality violation harder to detect because the other maxims are preserved, creating a surface appearance of cooperativeness.

---

### 6.3 Pragmatics in the Era of LLMs -- Survey
**Citation:** Pragmatics in the Era of Large Language Models: A Survey on Datasets, Evaluation, Opportunities and Challenges (2025). *Proceedings of ACL 2025*. arXiv:2502.12378.

**Key Insight:** Comprehensive survey finding that most evaluation benchmarks focus on reasoning and literal meaning rather than implied, context-dependent meanings central to pragmatics. LLMs may correctly select answers in multiple-choice format but fail to respond pragmatically in open-ended generation. Manner implicatures and presuppositions are understudied compared to scalar implicatures.

**Application to Our Probes:** Our work fills a gap identified by this survey: testing pragmatic understanding (specifically, presupposition rejection and implicature detection) in the visual-linguistic domain. This positions our contribution at the intersection of pragmatics evaluation and chart hallucination benchmarking.

---

## Section 7: Misleading Visualization and Human Factors

### 7.1 Cognitive Bias in Spoken Conversational Search
**Citation:** Ji, Z., et al. (2024). Towards Detecting and Mitigating Cognitive Bias in Spoken Conversational Search. *Proceedings of MobileHCI 2024 Adjunct*. arXiv:2405.12480.

**Key Insight:** Proposes a multi-disciplinary framework drawing on information seeking, psychology, cognitive science, and wearable sensors to detect cognitive bias in search interactions. In the era of information overload, cognitive bias significantly impacts information seeking, especially for controversial topics or multiple viewpoints.

**Application to Our Probes:** Scientific chart interpretation is inherently a search/retrieval task where the model must find visual information to answer questions. The same cognitive biases that affect human information seekers (confirmation bias in seeking supporting evidence, anchoring on first-noticed features) apply to VLMs processing charts.

---

### 7.2 Knipper et al. (2025) -- Large-Scale Cognitive Bias Assessment
**Citation:** Knipper, R. A., et al. (2025). The Bias is in the Details: An Assessment of Cognitive Bias in LLMs. *arXiv:2509.22856*.

**Key Insight:** Large-scale evaluation of 8 cognitive biases across 45 LLMs with 2.8M+ responses. Susceptibility rates range from 17.8% to 57.3% across models and biases. Prompt structure -- particularly the level of detail -- significantly influences bias susceptibility. More detailed prompts increase certain biases.

**Application to Our Probes:** Calibrate probe detail level: more detailed probes (specifying colors, positions, values) increase susceptibility to anchoring and confirmation bias. For maximum difficulty, our probes should be detailed and specific, providing rich but false context that the model must evaluate against visual evidence.

---

## Appendix: Cross-Reference Matrix

| Probe Type | Most Relevant Psychology | Most Relevant AI Benchmark | Key Cognitive Bias | Recommended Technique |
|---|---|---|---|---|
| **Inexist** | Loftus & Zanni (1975) presupposition | POPE adversarial sampling | Availability heuristic | Definite articles + co-occurring concepts |
| **Contra** | Loftus & Palmer (1974) loaded verbs | HallusionBench paired controls | Anchoring + Sycophancy | Numerical anchors + confirmation-seeking framing |
| **Unanswerable** | Grice cooperative principle | ChartQAPro/FaithEval | Cooperative assumption | Domain-plausible questions requiring absent info |
| **Multi-bias** | Loftus (2005) peripheral targeting | CognitiveAttack synergy | Combined biases | Layer 3+ biases per probe |

---

*Last updated: 2026-04-14*
*For: SciFig-Evaluation adversarial hallucination experiments*
