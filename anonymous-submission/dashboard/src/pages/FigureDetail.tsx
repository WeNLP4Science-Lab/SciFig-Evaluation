import { useState, useEffect, useCallback } from 'react'
import { getAnnotations, saveAnnotation, getReviews, saveReview, type AuthState, type AnnotationEntry, type ReviewEntry } from '../auth'

/* ── Types ── */

interface FigureEntry {
  id: string
  figure_type: string
  caption: string
  paper_title: string
  arxiv_id: string
  annotation_count: number
  annotations: string[]
}

interface CapabilityQuestion {
  question: string
  answer: string | number
  answer_type: string
  acceptable_range?: [number, number]
  category: string
  reasoning: string
  visual_elements: string[]
  difficulty?: string
  figure_dependent?: boolean
}

interface CapabilityData {
  figure_id: string
  figure_type: string
  questions: CapabilityQuestion[]
}

interface ProbeTarget {
  blurred_text: string
  question: string
  why_unrecoverable?: string
  reasoning_path?: string
  why_inferable?: string
  expected_behavior: string
}

interface ProbeData {
  figure_id: string
  selective_blur: {
    admittance?: ProbeTarget
    inductance?: ProbeTarget
  }
  ocr_texts?: string[]
}

const c = {
  bg: '#09090b',
  surface: '#131316',
  surfaceHover: '#1c1c21',
  surfaceActive: '#232329',
  surfaceRaised: '#18181b',
  border: 'rgba(255,255,255,0.06)',
  borderStrong: 'rgba(255,255,255,0.1)',
  fg: '#fafafa',
  muted: '#a1a1aa',
  dim: '#52525b',
  accent: '#3b82f6',
}

const TYPE_DOT: Record<string, string> = {
  'Bar Chart': '#f59e0b',
  'Line Plot': '#3b82f6',
  'Pie Chart': '#8b5cf6',
}
const TYPE_BG: Record<string, string> = {
  'Bar Chart': 'rgba(245,158,11,0.1)',
  'Line Plot': 'rgba(59,130,246,0.1)',
  'Pie Chart': 'rgba(139,92,246,0.1)',
}

