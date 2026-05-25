# ACL Meta-Review — Full Paper: SciFig-Eval

**Paper:** SciFig-Eval: Benchmarking Perception, Reasoning, and Behaviour in Vision-Language Models on Scientific Figures

**Meta-Reviewer:** Area Chair, Resources and Evaluation Track

**Area Chair Recommendation:** **4 — Accept (Main Conference)**

---

## Summary of Paper

This paper presents SciFig-Eval, a benchmark for evaluating vision-language models on scientific figure understanding across three dimensions: perception (description quality), reasoning (capability questions), and behaviour (epistemic honesty under uncertainty). The central contribution is the Admittance-Resistance-Inductance (A-R-I) framework, which operationalizes behaviour through selective-blur probes that distinguish fabrication on unrecoverable elements (admittance) from inference on recoverable elements (inductance), paired with probes testing robustness to false premises (resistance). The key finding—that the highest-quality describer (GPT-5.2) also fabricates most frequently when encountering blurred chart elements—reveals a critical perception-behaviour disconnect that quality benchmarks alone would miss.

---

## Reviewer Agreement

**Strengths all three reviewers endorse:**

1. **The perception-behaviour disconnect is a genuine, actionable finding.** Reviewer 1 validates this against statistics; Reviewer 2 calls it "the kind of finding that changes how people think about evaluation"; Reviewer 3 notes it produces memorable formulations ("confident fabricator"). All three agree this passes the "so what?" test for deployment.

2. **The A-R-I framework (especially admittance/inductance) is methodologically sound.** All three acknowledge the selective-blur methodology as novel. Reviewer 1 calls the admittance-inductance distinction "a genuine conceptual contribution"; Reviewer 2 calls it "a real contribution to evaluation design"; Reviewer 3 praises the "clearly operationalized" framework.

3. **Statistical practice is above field average.** Bootstrap CIs, split-half reliability (ρ = 0.979), scale validation, and probe-designer ablation signal methodological care. All three reviewers note these strengths explicitly.

4. **The paper is well-written and clearly structured.** Reviewer 1: "clear structure, precise claims"; Reviewer 2: "clearly presented"; Reviewer 3: gives 4/5 on clarity overall with specific praise for narrative arc and memorable formulations.

**Weaknesses all three reviewers endorse:**

1. **Judge validation is insufficient.** Reviewer 1 flags "rho = 1.0 on 8-model rankings is a low bar" and notes potential conflict-of-interest (GPT-4o judging GPT-5.2). Reviewer 2 calls single-judge reliance a weakness and lists cross-judge validation as a recommendation. Reviewer 3 echoes: perfect agreement on n=8 is not statistically compelling.

2. **Inter-annotator agreement lacks chance correction.** Reviewer 1 explicitly states "94% raw agreement is not sufficient for a benchmark paper" and requires Cohen's kappa or Krippendorff's alpha. This is a standard methodological bar for ACL benchmarks that the paper does not meet.

3. **Sample sizes for admittance/inductance are tight.** Reviewer 1 quantifies: "50 admittance blur candidates and 48 inductance blur candidates yield wide confidence intervals" and notes middle-tier models cannot be distinguished from noise. Reviewer 2 acknowledges this limits generalizability. Reviewer 3 notes the honest limitations section but points out the sample size is small.

4. **Reproducibility details are missing.** Reviewer 1: "API versions, exact prompts, and judge prompts should be in the appendix." No evidence any of these appear in the current draft.

---

## Points of Disagreement

### Disagreement 1: Novelty of Resistance and Transforms

**Reviewer 1 position:** Resistance probes are sound but not groundbreakingly novel. Notes: "hallucination probing (POPE, HallusionBench, CHOCOLATE), robustness testing (CHAOS, CHART NOISe)" already exist. Rates results soundness at 3.5/5 overall.

**Reviewer 2 position:** Resistance is "less novel" but not a major weakness. Admittance is the star; resistance is "useful but incremental." The core contribution (admittance-inductance) is sufficient to carry the paper. Rates excitement at 4/5 for results.

