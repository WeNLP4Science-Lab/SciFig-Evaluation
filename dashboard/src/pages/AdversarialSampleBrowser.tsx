import { useState, useEffect, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL, QUESTIONS_BLOB_URL, QUESTIONS_BLOB_WRITE_URL, HALLUCINATION_BLOB_URL, HALLUCINATION_BLOB_WRITE_URL } from '../config'
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

interface FigureQuestions {
  figure_key: string
  subfolder: string
  native_language: string
  questions_native: Question[]
  questions_english: Question[]
  questions_bg?: Question[]
  questions_cn?: Question[]
  questions_de?: Question[]
  questions_en?: Question[]
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

interface FigureHallucination {
  figure_key: string
  subfolder: string
  native_language: string
  probes_native: HallucinationProbe[]
  probes_english: HallucinationProbe[]
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
          <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-surface)' }}>{q.question}</p>
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
  const [questionsData, setQuestionsData] = useState<Record<string, FigureQuestions> | null>(null)
  const [halluData, setHalluData] = useState<Record<string, FigureHallucination> | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSubfolder, setSelectedSubfolder] = useState('')
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedTransform, setSelectedTransform] = useState<string | null>(null)
  const [expandedImage, setExpandedImage] = useState<{ src: string; label: string } | null>(null)
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<string | null>(null)
  const { isDark } = useTheme()

  const isAdversarial = manifest?.transforms != null

  useEffect(() => {
    setLoading(true)
    const loadQuestions = () =>
      fetch(`${QUESTIONS_BLOB_URL}?t=${Date.now()}`).then(r => r.ok ? r.json() : Promise.reject())
        .catch(() => fetch(`${import.meta.env.BASE_URL}data/capability_questions.json`).then(r => r.json()))
        .catch(() => null)

    const loadHallucination = () =>
      fetch(`${HALLUCINATION_BLOB_URL}?t=${Date.now()}`).then(r => r.ok ? r.json() : Promise.reject())
        .catch(() => fetch(`${import.meta.env.BASE_URL}data/hallucination_probes.json`).then(r => r.json()))
        .catch(() => null)

    Promise.all([
      fetch(`${import.meta.env.BASE_URL}data/${manifestFile}`).then(r => r.json()),
      loadQuestions(),
      loadHallucination(),
    ])
      .then(([manifestData, questionsJson, halluJson]) => {
        setManifest(manifestData as SampleManifest)
        if (questionsJson) setQuestionsData(questionsJson as Record<string, FigureQuestions>)
        if (halluJson) setHalluData(halluJson as Record<string, FigureHallucination>)
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

  const currentQuestions = useMemo(() => {
    if (!questionsData || !selectedFigure) return null
    return questionsData[selectedFigure] || null
  }, [questionsData, selectedFigure])

  const currentHallucination = useMemo(() => {
    if (!halluData || !selectedFigure) return null
    return halluData[selectedFigure] || null
  }, [halluData, selectedFigure])

  const handleQuestionUpdate = useCallback((langKey: string, qIndex: number, updated: Question) => {
    if (!questionsData || !selectedFigure) return
    const newData = { ...questionsData }
    const figQ = { ...newData[selectedFigure] }
    const arr = [...((figQ as Record<string, unknown>)[langKey] as Question[])]
    arr[qIndex] = updated
    ;(figQ as Record<string, unknown>)[langKey] = arr
    newData[selectedFigure] = figQ as FigureQuestions
    setQuestionsData(newData)
  }, [questionsData, selectedFigure])

  const handleSaveAll = useCallback(async () => {
    if (!questionsData && !halluData) return
    setSaving(true)
    setSaveStatus(null)
    try {
      const uploads: Promise<Response>[] = []
      if (questionsData) {
        uploads.push(fetch(QUESTIONS_BLOB_WRITE_URL, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'x-ms-blob-type': 'BlockBlob' },
          body: JSON.stringify(questionsData, null, 2),
        }))
      }
      if (halluData) {
        uploads.push(fetch(HALLUCINATION_BLOB_WRITE_URL, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'x-ms-blob-type': 'BlockBlob' },
          body: JSON.stringify(halluData, null, 2),
        }))
      }
      const results = await Promise.all(uploads)
      if (results.every(r => r.ok)) {
        setSaveStatus('Saved')
      } else {
        setSaveStatus(`Error: some saves failed`)
      }
    } catch (e) {
      setSaveStatus(`Error: ${e}`)
    } finally {
      setSaving(false)
      setTimeout(() => setSaveStatus(null), 3000)
    }
  }, [questionsData])

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

  const isMultiLang = selectedSubfolder === 'multi_language'

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

          {/* Capability Questions (collapsible) */}
          {isAdversarial && currentQuestions && (
            <>
              <CollapsibleSection title={`Questions — Native (${currentQuestions.native_language})`} count={currentQuestions.questions_native?.length}>
                <div className="space-y-3">
                  {currentQuestions.questions_native?.map((q, i) => (
                    <EditableQuestionCard
                      key={q.id}
                      q={q}
                      langLabel={currentQuestions.native_language}
                      onChange={updated => handleQuestionUpdate('questions_native', i, updated)}
                    />
                  ))}
                </div>
              </CollapsibleSection>

              <CollapsibleSection title="Questions — English" count={currentQuestions.questions_english?.length}>
                <div className="space-y-3">
                  {currentQuestions.questions_english?.map((q, i) => (
                    <EditableQuestionCard
                      key={q.id}
                      q={q}
                      langLabel="english"
                      onChange={updated => handleQuestionUpdate('questions_english', i, updated)}
                    />
                  ))}
                </div>
              </CollapsibleSection>

              {/* Multi-language extra languages */}
              {isMultiLang && currentQuestions.questions_bg && (
                <CollapsibleSection title="Questions — Bulgarian" count={currentQuestions.questions_bg.length}>
                  <div className="space-y-3">
                    {currentQuestions.questions_bg.map((q, i) => (
                      <EditableQuestionCard
                        key={q.id}
                        q={q}
                        langLabel="bulgarian"
                        onChange={updated => handleQuestionUpdate('questions_bg', i, updated)}
                      />
                    ))}
                  </div>
                </CollapsibleSection>
              )}
              {isMultiLang && currentQuestions.questions_cn && (
                <CollapsibleSection title="Questions — Chinese" count={currentQuestions.questions_cn.length}>
                  <div className="space-y-3">
                    {currentQuestions.questions_cn.map((q, i) => (
                      <EditableQuestionCard
                        key={q.id}
                        q={q}
                        langLabel="chinese"
                        onChange={updated => handleQuestionUpdate('questions_cn', i, updated)}
                      />
                    ))}
                  </div>
                </CollapsibleSection>
              )}
              {isMultiLang && currentQuestions.questions_de && (
                <CollapsibleSection title="Questions — German" count={currentQuestions.questions_de.length}>
                  <div className="space-y-3">
                    {currentQuestions.questions_de.map((q, i) => (
                      <EditableQuestionCard
                        key={q.id}
                        q={q}
                        langLabel="german"
                        onChange={updated => handleQuestionUpdate('questions_de', i, updated)}
                      />
                    ))}
                  </div>
                </CollapsibleSection>
              )}
            </>
          )}

          {/* Hallucination Probes (collapsible) */}
          {isAdversarial && currentHallucination && (
            <>
              <CollapsibleSection title={`Hallucination Probes — Native (${currentHallucination.native_language})`} count={currentHallucination.probes_native?.length}>
                <div className="space-y-3">
                  {currentHallucination.probes_native?.map((p) => (
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
                      <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-surface)' }}>{p.question}</p>
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

              <CollapsibleSection title="Hallucination Probes — English" count={currentHallucination.probes_english?.length}>
                <div className="space-y-3">
                  {currentHallucination.probes_english?.map((p) => (
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
                      <p className="text-xs leading-relaxed mb-2" style={{ color: 'var(--m3-on-surface)' }}>{p.question}</p>
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
            </>
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
