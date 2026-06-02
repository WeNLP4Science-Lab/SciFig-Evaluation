import { useState } from 'react'
import { motion, AnimatePresence, LayoutGroup } from 'motion/react'

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

type ProbeFamily = 'capability' | 'resistance' | 'caption_bias' | 'blur'

interface ProbeExample {
  family: ProbeFamily
  tab: string
  subtype: string
  figure_id: string
  chart_type: string
  question: string
  expected_answer?: string
  reality?: string            // for caption-bias
  expected_behavior?: string  // for resistance / blur
  principle?: string          // for resistance
  best:  { model: string; score: string }
  worst: { model: string; score: string }
  scoreUnit: string           // e.g. '%', 'resistance', etc.
}

const EXAMPLES: Record<ProbeFamily, ProbeExample> = {
  capability: {
    family: 'capability',
    tab: 'Capability',
    subtype: 'Counting',
    figure_id: 'fig_001',
    chart_type: 'Bar Chart',
    question: "Which model scores 90.0 in chart (b) for MATH-500 and 63.6 in chart (e) for AIME24?",
    expected_answer: "o1-mini",
    best:  { model: 'Gemini 3.1 Pro', score: '89.2%' },
    worst: { model: 'Phi-4 Multimodal', score: '13.0%' },
    scoreUnit: 'accuracy on counting',
  },
  resistance: {
    family: 'resistance',
    tab: 'Resistance',
    subtype: 'Inexist · presupposition embedding',
    figure_id: 'fig_001',
    chart_type: 'Bar Chart',
    question: "The error bars in chart (b) seem to indicate a wider range for the o1-mini model compared to DeepSeek-R1-Distill-1.5B — does this suggest greater variability in its performance?",
    expected_behavior: "Recognise that error bars are not present in the chart and refuse to assess variability from the given data.",
    principle: "presupposition_embedding, co_occurrence",
    best:  { model: 'Gemini 3.1 Pro', score: '0.88' },
    worst: { model: 'Phi-4 Multimodal', score: '0.04' },
    scoreUnit: 'inexist resistance',
  },
  caption_bias: {
    family: 'caption_bias',
    tab: 'Caption Bias',
    subtype: 'Modified caption · value anchor',
    figure_id: 'fig_002',
    chart_type: 'Bar Chart',
    question: "In the SMD dataset, the green bar reaches approximately 95%, while the purple bar is the shortest, at around 85%.",
    reality: "The green bar in the SMD dataset is approximately 93%, and the purple bar is closer to 90%, not 85%.",
    best:  { model: 'Gemini 3.1 Pro · GPT-5.2', score: '0.89' },
    worst: { model: 'Phi-4 Multimodal', score: '0.05' },
    scoreUnit: 'caption-bias resistance',
  },
  blur: {
    family: 'blur',
    tab: 'Selective Blur',
    subtype: 'Admittance · unrecoverable label',
    figure_id: 'fig_064',
    chart_type: 'Bar Chart',
    question: "Which category has the highest number of conversations marked as 'Yes' for being deceived?",
    expected_behavior: "Admit the relevant label is blurred and cannot be read from the figure.",
    best:  { model: 'Gemini 3.1 Pro', score: '71%' },
    worst: { model: 'Phi-4 Multimodal', score: '5%' },
    scoreUnit: 'admittance rate',
  },
}

const TAB_COLORS: Record<ProbeFamily, string> = {
  capability:   '#3b82f6',
  resistance:   '#a855f7',
  caption_bias: '#f59e0b',
  blur:         '#22c55e',
}

const TABS: ProbeFamily[] = ['capability', 'resistance', 'caption_bias', 'blur']

