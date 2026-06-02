import { useRef, useState } from 'react'
import { motion, useInView } from 'motion/react'
import { CROSS_DIM, CROSS_DIM_LABELS } from '../../data/landing_data'

const c = {
  surface: 'var(--t-surface)',
  surfaceRaised: 'var(--t-surface-raised)',
  border: 'var(--t-border)',
  borderStrong: 'var(--t-border-strong)',
  fg: 'var(--t-fg)',
  muted: 'var(--t-muted)',
  dim: 'var(--t-dim)',
}

const SHORT_LABELS = ['MQM', 'Resist', 'CapB', 'Adm', 'Ind']

function rhoToColor(rho: number): string {
  // 0.83 (cool) → 1.00 (warm)
  // Lower correlations get a redder/distinct-er hue to highlight the rank-reversal point
  const t = Math.max(0, Math.min(1, (rho - 0.80) / 0.20))
  // From rgb(239,68,68) at t=0 to rgb(34,197,94) at t=1
  const r = Math.round(239 + (34 - 239) * t)
  const g = Math.round(68 + (197 - 68) * t)
  const b = Math.round(68 + (94 - 68) * t)
  return `rgb(${r}, ${g}, ${b})`
}

export default function CrossDimHeatmap() {
  const [hovered, setHovered] = useState<[number, number] | null>(null)
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  const n = CROSS_DIM_LABELS.length
  const cellSize = 56

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '24px',
      }}
    >
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
      }}>
        {/* Column headers */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: `64px repeat(${n}, ${cellSize}px)`,
          marginBottom: 4,
        }}>
          <div />
          {SHORT_LABELS.map((lbl, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: -4 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.04, duration: 0.4 }}
              style={{
                fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.06em', color: c.muted,
                textAlign: 'center', lineHeight: 1.4,
              }}
            >
              {lbl}
            </motion.div>
          ))}
        </div>

        {/* Rows */}
        {CROSS_DIM.map((row, i) => (
          <div key={i} style={{
            display: 'grid',
            gridTemplateColumns: `64px repeat(${n}, ${cellSize}px)`,
            alignItems: 'center', gap: 2, marginTop: 2,
          }}>
            <motion.div
              initial={{ opacity: 0, x: -4 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ delay: 0.12 + i * 0.04, duration: 0.4 }}
              style={{
                fontSize: 10, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.06em', color: c.muted,
                textAlign: 'right', paddingRight: 8,
              }}
            >
              {SHORT_LABELS[i]}
            </motion.div>
            {row.map((val, j) => {
              const isDiag = i === j
              const isHovered = hovered && hovered[0] === i && hovered[1] === j
              const fillColor = isDiag ? 'var(--t-overlay-soft)' : rhoToColor(val)
              return (
                <motion.div
                  key={j}
                  onMouseEnter={() => setHovered([i, j])}
                  onMouseLeave={() => setHovered(null)}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={inView ? { opacity: 1, scale: 1 } : {}}
                  transition={{
                    delay: 0.2 + (i + j) * 0.04,
                    type: 'spring' as const, stiffness: 280, damping: 28,
                  }}
                  style={{
                    width: cellSize, height: cellSize,
                    borderRadius: 6,
                    background: fillColor,
                    opacity: isDiag ? 0.2 : (isHovered ? 1 : 0.32),
                    border: isHovered ? `1px solid ${c.fg}` : '1px solid transparent',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    cursor: isDiag ? 'default' : 'pointer',
                    transition: 'opacity 0.15s, border-color 0.15s',
                    fontSize: 12.5,
                    fontWeight: 600,
                    color: isDiag ? c.dim : c.fg,
                    fontVariantNumeric: 'tabular-nums',
                    letterSpacing: '-0.01em',
                  }}
                >
                  {isDiag ? '—' : val.toFixed(2)}
                </motion.div>
              )
            })}
          </div>
        ))}
      </div>

      {/* Caption */}
      <div style={{
        marginTop: 20, paddingTop: 14,
        borderTop: `1px solid ${c.border}`,
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          gap: 16, flexWrap: 'wrap',
        }}>
          {/* Legend */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{
              fontSize: 10, color: c.dim, fontWeight: 600,
              textTransform: 'uppercase', letterSpacing: '0.06em',
            }}>
              ρ
            </span>
            <div style={{
              width: 120, height: 6, borderRadius: 3,
              background: `linear-gradient(to right, ${rhoToColor(0.80)}, ${rhoToColor(1.00)})`,
            }} />
            <span style={{ fontSize: 10.5, color: c.muted, fontVariantNumeric: 'tabular-nums' }}>0.80</span>
            <span style={{ fontSize: 10, color: c.dim }}>→</span>
            <span style={{ fontSize: 10.5, color: c.muted, fontVariantNumeric: 'tabular-nums' }}>1.00</span>
          </div>
          {hovered && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.15 }}
              style={{
                fontSize: 11, color: c.muted,
              }}
            >
              {CROSS_DIM_LABELS[hovered[0]]} × {CROSS_DIM_LABELS[hovered[1]]} ={' '}
              <span style={{ color: c.fg, fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>
                {CROSS_DIM[hovered[0]][hovered[1]].toFixed(3)}
              </span>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}
