# Evaluation Paper Introductions: Annotated Study Guide

How do the best benchmark/evaluation papers make their work feel important and urgent?
Below: verbatim introductions from 6 landmark papers, annotated paragraph-by-paragraph.

---

## 1. HELM -- Holistic Evaluation of Language Models (Liang et al., 2023)

**Published in:** Transactions on Machine Learning Research (08/2023)
**Why study this:** A massive evaluation paper that had to justify why "yet another benchmark" matters. Opens not with models but with the *purpose of benchmarks in society*.

### Verbatim Introduction

**Paragraph 1:**

> Benchmarks orient AI. They encode values and priorities (Ethayarajh & Jurafsky, 2020; Birhane et al., 2022) that specify directions for the AI community to improve upon (Sparck Jones & Galliers, 1995; Sparck Jones, 2005; Kiela et al., 2021; Bowman & Dahl, 2021; Raji et al., 2021). When implemented and interpreted appropriately, they enable the broader community to better understand AI technology and influence its trajectory.

- **Technique:** HOOK -- philosophical/societal framing
- **First sentence analysis:** "Benchmarks orient AI." -- Three words. Declarative. Enormous claim. Does NOT start with "Large language models have..." or "Recently..." -- instead elevates benchmarks themselves to the status of societal instruments. This is a masterclass opening: short, bold, quotable.
- **Why it works:** Immediately positions the paper as being about something bigger than a leaderboard. The reader thinks: "benchmarks are important, and this paper is about to tell me we're doing them wrong."

**Paragraph 2:**

> In recent years, the AI technology that has arguably advanced the most is foundation models (Bommasani et al., 2021), headlined by the rise of language models (LMs; Peters et al., 2018; Devlin et al., 2019; Brown et al., 2020; Rae et al., 2021; Chowdhery et al., 2022). At its core, a language model is a box that takes in text and generates text (Figure 1). Despite their simplicity, when these models are trained on broad data at immense scale, they can be adapted (e.g. prompted or fine-tuned) to myriad downstream scenarios. Yet the immense surface of model capabilities, limitations, and risks remains poorly understood. The rapid development, rising impact, and inadequate understanding demand that we benchmark language models holistically.

- **Technique:** GAP -- establishes the problem space
- **Key move:** "Yet the immense surface of model capabilities, limitations, and risks remains poorly understood." This is the gap sentence. After establishing that LMs are everywhere, it says: we don't actually understand them. The final sentence ("demand that we benchmark...holistically") is the bridge to their solution.

**Paragraph 3:**

> But what does it mean to benchmark language models holistically? Language models are general-purpose text interfaces that could be applied across a vast expanse of scenarios. And for each scenario, we may have a broad set of desiderata: models should be accurate, robust, fair, efficient, and so on. In fact, the relative importance of these desiderata often will depend not only on the perspective and values one has, but the scenario itself (e.g. inference efficiency might be of greater importance in mobile applications).

- **Technique:** DEFINITION/FRAMEWORK -- rhetorical question as transition
- **Key move:** "But what does it mean to benchmark...holistically?" -- Asking the reader to think, then systematically unpacking the answer. This paragraph sets up the intellectual framework before revealing the solution.

**Paragraph 4 (enumerated list):**

> We believe holistic evaluation involves three elements:
>
> 1. **Broad coverage and recognition of incompleteness.** Given language models' vast surface of capabilities and risks, we need to evaluate language models over a broad range of scenarios. [...] However, it is neither possible to consider all the scenarios nor all the desiderata that (could) pertain to LMs. Therefore, holistic evaluation should provide a top-down taxonomy and make explicit all the major scenarios and metrics that are missing.
>
> 2. **Multi-metric measurement.** Societally beneficial systems reflect many values, not just accuracy. Holistic evaluation should represent these plural desiderata, evaluating every desideratum for each scenario considered.
>
> 3. **Standardization.** Our *object* of evaluation is the language model, not a scenario-specific system. Therefore, in order to meaningfully compare different LMs, the strategy for adapting an LM to a scenario should be controlled for. Furthermore, each LM should be evaluated on the same scenarios to the extent possible.

