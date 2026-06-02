import { useRef, useState } from 'react'
import { motion, useInView } from 'motion/react'
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

export interface ModelLollipopChartProps {
  values: Record<string, number>
  max?: number                       // default 100 (%), use 1 for resistance
  format?: (v: number) => string
  accent?: string                    // colour for the best performer
  sort?: 'desc' | 'data'             // sort by value desc, or use MODELS order
  unit?: string                      // small caption beneath chart
}

export default function ModelLollipopChart({
  values, max = 100, format, accent = '#3b82f6', sort = 'desc', unit,
}: ModelLollipopChartProps) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: false, margin: '-15% 0px' })
  const [hovered, setHovered] = useState<string | null>(null)

  const fmt = format ?? (max === 1
    ? (v: number) => v.toFixed(2)
    : (v: number) => `${Math.round(v)}${max === 100 ? '%' : ''}`)

  const rows = MODELS
    .map(m => ({ id: m.id, name: m.short, color: m.color, value: values[m.id] ?? 0 }))
    .sort((a, b) => sort === 'desc' ? b.value - a.value : 0)

  const bestValue = Math.max(...rows.map(r => r.value))

  // Layout
  const width = 760
  const height = 220
  const marginTop = 36
  const marginRight = 16
  const marginBottom = 48
  const marginLeft = 36
  const plotW = width - marginLeft - marginRight
  const plotH = height - marginTop - marginBottom

  const N = rows.length
  const colW = plotW / N
  const baseline = marginTop + plotH

  const yTicks = max === 1
    ? [0, 0.25, 0.5, 0.75, 1.0]
    : [0, 25, 50, 75, 100]
  const yScale = (v: number) => baseline - (v / max) * plotH

  return (
    <div ref={ref} style={{ width: '100%' }}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        style={{ display: 'block', overflow: 'visible' }}
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Gridlines */}
        {yTicks.map(t => (
          <g key={t}>
            <line
              x1={marginLeft} x2={width - marginRight}
              y1={yScale(t)} y2={yScale(t)}
              stroke="rgba(255,255,255,0.05)" strokeWidth={1}
              strokeDasharray={t === 0 ? '' : '2 3'}
            />
            <text
              x={marginLeft - 8}
              y={yScale(t) + 3}
              fill={c.dim}
              fontSize={9.5}
              textAnchor="end"
              fontFamily="JetBrains Mono, monospace"
            >
              {max === 1 ? t.toFixed(2) : t}
            </text>
          </g>
        ))}

        {/* Baseline */}
        <line
          x1={marginLeft} x2={width - marginRight}
          y1={baseline} y2={baseline}
          stroke={c.borderStrong} strokeWidth={1}
        />

        {/* Lollipops */}
        {rows.map((row, i) => {
          const cx = marginLeft + i * colW + colW / 2
          const cy = yScale(row.value)
          const isBest = row.value === bestValue && row.value > 0
          const isHovered = hovered === row.id
          const isDim = hovered !== null && !isHovered
          const dotColor = isBest ? accent : row.color
          const stemColor = isBest ? accent : row.color

          return (
            <motion.g
              key={row.id}
              onMouseEnter={() => setHovered(row.id)}
              onMouseLeave={() => setHovered(null)}
              animate={{ opacity: isDim ? 0.35 : 1 }}
              transition={{ duration: 0.18 }}
              style={{ cursor: 'pointer' }}
            >
              {/* Hit area (invisible wide column for easier hover) */}
              <rect
                x={cx - colW / 2}
                y={marginTop}
                width={colW}
                height={plotH + marginBottom}
                fill="transparent"
              />

              {/* Stem (animated height) */}
              <motion.line
                x1={cx} x2={cx}
                y1={baseline}
                initial={{ y2: baseline }}
                animate={inView ? { y2: cy + 6 } : { y2: baseline }}
                transition={{
                  delay: 0.1 + i * 0.05,
                  duration: 0.7,
                  ease: [0.22, 1, 0.36, 1],
                }}
                stroke={stemColor}
                strokeWidth={isHovered ? 2 : 1.2}
                opacity={isBest ? 1 : 0.55}
              />

              {/* Glow ring on hover or best */}
              {(isHovered || isBest) && (
                <motion.circle
                  initial={{ r: 0, opacity: 0 }}
                  animate={inView ? { r: isHovered ? 13 : 11, opacity: isBest ? 0.35 : 0.25 } : {}}
                  transition={{
                    delay: 0.1 + i * 0.05 + 0.4,
                    duration: 0.5,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                  cx={cx} cy={cy}
                  fill={dotColor}
                />
              )}

              {/* Dot */}
              <motion.circle
                initial={{ r: 0 }}
                animate={inView ? { r: isHovered ? 7 : (isBest ? 6.5 : 5.5) } : { r: 0 }}
                transition={{
                  delay: 0.1 + i * 0.05 + 0.4,
                  type: 'spring' as const,
                  stiffness: 280, damping: 22,
                }}
                cx={cx} cy={cy}
                fill={dotColor}
                stroke={c.surface}
                strokeWidth={1.5}
              />

              {/* Value label above dot */}
              <motion.text
                initial={{ opacity: 0, y: cy + 6 }}
                animate={inView ? { opacity: 1, y: cy - 12 } : {}}
                transition={{ delay: 0.1 + i * 0.05 + 0.55, duration: 0.4 }}
                x={cx}
                fill={isBest || isHovered ? c.fg : c.muted}
                fontSize={11}
                fontWeight={isBest ? 600 : 500}
                textAnchor="middle"
                fontFamily="JetBrains Mono, monospace"
                style={{ transition: 'fill 0.15s' }}
              >
                {fmt(row.value)}
              </motion.text>

              {/* Model label below baseline */}
              <g transform={`translate(${cx}, ${baseline + 16})`}>
                <circle
                  r={3}
                  cy={-3}
                  fill={row.color}
                  opacity={isDim ? 0.4 : 1}
                />
                <motion.text
                  animate={{
                    fill: isHovered || isBest ? c.fg : c.muted,
                  }}
                  transition={{ duration: 0.15 }}
                  fontSize={10.5}
                  textAnchor="middle"
                  y={12}
                  fontWeight={isHovered || isBest ? 600 : 400}
                >
                  {row.name}
                </motion.text>
              </g>
            </motion.g>
          )
        })}
      </svg>

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
