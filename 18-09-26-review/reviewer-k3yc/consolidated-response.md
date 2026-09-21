# Consolidated response to Reviewer k3yc (in progress)

## Response text (paste-ready)

We thank the reviewer. Point by point.

**Behavioural validation.** We acknowledge the concern. Unlike MQM's multi-item severity checklist, the behavioural labels are binary/ternary categorical (admits/fabricates/correct as y/n; resistance 0/0.5/1). During design, judge outputs were iteratively reviewed by humans and the prompts refined (per-score anchors and structured JSON in Appendix F) to reliably extract these categorical labels. For camera-ready we commit to stratified human validation across all four behavioural probe families, reporting per-label Krippendorff's α and Cohen's κ in Appendix C.

**Prompt cueing.** Additional prompt ablations were run on neutral prompts; relative comparisons still hold. The full comparison (neutral, abstention-supporting, adversarial) will be added for camera-ready.

**Inductance metric.** We will report the full outcome distribution (correct inference, incorrect fabrication, admitted uncertainty, omission) alongside an unconditional correctness rate in the camera-ready.

**Caption-bias.** MQM's baseline completeness axis already penalizes models that produce minimal or incomplete descriptions. The caption-bias experiment is strictly focused on capturing how much models give in to a false premise, so silence would pass; not addressing a claim isn't the same as giving in to it. However, we understand the concern and will add claim coverage as a paired transparency column for camera-ready.

**Quality-vs-behaviour claim.** We will soften the framing appropriately.

**Comments.** All noted and will be addressed appropriately.
