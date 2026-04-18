import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'

const cards = [
  {
    to: '/evaluation/full',
    title: 'Full Dataset',
    desc: 'Complete dataset evaluation across all figures and models',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <path d="M3 9h18" />
        <path d="M3 15h18" />
        <path d="M9 3v18" />
      </svg>
    ),
  },
  {
    to: '/evaluation/sample',
    title: '120 Sample',
    desc: 'Curated 120-figure sample with human evaluation comparison',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2" />
        <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
        <path d="M12 11h4" />
        <path d="M12 16h4" />
        <path d="M8 11h.01" />
        <path d="M8 16h.01" />
      </svg>
    ),
  },
  {
    to: '/evaluation/adversarial-120',
    title: '120 Sample Adversarial',
    desc: 'Browse all 120 sample figures with groundtruth for adversarial analysis',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <path d="M12 11h4" />
        <path d="M12 16h4" />
        <path d="M8 11h.01" />
        <path d="M8 16h.01" />
      </svg>
    ),
  },
  {
    to: '/evaluation/adversarial-subset',
    title: 'Adversarial Subset (45)',
    desc: 'Selected 45 figures with complex features for adversarial testing',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),
  },
  {
    to: '/evaluation/adversarial',
    title: 'Adversarial Evaluation',
    desc: 'Per-model prompt reverse and caption bias experiment results on 45 adversarial figures',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 11l3 3L22 4" />
        <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
      </svg>
    ),
  },
]

export default function EvaluationSelector() {
  const { isDark } = useTheme()

  return (
    <div
      className="min-h-screen flex flex-col animate-fade-in"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      <header
        className="px-6 py-4 flex items-center"
        style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}
      >
        <Link
          to="/"
          className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg"
          style={{ color: 'var(--m3-on-surface-variant)' }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 12H5" />
            <path d="M12 19l-7-7 7-7" />
          </svg>
          Back
        </Link>
      </header>

      <main className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-3xl px-6">
          <h1
            className="text-3xl font-normal tracking-tight mb-3"
            style={{ color: 'var(--m3-on-surface)', letterSpacing: '-0.25px' }}
          >
            Evaluation Review
          </h1>
          <p
            className="text-sm mb-12"
            style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.25px' }}
          >
            Review MQM judge evaluations, sample figures, and adversarial testing data
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 text-left">
            {cards.map(card => (
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
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.backgroundColor = 'var(--m3-surface-container)'
                }}
              >
                <div
                  className="w-11 h-11 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-primary)' }}
                >
                  {card.icon}
                </div>
                <div>
                  <h3
                    className="font-medium text-sm mb-1.5"
                    style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}
                  >
                    {card.title}
                  </h3>
                  <p
                    className="text-xs leading-relaxed"
                    style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.4px' }}
                  >
                    {card.desc}
                  </p>
                </div>
                <div className="flex justify-end">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-outline)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="transition-transform duration-300 group-hover:translate-x-1">
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
