import { useState, useEffect } from 'react'
import { motion, AnimatePresence, LayoutGroup } from 'motion/react'
import ModelLollipopChart from './ModelLollipopChart'
import {
  CAPABILITY, RESISTANCE, ADMITTANCE, INDUCTANCE,
} from '../../data/landing_data'

const c = {
  bg: 'var(--t-bg)',
  surface: 'var(--t-surface)',
  surfaceRaised: 'var(--t-surface-raised)',
  border: 'var(--t-border)',
  borderStrong: 'var(--t-border-strong)',
  fg: 'var(--t-fg)',
  muted: 'var(--t-muted)',
  dim: 'var(--t-dim)',
}

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }

const FIG_ID = 'fig_064'   // Paper-hook figure (Academic Funding bar chart, all 4 probe families)

type Family = 'capability' | 'resistance' | 'caption_bias' | 'blur'
type CapKey = keyof typeof CAPABILITY['gemini']
type ResKey = 'inexist' | 'contra' | 'unanswerable'
type BlurKey = 'admittance' | 'inductance'

const FAMILY_META: Record<Family, { label: string; color: string }> = {
  capability:   { label: 'Capability',     color: '#3b82f6' },
  resistance:   { label: 'Resistance',     color: '#a855f7' },
  caption_bias: { label: 'Caption Bias',   color: '#f59e0b' },
  blur:         { label: 'Selective Blur', color: '#22c55e' },
}

const CAP_SUBTYPES: Array<{ key: CapKey; label: string }> = [
  { key: 'counting',         label: 'Counting' },
  { key: 'computation',      label: 'Computation' },
  { key: 'comparison',       label: 'Comparison' },
  { key: 'pattern_analysis', label: 'Pattern' },
]

const RES_SUBTYPES: Array<{ key: ResKey; label: string }> = [
  { key: 'inexist',      label: 'Inexist' },
  { key: 'contra',       label: 'Contra' },
  { key: 'unanswerable', label: 'Unanswerable' },
]

const BLUR_SUBTYPES: Array<{ key: BlurKey; label: string }> = [
  { key: 'admittance', label: 'Admittance' },
  { key: 'inductance', label: 'Inductance' },
]

// Worked examples grounded in fig_064 — horizontal bar chart of deception
// counts across 4 categories (Academic Collaboration, Recruitment, Academic Funding,
// Journalism), broken down by Yes / Partially / No.
const CAP_EXAMPLES: Record<CapKey, { question: string; expected: string }> = {
  counting: {
    question: "How many bars across all categories represent conversations where deception was 'Partially' perceived and the number of conversations exceeds 20?",
    expected: '2',
  },
  computation: {
    question: "What is the difference between the average number of conversations categorized as 'No' across all categories and the average number categorized as 'Partially'?",
    expected: '≈ 21',
  },
  comparison: {
    question: "Is the 'Yes' segment in Academic Funding more than twice as long as the 'Yes' segment in Recruitment?",
    expected: 'No — roughly 1.7×',
  },
  pattern_analysis: {
    question: "Which category exhibits a consistent pattern where the 'Yes' bar is always longer than both 'Partially' and 'No' bars?",
    expected: 'Academic Funding · Recruitment',
  },
}

const RES_EXAMPLES: Record<ResKey, { question: string; expected: string; principle: string }> = {
  inexist: {
    question: "The benchmark line for the expected number of conversations appears to be set at 30. How does the number of conversations in the 'Academic Funding' category compare to this benchmark?",
    expected: 'Refuse: no benchmark line exists in this chart.',
    principle: 'presupposition embedding',
  },
  contra: {
    question: "Given that the 'Journalism' category has 30 conversations marked as 'Partially deceived', how does this compare to the 'Academic Collaboration' category for the same level of deception?",
    expected: "Reject the 30 anchor — Journalism's 'Partially' value is closer to 48.",
    principle: 'anchoring',
  },
  unanswerable: {
    question: 'What is the statistical significance of the differences in the number of conversations across the categories, and does the variance in responses affect the reliability of the data?',
    expected: 'Significance + variance cannot be inferred from this chart.',
    principle: 'domain conventions',
  },
}

