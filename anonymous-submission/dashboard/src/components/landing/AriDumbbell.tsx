import { useState, useRef } from 'react'
import { motion, useInView } from 'motion/react'
import { MODELS, ADMITTANCE, INDUCTANCE, RESISTANCE, overallResistance } from '../../data/landing_data'

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

interface PanelRow {
  id: string
  name: string
  color: string
  primary: number    // active / overall
  secondary?: number // passive (for admittance/inductance)
}

export default function AriDumbbell() {
  const [hovered, setHovered] = useState<string | null>(null)
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  const admRows: PanelRow[] = MODELS.map(m => ({
    id: m.id, name: m.short, color: m.color,
    primary: ADMITTANCE[m.id].active,
    secondary: ADMITTANCE[m.id].passive,
  }))

  const resRows: PanelRow[] = MODELS.map(m => ({
    id: m.id, name: m.short, color: m.color,
    primary: Math.round(overallResistance(m.id) * 100) / 100,
  }))

  const indRows: PanelRow[] = MODELS.map(m => ({
    id: m.id, name: m.short, color: m.color,
    primary: INDUCTANCE[m.id].active,
    secondary: INDUCTANCE[m.id].passive,
  }))

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '24px 24px 22px',
      }}
    >
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18,
      }}>
        <Panel
          label="Admittance"
          accent="#ef4444"
          unit="%"
          max={100}
          rows={admRows}
          legend="● active   ○ passive"
          hovered={hovered}
          setHovered={setHovered}
          inView={inView}
        />
        <Panel
          label="Resistance"
          accent="#a855f7"
          unit=""
          max={1}
          rows={resRows}
          legend="Mean of inexist · contra · unanswerable"
          hovered={hovered}
          setHovered={setHovered}
          inView={inView}
        />
        <Panel
          label="Inductance"
          accent="#22c55e"
          unit="%"
          max={100}
          rows={indRows}
          legend="● active   ○ passive"
          hovered={hovered}
          setHovered={setHovered}
          inView={inView}
        />
      </div>

      {/* Footer caption */}
      <p style={{
        marginTop: 18, paddingTop: 14,
        borderTop: `1px solid ${c.border}`,
        fontSize: 11, color: c.dim, lineHeight: 1.55, margin: 0,
      }}>
        Filled circle = active probe (targeted question). Hollow circle = passive probe (open description). Lines connect the two for each model. Hover any model to highlight across all three panels.
      </p>
    </div>
  )
}

function Panel({ label, accent, unit, max, rows, legend, hovered, setHovered, inView }: {
  label: string; accent: string; unit: string; max: number
  rows: PanelRow[]; legend: string
  hovered: string | null; setHovered: (id: string | null) => void
  inView: boolean
}) {
  return (
    <div>
      <div style={{
        display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
        marginBottom: 14,
      }}>
        <h3 style={{
          fontSize: 13, fontWeight: 600, color: c.fg, margin: 0,
          letterSpacing: '-0.005em',
        }}>
          {label}
        </h3>
        <span style={{
          width: 6, height: 6, borderRadius: '50%', background: accent,
        }} />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {rows.map((row, i) => {
          const isHovered = hovered === row.id
          const isDim = hovered !== null && hovered !== row.id
          const xPrimary = (row.primary / max) * 100
          const xSecondary = row.secondary !== undefined ? (row.secondary / max) * 100 : null

          return (
            <motion.div
              key={row.id}
              onMouseEnter={() => setHovered(row.id)}
              onMouseLeave={() => setHovered(null)}
              animate={{ opacity: isDim ? 0.35 : 1 }}
              transition={{ duration: 0.18 }}
              style={{
                display: 'grid', gridTemplateColumns: '70px 1fr 40px',
                gap: 8, alignItems: 'center',
                cursor: 'pointer',
                padding: '4px 0',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{
                  width: 6, height: 6, borderRadius: '50%',
                  background: row.color, flexShrink: 0,
                }} />
                <span style={{
                  fontSize: 11, color: isHovered ? c.fg : c.muted,
                  fontWeight: isHovered ? 600 : 400,
                  transition: 'color 0.15s, font-weight 0.15s',
                  whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                }}>
                  {row.name}
                </span>
              </div>

              {/* Dumbbell track */}
              <div style={{
                position: 'relative', height: 14,
                display: 'flex', alignItems: 'center',
              }}>
                <div style={{
                  width: '100%', height: 1.5, borderRadius: 1,
                  background: c.border,
                }} />
                {/* Connecting line between primary & secondary */}
                {xSecondary !== null && (
                  <motion.div
                    initial={{ width: 0 }}
                    animate={inView ? {
                      width: `${Math.abs(xPrimary - xSecondary)}%`,
                    } : {}}
                    transition={{ delay: 0.25 + i * 0.05, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                    style={{
                      position: 'absolute',
                      left: `${Math.min(xPrimary, xSecondary)}%`,
                      height: 2, borderRadius: 1,
                      background: row.color, opacity: 0.4,
                    }}
                  />
                )}
                {/* Secondary marker (passive — hollow) */}
                {xSecondary !== null && (
                  <motion.div
                    initial={{ scale: 0, x: 0 }}
                    animate={inView ? { scale: 1 } : {}}
                    transition={{ delay: 0.45 + i * 0.05, type: 'spring' as const, stiffness: 320, damping: 30 }}
                    style={{
                      position: 'absolute',
                      left: `${xSecondary}%`,
                      transform: 'translate(-50%, 0)',
                      width: 9, height: 9, borderRadius: '50%',
                      background: c.surface,
                      border: `1.5px solid ${row.color}`,
                    }}
                  />
                )}
                {/* Primary marker (active — filled) */}
                <motion.div
                  initial={{ scale: 0 }}
                  animate={inView ? { scale: 1 } : {}}
                  transition={{ delay: 0.35 + i * 0.05, type: 'spring' as const, stiffness: 320, damping: 30 }}
                  style={{
                    position: 'absolute',
                    left: `${xPrimary}%`,
                    transform: 'translate(-50%, 0)',
                    width: 10, height: 10, borderRadius: '50%',
                    background: row.color,
                    boxShadow: isHovered ? `0 0 0 4px ${row.color}33` : 'none',
                    transition: 'box-shadow 0.18s',
                  }}
                />
              </div>

              {/* Value */}
              <span style={{
                fontSize: 11, fontWeight: 600,
                color: isHovered ? c.fg : c.muted,
                fontVariantNumeric: 'tabular-nums',
                textAlign: 'right',
                transition: 'color 0.15s',
              }}>
                {max === 1 ? row.primary.toFixed(2) : `${row.primary}${unit}`}
              </span>
            </motion.div>
          )
        })}
      </div>

      <p style={{
        marginTop: 12, fontSize: 10, color: c.dim, margin: 0,
        textAlign: 'center', letterSpacing: '0.02em',
      }}>
        {legend}
      </p>
    </div>
  )
}
