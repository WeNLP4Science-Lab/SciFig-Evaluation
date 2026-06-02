import { useState, useEffect } from 'react'
import Landing from './pages/Landing'
import Dataset from './pages/Dataset'
import FigureDetail from './pages/FigureDetail'
import Tasks from './pages/Tasks'
import Login from './components/Login'
import { isAnnotationMode, getSavedAuth, loginAPI, clearAuth as clearStoredAuth, displayName, type AuthState } from './auth'

const sections = ['home', 'dataset', 'tasks', 'evaluation', 'analytics'] as const
type Section = typeof sections[number]

const sectionMeta: Record<Section, { label: string; ready: boolean }> = {
  home:       { label: 'Home',       ready: true },
  dataset:    { label: 'Dataset',    ready: true },
  tasks:      { label: 'Tasks',      ready: true },
  evaluation: { label: 'Evaluation', ready: false },
  analytics:  { label: 'Analytics',  ready: false },
}

export default function App() {
  // Read section from hash on load. Default to 'home' for the landing page.
  const getHashState = () => {
    const hash = window.location.hash.replace('#', '')
    if (hash.startsWith('fig_')) return { section: 'dataset' as Section, figure: hash }
    if (sections.includes(hash as Section)) return { section: hash as Section, figure: null }
    return { section: 'home' as Section, figure: null }
  }
  const initial = getHashState()
  const [active, setActive] = useState<Section>(initial.section)
  const [open, setOpen] = useState(false)
  const [selectedFigure, setSelectedFigure] = useState<string | null>(initial.figure)

  // Sync hash ↔ state
  const selectFigure = (id: string | null) => {
    setSelectedFigure(id)
    if (id) {
      window.location.hash = id
    } else {
      window.location.hash = active
    }
  }

  const switchSection = (section: Section) => {
    setActive(section)
    setSelectedFigure(null)
    window.location.hash = section
  }

  useEffect(() => {
    const onHash = () => {
      const state = getHashState()
      setActive(state.section)
      setSelectedFigure(state.figure)
    }
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  const annotateMode = isAnnotationMode()
  const [auth, setAuth] = useState<AuthState | null>(null)
  const [authChecked, setAuthChecked] = useState(false)

  // Auto-login from localStorage
  useEffect(() => {
    if (!annotateMode) { setAuthChecked(true); return }
    const saved = getSavedAuth()
    if (saved) {
      loginAPI(saved.name, saved.password).then(res => {
        if (res.ok) setAuth(saved)
        else clearStoredAuth()
        setAuthChecked(true)
      }).catch(() => setAuthChecked(true))
    } else {
      setAuthChecked(true)
    }
  }, [annotateMode])

  // Show login if annotation mode and not authenticated
  if (annotateMode && authChecked && !auth) {
    return <Login onLogin={setAuth} />
  }
  if (annotateMode && !authChecked) {
    return <div style={{ minHeight: '100vh', background: '#09090b' }} />
  }

  // Hide the sidebar everywhere except annotation mode (annotators need logout).
  const showSidebar = annotateMode

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#09090b' }}>
      {/* ── Sidebar (annotation mode only) ── */}
      {showSidebar && (
      <nav
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        style={{
          position: 'fixed', left: 0, top: 0, bottom: 0,
          width: open ? 192 : 52,
          background: '#09090b',
          borderRight: '1px solid rgba(255,255,255,0.06)',
          display: 'flex', flexDirection: 'column',
          zIndex: 40,
          transition: 'width 0.2s cubic-bezier(0.4,0,0.2,1)',
          overflow: 'hidden',
        }}
      >
        {/* Logo */}
        <div style={{
          height: 52, display: 'flex', alignItems: 'center', padding: '0 13px',
          borderBottom: '1px solid rgba(255,255,255,0.06)', flexShrink: 0,
        }}>
          <div style={{
            width: 26, height: 26, borderRadius: 7, background: '#3b82f6',
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
          }}>
            <span style={{ color: '#fff', fontSize: 10, fontWeight: 700 }}>SF</span>
          </div>
          <span style={{
            marginLeft: 12, fontSize: 13, fontWeight: 600, color: '#fafafa',
            whiteSpace: 'nowrap', opacity: open ? 1 : 0, transition: 'opacity 0.15s ease',
          }}>
            SciFig-Eval
          </span>
        </div>

        {/* Nav items */}
        <div style={{ flex: 1, padding: '8px 8px' }}>
          {sections.map(id => {
            const { label, ready } = sectionMeta[id]
            const isActive = active === id
            return (
              <button
                key={id}
                onClick={() => { if (ready) switchSection(id) }}
                style={{
                  display: 'flex', alignItems: 'center', gap: 10,
                  width: '100%', height: 34, padding: '0 8px', borderRadius: 6,
                  border: 'none',
                  background: isActive ? '#232329' : 'transparent',
                  color: isActive ? '#fafafa' : ready ? '#a1a1aa' : '#52525b',
                  fontSize: 13, fontWeight: isActive ? 500 : 400,
                  fontFamily: 'inherit', cursor: ready ? 'pointer' : 'default',
                  marginBottom: 2, transition: 'background 0.15s, color 0.15s',
                }}
                onMouseEnter={e => { if (ready && !isActive) { e.currentTarget.style.background = '#1c1c21'; e.currentTarget.style.color = '#fafafa' } }}
                onMouseLeave={e => { if (!isActive) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = ready ? '#a1a1aa' : '#52525b' } }}
              >
                <NavIcon id={id} />
                <span style={{
                  whiteSpace: 'nowrap', opacity: open ? 1 : 0,
                  transition: 'opacity 0.15s ease',
                  display: 'flex', alignItems: 'center', gap: 8,
                }}>
                  {label}
                  {!ready && (
                    <span style={{
                      fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
                      letterSpacing: '0.05em', padding: '1px 6px', borderRadius: 4,
                      background: '#131316', border: '1px solid rgba(255,255,255,0.06)',
                      color: '#52525b',
                    }}>Soon</span>
                  )}
                </span>
              </button>
            )
          })}
        </div>

        {/* Annotator badge + logout */}
        {auth && (
          <div style={{
            padding: '8px 10px', borderTop: '1px solid rgba(255,255,255,0.06)',
            overflow: 'hidden',
          }}>
            <div style={{
              display: 'flex', alignItems: 'center', gap: 8,
              opacity: open ? 1 : 0, transition: 'opacity 0.15s ease',
            }}>
              <div style={{
                width: 8, height: 8, borderRadius: '50%', background: '#22c55e', flexShrink: 0,
              }} />
              <span style={{ fontSize: 11, color: '#a1a1aa', whiteSpace: 'nowrap', flex: 1 }}>
                {displayName(auth.name)}
              </span>
              <button
                onClick={() => { clearStoredAuth(); setAuth(null) }}
                style={{
                  background: 'none', border: 'none', cursor: 'pointer',
                  color: '#52525b', fontSize: 10, fontFamily: 'inherit',
                  padding: '2px 0', whiteSpace: 'nowrap',
                  transition: 'color 0.15s',
                }}
                onMouseEnter={e => e.currentTarget.style.color = '#fafafa'}
                onMouseLeave={e => e.currentTarget.style.color = '#52525b'}
              >
                Logout
              </button>
            </div>
            {!open && (
              <div style={{
                width: 8, height: 8, borderRadius: '50%', background: '#22c55e',
                margin: '0 auto',
              }} />
            )}
          </div>
        )}
      </nav>
      )}

      {/* ── Main ── */}
      <main style={{ flex: 1, marginLeft: showSidebar ? 52 : 0 }}>
        {selectedFigure ? (
          <FigureDetail
            figureId={selectedFigure}
            onBack={() => selectFigure(null)}
            auth={auth}
          />
        ) : (
          <>
            {active === 'home' && <Landing onExploreDataset={() => switchSection('dataset')} />}
            {active === 'dataset' && <Dataset onSelectFigure={selectFigure} />}
            {active === 'tasks' && <Tasks />}
            {active === 'evaluation' && <PlaceholderPage label="Evaluation" />}
            {active === 'analytics' && <PlaceholderPage label="Result Analytics" />}
          </>
        )}
      </main>
    </div>
  )
}