**Reviewer 3 position:** Does not take a strong position on novelty; focuses on clarity (notes transform robustness results are "least novel part" and suggests compression to make room for behavioral findings).

**Meta-reviewer assessment:** Reviewer 2 is correct here. For a benchmark paper, novelty of individual probe types matters less than novelty of the framework and generalizability of findings. The A-R-I decomposition and the admittance-inductance methodology are the paper's core intellectual contribution. Resistance probes, while not individually novel, are well-motivated as part of a three-axis framework. Reviewer 2's recommendation (weak accept, contingent on sharpening positioning vs. CHOCOLATE/CHAOS) is the right bar. The paper should address this via a positioning table comparing A-R-I to prior work, but the core contribution is defensible.

### Disagreement 2: How Serious Is the Dataset Size Concern?

**Reviewer 1 position:** Small sample sizes (50/48) are "borderline" and "limit the precision of model-level comparisons." The directional findings are clear, but some model pairwise comparisons are underpowered. Flags this as a concern requiring author response (Issue 9, Moderate severity).

**Reviewer 2 position:** "250 figures is small by benchmark standards" but "depth over breadth is defensible." The paper is transparent about limitations. Rates this as a weakness but not a dealbreaker (Excitement: 3/5 for dataset section).

**Reviewer 3 position:** Notes limitations section is "commendably honest" about sample sizes; does not flag this as requiring a response in camera-ready.

**Meta-reviewer assessment:** Reviewer 1 is technically correct—with n=50/48, pairwise comparisons like "Llama 4 (22%) vs. Qwen-235B (12%)" lack power. However, this is mitigated by: (1) the paper's transparency about this tradeoff; (2) the directional findings (GPT-5.2 vs. Gemini) are clear and use the full 250-figure set; (3) split-half reliability (0.979) validates stability. For a main-conference accept, this is acceptable, but the authors should (in revision) provide estimated statistical power for key comparisons and note where confidence intervals overlap. This is a refinement, not a rejection criterion.

### Disagreement 3: Should The A-R-I Naming Be Reconsidered?

**Reviewer 2 position:** "The electrical engineering metaphor does not deepen understanding -- it is a naming convention, not a theoretical framework." Suggests "Honesty, robustness, and inference" would communicate the same content without metaphorical baggage. Rates this as a weakness.

**Reviewer 3 position:** The naming is "the paper's most distinctive contribution but also its biggest communication risk." The electrical meanings (admittance = ease of current flow) invert the paper's usage (high admittance is *good*). Recommends acknowledging the analogy is loose or dropping it entirely. Provides detailed technical explanation of the mapping problem. Suggests a one-sentence motivation.

**Reviewer 1 position:** Does not critique the A-R-I naming directly; treats it as a clear contribution.

**Meta-reviewer assessment:** Reviewers 2 and 3 are correct that the naming is a communication liability. The electrical engineering analogy is clever but not essential to the contribution. However, this is a presentation issue, not a methodological flaw. The paper is acceptable as-is because the framework is clearly defined operationally, even if the nomenclature is unmotivated. Recommendation: In camera-ready, add a one-sentence justification for the A-R-I terminology (e.g., "We adopt the circuit terminology as an evocative, memory-friendly acronym; the analogy is suggestive rather than formal"). This is a low-effort fix that addresses both reviewers' concerns.

---

## Key Concerns Requiring Author Response (Ranked)

### Tier 1: Must Address (Soundness-Critical)

1. **Inter-annotator agreement must use chance-corrected metrics.** Reviewer 1 is correct: 94% raw agreement is below the ACL benchmark standard. The authors must compute Cohen's kappa or Krippendorff's alpha for the annotator agreement data and report both the raw agreement and the corrected metric. If kappa < 0.75, the paper's annotation quality is suspect.

   *Why it matters:* For a benchmark paper held to higher methodological rigor, annotation quality is foundational. Raw agreement without chance correction is insufficient to validate dataset quality.