- **Technique:** APPROACH -- the contribution framed as principles
- **Key move:** They don't say "we built a benchmark with X datasets." They articulate *design principles*. This makes the contribution feel principled and inevitable, not arbitrary.

**Paragraph 5:**

> Overall, holistic evaluation builds transparency by assessing language models in their totality. Rather than honing in on a specific aspect, we strive for a fuller characterization of language models to improve scientific understanding and orient societal impact.

- **Technique:** VISION -- connecting back to the opening hook
- **Key move:** Bookends with the opening. "orient societal impact" echoes "Benchmarks orient AI." Circular structure that makes the intro feel complete.

### Lessons for SciFig
- The three-word opening sentence is devastatingly effective
- Never start with "Recently, large language models..."
- Frame your benchmark as serving a societal/scientific purpose, not just a technical gap
- Use a numbered list of design principles to make the approach feel inevitable

---

## 2. TruthfulQA -- Measuring How Models Mimic Human Falsehoods (Lin et al., 2022)

**Published in:** ACL 2022
**Why study this:** Opens with a real-world concern (deployed models making false statements), names specific consequences, and introduces a counterintuitive finding (bigger = less truthful).

### Verbatim Introduction

**Epigraph:**

> "The enemy of truth is blind acceptance." --Anonymous

- **Technique:** EPIGRAPH as hook
- **Why it works:** Sets the thematic tone. The paper is about models blindly reproducing human falsehoods. An unusual move for an NLP paper -- literary, memorable.

**Paragraph 1:**

> There is growing interest in using language models to generate text for practical applications. Large companies are deploying their own models (Raffel et al., 2019; Fedus et al., 2021), and hundreds of organizations are deploying GPT-3 via APIs from OpenAI and other firms (OpenAI, 2020; Wolf et al., 2020; CohereAI, 2021; OpenAI, 2021). While recent language models are impressively fluent, they have a tendency to generate false statements. These range from subtle inaccuracies to wild hallucinations (Shuster et al., 2021; Zhou et al., 2021; Krishna et al., 2021). This leads to three concerns:

- **Technique:** HOOK -- deployment reality + consequences
- **First sentence analysis:** "There is growing interest in using language models to generate text for practical applications." -- Slightly generic opening BUT immediately followed by concrete deployment facts (companies, APIs, hundreds of organizations). The real hook is the pivot: "impressively fluent" BUT "tendency to generate false statements." The word "wild" in "wild hallucinations" is doing heavy lifting.

**Paragraph 2 (enumerated concerns):**

> 1. **Accidental misuse.** Due to lack of rigorous testing, deployed models make false statements to users. This could lead to deception and distrust (Tamkin et al., 2021).
>
> 2. **Blocking positive applications.** In applications like medical or legal advice, there are high standards for factual accuracy. Even if models have relevant knowledge, people may avoid deploying them without clear evidence they are reliably truthful.
>
> 3. **Malicious misuse.** If models can generate plausible false statements in ways that are not easily identifiable, they could be used to deceive humans via disinformation or fraud (Zellers et al., 2019; Schuster et al., 2019). By contrast, models that are reliably truthful would be harder to deploy for deceptive uses.

- **Technique:** STAKES -- why this matters, concretely
- **Key move:** Three categories of harm, each grounded in a real application domain (medical, legal, disinformation). This is NOT abstract -- "people may avoid deploying them" is a concrete business consequence.

**Paragraph 3:**

> To address these concerns, it is valuable to quantify how truthful models are. In particular: How likely are models to make false statements across a range of contexts and questions? Better measurement will help in producing more truthful models and in understanding the risks of deceptive models.

- **Technique:** BRIDGE -- from problem to solution
- **Key move:** "it is valuable to quantify" -- understated, but this is where the benchmark is justified. The measurement itself is the contribution.

**Paragraph 4:**

