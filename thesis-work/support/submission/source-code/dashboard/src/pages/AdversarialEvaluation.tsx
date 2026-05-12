// @ts-nocheck
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL, ALL_BENCHMARKS_BLOB_URL, EXPERIMENT_RESULTS_BLOB_URL } from '../config'
import FigureSidebar from '../components/FigureSidebar'

/* ---------- types ---------- */

interface SampleManifest {
  figures_by_subfolder: Record<string, string[]>
  subfolders?: string[]
  transforms?: string[]
  transform_labels?: Record<string, string>
}

interface CaptionBiasModification {
  claim: string
  reality: string
  type: string
  principle: string
}

interface FigureBenchmark {
  figure_key: string
  subfolder: string
  native_language: string
  prompt_reverse?: {
    true_statement: string
    false_statement: string
    fact_description: string
    true_statement_english?: string
    false_statement_english?: string
  }
  caption_bias?: {
    original_caption: string
    modified_caption: string
    modifications: CaptionBiasModification[]
  }
}

interface ProbeResult {
  statement: string
  statement_english?: string
  answer: string
  correct: boolean
}

interface PromptReverseResult {
  fact_description: string
  true_probe: ProbeResult
  false_probe: ProbeResult
  score: number
  pattern: string
}

interface CaptionBiasEvalItem {
  claim: string
  claim_english?: string
  reality: string
  reality_english?: string
  mapped_to: string
  reason: string
  reason_english?: string
}

interface JudgeResult {
  resistance: number
  completeness: number
  evaluations: CaptionBiasEvalItem[]
}

interface CaptionBiasResult {
  description: string
  description_english?: string
  resistance?: number
  completeness?: number
  evaluations?: CaptionBiasEvalItem[]
  judges?: Record<string, JudgeResult>
}

interface HallucinationEvalItem {
  probe_id: string
  probe_type: string
  question: string
  model_answer: string
  model_answer_english?: string
  judge_score: number | null
  judge_reasoning: string
}

interface CapabilityEvalItem {
  question_id: string
  question: string
  question_english?: string
  expected_answer: string
  expected_answer_english?: string
  model_answer: string
  answer_type: string
  acceptable_range?: number[]
  score: number | null
  reason: string
  excluded: boolean
}

interface CapabilityJudgeResult {
  average_score: number
  total_scored: number
  evaluations: CapabilityEvalItem[]
}

interface CapabilityResult {
  judges: Record<string, CapabilityJudgeResult>
}

interface HallucinationResult {
  judges: Record<string, HallucinationEvalItem[]>
}

interface AdmittanceElement {
  element: string
  mentioned: boolean
  admits: boolean
  fabricates: boolean
  fabricated_value?: string | null
  correct: boolean
  reason: string
  admittance: number
}

interface AdmittanceBlurResult {
  admittance_score: number
  total_elements: number
  elements?: AdmittanceElement[]
  elements_by_language?: Record<string, AdmittanceElement[]>
  model_description?: string
  model_descriptions_by_language?: Record<string, string>
}

interface AdmittanceResult {
  judges: Record<string, Record<string, AdmittanceBlurResult>>
}

interface ActiveAdmittanceJudgeResult {
  question: string
  expected_answer: string
  blurred_element: string
  model_answer: string
  admits: boolean
  fabricates: boolean
  correct: boolean
  reason: string
  admittance_score: number
}

interface ActiveAdmittanceResult {
  judges: Record<string, ActiveAdmittanceJudgeResult>
}

interface ModelExperiment {
  prompt_reverse?: PromptReverseResult
  caption_bias?: CaptionBiasResult
  hallucination?: HallucinationResult
  capability?: CapabilityResult
  admittance?: AdmittanceResult
  active_admittance?: ActiveAdmittanceResult
}

interface FigureExperiment {
  models: Record<string, ModelExperiment>
}

type ExperimentResults = Record<string, FigureExperiment>

const ALL_MODELS = [
  'gpt-5.2',
  'gemini-3.1-pro',
  'claude-opus-4.6',
  'qwen3-vl-235b-a22b',
  'qwen3-vl-32b',
  'qwen3-vl-30b-a3b',
  'qwen3-vl-8b',
  'llama4-maverick',
  'llama4-scout',
  'gemma3-27b-it',
  'gemma3-12b-it',
  'gemma3-4b-it',
  'phi-4-multimodal',
]

