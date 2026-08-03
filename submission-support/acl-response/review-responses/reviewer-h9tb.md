# Response to Reviewer h9tb

## Reviewer scores (for our reference, do not include in submitted rebuttal)

Overall: 3 (Findings) · Soundness: 3 · Excitement: 3.5 · Confidence: 3
Reproducibility: 5 · Datasets: 5 · Software: 5

---

We thank the reviewer for the positive assessment and thoughtful feedback. We address each point below.

## Summary of Weaknesses

**W1.** Despite harvesting charts from authentic arXiv research papers, the dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding.

A: We agree that three chart types do not fully represent the diversity of scientific figures, and we do not intend SciFig-Eval to make that claim. Within the current scope, the dataset contribution extends beyond the raw figure count in two respects.

First, high-quality human annotation was carried out across perception, reasoning, and behaviour. All 250 figures received human-annotated expert ground-truth descriptions. 1,000 reasoning questions were independently human-reviewed against the source figures. 443 selective-blur targets were confirmed or replaced through human review using our OCR-localised pipeline. MQM judge validation was performed by three graduate-level annotators, with Krippendorff's α=0.91 on double-annotated pairs.

Second, the 250 figures were extended into a comprehensive evaluation benchmark through image transformations (1,243 transformed and page-context cases), 1,000 reasoning questions, 750 resistance probes, 100 caption-bias probes, and 443 confirmed selective-blur targets, producing over 34,000 evaluation setups across eight models. Split-half reliability is ρ=0.979 across 100 random splits, indicating stable model rankings within this scope.

Broader coverage of scatter plots, heatmaps, schematics, and other scientific figures remains important future work, as already stated in our Limitations section.

**W2.** Section 5 notes that Inexist probes, which embed false assumptions via definite articles, serve as the most potent deception vectors across all architectures due to a persistent "must answer" bias. However, the paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressures the model to comply with user prompts regardless of conflicting visual data.

A: This is a great point, and it is precisely what our staged evaluation design is intended to address. Our perception task measures how well models can see and describe scientific figures via open-ended MQM description of clean figures. Top models reach MQM 91.6, and the dissociation extends across the model set: even smaller models perform substantially better on perception than on Inexist resistance. When the same models still fabricate on Inexist probes about the same figures they can describe, visual blindness alone would not be a sufficient explanation, since the models have already demonstrated substantial perceptual capability. This dissociation is more consistent with instruction-tuning pressure to comply with user prompts. We will make this argument explicit in Section 5.

## Comments Suggestions And Typos

**C1.** Please ensure consistency when writing the name of Llama 4.

A: Thank you for catching this. We will standardise the model name as "Llama 4 Maverick" throughout the paper, tables, and appendices.
