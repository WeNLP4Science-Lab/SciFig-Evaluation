# Are Emergent Abilities of Large Language Models a Mirage?

**Authors:** Rylan Schaeffer, Brando Miranda, Sanmi Koyejo
**Venue:** NeurIPS 2023 Outstanding Paper Award
**ArXiv:** https://arxiv.org/abs/2304.15004

---

## Introduction

Emergent properties of complex systems have long been studied across disciplines, from physics to biology to mathematics. The idea of emergence was popularized by Nobel Prize-winning physicist P.W. Anderson's "More Is Different", which argues that as the complexity of a system increases, new properties may materialize that cannot be predicted even from a precise quantitative understanding of the system's microscopic details. Recently, the idea of emergence gained significant attention in machine learning due to observations that large language models (LLMs) such as GPT, PaLM and LaMDA exhibit so-called "emergent abilities."

The term "emergent abilities of LLMs" was recently and crisply defined as "abilities that are not present in smaller-scale models but are present in large-scale models; thus they cannot be predicted by simply extrapolating the performance improvements on smaller-scale models." Such emergent abilities were first discovered in the GPT-3 family. Subsequent work emphasized the discovery, writing that "[although model] performance is predictable at a general level, performance on a specific task can sometimes emerge quite unpredictably and abruptly at scale." These quotations collectively identify the two defining properties of emergent abilities in LLMs:

1. *Sharpness*, transitioning seemingly instantaneously from not present to present
2. *Unpredictability*, transitioning at seemingly unforeseeable model scales

These emergent abilities have garnered significant interest, raising questions such as: What controls *which* abilities will emerge? What controls *when* abilities will emerge? How can we make desirable abilities emerge faster, and ensure undesirable abilities never emerge? These questions are especially pertinent to AI safety and alignment, as emergent abilities forewarn that larger models might one day, without warning, acquire undesired mastery over dangerous capabilities.

In this paper, we call into question the claim that LLMs possess emergent abilities, by which we specifically mean *sharp* and *unpredictable* changes in model outputs as a function of model scale on specific tasks. Our doubt stems from the observation that emergent abilities seem to appear only under metrics that nonlinearly or discontinuously scale any model's per-token error rate. For instance, as we later show, > 92% of emergent abilities on BIG-Bench tasks (hand-annotated by [32]) appear under either of these two metrics:

Multiple Choice Grade: 1 if highest probability mass on correct option, 0 otherwise
Exact String Match: 1 if output string exactly matches target string, 0 otherwise

This raises the possibility of an alternative explanation for the origin of LLMs' emergent abilities: sharp and unpredictable changes might be induced by the researcher's choice of measurement, even though the model family's per-token error rate changes smoothly, continuously and predictably with increasing scale. Specifically, our alternative posits that emergent abilities are a mirage caused primarily by the researcher choosing a metric that nonlinearly or discontinuously deforms per-token error rates, and secondarily by possessing too few test data to accurately estimate the performance of smaller models, thereby causing smaller models to appear wholly unable to perform the task.

To communicate our alternative explanation, we present it as a simple mathematical model and demonstrate how it quantitatively reproduces the evidence offered in support of emergent abilities of LLMs. We then test our alternative explanation in three complementary ways:

1. We make, test and confirm three predictions based on our alternative hypotheses using the InstructGPT / GPT-3 model family.
2. We meta-analyze published benchmarks to reveal that emergent abilities only appear for specific metrics, not for model families on particular tasks, and that changing the metric causes the emergence phenomenon to evaporate.
3. We induce never-before-seen, seemingly emergent abilities in multiple architectures across various vision tasks by intentionally changing the metrics used for evaluation.

---

## Experiments / Results (Section 3: Analyzing InstructGPT/GPT-3's Emergent Arithmetic Abilities)

Previous papers prominently claimed the GPT family displays emergent abilities at integer arithmetic tasks. We chose these tasks as they were prominently presented, and we focused on the GPT family due to it being publicly queryable. As explained mathematically and visually in Sec. 2, our alternative explanation makes three predictions:

