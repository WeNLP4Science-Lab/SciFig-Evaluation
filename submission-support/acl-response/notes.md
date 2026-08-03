# ACL Response Notes

Reference numbers and drafts for the rebuttal. Keep this updated as we lock things in.

## Human annotation effort

Numbers confirmed with the team for the rebuttal paragraph on human annotation.

| Task | Annotators | Hours | Source |
|---|---|---|---|
| **Perception** (250 figure descriptions) | 3 | ~240 | Team recall (Wei) |
| **Reasoning** (1,000 GPT-generated questions, post-edited) | 4 | ~200 (~50 hrs/person × 4) | Team recall (Paul) |
| **Selective-blur** (443 OCR-generated targets, post-edited) | 3 | ~100 | Team recall (Paul) |
| **MQM evaluation** (120 pairs = 4 LLMs × 30 figures) | 3 | ~30 (estimated) | Paper `appendix_human_validation.tex` |

### Totals
- **Unique annotators across all tasks:** ~5 (assuming team overlap; team has 8 total)
- **Total hours:** ~570 → conservative "over 500 hours"

### MQM evaluation details (from paper)
- 3 annotators with graduate-level NLP expertise
- 4 LLMs: GPT-5.2, Qwen3-VL-30B, Qwen3-VL-8B, Gemma3-27B
- 30 figures × 4 models = 120 (figure, model) pairs
- 39 pairs double-annotated
- Krippendorff's α=0.91 (interval scale), ICC(2,1)=0.91, Pearson r=0.92, Spearman ρ=0.87

## Draft paragraph for rebuttal (professor's structure, numbers filled in)

> First, a high-quality human annotation campaign (involving 5 annotators for a total of over 500 hours) was carried out across the perception, reasoning, and behavioural probes. This includes 250 high-quality figure descriptions annotated by 3 student annotators over ~240 hours, including an overlapping subset for computing inter-annotator agreement. Additionally, 1,000 GPT-generated reasoning questions were post-edited by 4 annotators over ~200 hours to ensure correctness, and 443 OCR-generated selective-blur targets were post-edited by 3 annotators over ~100 hours. Furthermore, we provided a high-quality human evaluation of 4 LLMs on 30 figures using the MQM scheme, involving 3 annotators.

## Open questions

- Confirm total unique annotator count (currently estimated at 5). Could be 4–7 depending on overlap.
- Confirm "over 500 hours" wording vs "approximately 570 hours" — precision preference.
- Which reviewer response(s) does this paragraph go into?
  - Reviewer h9tb W1 (chart-type coverage)
  - Reviewer lhrb W1 (scale + diverse sources)
  - Reviewer no6d W3 (250 figures + 3 chart types)
  - Or all three?

## Item-level GPT-4o vs human agreement (pending)

- Reviewer No6d W4 asked for GPT-4o vs human item-level agreement on behavioural probes.
- **Existing data does NOT cover this** — no prior human judgment of model responses to behavioural probes exists in our records.
- To run: 48-item stratified sample × 3 annotators (blind annotation), ~2 hours per annotator = ~6 team-hours total.
- GPT-4o judge scores are already stored per item (`judge_score` + `judge_reasoning` in `results/evaluation/resistance/*/*.json` etc.).
- Currently: locked in as "will run in updated version" fallback pending team availability.

## Other verified paper numbers (for reference)

- **8 evaluated models** (proprietary + open-weight):
  - Gemini 3.1 Pro
  - GPT-5.2
  - Llama 4 Maverick
  - Qwen3-VL-235B (open-weight, largest at 235B)
  - Qwen3-VL-30B
  - Qwen3-VL-8B
  - Gemma3-27B
  - Phi-4-multimodal
- **250 English figures from 187 arXiv papers** (2023–2025), stratified sampling to preserve chart-type distribution
- **34,000+ evaluation setups** total
- **Split-half reliability ρ=0.979** across 100 random splits
- **Resistance scores converge by 100 figures** with maximum deviation 0.02 from full set
- **Judge dependence check:** Mistral Large 3 re-judged 344 capability items → 87.2% item-level agreement, identical model rankings

## Probe breakdown

| Probe family | Count | Purpose |
|---|---|---|
| Transformed + page-context cases | 1,243 | Perception under degradation |
| Reasoning (capability) questions | 1,000 | Figure-grounded reasoning |
| Resistance probes | 750 | Reject false-premise (inexist, contra, unanswerable) |
| Caption-bias probes | 100 | Reject misleading captions |
| Selective-blur targets | 443 | Admittance (unrecoverable) + Inductance (recoverable) |
