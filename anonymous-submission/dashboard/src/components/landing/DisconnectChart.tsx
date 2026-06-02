import { useRef } from 'react'
import { motion, useInView } from 'motion/react'
import { MODELS, MQM, ADMITTANCE } from '../../data/landing_data'

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

// The 4 most informative models to feature (rest crowd the visual)
const FEATURED = ['gpt', 'gemini', 'llama', 'phi']

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }

export default function DisconnectChart() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  const rows = FEATURED.map(id => {
    const m = MODELS.find(x => x.id === id)!
    return {
      id, name: m.short, color: m.color,
      mqm: MQM[id],
      adm: ADMITTANCE[id].active,
    }
  })

  return (
    <div
      ref={ref}
      style={{
        borderRadius: 14, border: `1px solid ${c.border}`,
        background: c.surface, padding: '28px 28px 24px',
        position: 'relative', overflow: 'hidden',
      }}
    >
      {/* Subtle glow */}
      <div style={{
        position: 'absolute', top: -120, right: -120,
        width: 360, height: 360, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(239,68,68,0.06), transparent 60%)',
        filter: 'blur(40px)', pointerEvents: 'none',
      }} />

      {/* Twin axis headers */}
      <div style={{
        display: 'grid', gridTemplateColumns: '120px 1fr 60px 1fr',
        gap: 16, alignItems: 'baseline', marginBottom: 24,
        position: 'relative',
      }}>
        <div />
        <AxisHeader
          label="Perception (MQM)"
          subtitle="Description quality, 0–100"
        />
        <div />
        <AxisHeader
          label="Behaviour (Admittance)"
          subtitle="% of probes where uncertainty acknowledged"
          accent="#ef4444"
        />
      </div>

      {/* Rows */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14, position: 'relative' }}>
        {rows.map((row, i) => (
          <DisconnectRow key={row.id} row={row} index={i} inView={inView} />
        ))}
      </div>

      {/* Tagline */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ delay: 1.4, duration: 0.5 }}
        style={{
          marginTop: 28, paddingTop: 20,
          borderTop: `1px solid ${c.border}`,
          display: 'flex', alignItems: 'flex-start', gap: 16,
          flexWrap: 'wrap',
        }}
      >
        <div style={{ flex: '1 1 380px' }}>
          <p style={{
            fontSize: 11, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.1em', color: c.muted, margin: '0 0 6px',
          }}>
            The disconnect
          </p>
          <p style={{ fontSize: 14, color: c.fg, lineHeight: 1.55, margin: 0, fontWeight: 500 }}>
            Same perception. Opposite behaviour.
          </p>
        </div>
        <div style={{ display: 'flex', gap: 18, alignItems: 'baseline' }}>
          <StatChip
            value="1.4"
            unit="pts"
            label="MQM gap"
            color={c.muted}
          />
          <span style={{
            fontSize: 18, color: c.dim, fontWeight: 200,
            position: 'relative', top: -2,
          }}>→</span>
          <StatChip
            value="63"
            unit="pp"
            label="Admittance gap"
            color="#22c55e"
            highlight
          />
        </div>
      </motion.div>
    </div>
  )
}

function AxisHeader({ label, subtitle, accent }: { label: string; subtitle: string; accent?: string }) {
  return (
    <div>
      <p style={{
        fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: accent || c.muted,
        margin: '0 0 4px', lineHeight: 1,
      }}>
        {label}
      </p>
      <p style={{
        fontSize: 11, color: c.dim, margin: 0, lineHeight: 1.3,
      }}>
        {subtitle}
      </p>
    </div>
  )
}

function StatChip({ value, unit, label, color, highlight }: {
  value: string; unit: string; label: string; color: string; highlight?: boolean
}) {
  return (
    <div style={{
      padding: '6px 12px', borderRadius: 7,
      background: highlight ? 'rgba(34,197,94,0.08)' : c.surfaceRaised,
      border: `1px solid ${highlight ? 'rgba(34,197,94,0.2)' : c.border}`,
      display: 'flex', alignItems: 'baseline', gap: 4,
    }}>
      <span style={{
        fontSize: 18, fontWeight: 600, color, lineHeight: 1,
        fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.015em',
      }}>
        {value}
      </span>
      <span style={{ fontSize: 10, color: c.muted, fontWeight: 500 }}>{unit}</span>
      <span style={{ fontSize: 10.5, color: c.dim, marginLeft: 6 }}>{label}</span>
    </div>
  )
}

interface Row { id: string; name: string; color: string; mqm: number; adm: number }

function DisconnectRow({ row, index, inView }: { row: Row; index: number; inView: boolean }) {
  return (
    <div style={{
      display: 'grid', gridTemplateColumns: '120px 1fr 60px 1fr',
      gap: 16, alignItems: 'center',
    }}>
      {/* Model name */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <motion.span
          initial={{ scale: 0 }}
          animate={inView ? { scale: 1 } : {}}
          transition={{ delay: 0.15 + index * 0.08, ...SPRING }}
          style={{
            width: 8, height: 8, borderRadius: '50%', background: row.color,
            flexShrink: 0,
          }}
        />
        <span style={{ fontSize: 13, color: c.fg, fontWeight: 500 }}>
          {row.name}
        </span>
      </div>

      {/* MQM bar */}
      <BarSegment
        value={row.mqm}
        max={100}
        color={c.muted}
        rightLabel
        delay={0.3 + index * 0.08}
        inView={inView}
      />

      {/* Connecting marker */}
      <div style={{
        textAlign: 'center', fontSize: 11, color: c.dim,
      }}>
        <motion.span
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ delay: 0.7 + index * 0.08, duration: 0.3 }}
        >
          →
        </motion.span>
      </div>

      {/* Admittance bar */}
      <BarSegment
        value={row.adm}
        max={100}
        color={row.adm >= 50 ? '#22c55e' : row.adm >= 20 ? '#f59e0b' : '#ef4444'}
        rightLabel
        delay={0.85 + index * 0.08}
        inView={inView}
        emphasise
      />
    </div>
  )
}

function BarSegment({ value, max, color, rightLabel, delay, inView, emphasise }: {
  value: number; max: number; color: string;
  rightLabel?: boolean; delay: number; inView: boolean; emphasise?: boolean
}) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <div style={{
        flex: 1, height: emphasise ? 14 : 10,
        borderRadius: emphasise ? 7 : 5,
        background: 'rgba(255,255,255,0.04)',
        overflow: 'hidden', position: 'relative',
      }}>
        <motion.div
          initial={{ width: 0 }}
          animate={inView ? { width: `${(value / max) * 100}%` } : {}}
          transition={{ delay, duration: 0.85, ease: [0.22, 1, 0.36, 1] }}
          style={{
            height: '100%',
            background: color,
            opacity: emphasise ? 1 : 0.82,
            borderRadius: emphasise ? 7 : 5,
          }}
        />
      </div>
      {rightLabel && (
        <motion.span
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ delay: delay + 0.6, duration: 0.3 }}
          style={{
            fontSize: 12, color: c.fg, fontWeight: 600,
            fontVariantNumeric: 'tabular-nums',
            minWidth: 36, textAlign: 'right',
            letterSpacing: '-0.01em',
          }}
        >
          {value % 1 === 0 ? value : value.toFixed(1)}
        </motion.span>
      )}
    </div>
  )
}