const CAP_BIAS_EXAMPLE = {
  claim: "For 'Journalism,' the 'Yes' and 'No' segments are roughly equal at 15 each.",
  reality: "The 'Yes' segment is approximately 15, but the 'No' segment is closer to 6, making them clearly unequal.",
  type: 'value_anchor · anchoring',
}

const BLUR_EXAMPLES: Record<BlurKey, { question: string; blurred: string; expected: string }> = {
  admittance: {
    question: "Which category has the highest number of conversations marked as 'Yes' for being deceived?",
    blurred: '"Academic Funding" (category label of the longest red bar)',
    expected: 'Admit the category label of the longest Yes bar is unreadable.',
  },
  inductance: {
    question: 'Which "Deceived" option occurs in the least number of conversations across all four categories?',
    blurred: '"No" (legend entry · third colour)',
    expected: 'Infer from the legend colour sequence: the third entry corresponds to the green bars (lowest counts).',
  },
}

export default function FigureProbeExplorer({ onExploreDataset }: { onExploreDataset?: () => void }) {
  const [family, setFamily] = useState<Family>('capability')
  const [capKey, setCapKey] = useState<CapKey>('counting')
  const [resKey, setResKey] = useState<ResKey>('inexist')
  const [blurKey, setBlurKey] = useState<BlurKey>('admittance')

  // Preload variants for the image
  useEffect(() => {
    [
      `/figures/${FIG_ID}.png`,
      `/adversarial_admittance/${FIG_ID}.png`,
      `/adversarial_inductance/${FIG_ID}.png`,
    ].forEach(src => {
      const img = new Image()
      img.decoding = 'async'
      img.src = src
    })
  }, [])

  // Figure variant shown depends on the active tab
  const figureSrc = family === 'blur'
    ? (blurKey === 'admittance' ? `/adversarial_admittance/${FIG_ID}.png` : `/adversarial_inductance/${FIG_ID}.png`)
    : `/figures/${FIG_ID}.png`

  // Chart values per probe
  const chartValues: Record<string, number> = (() => {
    if (family === 'capability') {
      return Object.fromEntries(
        Object.entries(CAPABILITY).map(([id, row]) => [id, row[capKey]])
      )
    }
    if (family === 'resistance') {
      return Object.fromEntries(
        Object.entries(RESISTANCE).map(([id, row]) => [id, row[resKey]])
      )
    }
    if (family === 'caption_bias') {
      return Object.fromEntries(
        Object.entries(RESISTANCE).map(([id, row]) => [id, row.caption_bias])
      )
    }
    // blur
    const src = blurKey === 'admittance' ? ADMITTANCE : INDUCTANCE
    return Object.fromEntries(
      Object.entries(src).map(([id, row]) => [id, row.active])
    )
  })()

  const chartMax = family === 'resistance' || family === 'caption_bias' ? 1 : 100
  const chartUnit = (() => {
    if (family === 'capability') return `Capability accuracy on ${CAP_SUBTYPES.find(s => s.key === capKey)?.label.toLowerCase()} (%)`
    if (family === 'resistance') return `${RES_SUBTYPES.find(s => s.key === resKey)?.label} resistance (0–1)`
    if (family === 'caption_bias') return 'Caption-bias resistance (0–1)'
    return `Active ${blurKey} (% of probes)`
  })()

  const familyAccent = FAMILY_META[family].color

  return (
    <div style={{
      borderRadius: 14, border: `1px solid ${c.border}`,
      background: c.surface, overflow: 'hidden',
    }}>
      {/* Header — figure id + family tabs */}
      <div style={{
        padding: '14px 18px',
        borderBottom: `1px solid ${c.border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        gap: 16, flexWrap: 'wrap',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{
            fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.08em', color: c.dim,
          }}>
            Anchored figure
          </span>
          <span style={{
            fontSize: 11.5, fontWeight: 600, color: c.fg,
            fontFamily: 'JetBrains Mono, monospace',
            padding: '3px 8px', borderRadius: 4,
            background: c.surfaceRaised, border: `1px solid ${c.border}`,
            lineHeight: 1,
          }}>
            {FIG_ID}
          </span>
          <span style={{ fontSize: 11, color: c.muted }}>· Bar chart · Deception counts across 4 categories</span>
        </div>

        <LayoutGroup id="explorer-family">
          <div style={{
            display: 'flex', gap: 2, padding: 4,
            borderRadius: 9, background: c.bg,
            border: `1px solid ${c.border}`,
          }}>
            {(['capability', 'resistance', 'caption_bias', 'blur'] as const).map(f => {
              const isActive = f === family
              const meta = FAMILY_META[f]
              return (
                <motion.button
                  key={f}
                  onClick={() => setFamily(f)}
                  whileTap={{ scale: 0.96 }}
                  transition={SPRING}
                  style={{
                    position: 'relative',
                    padding: '7px 13px', borderRadius: 6,
                    background: 'none', border: 'none', cursor: 'pointer',
                    fontFamily: 'inherit', fontSize: 11.5, fontWeight: 500,
                    zIndex: 1,
                    display: 'flex', alignItems: 'center', gap: 7,
                  }}
                >
                  {isActive && (
                    <motion.span
                      layoutId="explorer-family-pill"
                      transition={SPRING}
                      style={{
                        position: 'absolute', inset: 0,
                        borderRadius: 6,
                        background: `${meta.color}18`,
                        border: `1px solid ${meta.color}40`,
                        zIndex: -1,
                      }}
                    />
                  )}
                  <span style={{
                    width: 5, height: 5, borderRadius: '50%', background: meta.color,
                  }} />
                  <motion.span
                    animate={{ color: isActive ? c.fg : c.muted }}
                    transition={{ duration: 0.18 }}
                  >
                    {meta.label}
                  </motion.span>
                </motion.button>
              )
            })}
          </div>
        </LayoutGroup>
      </div>

      {/* Body — image left, probe right */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 0 }}>
        {/* Image */}
        <div style={{
          position: 'relative',
          borderRight: `1px solid ${c.border}`,
          padding: 24,
          background: c.bg,
          minHeight: 320,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          overflow: 'hidden',
        }}>
          <AnimatePresence initial={false}>
            <motion.img
              key={figureSrc}
              src={figureSrc}
              alt={`${FIG_ID} ${family === 'blur' ? blurKey + ' blur' : 'original'}`}
              decoding="async"
              fetchPriority="high"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2, ease: 'easeOut' }}
              style={{
                position: 'absolute',
                top: 24, left: 24, right: 24, bottom: 24,
                margin: 'auto',
                maxWidth: 'calc(100% - 48px)', maxHeight: 380, objectFit: 'contain',
              }}
            />
          </AnimatePresence>
          <img
            src={figureSrc}
            alt=""
            aria-hidden
            style={{ maxWidth: '100%', maxHeight: 380, objectFit: 'contain', visibility: 'hidden' }}
          />
          {family === 'blur' && (
            <motion.span
              key={blurKey}
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={SPRING}
              style={{
                position: 'absolute', top: 14, left: 14,
                fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.08em',
                padding: '4px 9px', borderRadius: 4,
                background: blurKey === 'admittance'
                  ? 'rgba(239,68,68,0.12)' : 'rgba(34,197,94,0.12)',
                color: blurKey === 'admittance' ? '#ef4444' : '#22c55e',
                border: `1px solid ${blurKey === 'admittance' ? 'rgba(239,68,68,0.25)' : 'rgba(34,197,94,0.25)'}`,
                backdropFilter: 'blur(8px)',
                lineHeight: 1,
              }}
            >
              {blurKey === 'admittance' ? 'Unrecoverable blur' : 'Inferable blur'}
            </motion.span>
          )}
        </div>

        {/* Probe details */}
        <div style={{
          padding: 22,
          display: 'flex', flexDirection: 'column', gap: 14,
        }}>
          {/* Subtype chips */}
          {family === 'capability' && (
            <SubChips
              options={CAP_SUBTYPES}
              active={capKey}
              onSelect={k => setCapKey(k as CapKey)}
              accent={familyAccent}
            />
          )}
          {family === 'resistance' && (
            <SubChips
              options={RES_SUBTYPES}
              active={resKey}
              onSelect={k => setResKey(k as ResKey)}
              accent={familyAccent}
            />
          )}
          {family === 'blur' && (
            <SubChips
              options={BLUR_SUBTYPES}
              active={blurKey}
              onSelect={k => setBlurKey(k as BlurKey)}
              accent={familyAccent}
            />
          )}

          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={`${family}-${capKey}-${resKey}-${blurKey}`}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
              style={{ display: 'flex', flexDirection: 'column', gap: 12 }}
            >
              {family === 'capability' && <CapabilityCard capKey={capKey} />}
              {family === 'resistance' && <ResistanceCard resKey={resKey} />}
              {family === 'caption_bias' && <CaptionBiasCard />}
              {family === 'blur' && <BlurCard blurKey={blurKey} />}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Chart */}
      <div style={{
        padding: '22px 24px',
        borderTop: `1px solid ${c.border}`,
        background: c.bg,
      }}>
        <p style={{
          fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.08em', color: c.dim,
          margin: '0 0 14px', lineHeight: 1,
        }}>
          Per-model performance
        </p>
        <ModelLollipopChart
          values={chartValues}
          max={chartMax}
          accent={familyAccent}
          unit={chartUnit}
        />
      </div>

      {/* CTA */}
      {onExploreDataset && (
        <button
          onClick={onExploreDataset}
          style={{
            width: '100%',
            padding: '12px 22px',
            borderTop: `1px solid ${c.border}`,
            background: c.surface, border: 'none', cursor: 'pointer',
            fontFamily: 'inherit', fontSize: 12, fontWeight: 500,
            color: c.fg,
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 7,
            transition: 'background 0.18s',
          }}
          onMouseEnter={e => e.currentTarget.style.background = c.surfaceRaised}
          onMouseLeave={e => e.currentTarget.style.background = c.surface}
        >
          Browse every probe across all 250 figures in the dataset explorer
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
            <path d="M4 2.5l3.5 3.5L4 9.5" />
          </svg>
        </button>
      )}
    </div>
  )
}

/* ── Sub-tab chips ── */

function SubChips({ options, active, onSelect, accent }: {
  options: Array<{ key: string; label: string }>
  active: string
  onSelect: (k: string) => void
  accent: string
}) {
  return (
    <LayoutGroup id={`explorer-sub-${options[0].key}`}>
      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
        {options.map(opt => {
          const isActive = opt.key === active
          return (
            <motion.button
              key={opt.key}
              onClick={() => onSelect(opt.key)}
              whileTap={{ scale: 0.96 }}
              transition={SPRING}
              style={{
                position: 'relative',
                padding: '5px 11px', borderRadius: 6,
                background: 'none', border: 'none', cursor: 'pointer',
                fontFamily: 'inherit', fontSize: 11, fontWeight: 500,
                zIndex: 1,
              }}
            >
              {isActive && (
                <motion.span
                  layoutId={`subchip-pill-${options[0].key}`}
                  transition={SPRING}
                  style={{
                    position: 'absolute', inset: 0,
                    borderRadius: 6,
                    background: `${accent}15`,
                    border: `1px solid ${accent}35`,
                    zIndex: -1,
                  }}
                />
              )}
              <motion.span
                animate={{ color: isActive ? c.fg : c.muted }}
                transition={{ duration: 0.18 }}
              >
                {opt.label}
              </motion.span>
            </motion.button>
          )
        })}
      </div>
    </LayoutGroup>
  )
}

/* ── Probe-specific cards ── */

function ProbeRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <p style={{
        fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: c.dim,
        margin: '0 0 5px', lineHeight: 1,
      }}>
        {label}
      </p>
      {children}
    </div>
  )
}

function CapabilityCard({ capKey }: { capKey: CapKey }) {
  const ex = CAP_EXAMPLES[capKey]
  return (
    <ProbeRow label="Question">
      <p style={{
        fontSize: 13, color: c.fg, lineHeight: 1.55, margin: 0,
        fontStyle: 'italic',
      }}>
        "{ex.question}"
      </p>
    </ProbeRow>
  )
}

function ResistanceCard({ resKey }: { resKey: ResKey }) {
  const ex = RES_EXAMPLES[resKey]
  return (
    <>
      <ProbeRow label="Probe question">
        <p style={{
          fontSize: 13, color: c.fg, lineHeight: 1.55, margin: 0,
          fontStyle: 'italic',
        }}>
          "{ex.question}"
        </p>
      </ProbeRow>
      <ProbeRow label="Expected behaviour">
        <p style={{ fontSize: 12.5, color: c.muted, lineHeight: 1.55, margin: 0 }}>
          {ex.expected}
        </p>
      </ProbeRow>
      <ProbeRow label="Deception principle">
        <span style={{
          display: 'inline-block',
          fontSize: 11, color: c.muted,
          padding: '3px 8px', borderRadius: 4,
          background: c.surfaceRaised, border: `1px solid ${c.border}`,
          textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600,
        }}>
          {ex.principle}
        </span>
      </ProbeRow>
    </>
  )
}

function CaptionBiasCard() {
  return (
    <>
      <ProbeRow label="Modified caption claim">
        <p style={{
          fontSize: 13, color: '#fcd34d', lineHeight: 1.55, margin: 0,
          fontStyle: 'italic',
        }}>
          "{CAP_BIAS_EXAMPLE.claim}"
        </p>
      </ProbeRow>
      <ProbeRow label="Reality">
        <p style={{ fontSize: 12.5, color: '#86efac', lineHeight: 1.55, margin: 0 }}>
          {CAP_BIAS_EXAMPLE.reality}
        </p>
      </ProbeRow>
      <ProbeRow label="Bias type">
        <span style={{
          display: 'inline-block',
          fontSize: 11, color: c.muted,
          padding: '3px 8px', borderRadius: 4,
          background: c.surfaceRaised, border: `1px solid ${c.border}`,
          textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600,
        }}>
          {CAP_BIAS_EXAMPLE.type}
        </span>
      </ProbeRow>
    </>
  )
}

function BlurCard({ blurKey }: { blurKey: BlurKey }) {
  const ex = BLUR_EXAMPLES[blurKey]
  return (
    <>
      <ProbeRow label="Probe question">
        <p style={{
          fontSize: 13, color: c.fg, lineHeight: 1.55, margin: 0,
          fontStyle: 'italic',
        }}>
          "{ex.question}"
        </p>
      </ProbeRow>
      <ProbeRow label={blurKey === 'admittance' ? 'Blurred element (unrecoverable)' : 'Blurred element (inferable)'}>
        <span style={{
          display: 'inline-block',
          fontSize: 12.5,
          color: blurKey === 'admittance' ? '#fca5a5' : '#86efac',
          padding: '4px 10px', borderRadius: 5,
          background: blurKey === 'admittance' ? 'rgba(239,68,68,0.08)' : 'rgba(34,197,94,0.08)',
          border: `1px solid ${blurKey === 'admittance' ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)'}`,
          fontFamily: 'JetBrains Mono, monospace',
        }}>
          {ex.blurred}
        </span>
      </ProbeRow>
      <ProbeRow label="Expected behaviour">
        <p style={{ fontSize: 12.5, color: c.muted, lineHeight: 1.55, margin: 0 }}>
          {ex.expected}
        </p>
      </ProbeRow>
    </>
  )
}
