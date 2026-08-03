# Response to Reviewer h9tb

## Reviewer scores (for our reference, do not include in submitted rebuttal)

Overall: 3 (Findings) · Soundness: 3 · Excitement: 3.5 · Confidence: 3
Reproducibility: 5 · Datasets: 5 · Software: 5

---

We thank the reviewer for the positive assessment and thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1.** Despite harvesting charts from authentic arXiv research papers, the dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding.

A: We agree that three chart types do not fully represent the diversity of scientific figures, and we do not intend SciFig-Eval to make that claim. Our present scope prioritises diagnostic depth. The 250 authentic figures from 187 papers support more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 capability questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets. Split-half reliability is high at $\rho=0.979$, indicating stable model rankings within this scope. Broader coverage of scatter plots, heatmaps, schematics, and other scientific figures remains important future work, as already stated in our Limitations section.

**W2.** Section 5 notes that Inexist probes, which embed false assumptions via definite articles, serve as the most potent deception vectors across all architectures due to a persistent "must answer" bias. However, the paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressures the model to comply with user prompts regardless of conflicting visual data.

A: This is a great point. This distinction is a central motivation for SciFig-Eval’s staged design. We first establish visual perception quality through open-ended descriptions of clean figures, then evaluate figure-grounded reasoning, before testing behavioural resistance to misleading queries. Models generally demonstrate substantial visual perception, with MQM scores reaching 91.6, while their Inexist resistance varies substantially and is often much poorer. This variation makes general visual inability unlikely to be the sole explanation. Instead, it shows that models capable of interpreting a figure can still accept a linguistically embedded false premise. We will clarify that the Inexist results identify this perception-behaviour dissociation and are consistent with instruction-tuning or presupposition pressure, without claiming to causally identify the internal training mechanism.

## Comments Suggestions And Typos

**C1.** Please ensure consistency when writing the name of Llama 4.

A: Thank you for catching this. We will standardise the model name as “Llama 4 Maverick” throughout the paper, tables, and appendices.
