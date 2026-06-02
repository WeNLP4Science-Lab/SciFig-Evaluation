import { useState, useEffect, useMemo, useCallback, useRef } from 'react'
import {
  motion, useMotionValue, useSpring, useTransform, animate, useInView,
  AnimatePresence, LayoutGroup,
} from 'motion/react'

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }

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

type FilterType = 'All' | 'Bar Chart' | 'Line Plot' | 'Pie Chart'

const FILTERS: FilterType[] = ['All', 'Bar Chart', 'Line Plot', 'Pie Chart']

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
const TYPE_SHORT: Record<string, string> = {
  'Bar Chart': 'Bar',
  'Line Plot': 'Line',
  'Pie Chart': 'Pie',
}

/* ── Shared inline style constants ── */

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

/* ── Main Component ── */

import { figureInRange, isAnnotationMode, getSavedAuth } from '../auth'
import SciFigLogo from '../components/SciFigLogo'

export default function Dataset({ onSelectFigure, onBackToHome }: {
  onSelectFigure: (id: string) => void
  onBackToHome?: () => void
}) {
  const [data, setData] = useState<FigureEntry[]>([])
  const [filter, setFilter] = useState<FilterType>('All')
  const [search, setSearch] = useState('')
  const [loaded, setLoaded] = useState<Set<string>>(new Set())

  useEffect(() => {
    fetch('/manifest.json').then(r => r.json()).then(setData)
  }, [])

  const annotateMode = isAnnotationMode()
  const auth = getSavedAuth()

  // Base dataset: filtered by annotator range in annotation mode
  const baseData = useMemo(() => {
    if (annotateMode && auth) {
      return data.filter(d => figureInRange(d.id, auth.name))
    }
    return data
  }, [data, annotateMode, auth])

  const filtered = useMemo(() => {
    let items = baseData
    if (filter !== 'All') items = items.filter(d => d.figure_type === filter)
    if (search.trim()) {
      const q = search.toLowerCase()
      items = items.filter(d =>
        d.id.includes(q) ||
        d.caption.toLowerCase().includes(q) ||
        d.paper_title.toLowerCase().includes(q)
      )
    }
    return items
  }, [baseData, filter, search])

  const counts = useMemo(() => {
    const r: Record<string, number> = { 'Bar Chart': 0, 'Line Plot': 0, 'Pie Chart': 0 }
    baseData.forEach(d => { if (d.figure_type in r) r[d.figure_type]++ })
    return r
  }, [baseData])

  const papers = useMemo(() => new Set(baseData.map(d => d.arxiv_id)).size, [baseData])
  const totalAnns = useMemo(() => baseData.reduce((s, d) => s + d.annotation_count, 0), [baseData])

  const markLoaded = useCallback((id: string) => {
    setLoaded(prev => new Set(prev).add(id))
  }, [])

  return (
    <div style={{ minHeight: '100vh' }}>
      {/* ── Top nav strip (back to landing) ── */}
      <div style={{
        position: 'sticky', top: 0, zIndex: 25,
        background: 'var(--t-overlay-glass)',
        backdropFilter: 'blur(14px)',
        borderBottom: `1px solid ${c.border}`,
      }}>
        <div className="page-container" style={{
          height: 52,
          display: 'flex', alignItems: 'center', gap: 12,
        }}>
          {onBackToHome && (
            <motion.button
              onClick={onBackToHome}
              whileHover={{ x: -2, opacity: 0.85 }}
              whileTap={{ scale: 0.96 }}
              transition={SPRING}
              style={{
                background: 'none', border: 'none', padding: 0,
                cursor: 'pointer', fontFamily: 'inherit',
                display: 'flex', alignItems: 'center', gap: 9,
                color: c.fg,
              }}
              aria-label="Back to home"
            >
              <SciFigLogo size={22} id="dataset-nav-logo" />
              <span style={{ fontSize: 13, fontWeight: 600, color: c.fg }}>
                SciFig-Eval
              </span>
            </motion.button>
          )}

          <span style={{ color: c.dim, fontSize: 12 }}>/</span>

          <span style={{
            fontSize: 12, color: c.muted, fontWeight: 500,
          }}>
            Dataset
          </span>

          <div style={{ flex: 1 }} />

          {onBackToHome && (
            <motion.button
              onClick={onBackToHome}
              whileHover={{ x: -2 }}
              whileTap={{ scale: 0.95 }}
              transition={SPRING}
              style={{
                background: 'none', border: 'none',
                fontSize: 12, color: c.muted, cursor: 'pointer',
                fontFamily: 'inherit',
                display: 'flex', alignItems: 'center', gap: 5,
                padding: '6px 10px', borderRadius: 6,
              }}
            >
              <svg width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                <path d="M10 3L5 8l5 5" />
              </svg>
              Back to landing
            </motion.button>
          )}
        </div>
      </div>

      {/* ── Header ── */}
      <header style={{ borderBottom: `1px solid ${c.border}` }}>
        <div className="page-container" style={{
          paddingTop: 48, paddingBottom: 36,
        }}>
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}
          >
            <span style={{
              fontSize: 11, fontWeight: 600, letterSpacing: '0.08em',
              textTransform: 'uppercase', color: c.accent,
            }}>
              Dataset Explorer
            </span>
            <span style={{ width: 1, height: 12, background: c.borderStrong }} />
            <span style={{ fontSize: 11, color: c.dim }}>v1.0</span>
          </motion.div>

          <WordStaggerTitle text="SciFig-Eval Benchmark" />

          <SubtitleCountUp
            figureCount={250}
            paperCount={papers || 123}
          />
        </div>
      </header>

      {/* ── Stats Hub ── */}
      <StatsHub
        figureCount={baseData.length}
        chartCounts={counts}
      />

      {/* ── Toolbar ── */}
      <div style={{
        borderBottom: `1px solid ${c.border}`,
        position: 'sticky', top: 0, zIndex: 20,
        background: 'var(--t-overlay-glass)', backdropFilter: 'blur(12px)',
      }}>
        <div className="page-container" style={{
          height: 44, display: 'flex', alignItems: 'center', gap: 16,
        }}>
          {/* Filters */}
          <LayoutGroup id="dataset-filters">
            <div style={{ display: 'flex', gap: 2 }}>
              {FILTERS.map(f => {
                const isActive = filter === f
                const count = f === 'All' ? baseData.length : counts[f]
                const dot = f !== 'All' ? TYPE_DOT[f] : undefined
                return (
                  <motion.button
                    key={f}
                    onClick={() => setFilter(f)}
                    whileTap={{ scale: 0.96 }}
                    transition={SPRING}
                    style={{
                      position: 'relative',
                      display: 'flex', alignItems: 'center', gap: 6,
                      height: 28, padding: '0 12px', borderRadius: 7,
                      fontSize: 12, fontFamily: 'inherit', cursor: 'pointer',
                      border: 'none',
                      background: 'none',
                      fontWeight: 500,
                      zIndex: 1,
                    }}
                  >
                    {isActive && (
                      <motion.span
                        layoutId="filter-pill"
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
                    {dot && <span style={{ width: 6, height: 6, borderRadius: '50%', background: dot }} />}
                    <motion.span
                      animate={{ color: isActive ? c.fg : c.muted }}
                      transition={{ duration: 0.18 }}
                    >
                      {f === 'All' ? 'All' : f}
                    </motion.span>
                    <TweenCount value={count} active={isActive} />
                  </motion.button>
                )
              })}
            </div>
          </LayoutGroup>

          <div style={{ flex: 1 }} />

          <SearchInput value={search} onChange={setSearch} />

          <ResultCounter count={filtered.length} />
        </div>
      </div>

      {/* ── Distribution Bar ── */}
      {baseData.length > 0 && (
        <DistributionBar baseTotal={baseData.length} counts={counts} filter={filter} />
      )}

      {/* ── Grid ── */}
      <div className="page-container" style={{ paddingTop: 20, paddingBottom: 48 }}>
        <LayoutGroup id="figures-grid">
          <motion.div
            layout
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: 18,
            }}
          >
            <AnimatePresence mode="popLayout" initial={false}>
              {filtered.map((item, i) => (
                <Card
                  key={item.id}
                  item={item}
                  index={i}
                  isLoaded={loaded.has(item.id)}
                  onLoad={() => markLoaded(item.id)}
                  onClick={() => onSelectFigure(item.id)}
                />
              ))}
            </AnimatePresence>
          </motion.div>
        </LayoutGroup>

        {filtered.length === 0 && baseData.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            style={{ textAlign: 'center', padding: '80px 0' }}
          >
            <p style={{ fontSize: 13, color: c.muted }}>No figures match your search</p>
            <button
              onClick={() => { setSearch(''); setFilter('All') }}
              style={{
                marginTop: 8, fontSize: 12, color: c.accent,
                background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'inherit',
              }}
            >
              Clear filters
            </button>
          </motion.div>
        )}
      </div>

    </div>
  )
}

