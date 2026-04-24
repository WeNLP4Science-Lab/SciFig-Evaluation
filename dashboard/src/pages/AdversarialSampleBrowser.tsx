// @ts-nocheck
import { useState, useEffect, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL, ALL_BENCHMARKS_BLOB_URL, ALL_BENCHMARKS_BLOB_WRITE_URL } from '../config'
import FigureSidebar from '../components/FigureSidebar'

interface SampleManifest {
  description: string
  total: number
  figures?: {
    figure_key: string
    subfolder: string
    figure_type: string
    paper_title: string
    caption: string
    figure_image: string
    annotations: {
      annotation_language: string
      annotation: string
      annotated_by: number
      figure_type: string
    }[]
  }[]
  figures_by_subfolder?: Record<string, string[]>
  transforms?: string[]
  transform_labels?: Record<string, string>
  subfolders?: string[]
}

interface Question {
  id: string
  question: string
  expected_answer: string
  answer_type: string
  category: string
}

interface HallucinationProbe {
  id: string
  type: string
  question: string
  expected_behavior: string
  false_element?: string
  false_premise?: string
  why_unanswerable?: string
  principle: string
  answer_type: string
}

interface PromptReverse {
  true_statement: string
  false_statement: string
  fact_description: string
}

interface AxisBlurElement {
  element: string
  description: string
}

interface AxisBlurProbe {
  subfolder: string
  blurred_elements: AxisBlurElement[]
  notes: string
}

interface ActiveAdmittanceProbe {
  subfolder: string
  question: string
  question_english?: string
  expected_answer: string
  blurred_element: string
  why_requires_blurred: string
}

interface CaptionBiasModification {
  claim: string
  reality: string
  type: string
  principle: string
}

interface CaptionBias {
  original_caption: string
  modified_caption: string
  modifications: CaptionBiasModification[]
}

interface FigureBenchmark {
  figure_key: string
  subfolder: string
  native_language: string
  capability_questions?: Question[]
  hallucination_probes?: HallucinationProbe[]
  prompt_reverse?: PromptReverse
  caption_bias?: CaptionBias
}

interface AdversarialSampleBrowserProps {
  manifestFile: string
  title: string
}

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

