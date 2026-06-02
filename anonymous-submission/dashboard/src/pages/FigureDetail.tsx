import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence, LayoutGroup } from 'motion/react'
import { getAnnotations, saveAnnotation, getReviews, saveReview, displayName, type AuthState, type AnnotationEntry, type ReviewEntry } from '../auth'

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }
const SPRING_SOFT = { type: 'spring' as const, stiffness: 180, damping: 26, mass: 0.9 }

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
  locked?: boolean
  status?: string
  reviewer_notes?: string
}

interface ProbeData {
  figure_id: string
  selective_blur: {
    admittance?: ProbeTarget
    inductance?: ProbeTarget
  }
  ocr_texts?: string[]
}

interface ResistanceProbe {
  type: 'inexist' | 'contra' | 'unanswerable'
  question: string
  expected_behavior: string
  false_element?: string
  false_premise?: string
  why_unanswerable?: string
  principle: string
}

interface ResistanceData {
  probes: ResistanceProbe[]
  figure_id: string
  figure_type: string
}

interface CaptionBiasModification {
  claim: string
  reality: string
  type: string
  principle: string
}

interface CaptionBiasData {
  modified_caption: string
  modifications: CaptionBiasModification[]
  correct_elements: string[]
  figure_id: string
  figure_type: string
  original_caption: string
  num_modifications: number
}

