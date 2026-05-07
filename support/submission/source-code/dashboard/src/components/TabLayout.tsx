import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { useTheme } from '../ThemeContext'

interface SubTab {
  label: string
  path: string
}

interface TabSection {
  label: string
  basePath: string
  subTabs: SubTab[]
}

const sections: TabSection[] = [
  {
    label: 'Dataset',
    basePath: '/dataset',
    subTabs: [
      { label: 'Full Corpus', path: '/dataset/full' },
      { label: '120 Sample', path: '/dataset/sample-120' },
      { label: 'Adversarial', path: '/dataset/adversarial-subset' },
      { label: 'Inferable Elements', path: '/dataset/inferable-blurs' },
    ],
  },
  {
    label: 'Evaluation',
    basePath: '/evaluation',
    subTabs: [
      { label: 'Full MQM', path: '/evaluation/full' },
      { label: 'Sample MQM', path: '/evaluation/sample' },
      { label: 'Transform MQM', path: '/evaluation/transform-mqm' },
      { label: 'Adversarial Probes', path: '/evaluation/adversarial' },
    ],
  },
  {
    label: 'Results',
    basePath: '/results',
    subTabs: [
      { label: 'Overview', path: '/results/overview' },
      { label: 'Adversarial Results', path: '/results/adversarial' },
      { label: 'Analytics', path: '/results/analytics' },
    ],
  },
]

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()
  return (
    <button
      onClick={toggleTheme}
      className="w-9 h-9 flex items-center justify-center rounded-full"
      style={{
        backgroundColor: 'var(--m3-surface-container-high)',
        transition: 'background-color 200ms var(--m3-easing-standard)',
      }}
      onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'var(--m3-surface-container-highest)' }}
      onMouseLeave={e => { e.currentTarget.style.backgroundColor = 'var(--m3-surface-container-high)' }}
      aria-label="Toggle theme"
    >
      {isDark ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
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
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      )}
    </button>
  )
}

export default function TabLayout() {
  const location = useLocation()

  const activeSection = sections.find(s => location.pathname.startsWith(s.basePath)) ?? sections[0]

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      {/* Top navigation bar */}
      <header
        style={{
          backgroundColor: 'var(--m3-surface)',
          borderBottom: '1px solid var(--m3-outline-variant)',
        }}
      >
        {/* Primary bar: branding + main tabs + theme toggle */}
        <div className="flex items-center justify-between px-5 h-14">
          <div className="flex items-center gap-8">
            {/* Branding */}
            <span
              className="text-sm font-semibold tracking-tight select-none"
              style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}
            >
              SciFig-Eval
            </span>

            {/* Main tabs */}
            <nav className="flex items-center gap-1">
              {sections.map(section => {
                const isActive = location.pathname.startsWith(section.basePath)
                return (
                  <NavLink
                    key={section.basePath}
                    to={section.subTabs[0].path}
                    className="relative px-4 py-2 rounded-lg text-sm font-medium"
                    style={{
                      color: isActive ? 'var(--m3-primary)' : 'var(--m3-on-surface-variant)',
                      backgroundColor: isActive ? 'var(--m3-primary-container)' : 'transparent',
                      letterSpacing: '0.1px',
                      transition: 'all 200ms var(--m3-easing-standard)',
                    }}
                    onMouseEnter={e => {
                      if (!isActive) {
                        e.currentTarget.style.backgroundColor = 'var(--m3-surface-container-high)'
                      }
                    }}
                    onMouseLeave={e => {
                      if (!isActive) {
                        e.currentTarget.style.backgroundColor = 'transparent'
                      }
                    }}
                  >
                    {section.label}
                  </NavLink>
                )
              })}
            </nav>
          </div>

          <ThemeToggle />
        </div>

        {/* Sub-tab bar */}
        <div
          className="flex items-center gap-0.5 px-5 h-10"
          style={{ backgroundColor: 'var(--m3-surface-container-low)' }}
        >
          {activeSection.subTabs.map(sub => {
            const isActive = location.pathname === sub.path
            return (
              <NavLink
                key={sub.path}
                to={sub.path}
                className="relative px-3.5 py-1.5 rounded-md text-xs font-medium"
                style={{
                  color: isActive ? 'var(--m3-on-surface)' : 'var(--m3-on-surface-variant)',
                  backgroundColor: isActive ? 'var(--m3-surface-container-high)' : 'transparent',
                  letterSpacing: '0.25px',
                  transition: 'all 150ms var(--m3-easing-standard)',
                }}
                onMouseEnter={e => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = 'var(--m3-surface-container)'
                  }
                }}
                onMouseLeave={e => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = 'transparent'
                  }
                }}
              >
                {sub.label}
                {isActive && (
                  <span
                    className="absolute bottom-0 left-3 right-3 h-0.5 rounded-full"
                    style={{ backgroundColor: 'var(--m3-primary)' }}
                  />
                )}
              </NavLink>
            )
          })}
        </div>
      </header>

      {/* Page content */}
      <main className="flex-1 flex flex-col min-h-0">
        <Outlet />
      </main>
    </div>
  )
}