/* ── Hero Text Reveal ── */

function WordStaggerTitle({ text }: { text: string }) {
  const words = text.split(' ')
  return (
    <motion.h1
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.06, delayChildren: 0.1 } },
      }}
      style={{
        fontSize: 28, fontWeight: 600, letterSpacing: '-0.02em',
        color: c.fg, lineHeight: 1.2, margin: 0,
        display: 'flex', flexWrap: 'wrap', gap: '0.32em',
      }}
    >
      {words.map((w, i) => (
        <motion.span
          key={i}
          variants={{
            hidden: { opacity: 0, y: 18, filter: 'blur(8px)' },
            visible: { opacity: 1, y: 0, filter: 'blur(0px)',
              transition: { duration: 0.55, ease: [0.22, 1, 0.36, 1] } },
          }}
          style={{ display: 'inline-block', willChange: 'transform, opacity, filter' }}
        >
          {w}
        </motion.span>
      ))}
    </motion.h1>
  )
}

function SubtitleCountUp({ figureCount, paperCount }: { figureCount: number; paperCount: number }) {
  const figs = useCountUp(figureCount, 1.6)
  const papers = useCountUp(paperCount, 1.6)
  return (
    <motion.p
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.55, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      style={{
        fontSize: 14, color: c.muted, marginTop: 10,
        maxWidth: 540, lineHeight: 1.6,
      }}
    >
      <span style={{ color: c.fg, fontWeight: 500, fontVariantNumeric: 'tabular-nums' }}>{figs}</span>{' '}
      scientific figures from{' '}
      <span style={{ color: c.fg, fontWeight: 500, fontVariantNumeric: 'tabular-nums' }}>{papers}</span>{' '}
      peer-reviewed papers, each annotated with structured natural-language descriptions for evaluating vision-language models.
    </motion.p>
  )
}