const c = {
  bg: 'var(--t-bg)',
  surface: 'var(--t-surface)',
  surfaceHover: 'var(--t-surface-hover)',
  surfaceActive: 'var(--t-surface-active)',
  surfaceRaised: 'var(--t-surface-raised)',
  border: 'var(--t-border)',
  borderStrong: 'var(--t-border-strong)',
  fg: 'var(--t-fg)',
  muted: 'var(--t-muted)',
  dim: 'var(--t-dim)',
  accent: 'var(--t-accent)',
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

interface VariantDef {
  id: string
  label: string
  path: string | null
  description: string
}

type TabId = 'info' | 'questions' | 'blur' | 'hallucination' | 'caption_bias'

interface TabDef {
  id: TabId
  label: string
  shortLabel: string
}

const TABS: TabDef[] = [
  { id: 'info',          label: 'Information',          shortLabel: 'Info' },
  { id: 'questions',     label: 'Capability Questions', shortLabel: 'Reasoning' },
  { id: 'blur',          label: 'Selective Blur',       shortLabel: 'Blur' },
  { id: 'hallucination', label: 'Hallucination',        shortLabel: 'Hallucinate' },
  { id: 'caption_bias',  label: 'Caption Bias',         shortLabel: 'Caption' },
]

const VARIANTS: VariantDef[] = [
  { id: 'original',         label: 'Original',         path: null,                          description: 'Untouched figure as published.' },
  { id: 'rotation',         label: 'Rotation',         path: '/transforms/rotation',        description: 'Rotated to test orientation robustness.' },
  { id: 'noise',            label: 'Noise',            path: '/transforms/noise',           description: 'Gaussian noise overlay.' },
  { id: 'low_contrast',     label: 'Low Contrast',     path: '/transforms/low_contrast',    description: 'Reduced luminance contrast.' },
  { id: 'in_paper',         label: 'In-Paper',         path: '/transforms/in_paper',        description: 'Figure embedded in its source PDF page.' },
  { id: 'in_paper_blur',    label: 'In-Paper Blur',    path: '/transforms/in_paper_blur',   description: 'In-paper variant with the figure region blurred.' },
  { id: 'admittance_blur',  label: 'Admittance Blur',  path: '/adversarial_admittance',     description: 'Unrecoverable element blurred — tests epistemic honesty.' },
  { id: 'inductance_blur',  label: 'Inductance Blur',  path: '/adversarial_inductance',     description: 'Inferable element blurred — tests contextual reasoning.' },
]

/* ── Main ── */

export default function FigureDetail({ figureId, onBack, auth }: {
  figureId: string
  onBack: () => void
  auth: AuthState | null
}) {
  const [figure, setFigure] = useState<FigureEntry | null>(null)
  const [capability, setCapability] = useState<CapabilityData | null>(null)
  const [probe, setProbe] = useState<ProbeData | null>(null)
  const [resistance, setResistance] = useState<ResistanceData | null>(null)
  const [captionBias, setCaptionBias] = useState<CaptionBiasData | null>(null)
  const [activeTab, setActiveTab] = useState<TabId>('info')
  const [annIdx, setAnnIdx] = useState(0)
  const [expandedQ, setExpandedQ] = useState<number | null>(null)
  const [annotations, setAnnotations] = useState<AnnotationEntry[]>([])
  const [reviews, setReviews] = useState<ReviewEntry[]>([])
  const [activeVariant, setActiveVariant] = useState<string>('original')
  const [availableVariants, setAvailableVariants] = useState<Set<string>>(new Set(['original']))

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
    fetch(`/resistance_probes/${figureId}.json`)
      .then(r => { if (r.ok) return r.json(); return null })
      .then(d => { if (d) setResistance(d); else setResistance(null) })
      .catch(() => setResistance(null))
    fetch(`/caption_bias/${figureId}.json`)
      .then(r => { if (r.ok) return r.json(); return null })
      .then(d => { if (d) setCaptionBias(d); else setCaptionBias(null) })
      .catch(() => setCaptionBias(null))
    loadAnnotations()

    setActiveVariant('original')
    const checkAvailable = async () => {
      const avail = new Set<string>(['original'])
      const checks: [string, string][] = VARIANTS
        .filter(v => v.path)
        .map(v => [v.id, `${v.path}/${figureId}.png`])
      await Promise.all(checks.map(([id, url]) =>
        fetch(url, { method: 'HEAD' })
          .then(r => { if (r.ok) avail.add(id) })
          .catch(() => {})
      ))
      setAvailableVariants(avail)
    }
    checkAvailable()
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
        background: 'var(--t-overlay-glass)', backdropFilter: 'blur(12px)',
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

          {/* Left: Figure Image + Variant Grid */}
          <div>
            <VariantHero
              figureId={figureId}
              caption={figure.caption}
              activeVariant={activeVariant}
              availableVariants={availableVariants}
              onSelect={setActiveVariant}
            />

            {/* Paper info below image */}
            {figure.paper_title && (
              <div style={{ marginTop: 20 }}>
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
            <SegmentedTabBar
              tabs={TABS.map(t => ({
                ...t,
                badge:
                  t.id === 'questions' ? capability?.questions.length :
                  t.id === 'hallucination' ? resistance?.probes.length :
                  t.id === 'caption_bias' ? captionBias?.modifications.length :
                  undefined,
                disabled:
                  (t.id === 'hallucination' && !resistance) ||
                  (t.id === 'caption_bias' && !captionBias),
              }))}
              active={activeTab}
              onSelect={setActiveTab}
            />

            {/* Tab Content */}
            <AnimatePresence mode="wait" initial={false}>
            {activeTab === 'info' && (
              <TabPanel key="info">
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
              </TabPanel>
            )}

            {activeTab === 'questions' && (
              <TabPanel key="questions">
                {capability && capability.questions.length > 0 ? (
                  <StaggerList>
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
                  </StaggerList>
                ) : (
                  <EmptyState text="No capability questions generated yet" />
                )}
              </TabPanel>
            )}

            {activeTab === 'blur' && (
              <TabPanel key="blur">
                {probe && probe.selective_blur ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
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
                      <EmptyState text="No selective-blur probes generated for this figure" />
                    )}
                  </div>
                ) : (
                  <EmptyState text="No blur probes available" />
                )}
              </TabPanel>
            )}

            {activeTab === 'hallucination' && (
              <TabPanel key="hallucination">
                {resistance && resistance.probes.length > 0 ? (
                  <StaggerList>
                    {resistance.probes.map((p, i) => (
                      <ResistanceCard key={`${p.type}-${i}`} probe={p} index={i} />
                    ))}
                  </StaggerList>
                ) : (
                  <EmptyState text="No hallucination probes available" />
                )}
              </TabPanel>
            )}

            {activeTab === 'caption_bias' && (
              <TabPanel key="caption_bias">
                {captionBias ? (
                  <CaptionBiasCard data={captionBias} originalCaption={figure.caption} />
                ) : (
                  <EmptyState text="No caption-bias data for this figure" />
                )}
              </TabPanel>
            )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── Variant Hero (image + SSENSE-style grid, premium motion) ── */

function VariantHero({ figureId, caption, activeVariant, availableVariants, onSelect }: {
  figureId: string
  caption?: string
  activeVariant: string
  availableVariants: Set<string>
  onSelect: (id: string) => void
}) {
  const variants = VARIANTS.filter(v => availableVariants.has(v.id))
  const active = variants.find(v => v.id === activeVariant) || VARIANTS[0]
  const heroSrc = active.path ? `${active.path}/${figureId}.png` : `/figures/${figureId}.png`

  // Preload every available variant once we know which exist — kills click lag
  useEffect(() => {
    variants.forEach(v => {
      const src = v.path ? `${v.path}/${figureId}.png` : `/figures/${figureId}.png`
      const img = new Image()
      img.decoding = 'async'
      img.src = src
    })
  }, [figureId, variants.length])

  return (
    <LayoutGroup id="variant-hero">
      <div>
        {/* Hero — instant overlapping crossfade between variants */}
        <motion.div
          layout
          transition={SPRING_SOFT}
          style={{
            borderRadius: 12, border: `1px solid ${c.border}`,
            background: c.surface, padding: 24,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            minHeight: 400, position: 'relative', overflow: 'hidden',
          }}
        >
          <AnimatePresence initial={false}>
            <motion.img
              key={active.id}
              src={heroSrc}
              alt={caption || figureId}
              decoding="async"
              fetchPriority="high"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.18, ease: 'easeOut' }}
              style={{
                position: 'absolute',
                top: 24, left: 24, right: 24, bottom: 24,
                margin: 'auto',
                maxWidth: 'calc(100% - 48px)', maxHeight: '60vh', objectFit: 'contain',
                willChange: 'opacity',
              }}
            />
          </AnimatePresence>
          {/* Invisible spacer to maintain hero box height */}
          <img
            src={heroSrc}
            alt=""
            aria-hidden
            style={{
              maxWidth: '100%', maxHeight: '60vh', objectFit: 'contain',
              visibility: 'hidden',
            }}
          />

          <AnimatePresence>
            {active.id !== 'original' && (
              <motion.span
                key={`badge-${active.id}`}
                initial={{ opacity: 0, y: -6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={SPRING}
                style={{
                  position: 'absolute', top: 14, left: 14,
                  fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
                  letterSpacing: '0.08em', padding: '4px 9px', borderRadius: 4,
                  color: c.fg, background: 'var(--t-border)',
                  border: `1px solid ${c.borderStrong}`, lineHeight: 1,
                  backdropFilter: 'blur(8px)',
                }}
              >
                {active.label}
              </motion.span>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Caption strip — vertical flip between labels */}
        <div style={{
          marginTop: 14, marginBottom: 14,
          display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
          gap: 16, minHeight: 36,
        }}>
          <div style={{ overflow: 'hidden' }}>
            <p style={{
              fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.1em', color: c.dim, margin: 0, lineHeight: 1,
            }}>
              Currently viewing
            </p>
            <div style={{ position: 'relative', height: 18, marginTop: 6 }}>
              <AnimatePresence mode="wait" initial={false}>
                <motion.p
                  key={active.id}
                  initial={{ y: 14, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -14, opacity: 0 }}
                  transition={SPRING}
                  style={{
                    position: 'absolute', inset: 0,
                    fontSize: 13, color: c.fg, margin: 0, fontWeight: 500,
                  }}
                >
                  {active.label}
                </motion.p>
              </AnimatePresence>
            </div>
          </div>
          <AnimatePresence mode="wait" initial={false}>
            <motion.p
              key={`desc-${active.id}`}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
              style={{
                fontSize: 11, color: c.muted, margin: 0, lineHeight: 1.5,
                maxWidth: '60%', textAlign: 'right',
              }}
            >
              {active.description}
            </motion.p>
          </AnimatePresence>
        </div>

        {/* Variant grid — staggered entrance + floating active ring */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.04, delayChildren: 0.05 } },
          }}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 10,
          }}
        >
          {variants.map(v => {
            const isActive = v.id === active.id
            const src = v.path ? `${v.path}/${figureId}.png` : `/figures/${figureId}.png`
            return (
              <motion.button
                key={v.id}
                onClick={() => onSelect(v.id)}
                variants={{
                  hidden: { opacity: 0, y: 12 },
                  visible: { opacity: 1, y: 0, transition: SPRING },
                }}
                whileHover={{ y: -3 }}
                whileTap={{ scale: 0.97 }}
                transition={SPRING}
                style={{
                  display: 'flex', flexDirection: 'column', alignItems: 'stretch',
                  gap: 6, padding: 0, background: 'none', border: 'none',
                  cursor: 'pointer', fontFamily: 'inherit', textAlign: 'left',
                  position: 'relative',
                }}
              >
                {/* Floating active ring — slides between tiles via shared layoutId */}
                {isActive && (
                  <motion.div
                    layoutId="variant-active-ring"
                    transition={SPRING}
                    style={{
                      position: 'absolute',
                      inset: '-4px -4px auto -4px',
                      aspectRatio: '1 / 1',
                      borderRadius: 11,
                      border: `1px solid var(--t-overlay-strong)`,
                      boxShadow: '0 0 0 4px var(--t-overlay-soft), 0 8px 32px rgba(0,0,0,0.4)',
                      pointerEvents: 'none',
                      zIndex: 2,
                    }}
                  />
                )}
                <motion.div
                  animate={{ opacity: isActive ? 1 : 0.62 }}
                  whileHover={{ opacity: 1 }}
                  transition={{ duration: 0.18 }}
                  style={{
                    aspectRatio: '1 / 1',
                    borderRadius: 8,
                    background: c.surface,
                    border: `1px solid ${c.border}`,
                    padding: 6,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    overflow: 'hidden',
                  }}
                >
                  <motion.img
                    src={src}
                    alt={v.label}
                    loading="lazy"
                    initial={{ filter: 'blur(6px)', opacity: 0 }}
                    animate={{ filter: 'blur(0px)', opacity: 1 }}
                    transition={{ duration: 0.4, ease: 'easeOut' }}
                    style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                  />
                </motion.div>
                <motion.p
                  animate={{ color: isActive ? c.fg : c.dim }}
                  transition={{ duration: 0.18 }}
                  style={{
                    margin: 0,
                    fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
                    letterSpacing: '0.07em',
                    lineHeight: 1.2,
                  }}
                >
                  {v.label}
                </motion.p>
              </motion.button>
            )
          })}
        </motion.div>
      </div>
    </LayoutGroup>
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
  const [showBlurred, setShowBlurred] = useState(true)
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
            {target.locked ? (
              <div style={{
                padding: '8px 14px', borderRadius: 6, fontSize: 11, fontWeight: 600,
                background: 'rgba(34,197,94,0.1)', color: '#22c55e',
                border: '1px solid rgba(34,197,94,0.2)',
                display: 'flex', alignItems: 'center', gap: 6,
              }}>
                <span>✓ Confirmed & Locked</span>
              </div>
            ) : !showReview ? (
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
                        Select Target
                      </p>
                      <div style={{
                        maxHeight: 140, overflowY: 'auto', borderRadius: 6,
                        border: `1px solid ${c.border}`, background: c.bg,
                      }}>
                        {[target.blurred_text, ...ocrTexts.filter(t => t !== target.blurred_text)].map((text, i, arr) => (
                          <button
                            key={i}
                            onClick={() => setNewTarget(text)}
                            style={{
                              display: 'block', width: '100%', textAlign: 'left',
                              padding: '6px 10px', border: 'none', cursor: 'pointer',
                              fontFamily: 'inherit', fontSize: 11,
                              background: newTarget === text ? accentBg : 'transparent',
                              color: newTarget === text ? accentColor : text === target.blurred_text ? c.fg : c.muted,
                              fontWeight: text === target.blurred_text ? 600 : 400,
                              borderBottom: i < arr.length - 1 ? `1px solid ${c.border}` : 'none',
                              transition: 'background 0.1s',
                            }}
                            onMouseEnter={e => { if (newTarget !== text) e.currentTarget.style.background = c.surfaceHover }}
                            onMouseLeave={e => { if (newTarget !== text) e.currentTarget.style.background = 'transparent' }}
                          >
                            {text === target.blurred_text ? `${text} (current)` : text}
                          </button>
                        ))}
                      </div>
                      {newTarget && (
                        <p style={{ fontSize: 11, color: accentColor, margin: '6px 0 0' }}>
                          Selected: <strong>{newTarget}</strong>{newTarget === target.blurred_text ? ' (current target)' : ''}
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

function SegmentedTabBar({ tabs, active, onSelect }: {
  tabs: Array<TabDef & { badge?: number; disabled?: boolean }>
  active: TabId
  onSelect: (id: TabId) => void
}) {
  return (
    <div style={{ position: 'relative', marginBottom: 22 }}>
      <div
        style={{
          display: 'flex', gap: 2,
          padding: 4,
          borderRadius: 10,
          background: c.surface,
          border: `1px solid ${c.border}`,
          overflowX: 'auto',
          scrollbarWidth: 'none',
        }}
        className="hide-scrollbar"
      >
        <LayoutGroup id="tab-bar">
          {tabs.map(t => {
            const isActive = t.id === active
            return (
              <motion.button
                key={t.id}
                onClick={() => !t.disabled && onSelect(t.id)}
                whileTap={t.disabled ? undefined : { scale: 0.96 }}
                transition={SPRING}
                style={{
                  position: 'relative',
                  flex: '0 0 auto',
                  padding: '7px 14px',
                  background: 'none', border: 'none',
                  cursor: t.disabled ? 'default' : 'pointer',
                  fontFamily: 'inherit',
                  fontSize: 11, fontWeight: 500,
                  whiteSpace: 'nowrap',
                  borderRadius: 7,
                  opacity: t.disabled ? 0.35 : 1,
                  zIndex: 1,
                  display: 'flex', alignItems: 'center', gap: 6,
                }}
              >
                {isActive && (
                  <motion.span
                    layoutId="tab-pill"
                    transition={SPRING}
                    style={{
                      position: 'absolute', inset: 0,
                      borderRadius: 7,
                      background: 'var(--t-overlay-medium)',
                      border: '1px solid var(--t-overlay-strong)',
                      zIndex: -1,
                    }}
                  />
                )}
                <motion.span
                  animate={{ color: isActive ? c.fg : c.muted }}
                  transition={{ duration: 0.18 }}
                >
                  {t.shortLabel}
                </motion.span>
                {typeof t.badge === 'number' && t.badge > 0 && (
                  <motion.span
                    animate={{
                      color: isActive ? c.fg : c.dim,
                      background: isActive ? 'var(--t-overlay-strong)' : 'var(--t-overlay-soft)',
                    }}
                    transition={{ duration: 0.18 }}
                    style={{
                      fontSize: 9, fontWeight: 600,
                      padding: '1px 6px', borderRadius: 4,
                      fontFamily: 'JetBrains Mono, monospace',
                      lineHeight: 1.4,
                    }}
                  >
                    {t.badge}
                  </motion.span>
                )}
              </motion.button>
            )
          })}
        </LayoutGroup>
      </div>
      {/* Fade edges */}
      <div style={{
        position: 'absolute', top: 0, bottom: 0, right: 0, width: 24,
        background: `linear-gradient(to right, transparent, ${c.bg})`,
        pointerEvents: 'none', borderTopRightRadius: 10, borderBottomRightRadius: 10,
      }} />
    </div>
  )
}

function TabPanel({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -6 }}
      transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  )
}

function StaggerList({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.05, delayChildren: 0.04 } },
      }}
      style={{ display: 'flex', flexDirection: 'column', gap: 12 }}
    >
      {Array.isArray(children) ? children.map((child, i) => (
        <motion.div
          key={i}
          variants={{
            hidden: { opacity: 0, y: 10 },
            visible: { opacity: 1, y: 0, transition: SPRING },
          }}
        >
          {child}
        </motion.div>
      )) : (
        <motion.div variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: SPRING } }}>
          {children}
        </motion.div>
      )}
    </motion.div>
  )
}