> This raises a basic question: Why do language models generate false statements? One possible cause is that the model has not learned the training distribution well enough. When asked the question, "What is 1241 x 123?", GPT-3 outputs "14812". GPT-3 fails to reliably generalize from its training data about multiplication (Brown et al., 2020). Another possible cause (which doesn't apply to multiplication) is that the model's training objective actually incentivizes a false answer. We call such false answers *imitative falsehoods*. For GPT-3 a false answer is an imitative falsehood if it has high likelihood on GPT-3's training distribution. Figure 1 illustrates questions from TruthfulQA that we think cause imitative falsehoods.

- **Technique:** MECHANISM -- introducing the key concept
- **Key move:** The concrete example ("What is 1241 x 123?") makes the abstract problem visceral. Then the paper introduces its key conceptual contribution: "imitative falsehoods" -- a new term that reframes the problem. This is the paragraph that makes the paper feel like it has intellectual depth, not just a dataset.

**Paragraph 5:**

> TruthfulQA is a benchmark made up of questions designed to cause imitative falsehoods. One reason to focus on imitative falsehoods is that they are less likely to be covered by existing question-answering benchmarks (Clark et al., 2018; Kwiatkowski et al., 2019; Joshi et al., 2017; Hendrycks et al., 2020). Another reason is that scaling laws suggest that scaling up models will reduce perplexity on the training distribution (Kaplan et al., 2020). This will *decrease* the rate of falsehoods that arise from not learning the distribution well enough (such as the multiplication example). Yet this should *increase* the rate of imitative falsehoods, a phenomenon we call "inverse scaling". Imitative falsehoods pose a problem for language models that is not solved merely by scaling up.

- **Technique:** COUNTERINTUITIVE FINDING as hook for the benchmark
- **Key move:** "inverse scaling" -- the idea that bigger models are LESS truthful is the paper's signature finding, and they plant it right in the introduction. This is the sentence that gets cited: "Imitative falsehoods pose a problem for language models that is not solved merely by scaling up."

### Lessons for SciFig
- Name your key concept early ("imitative falsehoods" = "caption-driven hallucination"?)
- Use a concrete example to make an abstract problem visceral
- Enumerate real-world consequences (accidental, blocking, malicious)
- A counterintuitive finding in the intro creates urgency and memorability
- Epigraphs are unusual and memorable (use sparingly)

---

## 3. FActScore -- Factual Precision in Atomicity Score (Min et al., 2023)

**Published in:** EMNLP 2023
**Why study this:** Introduces a new evaluation *metric*, not just a dataset. Opens with the core measurement problem.

### Verbatim Introduction

**Paragraph 1:**

> Long-form text generated by large language models (LMs) has widely been used (Brown et al., 2020; Ouyang et al., 2022); nonetheless, evaluating their factual precision -- whether each piece of information conveyed in a generation is factually accurate -- remains challenging for two reasons. First, a generation consists of a large number of pieces of information that are a mixture of true or false. Even a single sentence consists of multiple pieces of information (e.g., 4.4 per sentence in ChatGPT, 40% of which are a mixture of supported and unsupported information), making a binary judgment inadequate (Pagnoni et al., 2021). Second, validating every piece of information is time-consuming and costly.

- **Technique:** PROBLEM STATEMENT with concrete data
- **First sentence analysis:** Starts with the common "LMs are widely used" but immediately pivots to the measurement problem with a definition in em-dashes. The real power is the embedded statistic: "4.4 per sentence in ChatGPT, 40% of which are a mixture of supported and unsupported information." Numbers in the first paragraph create credibility.

**Paragraph 2:**

> In this paper, we introduce FActScore (Factual precision in Atomicity Score), a new evaluation of an LM that represents the percentage of atomic facts (pieces of information) supported by a given knowledge source. Computing FActScore involves (1) breaking a generation into a series of atomic facts -- short statements that each contain one piece of information (Nenkova and Passonneau, 2004; Shapira et al., 2019; Zhang and Bansal, 2021; Liu et al., 2022), and (2) assigning a binary label to each atomic fact, allowing a fine-grained evaluation of factual precision. We evaluate FActScore on the task of generating people biographies because generations consist of verifiable statements rather than debatable or subjective ones, and the scope is broad (i.e., covering diverse nationalities, professions, and levels of rarity).

- **Technique:** APPROACH -- clear two-step method
- **Key move:** The method is explained in one paragraph with a numbered procedure. Crystal clear. The choice of biography generation is justified in the same breath.

**Paragraph 3:**

> We perform extensive human annotations to obtain FActScores of three state-of-the-art, commercially available LMs: InstructGPT (Ouyang et al., 2022), ChatGPT (OpenAI, 2022), and search-augmented PerplexityAI. Our results indicate that commercially available LMs are riddled with errors, having FActScores of 42%, 58% and 71%, respectively. Their FActScores significantly drop as the rarity of the entities increases, e.g., 80% -> 16% for ChatGPT.

- **Technique:** FINDINGS -- shocking numbers
- **Key move:** "riddled with errors" -- strong language for an academic paper. The drop from 80% to 16% is the kind of number that gets quoted in blog posts and tweets. They put their most dramatic finding in paragraph 3, not buried in results.

**Paragraph 4:**

> Since human evaluation is costly, we next introduce an automatic evaluation of FActScore through a model that estimates a FActScore for a given LM. Our estimator decomposes generations into atomic facts and validates each based on a given knowledge source, leveraging retrieval from the given knowledge source and strong language models. Our estimator closely approximates FActScore with an error rate of <2% and can be applied to a range of new LMs at scale with no human effort. Our case study evaluates 6,500 generations from 13 LMs that could have cost $26K, with various findings: GPT-4 (OpenAI, 2023) and ChatGPT are far less factual than humans but are much better than public models, and there is a large variance between public models, with Vicuna (Chiang et al., 2023) and Alpaca (Taori et al., 2023) being some of the best.

- **Technique:** SCALABILITY + broader findings
- **Key move:** "$26K" -- putting a dollar figure on the cost of human evaluation makes the automatic estimator feel essential. Concrete cost = concrete value proposition.

**Paragraph 5 (contributions list):**

> In summary, our contributions are as follows.
> 1. We introduce FActScore, a new evaluation of factual precision of LMs [...]
> 2. We introduce a model that approximates FActScore with an error rate of <2% [...]
> 3. We open-sourced FActScore and the annotated data for public use, available via `pip install factscore`. [...]

- **Technique:** CONTRIBUTIONS LIST
- **Key move:** `pip install factscore` in the contributions list. Signaling immediate usability.

### Lessons for SciFig
- Put shocking numbers in paragraph 3, not in results
- Use dollar figures to make cost arguments concrete
- "riddled with errors" -- don't be afraid of strong language when the data supports it
- A degradation curve (80% -> 16%) is more compelling than a single number

---

## 4. MMLU -- Measuring Massive Multitask Language Understanding (Hendrycks et al., 2021)

**Published in:** ICLR 2021
**Why study this:** The "benchmarks keep getting saturated" argument -- establishes that existing evaluations are insufficient because models solve them too quickly.

### Verbatim Introduction

**Paragraph 1:**

> Natural Language Processing (NLP) models have achieved superhuman performance on a number of recently proposed benchmarks. However, these models are still well below human level performance for language understanding as a whole, suggesting a disconnect between our benchmarks and the actual capabilities of these models. The General Language Understanding Evaluation benchmark (GLUE) (Wang et al., 2018) was introduced in 2018 to evaluate performance on a wide range of NLP tasks, and top models achieved superhuman performance within a year. To address the shortcomings of GLUE, researchers designed the SuperGLUE benchmark with more difficult tasks (Wang et al., 2019). About a year since the release of SuperGLUE, performance is again essentially human-level (Raffel et al., 2019). While these benchmarks evaluate linguistic skills more than overall language understanding, an array of commonsense benchmarks have been proposed to measure basic reasoning and everyday knowledge (Zellers et al., 2019; Huang et al., 2019; Bisk et al., 2019). However, these recent benchmarks have similarly seen rapid progress (Khashabi et al., 2020). Overall, the near human-level performance on these benchmarks suggests that they are not capturing important facets of language understanding.

- **Technique:** HOOK -- the "arms race" narrative
- **First sentence analysis:** "Natural Language Processing (NLP) models have achieved superhuman performance on a number of recently proposed benchmarks." -- This IS the "LMs have..." opening, but it immediately subverts it: the achievement is the PROBLEM. Superhuman performance means the benchmarks are broken. The paragraph then walks through GLUE -> SuperGLUE -> commonsense benchmarks, each saturated within a year. This creates a narrative of escalating failure.
- **Why it works:** Every reader who has followed NLP knows this story. The paragraph validates their experience and then names the uncomfortable truth: "they are not capturing important facets of language understanding."

**Paragraph 2:**

> Transformer models have driven this recent progress by pretraining on massive text corpora, including all of Wikipedia, thousands of books, and numerous websites. These models consequently see extensive information about specialized topics, most of which is not assessed by existing NLP benchmarks. It consequently remains an open question just how capable current language models are at learning and applying knowledge from many domains.

- **Technique:** GAP -- the unexplored territory
- **Key move:** "most of which is not assessed by existing NLP benchmarks" -- the gap is not that models are bad, but that we don't know how good they are. This reframes evaluation as discovery.

**Paragraph 3:**

> To bridge the gap between the wide-ranging knowledge that models see during pretraining and the existing measures of success, we introduce a new benchmark for assessing models across a diverse set of subjects that humans learn. We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings. This makes the benchmark more challenging and more similar to how we evaluate humans. The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability. Subjects range from traditional areas, such as mathematics and history, to more specialized areas like law and ethics (Hendrycks et al., 2020). The granularity and breadth of the subjects makes the benchmark ideal for identifying a model's blind spots.

- **Technique:** APPROACH -- the benchmark design
- **Key move:** "more similar to how we evaluate humans" -- the analogy to human testing (exams, professional licensing) makes the benchmark feel natural and well-motivated. 57 subjects gives it the feel of comprehensiveness.

**Paragraph 4:**

> We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b). On the other hand, unlike human professionals, GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects.