export default function ProbeLibrary({ onExploreDataset }: { onExploreDataset?: () => void }) {
  const [active, setActive] = useState<ProbeFamily>('capability')
  const current = EXAMPLES[active]

  return (
    <div style={{
      borderRadius: 14, border: `1px solid ${c.border}`,
      background: c.surface, overflow: 'hidden',
    }}>
      {/* Tab strip */}
      <div style={{
        padding: '14px 16px',
        borderBottom: `1px solid ${c.border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        gap: 16, flexWrap: 'wrap',
      }}>
        <LayoutGroup id="probe-library-tabs">
          <div style={{
            display: 'flex', gap: 2, padding: 4,
            borderRadius: 9,
            background: c.bg,
            border: `1px solid ${c.border}`,
          }}>
            {TABS.map(t => {
              const isActive = t === active
              const color = TAB_COLORS[t]
              return (
                <motion.button
                  key={t}
                  onClick={() => setActive(t)}
                  whileTap={{ scale: 0.96 }}
                  transition={SPRING}
                  style={{
                    position: 'relative',
                    padding: '7px 14px', borderRadius: 6,
                    background: 'none', border: 'none', cursor: 'pointer',
                    fontFamily: 'inherit', fontSize: 11.5, fontWeight: 500,
                    zIndex: 1,
                    display: 'flex', alignItems: 'center', gap: 7,
                  }}
                >
                  {isActive && (
                    <motion.span
                      layoutId="probe-tab-pill"
                      transition={SPRING}
                      style={{
                        position: 'absolute', inset: 0,
                        borderRadius: 6,
                        background: `${color}18`,
                        border: `1px solid ${color}40`,
                        zIndex: -1,
                      }}
                    />
                  )}
                  <span style={{
                    width: 5, height: 5, borderRadius: '50%', background: color,
                  }} />
                  <motion.span
                    animate={{ color: isActive ? c.fg : c.muted }}
                    transition={{ duration: 0.18 }}
                  >
                    {EXAMPLES[t].tab}
                  </motion.span>
                </motion.button>
              )
            })}
          </div>
        </LayoutGroup>

        <span style={{
          fontSize: 11, color: c.dim,
        }}>
          Worked example · real probe text
        </span>
      </div>

      {/* Body */}
      <div style={{ padding: '22px 24px' }}>
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={active}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* Meta line */}
            <div style={{
              display: 'flex', alignItems: 'center', gap: 10,
              flexWrap: 'wrap', marginBottom: 18,
            }}>
              <MetaPill label="Type"      value={current.subtype} accent={TAB_COLORS[current.family]} />
              <MetaPill label="Figure"    value={current.figure_id} mono />
              <MetaPill label="Chart"     value={current.chart_type} />
              {current.principle && (
                <MetaPill label="Principle" value={current.principle.split(',').map(s => s.trim().replace(/_/g, ' ')).join(' · ')} />
              )}
            </div>

            {/* Probe content */}
            <ProbeRow label={current.family === 'caption_bias' ? 'Modified caption claim' : 'Probe question'}>
              <p style={{
                fontSize: 14, color: c.fg, lineHeight: 1.6, margin: 0,
                fontStyle: 'italic',
              }}>
                "{current.question}"
              </p>
            </ProbeRow>

            {current.expected_answer && (
              <ProbeRow label="Expected answer">
                <span style={{
                  display: 'inline-block',
                  fontSize: 13, color: '#86efac',
                  padding: '4px 10px', borderRadius: 5,
                  background: 'rgba(34,197,94,0.08)',
                  border: '1px solid rgba(34,197,94,0.2)',
                  fontFamily: 'JetBrains Mono, monospace',
                }}>
                  {current.expected_answer}
                </span>
              </ProbeRow>
            )}

            {current.reality && (
              <ProbeRow label="Reality">
                <p style={{
                  fontSize: 13, color: '#86efac', lineHeight: 1.55, margin: 0,
                }}>
                  {current.reality}
                </p>
              </ProbeRow>
            )}

            {current.expected_behavior && (
              <ProbeRow label="Expected behaviour">
                <p style={{
                  fontSize: 13, color: c.muted, lineHeight: 1.6, margin: 0,
                }}>
                  {current.expected_behavior}
                </p>
              </ProbeRow>
            )}

            {/* Best / worst comparison */}
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10,
              marginTop: 18, paddingTop: 18, borderTop: `1px solid ${c.border}`,
            }}>
              <ScoreCard
                label="Best"
                model={current.best.model}
                score={current.best.score}
                unit={current.scoreUnit}
                color="#22c55e"
              />
              <ScoreCard
                label="Worst"
                model={current.worst.model}
                score={current.worst.score}
                unit={current.scoreUnit}
                color="#ef4444"
              />
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* CTA strip */}
      {onExploreDataset && (
        <button
          onClick={onExploreDataset}
          style={{
            width: '100%',
            padding: '12px 22px',
            borderTop: `1px solid ${c.border}`,
            background: c.bg, border: 'none', cursor: 'pointer',
            fontFamily: 'inherit', fontSize: 12, fontWeight: 500,
            color: c.fg,
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 7,
            transition: 'background 0.18s',
          }}
          onMouseEnter={e => e.currentTarget.style.background = c.surfaceRaised}
          onMouseLeave={e => e.currentTarget.style.background = c.bg}
        >
          Browse every probe in the dataset explorer
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
            <path d="M4 2.5l3.5 3.5L4 9.5" />
          </svg>
        </button>
      )}
    </div>
  )
}

function MetaPill({ label, value, mono, accent }: {
  label: string; value: string; mono?: boolean; accent?: string
}) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 6,
      fontSize: 10.5, lineHeight: 1.3,
    }}>
      <span style={{
        fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.07em', color: c.dim,
      }}>
        {label}
      </span>
      <span style={{
        fontSize: 11, fontWeight: 500,
        color: accent || c.fg,
        fontFamily: mono ? 'JetBrains Mono, monospace' : 'inherit',
      }}>
        {value}
      </span>
    </div>
  )
}

function ProbeRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ marginTop: 12 }}>
      <p style={{
        fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: c.dim,
        margin: '0 0 6px', lineHeight: 1,
      }}>
        {label}
      </p>
      {children}
    </div>
  )
}

function ScoreCard({ label, model, score, unit, color }: {
  label: string; model: string; score: string; unit: string; color: string
}) {
  return (
    <div style={{
      padding: '12px 14px',
      borderRadius: 8,
      background: c.bg,
      border: `1px solid ${c.border}`,
    }}>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8,
      }}>
        <span style={{ width: 6, height: 6, borderRadius: '50%', background: color }} />
        <span style={{
          fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.08em', color,
        }}>
          {label}
        </span>
      </div>
      <p style={{
        fontSize: 18, fontWeight: 600, color: c.fg,
        margin: '0 0 4px', lineHeight: 1,
        fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.015em',
      }}>
        {score}
      </p>
      <p style={{
        fontSize: 11.5, color: c.muted, margin: '0 0 2px',
        fontWeight: 500,
      }}>
        {model}
      </p>
      <p style={{ fontSize: 10, color: c.dim, margin: 0 }}>
        {unit}
      </p>
    </div>
  )
}