const CAT_COLORS: Record<string, { dot: string; bg: string }> = {
  counting:         { dot: '#f59e0b', bg: 'rgba(245,158,11,0.1)' },
  computation:      { dot: '#3b82f6', bg: 'rgba(59,130,246,0.1)' },
  comparison:       { dot: '#8b5cf6', bg: 'rgba(139,92,246,0.1)' },
  pattern_analysis: { dot: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
}

const CAT_LABELS: Record<string, string> = {
  counting: 'Counting',
  computation: 'Computation',
  comparison: 'Comparison',
  pattern_analysis: 'Pattern Analysis',
}

/* ── Main ── */

export default function FigureDetail({ figureId, onBack, auth }: {
  figureId: string
  onBack: () => void
  auth: AuthState | null
}) {
  const [figure, setFigure] = useState<FigureEntry | null>(null)
  const [capability, setCapability] = useState<CapabilityData | null>(null)
  const [probe, setProbe] = useState<ProbeData | null>(null)
  const [activeTab, setActiveTab] = useState<'info' | 'questions' | 'adversarial'>('info')
  const [annIdx, setAnnIdx] = useState(0)
  const [expandedQ, setExpandedQ] = useState<number | null>(null)
  const [annotations, setAnnotations] = useState<AnnotationEntry[]>([])
  const [reviews, setReviews] = useState<ReviewEntry[]>([])

  const loadAnnotations = useCallback(() => {
    if (auth) {
      getAnnotations(figureId).then(setAnnotations).catch(() => {})
      getReviews(figureId).then(setReviews).catch(() => {})
    }
  }, [figureId, auth])

  useEffect(() => {
    fetch('/manifest.json')
      .then(r => r.json())
      .then((data: FigureEntry[]) => {
        const fig = data.find(d => d.id === figureId)
        if (fig) setFigure(fig)
      })
    fetch(`/capability_questions/${figureId}.json`)
      .then(r => { if (r.ok) return r.json(); return null })
      .then(d => { if (d) setCapability(d) })
      .catch(() => {})
    fetch(`/probes/${figureId}.json`)
      .then(r => { if (r.ok) return r.json(); return null })
      .then(d => { if (d) setProbe(d) })
      .catch(() => {})
    loadAnnotations()
  }, [figureId])

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape') onBack() }
    document.addEventListener('keydown', h)
    return () => document.removeEventListener('keydown', h)
  }, [onBack])

  if (!figure) return null

  const dot = TYPE_DOT[figure.figure_type] || '#888'
  const bg = TYPE_BG[figure.figure_type] || 'rgba(136,136,136,0.1)'

  return (
    <div style={{ minHeight: '100vh', animation: 'fadeIn 0.25s ease-out both' }}>
      {/* ── Top Bar ── */}
      <div style={{
        position: 'sticky', top: 0, zIndex: 20,
        borderBottom: `1px solid ${c.border}`,
        background: 'rgba(9,9,11,0.92)', backdropFilter: 'blur(12px)',
      }}>
        <div className="page-container" style={{
          height: 48, display: 'flex', alignItems: 'center', gap: 12,
        }}>
          <button
            onClick={onBack}
            style={{
              display: 'flex', alignItems: 'center', gap: 6,
              background: 'none', border: 'none', cursor: 'pointer',
              color: c.muted, fontSize: 13, fontFamily: 'inherit',
              padding: '4px 0', transition: 'color 0.15s',
            }}
            onMouseEnter={e => e.currentTarget.style.color = c.fg}
            onMouseLeave={e => e.currentTarget.style.color = c.muted}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10 3L5 8l5 5" />
            </svg>
            Dataset
          </button>

          <span style={{ color: c.dim, fontSize: 12 }}>/</span>

          <span style={{
            fontSize: 13, fontFamily: 'JetBrains Mono, monospace',
            fontWeight: 600, color: c.fg,
          }}>
            {figureId}
          </span>

          <span style={{
            fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.04em', padding: '3px 8px', borderRadius: 4,
            color: dot, background: bg, lineHeight: 1,
          }}>
            {figure.figure_type}
          </span>
        </div>
      </div>

      {/* ── Content ── */}
      <div className="page-container" style={{ paddingTop: 32, paddingBottom: 48 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 420px', gap: 32 }}>

          {/* Left: Figure Image */}
          <div>
            <div style={{
              borderRadius: 12, border: `1px solid ${c.border}`,
              background: c.surface, padding: 24,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              minHeight: 400,
            }}>
              <img
                src={`/figures/${figureId}.png`}
                alt={figure.caption || figureId}
                style={{ maxWidth: '100%', maxHeight: '60vh', objectFit: 'contain' }}
              />
            </div>

            {/* Paper info below image */}
            {figure.paper_title && (
              <div style={{ marginTop: 16 }}>
                <p style={{ fontSize: 14, color: c.fg, lineHeight: 1.6 }}>
                  {figure.paper_title}
                </p>
                {figure.arxiv_id && (
                  <p style={{
                    fontSize: 11, color: c.dim, fontFamily: 'JetBrains Mono, monospace',
                    marginTop: 4,
                  }}>
                    {figure.arxiv_id}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Right: Tabs Panel */}
          <div>
            {/* Tab Headers */}
            <div style={{
              display: 'flex', gap: 0,
              borderBottom: `1px solid ${c.border}`, marginBottom: 20,
            }}>
              <TabButton
                label="Information"
                active={activeTab === 'info'}
                onClick={() => setActiveTab('info')}
              />
              <TabButton
                label={`Capability Questions${capability ? ` (${capability.questions.length})` : ''}`}
                active={activeTab === 'questions'}
                onClick={() => setActiveTab('questions')}
                badge={capability ? capability.questions.length : undefined}
              />
              <TabButton
                label="Adversarial"
                active={activeTab === 'adversarial'}
                onClick={() => setActiveTab('adversarial')}
              />
            </div>

            {/* Tab Content */}
            {activeTab === 'info' && (
              <div style={{ animation: 'fadeIn 0.2s ease-out both' }}>
                {/* Annotations */}
                {figure.annotations.length > 0 && (
                  <Section label={`Annotations (${figure.annotations.length})`}>
                    {figure.annotations.length > 1 && (
                      <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
                        {figure.annotations.map((_, i) => (
                          <button
                            key={i}
                            onClick={() => setAnnIdx(i)}
                            style={{
                              height: 26, minWidth: 32, padding: '0 10px',
                              borderRadius: 6, fontSize: 11, fontWeight: 500,
                              fontFamily: 'inherit', cursor: 'pointer',
                              background: annIdx === i ? 'rgba(59,130,246,0.12)' : c.surface,
                              color: annIdx === i ? c.accent : c.dim,
                              border: annIdx === i ? '1px solid rgba(59,130,246,0.25)' : `1px solid ${c.border}`,
                              transition: 'all 0.15s ease',
                            }}
                          >
                            Annotator {i + 1}
                          </button>
                        ))}
                      </div>
                    )}
                    <div style={{
                      borderRadius: 8, background: c.surfaceRaised,
                      border: `1px solid ${c.border}`, padding: 16,
                    }}>
                      <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.8, margin: 0 }}>
                        {figure.annotations[annIdx]}
                      </p>
                    </div>
                  </Section>
                )}

                {/* Paper & Caption */}
                {figure.paper_title && (
                  <Section label="Paper">
                    <p style={{ fontSize: 13, color: c.fg, lineHeight: 1.6, margin: 0 }}>
                      {figure.paper_title}
                    </p>
                  </Section>
                )}

                {figure.caption && (
                  <Section label="Caption">
                    <div style={{
                      borderRadius: 8, background: c.surfaceRaised,
                      border: `1px solid ${c.border}`, padding: 12,
                    }}>
                      <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.7, margin: 0, fontStyle: 'italic' }}>
                        {figure.caption}
                      </p>
                    </div>
                  </Section>
                )}

                {/* Metadata */}
                <Section label="Metadata">
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                    <MetaItem label="Chart Type" value={figure.figure_type} />
                    <MetaItem label="Figure Number" value={(figure as FigureEntry & { figure_number?: string }).figure_number || '—'} />
                    {figure.arxiv_id ? (
                      <div style={{
                        borderRadius: 6, border: `1px solid ${c.border}`,
                        background: c.surfaceRaised, padding: '8px 12px',
                      }}>
                        <p style={{ fontSize: 9, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', color: c.dim, margin: '0 0 3px' }}>
                          arXiv
                        </p>
                        <a
                          href={`https://arxiv.org/pdf/${figure.arxiv_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ fontSize: 12, color: c.accent, fontFamily: 'JetBrains Mono, monospace', textDecoration: 'none' }}
                          onMouseEnter={e => (e.currentTarget.style.textDecoration = 'underline')}
                          onMouseLeave={e => (e.currentTarget.style.textDecoration = 'none')}
                        >
                          {figure.arxiv_id}
                        </a>
                      </div>
                    ) : (
                      <MetaItem label="arXiv" value="—" />
                    )}
                    {(figure as FigureEntry & { pdf_page?: number }).pdf_page && (
                      <MetaItem label="PDF Page" value={String((figure as FigureEntry & { pdf_page?: number }).pdf_page)} />
                    )}
                  </div>
                </Section>

                {/* Editable metadata — annotation mode only */}
                {auth && (
                  <MetadataEditor
                    figureId={figureId}
                    auth={auth}
                    currentPage={(figure as FigureEntry & { pdf_page?: number }).pdf_page}
                    currentCaption={figure.caption}
                    reviews={reviews}
                    onSaved={loadAnnotations}
                  />
                )}
              </div>
            )}

            {activeTab === 'questions' && (
              <div style={{ animation: 'fadeIn 0.2s ease-out both' }}>
                {capability && capability.questions.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {capability.questions.map((q, i) => (
                      <QuestionCard
                        key={i}
                        question={q}
                        index={i}
                        expanded={expandedQ === i}
                        onToggle={() => setExpandedQ(expandedQ === i ? null : i)}
                        auth={auth}
                        figureId={figureId}
                        annotations={annotations.filter(a => a.category === q.category)}
                        onSaved={loadAnnotations}
                      />
                    ))}
                  </div>
                ) : (
                  <div style={{
                    textAlign: 'center', padding: '48px 0',
                    color: c.dim, fontSize: 13,
                  }}>
                    No capability questions generated yet
                  </div>
                )}
              </div>
            )}

            {activeTab === 'adversarial' && (
              <div style={{ animation: 'fadeIn 0.2s ease-out both' }}>
                {probe && probe.selective_blur ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                    {/* Admittance */}
                    {probe.selective_blur.admittance && (
                      <BlurCard
                        type="admittance"
                        label="Admittance Test"
                        description="Model should honestly admit it cannot determine the blurred information"
                        figureId={figureId}
                        target={probe.selective_blur.admittance}
                        accentColor="#ef4444"
                        accentBg="rgba(239,68,68,0.08)"
                        auth={auth}
                        reviews={reviews}
                        onSaved={loadAnnotations}
                        ocrTexts={probe.ocr_texts || []}
                      />
                    )}

                    {/* Inductance */}
                    {probe.selective_blur.inductance && (
                      <BlurCard
                        type="inductance"
                        label="Inductance Test"
                        description="Model should attempt to infer from remaining visual context"
                        figureId={figureId}
                        target={probe.selective_blur.inductance}
                        accentColor="#22c55e"
                        accentBg="rgba(34,197,94,0.08)"
                        auth={auth}
                        reviews={reviews}
                        onSaved={loadAnnotations}
                        ocrTexts={probe.ocr_texts || []}
                      />
                    )}

                    {!probe.selective_blur.admittance && !probe.selective_blur.inductance && (
                      <div style={{ textAlign: 'center', padding: '48px 0', color: c.dim, fontSize: 13 }}>
                        No adversarial probes generated for this figure
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{ textAlign: 'center', padding: '48px 0', color: c.dim, fontSize: 13 }}>
                    No adversarial data available
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── Blur Card ── */

function BlurCard({ type, label, description, figureId, target, accentColor, accentBg, auth, reviews, onSaved, ocrTexts }: {
  type: 'admittance' | 'inductance'
  label: string
  description: string
  figureId: string
  target: ProbeTarget
  accentColor: string
  accentBg: string
  auth: AuthState | null
  reviews: ReviewEntry[]
  onSaved: () => void
  ocrTexts: string[]
}) {
  const [showBlurred, setShowBlurred] = useState(false)
  const [showReview, setShowReview] = useState(false)
  const [status, setStatus] = useState('')
  const [newTarget, setNewTarget] = useState('')
  const [newQuestion, setNewQuestion] = useState('')
  const [notes, setNotes] = useState('')
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  const reviewKey = `blur_${type}`
  const existingReview = reviews.find(r => r.review_type === reviewKey && r.annotator === auth?.name)

  // Load existing review
  useEffect(() => {
    if (existingReview) {
      setStatus(existingReview.status || '')
      setNewTarget(existingReview.new_blur_target || '')
      setNewQuestion(existingReview.new_question || '')
      setNotes(existingReview.notes || '')
    }
  }, [existingReview?.timestamp])

  const handleSaveReview = async () => {
    if (!auth || !status) return
    setSaving(true)
    await saveReview({
      figure_id: figureId,
      annotator: auth.name,
      password: auth.password,
      review_type: reviewKey,
      probe_type: type,
      status,
      new_blur_target: newTarget || undefined,
      new_question: newQuestion || undefined,
      notes: notes || undefined,
    })
    setSaving(false)
    setSaved(true)
    onSaved()
    setTimeout(() => setSaved(false), 2000)
  }

  const imgSrc = type === 'admittance'
    ? `/adversarial_admittance/${figureId}.png`
    : `/adversarial_inductance/${figureId}.png`

  return (
    <div style={{
      borderRadius: 10, border: `1px solid ${c.border}`,
      background: c.surface, overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '14px 16px',
        borderBottom: `1px solid ${c.border}`,
        display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <span style={{
          width: 8, height: 8, borderRadius: '50%',
          background: accentColor, flexShrink: 0,
        }} />
        <div style={{ flex: 1 }}>
          <p style={{ fontSize: 13, fontWeight: 600, color: c.fg, margin: 0 }}>{label}</p>
          <p style={{ fontSize: 11, color: c.dim, margin: '2px 0 0' }}>{description}</p>
        </div>
      </div>

      {/* Blurred image toggle */}
      <div style={{ padding: '16px', borderBottom: `1px solid ${c.border}` }}>
        <div style={{
          display: 'flex', gap: 4, marginBottom: 12,
        }}>
          <button
            onClick={() => setShowBlurred(false)}
            style={{
              padding: '5px 12px', borderRadius: 5, fontSize: 11, fontWeight: 500,
              fontFamily: 'inherit', cursor: 'pointer',
              background: !showBlurred ? c.surfaceActive : c.surfaceRaised,
              color: !showBlurred ? c.fg : c.dim,
              border: `1px solid ${!showBlurred ? c.borderStrong : c.border}`,
              transition: 'all 0.15s',
            }}
          >
            Original
          </button>
          <button
            onClick={() => setShowBlurred(true)}
            style={{
              padding: '5px 12px', borderRadius: 5, fontSize: 11, fontWeight: 500,
              fontFamily: 'inherit', cursor: 'pointer',
              background: showBlurred ? accentBg : c.surfaceRaised,
              color: showBlurred ? accentColor : c.dim,
              border: `1px solid ${showBlurred ? accentColor + '40' : c.border}`,
              transition: 'all 0.15s',
            }}
          >
            Blurred
          </button>
        </div>
        <div style={{
          borderRadius: 8, background: c.bg, border: `1px solid ${c.border}`,
          padding: 12, display: 'flex', alignItems: 'center', justifyContent: 'center',
          minHeight: 160,
        }}>
          <img
            src={showBlurred ? imgSrc : `/figures/${figureId}.png`}
            alt={showBlurred ? `${type} blur` : 'original'}
            style={{ maxWidth: '100%', maxHeight: '40vh', objectFit: 'contain' }}
          />
        </div>
      </div>

      {/* Details */}
      <div style={{ padding: '14px 16px' }}>
        {/* Blurred text */}
        <div style={{ marginBottom: 14 }}>
          <p style={{
            fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
          }}>
            Blurred Element
          </p>
          <span style={{
            display: 'inline-block', padding: '4px 10px', borderRadius: 5,
            background: accentBg, border: `1px solid ${accentColor}30`,
            fontSize: 12, fontWeight: 600, color: accentColor,
            fontFamily: 'JetBrains Mono, monospace',
          }}>
            {target.blurred_text}
          </span>
        </div>

        {/* Question */}
        <div style={{ marginBottom: 14 }}>
          <p style={{
            fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
          }}>
            Evaluation Question
          </p>
          <div style={{
            borderRadius: 8, background: c.surfaceRaised,
            border: `1px solid ${c.border}`, padding: 12,
          }}>
            <p style={{ fontSize: 13, color: c.fg, lineHeight: 1.6, margin: 0 }}>
              {target.question}
            </p>
          </div>
        </div>

        {/* Reasoning (inductance only) */}
        {target.reasoning_path && (
          <div>
            <p style={{
              fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
            }}>
              Reasoning Path
            </p>
            <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.6, margin: 0 }}>
              {target.reasoning_path}
            </p>
          </div>
        )}

        {/* Why (admittance) */}
        {target.why_unrecoverable && (
          <div>
            <p style={{
              fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
            }}>
              Why Unrecoverable
            </p>
            <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.6, margin: 0 }}>
              {target.why_unrecoverable}
            </p>
          </div>
        )}

        {/* Review controls — annotation mode */}
        {auth && (
          <div style={{ marginTop: 16, paddingTop: 14, borderTop: `1px solid ${c.border}` }}>
            {!showReview ? (
              <button
                onClick={() => setShowReview(true)}
                style={{
                  padding: '6px 14px', borderRadius: 6, fontSize: 11, fontWeight: 500,
                  fontFamily: 'inherit', cursor: 'pointer',
                  background: existingReview ? (existingReview.status === 'approved' ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)') : c.surfaceRaised,
                  color: existingReview ? (existingReview.status === 'approved' ? '#22c55e' : '#ef4444') : c.muted,
                  border: `1px solid ${c.border}`,
                }}
              >
                {existingReview ? (existingReview.status === 'approved' ? 'Approved' : 'Rejected — Edit') : 'Review This'}
              </button>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <div style={{ display: 'flex', gap: 6 }}>
                  {['approved', 'rejected'].map(s => (
                    <button
                      key={s}
                      onClick={() => setStatus(s)}
                      style={{
                        padding: '5px 14px', borderRadius: 6, fontSize: 11, fontWeight: 500,
                        fontFamily: 'inherit', cursor: 'pointer',
                        background: status === s ? (s === 'approved' ? 'rgba(34,197,94,0.15)' : 'rgba(239,68,68,0.15)') : c.surfaceRaised,
                        color: status === s ? (s === 'approved' ? '#22c55e' : '#ef4444') : c.dim,
                        border: `1px solid ${status === s ? (s === 'approved' ? '#22c55e40' : '#ef444440') : c.border}`,
                      }}
                    >
                      {s === 'approved' ? 'Approve' : 'Reject'}
                    </button>
                  ))}
                </div>
                {status === 'rejected' && (
                  <>
                    <div>
                      <p style={{
                        fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                        letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
                      }}>
                        Select New Target
                      </p>
                      <div style={{
                        maxHeight: 140, overflowY: 'auto', borderRadius: 6,
                        border: `1px solid ${c.border}`, background: c.bg,
                      }}>
                        {ocrTexts.map((text, i) => (
                          <button
                            key={i}
                            onClick={() => setNewTarget(text)}
                            style={{
                              display: 'block', width: '100%', textAlign: 'left',
                              padding: '6px 10px', border: 'none', cursor: 'pointer',
                              fontFamily: 'inherit', fontSize: 11,
                              background: newTarget === text ? accentBg : 'transparent',
                              color: newTarget === text ? accentColor : c.muted,
                              borderBottom: i < ocrTexts.length - 1 ? `1px solid ${c.border}` : 'none',
                              transition: 'background 0.1s',
                            }}
                            onMouseEnter={e => { if (newTarget !== text) e.currentTarget.style.background = c.surfaceHover }}
                            onMouseLeave={e => { if (newTarget !== text) e.currentTarget.style.background = 'transparent' }}
                          >
                            {text}
                          </button>
                        ))}
                      </div>
                      {newTarget && (
                        <p style={{ fontSize: 11, color: accentColor, margin: '6px 0 0' }}>
                          Selected: <strong>{newTarget}</strong>
                        </p>
                      )}
                    </div>
                    <div>
                      <p style={{
                        fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                        letterSpacing: '0.06em', color: c.dim, margin: '0 0 4px',
                      }}>
                        New Question
                      </p>
                      <input
                        value={newQuestion}
                        onChange={e => setNewQuestion(e.target.value)}
                        placeholder="Write evaluation question for the new target..."
                        style={{
                          width: '100%', padding: '7px 10px', borderRadius: 6, fontSize: 12,
                          fontFamily: 'inherit', background: c.bg, border: `1px solid ${c.border}`,
                          color: c.fg, outline: 'none',
                        }}
                      />
                    </div>
                  </>
                )}
                <input
                  value={notes}
                  onChange={e => setNotes(e.target.value)}
                  placeholder="Notes (optional)..."
                  style={{
                    width: '100%', padding: '7px 10px', borderRadius: 6, fontSize: 12,
                    fontFamily: 'inherit', background: c.bg, border: `1px solid ${c.border}`,
                    color: c.fg, outline: 'none',
                  }}
                />
                <div style={{ display: 'flex', gap: 6 }}>
                  <button
                    onClick={handleSaveReview}
                    disabled={!status || saving}
                    style={{
                      padding: '6px 16px', borderRadius: 6, border: 'none',
                      background: saved ? '#22c55e' : status ? c.accent : c.dim,
                      color: '#fff', fontSize: 11, fontWeight: 500, fontFamily: 'inherit',
                      cursor: status ? 'pointer' : 'default',
                    }}
                  >
                    {saving ? 'Saving...' : saved ? 'Saved' : 'Save Review'}
                  </button>
                  <button
                    onClick={() => setShowReview(false)}
                    style={{
                      padding: '6px 12px', borderRadius: 6, border: `1px solid ${c.border}`,
                      background: 'none', color: c.dim, fontSize: 11, fontFamily: 'inherit',
                      cursor: 'pointer',
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

/* ── Question Card ── */

function QuestionCard({ question, index, expanded, onToggle, auth, figureId, annotations, onSaved }: {
  question: CapabilityQuestion
  index: number
  expanded: boolean
  onToggle: () => void
  auth: AuthState | null
  figureId: string
  annotations: AnnotationEntry[]
  onSaved: () => void
}) {
  const cat = CAT_COLORS[question.category] || { dot: '#888', bg: 'rgba(136,136,136,0.1)' }
  const label = CAT_LABELS[question.category] || question.category

  return (
    <div style={{
      borderRadius: 10, border: `1px solid ${c.border}`,
      background: c.surface, overflow: 'hidden',
      transition: 'border-color 0.15s',
    }}>
      {/* Header — clickable */}
      <button
        onClick={onToggle}
        style={{
          width: '100%', display: 'flex', alignItems: 'flex-start', gap: 12,
          padding: '14px 16px', background: 'none', border: 'none',
          cursor: 'pointer', textAlign: 'left', fontFamily: 'inherit',
        }}
      >
        {/* Number */}
        <span style={{
          width: 22, height: 22, borderRadius: 6,
          background: cat.bg, color: cat.dot,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 11, fontWeight: 600, flexShrink: 0, marginTop: 1,
        }}>
          {index + 1}
        </span>

        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Category badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
            <span style={{
              fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.05em', color: cat.dot,
            }}>
              {label}
            </span>
          </div>
          {/* Question text */}
          <p style={{ fontSize: 13, color: c.fg, lineHeight: 1.55, margin: 0 }}>
            {question.question}
          </p>
        </div>

        {/* Expand arrow */}
        <svg
          width="16" height="16" viewBox="0 0 16 16"
          fill="none" stroke={c.dim} strokeWidth="1.5" strokeLinecap="round"
          style={{
            flexShrink: 0, marginTop: 2,
            transform: expanded ? 'rotate(180deg)' : 'rotate(0)',
            transition: 'transform 0.2s ease',
          }}
        >
          <path d="M4 6l4 4 4-4" />
        </svg>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div style={{
          padding: '0 16px 16px', paddingLeft: 50,
          animation: 'fadeIn 0.15s ease-out both',
        }}>
          {/* Annotation form — only in annotation mode */}
          {auth && (
            <AnnotationForm
              auth={auth}
              figureId={figureId}
              category={question.category}
              annotations={annotations}
              onSaved={onSaved}
            />
          )}
        </div>
      )}
    </div>
  )
}

/* ── Shared Components ── */

function TabButton({ label, active, onClick }: {
  label: string; active: boolean; onClick: () => void; badge?: number
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '10px 16px', background: 'none', border: 'none',
        borderBottom: active ? '2px solid #3b82f6' : '2px solid transparent',
        cursor: 'pointer', fontFamily: 'inherit',
        fontSize: 12, fontWeight: active ? 500 : 400,
        color: active ? c.fg : c.muted,
        transition: 'all 0.15s ease',
        marginBottom: -1,
      }}
    >
      {label}
    </button>
  )
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <p style={{
        fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: c.dim, margin: '0 0 10px',
        lineHeight: 1,
      }}>
        {label}
      </p>
      {children}
    </div>
  )
}

function MetaItem({ label, value }: { label: string; value: string }) {
  return (
    <div style={{
      borderRadius: 6, border: `1px solid ${c.border}`,
      background: c.surfaceRaised, padding: '8px 12px',
    }}>
      <p style={{ fontSize: 9, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', color: c.dim, margin: '0 0 3px' }}>
        {label}
      </p>
      <p style={{ fontSize: 12, color: c.fg, margin: 0, fontFamily: 'JetBrains Mono, monospace' }}>
        {value}
      </p>
    </div>
  )
}

/* ── Annotation Form ── */

function AnnotationForm({ auth, figureId, category, annotations, onSaved }: {
  auth: AuthState
  figureId: string
  category: string
  annotations: AnnotationEntry[]
  onSaved: () => void
}) {
  const isAdmin = auth.name === 'Admin'
  const myAnnotation = isAdmin ? undefined : annotations.find(a => a.annotator === auth.name)
  const otherAnnotations = isAdmin ? annotations : []

  const [answer, setAnswer] = useState(myAnnotation?.answer || '')
  const [editedQ, setEditedQ] = useState(myAnnotation?.edited_question || '')
  const [notes, setNotes] = useState(myAnnotation?.notes || '')
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    setSaved(false)
    const res = await saveAnnotation({
      figure_id: figureId,
      category,
      annotator: auth.name,
      password: auth.password,
      answer,
      edited_question: editedQ || undefined,
      notes: notes || undefined,
    })
    setSaving(false)
    if (res.ok) {
      setSaved(true)
      onSaved()
      setTimeout(() => setSaved(false), 2000)
    }
  }

  const inputStyle = {
    width: '100%', padding: '8px 10px', borderRadius: 6, fontSize: 12,
    fontFamily: 'inherit', background: c.bg, border: `1px solid ${c.border}`,
    color: c.fg, outline: 'none', marginTop: 6, resize: 'none' as const,
  }
  const labelStyle = {
    fontSize: 10, fontWeight: 600 as const, textTransform: 'uppercase' as const,
    letterSpacing: '0.06em', color: c.dim,
  }

  return (
    <div style={{
      marginTop: 16, paddingTop: 16,
      borderTop: `1px solid ${c.border}`,
    }}>
      {/* Annotation form — hidden for Admin */}
      {!isAdmin && (
        <>
          <p style={{ ...labelStyle, marginBottom: 8 }}>
            Your Annotation ({auth.name})
          </p>

          <div style={{ marginBottom: 12 }}>
            <label style={labelStyle}>Answer</label>
            <input
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              placeholder="Enter your answer..."
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: 12 }}>
            <label style={labelStyle}>Suggest Question Edit (optional)</label>
            <textarea
              value={editedQ}
              onChange={e => setEditedQ(e.target.value)}
              placeholder="Leave empty if question is fine. Otherwise, write your revised question..."
              rows={2}
              style={inputStyle}
            />
            {editedQ && (
              <div style={{
                marginTop: 6, padding: '6px 10px', borderRadius: 4,
                background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.2)',
              }}>
                <span style={{ fontSize: 9, fontWeight: 600, color: '#f59e0b', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Change Requested
                </span>
              </div>
            )}
          </div>

          <div style={{ marginBottom: 12 }}>
            <label style={labelStyle}>Notes (optional)</label>
            <textarea
              value={notes}
              onChange={e => setNotes(e.target.value)}
              placeholder="Any additional notes..."
              rows={1}
              style={inputStyle}
            />
          </div>

          <button
            onClick={handleSave}
        disabled={!answer || saving}
        style={{
          padding: '6px 16px', borderRadius: 6, border: 'none',
          background: saved ? '#22c55e' : answer ? '#3b82f6' : c.dim,
          color: '#fff', fontSize: 12, fontWeight: 500, fontFamily: 'inherit',
          cursor: answer ? 'pointer' : 'default',
          opacity: saving ? 0.6 : 1,
          transition: 'background 0.2s',
        }}
      >
        {saving ? 'Saving...' : saved ? 'Saved' : myAnnotation ? 'Update' : 'Save'}
      </button>
        </>
      )}

      {/* All annotations — admin only */}
      {isAdmin && otherAnnotations.length > 0 && (
        <div style={{ marginTop: isAdmin ? 0 : 20 }}>
          <p style={{ ...labelStyle, marginBottom: 8 }}>
            Annotations ({otherAnnotations.length})
          </p>
          {otherAnnotations.map((a, i) => (
            <div key={i} style={{
              padding: 10, borderRadius: 6, marginBottom: 6,
              background: c.surfaceRaised, border: `1px solid ${c.border}`,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
                <span style={{ fontSize: 11, fontWeight: 600, color: c.fg }}>{a.annotator}</span>
                {a.change_requested && (
                  <span style={{
                    fontSize: 8, fontWeight: 600, color: '#f59e0b', textTransform: 'uppercase',
                    padding: '1px 5px', borderRadius: 3,
                    background: 'rgba(245,158,11,0.1)',
                  }}>
                    edit suggested
                  </span>
                )}
              </div>
              <p style={{ fontSize: 12, color: c.muted, margin: 0 }}>
                <strong>Answer:</strong> {a.answer}
              </p>
              {a.edited_question && (
                <p style={{ fontSize: 11, color: '#f59e0b', margin: '4px 0 0', fontStyle: 'italic' }}>
                  Suggested: {a.edited_question}
                </p>
              )}
              {a.notes && (
                <p style={{ fontSize: 11, color: c.dim, margin: '4px 0 0' }}>
                  Note: {a.notes}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ── Metadata Editor ── */

function MetadataEditor({ figureId, auth, currentPage, currentCaption, reviews, onSaved }: {
  figureId: string
  auth: AuthState
  currentPage?: number
  currentCaption?: string
  reviews: ReviewEntry[]
  onSaved: () => void
}) {
  const existing = reviews.find(r => r.review_type === 'metadata' && r.annotator === auth.name)

  const [pdfPage, setPdfPage] = useState(existing?.pdf_page || String(currentPage || ''))
  const [figNumber, setFigNumber] = useState(existing?.figure_number || '')
  const [caption, setCaption] = useState(existing?.caption || '')
  const [notes, setNotes] = useState(existing?.notes || '')
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (existing) {
      setPdfPage(existing.pdf_page || String(currentPage || ''))
      setFigNumber(existing.figure_number || '')
      setCaption(existing.caption || '')
      setNotes(existing.notes || '')
    }
  }, [existing?.timestamp])

  const hasChanges = pdfPage !== String(currentPage || '') || figNumber || caption || notes

  const handleSave = async () => {
    setSaving(true)
    await saveReview({
      figure_id: figureId,
      annotator: auth.name,
      password: auth.password,
      review_type: 'metadata',
      pdf_page: pdfPage || undefined,
      figure_number: figNumber || undefined,
      caption: caption || undefined,
      notes: notes || undefined,
    })
    setSaving(false)
    setSaved(true)
    onSaved()
    setTimeout(() => setSaved(false), 2000)
  }

  const inputStyle = {
    width: '100%', padding: '7px 10px', borderRadius: 6, fontSize: 12,
    fontFamily: 'inherit', background: c.bg, border: `1px solid ${c.border}`,
    color: c.fg, outline: 'none',
  }
  const labelStyle = {
    fontSize: 10, fontWeight: 600 as const, textTransform: 'uppercase' as const,
    letterSpacing: '0.06em', color: c.dim, marginBottom: 4,
  }

  return (
    <Section label="Review & Corrections">
      <div style={{
        borderRadius: 8, border: `1px solid ${c.border}`,
        background: c.surface, padding: 14,
        display: 'flex', flexDirection: 'column', gap: 10,
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          <div>
            <p style={labelStyle}>PDF Page {currentPage ? `(current: ${currentPage})` : ''}</p>
            <input
              value={pdfPage}
              onChange={e => setPdfPage(e.target.value)}
              placeholder="Page number..."
              type="number"
              style={inputStyle}
            />
          </div>
          <div>
            <p style={labelStyle}>Figure Number (e.g., Figure 4)</p>
            <input
              value={figNumber}
              onChange={e => setFigNumber(e.target.value)}
              placeholder="e.g., Figure 4"
              style={inputStyle}
            />
          </div>
        </div>
        <div>
          <p style={labelStyle}>Caption Correction (if wrong)</p>
          <textarea
            value={caption}
            onChange={e => setCaption(e.target.value)}
            placeholder={currentCaption ? `Current: ${currentCaption.substring(0, 80)}...` : 'Enter corrected caption...'}
            rows={2}
            style={{ ...inputStyle, resize: 'none' as const }}
          />
        </div>
        <div>
          <p style={labelStyle}>Notes</p>
          <input
            value={notes}
            onChange={e => setNotes(e.target.value)}
            placeholder="Any notes..."
            style={inputStyle}
          />
        </div>
        <button
          onClick={handleSave}
          disabled={saving || (!hasChanges && !existing)}
          style={{
            alignSelf: 'flex-start',
            padding: '6px 16px', borderRadius: 6, border: 'none',
            background: saved ? '#22c55e' : hasChanges ? c.accent : c.dim,
            color: '#fff', fontSize: 11, fontWeight: 500, fontFamily: 'inherit',
            cursor: hasChanges ? 'pointer' : 'default',
          }}
        >
          {saving ? 'Saving...' : saved ? 'Saved' : existing ? 'Update' : 'Save'}
        </button>
      </div>
    </Section>
  )
}
