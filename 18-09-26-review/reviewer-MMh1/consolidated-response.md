# Consolidated response to Reviewer MMh1 (all 6 weaknesses, ≤300 words / ≤2000 chars)

## Response text (paste-ready)

We thank the reviewer. Point by point.

**Behavioural validation.** We acknowledge the concern. Unlike MQM's multi-item severity checklist, the behavioural labels are binary/ternary categorical (admits/fabricates/correct as y/n; resistance 0/0.5/1). During design, judge outputs were iteratively reviewed by humans and the prompts refined (per-score anchors and structured JSON in Appendix F) to reliably extract these categorical labels. For camera-ready we commit to stratified human validation across all four behavioural probe families, reporting per-label Krippendorff's α and Cohen's κ in Appendix C.

**Prompt cueing.** All models receive identical system-level and user-level prompts across providers. We ran the requested prompt-variant ablation and will add the full comparison (neutral, abstention-supporting, adversarial) to the camera-ready version.

**A-R-I distinctness.** We ran the suggested partial Spearman correlations controlling for MQM baseline. The three A-R-I axes are distinct: Resistance ↔ Inductance partial ρ = −0.04, Admittance ↔ Inductance = +0.19, Admittance ↔ Resistance = 0.61 (the only pair with meaningful shared variance, reasonable since both involve honesty under uncertainty). Full results in camera-ready.

**Inductance metric.** We will report the full outcome distribution (correct inference, incorrect fabrication, admitted uncertainty, omission) alongside a selective-risk curve in the camera-ready.

**Caption-bias.** MQM's baseline completeness axis already penalizes models that produce minimal or incomplete descriptions. The caption-bias experiment is strictly focused on capturing how much models give in to a false premise, so silence would pass; not addressing a claim isn't the same as giving in to it. However, we understand the concern and will add claim coverage as a paired transparency column for camera-ready.

**Scope.** We agree to manage scope appropriately.

**Comments.** All noted and will be addressed appropriately.
