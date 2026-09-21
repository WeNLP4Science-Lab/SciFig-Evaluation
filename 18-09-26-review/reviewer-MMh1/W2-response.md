# Draft response to Reviewer MMh1 — W2 (prompts may induce the measured behaviour)

## Response text (paste-ready, ~140 words)

> We agree that a prompt-variant ablation would strengthen the analysis and will
> add one for the camera-ready. Two existing patterns, however, already indicate
> resistance scores are not reducible to instruction compliance.
>
> R2 instructs models to flag content not present in the figure, applying equally
> to inexist and unanswerable probes. Under a compliance account, both should score
> similarly. Instead, every one of the eight models scores higher on unanswerable
> (range 0.56 to 0.95) than on inexist (range 0.04 to 0.88), with per-model gaps
> as large as 0.76 for Gemma 3 27B (0.93 vs. 0.17; §5, presupposition embedding).
>
> Separately, the baseline description prompt (D1–D4) contains no instruction to
> flag misleading content or acknowledge uncertainty. Under this neutral prompt,
> passive admittance on selectively blurred figures spans 2% to 77% across models,
> and caption-bias resistance spans 0.05 to 0.89. Both target behaviours emerge
> without any prompt cueing.
>
> Prompts are identical across providers.

---

## Notes

- Standard review-response opening ("We agree that... and will add...")
- Pivot with "however" is the professional way to concede then present counter-evidence
- Two arguments, tightly written. Inexist paradox uses reviewer's own probe
  categories. Neutral-prompt evidence uses passive admittance (fully clean input)
  and caption-bias (adversarial input only in the caption) together, closing both
  the "prompt cues it" and "input cues it" pushbacks
- No em-dashes, no colons in the body

## Fallback if pushed further

If MMh1 says cross-model spread only argues for relative rankings, shift to k3yc's
framing. Absolute resistance numbers should be interpreted with the caveat that
prompts license the target behaviour. The paper's central claims rest on relative
comparisons across models, which are robust to probe design (Table 12), alternative
judges (Table 10), and (committed) prompt formulation.
