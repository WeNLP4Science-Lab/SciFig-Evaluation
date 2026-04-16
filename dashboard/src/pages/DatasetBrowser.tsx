import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import type { DatasetManifest } from '../types'
import FigureSidebar from '../components/FigureSidebar'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL } from '../config'

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()
  return (
    <button
      onClick={toggleTheme}
      className="w-10 h-10 flex items-center justify-center rounded-full m3-state-hover"
      style={{ backgroundColor: 'var(--m3-surface-container-high)' }}
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

export default function DatasetBrowser() {
  const [dataset, setDataset] = useState<DatasetManifest | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedSubfolder, setSelectedSubfolder] = useState<string>('')
  const [selectedFigureType, setSelectedFigureType] = useState<string>('')
  const [selectedFigure, setSelectedFigure] = useState<string>('')
  const { isDark } = useTheme()

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/dataset.json`)
      .then(r => {
        if (!r.ok) throw new Error('Failed to load dataset.json')
        return r.json()
      })
      .then((data: DatasetManifest) => {
        setDataset(data)
        if (data.subfolders.length) setSelectedSubfolder(data.subfolders[0])
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  // Figures filtered by subfolder only (for computing available figure types)
  const subfolderFigures = useMemo(() => {
    if (!dataset) return []
    if (!selectedSubfolder) return dataset.figures
    return dataset.figures.filter(f => f.subfolder === selectedSubfolder)
  }, [dataset, selectedSubfolder])

  // Available figure types for current subfolder
  const figureTypes = useMemo(() => {
    const types = new Map<string, number>()
    subfolderFigures.forEach(f => {
      types.set(f.figure_type, (types.get(f.figure_type) || 0) + 1)
    })
    return Array.from(types.entries()).sort((a, b) => b[1] - a[1])
  }, [subfolderFigures])

  // Reset figure type filter when subfolder changes
  useEffect(() => {
    setSelectedFigureType('')
  }, [selectedSubfolder])

  // Final filtered figures (subfolder + figure type)
  const filteredFigures = useMemo(() => {
    if (!selectedFigureType) return subfolderFigures
    return subfolderFigures.filter(f => f.figure_type === selectedFigureType)
  }, [subfolderFigures, selectedFigureType])

  const figureKeys = useMemo(() => filteredFigures.map(f => f.figure_key), [filteredFigures])

  useEffect(() => {
    if (filteredFigures.length && !filteredFigures.find(f => f.figure_key === selectedFigure)) {
      setSelectedFigure(filteredFigures[0].figure_key)
    }
  }, [filteredFigures, selectedFigure])

  const currentFigure = filteredFigures.find(f => f.figure_key === selectedFigure)

  // Loading
  if (loading) return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div
          className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin"
          style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }}
        />
        <span
          className="text-sm font-medium"
          style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.25px' }}
        >
          Loading dataset
        </span>
      </div>
    </div>
  )

  // Error
  if (error) return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      <div className="text-center animate-fade-in max-w-md">
        <div
          className="w-14 h-14 rounded-2xl mx-auto mb-5 flex items-center justify-center"
          style={{ backgroundColor: 'var(--m3-error-container)' }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke={isDark ? '#f2b8b5' : '#ba1a1a'} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
        </div>
        <p
          className="text-sm font-medium mb-2"
          style={{ color: 'var(--m3-error)', letterSpacing: '0.25px' }}
        >
          {error}
        </p>
        <p
          className="text-xs mb-4"
          style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.4px' }}
        >
          Run the export script first:
        </p>
        <code
          className="inline-block px-4 py-3 rounded-lg text-xs font-mono"
          style={{
            backgroundColor: 'var(--m3-surface-container)',
            color: 'var(--m3-on-surface-variant)',
            border: `1px solid var(--m3-outline-variant)`,
          }}
        >
          python3 scripts/evaluation/export_dashboard_data.py --dataset
        </code>
      </div>
    </div>
  )

  if (!dataset) return null

  return (
    <div
      className="h-screen flex flex-col overflow-hidden animate-fade-in"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      {/* Header */}
      <header
        className="px-6 h-16 flex items-center gap-4"
        style={{
          borderBottom: '1px solid var(--m3-outline-variant)',
          backgroundColor: 'var(--m3-surface)',
        }}
      >
        <Link
          to="/dataset"
          className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg"
          style={{
            color: 'var(--m3-on-surface-variant)',
            transition: 'all 200ms var(--m3-easing-standard)',
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 12H5" />
            <path d="M12 19l-7-7 7-7" />
          </svg>
        </Link>

        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: 'var(--m3-primary)' }}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
          </div>
          <h1
            className="text-base font-medium"
            style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}
          >
            Dataset Browser
          </h1>
        </div>

        <div className="ml-auto">
          <ThemeToggle />
        </div>
      </header>

      {/* Subfolder Filter Chips */}
      <div
        className="px-6 py-3 flex items-center gap-2 flex-wrap"
        style={{
          borderBottom: '1px solid var(--m3-outline-variant)',
          backgroundColor: 'var(--m3-surface-container-low)',
        }}
      >
        {dataset.subfolders.map(sub => {
          const isActive = selectedSubfolder === sub
          const count = dataset.subfolder_counts[sub] ?? 0
          return (
            <button
              key={sub}
              onClick={() => setSelectedSubfolder(sub)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium"
              style={{
                backgroundColor: isActive
                  ? 'var(--m3-secondary-container)'
                  : 'transparent',
                border: `1px solid ${isActive ? 'var(--m3-secondary-container)' : 'var(--m3-outline-variant)'}`,
                color: isActive
                  ? 'var(--m3-on-secondary-container)'
                  : 'var(--m3-on-surface-variant)',
                transition: 'all 200ms var(--m3-easing-standard)',
                letterSpacing: '0.1px',
                cursor: 'pointer',
              }}
            >
              {isActive && (
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              )}
              {sub}
              <span
                className="px-1.5 py-0.5 rounded-full text-[10px] font-medium tabular-nums"
                style={{
                  backgroundColor: isActive
                    ? 'color-mix(in srgb, var(--m3-on-secondary-container) 12%, transparent)'
                    : 'var(--m3-surface-container-highest)',
                  color: isActive
                    ? 'var(--m3-on-secondary-container)'
                    : 'var(--m3-on-surface-variant)',
                }}
              >
                {count}
              </span>
            </button>
          )
        })}
      </div>

      {/* Figure Type Filter Chips */}
      {figureTypes.length > 1 && (
        <div
          className="px-6 py-2.5 flex items-center gap-2 flex-wrap"
          style={{
            borderBottom: '1px solid var(--m3-outline-variant)',
            backgroundColor: 'var(--m3-surface)',
          }}
        >
          <span
            className="text-[11px] font-medium uppercase mr-1"
            style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
          >
            Type
          </span>
          <button
            onClick={() => setSelectedFigureType('')}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[11px] font-medium"
            style={{
              backgroundColor: !selectedFigureType
                ? 'var(--m3-tertiary-container)'
                : 'transparent',
              border: `1px solid ${!selectedFigureType ? 'var(--m3-tertiary-container)' : 'var(--m3-outline-variant)'}`,
              color: !selectedFigureType
                ? 'var(--m3-on-tertiary-container)'
                : 'var(--m3-on-surface-variant)',
              transition: 'all 200ms var(--m3-easing-standard)',
              letterSpacing: '0.1px',
              cursor: 'pointer',
            }}
          >
            All
            <span
              className="px-1.5 py-0.5 rounded-full text-[10px] font-medium tabular-nums"
              style={{
                backgroundColor: !selectedFigureType
                  ? 'color-mix(in srgb, var(--m3-on-tertiary-container) 12%, transparent)'
                  : 'var(--m3-surface-container-highest)',
                color: !selectedFigureType
                  ? 'var(--m3-on-tertiary-container)'
                  : 'var(--m3-on-surface-variant)',
              }}
            >
              {subfolderFigures.length}
            </span>
          </button>
          {figureTypes.map(([type, count]) => {
            const isActive = selectedFigureType === type
            return (
              <button
                key={type}
                onClick={() => setSelectedFigureType(isActive ? '' : type)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[11px] font-medium"
                style={{
                  backgroundColor: isActive
                    ? 'var(--m3-tertiary-container)'
                    : 'transparent',
                  border: `1px solid ${isActive ? 'var(--m3-tertiary-container)' : 'var(--m3-outline-variant)'}`,
                  color: isActive
                    ? 'var(--m3-on-tertiary-container)'
                    : 'var(--m3-on-surface-variant)',
                  transition: 'all 200ms var(--m3-easing-standard)',
                  letterSpacing: '0.1px',
                  cursor: 'pointer',
                }}
              >
                {isActive && (
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                )}
                {type}
                <span
                  className="px-1.5 py-0.5 rounded-full text-[10px] font-medium tabular-nums"
                  style={{
                    backgroundColor: isActive
                      ? 'color-mix(in srgb, var(--m3-on-tertiary-container) 12%, transparent)'
                      : 'var(--m3-surface-container-highest)',
                    color: isActive
                      ? 'var(--m3-on-tertiary-container)'
                      : 'var(--m3-on-surface-variant)',
                  }}
                >
                  {count}
                </span>
              </button>
            )
          })}
        </div>
      )}

      {/* Main area with sidebar */}
      <div className="flex-1 flex min-h-0">
        {/* Sidebar */}
        <FigureSidebar
          figureKeys={figureKeys}
          selectedKey={selectedFigure}
          onSelect={setSelectedFigure}
        />

        {/* Content */}
        {currentFigure ? (
          <div
            className="flex-1 overflow-y-auto p-6"
            style={{ backgroundColor: 'var(--m3-surface)' }}
          >
            {/* Metadata */}
            <div className="mb-6 animate-fade-in-up">
              <div className="flex items-start justify-between mb-2">
                <h2
                  className="text-lg font-medium"
                  style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}
                >
                  {currentFigure.figure_key}
                </h2>
                <span
                  className="text-[11px] font-medium px-2.5 py-1 rounded-full flex-shrink-0 ml-3"
                  style={{
                    backgroundColor: 'var(--m3-surface-container-highest)',
                    color: 'var(--m3-on-surface-variant)',
                    letterSpacing: '0.5px',
                  }}
                >
                  {currentFigure.figure_type}
                </span>
              </div>
              {currentFigure.paper_title && (
                <p
                  className="text-sm leading-relaxed mb-1"
                  style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.25px' }}
                >
                  {currentFigure.paper_title}
                </p>
              )}
              {currentFigure.caption && (
                <p
                  className="text-xs leading-relaxed"
                  style={{ color: 'var(--m3-outline)', letterSpacing: '0.4px' }}
                >
                  {currentFigure.caption}
                </p>
              )}
            </div>

            {/* Figure Image */}
            <div
              className="rounded-xl overflow-hidden mb-8 animate-scale-in"
              style={{
                border: '1px solid var(--m3-outline-variant)',
                backgroundColor: 'var(--m3-surface-container)',
              }}
            >
              <img
                src={`${FIGURES_BASE_URL}/${currentFigure.figure_image.replace('figures/', '')}`}
                alt={currentFigure.figure_key}
                className="w-full max-w-2xl mx-auto"
                style={{ display: 'block' }}
              />
            </div>

            {/* Groundtruth Annotations */}
            <div className="mb-4">
              <div className="flex items-center gap-3 mb-4">
                <h3
                  className="text-[11px] font-medium uppercase"
                  style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
                >
                  Groundtruth Annotations
                </h3>
                <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
              </div>

              <div className={currentFigure.annotations.length === 1
                ? ''
                : 'grid grid-cols-1 lg:grid-cols-2 gap-4'
              }>
                {currentFigure.annotations.map((ann, i) => (
                  <div
                    key={i}
                    className="rounded-xl p-5"
                    style={{
                      backgroundColor: 'var(--m3-surface-container)',
                      border: '1px solid var(--m3-outline-variant)',
                    }}
                  >
                    <div className="flex items-center gap-2 mb-3">
                      <span
                        className="text-[11px] font-medium px-2.5 py-1 rounded-full"
                        style={{
                          backgroundColor: 'var(--m3-primary-container)',
                          color: 'var(--m3-on-primary-container)',
                          letterSpacing: '0.5px',
                        }}
                      >
                        {ann.annotation_language}
                      </span>
                      <span
                        className="text-xs font-medium"
                        style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.1px' }}
                      >
                        Annotator #{ann.annotated_by}
                      </span>
                    </div>
                    <p
                      className="text-sm leading-relaxed"
                      style={{
                        color: 'var(--m3-on-surface)',
                        whiteSpace: 'pre-wrap',
                        letterSpacing: '0.25px',
                        lineHeight: '22px',
                      }}
                    >
                      {ann.annotation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div
            className="flex-1 flex items-center justify-center"
            style={{ backgroundColor: 'var(--m3-surface)' }}
          >
            <div className="text-center animate-fade-in">
              <div
                className="w-14 h-14 rounded-2xl mx-auto mb-4 flex items-center justify-center"
                style={{ backgroundColor: 'var(--m3-surface-container-high)' }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--m3-outline)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21 15 16 10 5 21" />
                </svg>
              </div>
              <p
                className="text-sm font-medium"
                style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.25px' }}
              >
                No figure selected
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