function EditableQuestionCard({ q, onChange, langLabel }: { q: Question; onChange: (updated: Question) => void; langLabel?: string }) {
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(q)

  useEffect(() => { setDraft(q); setEditing(false) }, [q.id])

  const handleSave = () => {
    onChange(draft)
    setEditing(false)
  }

  const handleCancel = () => {
    setDraft(q)
    setEditing(false)
  }

  return (
    <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
          {q.id}
        </span>
        <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-tertiary-container)', color: 'var(--m3-on-tertiary-container)' }}>
          {q.category}
        </span>
        <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-secondary-container)', color: 'var(--m3-on-secondary-container)' }}>
          {q.answer_type}
        </span>
        {langLabel && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' }}>
            {langLabel}
          </span>
        )}
        <div className="flex-1" />
        {!editing && (
          <button onClick={() => setEditing(true)} className="text-[10px] font-medium px-2 py-1 rounded m3-state-hover" style={{ color: 'var(--m3-primary)' }}>
            Edit
          </button>
        )}
      </div>

      {editing ? (
        <div className="space-y-3">
          <div>
            <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Question</label>
            <textarea
              value={draft.question}
              onChange={e => setDraft({ ...draft, question: e.target.value })}
              className="w-full text-xs p-2 rounded-lg resize-none"
              style={{ backgroundColor: 'var(--m3-surface-container-low)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)`, minHeight: '60px' }}
            />
          </div>
          <div>
            <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Expected Answer</label>
            <textarea
              value={draft.expected_answer}
              onChange={e => setDraft({ ...draft, expected_answer: e.target.value })}
              className="w-full text-xs p-2 rounded-lg resize-none"
              style={{ backgroundColor: 'var(--m3-surface-container-low)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)`, minHeight: '40px' }}
            />
          </div>
          <div className="flex gap-3">
            <div className="flex-1">
              <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Answer Type</label>
              <select
                value={draft.answer_type}
                onChange={e => setDraft({ ...draft, answer_type: e.target.value })}
                className="w-full text-xs p-2 rounded-lg"
                style={{ backgroundColor: 'var(--m3-surface-container-low)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)` }}
              >
                <option value="exact">exact</option>
                <option value="approximate">approximate</option>
                <option value="open_ended">open_ended</option>
              </select>
            </div>
            <div className="flex-1">
              <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Category</label>
              <select
                value={draft.category}
                onChange={e => setDraft({ ...draft, category: e.target.value })}
                className="w-full text-xs p-2 rounded-lg"
                style={{ backgroundColor: 'var(--m3-surface-container-low)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)` }}
              >
                <option value="value_reading">value_reading</option>
                <option value="comparison">comparison</option>
                <option value="counting">counting</option>
                <option value="computation">computation</option>
                <option value="trend_analysis">trend_analysis</option>
                <option value="text_reading">text_reading</option>
              </select>
            </div>
          </div>
          <div className="flex gap-2 pt-1">
            <button onClick={handleSave} className="text-[11px] font-medium px-3 py-1.5 rounded-lg" style={{ backgroundColor: 'var(--m3-primary)', color: 'var(--m3-on-primary)' }}>
              Save
            </button>
            <button onClick={handleCancel} className="text-[11px] font-medium px-3 py-1.5 rounded-lg m3-state-hover" style={{ color: 'var(--m3-on-surface-variant)', backgroundColor: 'var(--m3-surface-container-high)' }}>
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface)' }}>{q.question}</p>
          {(q as Record<string, unknown>).question_english && (q as Record<string, unknown>).question_english !== q.question && (
            <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
              <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
              {(q as Record<string, unknown>).question_english as string}
            </p>
          )}
          <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-primary)' }}>
            <span style={{ color: 'var(--m3-outline)' }}>Answer: </span>{q.expected_answer}
          </p>
        </div>
      )}
    </div>
  )
}

export default function AdversarialSampleBrowser({ manifestFile, title }: AdversarialSampleBrowserProps) {
  const [manifest, setManifest] = useState<SampleManifest | null>(null)
  const [benchmarks, setBenchmarks] = useState<Record<string, FigureBenchmark> | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSubfolder, setSelectedSubfolder] = useState('')
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedTransform, setSelectedTransform] = useState<string | null>(null)
  const [expandedImage, setExpandedImage] = useState<{ src: string; label: string } | null>(null)
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<string | null>(null)
  const [axisBlurProbes, setAxisBlurProbes] = useState<Record<string, AxisBlurProbe> | null>(null)
  const [selectiveBlurProbes, setSelectiveBlurProbes] = useState<Record<string, AxisBlurProbe> | null>(null)
  const [activeProbes, setActiveProbes] = useState<Record<string, ActiveAdmittanceProbe> | null>(null)
  const [atomsData, setAtomsData] = useState<Record<string, any> | null>(null)
  const { isDark } = useTheme()

  const isAdversarial = manifest?.transforms != null

  useEffect(() => {
    setLoading(true)
    const loadBenchmarks = () =>
      fetch(`${ALL_BENCHMARKS_BLOB_URL}?t=${Date.now()}`).then(r => r.ok ? r.json() : Promise.reject())
        .catch(() => fetch(`${import.meta.env.BASE_URL}data/all_benchmarks.json`).then(r => r.json()))
        .catch(() => null)

    Promise.all([
      fetch(`${import.meta.env.BASE_URL}data/${manifestFile}`).then(r => r.json()),
      loadBenchmarks(),
      fetch(`${import.meta.env.BASE_URL}data/axis_blur_probes.json`).then(r => r.json()).catch(() => null),
      fetch(`${import.meta.env.BASE_URL}data/selective_blur_probes.json`).then(r => r.json()).catch(() => null),
      fetch(`${import.meta.env.BASE_URL}data/active_selective_blur_probes.json`).then(r => r.json()).catch(() => null),
      fetch(`${import.meta.env.BASE_URL}data/atoms.json`).then(r => r.ok ? r.json() : null).catch(() => null),
    ])
      .then(([manifestData, benchmarksJson, axisBlurData, selectiveBlurData, activeProbesData, atomsJson]) => {
        setManifest(manifestData as SampleManifest)
        if (benchmarksJson) setBenchmarks(benchmarksJson as Record<string, FigureBenchmark>)
        if (axisBlurData) setAxisBlurProbes(axisBlurData.figures as Record<string, AxisBlurProbe>)
        if (selectiveBlurData) setSelectiveBlurProbes(selectiveBlurData.figures as Record<string, AxisBlurProbe>)
        if (activeProbesData) setActiveProbes(activeProbesData.figures as Record<string, ActiveAdmittanceProbe>)
        if (atomsJson) setAtomsData(atomsJson)
        const subs = (manifestData as SampleManifest).subfolders || []
        if (subs.length) setSelectedSubfolder(subs[0])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [manifestFile])

  const subfolders = useMemo(() => manifest?.subfolders || [], [manifest])

  const figureKeys = useMemo(() => {
    if (!manifest) return []
    if (isAdversarial && manifest.figures_by_subfolder) {
      return manifest.figures_by_subfolder[selectedSubfolder] || []
    }
    return (manifest.figures || []).filter(f => f.subfolder === selectedSubfolder).map(f => f.figure_key)
  }, [manifest, selectedSubfolder, isAdversarial])

  useEffect(() => {
    if (figureKeys.length && !figureKeys.includes(selectedFigure)) {
      setSelectedFigure(figureKeys[0])
    }
  }, [figureKeys, selectedFigure])

  const currentFigureData = useMemo(() => {
    if (!manifest?.figures) return null
    return manifest.figures.find(f => f.figure_key === selectedFigure && f.subfolder === selectedSubfolder)
  }, [manifest, selectedFigure, selectedSubfolder])

  const currentBenchmark = useMemo(() => {
    if (!benchmarks || !selectedFigure) return null
    return benchmarks[selectedFigure] || null
  }, [benchmarks, selectedFigure])

  const handleQuestionUpdate = useCallback((qIndex: number, updated: Question) => {
    if (!benchmarks || !selectedFigure || !benchmarks[selectedFigure]?.capability_questions) return
    const newData = { ...benchmarks }
    const fig = { ...newData[selectedFigure] }
    const arr = [...(fig.capability_questions || [])]
    arr[qIndex] = updated
    fig.capability_questions = arr
    newData[selectedFigure] = fig
    setBenchmarks(newData)
  }, [benchmarks, selectedFigure])

  const handleSaveAll = useCallback(async () => {
    if (!benchmarks) return
    setSaving(true)
    setSaveStatus(null)
    try {
      const resp = await fetch(ALL_BENCHMARKS_BLOB_WRITE_URL, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'x-ms-blob-type': 'BlockBlob' },
        body: JSON.stringify(benchmarks, null, 2),
      })
      if (resp.ok) {
        setSaveStatus('Saved')
      } else {
        setSaveStatus(`Error: save failed (${resp.status})`)
      }
    } catch (e) {
      setSaveStatus(`Error: ${e}`)
    } finally {
      setSaving(false)
      setTimeout(() => setSaveStatus(null), 3000)
    }
  }, [benchmarks])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>Loading</span>
      </div>
    </div>
  )

  if (!manifest) return null

  const imgBase = isAdversarial
    ? `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}`
    : null

  return (
    <div className="h-screen flex flex-col overflow-hidden animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header className="px-6 h-16 flex items-center gap-4" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface)' }}>
        <Link to="/dataset" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
        </Link>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--m3-primary)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <h1 className="text-base font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}>{title}</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          {saveStatus && (
            <span className="text-[11px] font-medium px-3 py-1 rounded-full" style={{ backgroundColor: saveStatus === 'Saved' ? 'var(--m3-primary-container)' : 'var(--m3-error-container)', color: saveStatus === 'Saved' ? 'var(--m3-on-primary-container)' : 'var(--m3-on-error-container)' }}>
              {saveStatus}
            </span>
          )}
          <button
            onClick={handleSaveAll}
            disabled={saving}
            className="text-[11px] font-medium px-3 py-1.5 rounded-lg"
            style={{ backgroundColor: 'var(--m3-primary)', color: 'var(--m3-on-primary)', opacity: saving ? 0.6 : 1 }}
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
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
        <FigureSidebar figureKeys={figureKeys} selectedKey={selectedFigure} onSelect={k => { setSelectedFigure(k); setSelectedTransform(null) }} />

        <div className="flex-1 overflow-y-auto">
          {/* Original image + selected transform */}
          <div className="p-6" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container-low)' }}>
            <div className="flex items-start gap-6 animate-fade-in-up">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-4">
                  <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                    {selectedFigure}
                  </h2>
                  <span className="text-[11px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>
                    Original
                  </span>
                </div>
                {currentFigureData?.paper_title && (
                  <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface-variant)' }}>{currentFigureData.paper_title}</p>
                )}
                {currentFigureData?.caption && (
                  <p className="text-xs leading-relaxed mb-3" style={{ color: 'var(--m3-outline)' }}>Caption: {currentFigureData.caption}</p>
                )}
                <div
                  className="rounded-xl overflow-hidden inline-block cursor-pointer"
                  style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}
                  onClick={() => {
                    const src = isAdversarial ? `${imgBase}/original.png` : `${FIGURES_BASE_URL}/${currentFigureData?.figure_image?.replace('figures/', '') || `${selectedSubfolder}/${selectedFigure}.png`}`
                    setExpandedImage({ src, label: `${selectedFigure} — Original` })
                  }}
                >
                  <img
                    src={isAdversarial ? `${imgBase}/original.png` : `${FIGURES_BASE_URL}/${currentFigureData?.figure_image?.replace('figures/', '') || `${selectedSubfolder}/${selectedFigure}.png`}`}
                    alt={`${selectedFigure} original`}
                    className="max-h-72 w-auto"
                    style={{ display: 'block' }}
                  />
                </div>
              </div>

              {isAdversarial && selectedTransform && (
                <div className="flex-1 animate-fade-in">
                  <div className="flex items-center gap-3 mb-4">
                    <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                      {manifest.transform_labels?.[selectedTransform] || selectedTransform}
                    </h2>
                    <span className="text-[11px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>
                      Transformed
                    </span>
                  </div>
                  <div
                    className="rounded-xl overflow-hidden inline-block cursor-pointer"
                    style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}
                    onClick={() => setExpandedImage({ src: `${imgBase}/${selectedTransform}.png`, label: `${selectedFigure} — ${manifest.transform_labels?.[selectedTransform] || selectedTransform}` })}
                  >
                    <img
                      src={`${imgBase}/${selectedTransform}.png`}
                      alt={`${selectedFigure} ${selectedTransform}`}
                      className="max-h-72 w-auto"
                      style={{ display: 'block' }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Transforms (collapsible) */}
          {isAdversarial && manifest.transforms && (
            <CollapsibleSection title="Transforms" count={manifest.transforms.length}>
              <div className="flex items-center gap-2 mb-4">
                {selectedTransform && (
                  <button onClick={() => setSelectedTransform(null)} className="text-[11px] font-medium px-2.5 py-1 rounded-full m3-state-hover" style={{ color: 'var(--m3-primary)', backgroundColor: 'var(--m3-surface-container-high)' }}>
                    Clear selection
                  </button>
                )}
              </div>
              <div className="grid grid-cols-4 lg:grid-cols-7 gap-3">
                {manifest.transforms.map(t => {
                  const isActive = selectedTransform === t
                  return (
                    <button
                      key={t}
                      onClick={() => setSelectedTransform(isActive ? null : t)}
                      className="rounded-xl overflow-hidden text-left group"
                      style={{
                        border: isActive ? '2px solid var(--m3-primary)' : `1px solid var(--m3-outline-variant)`,
                        backgroundColor: isActive ? 'var(--m3-surface-container-high)' : 'var(--m3-surface-container)',
                        transition: 'all 200ms var(--m3-easing-standard)',
                      }}
                    >
                      <div className="aspect-[4/3] overflow-hidden" style={{ backgroundColor: 'var(--m3-surface-container-highest)' }}>
                        <img
                          src={`${imgBase}/${t}.png`}
                          alt={`${selectedFigure} ${t}`}
                          className="w-full h-full object-contain transition-transform duration-300 group-hover:scale-105"
                          style={{ display: 'block' }}
                        />
                      </div>
                      <div className="p-2">
                        <h4 className="text-[10px] font-medium" style={{ color: isActive ? 'var(--m3-primary)' : 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                          {manifest.transform_labels?.[t] || t}
                        </h4>
                      </div>
                    </button>
                  )
                })}
              </div>
            </CollapsibleSection>
          )}

          {/* Axis Blur — Passive Admittance */}
          {isAdversarial && axisBlurProbes && axisBlurProbes[selectedFigure] && (
            <CollapsibleSection title="Axis Blur — Passive Admittance" count={axisBlurProbes[selectedFigure].blurred_elements.length}>
              <div className="space-y-3">
                <div className="flex gap-4 mb-4">
                  <div className="flex-1">
                    <img
                      src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/axis_blurred.png`}
                      alt="Axis blurred"
                      className="rounded-lg max-h-48 w-auto cursor-pointer"
                      onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/axis_blurred.png`, label: 'Axis Blurred' })}
                    />
                    <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Axis Blurred</p>
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
                <p className="text-[10px] font-medium uppercase mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Blurred Elements</p>
                {axisBlurProbes[selectedFigure].blurred_elements.map((el, i) => (
                  <div key={i} className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)' }}>
                        {el.element}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{el.description}</p>
                  </div>
                ))}
                {axisBlurProbes[selectedFigure].notes && (
                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Notes</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{axisBlurProbes[selectedFigure].notes}</p>
                  </div>
                )}
              </div>
            </CollapsibleSection>
          )}

          {/* Selective Blur — Passive Admittance */}
          {isAdversarial && selectiveBlurProbes && selectiveBlurProbes[selectedFigure] && (
            <CollapsibleSection title="Selective Blur — Passive Admittance" count={selectiveBlurProbes[selectedFigure].blurred_elements.length}>
              <div className="space-y-3">
                <div className="flex gap-4 mb-4">
                  <div className="flex-1">
                    <img
                      src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`}
                      alt="Selective blur"
                      className="rounded-lg max-h-48 w-auto cursor-pointer"
                      onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`, label: 'Selective Blur' })}
                    />
                    <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Selective Blur</p>
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
                {(selectiveBlurProbes[selectedFigure] as Record<string, unknown>).skip_passive_admittance && (
                  <div className="rounded-lg p-3 mb-2" style={{ backgroundColor: 'var(--m3-tertiary-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-tertiary-container)' }}>
                      <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>SKIPPED: </span>
                      {(selectiveBlurProbes[selectedFigure] as Record<string, unknown>).skip_reason as string}
                    </p>
                  </div>
                )}
                <p className="text-[10px] font-medium uppercase mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Blurred Elements</p>
                {selectiveBlurProbes[selectedFigure].blurred_elements.map((el, i) => (
                  <div key={i} className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-tertiary-container)', color: 'var(--m3-on-tertiary-container)' }}>
                        {el.element}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{el.description}</p>
                  </div>
                ))}
                {selectiveBlurProbes[selectedFigure].notes && (
                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                    <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Notes</p>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{selectiveBlurProbes[selectedFigure].notes}</p>
                  </div>
                )}
              </div>
            </CollapsibleSection>
          )}

          {/* Active Admittance — Selective Blur */}
          {isAdversarial && activeProbes && activeProbes[selectedFigure] && (
            <CollapsibleSection title="Active Admittance — Selective Blur Probe">
              <div className="space-y-3">
                <div className="flex gap-4 mb-4">
                  <div className="flex-1">
                    <img
                      src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`}
                      alt="Selective blur"
                      className="rounded-lg max-h-48 w-auto cursor-pointer"
                      onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/selective_blur.png`, label: 'Selective Blur' })}
                    />
                    <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Selective Blur (sent to model)</p>
                  </div>
                </div>
                <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                  <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Question</p>
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{activeProbes[selectedFigure].question}</p>
                  {activeProbes[selectedFigure].question_english && activeProbes[selectedFigure].question_english !== activeProbes[selectedFigure].question && (
                    <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                      <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                      {activeProbes[selectedFigure].question_english}
                    </p>
                  )}
                </div>
                <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-primary-container)', border: `1px solid var(--m3-outline-variant)` }}>
                  <p className="text-[10px] font-medium uppercase mb-1" style={{ color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>Expected Answer</p>
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-primary-container)' }}>{activeProbes[selectedFigure].expected_answer}</p>
                </div>
                <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-low)', border: `1px solid var(--m3-outline-variant)` }}>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)' }}>
                      {activeProbes[selectedFigure].blurred_element}
                    </span>
                  </div>
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{activeProbes[selectedFigure].why_requires_blurred}</p>
                </div>
              </div>
            </CollapsibleSection>
          )}

          {/* Capability Questions */}
          {isAdversarial && currentBenchmark?.capability_questions && currentBenchmark.capability_questions.length > 0 && (
            <CollapsibleSection title={`Capability Questions (${currentBenchmark.native_language})`} count={currentBenchmark.capability_questions.length}>
              <div className="space-y-3">
                {currentBenchmark.capability_questions.map((q, i) => (
                  <EditableQuestionCard
                    key={q.id}
                    q={q}
                    langLabel={currentBenchmark.native_language}
                    onChange={updated => handleQuestionUpdate(i, updated)}
                  />
                ))}
              </div>
            </CollapsibleSection>
          )}

          {/* Hallucination Probes */}
          {isAdversarial && currentBenchmark?.hallucination_probes && currentBenchmark.hallucination_probes.length > 0 && (
            <CollapsibleSection title={`Hallucination Probes (${currentBenchmark.native_language})`} count={currentBenchmark.hallucination_probes.length}>
              <div className="space-y-3">
                {currentBenchmark.hallucination_probes.map((p) => (
                  <div key={p.id} className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
                        {p.id}
                      </span>
                      <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{
                        backgroundColor: p.type === 'inexist' ? 'var(--m3-error-container)' : p.type === 'contra' ? 'var(--m3-tertiary-container)' : 'var(--m3-secondary-container)',
                        color: p.type === 'inexist' ? 'var(--m3-on-error-container)' : p.type === 'contra' ? 'var(--m3-on-tertiary-container)' : 'var(--m3-on-secondary-container)',
                      }}>
                        {p.type}
                      </span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-high)', color: 'var(--m3-outline)' }}>
                        {p.principle}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface)' }}>{p.question}</p>
                    {(p as Record<string, unknown>).question_english && (p as Record<string, unknown>).question_english !== p.question && (
                      <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                        <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                        {(p as Record<string, unknown>).question_english as string}
                      </p>
                    )}
                    <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-primary)' }}>
                      <span style={{ color: 'var(--m3-outline)' }}>Expected: </span>{p.expected_behavior}
                    </p>
                    {p.false_element && <p className="text-[11px]" style={{ color: 'var(--m3-error)' }}>False element: {p.false_element}</p>}
                    {p.false_premise && <p className="text-[11px]" style={{ color: 'var(--m3-error)' }}>False premise: {p.false_premise}</p>}
                    {p.why_unanswerable && <p className="text-[11px]" style={{ color: 'var(--m3-error)' }}>Why unanswerable: {p.why_unanswerable}</p>}
                  </div>
                ))}
              </div>
            </CollapsibleSection>
          )}

          {/* Prompt Reverse */}
          {isAdversarial && currentBenchmark?.prompt_reverse && currentBenchmark.prompt_reverse.fact_description && (
            <CollapsibleSection title="Prompt Reverse">
              <div className="rounded-lg p-4 space-y-3" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <div>
                  <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Fact</span>
                  <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-on-surface)' }}>{currentBenchmark.prompt_reverse.fact_description}</p>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-primary-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <span className="text-[10px] font-medium uppercase block mb-1" style={{ color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>TRUE (Native)</span>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-primary-container)' }}>{currentBenchmark.prompt_reverse.true_statement}</p>
                    {currentBenchmark.prompt_reverse.true_statement_english && currentBenchmark.prompt_reverse.true_statement_english !== currentBenchmark.prompt_reverse.true_statement && (
                      <p className="text-xs leading-relaxed mt-2 pt-2" style={{ color: 'var(--m3-on-primary-container)', opacity: 0.7, borderTop: '1px solid var(--m3-outline-variant)' }}>
                        <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>English: </span>
                        {currentBenchmark.prompt_reverse.true_statement_english}
                      </p>
                    )}
                  </div>
                  <div className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-error-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <span className="text-[10px] font-medium uppercase block mb-1" style={{ color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>FALSE (Native)</span>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-error-container)' }}>{currentBenchmark.prompt_reverse.false_statement}</p>
                    {currentBenchmark.prompt_reverse.false_statement_english && currentBenchmark.prompt_reverse.false_statement_english !== currentBenchmark.prompt_reverse.false_statement && (
                      <p className="text-xs leading-relaxed mt-2 pt-2" style={{ color: 'var(--m3-on-error-container)', opacity: 0.7, borderTop: '1px solid var(--m3-outline-variant)' }}>
                        <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>English: </span>
                        {currentBenchmark.prompt_reverse.false_statement_english}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            </CollapsibleSection>
          )}

          {/* Caption Bias */}
          {isAdversarial && currentBenchmark?.caption_bias && currentBenchmark.caption_bias.original_caption && (
            <CollapsibleSection title="Caption Bias" count={currentBenchmark.caption_bias.modifications?.length}>
              <div className="rounded-lg p-4 space-y-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                <div>
                  <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Original Caption</span>
                  <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-on-surface)' }}>{currentBenchmark.caption_bias.original_caption}</p>
                  {(currentBenchmark.caption_bias as unknown as Record<string, unknown>).original_caption_english && (currentBenchmark.caption_bias as unknown as Record<string, unknown>).original_caption_english !== currentBenchmark.caption_bias.original_caption && (
                    <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-on-surface)', opacity: 0.6 }}>
                      <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                      {(currentBenchmark.caption_bias as unknown as Record<string, unknown>).original_caption_english as string}
                    </p>
                  )}
                </div>
                <div>
                  <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Modified Caption</span>
                  <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-error)' }}>{currentBenchmark.caption_bias.modified_caption}</p>
                  {(currentBenchmark.caption_bias as unknown as Record<string, unknown>).modified_caption_english && (currentBenchmark.caption_bias as unknown as Record<string, unknown>).modified_caption_english !== currentBenchmark.caption_bias.modified_caption && (
                    <p className="text-xs leading-relaxed mt-1" style={{ color: 'var(--m3-error)', opacity: 0.6 }}>
                      <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                      {(currentBenchmark.caption_bias as unknown as Record<string, unknown>).modified_caption_english as string}
                    </p>
                  )}
                </div>
                {currentBenchmark.caption_bias.modifications && currentBenchmark.caption_bias.modifications.length > 0 && (
                  <div>
                    <span className="text-[10px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Modifications</span>
                    <div className="space-y-2 mt-2">
                      {currentBenchmark.caption_bias.modifications.map((mod, i) => (
                        <div key={i} className="rounded-lg p-3" style={{ backgroundColor: 'var(--m3-surface-container-high)', border: `1px solid var(--m3-outline-variant)` }}>
                          <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>
                            <span style={{ color: 'var(--m3-error)' }}>{mod.claim}</span>
                          </p>
                          {(mod as unknown as Record<string, unknown>).claim_english && (mod as unknown as Record<string, unknown>).claim_english !== mod.claim && (
                            <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-error)', opacity: 0.6 }}>
                              <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                              {(mod as unknown as Record<string, unknown>).claim_english as string as any}
                            </p>
                          )}
                          <p className="text-[11px] mt-1" style={{ color: 'var(--m3-on-surface-variant)' }}>
                            Reality: {mod.reality}
                          </p>
                          {(mod as unknown as Record<string, unknown>).reality_english && (mod as unknown as Record<string, unknown>).reality_english !== mod.reality && (
                            <p className="text-[11px]" style={{ color: 'var(--m3-on-surface-variant)', opacity: 0.6 }}>
                              <span className="text-[10px] font-medium uppercase" style={{ letterSpacing: '0.5px' }}>EN: </span>
                              {(mod as unknown as Record<string, unknown>).reality_english as string as any}
                            </p>
                          )}
                          <span className="text-[10px] px-2 py-0.5 rounded-full mt-1 inline-block" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-outline)' }}>
                            {mod.principle}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CollapsibleSection>
          )}

          {/* Annotations (non-adversarial) */}
          {!isAdversarial && currentFigureData?.annotations && (
            <CollapsibleSection title="Groundtruth Annotations" count={currentFigureData.annotations.length} defaultOpen>
              <div className="space-y-4">
                {currentFigureData.annotations.map((ann, idx) => (
                  <div key={idx} className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' }}>
                        {ann.annotation_language}
                      </span>
                      <span className="text-[10px]" style={{ color: 'var(--m3-outline)' }}>Annotator {ann.annotated_by}</span>
                    </div>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.25px' }}>
                      {ann.annotation}
                    </p>
                  </div>
                ))}
              </div>
            </CollapsibleSection>
          )}

          {/* Atomic MQM Checklist */}
          {atomsData && atomsData[selectedFigure] && (() => {
            const figAtoms = atomsData[selectedFigure]
            const severityColor = (sev: string) => {
              if (sev === 'critical') return { bg: 'var(--m3-error-container)', text: 'var(--m3-on-error-container)' }
              if (sev === 'important') return { bg: 'var(--m3-tertiary-container)', text: 'var(--m3-on-tertiary-container)' }
              return { bg: 'var(--m3-surface-container-highest)', text: 'var(--m3-on-surface-variant)' }
            }
            return (
              <CollapsibleSection title="Atomic MQM Checklist" count={figAtoms.atom_count}>
                {figAtoms.reference_description && (
                  <div className="rounded-lg p-4 mb-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: '1px solid var(--m3-outline-variant)' }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-medium uppercase px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>
                        Groundtruth Reference
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.25px', whiteSpace: 'pre-wrap' }}>
                      {figAtoms.reference_description}
                    </p>
                  </div>
                )}
                <div className="rounded-xl overflow-hidden" style={{ border: '1px solid var(--m3-outline-variant)', backgroundColor: 'var(--m3-surface-container)' }}>
                  <table className="w-full text-sm">
                    <thead>
                      <tr style={{ borderBottom: '1px solid var(--m3-outline-variant)' }}>
                        <th className="text-left px-4 py-3 text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px', width: '120px' }}>ID</th>
                        <th className="text-left px-4 py-3 text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px', width: '80px' }}>Severity</th>
                        <th className="text-left px-4 py-3 text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {figAtoms.atoms.map((atom: any, i: number) => {
                        const sc = severityColor(atom.severity)
                        return (
                          <tr key={atom.id} style={{ borderBottom: i < figAtoms.atoms.length - 1 ? '1px solid var(--m3-outline-variant)' : 'none' }}>
                            <td className="px-4 py-3 text-xs font-mono" style={{ color: 'var(--m3-on-surface-variant)', verticalAlign: 'top' }}>{atom.id}</td>
                            <td className="px-4 py-3" style={{ verticalAlign: 'top' }}>
                              <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: sc.bg, color: sc.text, letterSpacing: '0.3px' }}>{atom.severity}</span>
                            </td>
                            <td className="px-4 py-3 text-sm leading-relaxed" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.25px' }}>{atom.value}</td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </CollapsibleSection>
            )
          })()}
        </div>
      </div>

      {/* Fullscreen image modal */}
      {expandedImage && (
        <div
          className="fixed inset-0 z-50 flex flex-col items-center justify-center"
          style={{ backgroundColor: 'rgba(0,0,0,0.85)' }}
          onClick={() => setExpandedImage(null)}
          onKeyDown={e => { if (e.key === 'Escape') setExpandedImage(null) }}
          tabIndex={0}
          ref={el => el?.focus()}
        >
          <div className="absolute top-4 left-0 right-0 flex items-center justify-between px-6">
            <span className="text-sm font-medium text-white/90">{expandedImage.label}</span>
            <button
              onClick={() => setExpandedImage(null)}
              className="w-10 h-10 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
            </button>
          </div>
          <img
            src={expandedImage.src}
            alt={expandedImage.label}
            className="max-h-[90vh] max-w-[95vw] object-contain"
            onClick={e => e.stopPropagation()}
            style={{ display: 'block' }}
          />
        </div>
      )}
    </div>
  )
}
