# ACL Meta-Review: Wave 1
## Reviewer Synthesis and Recommendation

---

## Summary of Paper

SciFig-Eval is a benchmark for evaluating vision-language models on scientific figure understanding, comprising 250 figures (bar charts, line plots, pie charts) annotated with structured quality metrics and targeted behavioral probes. The paper adapts the MQM framework from translation evaluation to chart descriptions and introduces the A-R-I framework (Admittance-Resistance-Inductance), which decomposes VLM behavioral reliability into three orthogonal dimensions. The core contribution is demonstrating that model rankings under standard quality evaluation diverge substantially from rankings under adversarial behavioral conditions, showing that quality and reliability are independent dimensions of competence.

---

## Reviewer Agreement

All three reviewers agree on the following strengths and weaknesses:

**Clear Agreement — Strengths:**
1. **The A-R-I framework is a genuine conceptual contribution.** All reviewers identify the three-way decomposition (Admittance, Resistance, Inductance) as novel and well-grounded in cognitive science. Reviewer 2 calls it "a real intellectual contribution," and Reviewer 3 acknowledges it as "the backbone" of the paper. This is the paper's clearest strength.
2. **The cognitive science grounding is compelling.** The mapping of VLM failure modes to named cognitive biases (presupposition embedding, anchoring, cooperative principle, sycophancy) is noted as genuinely novel by Reviewer 2. Reviewers 1 and 3 note that this is the most interesting aspect of the positioning.
3. **The 2×2 matrix is an effective organizing device.** All three reviewers praise the matrix (Table 2) as clear and immediately graspable.
4. **Strong methodology in specific subsections.** The A/B randomization for caption bias judging (Reviewers 1, 3), the inductance validation methodology (Reviewer 2), and the binding verification extension to MQM (all reviewers) are noted as careful, principled work.

**Clear Agreement — Weaknesses:**
1. **The dataset section is underdeveloped.** All three reviewers flag missing critical information: sampling methodology (which arXiv fields, date range, extraction method), inter-annotator agreement, annotator qualifications, and domain distribution. Reviewer 1 rates this section 3/5 on soundness; Reviewer 3 rates it 3/5 on clarity; Reviewer 2 rates it 2/5 on excitement. The shortfall is consistent across all dimensions.
2. **The rho = 1.0 claim demands scrutiny.** All three reviewers flag the perfect Spearman correlation between automated MQM and human rankings as potentially suspicious or at minimum underspecified. Reviewers 1 and 3 request sample sizes and p-values; Reviewer 2 expresses skepticism. This is the most pressing methodological concern across all sections.
3. **The dataset is small and scale concerns are inadequately addressed.** Reviewer 2 explicitly rates the dataset as thin (250 figures, 100 primary); Reviewer 3 notes that "scale concern is unaddressed"; Reviewer 1 acknowledges that 50 figures for ablation may be underpowered for per-chart-type analysis. None of the reviewers are fully convinced the scale is sufficient for the scope of claims.
4. **A-R-I terminology appears before framework is introduced.** Reviewer 3 flags a critical ordering problem: the dataset section uses terms like "admittance blur" and "inductance blur" before the A-R-I framework is defined. Reviewers 1 and 3 both recommend either moving the dataset section after the framework or adding forward references.

---

## Points of Disagreement

**1. The novelty and significance of the benchmark itself (cognitive science grounding)**

**Position A (Reviewer 2 — Novelty-focused):** The cognitive science mapping is the most innovative contribution and elevates the paper from "harder questions" to "principled probe design." This deserves more prominence in the related work section, which currently compresses the four cognitive biases into one sentence. The grounding warrants expansion.

**Position B (Reviewer 1 — Methodology-focused):** While the cognitive science grounding is interesting, the related work oversells it slightly. The paper should acknowledge that it maps VLM failure modes to cognitive biases, but the connection between probe type and bias should be more explicit in the paper itself. The framework section mentions presupposition → inexist, anchoring → contra, etc., but the related work does not make this mapping fully transparent.

**Meta-Reviewer Assessment:** Reviewer 2 is correct that the cognitive science contribution is undercommunicated in the related work. The related work should expand the single 47-word sentence (lines 23-24) into 2-3 sentences that name each bias, cite it, and briefly explain why it maps to a specific VLM failure mode. This is not just a novelty point but a clarity issue — Reviewer 3 flags the same sentence as "too dense" and recommends restructuring. **Action: Authors should expand the cognitive science paragraph in related work to clarify the mapping between biases and probes.** This addresses both reviewers' concerns without requiring fundamental changes to the contribution.

