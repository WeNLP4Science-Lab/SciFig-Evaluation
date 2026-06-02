import { useState, useRef } from 'react'
import { motion, AnimatePresence, useInView } from 'motion/react'

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

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }

interface PaperFigureProps {
  src: string
  alt: string
  label?: string
  caption: string
  highlights?: string[]
  background?: 'light' | 'dark'
  legend?: Array<{ abbr: string; full: string }>  // optional inline glossary above caption
}

export default function PaperFigure({
  src, alt, label, caption, highlights, background = 'light', legend,
}: PaperFigureProps) {
  const [zoomed, setZoomed] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  return (
    <>
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 18 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
        style={{
          borderRadius: 14, border: `1px solid ${c.border}`,
          background: c.surface, overflow: 'hidden',
        }}
      >
        {/* Image plate */}
        <div
          onClick={() => setZoomed(true)}
          style={{
            position: 'relative',
            background: background === 'light' ? '#fafafa' : c.bg,
            padding: 24,
            cursor: 'zoom-in',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            minHeight: 280,
          }}
        >
          <motion.img
            src={src}
            alt={alt}
            initial={{ opacity: 0, scale: 1.02 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ delay: 0.15, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            loading="lazy"
            style={{
              maxWidth: '100%', maxHeight: '60vh', objectFit: 'contain',
              userSelect: 'none',
            }}
          />

          {label && (
            <motion.span
              initial={{ opacity: 0, y: -4 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.35, ...SPRING }}
              style={{
                position: 'absolute', top: 14, left: 14,
                fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.08em',
                padding: '4px 9px', borderRadius: 4,
                background: 'rgba(9,9,11,0.78)',
                color: '#fafafa',
                border: '1px solid rgba(255,255,255,0.15)',
                backdropFilter: 'blur(6px)',
                lineHeight: 1,
              }}
            >
              {label}
            </motion.span>
          )}

          {/* Zoom hint */}
          <motion.span
            initial={{ opacity: 0 }}
            animate={inView ? { opacity: 1 } : {}}
            transition={{ delay: 0.6, duration: 0.4 }}
            style={{
              position: 'absolute', bottom: 14, right: 14,
              fontSize: 9.5, fontWeight: 500,
              padding: '4px 8px', borderRadius: 4,
              background: 'rgba(9,9,11,0.78)',
              color: '#a1a1aa',
              border: '1px solid rgba(255,255,255,0.1)',
              backdropFilter: 'blur(6px)',
              display: 'flex', alignItems: 'center', gap: 4,
              lineHeight: 1,
            }}
          >
            <svg width="9" height="9" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
              <path d="M2.5 6h7M6 2.5v7" />
            </svg>
            Click to zoom
          </motion.span>
        </div>

        {/* Caption + highlights */}
        <div style={{ padding: '16px 22px 18px', borderTop: `1px solid ${c.border}` }}>
          {legend && legend.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <p style={{
                fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.08em', color: c.dim,
                margin: '0 0 8px', lineHeight: 1,
              }}>
                Conditions
              </p>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                gap: '6px 16px',
              }}>
                {legend.map(item => (
                  <div key={item.abbr} style={{
                    display: 'flex', alignItems: 'baseline', gap: 6,
                    fontSize: 11, lineHeight: 1.4,
                  }}>
                    <span style={{
                      fontSize: 10.5, fontFamily: 'JetBrains Mono, monospace',
                      fontWeight: 600, color: c.fg, flexShrink: 0,
                    }}>
                      {item.abbr}
                    </span>
                    <span style={{ color: c.muted }}>
                      {item.full}
                    </span>
                  </div>
                ))}
              </div>
              <div style={{
                height: 1, background: c.border, margin: '12px 0',
              }} />
            </div>
          )}
          <p style={{
            fontSize: 12.5, color: c.muted, lineHeight: 1.6,
            margin: 0,
          }}>
            {caption}
          </p>
          {highlights && highlights.length > 0 && (
            <div style={{
              display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 12,
            }}>
              {highlights.map((h, i) => (
                <motion.span
                  key={i}
                  initial={{ opacity: 0, y: 4 }}
                  animate={inView ? { opacity: 1, y: 0 } : {}}
                  transition={{ delay: 0.5 + i * 0.06, duration: 0.4 }}
                  style={{
                    fontSize: 10.5, fontWeight: 500, color: c.fg,
                    padding: '4px 10px', borderRadius: 5,
                    background: c.surfaceRaised,
                    border: `1px solid ${c.border}`,
                    lineHeight: 1.3,
                    letterSpacing: '0.005em',
                  }}
                >
                  {h}
                </motion.span>
              ))}
            </div>
          )}
        </div>
      </motion.div>

      {/* Zoom modal */}
      <AnimatePresence>
        {zoomed && (
          <motion.div
            key="zoom-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={() => setZoomed(false)}
            style={{
              position: 'fixed', inset: 0, zIndex: 60,
              background: 'rgba(0,0,0,0.92)',
              backdropFilter: 'blur(14px)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              padding: 32, cursor: 'zoom-out',
            }}
          >
            <motion.img
              initial={{ scale: 0.94, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.96, opacity: 0 }}
              transition={SPRING}
              src={src}
              alt={alt}
              onClick={e => e.stopPropagation()}
              style={{
                maxWidth: '92vw', maxHeight: '88vh',
                objectFit: 'contain',
                borderRadius: 8,
                background: background === 'light' ? '#fafafa' : c.bg,
                padding: 32,
                cursor: 'default',
              }}
            />
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.15 }}
              onClick={() => setZoomed(false)}
              style={{
                position: 'absolute', top: 24, right: 24,
                width: 36, height: 36, borderRadius: '50%',
                background: 'rgba(255,255,255,0.08)',
                border: '1px solid rgba(255,255,255,0.12)',
                color: '#fafafa', cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}
            >
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
                <path d="M3 3l10 10M13 3L3 13" />
              </svg>
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