- **Technique:** FINDINGS -- the "still far from human" argument
- **Key move:** "meaningful progress has only become possible in recent months" -- positions the benchmark as forward-looking, not yet saturated. The 25% -> 43.9% gap and "lopsided" performance create a clear picture of model limitations.

**Paragraph 5:**

> Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality. This second weakness is particularly concerning because it will be important for future models to have a strong understanding of what is legal and what is ethical. Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy.

- **Technique:** IMPLICATIONS -- connecting findings to societal concerns
- **Key move:** "what is legal and what is ethical" -- elevates a benchmark result into a safety concern. The calibration finding (24% off) adds another dimension. This paragraph does what great evaluation papers do: makes a number feel dangerous.

### Lessons for SciFig
- The "benchmarks keep getting saturated" narrative is powerful for justifying new benchmarks
- Walk through the history of predecessors being solved to show the escalating challenge
- "More similar to how we evaluate humans" is a compelling design principle
- Connect specific failures to societal concerns (law, ethics, safety)

---

## 5. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)

**Published in:** NeurIPS 2023
**Why study this:** Identifies a fundamental disconnect between existing benchmarks and user experience. Opens with a paradox.

### Verbatim Introduction

**Paragraph 1:**

> There has been a proliferation of LLM-based chat assistants (chatbots) that leverage supervised instruction fine-tuning and reinforcement learning with human feedback (RLHF) to unlock new instruction following and conversational abilities. Once aligned with humans, these chat models are strongly preferred by human users over the original, unaligned models on which they are built. However, the heightened user preference does not always correspond to improved scores on traditional LLM benchmarks -- benchmarks like MMLU and HELM cannot effectively tell the difference between these aligned models and the base models. This phenomenon suggests that there is a fundamental discrepancy between user perceptions of the usefulness of chatbots and the criteria adopted by conventional benchmarks.

