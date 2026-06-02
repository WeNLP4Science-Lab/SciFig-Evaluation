import { motion, AnimatePresence } from 'motion/react'
import { useTheme } from '../theme'

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.7 }

export default function ThemeToggle() {
  const { theme, toggle } = useTheme()
  const isDark = theme === 'dark'

  return (
    <motion.button
      onClick={toggle}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.92 }}
      transition={SPRING}
      aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      style={{
        width: 32, height: 32, borderRadius: 8,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'var(--t-surface)',
        border: '1px solid var(--t-border-strong)',
        color: 'var(--t-fg)',
        cursor: 'pointer',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <AnimatePresence mode="wait" initial={false}>
        {isDark ? (
          <motion.svg
            key="moon"
            initial={{ y: 14, opacity: 0, rotate: -45 }}
            animate={{ y: 0, opacity: 1, rotate: 0 }}
            exit={{ y: -14, opacity: 0, rotate: 45 }}
            transition={SPRING}
            width="15" height="15" viewBox="0 0 16 16"
            fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"
          >
            <path d="M13.5 9.5A5 5 0 1 1 6.5 2.5a4 4 0 0 0 7 7Z" />
          </motion.svg>
        ) : (
          <motion.svg
            key="sun"
            initial={{ y: 14, opacity: 0, rotate: -45 }}
            animate={{ y: 0, opacity: 1, rotate: 0 }}
            exit={{ y: -14, opacity: 0, rotate: 45 }}
            transition={SPRING}
            width="15" height="15" viewBox="0 0 16 16"
            fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"
          >
            <circle cx="8" cy="8" r="3" />
            <path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3 3l1 1M12 12l1 1M3 13l1-1M12 4l1-1" />
          </motion.svg>
        )}
      </AnimatePresence>
    </motion.button>
  )
}
