# Consolidated response to Reviewer yQSV (in progress)

## Response text (paste-ready)

We thank the reviewer.

**Novelty vs. closest competitors.** A-R-I's novelty lies in how it organizes behavioural evaluation along a 2D space of evidence conditions, presence (is the queried element in the figure?) and recoverability (is it inferable from context?), both critical in practical deployment. This yields three regimes: Resistance for absent evidence, Admittance for present but unrecoverable evidence, and Inductance for present and recoverable evidence, as stated in §3.3. Additionally Inductance, is to our knowledge novel as an evaluation axis. We agree that adding ChartHal and CHART-NOISe (which we discuss in Related Work) to Table 1 will strengthen the comparison, and we will do so in the camera-ready.

**Admittance definition.** We understand the concern. However, this is an intentional design. Admittance in our framework is deliberately defined as the model's acknowledgment of uncertainty, not the suppression of an answer. Models typically have a "must respond" bias, hence practically what matters is that a model admits it is uncertain, even if it goes ahead to infer some response. Requiring admit-without-further-inference would conflate two axes. We will provide the stricter pure-admittance breakdown as supplementary detail in the camera-ready.

**Hallucinated content agreement.** We audited the 30 human-flagged pairs. All 30 receive some judge penalty; none missed entirely. The 28 not flagged under "Hallucinated Content" are penalised under adjacent sub-types (e.g., Missing Visual Features, Incorrect Visual Attribute Mapping). Mean judge penalty is 32.2 vs 25.5 (human), so the divergence is a labelling difference, not a severity gap. Full breakdown to be added to Appendix C.1.

**Dataset scale.** We believe that at 34,000 evaluations and 600+ annotation hours, our methodology is robust and in-depth. We agree that expanding dataset will strengthen the analysis, and note this as future work.

**Comments.** All noted and will be addressed appropriately.
