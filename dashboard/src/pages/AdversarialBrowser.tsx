import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL } from '../config'
import FigureSidebar from '../components/FigureSidebar'

interface AdversarialManifest {
  figures_by_subfolder: Record<string, string[]>
  total_figures: number
  transforms: Record<string, string>
}

const TRANSFORM_LABELS: Record<string, string> = {
  jpeg_compression: 'JPEG Compression',
  noise: 'Noise',
  grayscale: 'Grayscale',
  aspect_ratio: 'Aspect Ratio',
  low_contrast: 'Low Contrast',
}

const TRANSFORM_DESCRIPTIONS: Record<string, string> = {
  jpeg_compression: 'Artifacts from heavy compression (quality=15)',
  noise: 'Gaussian noise overlay (sigma=30)',
  grayscale: 'All color information removed',
  aspect_ratio: 'Width stretched by 1.2x (mild distortion)',
  low_contrast: 'Contrast reduced by 50% (faded appearance)',
}

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()
  return (
    <button onClick={toggleTheme} className="w-10 h-10 flex items-center justify-center rounded-full m3-state-hover" style={{ backgroundColor: 'var(--m3-surface-container-high)' }} aria-label="Toggle theme">
      {isDark ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
      )}
    </button>
  )
}

export default function AdversarialBrowser() {
  const [manifest, setManifest] = useState<AdversarialManifest | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSubfolder, setSelectedSubfolder] = useState('')
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedTransform, setSelectedTransform] = useState<string | null>(null)
  const { isDark } = useTheme()

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/adversarial_manifest.json`)
      .then(r => r.json())
      .then((data: AdversarialManifest) => {
        setManifest(data)
        const subs = Object.keys(data.figures_by_subfolder).sort()
        if (subs.length) {
          setSelectedSubfolder(subs[0])
          const figs = data.figures_by_subfolder[subs[0]]
          if (figs?.length) setSelectedFigure(figs[0])
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const subfolders = useMemo(() => manifest ? Object.keys(manifest.figures_by_subfolder).sort() : [], [manifest])
  const figures = useMemo(() => manifest?.figures_by_subfolder[selectedSubfolder] || [], [manifest, selectedSubfolder])
  const transforms = useMemo(() => manifest ? Object.keys(manifest.transforms) : [], [manifest])

  useEffect(() => {
    if (figures.length && !figures.includes(selectedFigure)) {
      setSelectedFigure(figures[0])
    }
  }, [figures, selectedFigure])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>Loading</span>
      </div>
    </div>
  )

  if (!manifest) return null

  return (
    <div className="h-screen flex flex-col overflow-hidden animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header className="px-6 h-16 flex items-center gap-4" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface)' }}>
        <Link to="/" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
        </Link>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--m3-primary)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <h1 className="text-base font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}>Adversarial Transforms</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <div className="flex items-center gap-2">
            <label className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Dataset</label>
            <select className="m3-select" value={selectedSubfolder} onChange={e => setSelectedSubfolder(e.target.value)}>
              {subfolders.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <span className="text-xs font-medium tabular-nums px-3 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
            {figures.length} figures
          </span>
          <ThemeToggle />
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 flex min-h-0 overflow-hidden">
        {/* Sidebar */}
        <FigureSidebar
          figureKeys={figures}
          selectedKey={selectedFigure}
          onSelect={setSelectedFigure}
        />

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          {/* Original section */}
          <div className="p-6" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container-low)' }}>
            <div className="flex items-start gap-6 animate-fade-in-up">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-4">
                  <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                    {selectedFigure}
                  </h2>
                  <span className="text-[11px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)', letterSpacing: '0.5px' }}>
                    Original
                  </span>
                </div>
                <div className="rounded-xl overflow-hidden inline-block" style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}>
                  <img
                    src={`${FIGURES_BASE_URL}/${selectedSubfolder}/${selectedFigure}.png`}
                    alt={`${selectedFigure} original`}
                    className="max-h-72 w-auto"
                    style={{ display: 'block' }}
                  />
                </div>
              </div>

              {/* Enlarged transform preview */}
              {selectedTransform && (
                <div className="flex-1 animate-fade-in">
                  <div className="flex items-center gap-3 mb-4">
                    <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                      {TRANSFORM_LABELS[selectedTransform]}
                    </h2>
                    <span className="text-[11px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>
                      Transformed
                    </span>
                  </div>
                  <div className="rounded-xl overflow-hidden inline-block" style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}>
                    <img
                      src={`${FIGURES_BASE_URL}/transform_${selectedTransform}/${selectedSubfolder}/${selectedFigure}.png`}
                      alt={`${selectedFigure} ${selectedTransform}`}
                      className="max-h-72 w-auto"
                      style={{ display: 'block' }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Transforms grid */}
          <div className="p-6" style={{ backgroundColor: 'var(--m3-surface)' }}>
            <div className="flex items-center gap-3 mb-5">
              <h3 className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                Transforms
              </h3>
              <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
              {selectedTransform && (
                <button
                  onClick={() => setSelectedTransform(null)}
                  className="text-[11px] font-medium px-2.5 py-1 rounded-full m3-state-hover"
                  style={{ color: 'var(--m3-primary)', backgroundColor: 'var(--m3-surface-container-high)' }}
                >
                  Clear selection
                </button>
              )}
            </div>

            <div className="grid grid-cols-5 gap-4">
              {transforms.map(t => {
                const isActive = selectedTransform === t
                return (
                  <button
                    key={t}
                    onClick={() => setSelectedTransform(isActive ? null : t)}
                    className="rounded-xl overflow-hidden text-left group"
                    style={{
                      border: isActive
                        ? '2px solid var(--m3-primary)'
                        : `1px solid var(--m3-outline-variant)`,
                      backgroundColor: isActive
                        ? 'var(--m3-surface-container-high)'
                        : 'var(--m3-surface-container)',
                      transition: 'all 200ms var(--m3-easing-standard)',
                    }}
                  >
                    <div className="aspect-[4/3] overflow-hidden" style={{ backgroundColor: 'var(--m3-surface-container-highest)' }}>
                      <img
                        src={`${FIGURES_BASE_URL}/transform_${t}/${selectedSubfolder}/${selectedFigure}.png`}
                        alt={`${selectedFigure} ${t}`}
                        className="w-full h-full object-contain transition-transform duration-300 group-hover:scale-105"
                        style={{ display: 'block' }}
                      />
                    </div>
                    <div className="p-3">
                      <h4 className="text-xs font-medium mb-0.5" style={{ color: isActive ? 'var(--m3-primary)' : 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                        {TRANSFORM_LABELS[t]}
                      </h4>
                      <p className="text-[10px] leading-relaxed" style={{ color: 'var(--m3-outline)', letterSpacing: '0.4px' }}>
                        {TRANSFORM_DESCRIPTIONS[t]}
                      </p>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
