# Consolidated response to Reviewer YLTQ (in progress)

## Response text (paste-ready)

We thank the reviewer. Point by point.

**Previous-round follow-through.** (a) The mapping from probe families to deployment failure modes was intended as motivational context rather than an empirical frequency claim; comprehensive frequency data would require large-scale industry surveys beyond the scope of a benchmark paper. (b) The controlled experiment the reviewer suggests was run as a prompt-variant ablation on resistance probes; the full comparison (neutral, abstention-supporting, adversarial) will be reported in the camera-ready. (c) While we are confident our methodology is robust, we acknowledge the dataset-scale concern. Extending to further charts and chart types would be suitable future work, as covered in our Limitations section.

**Dataset scope.** We agree the source venues (NLP/ML/CL arXiv) are narrow. However, our analysis methodology applies to bar/line/pie charts across any domain and would likely surface the same behavioural patterns regardless. We further acknowledge that the word "scientific" in the title should reflect our sampling scope, and we will frame this appropriately. Expanding chart-type coverage is discussed as future work in our Limitations section.

**Judge dual role and item-level noise.** The dual-role concern is mitigated by three existing checks: probe-designer ablation (Table 12), cross-judge ablation on capability (Table 10), and human-in-the-loop review of probe candidates (§3.1). Item-level MQM quality is analysed in Appendix C.1 (r=0.68, ρ=0.58, systematic −15 bias) and known LLM-judge failure modes are explicitly documented there (Table 9 "Divergent" panel). The systematic bias preserves aggregate rankings. Per-item quality for the behavioural labels will be added in the camera-ready human validation.

**Dataset and code availability.** We will provide the full dataset and source code with the camera-ready.

**Comments.** All noted and will be addressed appropriately.
