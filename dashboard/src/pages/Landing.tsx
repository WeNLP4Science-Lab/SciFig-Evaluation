import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()
  return (
    <button
      onClick={toggleTheme}
      className="w-10 h-10 flex items-center justify-center rounded-full m3-state-hover"
      style={{
        backgroundColor: 'var(--m3-surface-container-high)',
      }}
      aria-label="Toggle theme"
    >
      {isDark ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      )}
    </button>
  )
}

export default function Landing() {
  const { isDark } = useTheme()

  const navCards = [
    {
      to: '/dataset',
      title: 'Dataset Browser',
      desc: 'Browse scientific figures and groundtruth annotations across all language subsets',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="7" height="7" rx="1" />
          <rect x="14" y="3" width="7" height="7" rx="1" />
          <rect x="3" y="14" width="7" height="7" rx="1" />
          <rect x="14" y="14" width="7" height="7" rx="1" />
        </svg>
      ),
    },
    {
      to: '/review',
      title: 'Evaluation Review',
      desc: 'Review MQM judge evaluations with annotated error spans across models',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" />
          <rect x="9" y="3" width="6" height="4" rx="2" />
          <path d="M9 14l2 2 4-4" />
        </svg>
      ),
    },
  ]

  return (
    <div
      className="min-h-screen flex flex-col m3-grid-bg m3-grid-fine animate-fade-in"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      {/* Header */}
      <header
        className="px-6 py-4 flex items-center justify-between"
        style={{
          borderBottom: `1px solid var(--m3-outline-variant)`,
          backgroundColor: 'var(--m3-surface)',
        }}
      >
        <div className="flex items-center gap-3">
          <span
            className="text-base font-medium tracking-tight"
            style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}
          >
            SciFig Evaluation
          </span>
        </div>
        <ThemeToggle />
      </header>

      {/* Hero */}
      <main className="flex-1 flex items-center justify-center relative z-10">
        <div className="text-center max-w-2xl px-6 animate-fade-in-up">
          {/* Chip */}
          <div
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-10"
            style={{
              backgroundColor: 'var(--m3-primary-container)',
              color: 'var(--m3-on-primary-container)',
            }}
          >
            <span
              className="w-1.5 h-1.5 rounded-full"
              style={{ backgroundColor: 'var(--m3-primary)' }}
            />
            <span className="text-xs font-medium" style={{ letterSpacing: '0.5px' }}>
              MQM Framework
            </span>
          </div>

          <h1
            className="text-5xl font-normal tracking-tight mb-4"
            style={{
              color: 'var(--m3-on-surface)',
              letterSpacing: '-0.25px',
              lineHeight: '56px',
            }}
          >
            Evaluation Dashboard
          </h1>

          <p
            className="text-base mb-3 max-w-lg mx-auto"
            style={{
              color: 'var(--m3-on-surface-variant)',
              lineHeight: '24px',
              letterSpacing: '0.5px',
            }}
          >
            Multilingual scientific figure annotation quality evaluation
            using the Multidimensional Quality Metrics framework.
          </p>
          <p
            className="text-sm mb-16 max-w-md mx-auto"
            style={{
              color: 'var(--m3-outline)',
              lineHeight: '20px',
              letterSpacing: '0.25px',
            }}
          >
            Three judge approaches with color-coded error annotations
            on model output for granular quality assessment.
          </p>

          {/* Navigation Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 text-left max-w-xl mx-auto">
            {navCards.map((card) => (
              <Link
                key={card.to}
                to={card.to}
                className="group rounded-xl p-6 flex flex-col gap-4"
                style={{
                  backgroundColor: 'var(--m3-surface-container)',
                  transition: 'all 250ms var(--m3-easing-standard)',
                  boxShadow: isDark
                    ? '0 1px 2px 0 rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15)'
                    : '0 1px 2px 0 rgba(0,0,0,0.15), 0 1px 3px 1px rgba(0,0,0,0.08)',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.backgroundColor = 'var(--m3-surface-container-high)'
                  e.currentTarget.style.boxShadow = isDark
                    ? '0 1px 2px 0 rgba(0,0,0,0.3), 0 2px 6px 2px rgba(0,0,0,0.15)'
                    : '0 1px 2px 0 rgba(0,0,0,0.15), 0 2px 6px 2px rgba(0,0,0,0.08)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.backgroundColor = 'var(--m3-surface-container)'
                  e.currentTarget.style.boxShadow = isDark
                    ? '0 1px 2px 0 rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15)'
                    : '0 1px 2px 0 rgba(0,0,0,0.15), 0 1px 3px 1px rgba(0,0,0,0.08)'
                }}
              >
                <div
                  className="w-11 h-11 rounded-lg flex items-center justify-center"
                  style={{
                    backgroundColor: 'var(--m3-surface-container-highest)',
                    color: 'var(--m3-primary)',
                  }}
                >
                  {card.icon}
                </div>
                <div className="flex-1">
                  <h3
                    className="font-medium text-sm mb-1.5"
                    style={{
                      color: 'var(--m3-on-surface)',
                      letterSpacing: '0.1px',
                      lineHeight: '20px',
                    }}
                  >
                    {card.title}
                  </h3>
                  <p
                    className="text-xs leading-relaxed"
                    style={{
                      color: 'var(--m3-on-surface-variant)',
                      letterSpacing: '0.4px',
                      lineHeight: '16px',
                    }}
                  >
                    {card.desc}
                  </p>
                </div>
                <div className="flex justify-end">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="var(--m3-outline)"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="transition-transform duration-300 group-hover:translate-x-1"
                  >
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer
        className="px-6 py-4 text-center relative z-10"
        style={{
          borderTop: `1px solid var(--m3-outline-variant)`,
        }}
      >
        <p
          className="text-xs"
          style={{
            color: 'var(--m3-outline)',
            letterSpacing: '0.4px',
          }}
        >
          SciFig Evaluation -- MQM Quality Assessment
        </p>
      </footer>
    </div>
  )
}