- **Technique:** HOOK -- the paradox
- **First sentence analysis:** Not the strongest opener (starts with "There has been a proliferation..."), BUT the paragraph quickly builds to a genuine paradox: users strongly prefer aligned models, but benchmarks can't tell them apart. The word "fundamental discrepancy" signals that this is not a small oversight but a structural problem with evaluation.
- **Why it works:** Anyone who has used ChatGPT knows it feels better than GPT-3, but MMLU scores don't show it. The paper names this disconnect.

**Paragraph 2:**

> We argue that this discrepancy primarily arises due to existing evaluation that only measures LLMs' core capability on a confined set of tasks (e.g., multi-choice knowledge or retrieval questions), without adequately assessing its alignment with human preference in open-ended tasks, such as the ability to accurately adhere to instructions in multi-turn dialogues.

- **Technique:** DIAGNOSIS -- naming the cause
- **Key move:** Short, sharp paragraph. One sentence. Identifies exactly what is wrong with existing benchmarks: they measure capability, not alignment. This is the kind of paragraph that makes reviewers nod.

**Paragraph 3:**

> To study this, we introduce two benchmarks with human ratings as the primary evaluation metric: MT-bench and Chatbot Arena. MT-bench is a series of open-ended questions that evaluate a chatbot's multi-turn conversational and instruction-following ability -- two critical elements for human preference. MT-bench is also carefully constructed to differentiate chatbots based on their core capabilities, such as reasoning and math. In addition, we develop Chatbot Arena, a crowdsourced platform featuring anonymous battles between chatbots in real-world scenarios -- Users engage in conversations with two chatbots at the same time and rate their responses based on personal preferences.