---

**2. Whether dataset size is adequate and how to communicate this**

**Position A (Reviewer 2 — Pragmatic defense):** 250 figures is thin *as a corpus*, but the benchmark's real contribution is not size but *annotation depth and adversarial stimulus design*. The authors should lead with this framing: "Rather than seeking scale, we seek depth. Each of 100 primary figures receives X evaluation instances across Y conditions." The concern is not that 250 is too small *in principle*, but that the paper does not pre-empt the reviewer instinct to ask "is this enough?"

**Position B (Reviewer 1 — Methodological skepticism):** 50 figures for the ablation subset, split across three chart types, yields only ~10-15 pie charts per model. With 8 models, that is 80-120 data points per chart type — "possibly sufficient for rank correlation but tight for any per-type analysis." The sample sizes behind key empirical claims (especially the 21-81% vs. 0-14% inductance validation) are not reported. The paper should acknowledge limitations and report actual per-cell counts.

**Meta-Reviewer Assessment:** Both positions are valid and complementary. Reviewer 2 is right that the benchmark's value is depth, not scale, and this should be stated explicitly. Reviewer 1 is right that sample sizes for ablation analyses are not reported and should be. **Action: Authors should (a) add one paragraph to the dataset section justifying the design choice (annotation depth over scale) and citing comparison to prior benchmarks by size, and (b) report actual sample sizes for the inductance validation numbers (21-81% vs. 0-14%) and the 6% vs. 90% admittance divergence.** These are not contradictory fixes; they address different aspects of the same concern.

---

**3. Whether specific empirical findings belong in the framework section or should be deferred to results**

**Position A (Reviewer 1 — Methodological clarity):** The headline findings (6% admittance for best MQM model vs. 90% for second, 21-81% vs. 0-14% inductance correctness) appear in the framework section (lines 74, 76) but belong in results. The framework should state what *will be measured*, not what *was found*. Mixing methodology and findings blurs the line.

**Position B (Reviewer 2 — Pedagogical support):** The inductance validation numbers (21-81% vs. 0-14%) are actually empirical *validation* of the framework itself—they show that the inductance dimension captures real reasoning, not noise. This is methodological evidence that the framework is sound and belongs in the framework section.

**Position C (Reviewer 3 — Compromise):** The numbers are compelling but premature here. Use forward references ("as we show in §results") or move the specific numbers to the results section while keeping the conceptual claim in the framework.

**Meta-Reviewer Assessment:** Reviewer 2's point that inductance validation is about proving the framework works is subtle and partially correct, but Reviewers 1 and 3 are right that mixing empirical findings into a methodology section makes the paper harder to follow. **Action: Authors should move the specific numerical results (6% vs. 90%, 21-81% vs. 0-14%) to the results section, or mark them clearly as forward-looking ("as we later show..."). Keep the conceptual definitions (what inductance measures) in the framework, but defer the empirical validation.** This preserves the framework's logical structure and makes the results section stronger.

---

**4. Chart-type-specific comparability of MQM scores**

**Position A (Reviewer 1 — Technical concern):** The MQM formula divides by D, which is the severity-adjusted maximum. Since D varies by chart type (14/15/11 checklist items), MQM scores are not directly comparable across chart types without acknowledging different denominators. The paper does not discuss cross-type comparison.

**Position B (Reviewer 3 — Not flagged as critical):** Reviewer 3 notes the different checklist sizes but does not flag it as a core issue, suggesting it may be an acceptable design choice if acknowledged.

**Meta-Reviewer Assessment:** Reviewer 1 raises a valid technical point, but it is not a fatal flaw if the paper acknowledges it. **Action: Authors should add one sentence to the MQM section clarifying whether cross-chart-type MQM comparison is intended and, if so, how the different denominators are handled. If not intended (e.g., results only compare models within chart type), state this explicitly.** This is a minor clarification but matters for reproducibility.

---

## Key Concerns Requiring Author Response

Ranked by impact and specificity:

**1. CRITICAL: The rho = 1.0 MQM-human correlation must be scrutinized and properly reported.** (Flagged by Reviewers 1, 2, 3)
   - **Why it matters:** Perfect correlation is a strong validation claim but raises questions about overfitting the rubric to match a single annotator.
   - **Required action:** Report the sample size (number of models ranked, number of human annotators). If based on 8 models and 1 annotator, state this and consider adding a second annotator to validate. Include the p-value or 95% CI.
   - **Affected text:** Framework section, line 37.