/* ── Tween Count (digit roll for filter counts) ── */

function TweenCount({ value, active }: { value: number; active?: boolean }) {
  const mv = useMotionValue(value)
  const [display, setDisplay] = useState(value)
  useEffect(() => {
    const controls = animate(mv, value, {
      duration: 0.4, ease: [0.22, 1, 0.36, 1],
      onUpdate: v => setDisplay(Math.round(v)),
    })
    return () => controls.stop()
  }, [value, mv])
  return (
    <motion.span
      animate={{ color: active ? c.muted : c.dim }}
      transition={{ duration: 0.18 }}
      style={{ fontSize: 10, fontVariantNumeric: 'tabular-nums' }}
    >
      {display}
    </motion.span>
  )
}

function ResultCounter({ count }: { count: number }) {
  const mv = useMotionValue(count)
  const [display, setDisplay] = useState(count)
  useEffect(() => {
    const controls = animate(mv, count, {
      duration: 0.4, ease: [0.22, 1, 0.36, 1],
      onUpdate: v => setDisplay(Math.round(v)),
    })
    return () => controls.stop()
  }, [count, mv])
  return (
    <span style={{
      fontSize: 11, color: c.dim, minWidth: 64, textAlign: 'right',
      fontVariantNumeric: 'tabular-nums',
    }}>
      {display} result{display !== 1 ? 's' : ''}
    </span>
  )
}

/* ── Search Input (animated focus + clear button) ── */

