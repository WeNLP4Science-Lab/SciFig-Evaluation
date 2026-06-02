import { useRef, useState } from 'react'
import { motion, useInView } from 'motion/react'
import { MODELS, CAPABILITY } from '../../data/landing_data'

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

const CATEGORIES = [
  { key: 'counting',         label: 'Counting',    color: '#3b82f6' },
  { key: 'computation',      label: 'Computation', color: '#a855f7' },
  { key: 'comparison',       label: 'Comparison',  color: '#22c55e' },
  { key: 'pattern_analysis', label: 'Pattern',     color: '#f59e0b' },
] as const

export default function GroupedBarChart() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })
  const [hoveredCat, setHoveredCat] = useState<string | null>(null)
  const [hoveredModel, setHoveredModel] = useState<string | null>(null)

  // Layout constants
  const width = 760
  const height = 320
  const marginTop = 20
  const marginRight = 24
  const marginBottom = 56
  const marginLeft = 40
  const plotW = width - marginLeft - marginRight
  const plotH = height - marginTop - marginBottom

  const N_MODELS = MODELS.length
  const N_CATS = CATEGORIES.length
  const groupGap = 14
  const groupW = (plotW - (N_MODELS - 1) * groupGap) / N_MODELS
  const barGap = 1
  const barW = (groupW - (N_CATS - 1) * barGap) / N_CATS

  const yScale = (v: number) => plotH - (v / 100) * plotH
  const xGroup = (i: number) => marginLeft + i * (groupW + groupGap)
  const yTicks = [0, 25, 50, 75, 100]

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '24px 24px 18px',
      }}
    >
      {/* Legend */}
      <div style={{
        display: 'flex', gap: 16, marginBottom: 16, flexWrap: 'wrap',
        alignItems: 'center',
      }}>
        {CATEGORIES.map(cat => {
          const dim = hoveredCat !== null && hoveredCat !== cat.key
          return (
            <motion.div
              key={cat.key}
              onMouseEnter={() => setHoveredCat(cat.key)}
              onMouseLeave={() => setHoveredCat(null)}
              animate={{ opacity: dim ? 0.4 : 1 }}
              transition={{ duration: 0.18 }}
              style={{
                display: 'flex', alignItems: 'center', gap: 7,
                cursor: 'pointer',
              }}
            >
              <span style={{
                width: 10, height: 10, borderRadius: 2.5, background: cat.color,
              }} />
              <span style={{ fontSize: 11.5, color: c.fg, fontWeight: 500 }}>
                {cat.label}
              </span>
            </motion.div>
          )
        })}
      </div>

      {/* SVG chart */}
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        style={{ display: 'block' }}
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Y-axis gridlines */}
        {yTicks.map(t => (
          <g key={t}>
            <line
              x1={marginLeft} x2={width - marginRight}
              y1={marginTop + yScale(t)} y2={marginTop + yScale(t)}
              stroke="var(--t-overlay-soft)" strokeWidth={1}
              strokeDasharray={t === 0 ? '' : '2 3'}
            />
            <text
              x={marginLeft - 8}
              y={marginTop + yScale(t) + 3}
              fill={c.dim}
              fontSize={9.5}
              textAnchor="end"
              fontFamily="JetBrains Mono, monospace"
            >
              {t}
            </text>
          </g>
        ))}

        {/* Groups */}
        {MODELS.map((m, gi) => {
          const gx = xGroup(gi)
          const groupHovered = hoveredModel === m.id
          const groupDim = hoveredModel !== null && hoveredModel !== m.id

          return (
            <g
              key={m.id}
              onMouseEnter={() => setHoveredModel(m.id)}
              onMouseLeave={() => setHoveredModel(null)}
              style={{ cursor: 'pointer' }}
              opacity={groupDim ? 0.55 : 1}
            >
              {/* Hover bg */}
              {groupHovered && (
                <rect
                  x={gx - 4} y={marginTop - 4}
                  width={groupW + 8} height={plotH + 8}
                  fill="var(--t-overlay-soft)"
                  rx={4}
                />
              )}

              {/* Bars */}
              {CATEGORIES.map((cat, bi) => {
                const value = CAPABILITY[m.id][cat.key]
                const bx = gx + bi * (barW + barGap)
                const bh = (value / 100) * plotH
                const by = marginTop + plotH - bh
                const catDim = hoveredCat !== null && hoveredCat !== cat.key

                return (
                  <g key={cat.key}>
                    <motion.rect
                      x={bx}
                      width={barW}
                      initial={{ height: 0, y: marginTop + plotH }}
                      animate={inView ? {
                        height: bh,
                        y: by,
                      } : {}}
                      transition={{
                        delay: 0.15 + gi * 0.04 + bi * 0.025,
                        duration: 0.75,
                        ease: [0.22, 1, 0.36, 1],
                      }}
                      fill={cat.color}
                      opacity={catDim ? 0.3 : 0.95}
                      rx={1.5}
                    />
                    {/* Value label on hover */}
                    {groupHovered && (
                      <motion.text
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.18 }}
                        x={bx + barW / 2}
                        y={by - 4}
                        fill={c.fg}
                        fontSize={9.5}
                        textAnchor="middle"
                        fontFamily="JetBrains Mono, monospace"
                        fontWeight={600}
                      >
                        {Math.round(value)}
                      </motion.text>
                    )}
                  </g>
                )
              })}

              {/* Model label */}
              <g transform={`translate(${gx + groupW / 2}, ${marginTop + plotH + 14})`}>
                <circle r={3.5} cy={-4} fill={m.color} />
                <text
                  fill={groupHovered ? c.fg : c.muted}
                  fontSize={10.5}
                  textAnchor="middle"
                  y={12}
                  fontWeight={groupHovered ? 600 : 400}
                  style={{ transition: 'fill 0.15s, font-weight 0.15s' }}
                >
                  {m.short}
                </text>
              </g>
            </g>
          )
        })}
      </svg>

      {/* Footer caption */}
      <p style={{
        marginTop: 4, paddingTop: 10,
        borderTop: `1px solid ${c.border}`,
        fontSize: 11, color: c.dim, lineHeight: 1.55, margin: 0,
      }}>
        Capability accuracy (%) by category, across all 8 models on 250 figures.
        Hover any model for exact values, or hover a legend item to isolate one category.
      </p>
    </div>
  )
}
