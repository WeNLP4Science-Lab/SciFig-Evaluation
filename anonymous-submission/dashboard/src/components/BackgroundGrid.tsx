import { useEffect } from 'react'
import { motion, useMotionValue, useSpring, useMotionTemplate, useReducedMotion } from 'motion/react'

/**
 * Full-viewport ambient gridlines that drift slowly. A brighter copy of the
 * grid is masked by a soft circle following the pointer — the cursor
 * "spotlight" reveals the grid more intensely under it.
 *
 * Mount once at the App root. Position: fixed, pointer-events: none.
 * Theme switching is automatic via CSS vars (--t-grid-line, --t-grid-reveal).
 */
export default function BackgroundGrid() {
  const reduce = useReducedMotion()

  // Cursor tracking with soft spring for smooth follow
  const mvX = useMotionValue(-9999)
  const mvY = useMotionValue(-9999)
  const x = useSpring(mvX, { stiffness: 90, damping: 22, mass: 0.6 })
  const y = useSpring(mvY, { stiffness: 90, damping: 22, mass: 0.6 })

  useEffect(() => {
    if (reduce) return
    const handle = (e: MouseEvent) => {
      mvX.set(e.clientX)
      mvY.set(e.clientY)
    }
    const leave = () => {
      mvX.set(-9999)
      mvY.set(-9999)
    }
    window.addEventListener('mousemove', handle, { passive: true })
    document.addEventListener('mouseleave', leave)
    return () => {
      window.removeEventListener('mousemove', handle)
      document.removeEventListener('mouseleave', leave)
    }
  }, [mvX, mvY, reduce])

  // Mask centred on cursor; black inside the circle, transparent outside
  const maskImage = useMotionTemplate`radial-gradient(circle 280px at ${x}px ${y}px, black 0%, transparent 75%)`

  const baseLayer = {
    position: 'fixed' as const,
    inset: 0,
    pointerEvents: 'none' as const,
    backgroundImage: `
      linear-gradient(to right, var(--t-grid-line) 1px, transparent 1px),
      linear-gradient(to bottom, var(--t-grid-line) 1px, transparent 1px)
    `,
    backgroundSize: '64px 64px',
    backgroundPosition: '0 0, 0 0',
    animation: reduce ? 'none' : 'gridDrift 90s linear infinite',
    zIndex: 0,
  }

  return (
    <>
      <div aria-hidden style={baseLayer} />
      {!reduce && (
        <motion.div
          aria-hidden
          style={{
            position: 'fixed',
            inset: 0,
            pointerEvents: 'none',
            backgroundImage: `
              linear-gradient(to right, var(--t-grid-reveal) 1px, transparent 1px),
              linear-gradient(to bottom, var(--t-grid-reveal) 1px, transparent 1px)
            `,
            backgroundSize: '64px 64px',
            backgroundPosition: '0 0, 0 0',
            maskImage: maskImage,
            WebkitMaskImage: maskImage,
            zIndex: 0,
          }}
        />
      )}
    </>
  )
}