function EmptyState({ text }: { text: string }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.25 }}
      style={{
        textAlign: 'center', padding: '48px 0',
        color: c.dim, fontSize: 13,
      }}
    >
      {text}
    </motion.div>
  )
}

/* ── Resistance Probe Card ── */

const RESISTANCE_META: Record<ResistanceProbe['type'], { label: string; color: string; bg: string; description: string }> = {
  inexist:      { label: 'Inexist',      color: '#a855f7', bg: 'rgba(168,85,247,0.08)', description: 'False premise about a chart element that does not exist' },
  contra:       { label: 'Contra',       color: '#f97316', bg: 'rgba(249,115,22,0.08)', description: 'False numerical anchor that contradicts the chart' },
  unanswerable: { label: 'Unanswerable', color: '#06b6d4', bg: 'rgba(6,182,212,0.08)',  description: 'Question that cannot be answered from the figure alone' },
}

function ResistanceCard({ probe, index }: { probe: ResistanceProbe; index: number }) {
  const meta = RESISTANCE_META[probe.type]
  const detail = probe.false_element || probe.false_premise || probe.why_unanswerable

  return (
    <div style={{
      borderRadius: 10, border: `1px solid ${c.border}`,
      background: c.surface, overflow: 'hidden',
    }}>
      <div style={{
        padding: '14px 16px',
        borderBottom: `1px solid ${c.border}`,
        display: 'flex', alignItems: 'flex-start', gap: 10,
      }}>
        <span style={{
          width: 22, height: 22, borderRadius: 6,
          background: meta.bg, color: meta.color,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 11, fontWeight: 600, flexShrink: 0, marginTop: 1,
        }}>
          {index + 1}
        </span>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
            <span style={{
              fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.06em', color: meta.color,
              padding: '2px 7px', borderRadius: 4,
              background: meta.bg, border: `1px solid ${meta.color}30`,
              lineHeight: 1,
            }}>
              {meta.label}
            </span>
          </div>
          <p style={{ fontSize: 11, color: c.dim, margin: 0, lineHeight: 1.5 }}>
            {meta.description}
          </p>
        </div>
      </div>

      <div style={{ padding: '14px 16px' }}>
        <p style={{
          fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
        }}>
          Probe Question
        </p>
        <div style={{
          borderRadius: 8, background: c.surfaceRaised,
          border: `1px solid ${c.border}`, padding: 12, marginBottom: 14,
        }}>
          <p style={{ fontSize: 13, color: c.fg, lineHeight: 1.6, margin: 0 }}>
            {probe.question}
          </p>
        </div>

        <p style={{
          fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
        }}>
          Expected Behaviour
        </p>
        <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.6, margin: '0 0 14px' }}>
          {probe.expected_behavior}
        </p>

        {detail && (
          <>
            <p style={{
              fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
            }}>
              {probe.type === 'inexist' ? 'Why Plausible' : probe.type === 'contra' ? 'False Anchor' : 'Why Unanswerable'}
            </p>
            <p style={{ fontSize: 12, color: c.muted, lineHeight: 1.6, margin: '0 0 14px' }}>
              {detail}
            </p>
          </>
        )}

        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {probe.principle.split(',').map(p => p.trim()).filter(Boolean).map(p => (
            <span key={p} style={{
              fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.05em', color: c.muted,
              padding: '2px 7px', borderRadius: 4,
              background: c.surfaceRaised, border: `1px solid ${c.border}`,
              lineHeight: 1.3,
            }}>
              {p.replace(/_/g, ' ')}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ── Caption Bias Card ── */

function CaptionBiasCard({ data, originalCaption }: {
  data: CaptionBiasData
  originalCaption?: string
}) {
  const [view, setView] = useState<'modified' | 'original'>('modified')
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null)

  const highlightCaption = (text: string) => {
    let result: React.ReactNode[] = [text]
    data.modifications.forEach((mod, idx) => {
      const next: React.ReactNode[] = []
      result.forEach(segment => {
        if (typeof segment !== 'string') { next.push(segment); return }
        const at = segment.indexOf(mod.claim)
        if (at === -1) { next.push(segment); return }
        next.push(segment.slice(0, at))
        next.push(
          <motion.span
            key={`mod-${idx}`}
            onClick={() => setExpandedIdx(expandedIdx === idx ? null : idx)}
            whileHover={{ background: 'rgba(245,158,11,0.18)' }}
            transition={{ duration: 0.15 }}
            style={{
              background: 'rgba(245,158,11,0.1)',
              borderBottom: '1px dashed #f59e0b',
              padding: '0 2px', cursor: 'pointer',
              color: '#fcd34d',
            }}
          >
            {mod.claim}
          </motion.span>
        )
        next.push(segment.slice(at + mod.claim.length))
      })
      result = next
    })
    return result
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {/* Caption view toggle */}
      <div style={{ display: 'flex', gap: 4 }}>
        {(['modified', 'original'] as const).map(v => (
          <motion.button
            key={v}
            onClick={() => setView(v)}
            whileTap={{ scale: 0.96 }}
            transition={SPRING}
            style={{
              position: 'relative',
              padding: '6px 14px', borderRadius: 6,
              fontFamily: 'inherit', fontSize: 11, fontWeight: 500,
              background: 'none', border: 'none', cursor: 'pointer',
              zIndex: 1,
            }}
          >
            {view === v && (
              <motion.span
                layoutId="caption-view-pill"
                transition={SPRING}
                style={{
                  position: 'absolute', inset: 0,
                  borderRadius: 6,
                  background: 'rgba(245,158,11,0.1)',
                  border: '1px solid rgba(245,158,11,0.25)',
                  zIndex: -1,
                }}
              />
            )}
            <motion.span animate={{ color: view === v ? '#f59e0b' : c.dim }} transition={{ duration: 0.18 }}>
              {v === 'modified' ? 'Modified' : 'Original'}
            </motion.span>
          </motion.button>
        ))}
      </div>

      {/* Caption text */}
      <div style={{
        borderRadius: 10, border: `1px solid ${c.border}`,
        background: c.surface, padding: 16,
        position: 'relative',
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          marginBottom: 10,
        }}>
          <span style={{
            fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.06em', color: c.dim, lineHeight: 1,
          }}>
            {view === 'modified' ? 'Caption with Bias' : 'Original Caption'}
          </span>
          {view === 'modified' && (
            <span style={{
              fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
              letterSpacing: '0.06em',
              padding: '2px 7px', borderRadius: 4,
              background: 'rgba(245,158,11,0.1)', color: '#f59e0b',
              border: '1px solid rgba(245,158,11,0.25)',
              lineHeight: 1,
            }}>
              {data.num_modifications} false claim{data.num_modifications !== 1 ? 's' : ''}
            </span>
          )}
        </div>
        <AnimatePresence mode="wait" initial={false}>
          <motion.p
            key={view}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
            style={{
              fontSize: 12.5, color: c.muted, lineHeight: 1.75,
              margin: 0, fontStyle: 'italic',
            }}
          >
            {view === 'modified' ? highlightCaption(data.modified_caption) : (originalCaption || 'No original caption available.')}
          </motion.p>
        </AnimatePresence>
      </div>

      {/* Modifications list */}
      <div>
        <p style={{
          fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.08em', color: c.dim, margin: '0 0 10px',
        }}>
          False Claims ({data.modifications.length})
        </p>
        <StaggerList>
          {data.modifications.map((mod, i) => {
            const isOpen = expandedIdx === i
            return (
              <motion.div
                key={i}
                layout
                transition={SPRING_SOFT}
                style={{
                  borderRadius: 10, border: `1px solid ${c.border}`,
                  background: c.surface, overflow: 'hidden',
                }}
              >
                <motion.button
                  onClick={() => setExpandedIdx(isOpen ? null : i)}
                  whileTap={{ scale: 0.995 }}
                  style={{
                    width: '100%', display: 'flex', alignItems: 'flex-start', gap: 10,
                    padding: '12px 14px', background: 'none', border: 'none',
                    cursor: 'pointer', textAlign: 'left', fontFamily: 'inherit',
                  }}
                >
                  <span style={{
                    width: 20, height: 20, borderRadius: 5,
                    background: 'rgba(245,158,11,0.1)', color: '#f59e0b',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 10, fontWeight: 600, flexShrink: 0, marginTop: 1,
                  }}>
                    {i + 1}
                  </span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', gap: 6, marginBottom: 4 }}>
                      <span style={{
                        fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
                        letterSpacing: '0.05em', color: c.muted,
                        padding: '1px 6px', borderRadius: 4,
                        background: c.surfaceRaised, border: `1px solid ${c.border}`,
                      }}>
                        {mod.type.replace(/_/g, ' ')}
                      </span>
                      <span style={{
                        fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
                        letterSpacing: '0.05em', color: c.muted,
                        padding: '1px 6px', borderRadius: 4,
                        background: c.surfaceRaised, border: `1px solid ${c.border}`,
                      }}>
                        {mod.principle.replace(/_/g, ' ')}
                      </span>
                    </div>
                    <p style={{
                      fontSize: 12, color: '#fcd34d', lineHeight: 1.5, margin: 0,
                      fontStyle: 'italic',
                    }}>
                      “{mod.claim}”
                    </p>
                  </div>
                  <motion.svg
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={SPRING}
                    width="14" height="14" viewBox="0 0 16 16"
                    fill="none" stroke={c.dim} strokeWidth="1.5" strokeLinecap="round"
                    style={{ flexShrink: 0, marginTop: 4 }}
                  >
                    <path d="M4 6l4 4 4-4" />
                  </motion.svg>
                </motion.button>
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={SPRING_SOFT}
                      style={{ overflow: 'hidden' }}
                    >
                      <div style={{
                        padding: '0 14px 14px 44px',
                      }}>
                        <p style={{
                          fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                          letterSpacing: '0.06em', color: c.dim, margin: '0 0 6px',
                        }}>
                          Reality
                        </p>
                        <p style={{ fontSize: 12, color: '#86efac', lineHeight: 1.6, margin: 0 }}>
                          {mod.reality}
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}
        </StaggerList>
      </div>
    </div>
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
            Your Annotation ({displayName(auth.name)})
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
                <span style={{ fontSize: 11, fontWeight: 600, color: c.fg }}>{displayName(a.annotator)}</span>
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