- **Technique:** APPROACH -- two complementary solutions
- **Key move:** "anonymous battles between chatbots in real-world scenarios" -- the Arena concept is immediately vivid and engaging. The dual-benchmark design (controlled + wild) addresses both rigor and ecological validity.

**Paragraph 4:**

> While human evaluation is the gold standard for assessing human preferences, it is exceptionally slow and costly. To automate the evaluation, we explore the use of state-of-the-art LLMs, such as GPT-4, as a surrogate for humans. Because these models are often trained with RLHF, they already exhibit strong human alignment. We call this approach "LLM-as-a-judge". This approach has been tried in our earlier blog post and other concurrent or follow-up work. However, there has not been a systematic study of this approach.

- **Technique:** SECOND GAP -- the automation problem
- **Key move:** Introduces "LLM-as-a-judge" as a named concept. The paper is solving two problems at once: (1) what to evaluate and (2) how to evaluate it cheaply. Naming the concept is crucial -- it becomes the paper's lasting contribution to the field's vocabulary.

**Paragraph 5:**

> In this paper, we study the LLM-as-a-judge approach by comparing it to the gold standard of human evaluation. We examine several potential limitations of the LLM-as-a-judge approach including position bias, verbosity bias, self-enhancement bias, and limited reasoning ability. We show that some of the biases are minor or can be mitigated. Once addressed, our results from 3K controlled expert votes and 3K crowdsourced human votes in the wild verify that "GPT-4 judge match human evaluations at an agreement rate exceeding 80%, achieving the same level of human-human agreement." Consequently, this suggests LLM-as-a-judge is a scalable method to swiftly evaluate human preference, serving as a promising alternative to traditional human evaluations.

- **Technique:** VALIDATION -- credibility through scale and rigor
- **Key move:** "3K controlled expert votes and 3K crowdsourced human votes" -- the dual validation (expert + crowd) and the specific number "exceeding 80%" matching "human-human agreement" is the key result. Placing it in the intro signals confidence.

**Paragraph 6:**

> This paper makes two contributions: (1) a systematic study of LLM-as-a-judge; and (2) human preference datasets with high-quality questions and diverse user interactions from MT-bench and Chatbot Arena. In addition, we argue for the adoption of a hybrid evaluation framework for future LLM benchmarks: by combining the existing capability-based benchmarks and the new preference-based benchmarks with LLM-as-a-judge, one can swiftly and automatically evaluate both the core capabilities and human alignment of models. We publicly release 80 MT-bench questions, 3K expert votes, and 30K conversations with human preferences for future study.