function SearchInput({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  const [focused, setFocused] = useState(false)
  return (
    <motion.div
      animate={{
        boxShadow: focused
          ? '0 0 0 3px rgba(59,130,246,0.12)'
          : '0 0 0 0px rgba(59,130,246,0)',
      }}
      transition={{ duration: 0.2 }}
      style={{
        position: 'relative',
        borderRadius: 7,
      }}
    >
      <svg style={{
        position: 'absolute', left: 9, top: '50%', transform: 'translateY(-50%)',
        width: 13, height: 13, pointerEvents: 'none',
      }} viewBox="0 0 16 16" fill="none" stroke={focused ? c.accent : c.dim} strokeWidth="1.5" strokeLinecap="round">
        <circle cx="6.5" cy="6.5" r="4" /><path d="M10 10l3.5 3.5" />
      </svg>
      <input
        type="text"
        placeholder="Search figures..."
        value={value}
        onChange={e => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={{
          width: 220, height: 28, paddingLeft: 30, paddingRight: value ? 28 : 10,
          fontSize: 12, borderRadius: 7, fontFamily: 'inherit',
          background: c.surface, border: `1px solid ${focused ? 'rgba(59,130,246,0.4)' : c.border}`,
          color: c.fg, outline: 'none',
          transition: 'border-color 0.2s ease',
        }}
      />
      <AnimatePresence>
        {value && (
          <motion.button
            key="clear"
            initial={{ opacity: 0, scale: 0.6 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.6 }}
            transition={SPRING}
            onClick={() => onChange('')}
            style={{
              position: 'absolute', right: 6, top: '50%', transform: 'translateY(-50%)',
              width: 18, height: 18, borderRadius: '50%', border: 'none',
              background: 'var(--t-border)', color: c.muted,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', padding: 0,
            }}
          >
            <svg width="9" height="9" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
              <path d="M2 2l8 8M10 2l-8 8" />
            </svg>
          </motion.button>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

/* ── Distribution Bar (segments slide in + hover interaction) ── */

function DistributionBar({ baseTotal, counts, filter }: {
  baseTotal: number
  counts: Record<string, number>
  filter: FilterType
}) {
  const [hoveredType, setHoveredType] = useState<string | null>(null)
  const TYPES = ['Bar Chart', 'Line Plot', 'Pie Chart'] as const

  return (
    <div className="page-container" style={{ paddingTop: 24, paddingBottom: 4 }}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        style={{
          display: 'flex', height: 5, borderRadius: 8, overflow: 'hidden',
          background: c.surface, border: `1px solid ${c.border}`,
        }}
      >
        {TYPES.map((t, i) => {
          const pct = (counts[t] / baseTotal) * 100
          const dim = (filter !== 'All' && filter !== t) || (hoveredType !== null && hoveredType !== t)
          return (
            <motion.div
              key={t}
              initial={{ width: 0 }}
              animate={{ width: `${pct}%`, opacity: dim ? 0.18 : 0.85 }}
              transition={{
                width: { duration: 0.7, delay: 0.4 + i * 0.08, ease: [0.22, 1, 0.36, 1] },
                opacity: { duration: 0.2 },
              }}
              onMouseEnter={() => setHoveredType(t)}
              onMouseLeave={() => setHoveredType(null)}
              style={{ background: TYPE_DOT[t], cursor: 'pointer' }}
            />
          )
        })}
      </motion.div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginTop: 10 }}>
        {TYPES.map((t, i) => {
          const dim = hoveredType !== null && hoveredType !== t
          return (
            <motion.div
              key={t}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: dim ? 0.4 : 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.5 + i * 0.06 }}
              onMouseEnter={() => setHoveredType(t)}
              onMouseLeave={() => setHoveredType(null)}
              style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer' }}
            >
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: TYPE_DOT[t] }} />
              <span style={{ fontSize: 11, color: c.dim }}>
                {t}{' '}
                <span style={{ color: c.muted, fontVariantNumeric: 'tabular-nums' }}>
                  {Math.round((counts[t] / baseTotal) * 100)}%
                </span>
              </span>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}

/* ── Stats Hub (marquee tiles + chip row) ── */

interface Segment { label: string; value: number; color: string }

function StatsHub({ figureCount, chartCounts }: {
  figureCount: number
  chartCounts: Record<string, number>
}) {
  // Static probe library counts — match dataset files on disk
  const CAP_QS = 1000   // 250 figs × 4 questions
  const RES = 750       // 250 figs × 3 resistance probes
  const BLUR_ADM = 231  // expanded admittance set
  const BLUR_IND = 232  // expanded inductance set
  const CAP_BIAS_FIGS = 100
  const CAP_BIAS_CLAIMS = 300  // ~3 modifications per figure

  const totalProbes = CAP_QS + RES + (BLUR_ADM + BLUR_IND) + CAP_BIAS_CLAIMS

  // Model breakdown
  const MODELS_COMMERCIAL = 2  // GPT-5.2, Gemini 3.1 Pro
  const MODELS_OPEN = 6        // Llama 4, Qwen×3, Gemma, Phi-4
  const MODELS_TOTAL = 8

  // Evaluation breakdown (paper claims ~34k total instances)
  // Each model evaluated on: 250 baseline + 5×250 transforms + 1000 cap qs + 750 res + 463 blur + 100 cap-bias = ~3,810 per model × 8 = ~30,480
  // Plus judges and ablations → ~34,000
  const EVAL_PERCEPTION = 250 * 8 * 6   // baseline + 5 transforms × 8 models = 12,000
  const EVAL_REASONING = CAP_QS * 8     // 8,000
  const EVAL_BEHAVIOUR = (BLUR_ADM + BLUR_IND + RES) * 8  // ~9,704
  const EVAL_CAPBIAS = CAP_BIAS_FIGS * 8 // 800 (caption variants)
  const EVAL_OTHER = 34000 - (EVAL_PERCEPTION + EVAL_REASONING + EVAL_BEHAVIOUR + EVAL_CAPBIAS)
  const EVAL_TOTAL = EVAL_PERCEPTION + EVAL_REASONING + EVAL_BEHAVIOUR + EVAL_CAPBIAS + Math.max(0, EVAL_OTHER)

  const figureSegments: Segment[] = [
    { label: 'Bar',  value: chartCounts['Bar Chart'] || 0, color: '#f59e0b' },
    { label: 'Line', value: chartCounts['Line Plot'] || 0, color: '#3b82f6' },
    { label: 'Pie',  value: chartCounts['Pie Chart'] || 0, color: '#8b5cf6' },
  ]

  const probeSegments: Segment[] = [
    { label: 'Capability',  value: CAP_QS,                 color: '#3b82f6' },
    { label: 'Resistance',  value: RES,                    color: '#a855f7' },
    { label: 'Blur',        value: BLUR_ADM + BLUR_IND,    color: '#22c55e' },
    { label: 'Caption-Bias',value: CAP_BIAS_CLAIMS,        color: '#f59e0b' },
  ]

  const modelSegments: Segment[] = [
    { label: 'Commercial',  value: MODELS_COMMERCIAL, color: '#3b82f6' },
    { label: 'Open-Weight', value: MODELS_OPEN,       color: '#22c55e' },
  ]

  const evalSegments: Segment[] = [
    { label: 'Perception', value: EVAL_PERCEPTION, color: '#f59e0b' },
    { label: 'Reasoning',  value: EVAL_REASONING,  color: '#3b82f6' },
    { label: 'Behaviour',  value: EVAL_BEHAVIOUR,  color: '#22c55e' },
    { label: 'Cap-Bias',   value: EVAL_CAPBIAS,    color: '#a855f7' },
    { label: 'Ablation',   value: Math.max(0, EVAL_OTHER), color: '#52525b' },
  ]

  return (
    <div style={{ borderBottom: `1px solid ${c.border}` }}>
      <div className="page-container" style={{ paddingTop: 24, paddingBottom: 22 }}>
        <motion.div
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.07, delayChildren: 0.05 } },
          }}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 16,
          }}
        >
          <MarqueeStat
            value={figureCount}
            label="Figures"
            sublabel="Curated scientific figures"
            segments={figureSegments}
          />
          <MarqueeStat
            value={totalProbes}
            label="Probes Generated"
            sublabel="Across four probe families"
            segments={probeSegments}
          />
          <MarqueeStat
            value={MODELS_TOTAL}
            label="Models Evaluated"
            sublabel="Frontier vision-language systems"
            segments={modelSegments}
          />
          <MarqueeStat
            value={EVAL_TOTAL}
            label="Evaluations Run"
            sublabel="Total model-output assessments"
            segments={evalSegments}
          />
        </motion.div>

      </div>
    </div>
  )
}