/* ---------- helpers ---------- */

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()
  return (
    <button onClick={toggleTheme} className="w-10 h-10 flex items-center justify-center rounded-full m3-state-hover" style={{ backgroundColor: 'var(--m3-surface-container-high)' }} aria-label="Toggle theme">
      {isDark ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
      )}
    </button>
  )
}

function ChevronIcon({ open }: { open: boolean }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
      style={{ transform: open ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 200ms ease' }}>
      <polyline points="6 9 12 15 18 9" />
    </svg>
  )
}

function CollapsibleSection({ title, count, defaultOpen = false, children }: { title: string; count?: number; defaultOpen?: boolean; children: React.ReactNode }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full px-6 py-4 flex items-center gap-3 m3-state-hover"
        style={{ backgroundColor: 'var(--m3-surface)' }}
      >
        <h3 className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
          {title}{count != null ? ` (${count})` : ''}
        </h3>
        <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
        <span style={{ color: 'var(--m3-outline)' }}><ChevronIcon open={open} /></span>
      </button>
      {open && <div className="px-6 pb-6">{children}</div>}
    </div>
  )
}

function Badge({ label, variant }: { label: string; variant: 'success' | 'error' | 'neutral' | 'primary' | 'tertiary' }) {
  const styles: Record<string, { bg: string; color: string }> = {
    success: { bg: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' },
    error: { bg: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)' },
    neutral: { bg: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' },
    primary: { bg: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' },
    tertiary: { bg: 'var(--m3-tertiary-container)', color: 'var(--m3-on-tertiary-container)' },
  }
  const s = styles[variant]
  return (
    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: s.bg, color: s.color }}>
      {label}
    </span>
  )
}

function ScoreBar({ value, label }: { value: number; label: string }) {
  const pct = Math.round(value * 100)
  return (
    <div className="flex items-center gap-3">
      <span className="text-[10px] font-medium uppercase w-24 text-right" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>{label}</span>
      <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--m3-surface-container-highest)' }}>
        <div
          className="h-full rounded-full"
          style={{
            width: `${pct}%`,
            backgroundColor: pct >= 80 ? 'var(--m3-primary)' : pct >= 50 ? 'var(--m3-tertiary)' : 'var(--m3-error)',
            transition: 'width 300ms ease',
          }}
        />
      </div>
      <span className="text-xs font-medium tabular-nums w-12" style={{ color: 'var(--m3-on-surface)' }}>{pct}%</span>
    </div>
  )
}

/* ---------- main component ---------- */

