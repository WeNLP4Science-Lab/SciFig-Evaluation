import { useRef, useState } from 'react'
import { motion, useInView } from 'motion/react'
import { MODELS, MQM, ADMITTANCE, overallResistance } from '../../data/landing_data'

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

interface ScatterPoint {
  id: string
  name: string
  color: string
  x: number  // MQM
  y: number  // Admittance % or Resistance (0-1 scaled)
}

export default function ScatterChart() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })
  const [hovered, setHovered] = useState<string | null>(null)

  const admPoints: ScatterPoint[] = MODELS.map(m => ({
    id: m.id, name: m.short, color: m.color,
    x: MQM[m.id],
    y: ADMITTANCE[m.id].active,
  }))

  const resPoints: ScatterPoint[] = MODELS.map(m => ({
    id: m.id, name: m.short, color: m.color,
    x: MQM[m.id],
    y: overallResistance(m.id) * 100,  // scale to 0-100 for shared axis math
  }))

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '24px 28px 22px',
      }}
    >
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28,
      }}>
        <ScatterPanel
          title="Perception → Admittance"
          xLabel="MQM (Perception)"
          yLabel="Admittance (%)"
          xRange={[55, 100]}
          yRange={[0, 80]}
          points={admPoints}
          inView={inView}
          hovered={hovered}
          setHovered={setHovered}
          referenceLine
          referenceLabel="If quality predicted behaviour"
          yFormat={v => `${Math.round(v)}`}
        />
        <ScatterPanel
          title="Perception → Resistance"
          xLabel="MQM (Perception)"
          yLabel="Resistance (0-1)"
          xRange={[55, 100]}
          yRange={[0, 100]}
          points={resPoints}
          inView={inView}
          hovered={hovered}
          setHovered={setHovered}
          referenceLine
          referenceLabel="Reference"
          yFormat={v => (v / 100).toFixed(2)}
        />
      </div>

      {/* Caption */}
      <p style={{
        marginTop: 18, paddingTop: 14,
        borderTop: `1px solid ${c.border}`,
        fontSize: 11.5, color: c.dim, lineHeight: 1.55, margin: 0,
      }}>
        Each dot is one of eight models, plotted by perception (MQM) vs behaviour.
        Hover any dot to highlight that model across both panels.
        The dashed line shows where points would fall if quality predicted behaviour — most don't.
      </p>
    </div>
  )
}