2. **Judge validation must be granular, not just rank correlation.** The claim "perfect agreement, rho = 1.0" on 8 models is unconvincing. The authors must report: (a) how many figures were validated by human judges; (b) per-figure MQM correlation (not just rank-order); (c) discussion of potential bias in GPT-4o judging GPT-5.2 outputs. If the validation is only rank-order on all 8 models, this must be stated clearly with n and caveats.

   *Why it matters:* The entire A-R-I scoring depends on GPT-4o as judge. If the human-judge agreement is weak at the fine-grained level, MQM scores are unreliable.

3. **API versions, prompt templates, and seed reporting for reproducibility.** Reviewer 1 flags: "API dates/versions (model snapshots change), exact prompt templates used for each evaluation condition, or seeds for any stochastic components beyond dataset sampling." These must be in the appendix or supplementary materials.

   *Why it matters:* Closed-model evaluations are opaque by nature. Reproducibility at the level of exact prompts and model snapshots is non-negotiable for a benchmark.

### Tier 2: Should Address (Robustness Enhancement)

4. **Statistical testing inconsistency.** Some comparisons use p-values and effect sizes (GPT-5.2 vs. Gemini); others report raw numbers (middle-tier models). If significance testing is used, apply it consistently. If not, remove it. Multiple-comparisons correction should be applied or discussed.

   *Why it matters:* Methodological consistency matters for a methodology-focused paper. Currently this appears sloppy, even if the findings are sound.

5. **Capability question analysis is shallow.** Table 4 shows GPT-5.2 leads on computation/pattern, Gemini leads overall, but minimal breakdown by chart type, error analysis, or question difficulty is provided. Expand this section or merge it into behavior results to avoid a thin subsection.

   *Why it matters:* Reasoning is one of the three pillars of the framework; it deserves equal depth to perception and behavior.

### Tier 3: Nice-to-Have (Presentation Polish)

