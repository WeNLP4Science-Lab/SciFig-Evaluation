// Single source of truth for landing-page numbers.
// All values mirror the ACL submission (paper/sections/results.tex + tables/).

export interface ModelMeta {
  id: string
  name: string
  short: string
  color: string         // brand hue, mirrors dashboard tab styling
  family: 'commercial' | 'open'
  archetype?: string    // one-line characterisation (used in tooltips)
}

export const MODELS: ModelMeta[] = [
  { id: 'gemini',    name: 'Gemini 3.1 Pro',     short: 'Gemini',    color: '#22c55e', family: 'commercial', archetype: 'Cautious leader' },
  { id: 'gpt',       name: 'GPT-5.2',            short: 'GPT-5.2',   color: '#3b82f6', family: 'commercial', archetype: 'Confident fabricator' },
  { id: 'llama',     name: 'Llama 4 Maverick',   short: 'Llama 4',   color: '#a1a1aa', family: 'open',       archetype: 'Mid-tier all-rounder' },
  { id: 'qwen235',   name: 'Qwen3-VL-235B',      short: 'Qwen-235B', color: '#a1a1aa', family: 'open' },
  { id: 'qwen8',     name: 'Qwen3-VL-8B',        short: 'Qwen-8B',   color: '#a1a1aa', family: 'open' },
  { id: 'qwen30',    name: 'Qwen3-VL-30B-A3B',   short: 'Qwen-30B',  color: '#a1a1aa', family: 'open' },
  { id: 'gemma',     name: 'Gemma-3-27B-IT',     short: 'Gemma',     color: '#a1a1aa', family: 'open' },
  { id: 'phi',       name: 'Phi-4 Multimodal',   short: 'Phi-4',     color: '#ef4444', family: 'open',       archetype: 'Floor / sanity check' },
]

// Baseline MQM (Table 3, Base column) — perception quality on 250 figs
export const MQM: Record<string, number> = {
  gemini: 90.2,
  gpt:    91.6,
  llama:  81.4,
  qwen235: 80.8,
  qwen8:  78.9,
  qwen30: 74.4,
  gemma:  69.1,
  phi:    62.2,
}

// Capability accuracy by category (Table 4 — Capability columns)
export interface CapabilityRow {
  counting: number
  computation: number
  comparison: number
  pattern_analysis: number
}

export const CAPABILITY: Record<string, CapabilityRow> = {
  gemini:  { counting: 89.2, computation: 79.4, comparison: 89.6, pattern_analysis: 70.0 },
  gpt:     { counting: 76.1, computation: 82.8, comparison: 77.9, pattern_analysis: 72.0 },
  llama:   { counting: 45.6, computation: 53.4, comparison: 37.2, pattern_analysis: 48.0 },
  qwen235: { counting: 65.2, computation: 63.7, comparison: 50.0, pattern_analysis: 52.0 },
  qwen8:   { counting: 47.8, computation: 52.8, comparison: 45.4, pattern_analysis: 50.0 },
  qwen30:  { counting: 43.5, computation: 45.9, comparison: 31.4, pattern_analysis: 30.0 },
  gemma:   { counting: 15.2, computation: 29.4, comparison: 18.6, pattern_analysis: 40.0 },
  phi:     { counting: 13.0, computation:  6.2, comparison:  3.5, pattern_analysis: 16.0 },
}

// Active / passive admittance (Table 4) — % of probes where model acknowledged uncertainty
export const ADMITTANCE: Record<string, { active: number; passive: number }> = {
  gemini:  { active: 71, passive: 59 },
  gpt:     { active: 8,  passive: 23 },
  llama:   { active: 19, passive: 5  },
  qwen235: { active: 15, passive: 13 },
  qwen8:   { active: 7,  passive: 3  },
  qwen30:  { active: 7,  passive: 0  },
  gemma:   { active: 8,  passive: 2  },
  phi:     { active: 5,  passive: 2  },
}

// Active / passive inductance — % of fabricated answers that were correct on inferable elements
export const INDUCTANCE: Record<string, { active: number; passive: number }> = {
  gemini:  { active: 66, passive: 73 },
  gpt:     { active: 59, passive: 77 },
  llama:   { active: 34, passive: 58 },
  qwen235: { active: 29, passive: 58 },
  qwen8:   { active: 22, passive: 52 },
  qwen30:  { active: 24, passive: 58 },
  gemma:   { active: 14, passive: 41 },
  phi:     { active: 15, passive: 35 },
}

// Resistance (Table 4) — 0–1 scale, per probe type + caption-bias
export interface ResistanceRow {
  inexist: number
  contra: number
  unanswerable: number
  caption_bias: number
}

export const RESISTANCE: Record<string, ResistanceRow> = {
  gemini:  { inexist: 0.88, contra: 0.91, unanswerable: 0.95, caption_bias: 0.89 },
  gpt:     { inexist: 0.77, contra: 0.75, unanswerable: 0.92, caption_bias: 0.89 },
  llama:   { inexist: 0.63, contra: 0.76, unanswerable: 0.94, caption_bias: 0.74 },
  qwen235: { inexist: 0.67, contra: 0.64, unanswerable: 0.94, caption_bias: 0.54 },
  qwen8:   { inexist: 0.40, contra: 0.44, unanswerable: 0.88, caption_bias: 0.43 },
  qwen30:  { inexist: 0.23, contra: 0.37, unanswerable: 0.73, caption_bias: 0.30 },
  gemma:   { inexist: 0.17, contra: 0.24, unanswerable: 0.93, caption_bias: 0.38 },
  phi:     { inexist: 0.04, contra: 0.04, unanswerable: 0.56, caption_bias: 0.05 },
}

// Mean of inexist/contra/unanswerable — overall resistance score
export function overallResistance(id: string): number {
  const r = RESISTANCE[id]
  return (r.inexist + r.contra + r.unanswerable) / 3
}

// Cross-dimensional Spearman rank correlations (Table A9)
// Symmetric, diagonal = 1.0. Order: MQM, Resistance, CapBias, Admittance, Inductance.
export const CROSS_DIM_LABELS = ['MQM', 'Resistance', 'Caption-Bias', 'Admittance', 'Inductance']
export const CROSS_DIM: number[][] = [
  [1.00, 0.95, 0.95, 0.83, 0.95],
  [0.95, 1.00, 1.00, 0.86, 0.93],
  [0.95, 1.00, 1.00, 0.86, 0.93],
  [0.83, 0.86, 0.86, 1.00, 0.88],
  [0.95, 0.93, 0.93, 0.88, 1.00],
]

// Headline benchmark stats
export const BENCHMARK_STATS = {
  figures: 250,
  papers: 123,
  capability_questions: 1000,
  resistance_probes: 750,
  admittance_targets: 228,
  inductance_targets: 215,
  caption_bias_figs: 100,
  models: 8,
  total_evaluations: 34000,
  languages: 1,  // English only in current submission
  chart_types: 3,
}

// Method credibility numbers
export const METHOD_CREDIBILITY = {
  krippendorff_alpha: 0.91,
  split_half_rho: 0.979,
  cross_judge_rho: 1.000,
  scale_validation_max_deviation: 0.02,
  human_validation_pairs: 200,
}

// Headline contrast — the "money number"
export const HEADLINE_CONTRAST = {
  mqm_gap: 1.4,                // GPT-5.2 - Gemini
  admittance_gap_pp: 63,       // Gemini - GPT-5.2
  top_models: ['gpt', 'gemini'],
}