function ScatterPanel({
  title, xLabel, yLabel, xRange, yRange, points, inView, hovered, setHovered,
  referenceLine, referenceLabel, yFormat,
}: {
  title: string
  xLabel: string; yLabel: string
  xRange: [number, number]; yRange: [number, number]
  points: ScatterPoint[]
  inView: boolean
  hovered: string | null
  setHovered: (id: string | null) => void
  referenceLine?: boolean
  referenceLabel?: string
  yFormat: (v: number) => string
}) {
  const width = 360
  const height = 280
  const marginTop = 22
  const marginRight = 16
  const marginBottom = 38
  const marginLeft = 44
  const plotW = width - marginLeft - marginRight
  const plotH = height - marginTop - marginBottom

  const xScale = (v: number) => marginLeft + ((v - xRange[0]) / (xRange[1] - xRange[0])) * plotW
  const yScale = (v: number) => marginTop + plotH - ((v - yRange[0]) / (yRange[1] - yRange[0])) * plotH

  const xTicks = [60, 70, 80, 90, 100]
  const yTicks = yRange[1] === 80
    ? [0, 20, 40, 60, 80]
    : [0, 25, 50, 75, 100]

  const hoveredPoint = points.find(p => p.id === hovered)

  return (
    <div>
      <p style={{
        fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: c.muted,
        margin: '0 0 10px', lineHeight: 1,
      }}>
        {title}
      </p>

      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        style={{ display: 'block', overflow: 'visible' }}
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Gridlines */}
        {yTicks.map(t => (
          <g key={`y-${t}`}>
            <line
              x1={marginLeft} x2={width - marginRight}
              y1={yScale(t)} y2={yScale(t)}
              stroke="var(--t-overlay-soft)" strokeWidth={1}
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
              {yFormat(t)}
            </text>
          </g>
        ))}
        {xTicks.map(t => (
          <g key={`x-${t}`}>
            <line
              x1={xScale(t)} x2={xScale(t)}
              y1={marginTop} y2={marginTop + plotH}
              stroke="var(--t-overlay-soft)" strokeWidth={1}
              strokeDasharray="2 3"
            />
            <text
              x={xScale(t)}
              y={marginTop + plotH + 14}
              fill={c.dim}
              fontSize={9.5}
              textAnchor="middle"
              fontFamily="JetBrains Mono, monospace"
            >
              {t}
            </text>
          </g>
        ))}

        {/* Reference line (linear y = x*scaling within plot) */}
        {referenceLine && (
          <motion.line
            initial={{ pathLength: 0, opacity: 0 }}
            animate={inView ? { pathLength: 1, opacity: 1 } : {}}
            transition={{ delay: 0.3, duration: 0.9, ease: 'easeOut' }}
            x1={xScale(xRange[0])}
            y1={yScale(yRange[0])}
            x2={xScale(xRange[1])}
            y2={yScale(yRange[1])}
            stroke={c.dim}
            strokeWidth={1.2}
            strokeDasharray="4 4"
            opacity={0.5}
          />
        )}
        {referenceLine && (
          <motion.text
            initial={{ opacity: 0 }}
            animate={inView ? { opacity: 1 } : {}}
            transition={{ delay: 1.0, duration: 0.4 }}
            x={xScale(xRange[1]) - 4}
            y={yScale(yRange[1]) + 14}
            fill={c.dim}
            fontSize={9}
            textAnchor="end"
            fontStyle="italic"
          >
            {referenceLabel}
          </motion.text>
        )}

        {/* Axis labels */}
        <text
          x={marginLeft + plotW / 2}
          y={height - 6}
          fill={c.muted}
          fontSize={10}
          textAnchor="middle"
        >
          {xLabel}
        </text>
        <text
          x={-marginTop - plotH / 2}
          y={12}
          fill={c.muted}
          fontSize={10}
          textAnchor="middle"
          transform="rotate(-90)"
        >
          {yLabel}
        </text>

        {/* Points */}
        {points.map((p, i) => {
          const isHovered = hovered === p.id
          const isDim = hovered !== null && !isHovered
          return (
            <motion.g
              key={p.id}
              onMouseEnter={() => setHovered(p.id)}
              onMouseLeave={() => setHovered(null)}
              animate={{ opacity: isDim ? 0.3 : 1 }}
              transition={{ duration: 0.18 }}
              style={{ cursor: 'pointer' }}
            >
              {/* Glow on hover */}
              {isHovered && (
                <motion.circle
                  initial={{ r: 8, opacity: 0 }}
                  animate={{ r: 14, opacity: 0.35 }}
                  transition={{ duration: 0.2 }}
                  cx={xScale(p.x)} cy={yScale(p.y)}
                  fill={p.color}
                />
              )}
              <motion.circle
                initial={{ r: 0, cx: xScale(p.x), cy: yScale(p.y) }}
                animate={inView ? { r: isHovered ? 7 : 5.5 } : {}}
                transition={{
                  r: { duration: 0.18 },
                  default: { delay: 0.4 + i * 0.05, type: 'spring' as const, stiffness: 320, damping: 22 },
                }}
                cx={xScale(p.x)} cy={yScale(p.y)}
                fill={p.color}
                stroke={c.surface}
                strokeWidth={1.5}
              />
            </motion.g>
          )
        })}

        {/* Hover tooltip */}
        {hoveredPoint && (
          <g transform={`translate(${xScale(hoveredPoint.x) + 12}, ${yScale(hoveredPoint.y) - 22})`}>
            <rect
              x={0} y={0}
              width={110} height={36}
              rx={5}
              fill={c.bg}
              stroke={c.borderStrong}
              strokeWidth={1}
            />
            <text x={10} y={14} fill={c.fg} fontSize={11} fontWeight={600}>
              {hoveredPoint.name}
            </text>
            <text x={10} y={28} fill={c.muted} fontSize={10}
              fontFamily="JetBrains Mono, monospace">
              MQM {hoveredPoint.x.toFixed(1)} · {yFormat(hoveredPoint.y)}
            </text>
          </g>
        )}
      </svg>
    </div>
  )
}
