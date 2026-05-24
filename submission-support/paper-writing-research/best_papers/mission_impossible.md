# Mission: Impossible Language Models

**Authors:** Julie Kallini, Isabel Papadimitriou, Richard Futrell, Kyle Mahowald, Christopher Potts
**Venue:** ACL 2024 Best Paper Award
**ArXiv:** https://arxiv.org/abs/2401.06416

---

## Introduction

Chomsky (2023), Chomsky et al. (2023), Moro et al. (2023), and Bolhuis et al. (2024) make very broad claims to the effect that large language models (LLMs) are equally capable of learning possible and impossible human languages. For these authors, it follows from this claim that LLMs cannot teach us anything about language, and so the claim (if true) would have significant consequences for linguistic methodology and potentially also for the viability of LLMs as the basis for robust language capabilities.

These authors state this claim in absolute terms. For example, Chomsky et al. (2023) flatly assert that LLMs "are incapable of distinguishing the possible from the impossible," Chomsky (2023) says this property "can't be modified," and Moro et al. (2023) write that "the distinction between possible versus impossible languages cannot be formulated by definition for LLM." Bolhuis et al. (2024) go so far as to claim that "LLMs can produce 'impossible' languages [...] just as well as (if not better than) natural language output." One might expect such strong claims to be supported by extensive formal analysis and/or experimental evidence. However, as far as we are aware, this is not the case. The sole experimental paper cited by the above authors is Mitchell and Bowers (2020) -- an important and inspiring paper but not one that can resolve these questions on its own. In addition, linguists themselves do not even have an agreed upon notion of what defines the possible or the impossible languages, to say nothing of having formal results with respect to LLMs.

Here we provide extensive new experimental evidence to inform the claim that LLMs are equally capable of learning possible and impossible languages in the human sense. Arguably, the central challenge for such work is the fact that there is no agreed-upon way of distinguishing these two groups. We do not feel positioned ourselves to assert such a definition, so we instead offer some examples of impossible languages on a continuum of intuitive complexity. Some of these examples seem intuitively impossible, such as random sentence-level shuffling of English words. Others operationalize less obvious but common claims in the linguistics literature about rules that are impossible, like those that depend on counting words.

All of our examples are, we take it, uncontroversial instances of impossible languages. Thus, our experiments can inform the core hypotheses as follows: if LLMs learn these languages as well as they learn natural languages, then the claims of Chomsky and others are supported (for the specific class of LLMs tested). Conversely, if LLMs do not learn these languages as well as the possible ones, it would call into question those assertions. In that case, proponents of those claims ought to provide examples of impossible languages that they find more informative, which we can then evaluate using our approach to further advance the discussion.

Our experiments use GPT-2 small models (Radford et al., 2018, 2019), and our base training corpus is the BabyLM dataset (Warstadt et al., 2023), which we modify in various ways to implement our impossible languages. What we find is that these models indeed struggle to learn impossible languages, shown through three core experiments:

- In Experiment 1, we train GPT-2 models on our set of defined possible and impossible languages, measuring their learning efficiency through test set perplexities. We find that *models trained on possible languages learn more efficiently*, evident from lower perplexities achieved in fewer training steps.

- In Experiment 2, we more closely examine a set of languages that exhibit count-based verb marking rules, using surprisal comparisons to target the relevant patterns. We find that *GPT-2s trained on possible languages are more surprised by ungrammatical constructions*, indicating that *models disprefer agreement rules involving counting*.

- In Experiment 3, we dive deeper into the internal mechanisms that models may develop to learn such count-based grammar rules using causal abstraction analysis. We find that *models develop natural, modular solutions to unnatural grammatical patterns*.

Overall, our experimental results strongly challenge the claims of Chomsky and others given above, and we believe they pave the way for even deeper discussions of LLMs as models of language learning. At the same time, we recognize that models and humans exhibit fundamental differences, but the extent to which models favor or disfavor natural languages can be influenced by specific architectural decisions (as demonstrated by our findings on tokenization and positional encodings). We hope this paper initiates a new line of work that explores how different model architectures can distinguish between the possible and impossible languages.

