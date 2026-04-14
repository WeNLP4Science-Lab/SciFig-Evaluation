import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import FigureSidebar from '../components/FigureSidebar'

interface SampleManifest {
  description: string
  total: number
  figures?: {
    figure_key: string
    subfolder: string
    figure_type: string
    paper_title: string
    caption: string
    figure_image: string
    annotations: {
      annotation_language: string
      annotation: string
      annotated_by: number
      figure_type: string
    }[]
  }[]
  // Adversarial manifest format
  figures_by_subfolder?: Record<string, string[]>
  transforms?: string[]
  transform_labels?: Record<string, string>
  subfolders?: string[]
}

interface AdversarialSampleBrowserProps {
  manifestFile: string
  title: string
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

export default function AdversarialSampleBrowser({ manifestFile, title }: AdversarialSampleBrowserProps) {
  const [manifest, setManifest] = useState<SampleManifest | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSubfolder, setSelectedSubfolder] = useState('')
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedTransform, setSelectedTransform] = useState<string | null>(null)
  const { isDark } = useTheme()

  // Detect if this is adversarial format (has transforms) or sample format (has figures array)
  const isAdversarial = manifest?.transforms != null

  useEffect(() => {
    setLoading(true)
    fetch(`${import.meta.env.BASE_URL}data/${manifestFile}`)
      .then(r => r.json())
      .then((data: SampleManifest) => {
        setManifest(data)
        const subs = data.subfolders || []
        if (subs.length) setSelectedSubfolder(subs[0])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [manifestFile])

  const subfolders = useMemo(() => manifest?.subfolders || [], [manifest])

  const figureKeys = useMemo(() => {
    if (!manifest) return []
    if (isAdversarial && manifest.figures_by_subfolder) {
      return manifest.figures_by_subfolder[selectedSubfolder] || []
    }
    return (manifest.figures || []).filter(f => f.subfolder === selectedSubfolder).map(f => f.figure_key)
  }, [manifest, selectedSubfolder, isAdversarial])

  useEffect(() => {
    if (figureKeys.length && !figureKeys.includes(selectedFigure)) {
      setSelectedFigure(figureKeys[0])
    }
  }, [figureKeys, selectedFigure])

  // For non-adversarial, get figure data
  const currentFigureData = useMemo(() => {
    if (!manifest?.figures) return null
    return manifest.figures.find(f => f.figure_key === selectedFigure && f.subfolder === selectedSubfolder)
  }, [manifest, selectedFigure, selectedSubfolder])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>Loading</span>
      </div>
    </div>
  )

  if (!manifest) return null

  const imgBase = isAdversarial
    ? `${import.meta.env.BASE_URL}figures/adversarial/${selectedSubfolder}/${selectedFigure}`
    : null

  return (
    <div className="h-screen flex flex-col overflow-hidden animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header className="px-6 h-16 flex items-center gap-4" style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface)' }}>
        <Link to="/dataset" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
        </Link>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--m3-primary)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <h1 className="text-base font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}>{title}</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <div className="flex items-center gap-2">
            <label className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Dataset</label>
            <select className="m3-select" value={selectedSubfolder} onChange={e => setSelectedSubfolder(e.target.value)}>
              {subfolders.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <span className="text-xs font-medium tabular-nums px-3 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-on-surface-variant)' }}>
            {figureKeys.length} figures
          </span>
          <ThemeToggle />
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 flex min-h-0 overflow-hidden">
        <FigureSidebar figureKeys={figureKeys} selectedKey={selectedFigure} onSelect={k => { setSelectedFigure(k); setSelectedTransform(null) }} />

        <div className="flex-1 overflow-y-auto">
          {/* Original image */}
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
                {/* Show caption/title for non-adversarial */}
                {currentFigureData?.paper_title && (
                  <p className="text-xs leading-relaxed mb-1" style={{ color: 'var(--m3-on-surface-variant)' }}>{currentFigureData.paper_title}</p>
                )}
                {currentFigureData?.caption && (
                  <p className="text-xs leading-relaxed mb-3" style={{ color: 'var(--m3-outline)' }}>Caption: {currentFigureData.caption}</p>
                )}
                <div className="rounded-xl overflow-hidden inline-block" style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}>
                  <img
                    src={isAdversarial ? `${imgBase}/original.png` : `${import.meta.env.BASE_URL}${currentFigureData?.figure_image || `figures/${selectedSubfolder}/${selectedFigure}.png`}`}
                    alt={`${selectedFigure} original`}
                    className="max-h-72 w-auto"
                    style={{ display: 'block' }}
                  />
                </div>
              </div>

              {/* Selected transform preview */}
              {isAdversarial && selectedTransform && (
                <div className="flex-1 animate-fade-in">
                  <div className="flex items-center gap-3 mb-4">
                    <h2 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                      {manifest.transform_labels?.[selectedTransform] || selectedTransform}
                    </h2>
                    <span className="text-[11px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: 'var(--m3-error-container)', color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>
                      Transformed
                    </span>
                  </div>
                  <div className="rounded-xl overflow-hidden inline-block" style={{ border: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface-container)' }}>
                    <img
                      src={`${imgBase}/${selectedTransform}.png`}
                      alt={`${selectedFigure} ${selectedTransform}`}
                      className="max-h-72 w-auto"
                      style={{ display: 'block' }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Transforms grid (adversarial only) */}
          {isAdversarial && manifest.transforms && (
            <div className="p-6" style={{ backgroundColor: 'var(--m3-surface)' }}>
              <div className="flex items-center gap-3 mb-5">
                <h3 className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                  Transforms ({manifest.transforms.length})
                </h3>
                <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
                {selectedTransform && (
                  <button onClick={() => setSelectedTransform(null)} className="text-[11px] font-medium px-2.5 py-1 rounded-full m3-state-hover" style={{ color: 'var(--m3-primary)', backgroundColor: 'var(--m3-surface-container-high)' }}>
                    Clear
                  </button>
                )}
              </div>
              <div className="grid grid-cols-4 lg:grid-cols-7 gap-3">
                {manifest.transforms.map(t => {
                  const isActive = selectedTransform === t
                  return (
                    <button
                      key={t}
                      onClick={() => setSelectedTransform(isActive ? null : t)}
                      className="rounded-xl overflow-hidden text-left group"
                      style={{
                        border: isActive ? '2px solid var(--m3-primary)' : `1px solid var(--m3-outline-variant)`,
                        backgroundColor: isActive ? 'var(--m3-surface-container-high)' : 'var(--m3-surface-container)',
                        transition: 'all 200ms var(--m3-easing-standard)',
                      }}
                    >
                      <div className="aspect-[4/3] overflow-hidden" style={{ backgroundColor: 'var(--m3-surface-container-highest)' }}>
                        <img
                          src={`${imgBase}/${t}.png`}
                          alt={`${selectedFigure} ${t}`}
                          className="w-full h-full object-contain transition-transform duration-300 group-hover:scale-105"
                          style={{ display: 'block' }}
                        />
                      </div>
                      <div className="p-2">
                        <h4 className="text-[10px] font-medium" style={{ color: isActive ? 'var(--m3-primary)' : 'var(--m3-on-surface)', letterSpacing: '0.1px' }}>
                          {manifest.transform_labels?.[t] || t}
                        </h4>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          {/* Annotations (non-adversarial) */}
          {!isAdversarial && currentFigureData?.annotations && (
            <div className="p-6" style={{ backgroundColor: 'var(--m3-surface)' }}>
              <div className="flex items-center gap-3 mb-5">
                <h3 className="text-[11px] font-medium uppercase" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>
                  Groundtruth Annotations ({currentFigureData.annotations.length})
                </h3>
                <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
              </div>
              <div className="space-y-4">
                {currentFigureData.annotations.map((ann, idx) => (
                  <div key={idx} className="rounded-lg p-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' }}>
                        {ann.annotation_language}
                      </span>
                      <span className="text-[10px]" style={{ color: 'var(--m3-outline)' }}>Annotator {ann.annotated_by}</span>
                    </div>
                    <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.25px' }}>
                      {ann.annotation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