**2. HIGH: Add critical dataset construction details to main paper.** (Flagged by Reviewers 1, 2, 3)
   - **Why it matters:** A benchmark paper lives or dies on data quality. Reviewers cannot assess rigor without knowing how figures were sampled, who annotated them, and what agreement was achieved.
   - **Required actions:**
     - Add 1-2 sentences on arXiv sampling: Which fields/years? How many unique papers? Automatic or manual figure extraction?
     - Report inter-annotator agreement (IAA) for structured annotations, or justify single-annotator approach (e.g., "checklist items are verifiable facts, not subjective judgments").
     - Name the annotator(s) and their qualifications briefly.
   - **Affected text:** Dataset section (lines 5-6).
   - **Note:** This may be in the appendix, but the main text should summarize the essentials.

**3. HIGH: Resolve dataset terminology ordering issue.** (Flagged by Reviewer 3)
   - **Why it matters:** The dataset section uses A-R-I framework terminology before the framework is explained, creating forward-reference confusion.
   - **Required actions:** Either (a) move the dataset section after the framework section, or (b) add one clarifying sentence at first mention of "admittance blur"/"inductance blur" (line 11): "These categories correspond to the behavioral framework dimensions introduced in §3.5."
   - **Affected text:** Dataset section, line 11.

**4. MEDIUM: Expand cognitive science paragraph in related work.** (Flagged by Reviewers 2, 3)
   - **Why it matters:** The current sentence (line 23) is 47 words and lists four biases in rapid succession. This is the most novel aspect of the positioning and deserves clarity.
   - **Required action:** Expand to 2-3 sentences, giving each bias a dedicated mention and briefly explaining why it maps to a VLM failure mode. Example: "Presupposition embedding, where definite articles presuppose existence, maps to models hallucinating chart elements they encounter in questions. Anchoring bias, where initial numbers bias judgment, explains models' susceptibility to false numerical context..."
   - **Affected text:** Related work, line 23.

**5. MEDIUM: Report sample sizes for empirical validation claims.** (Flagged by Reviewers 1, 2)
   - **Why it matters:** The 21-81% vs. 0-14% inductance validation and the 6% vs. 90% admittance divergence are striking claims, but their statistical power is unclear.
   - **Required actions:** Report the number of figures, models, and total evaluation instances behind these numbers. For the inductance validation, report the counts of inferable vs. non-inferable blur candidates per chart type.
   - **Affected text:** Framework section, lines 74 and 76; or move to results section with sample sizes in caption.

---

## Overall Scores

| Dimension | R1 (Methodology) | R2 (Novelty) | R3 (Clarity) | Meta Score |
|-----------|---|---|---|---|
| Soundness | 3.5/5 | 3.5/5 | 3.7/5 | **3.5/5** |
| Excitement | 3.5/5 | 3.5/5 | 3.7/5 | **3.6/5** |
| Overall | 3.5/5 | 3.5/5 | 3.7/5 | **3.6/5** |

**Interpretation:**
- **Soundness (3.5/5):** The framework and A-R-I methodology are sound and well-grounded. The dataset methodology has critical gaps (sampling, IAA, annotation details). The rho=1.0 claim is not established soundly. With revisions to address items 1-2 above, soundness could reach 4/5.
- **Excitement (3.6/5):** The A-R-I framework is genuinely novel and the quality-reliability divergence finding (if properly validated) is significant. The cognitive science grounding is the most interesting conceptual move. The scale and positioning concerns limit excitement; with clarification these can be overcome.
- **Overall (3.6/5):** A paper with real contributions that has been submitted with insufficient rigor on methodological details and presentation clarity. Not in reject territory, but not yet in accept territory either.

---

## Recommendation

**3 — Accept (Findings Track)**

This paper presents a solid benchmark contribution with a novel A-R-I framework and interesting adversarial probe design grounded in cognitive science. However, critical methodological details are missing from the dataset section (sampling strategy, inter-annotator agreement, annotator qualifications), and the rho=1.0 validation claim requires careful scrutiny and reporting of sample sizes. The paper would benefit from restructuring to address forward-reference problems (A-R-I terminology in dataset before framework) and expanding the cognitive science contribution in the related work section.

The work is **not ready for main conference acceptance** in its current form because:
1. Dataset construction methodology is insufficiently documented for a benchmark paper, where data quality is paramount.
2. The rho=1.0 claim is underspecified and potentially overstated.
3. The scale concern (250 figures, 100 primary, 50 ablation) is acknowledged but not adequately justified.

