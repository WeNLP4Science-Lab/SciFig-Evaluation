import { motion } from 'motion/react'
import { MODELS } from '../../data/landing_data'

const c = {
  bg: '#09090b',
  surface: '#131316',
  surfaceRaised: '#18181b',
  border: 'rgba(255,255,255,0.06)',
  borderStrong: 'rgba(255,255,255,0.1)',
  fg: '#fafafa',
  muted: '#a1a1aa',
  dim: '#52525b',
}

export interface ModelBarChartProps {
  values: Record<string, number>     // model id → value
  max?: number                        // default 100 for %, 1 for resistance
  format?: (v: number) => string     // value formatter
  accent?: string                     // best-performer colour
  sort?: 'desc' | 'data'              // sort by value desc, or use MODELS order
  label?: string                      // optional small heading
  unit?: string                       // small grey unit under chart
}

export default function ModelBarChart({
  values, max = 100, format, accent = '#3b82f6',
  sort = 'desc', label, unit,
}: ModelBarChartProps) {
  const fmt = format ?? (max === 1 ? (v: number) => v.toFixed(2) : (v: number) => `${Math.round(v)}${max === 100 ? '%' : ''}`)

  const rows = MODELS
    .map(m => ({ id: m.id, name: m.short, color: m.color, value: values[m.id] ?? 0 }))
    .sort((a, b) => sort === 'desc' ? b.value - a.value : 0)

  const bestValue = Math.max(...rows.map(r => r.value))

  return (
    <div style={{ width: '100%' }}>
      {label && (
        <p style={{
          fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.08em', color: c.dim,
          margin: '0 0 10px', lineHeight: 1,
        }}>
          {label}
        </p>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
        {rows.map((row, i) => {
          const pct = (row.value / max) * 100
          const isBest = row.value === bestValue && row.value > 0
          return (
            <div
              key={row.id}
              style={{
                display: 'grid',
                gridTemplateColumns: '88px 1fr 48px',
                alignItems: 'center', gap: 10,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{
                  width: 6, height: 6, borderRadius: '50%', background: row.color,
                }} />
                <span style={{
                  fontSize: 11.5,
                  color: isBest ? c.fg : c.muted,
                  fontWeight: isBest ? 600 : 400,
                  whiteSpace: 'nowrap',
                  overflow: 'hidden', textOverflow: 'ellipsis',
                }}>
                  {row.name}
                </span>
              </div>

              <div style={{
                position: 'relative', height: 9,
                borderRadius: 5,
                background: 'rgba(255,255,255,0.04)',
                overflow: 'hidden',
              }}>
                <motion.div
                  key={`${row.id}-${row.value}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${pct}%` }}
                  transition={{
                    delay: 0.05 + i * 0.04,
                    duration: 0.7,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                  style={{
                    height: '100%',
                    background: isBest ? accent : row.color,
                    opacity: isBest ? 1 : 0.7,
                    borderRadius: 5,
                  }}
                />
              </div>

              <span style={{
                fontSize: 11.5, fontWeight: 600,
                color: isBest ? c.fg : c.muted,
                fontVariantNumeric: 'tabular-nums',
                textAlign: 'right',
                letterSpacing: '-0.01em',
              }}>
                {fmt(row.value)}
              </span>
            </div>
          )
        })}
      </div>
      {unit && (
        <p style={{
          fontSize: 10.5, color: c.dim, margin: '12px 0 0',
          textAlign: 'right',
        }}>
          {unit}
        </p>
      )}
    </div>
  )
}