- **Technique:** CONTRIBUTIONS + VISION
- **Key move:** "we argue for the adoption of a hybrid evaluation framework" -- the paper doesn't just contribute a benchmark; it proposes a new paradigm for how evaluation should work. This elevates it beyond a resource paper.

### Lessons for SciFig
- A paradox (users love it, benchmarks can't tell) is an extremely effective hook
- Name your concepts ("LLM-as-a-judge" = instantly citeable)
- Solve two problems at once (what to measure + how to measure cheaply)
- Propose a paradigm, not just a dataset
- One-sentence paragraphs can be powerful for the diagnosis

---

## 6. GPQA -- A Graduate-Level Google-Proof Q&A Benchmark (Rein et al., 2023)

**Published in:** arXiv 2023 (later ICLR 2024)
**Why study this:** Opens with a forward-looking *safety* argument rather than a capabilities argument. The benchmark is motivated by a future problem, not a current one.

### Verbatim Introduction

**Paragraph 1:**

> Rapid advancements in large language model (LLM) capabilities present the possibility that in the near future, narrowly superhuman AI systems could help advance the frontier of human knowledge. To measure our ability to align models for this purpose, we need evaluation testbeds for reliably extracting truthful information from these models even on questions where we cannot produce or verify the truth on our own -- a problem known as *scalable oversight* (Amodei et al., 2016). These testbeds need to be maximally difficult even for highly skilled non-experts to solve on their own, to give the best chance of generalization to harder tasks that no human can complete. As LLMs are used to answer increasingly difficult questions, we expect it will become harder for human annotators to directly evaluate the truthfulness of model responses, particularly in domains requiring large amounts of specialized knowledge and expertise. Oversight methods like reinforcement learning from human feedback (RLHF; Christiano et al., 2017) rely on human annotators' ability to accurately determine whether the LLMs' output is actually correct. In settings where annotators cannot do this, we would expect issues like hallucination (Zhang et al., 2023) and sycophancy (Perez et al., 2022b; Sharma et al., 2023) to be exacerbated.

- **Technique:** HOOK -- future-oriented safety framing
- **First sentence analysis:** "Rapid advancements in large language model (LLM) capabilities present the possibility that in the near future, narrowly superhuman AI systems could help advance the frontier of human knowledge." -- This IS the "LLMs are advancing" opening, but it immediately orients toward the FUTURE and toward SAFETY. The key concept "scalable oversight" appears in the first paragraph. The paper is not about measuring current models -- it's about preparing for future ones.
- **Why it works:** Makes a benchmark paper feel like it's about the future of AI safety, not just another leaderboard.

**Paragraph 2:**

> To study methods for scalable oversight in this setting, we need tasks that non-experts are unable to complete on their own. For some tasks, merely giving the non-expert access to internet resources will be enough for them to verify an AI system's output. But when overseeing LLMs' ability to, for example, help create new knowledge in scientific disciplines where expert consensus hasn't already been reached, we expect scalable oversight to require the full abilities of *expert* overseers, including access to large sources of information like the internet. Collecting evidence that we can successfully supervise superhuman models requires datasets that test as close as possible to the edge of human expertise -- ideally, datasets of questions which have a ground truth answer known to certain experts, but which even highly skilled, well resourced, and motivated non-experts still cannot reliably solve.

- **Technique:** GAP -- the specific type of difficulty needed
- **Key move:** "the edge of human expertise" -- this phrase defines the benchmark's design goal. The distinction between expert and non-expert is the paper's core mechanism.

**Paragraph 3:**

> With this goal in mind, we present GPQA, an evaluation dataset consisting of graduate-level multiple-choice questions in subdomains of physics, chemistry, and biology. Uniquely, in addition to validating the questions' correctness with domain experts, we also ensure that the questions are difficult for highly skilled and incentivized non-experts, who have or are pursuing PhDs in *other* domains, and who have access to any internet resources they can find (excluding LLM assistants), spending on average 37 minutes trying to answer each question.

- **Technique:** APPROACH -- with the "Google-proof" hook
- **Key move:** "spending on average 37 minutes trying to answer each question" -- this single statistic communicates the difficulty better than any adjective could. "Google-proof" (from the title) is the concept that makes this paper memorable.

**Paragraph 4:**

> The questions are reasonably objective: experts achieve 65% accuracy, and many of their errors arise not from disagreement over the correct answer to the question, but mistakes due to the question's sheer difficulty (when accounting for this conservatively, expert agreement is 74%). In contrast, our non-experts achieve only 34% accuracy, and GPT-4 with few-shot chain-of-thought prompting achieves 39%, where 25% accuracy is random chance. This confirms that GPQA is difficult enough to be useful for scalable oversight research on future models significantly more capable than the best existing public models.

- **Technique:** FINDINGS -- the difficulty proof
- **Key move:** The expert vs. non-expert vs. GPT-4 comparison (65% vs. 34% vs. 39%) is the paper's signature result. Non-experts WITH Google perform worse than experts WITHOUT it. GPT-4 is barely above non-experts. This three-way comparison is elegant and immediately convincing.

### Lessons for SciFig
- Motivate a benchmark with a future problem, not just a current gap
- A single vivid statistic ("37 minutes per question") communicates difficulty better than adjectives
- The three-way comparison (expert vs. non-expert vs. model) is a powerful proof of concept
- "Google-proof" as a concept is sticky and memorable -- find your equivalent

---

## Cross-Paper Analysis: Patterns and Anti-Patterns

### What the best papers do in their first sentence:

| Paper | First sentence | Technique |
|-------|---------------|-----------|
| HELM | "Benchmarks orient AI." | Bold 3-word declaration |
| TruthfulQA | "There is growing interest..." | Generic BUT immediately pivots to specifics |
| FActScore | "Long-form text generated by LMs has widely been used..." | Generic BUT embeds the measurement problem in same sentence |
| MMLU | "NLP models have achieved superhuman performance..." | Achievement-as-problem subversion |
| LLM-as-Judge | "There has been a proliferation..." | Generic, weakest opener of the set |
| GPQA | "Rapid advancements in LLM capabilities present the possibility..." | Future-oriented, safety-motivated |

**Winner:** HELM's "Benchmarks orient AI." -- by a mile.

### The 5-paragraph structure that works:

1. **Hook** -- Why should anyone care? (societal stake, paradox, failure, or bold claim)
2. **Gap** -- What's broken about current evaluation? (with evidence)
3. **Approach** -- What do we do about it? (framed as principles, not just "we built X")
4. **Findings** -- What did we discover? (most dramatic number, in the intro, not buried)
5. **Contributions/Vision** -- What does this change? (paradigm shift, not just a resource)

### Anti-patterns to avoid:

- "Large language models have shown remarkable capabilities..." (3 of 6 papers open this way or close to it -- the WEAKEST parts of their intros)
- Saving all findings for the results section (every good paper previews the most dramatic finding)
- Listing datasets and models without framing WHY they matter
- Contribution lists that are just method steps ("We collect... We evaluate... We release...")

### What SciFig can learn:

1. **Your HELM-style opener could be:** "Scientific figures are the evidence of science." or "When a model describes a chart, it reveals what it actually sees -- and what it fabricates."
2. **Your TruthfulQA-style concept could be:** Name the phenomenon. "Caption-driven hallucination"? "Visual confabulation"? Give it a term.
3. **Your FActScore-style number could be:** Put your most dramatic finding in paragraph 3. "Models hallucinate axis values in 47% of descriptions" (or whatever the number is).
4. **Your MMLU-style argument could be:** Walk through how figure understanding benchmarks keep getting "solved" while models still can't read a bar chart correctly.
5. **Your GPQA-style forward argument could be:** "As scientific publishing accelerates, automated figure understanding becomes critical for literature review, accessibility, and reproducibility."