---

## Experiments (First Paragraphs)

We train GPT-2 models on all of the languages described in Table 1, and evaluate each model's perplexities on a test set over the course of training. Test perplexities provide a general metric for the extent to which a model has learned a language.

**Setup.** We sample 10K sentences from the BabyLM test set and perturb this sample for each impossible language. For a given impossible language model, we report the geometric mean of the individual sentence perplexities in the corresponding test sample.

**Hypothesis.** Models trained on possible languages will achieve lower average perplexities more quickly (as measured in training steps) than those trained on impossible languages.

**Results.** Our results are in Figure 2. There are clear distinctions between model perplexities after about 500 training steps. First considering the *Shuffle models, the NondeterministicShuffle model has the highest perplexities, followed by the three DeterministicShuffle models, indicating that GPT-2 is better at learning shuffling patterns when they are deterministic, invertible functions.

---

## Discussion and Conclusion

Contra claims by Chomsky and others that LLMs cannot possibly inform our understanding of human language, we argue there is great value in treating LLMs as a comparative system for human language and in understanding what systems like LLMs can and cannot learn. Prior explorations of neural language models have already been fruitful for understanding the generalization of syntactic principles from data (Wilcox et al., 2018; Marvin and Linzen, 2018; Futrell et al., 2019; Prasad et al., 2019; Hu et al., 2020). Our paper complements this line of work. We have shown that GPT-2 models do not master our set of synthetic impossible languages as well as natural ones, challenging the unfounded assertions stated previously.

Even in the absence of a clear definition of what constitutes a possible or impossible language, we believe that our investigations advance this debate regarding LLMs. The lack of a definition does not hinder inquiry into this topic; in fact, it beckons further explorations of the boundary between the possible and impossible languages, as shown in our hypothesized continuum in Figure 1. We believe that the *Hop languages we propose closely approach this boundary.

At the same time, conclusions about LLMs' linguistic competence and preferences for natural languages should be informed by an understanding of the ways that models fundamentally differ from humans. For instance, we saw that models can perform operations that involve counting tokens because LLMs rely on tokens as basic units. While humans are sensitive to morpheme boundaries and word boundaries, it is unlikely humans rely on atomic tokens in the way that LLMs do. This does not mean that LLMs can fundamentally tell us nothing about human language. Rather, as we did here, it is valuable to consider and control for this difference before making generalizations.

Since at least the 1950s, a major line of linguistic inquiry has focused on what aspects of syntactic structure can be learned just from data, without domain-specific innate priors (e.g. a Universal Grammar). LLMs lack strong in-built linguistic priors, yet they can learn complex syntactic structures. While many LLMs are trained with vastly more data than children see, there is increasing evidence that even systems trained on smaller amounts of data can learn interesting linguistic information (Warstadt et al., 2023). The current paper raises further questions along similar lines. Since we do find that real languages are more learnable by GPT-2, this leads us to wonder what inductive bias of GPT language models matches natural language. We believe that this inductive bias is related to information locality, the tendency for statistical correlations in text to be short range. Information locality arises in GPTs due to their autoregressive training objective and has been argued to arise in humans due to the incremental nature of real-time language processing (Futrell, 2019; Hahn et al., 2021).

Since LLMs have been shown to learn the complex structures of human language and have a preference for learning such structures over unnatural counterfactuals, it follows that they are clearly relevant to investigations and claims about the necessary innate priors for language learning. Arguments that they are "by design, unlimited in what they can 'learn'" and "incapable of distinguishing the possible from the impossible" (Chomsky et al., 2023) do not offer convincing evidence otherwise.

---

## Notable Writing Observations

- The introduction opens by directly quoting the opposition's claims, setting up a clear adversarial framing
- Strong use of "we take it" and "as far as we are aware" for epistemic hedging
- The paper frames its contribution as informing a debate rather than definitively settling it
- Bullet-point experiment summaries in the intro give a clear roadmap with italicized findings
- The conclusion circles back to the exact claims made in the introduction, creating satisfying closure