6. **Terminology consistency table** (Reviewer 3's recommendation). "Admittance blur" vs. "selective-blur admittance probes," "blur candidates" vs. "blur probes," abbreviations (CapB, Inex, Cont) that are defined in captions but not intuitive. A footnote or appendix glossary would help.

7. **Motivate A-R-I naming** with one sentence explaining why electrical terminology was chosen (Reviewer 3). Acknowledge that the analogy is loose.

---

## Overall Scores

| Dimension | Reviewer 1 (Methodology) | Reviewer 2 (Novelty) | Reviewer 3 (Clarity) | Meta Score |
|-----------|--------------------------|----------------------|----------------------|------------|
| **Soundness** | 3.5/5 | 3.5/5 (implicit) | 4/5 | **3.5/5** |
| **Excitement** | 3.5/5 | 3.5/5 | 4/5 | **3.7/5** |
| **Overall** | 3.5/5 (Borderline Accept) | 3.5/5 (Weak Accept) | 4/5 | **3.7/5** |

**Interpretation:**
- Soundness = 3.5 reflects the concerns about judge validation, IAA, and sample sizes. These are real but not fatal; the core findings are valid despite methodological imprecision.
- Excitement = 3.7 reflects a genuinely novel finding (perception-behaviour disconnect) and a methodological contribution (admittance-inductance framework) that will interest the benchmark community, even if parts are incremental.
- Overall = 3.7 places this at the high end of "solid accept" for main conference. The paper makes concrete contributions, the findings are actionable, and the evaluation is mostly rigorous.

---

## Recommendation

### **4 — Accept (Main Conference)**

**Justification:**

This paper makes two defensible contributions that merit main-conference acceptance:

1. **A methodological innovation (admittance-inductance split)** that others in the VLM evaluation community will adopt. The idea of distinguishing "the model cannot possibly know this" from "the model could infer this from context" is intuitive and well-operationalized through selective blur. This alone justifies publication.

2. **A surprising, deployment-relevant finding** that quality metrics (MQM) do not predict behavioural reliability. The GPT-5.2 vs. Gemini divergence—identical description quality (91.6 vs. 90.2), opposite admittance (6% vs. 90%)—is the kind of result that will shape how VLM evaluation is done going forward.

**Why not higher?**

- Judge validation is weak (rho=1.0 on n=8 is unconvincing). A grant of main-conference accept assumes the authors will strengthen this in revision.
- IAA should use chance-corrected metrics (currently it does not).
- Sample sizes (50/48 figures for admittance/inductance) limit precision, though directional findings are clear.
- Parts of the evaluation (transform robustness, basic resistance probes) retread ground covered by CHAOS and CHOCOLATE. The novelty is in the behavioral dimension and the admittance-inductance distinction, not in perceptual transforms.

**Why not lower?**

- The core contribution is sound. The A-R-I framework is clearly defined and empirically separable (split-half ρ = 0.979 confirms stability).
- Statistical practice is above field average (bootstrap CIs, reliability analysis, ablation).
- The paper is well-written, transparent about limitations, and actionable for practitioners.
- The findings address a gap: prior benchmarks do not distinguish fabrication from inference, nor do they evaluate epistemic honesty under uncertainty.

**Alignment with benchmark criteria:** This is a Resources and Evaluation track paper. The bar for benchmarks is *higher on thoroughness and rigor, lower on novelty of individual components*. This paper clears the bar: the dataset is annotated with care (though IAA needs correction), the evaluation framework is novel, and the findings are generalizable beyond this specific dataset.

---

## Guidance for Camera-Ready

### Must-do revisions:

1. **Report IAA with Cohen's kappa or Krippendorff's alpha.** If k < 0.75, discuss implications. This is non-negotiable for ACL standards.

2. **Expand judge validation section** with per-figure MQM correlation (not just rank-order). Report n of figures validated, describe validation protocol, and discuss potential bias in GPT-4o judging GPT-5.2.

3. **Add reproducibility appendix** with: (a) exact prompt templates for each condition; (b) API snapshot dates and model versions; (c) seeds for all stochastic components; (d) GPT-4o MQM rubric/prompt.

4. **Unify significance testing.** Either apply statistical tests consistently across all model comparisons, or remove them. Apply multiple-comparisons correction if using multiple tests.

### High-impact revisions (recommend):

5. **Add a positioning table** comparing SciFig-Eval to CHOCOLATE, ChartHal, CHAOS, and CHART NOISe on what each benchmark measures. Clarify what SciFig-Eval reveals that they cannot.

6. **Expand Section 4.3 (Reasoning)** with breakdown by chart type, question difficulty, and error analysis. Currently this subsection is thin and undercuts the "three-axis" framework.

7. **One-sentence motivation for A-R-I naming** (e.g., "We adopt this terminology as a memorable acronym; the electrical analogy is evocative rather than formal.").

8. **Add qualitative example box** showing a "confident fabricator" response (GPT-5.2) alongside an honest one (Gemini). Beyond the hook figure, one additional example would help readers assess whether the judge is classifying correctly.

### Nice-to-have polish:

9. Terminology consistency footnote (admittance vs. admittance blur, blur candidates vs. probes, abbreviation glossary).

10. Remove "Orig" ambiguity in Table 3 and unify scales in Table 4 (all percentages or all 0-1).

---

## Summary for Conference Organizers

**Recommendation: ACCEPT**

**Expected impact:** This paper will be cited by VLM evaluation researchers. The perception-behaviour disconnect is a memorable finding, and the selective-blur methodology for distinguishing fabrication from inference will be adopted. Benchmark quality is above average; the three main concerns (IAA metric, judge validation granularity, sample size) are addressable in revision and do not undermine the core contribution.

**Risk assessment:** Low. The authors are responsive (as evidenced by honest limitations section). The findings are sound despite methodological imprecision. The paper fits the Resources and Evaluation track perfectly.

**Session fit:** Suitable for the benchmark track or a dedicated VLM evaluation session. Strong candidate for an oral if the conference prioritizes practitioner-relevant findings.