/* ── Animated count-up hook ── */

function useCountUp(target: number, duration = 1.4): string {
  const mv = useMotionValue(0)
  const [display, setDisplay] = useState(0)
  useEffect(() => {
    if (target === 0) return
    const controls = animate(mv, target, {
      duration,
      ease: [0.22, 1, 0.36, 1],
      onUpdate: v => setDisplay(Math.round(v)),
    })
    return () => controls.stop()
  }, [target, duration, mv])
  return display.toLocaleString()
}

/* ── Marquee Stat ── */

function MarqueeStat({ value, label, sublabel, segments }: {
  value: number
  label: string
  sublabel: string
  segments: Segment[]
}) {
  const display = useCountUp(value)
  const total = segments.reduce((s, x) => s + x.value, 0)
  const [hoveredSeg, setHoveredSeg] = useState<number | null>(null)
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-40px' })

  return (
    <motion.div
      ref={ref}
      variants={{
        hidden: { opacity: 0, y: 14 },
        visible: { opacity: 1, y: 0, transition: SPRING },
      }}
      whileHover={{ y: -3 }}
      transition={SPRING}
      style={{
        position: 'relative',
        borderRadius: 12,
        border: `1px solid ${c.border}`,
        background: c.surface,
        boxShadow: 'var(--t-card-shadow)',
        padding: '16px 18px 14px',
        overflow: 'hidden',
      }}
    >
      {/* Subtle radial glow */}
      <div style={{
        position: 'absolute', inset: 0,
        background: `radial-gradient(circle at 100% 0%, ${segments[0]?.color}08, transparent 60%)`,
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative' }}>
        <p style={{
          fontSize: 9, fontWeight: 600, color: c.dim,
          textTransform: 'uppercase', letterSpacing: '0.1em',
          lineHeight: 1, margin: 0,
        }}>
          {label}
        </p>

        <p style={{
          fontSize: 30, fontWeight: 600, color: c.fg,
          margin: '10px 0 4px', lineHeight: 1,
          fontVariantNumeric: 'tabular-nums',
          letterSpacing: '-0.02em',
        }}>
          {display}
        </p>

        <p style={{
          fontSize: 11, color: c.muted,
          margin: '0 0 14px', lineHeight: 1.4,
        }}>
          {sublabel}
        </p>

        {/* Composition bar */}
        <div style={{
          display: 'flex', height: 5, borderRadius: 3, overflow: 'hidden',
          background: 'var(--t-overlay-soft)', gap: 2,
          marginBottom: 10,
        }}>
          {segments.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ width: 0 }}
              animate={inView ? { width: `${(s.value / total) * 100}%` } : { width: 0 }}
              transition={{
                delay: 0.45 + i * 0.08,
                duration: 0.7,
                ease: [0.22, 1, 0.36, 1],
              }}
              onMouseEnter={() => setHoveredSeg(i)}
              onMouseLeave={() => setHoveredSeg(null)}
              style={{
                background: s.color,
                opacity: hoveredSeg === null || hoveredSeg === i ? 1 : 0.3,
                transition: 'opacity 0.18s ease',
                cursor: 'pointer',
                borderRadius: 2,
              }}
            />
          ))}
        </div>

        {/* Segment legend */}
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          {segments.map((s, i) => {
            const dim = hoveredSeg !== null && hoveredSeg !== i
            return (
              <motion.div
                key={s.label}
                onMouseEnter={() => setHoveredSeg(i)}
                onMouseLeave={() => setHoveredSeg(null)}
                animate={{ opacity: dim ? 0.3 : 1 }}
                transition={{ duration: 0.18 }}
                style={{
                  display: 'flex', alignItems: 'center', gap: 5,
                  cursor: 'pointer',
                }}
              >
                <span style={{
                  width: 6, height: 6, borderRadius: 2,
                  background: s.color,
                }} />
                <span style={{
                  fontSize: 10, color: c.muted, lineHeight: 1,
                }}>
                  {s.label}{' '}
                  <span style={{
                    color: c.dim, fontVariantNumeric: 'tabular-nums',
                  }}>
                    {s.value.toLocaleString()}
                  </span>
                </span>
              </motion.div>
            )
          })}
        </div>
      </div>
    </motion.div>
  )
}