function PlaceholderPage({ label }: { label: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: 18, fontWeight: 500, color: '#a1a1aa' }}>{label}</p>
        <p style={{ fontSize: 13, color: '#52525b', marginTop: 6 }}>Coming soon</p>
      </div>
    </div>
  )
}

function NavIcon({ id }: { id: string }) {
  const s = { width: 18, height: 18, flexShrink: 0 } as const
  if (id === 'home') return (
    <svg style={s} viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2.5 8L9 2.5l6.5 5.5" />
      <path d="M4 7.5V15h10V7.5" />
      <path d="M7 15v-4h4v4" />
    </svg>
  )
  if (id === 'tasks') return (
    <svg style={s} viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 9l3 3 7-7" /><rect x="2" y="2" width="14" height="14" rx="2" />
    </svg>
  )
  if (id === 'dataset') return (
    <svg style={s} viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="2" width="5.5" height="5.5" rx="1.2" /><rect x="10.5" y="2" width="5.5" height="5.5" rx="1.2" />
      <rect x="2" y="10.5" width="5.5" height="5.5" rx="1.2" /><rect x="10.5" y="10.5" width="5.5" height="5.5" rx="1.2" />
    </svg>
  )
  if (id === 'evaluation') return (
    <svg style={s} viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 9.5l2 2 4-5" /><circle cx="9" cy="9" r="7" />
    </svg>
  )
  return (
    <svg style={s} viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 15V9.5" /><path d="M7 15V5" /><path d="M11 15V10.5" /><path d="M15 15V3" />
    </svg>
  )
}