export default function AdversarialEvaluation() {
  const [manifest, setManifest] = useState<SampleManifest | null>(null)
  const [benchmarks, setBenchmarks] = useState<Record<string, FigureBenchmark> | null>(null)
  const [experiments, setExperiments] = useState<ExperimentResults | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSubfolder, setSelectedSubfolder] = useState('')
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedModel, setSelectedModel] = useState(ALL_MODELS[0])
  const [expandedImage, setExpandedImage] = useState<{ src: string; label: string } | null>(null)
  const { isDark } = useTheme()

  useEffect(() => {
    setLoading(true)
    const loadBenchmarks = () =>
      fetch(`${ALL_BENCHMARKS_BLOB_URL}?t=${Date.now()}`).then(r => r.ok ? r.json() : Promise.reject())
        .catch(() => fetch(`${import.meta.env.BASE_URL}data/all_benchmarks.json`).then(r => r.json()))
        .catch(() => null)

    const loadExperiments = () =>
      fetch(`${EXPERIMENT_RESULTS_BLOB_URL}?t=${Date.now()}`).then(r => r.ok ? r.json() : Promise.reject())
        .catch(() => fetch(`${import.meta.env.BASE_URL}data/experiment_results.json`).then(r => r.json()))
        .catch(() => null)

    Promise.all([
      fetch(`${import.meta.env.BASE_URL}data/adversarial_experiments.json`).then(r => r.json()),
      loadBenchmarks(),
      loadExperiments(),
    ])
      .then(([manifestData, benchmarksJson, experimentsJson]) => {
        setManifest(manifestData as SampleManifest)
        if (benchmarksJson) setBenchmarks(benchmarksJson as Record<string, FigureBenchmark>)
        if (experimentsJson) setExperiments(experimentsJson as ExperimentResults)
        const subs = (manifestData as SampleManifest).subfolders || Object.keys((manifestData as SampleManifest).figures_by_subfolder)
        if (subs.length) setSelectedSubfolder(subs[0])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const subfolders = useMemo(() => {
    if (!manifest) return []
    return manifest.subfolders || Object.keys(manifest.figures_by_subfolder)
  }, [manifest])

  const figureKeys = useMemo(() => {
    if (!manifest) return []
    return manifest.figures_by_subfolder[selectedSubfolder] || []
  }, [manifest, selectedSubfolder])

  useEffect(() => {
    if (figureKeys.length && !figureKeys.includes(selectedFigure)) {
      setSelectedFigure(figureKeys[0])
    }
  }, [figureKeys, selectedFigure])

  const currentBenchmark = useMemo(() => {
    if (!benchmarks || !selectedFigure) return null
    return benchmarks[selectedFigure] || null
  }, [benchmarks, selectedFigure])

  const currentExperiment = useMemo(() => {
    if (!experiments || !selectedFigure) return null
    return experiments[selectedFigure] || null
  }, [experiments, selectedFigure])

  const modelData = useMemo(() => {
    if (!currentExperiment) return null
    return currentExperiment.models[selectedModel] || null
  }, [currentExperiment, selectedModel])

  const availableModels = useMemo(() => {
    if (!currentExperiment) return ALL_MODELS
    return ALL_MODELS.filter(m => currentExperiment.models[m])
  }, [currentExperiment])

  const [selectedJudge, setSelectedJudge] = useState('gpt-4o')

  // Get caption bias data for current judge
  const cb = useMemo(() => {
    if (!modelData?.caption_bias) return null
    const cbData = modelData.caption_bias
    // New format with judges
    if (cbData.judges && cbData.judges[selectedJudge]) {
      const judgeData = cbData.judges[selectedJudge]
      return {
        description: cbData.description,
        description_english: cbData.description_english,
        resistance: judgeData.resistance,
        completeness: judgeData.completeness,
        evaluations: judgeData.evaluations,
      }
    }
    // Old format (backwards compat)
    if (cbData.evaluations) {
      return cbData as { description: string; description_english?: string; resistance: number; completeness: number; evaluations: CaptionBiasEvalItem[] }
    }
    return null
  }, [modelData, selectedJudge])

  const availableJudges = useMemo(() => {
    if (!modelData?.caption_bias?.judges) return ['gpt-4o']
    return Object.keys(modelData.caption_bias.judges)
  }, [modelData])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>Loading</span>
      </div>
    </div>
  )

  if (!manifest) return null

  const imgBase = `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}`
  const pr = modelData?.prompt_reverse || null

  return (
    <div className="h-screen flex flex-col overflow-hidden animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header className="px-6 h-16 flex items-center gap-4" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface)' }}>
        <Link to="/evaluation" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
        </Link>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--m3-primary)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
            </svg>
          </div>
          <h1 className="text-base font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}>Adversarial Evaluation</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <div className="flex items-center gap-2">
            <label className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model</label>
            <select className="m3-select" value={selectedModel} onChange={e => setSelectedModel(e.target.value)}>
              {ALL_MODELS.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Judge</label>
            <select className="m3-select" value={selectedJudge} onChange={e => setSelectedJudge(e.target.value)}>
              {availableJudges.map(j => <option key={j} value={j}>{j}</option>)}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Dataset</label>
            <select className="m3-select" value={selectedSubfolder} onChange={e => setSelectedSubfolder(e.target.value)}>
              {subfolders.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <span className="text-xs font-medium tabular-nums px-3 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
            {figureKeys.length} figures
          </span>
          <ThemeToggle />
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 flex min-h-0 overflow-hidden">
        <FigureSidebar figureKeys={figureKeys} selectedKey={selectedFigure} onSelect={k => setSelectedFigure(k)} />

        <div className="flex-1 overflow-y-auto">
          {/* Figure header with image */}
          <div className="p-6" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container-low)' }}>
            <div className="flex items-start gap-6 animate-fade-in-up">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                    {selectedFigure}
                  </h2>
                  {!availableModels.includes(selectedModel) && (
                    <Badge label="No data for this model" variant="neutral" />
                  )}
                  {pr && <Badge label={`PR: ${pr.pattern}`} variant={pr.pattern === 'correct' ? 'success' : 'error'} />}
                  {cb && <Badge label={`Resistance: ${Math.round(cb.resistance * 100)}%`} variant={cb.resistance >= 0.7 ? 'success' : 'error'} />}
                </div>
                <div
                  className="rounded-xl overflow-hidden inline-block cursor-pointer"
                  style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}
                  onClick={() => setExpandedImage({ src: `${imgBase}/original.png`, label: `${selectedFigure} -- Original` })}
                >
                  <img
                    src={`${imgBase}/original.png`}
                    alt={`${selectedFigure} original`}
                    className="max-h-72 w-auto"
                    style={{ display: 'block' }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Prompt Reverse section */}
          <CollapsibleSection title="Prompt Reverse" defaultOpen={true}>
            {pr ? (
              <div className="space-y-4 animate-fade-in">
                {/* Fact */}
                <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                  <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Fact Being Tested</span>
                  <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-on-surface)' }}>{pr.fact_description}</p>
                </div>

                {/* Two probe cards side by side */}
                <div className="grid grid-cols-2 gap-4">
                  {/* TRUE probe */}
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-primary-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>TRUE Statement</span>
                      <div className="flex-1" />
                      <Badge label={pr.true_probe.correct ? 'Correct' : 'Wrong'} variant={pr.true_probe.correct ? 'success' : 'error'} />
                    </div>
                    <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-primary-container)' }}>
                      {pr.true_probe.statement}
                    </p>
                    {pr.true_probe.statement_english && pr.true_probe.statement_english !== pr.true_probe.statement && (
                      <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-primary-container)', opacity: 0.6 }}>
                        <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                        {pr.true_probe.statement_english}
                      </p>
                    )}
                    <div className="flex items-center gap-2 pt-2" style={{ borderTop: '1px solid var(--m3-outline-variant)' }}>
                      <span className="text-[10px]" style={{ color: 'var(--m3-on-primary-container)', opacity: 0.7 }}>Model answered:</span>
                      <span className="text-xs font-medium" style={{ color: 'var(--m3-on-primary-container)' }}>{pr.true_probe.answer}</span>
                      <span className="text-[10px]" style={{ color: 'var(--m3-on-primary-container)', opacity: 0.7 }}>(expected: A)</span>
                    </div>
                  </div>

                  {/* FALSE probe */}
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-error-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>FALSE Statement</span>
                      <div className="flex-1" />
                      <Badge label={pr.false_probe.correct ? 'Correct' : 'Wrong'} variant={pr.false_probe.correct ? 'success' : 'error'} />
                    </div>
                    <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-error-container)' }}>
                      {pr.false_probe.statement}
                    </p>
                    {pr.false_probe.statement_english && pr.false_probe.statement_english !== pr.false_probe.statement && (
                      <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-error-container)', opacity: 0.6 }}>
                        <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                        {pr.false_probe.statement_english}
                      </p>
                    )}
                    <div className="flex items-center gap-2 pt-2" style={{ borderTop: '1px solid var(--m3-outline-variant)' }}>
                      <span className="text-[10px]" style={{ color: 'var(--m3-on-error-container)', opacity: 0.7 }}>Model answered:</span>
                      <span className="text-xs font-medium" style={{ color: 'var(--m3-on-error-container)' }}>{pr.false_probe.answer}</span>
                      <span className="text-[10px]" style={{ color: 'var(--m3-on-error-container)', opacity: 0.7 }}>(expected: B)</span>
                    </div>
                  </div>
                </div>

                {/* Score + pattern */}
                <div className="flex items-center gap-4">
                  <ScoreBar value={pr.score} label="Score" />
                  <Badge
                    label={pr.pattern}
                    variant={pr.pattern === 'correct' ? 'success' : pr.pattern === 'true_bias' || pr.pattern === 'false_bias' ? 'tertiary' : 'error'}
                  />
                </div>
              </div>
            ) : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No prompt reverse data available for {selectedModel} on this figure.</p>
              </div>
            )}
          </CollapsibleSection>

          {/* Caption Bias section */}
          <CollapsibleSection title="Caption Bias" defaultOpen={true}>
            {cb ? (
              <div className="space-y-4 animate-fade-in">
                {/* Original & modified captions from benchmarks */}
                {currentBenchmark?.caption_bias && (
                  <>
                    <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                      <span className="text-[10px] font-medium uppercase block mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Original Caption</span>
                      <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>
                        {currentBenchmark.caption_bias.original_caption}
                      </p>
                    </div>
                    <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-error-container)', border: `1px solid var(--m3-outline-variant)` }}>
                      <span className="text-[10px] font-medium uppercase block mb-1" style={{ color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>Modified Caption (with injected errors)</span>
                      <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-error-container)' }}>
                        {currentBenchmark.caption_bias.modified_caption}
                      </p>
                    </div>

                    {/* Modifications list */}
                    <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                      <span className="text-[10px] font-medium uppercase block mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                        Modifications ({currentBenchmark.caption_bias.modifications.length})
                      </span>
                      <div className="space-y-2">
                        {currentBenchmark.caption_bias.modifications.map((mod, i) => (
                          <div key={i} className="flex items-start gap-2 text-xs" style={{ color: 'var(--m3-on-surface)' }}>
                            <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded flex-shrink-0" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                              #{i + 1}
                            </span>
                            <div>
                              <p className="leading-relaxed"><strong>Claim:</strong> {mod.claim}</p>
                              <p className="leading-relaxed" style={{ color: 'var(--m3-error)' }}><strong>Reality:</strong> {mod.reality}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </>
                )}

                {/* Model's description */}
                <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                  <span className="text-[10px] font-medium uppercase block mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                    Model Description ({selectedModel})
                  </span>
                  <p className="text-xs leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--m3-on-surface)' }}>
                    {cb.description || '(no description available)'}
                  </p>
                  {cb.description_english && cb.description_english !== cb.description && (
                    <p className="text-xs leading-relaxed whitespace-pre-wrap mt-2" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                      <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                      {cb.description_english}
                    </p>
                  )}
                </div>

                {/* Judge evaluations */}
                <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                  <span className="text-[10px] font-medium uppercase block mb-3" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                    Judge Evaluation ({cb.evaluations.length} modifications)
                  </span>
                  <div className="space-y-3">
                    {cb.evaluations.map((ev, i) => (
                      <div key={i} className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                            #{i + 1}
                          </span>
                          <Badge
                            label={ev.mapped_to}
                            variant={ev.mapped_to === 'image' ? 'success' : ev.mapped_to === 'caption' ? 'error' : 'neutral'}
                          />
                        </div>
                        <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface)' }}>
                          <strong>Claim:</strong> {ev.claim}
                        </p>
                        {ev.claim_english && ev.claim_english !== ev.claim && (
                          <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.claim_english}
                          </p>
                        )}
                        <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-error)' }}>
                          <strong>Reality:</strong> {ev.reality}
                        </p>
                        {ev.reality_english && ev.reality_english !== ev.reality && (
                          <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-error)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.reality_english}
                          </p>
                        )}
                        <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>
                          <strong>Reason:</strong> {ev.reason}
                        </p>
                        {ev.reason_english && ev.reason_english !== ev.reason && (
                          <p className="text-[11px]" style={{ color: 'var(--m3-on-surface-variant)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.reason_english}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Scores */}
                <div className="space-y-2">
                  <ScoreBar value={cb.resistance} label="Resistance" />
                  <ScoreBar value={cb.completeness} label="Completeness" />
                </div>
              </div>
            ) : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No caption bias evaluation available for {selectedModel} on this figure.</p>
              </div>
            )}
          </CollapsibleSection>

          {/* Hallucination Probes Evaluation */}
          <CollapsibleSection title={`Hallucination Probes (${selectedJudge})`} count={modelData?.hallucination?.judges?.[selectedJudge]?.length}>
            {modelData?.hallucination?.judges?.[selectedJudge] ? (
              <div className="space-y-3">
                {modelData.hallucination.judges[selectedJudge].map((ev) => {
                  const probe = currentBenchmark?.hallucination_probes?.find((p: Record<string, unknown>) => p.id === ev.probe_id) as Record<string, unknown> | undefined
                  return (
                    <div key={ev.probe_id} className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                          {ev.probe_id}
                        </span>
                        <Badge
                          label={ev.probe_type}
                          variant={ev.probe_type === 'inexist' ? 'error' : ev.probe_type === 'contra' ? 'tertiary' : 'neutral'}
                        />
                        <Badge
                          label={ev.judge_score === 1 ? 'PASS' : ev.judge_score === 0.5 ? 'PARTIAL' : ev.judge_score === 0 ? 'FAIL' : 'N/A'}
                          variant={ev.judge_score === 1 ? 'success' : ev.judge_score === 0.5 ? 'tertiary' : 'error'}
                        />
                        <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                          {ev.judge_score}
                        </span>
                      </div>

                      <div className="mb-2">
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Probe</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)' }}>{ev.question}</p>
                        {probe?.question_english && probe.question_english !== ev.question && (
                          <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {probe.question_english as string}
                          </p>
                        )}
                      </div>

                      {probe?.expected_behavior && (
                        <div className="mb-2">
                          <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Expected</span>
                          <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-primary)' }}>{probe.expected_behavior as string}</p>
                        </div>
                      )}

                      <div className="mb-2">
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Answer</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)' }}>{ev.model_answer?.substring(0, 300)}{ev.model_answer?.length > 300 ? '...' : ''}</p>
                        {ev.model_answer_english && ev.model_answer_english !== ev.model_answer && (
                          <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.model_answer_english}
                          </p>
                        )}
                      </div>

                      <div>
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Judge Reasoning</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface-variant)' }}>{ev.judge_reasoning}</p>
                      </div>
                    </div>
                  )
                })}

                {/* Summary scores */}
                <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container-high)', border: `1px solid var(--m3-outline-variant)` }}>
                  {(() => {
                    const evals = modelData.hallucination!.judges[selectedJudge]
                    const byType: Record<string, number[]> = {}
                    evals.forEach(e => {
                      if (e.judge_score != null) {
                        if (!byType[e.probe_type]) byType[e.probe_type] = []
                        byType[e.probe_type].push(e.judge_score)
                      }
                    })
                    return (
                      <div className="space-y-2">
                        {Object.entries(byType).map(([type, scores]) => (
                          <ScoreBar key={type} value={scores.reduce((a, b) => a + b, 0) / scores.length} label={`${type} (${scores.length})`} />
                        ))}
                        {(() => {
                          const all = evals.filter(e => e.judge_score != null).map(e => e.judge_score!)
                          return all.length > 0 ? <ScoreBar value={all.reduce((a, b) => a + b, 0) / all.length} label={`Overall (${all.length})`} /> : null
                        })()}
                      </div>
                    )
                  })()}
                </div>
              </div>
            ) : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No hallucination evaluation available for {selectedModel} with {selectedJudge}.</p>
              </div>
            )}
          </CollapsibleSection>

          {/* Capability Questions Evaluation */}
          <CollapsibleSection title={`Capability Questions (${selectedJudge})`} count={modelData?.capability?.judges?.[selectedJudge]?.total_scored}>
            {modelData?.capability?.judges?.[selectedJudge] ? (() => {
              const capJudge = modelData.capability!.judges[selectedJudge]
              return (
                <div className="space-y-3">
                  {capJudge.evaluations.map((ev) => (
                    <div key={ev.question_id} className="rounded-lg p-4" style={{
                      backgroundColor: 'var(--m3-surface-container)',
                      border: `1px solid var(--m3-outline-variant)`,
                      opacity: ev.excluded ? 0.5 : 1,
                    }}>
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                          {ev.question_id}
                        </span>
                        <Badge label={ev.answer_type} variant="neutral" />
                        {ev.excluded ? (
                          <Badge label="EXCLUDED" variant="neutral" />
                        ) : (
                          <Badge
                            label={ev.score === 1 ? 'CORRECT' : ev.score === 0.5 ? 'PARTIAL' : ev.score === 0 ? 'WRONG' : 'N/A'}
                            variant={ev.score === 1 ? 'success' : ev.score === 0.5 ? 'tertiary' : 'error'}
                          />
                        )}
                        {ev.score !== null && !ev.excluded && (
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                            {ev.score}
                          </span>
                        )}
                      </div>

                      <div className="mb-2">
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Question</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)' }}>{ev.question}</p>
                        {ev.question_english && ev.question_english !== ev.question && (
                          <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.question_english}
                          </p>
                        )}
                      </div>

                      <div className="mb-2">
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Expected Answer</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-primary)' }}>
                          {ev.expected_answer}
                          {ev.acceptable_range && <span style={{ color: 'var(--m3-outline)' }}> (range: [{ev.acceptable_range[0]}, {ev.acceptable_range[1]}])</span>}
                        </p>
                        {ev.expected_answer_english && ev.expected_answer_english !== ev.expected_answer && (
                          <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-primary)', opacity: 0.6 }}>
                            <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                            {ev.expected_answer_english}
                          </p>
                        )}
                      </div>

                      <div className="mb-2">
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Answer</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface)' }}>{ev.model_answer?.substring(0, 300)}{ev.model_answer?.length > 300 ? '...' : ''}</p>
                      </div>

                      <div>
                        <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Scoring Reason</span>
                        <p className="text-xs leading-relaxed mt-0.5" style={{ color: 'var(--m3-on-surface-variant)' }}>{ev.reason}</p>
                      </div>
                    </div>
                  ))}

                  <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container-high)', border: `1px solid var(--m3-outline-variant)` }}>
                    <ScoreBar value={capJudge.average_score} label={`Overall (${capJudge.total_scored} scored)`} />
                  </div>
                </div>
              )
            })() : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No capability evaluation available for {selectedModel} with {selectedJudge}.</p>
              </div>
            )}
          </CollapsibleSection>

          {/* Passive Admittance Evaluation */}
          <CollapsibleSection title={`Passive Admittance (${selectedJudge})`}>
            {modelData?.admittance?.judges?.[selectedJudge] ? (() => {
              const admJudge = modelData.admittance!.judges[selectedJudge]
              return (
                <div className="space-y-4">
                  {Object.entries(admJudge).map(([blurType, blurResult]) => (
                    <div key={blurType}>
                      <div className="flex items-center gap-2 mb-3">
                        <h4 className="text-xs font-medium" style={{ color: 'var(--m3-on-surface)' }}>
                          {blurType === 'axis_blurred' ? 'Axis Blur' : 'Selective Blur'}
                        </h4>
                        <Badge
                          label={`A=${blurResult.admittance_score.toFixed(2)}`}
                          variant={blurResult.admittance_score >= 0.7 ? 'success' : blurResult.admittance_score >= 0.3 ? 'tertiary' : 'error'}
                        />
                      </div>
                      {blurResult.model_description && (
                        <div className="rounded-lg p-3 mb-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                          <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Description</p>
                          <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{blurResult.model_description.substring(0, 500)}{blurResult.model_description.length > 500 ? '...' : ''}</p>
                        </div>
                      )}
                      {blurResult.model_descriptions_by_language && Object.keys(blurResult.model_descriptions_by_language).length > 0 && (
                        <div className="rounded-lg p-3 mb-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                          <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Descriptions</p>
                          {Object.entries(blurResult.model_descriptions_by_language).map(([lang, desc]) => (
                            <div key={lang} className="mb-2">
                              <p className="text-[10px] font-medium" style={{ color: 'var(--m3-primary)' }}>{lang}</p>
                              <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{desc.substring(0, 400)}{desc.length > 400 ? '...' : ''}</p>
                            </div>
                          ))}
                        </div>
                      )}
                      <div className="space-y-2">
                        {(blurResult.elements || []).map((el, i) => (
                          <div key={i} className="rounded-lg p-3" style={{
                            backgroundColor: 'var(--m3-surface-container)',
                            border: `1px solid var(--m3-outline-variant)`,
                          }}>
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{
                                backgroundColor: !el.mentioned ? 'var(--m3-surface-container-highest)' : el.admits ? 'var(--m3-primary-container)' : 'var(--m3-error-container)',
                                color: !el.mentioned ? 'var(--m3-on-surface-variant)' : el.admits ? 'var(--m3-on-primary-container)' : 'var(--m3-on-error-container)',
                              }}>
                                {el.element}
                              </span>
                              {!el.mentioned && <Badge label="SILENT" variant="neutral" />}
                              {el.mentioned && el.admits && <Badge label="ADMITS" variant="success" />}
                              {el.mentioned && !el.admits && <Badge label="NO ADMIT" variant="error" />}
                              {el.fabricates && <Badge label={el.correct ? 'FABRICATES ✓' : 'FABRICATES ✗'} variant={el.correct ? 'tertiary' : 'error'} />}
                            </div>
                            <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{el.reason}</p>
                            {el.fabricated_value && (
                              <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-error)' }}>
                                <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>Fabricated: </span>
                                {el.fabricated_value}
                              </p>
                            )}
                          </div>
                        ))}
                        {blurResult.elements_by_language && Object.entries(blurResult.elements_by_language).map(([lang, els]) => (
                          <div key={lang}>
                            <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>{lang}</p>
                            {els.map((el, i) => (
                              <div key={i} className="rounded-lg p-3 mb-2" style={{
                                backgroundColor: 'var(--m3-surface-container)',
                                border: `1px solid var(--m3-outline-variant)`,
                              }}>
                                <div className="flex items-center gap-2 mb-1">
                                  <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{
                                    backgroundColor: el.status === 'admits' ? 'var(--m3-primary-container)' : el.status === 'fabricates' ? 'var(--m3-error-container)' : 'var(--m3-surface-container-highest)',
                                    color: el.status === 'admits' ? 'var(--m3-on-primary-container)' : el.status === 'fabricates' ? 'var(--m3-on-error-container)' : 'var(--m3-on-surface-variant)',
                                  }}>
                                    {el.element}
                                  </span>
                                  <Badge
                                    label={el.status === 'admits' ? 'ADMITS' : el.status === 'fabricates' ? 'FABRICATES' : 'SILENT'}
                                    variant={el.status === 'admits' ? 'success' : el.status === 'fabricates' ? 'error' : 'neutral'}
                                  />
                                </div>
                                <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{el.reason}</p>
                                {el.fabricated_value && (
                                  <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-error)' }}>
                                    <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>Fabricated: </span>
                                    {el.fabricated_value}
                                  </p>
                                )}
                              </div>
                            ))}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )
            })() : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No admittance evaluation available for {selectedModel} with {selectedJudge}.</p>
              </div>
            )}
          </CollapsibleSection>

          {/* Active Admittance Evaluation */}
          <CollapsibleSection title={`Active Admittance (${selectedJudge})`}>
            {modelData?.active_admittance?.judges?.[selectedJudge] ? (() => {
              const aa = modelData.active_admittance!.judges[selectedJudge]
              return (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-3">
                    <Badge
                      label={`A=${aa.admittance_score.toFixed(2)}`}
                      variant={aa.admittance_score >= 0.7 ? 'success' : aa.admittance_score >= 0.3 ? 'tertiary' : 'error'}
                    />
                    {aa.admits && <Badge label="ADMITS" variant="success" />}
                    {!aa.admits && aa.fabricates && <Badge label="NO ADMIT" variant="error" />}
                    {aa.fabricates && <Badge label={aa.correct ? 'FABRICATES ✓' : 'FABRICATES ✗'} variant={aa.correct ? 'tertiary' : 'error'} />}
                  </div>

                  <div className="flex gap-4 mb-3">
                    <div className="flex-1">
                      <img
                        src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`}
                        alt="Selective blur"
                        className="rounded-lg max-h-48 w-auto cursor-pointer"
                        onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`, label: 'Selective Blur (sent to model)' })}
                      />
                      <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Selective Blur (sent to model)</p>
                    </div>
                    <div className="flex-1">
                      <img
                        src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original.png`}
                        alt="Original"
                        className="rounded-lg max-h-48 w-auto cursor-pointer"
                        onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original.png`, label: 'Original' })}
                      />
                      <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Original</p>
                    </div>
                  </div>

                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Question</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{aa.question}</p>
                  </div>

                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-primary-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>Expected Answer</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-primary-container)' }}>{aa.expected_answer}</p>
                  </div>

                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Answer</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{aa.model_answer?.substring(0, 500)}{(aa.model_answer?.length || 0) > 500 ? '...' : ''}</p>
                  </div>

                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-high)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)' }}>
                        {aa.blurred_element}
                      </span>
                    </div>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Judge Reasoning</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{aa.reason}</p>
                  </div>
                </div>
              )
            })() : (
              <div className="rounded-lg p-6 text-center" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No active admittance evaluation available for {selectedModel} with {selectedJudge}.</p>
              </div>
            )}
          </CollapsibleSection>
        </div>
      </div>

      {/* Expanded image overlay */}
      {expandedImage && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center animate-fade-in"
          style={{ backgroundColor: isDark ? 'rgba(0,0,0,0.85)' : 'rgba(0,0,0,0.6)' }}
          onClick={() => setExpandedImage(null)}
        >
          <div className="relative max-w-5xl max-h-[90vh] p-4">
            <p className="text-xs font-medium mb-3 text-center" style={{ color: '#fff' }}>{expandedImage.label}</p>
            <img src={expandedImage.src} alt={expandedImage.label} className="max-w-full max-h-[80vh] rounded-xl" style={{ display: 'block', margin: '0 auto' }} />
          </div>
        </div>
      )}
    </div>
  )
}