1. Changing the metric from a nonlinear or discontinuous metric to a linear or continuous metric should reveal smooth, continuous, predictable performance improvement with model scale.
2. For nonlinear metrics, increasing the resolution of measured model performance by increasing the test dataset size should reveal smooth, continuous, predictable model improvements commensurate with the predictable nonlinear effect of the chosen metric.
3. Regardless of metric, increasing the target string length should predictably affect the model's performance as a function of the length-1 target performance: approximately geometrically for accuracy and approximately quasilinearly for token edit distance.

To test these predictions, we collected outputs from the InstructGPT/GPT-3 family on two tasks: 2-shot multiplication between two 2-digit integers and 2-shot addition between two 4-digit integers.

**Prediction: Emergent Abilities Disappear With Different Metrics.** On both arithmetic tasks, the GPT family displays emergent abilities if the target has 4 or 5 digits and if the metric is Accuracy. However, if one changes from nonlinear Accuracy to linear Token Edit Distance *while keeping the models' outputs fixed*, the family's performance smoothly, continuously and predictably improves with increasing scale. This confirms our first prediction and supports our alternative explanation that the source of emergent abilities is the researcher's choice of metric, *not changes in the model family's outputs*.

**Prediction: Emergent Abilities Disappear With Better Statistics.** We next tested our second prediction: that even on nonlinear metrics such as accuracy, smaller models do not have zero accuracy, but rather have non-zero above-chance accuracy *commensurate with choosing to use accuracy as the metric*. In order to accurately measure models' accuracy, we increased the resolution by generating additional test data, and found that on both arithmetic tasks, all models in the InstructGPT/GPT-3 family achieve above-chance accuracy.

---

## Discussion (Conclusion)

Our paper presents an alternative explanation for claimed emergent abilities of large language models. For a fixed task and a fixed model family, the researcher can choose a metric to create an emergent ability or choose a metric to ablate an emergent ability. Ergo, *emergent abilities may be creations of the researcher's choices, not a fundamental property of the model family on the specific task*. We emphasize that nothing in this paper should be interpreted as claiming that large language models *cannot* display emergent abilities; rather, our message is that previously claimed emergent abilities in [3, 8, 28, 33] might likely be a mirage induced by researcher analyses.

Our paper has several implications. Firstly, a task and a metric are distinct and meaningful choices when constructing a benchmark. Secondly, when choosing metric(s), one should consider the metric's effect on the per-token error rate and adapt their measuring process accordingly, e.g., if one chooses accuracy, one should make sure to have sufficient data to accurately measure accuracy to avoid the risk of drawing invalid scientific conclusions. Thirdly, when making claims about capabilities of large models, including proper controls is critical. In this particular setting, emergent abilities claims are possibly infected by a failure to control for multiple comparisons. In BIG-Bench alone, there are >= 220 tasks, ~40 metrics per task, ~10 model families, for a total of ~10^6 task-metric-model family triplets, meaning probability that *no* task-metric-model family triplet exhibits an emergent ability by random chance might be small. Fourthly, scientific progress can be hampered when models and their outputs are not made public for independent scientific investigation.

---

## Notable Writing Observations

- Masterful use of "Ergo" -- a single Latin word that carries the weight of the entire argument
- The paper's core argument is devastatingly simple: it's the metric, not the model. This simplicity is a rhetorical strength
- The word "mirage" in the title is perfect -- evocative, precise, and memorable
- Strong epistemic hedging: "We emphasize that nothing in this paper should be interpreted as claiming that large language models *cannot* display emergent abilities"
- The numbered predictions structure (predict, test, confirm) gives the experiments a hypothesis-driven scientific feel that is very compelling
- Uses "while keeping the models' outputs fixed" -- a devastating clause that makes the metric-dependence argument irrefutable
- The multiple comparisons point in the discussion is a methodological insight that applies far beyond this specific paper
- Directly relevant to our work: their argument about metric choice affecting conclusions about model capabilities parallels our MQM evaluation design choices
