import { useState, useRef } from 'react'
import { motion, AnimatePresence, useInView } from 'motion/react'
import { MODELS, RESISTANCE, overallResistance } from '../../data/landing_data'

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

const PROBE_META = {
  inexist:      { label: 'Inexist',      color: '#a855f7' },
  contra:       { label: 'Contra',       color: '#f97316' },
  unanswerable: { label: 'Unanswerable', color: '#06b6d4' },
}

export default function ResistanceLadder() {
  const [expanded, setExpanded] = useState<string | null>(null)
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  // Sort models by overall resistance descending
  const rows = MODELS
    .map(m => ({
      id: m.id, name: m.short, color: m.color,
      overall: overallResistance(m.id),
      breakdown: RESISTANCE[m.id],
    }))
    .sort((a, b) => b.overall - a.overall)

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '24px 24px 22px',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {rows.map((row, i) => {
          const pct = row.overall * 100
          const isOpen = expanded === row.id
          return (
            <motion.div
              key={row.id}
              layout
              transition={{ type: 'spring' as const, stiffness: 280, damping: 28 }}
            >
              <motion.div
                onClick={() => setExpanded(isOpen ? null : row.id)}
                whileHover={{ x: 2 }}
                style={{
                  display: 'grid', gridTemplateColumns: '120px 1fr 64px 20px',
                  gap: 12, alignItems: 'center',
                  cursor: 'pointer', padding: '4px 0',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{
                    width: 7, height: 7, borderRadius: '50%', background: row.color,
                  }} />
                  <span style={{ fontSize: 12.5, color: c.fg, fontWeight: 500 }}>
                    {row.name}
                  </span>
                </div>

                <div style={{
                  position: 'relative', height: 9,
                  borderRadius: 5,
                  background: 'var(--t-overlay-soft)',
                  overflow: 'hidden',
                }}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={inView ? { width: `${pct}%` } : {}}
                    transition={{ delay: 0.12 + i * 0.06, duration: 0.85, ease: [0.22, 1, 0.36, 1] }}
                    style={{
                      height: '100%',
                      background: pct >= 75 ? '#22c55e' : pct >= 50 ? '#f59e0b' : pct >= 35 ? '#fb923c' : '#ef4444',
                      borderRadius: 5,
                    }}
                  />
                </div>

                <span style={{
                  fontSize: 12.5, fontWeight: 600, color: c.fg,
                  fontVariantNumeric: 'tabular-nums',
                  textAlign: 'right',
                  letterSpacing: '-0.01em',
                }}>
                  {row.overall.toFixed(2)}
                </span>

                <motion.svg
                  animate={{ rotate: isOpen ? 180 : 0 }}
                  transition={{ type: 'spring' as const, stiffness: 320, damping: 28 }}
                  width="11" height="11" viewBox="0 0 12 12"
                  fill="none" stroke={c.dim} strokeWidth="1.5" strokeLinecap="round"
                >
                  <path d="M3 4.5l3 3 3-3" />
                </motion.svg>
              </motion.div>

              <AnimatePresence initial={false}>
                {isOpen && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
                    style={{ overflow: 'hidden' }}
                  >
                    <div style={{
                      marginTop: 8, marginLeft: 132, marginRight: 100,
                      padding: '12px 14px', borderRadius: 8,
                      background: c.bg, border: `1px solid ${c.border}`,
                    }}>
                      <p style={{
                        fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                        letterSpacing: '0.06em', color: c.dim,
                        margin: '0 0 8px',
                      }}>
                        Breakdown by probe type
                      </p>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {(['inexist', 'contra', 'unanswerable'] as const).map(k => (
                          <div key={k} style={{
                            display: 'grid', gridTemplateColumns: '90px 1fr 40px',
                            gap: 10, alignItems: 'center',
                          }}>
                            <span style={{
                              fontSize: 11, color: c.muted,
                              display: 'flex', alignItems: 'center', gap: 5,
                            }}>
                              <span style={{
                                width: 5, height: 5, borderRadius: '50%',
                                background: PROBE_META[k].color,
                              }} />
                              {PROBE_META[k].label}
                            </span>
                            <div style={{
                              height: 5, borderRadius: 3,
                              background: 'var(--t-overlay-soft)',
                              overflow: 'hidden',
                            }}>
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${row.breakdown[k] * 100}%` }}
                                transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                                style={{ height: '100%', background: PROBE_META[k].color, opacity: 0.85 }}
                              />
                            </div>
                            <span style={{
                              fontSize: 11, color: c.muted, fontWeight: 600,
                              fontVariantNumeric: 'tabular-nums',
                              textAlign: 'right',
                            }}>
                              {row.breakdown[k].toFixed(2)}
                            </span>
                          </div>
                        ))}
                        <div style={{
                          display: 'grid', gridTemplateColumns: '90px 1fr 40px',
                          gap: 10, alignItems: 'center',
                          paddingTop: 6, borderTop: `1px solid ${c.border}`,
                          marginTop: 4,
                        }}>
                          <span style={{
                            fontSize: 11, color: c.muted,
                            display: 'flex', alignItems: 'center', gap: 5,
                          }}>
                            <span style={{
                              width: 5, height: 5, borderRadius: '50%',
                              background: '#f59e0b',
                            }} />
                            Caption Bias
                          </span>
                          <div style={{
                            height: 5, borderRadius: 3,
                            background: 'var(--t-overlay-soft)',
                            overflow: 'hidden',
                          }}>
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${row.breakdown.caption_bias * 100}%` }}
                              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.1 }}
                              style={{ height: '100%', background: '#f59e0b', opacity: 0.85 }}
                            />
                          </div>
                          <span style={{
                            fontSize: 11, color: c.muted, fontWeight: 600,
                            fontVariantNumeric: 'tabular-nums',
                            textAlign: 'right',
                          }}>
                            {row.breakdown.caption_bias.toFixed(2)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </div>

      <p style={{
        marginTop: 16, paddingTop: 14,
        borderTop: `1px solid ${c.border}`,
        fontSize: 11, color: c.dim, lineHeight: 1.55, margin: 0,
      }}>
        Overall resistance is the mean of three probe types. Click any row to see the per-probe breakdown — including caption-bias resistance (orange).
      </p>
    </div>
  )
}