The work is **suitable for Findings Track** because:
1. The A-R-I framework is a real conceptual contribution that could influence how the community evaluates VLM reliability beyond chart understanding.
2. The empirical finding that quality and reliability rankings diverge is significant and would interest the evaluation community.
3. The dataset, while modest in scale, represents a careful application of MQM to a new domain with principled behavioral probes.
4. Revisions to address the concerns above are achievable and would strengthen the paper significantly.

---

## Justification

The paper's core contribution — decomposing VLM behavioral reliability into three measurable, orthogonal dimensions grounded in cognitive science — is novel and well-executed in the framework section. Reviewer 2 correctly identifies that "the A-R-I framework has adoption potential" and provides "clear, measurable dimensions with intuitive names." The inductance validation (21-81% vs. 0-14% correctness on inferable vs. non-inferable elements) is a clever internal consistency check that suggests the framework measures something real.

However, the benchmark's credibility rests on the quality of its dataset, and here the paper falls short. The dataset section omits information that is standard in benchmark papers: How were figures sampled from arXiv? What are the annotation procedures? What is inter-annotator agreement? Reviewer 1 correctly notes that "a benchmark paper lives or dies on its dataset construction methodology, and key details are absent." The paper mentions that annotations were "verified against the original PDF context" but does not explain by whom, using what process, or with what error rate. For Reviewer 1, this is a soundness issue (3/5 rating); for Reviewer 2, it is an excitement issue (2/5 rating); for Reviewer 3, it is a clarity issue (3/5 rating). The consensus is that the section is underdeveloped.

The rho=1.0 claim is the second major concern. All three reviewers flag this as suspicious or underspecified. If the correlation is based on 8 models ranked by a single annotator, rho=1.0 is possible but not necessarily impressive (there are only 8 data points; the probability of perfect agreement by chance is non-trivial). If it is based on a larger corpus, the sample size should be stated. The paper provides no p-value, confidence interval, or even an explicit statement of sample size. For Reviewer 1, this is "the most critical methodological concern"; for Reviewer 2, it "almost too perfect"; for Reviewer 3, it requires "qualification." This must be fixed.

Third, the paper creates an ordering problem by using A-R-I terminology in the dataset section before the framework is introduced. Reviewer 3 explicitly flags this as a "critical ordering problem" and Reviewer 1 notes that clarity is lost. This is a straightforward fix.

These are not fatal flaws. The paper's contributions are real and the methodology in the framework section is strong. But the work needs significant revision — not in terms of new experiments or data collection, but in terms of documenting what was done, justifying design choices, and reordering sections for clarity. For a main conference, the bar for data quality documentation is very high; this paper does not clear it in its current form. For Findings Track, these issues are acceptable provided the authors commit to addressing them in the camera-ready version.

---

## Guidance for Authors

**If accepting (Findings Track), top 3 impactful changes:**

1. **Add 3-4 sentences to the dataset section describing sampling and annotation procedures.** This is your highest ROI revision. Include:
   - arXiv sampling strategy: fields, date range, ~how many papers sampled to extract 250 figures, automatic or manual extraction
   - Annotator details: who annotated, their qualifications/expertise, how many annotators
   - Inter-annotator agreement: report the statistic (Krippendorff's α, Cohen's κ, or percentage agreement), or justify single-annotator approach
   - Domain distribution: approximate field breakdown (CS, physics, biology, etc.)

2. **Report full details for the rho=1.0 correlation claim.** State:
   - Number of models ranked (8?)
   - Number of human annotators (1? 2?)
   - Number of figures used in the human evaluation (all 100 primary, or a sample?)
   - p-value or 95% confidence interval
   - If based on single annotator, consider adding a second

3. **Expand the cognitive science paragraph in related work (line 23).** Break the 47-word sentence into 2-3 shorter sentences, each naming a cognitive bias and explaining why it maps to a VLM failure mode. This clarifies your most novel conceptual contribution.

**Additional improvements (if time permits):**
- Move specific empirical results (6% vs. 90%, 21-81% vs. 0-14%) to the results section or mark as forward-looking.
- Add one clarifying sentence at first mention of "admittance blur"/"inductance blur" in dataset section, pointing forward to §3.5.
- Clarify cross-chart-type MQM comparability given different checklist sizes.
- Add sample sizes (number of blur candidates, models, figures) for the inductance validation numbers.

These revisions will address all three reviewers' main concerns and significantly strengthen the paper for publication.

