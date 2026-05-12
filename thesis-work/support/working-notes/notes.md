1. Models cheat — "See or Recall" (2025) showed models can answer chart questions without even seeing the chart. They're
  pattern-matching from training data, not actually reading figures.
  2. Models can't detect misleading charts — CALVI found ALL models max out at 30% accuracy on detecting truncated axes, inverted
  scales, etc. Humans get 80%+.
  3. Description is easy, reasoning is hard — GPT-4o scores 80% on "what does this chart show?" but drops to 47% on "what does this
   data mean?" (CharXiv). The gap is the real test.
  4. Numerical precision is terrible — Models can't reliably read exact values from charts. They approximate, round, and fabricate
  plausible numbers.
  5. Log scales break models — They consistently read logarithmic axes as linear, getting orders of magnitude wrong.
  6. Captions bias models — When given a misleading caption with a figure, models tend to describe what the caption says rather
  than what the image actually shows.
  7. Multi-panel reasoning is near zero — Models can describe individual panels but can't cross-reference between them (e.g., "does
   panel A support the trend in panel B?").
  8. More detail = more hallucination — As you push models for longer descriptions, they start inventing plausible but wrong
  information to fill space.



    1. Visual reasoning vs text reasoning — all models drop 35-55% when they must extract
   info visually vs from text/tables (ChartMuseum). This is the core problem.
  2. Hallucination when info is absent — GPT-5 scores only 34.5% when asked about
  information that's NOT in the chart (ChartHal). Models fabricate plausible answers.
  3. Numerical value fabrication — models produce incorrect but plausible numbers. The
  FUGU paper shows the vision encoder captures the right info but the handoff to the
  language model loses it — an architectural limitation.
  4. Misleading charts — even the best model maxes at 30% on detecting truncated axes,
  inverted scales, etc. Models can't critically evaluate what they see.
  5. Prompt reverse inconsistency — models contradict themselves when asked to confirm
  vs deny the same statement about a chart (CHARTNOISE). Their understanding isn't
  stable.



  APRIL 15

  Hallucination probing guide in paper writing



  