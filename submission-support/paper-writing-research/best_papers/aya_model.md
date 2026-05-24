# Aya Model: An Instruction Finetuned Open-Access Multilingual Language Model

**Authors:** Ahmet Ustun, Viraat Aryabumi, Zheng-Xin Yong, Wei-Yin Ko, Daniel D'souza, Gbemileke Onilude, Neel Bhandari, Shivalika Singh, Hui-Lee Ooi, Amr Kayid, Freddie Vargus, Phil Blunsom, Shayne Longpre, Niklas Muennighoff, Marzieh Fadaee, Julia Kreutzer, Sara Hooker
**Venue:** ACL 2024 Outstanding Paper
**ArXiv:** https://arxiv.org/abs/2402.07827

---

## Introduction

*The limits of my language means the limits of my world.* -- Ludwig Wittgenstein

A fundamental question in machine learning is how to effectively capture the nuances of the long tail. The world around us, encompassing language and tangible objects, is naturally filled with rare and underrepresented examples. Yet, this imbalance intensifies as we transpose our intricate world into the matrices of data that train our models. Datasets have been the foundation of modern machine learning progress, but have coalesced around a few data-rich languages. What languages are favored is often a symptom of historical technological use and access to resources, rather than the languages most frequently spoken or written in the real world.

Recent breakthroughs in natural language processing (NLP) have been no different, with the instruction-following capabilities of existing open-source models, such as Alpaca, Dolly, and Vicuna, mainly developed for English tasks. Instruction finetuning (IFT) involves curating pairs of prompts and completions, and has been shown to significantly improve the helpfulness and general instruction following capabilities of large language models (LLMs). However, a sizable gap between the available amount of instruction prompts for English and all other languages exists. More than 7,000 languages are spoken around the world today, but an astounding 73% of popular IFT datasets are primarily English.

This severe sampling bias in the construction of our datasets violates a key machine learning principle: *your training distribution should mirror the underlying distribution you hope to model in the real world*. The consequence is that recent breakthroughs in NLP have amplified disparities in model performance outside of resource-rich languages. Models perform better on the distribution they are trained to mimic which often introduces known biases towards languages not included during training and critical security and safety flaws for all users. A growing divide in the cost of use of technology is emerging as marginalized languages require more tokens and incur higher latency for generations, consigning speakers of lower-performing languages to lower-quality technology.

Bridging this widening language gap and conferring *Multilingual Instruction-Following Capabilities* is not a trivial problem. Some multilingual abilities can be inherited by pretraining on diverse multilingual data -- often described as *surprising* multilingual abilities noted in finetuned models like PaLM or Flan-PaLM which are not explicitly finetuned to be multilingual. However, this was not proven to be competitive with a second direction of *both* pretraining and instruction finetuning with a multilingual corpus. Pursuing this second approach has been the subject of several recent works where the persistent struggle to secure comprehensive multilingual IFT datasets remains a fundamental obstacle. This second direction is the focus of our work.

**In this work, we address several core limitations of recent multilingual IFT models in order to reduce their linguistic inequality:** We aim to create a model that performs well on downstream tasks when given prompts in any of the included languages, rather than requiring multilingual speakers to write prompts in English. Our goal is also to greatly expand the coverage of languages to 101, far beyond the current coverage of open-source massively multilingual models such as Okapi (25 languages), mT0 (46 languages), BLOOMZ (46 languages), and Bactrian-X (52 languages). To do so, we embark on an ambitious effort to expand the size of the training corpus as well as the breadth of evaluation.

The core contribution of our work is an **open-source multilingual instruction-finetuned LLM with diverse linguistic representation**: the **Aya** model. Our primary contributions can be enumerated as follows:

1. **Expansion of Language Coverage** We significantly expand the size of available training data to directly address the linguistic inequality of recent NLP development. In comparison to recently proposed multilingual IFT datasets such as xP3 which covers 46 languages and includes 81M data points, our Aya training mix broadens coverage to 101 languages and is 2.5x the size of the original xP3 dataset with 203M data points. Perhaps more significantly, while prior datasets like xP3 remain 39% English, our mix is far less skewed with only 21.5% English. Among the 101 languages covered by Aya, 51 are deemed lower-resourced.

2. **Broadening Multilingual Evaluation** We extend the axes of multilingual evaluation to cover 99 languages by investing in evaluation across 1) discriminative 2) generative 3) LLM-as-a-judge simulated win rate comparisons, 4) human evaluation, and 5) safety evaluations. Across these benchmarks, our Aya model demonstrates relative performance gains of 13.1% and 11.7% over mT0x for discriminative and generative tasks respectively. Human preference evaluations for 7 languages show win rates of 75% relative to mT0x.

3. **Data Weighting and Pruning** Our emphasis on only using datasets with permissive licensing results in an over-indexing of academic-style multilingual datasets. To rebalance the distribution, we explore the benefits of data pruning, removing 19.66% of English instances and 18.25% of multilingual instances based upon human annotations. Additionally, we conduct extensive ablations to explore the role of different data sources by varying the weight of 1) translated data, 2) templated data, and 3) human annotations.

4. **Safety** We implement multilingual safety context distillation as a first step towards mitigating LLM safety concerns multilingually. This step reduces harmful generations for adversarial prompts by 78-89% as judged by human experts. To further characterize the risk profile of our model, we perform an analysis of toxicity, social bias, and gender bias in models' generations across 18 languages.

---

## Results (First Paragraphs)

We report results of our Aya model and its variants against the baseline models across our expanded evaluations. The Aya human-anno-heavy, Aya template-heavy, and Aya translation-heavy variants of our Aya model are based on the sampling ablations.

### Discriminative Tasks

#### Unseen tasks

Table 5 and Figure 3a show average scores across languages for unseen discriminative tasks on XWinograd, XNLI, XCOPA, and XStoryCloze. We compare Aya models with the following baselines: (1) mT0, (2) BLOOMZ, (3) Bactrian-X, and (4) mT0x. Among these baselines, all Aya variants and mT0x saw 101 languages during instruction tuning while Bactrian-X saw 52 and mT0/BLOOMZ saw 46. Since all discriminative tasks were unseen during training, we measure zero-shot performance during evaluations.

**Comparison with mT0, BLOOMZ, Bactrian-X:** Our Aya model covers approximately double the languages of these baselines, and so we expect these to be strong baselines in line with *the curse of multilinguality*. As seen in Table 5, our best Aya variant (template-heavy) scores an average performance of 75.12% despite the massive jump in languages covered. Of the baselines, mT0 (46 languages) scored the highest average performance at 72.9% and Bactrian-X (52 languages) was the lowest at 47.3%. Aya (template-heavy) outperforms these baselines by an average of 19.8% across tasks.

This shows the importance of a high-quality, diverse, and balanced instruction finetuning mixture to achieve high performance and offset *the curse of multilinguality*.

---

## Conclusion

[Note: The full conclusion was not available in the HTML extraction -- the paper content was truncated before reaching the conclusion section.]

---

## Notable Writing Observations

- Opens with a literary epigraph (Wittgenstein quote), setting a philosophical tone for what is fundamentally a systems paper
- Frames the problem as a machine learning principle violation: "your training distribution should mirror the underlying distribution you hope to model"
- Strong use of comparative statistics: "73% of popular IFT datasets are primarily English"
- The word "ambitious" is used without false modesty -- justified by the scale (101 languages)
- Contributions are clearly enumerated with bold headers and concrete numbers
- Italic emphasis on key phrases like "the curse of multilinguality" to flag recurring themes
- The phrase "consigning speakers of lower-performing languages to lower-quality technology" adds moral weight to a technical problem