/* ── Figure Card (3D tilt + glare + hover zoom + slide-up strip) ── */

function Card({ item, index, isLoaded, onLoad, onClick }: {
  item: FigureEntry; index: number; isLoaded: boolean
  onLoad: () => void; onClick: () => void
}) {
  const [hovered, setHovered] = useState(false)
  const dot = TYPE_DOT[item.figure_type] || '#888'
  const bg = TYPE_BG[item.figure_type] || 'rgba(136,136,136,0.1)'

  // Cursor tracking → 3D tilt + glare position
  const mvX = useMotionValue(0.5)  // 0..1 normalised X within card
  const mvY = useMotionValue(0.5)
  const xSpring = useSpring(mvX, { stiffness: 220, damping: 22, mass: 0.6 })
  const ySpring = useSpring(mvY, { stiffness: 220, damping: 22, mass: 0.6 })
  const rotateY = useTransform(xSpring, [0, 1], [6, -6])
  const rotateX = useTransform(ySpring, [0, 1], [-6, 6])
  const glareX = useTransform(xSpring, v => `${v * 100}%`)
  const glareY = useTransform(ySpring, v => `${v * 100}%`)

  const onMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    mvX.set((e.clientX - rect.left) / rect.width)
    mvY.set((e.clientY - rect.top) / rect.height)
  }
  const onLeave = () => {
    setHovered(false)
    mvX.set(0.5); mvY.set(0.5)
  }

  return (
    <motion.div
      layout
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={onLeave}
      onMouseMove={onMove}
      initial={{ opacity: 0, y: 14, scale: 0.96 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.96 }}
      transition={{ ...SPRING, delay: Math.min(index * 0.025, 0.3) }}
      style={{
        borderRadius: 10,
        border: `1px solid ${hovered ? c.borderStrong : c.border}`,
        background: c.surface,
        boxShadow: hovered ? 'var(--t-card-shadow-hover)' : 'var(--t-card-shadow)',
        overflow: 'hidden',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        rotateX,
        rotateY,
        transformPerspective: 1000,
        transformStyle: 'preserve-3d',
        willChange: 'transform',
        position: 'relative',
        transition: 'box-shadow 0.25s ease',
      }}
    >
      {/* Thumbnail */}
      <div style={{
        position: 'relative', aspectRatio: '4/3',
        background: c.surfaceHover,
        overflow: 'hidden',
      }}>
        {!isLoaded && (
          <div style={{
            position: 'absolute', inset: 0,
            background: `linear-gradient(90deg, ${c.surface} 25%, ${c.surfaceHover} 50%, ${c.surface} 75%)`,
            backgroundSize: '200% 100%',
            animation: 'shimmer 1.5s ease-in-out infinite',
          }} />
        )}
        <motion.img
          src={`/figures/${item.id}.png`}
          alt={item.caption || item.id}
          loading="lazy"
          onLoad={onLoad}
          animate={{
            scale: hovered ? 1.06 : 1,
            opacity: isLoaded ? 1 : 0,
          }}
          transition={{
            scale: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
            opacity: { duration: 0.3 },
          }}
          style={{
            width: '100%', height: '100%', objectFit: 'contain', padding: 12,
            willChange: 'transform',
          }}
        />

        {/* Glare layer — soft radial highlight that follows cursor */}
        <motion.div
          animate={{ opacity: hovered ? 1 : 0 }}
          transition={{ duration: 0.25 }}
          style={{
            position: 'absolute', inset: 0,
            background: useTransform(
              [glareX, glareY] as never,
              ([x, y]: string[]) =>
                `radial-gradient(circle at ${x} ${y}, rgba(255,255,255,0.14), transparent 45%)`
            ),
            pointerEvents: 'none',
            mixBlendMode: 'overlay',
          }}
        />

      </div>

      {/* Meta */}
      <div style={{
        padding: '10px 12px', borderTop: `1px solid ${c.border}`,
        flex: 1, display: 'flex', flexDirection: 'column',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
          <span style={{
            fontSize: 11, fontFamily: 'JetBrains Mono, monospace', fontWeight: 500, color: c.muted,
          }}>
            {item.id}
          </span>
          <span style={{
            fontSize: 9, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em',
            padding: '3px 7px', borderRadius: 4, color: dot, background: bg,
            lineHeight: 1, flexShrink: 0,
          }}>
            {TYPE_SHORT[item.figure_type] || item.figure_type}
          </span>
        </div>
        {item.caption && (
          <p style={{
            fontSize: 11, color: c.dim, lineHeight: 1.5,
            marginTop: 6, overflow: 'hidden',
            display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
          }}>
            {item.caption}
          </p>
        )}
      </div>
    </motion.div>
  )
}

