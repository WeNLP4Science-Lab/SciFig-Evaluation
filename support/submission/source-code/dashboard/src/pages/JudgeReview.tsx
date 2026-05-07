import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import type { DataManifest, JudgeType } from '../types'
import { JUDGE_LABELS } from '../types'
import AnnotatedText from '../components/AnnotatedText'
import { FIGURES_BASE_URL } from '../config'
import ErrorPanel from '../components/ErrorPanel'
import FigureSidebar from '../components/FigureSidebar'
import { useTheme } from '../ThemeContext'

const JUDGE_TYPES: JudgeType[] = ['reference_free', 'reference_only', 'reference_with_image']

const JUDGE_ICONS: Record<JudgeType, React.ReactNode> = {
  reference_free: (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="16" />
      <line x1="8" y1="12" x2="16" y2="12" />
    </svg>
  ),
  reference_only: (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  ),
  reference_with_image: (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <circle cx="8.5" cy="8.5" r="1.5" />
      <polyline points="21 15 16 10 5 21" />
    </svg>
  ),
}

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

interface JudgeReviewProps {
  manifestFile?: string
  title?: string
}

export default function JudgeReview({ manifestFile = 'manifest.json', title = 'Judge Review' }: JudgeReviewProps) {
  const [manifest, setManifest] = useState<DataManifest | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [selectedModel, setSelectedModel] = useState<string>('')
  const [selectedSubfolder, setSelectedSubfolder] = useState<string>('')
  const [selectedFigure, setSelectedFigure] = useState<string>('')
  const [selectedJudgeModel, setSelectedJudgeModel] = useState<string>('')
  const [activeJudge, setActiveJudge] = useState<JudgeType>('reference_free')
  const [hoveredError, setHoveredError] = useState<number | null>(null)
  const [highlightedCategory, setHighlightedCategory] = useState<string | null>(null)
  const [focusedError, setFocusedError] = useState<number | null>(null)

  const { isDark } = useTheme()

  useEffect(() => {
    setLoading(true)
    setManifest(null)
    const url = import.meta.env.PROD && (manifestFile === 'manifest_full.json' || manifestFile === 'manifest_sample.json')
      ? `https://scifigfigures.blob.core.windows.net/data/${manifestFile}`
      : `${import.meta.env.BASE_URL}data/${manifestFile}`
    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`Failed to load ${manifestFile}`)
        return r.json()
      })
      .then((data: DataManifest) => {
        setManifest(data)
        if (data.models.length) setSelectedModel(data.models[0])
        if (data.subfolders.length) setSelectedSubfolder(data.subfolders[0])
        if (data.judge_models?.length) setSelectedJudgeModel(data.judge_models[0])
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [manifestFile])

  const filteredFigures = useMemo(() => {
    if (!manifest) return []
    return manifest.figures.filter(
      f => f.model_name === selectedModel && f.subfolder === selectedSubfolder
    )
  }, [manifest, selectedModel, selectedSubfolder])

  const figureKeys = useMemo(() => filteredFigures.map(f => f.figure_key), [filteredFigures])

  useEffect(() => {
    if (filteredFigures.length && !filteredFigures.find(f => f.figure_key === selectedFigure)) {
      setSelectedFigure(filteredFigures[0].figure_key)
    }
  }, [filteredFigures, selectedFigure])

  const availableJudges = useMemo(() => {
    if (!manifest) return []
    return manifest.judge_models || []
  }, [manifest])

  const currentFigure = filteredFigures.find(f => f.figure_key === selectedFigure)
  const currentJudgeResults = currentFigure?.judges[selectedJudgeModel]
  const currentJudge = currentJudgeResults?.[activeJudge]

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
          Loading evaluation data
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
          python3 scripts/evaluation/export_dashboard_data.py --judge gpt-5-mini
        </code>
      </div>
    </div>
  )

  if (!manifest) return null

  return (
    <div
      className="h-screen flex flex-col overflow-hidden animate-fade-in"
      style={{ backgroundColor: 'var(--m3-surface)' }}
    >
      {/* Top Bar */}
      <header
        className="px-6 h-16 flex items-center gap-4"
        style={{
          borderBottom: `1px solid var(--m3-outline-variant)`,
          backgroundColor: 'var(--m3-surface)',
        }}
      >
        <Link
          to="/evaluation"
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
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" />
              <rect x="9" y="3" width="6" height="4" rx="2" />
            </svg>
          </div>
          <h1
            className="text-base font-medium"
            style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}
          >
            {title}
          </h1>
        </div>

        <div className="ml-auto">
          <ThemeToggle />
        </div>
      </header>

      {/* Controls Bar */}
      <div
        className="px-6 h-14 flex items-center gap-6"
        style={{
          borderBottom: `1px solid var(--m3-outline-variant)`,
          backgroundColor: 'var(--m3-surface-container-low)',
        }}
      >
        <div className="flex items-center gap-2">
          <label
            className="text-[11px] font-medium uppercase"
            style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
          >
            Model
          </label>
          <select
            className="m3-select"
            value={selectedModel}
            onChange={e => setSelectedModel(e.target.value)}
          >
            {manifest.models.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>

        <div className="w-px h-6" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />

        <div className="flex items-center gap-2">
          <label
            className="text-[11px] font-medium uppercase"
            style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
          >
            Dataset
          </label>
          <select
            className="m3-select"
            value={selectedSubfolder}
            onChange={e => setSelectedSubfolder(e.target.value)}
          >
            {manifest.subfolders.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <div className="w-px h-6" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />

        <div className="flex items-center gap-2">
          <label
            className="text-[11px] font-medium uppercase"
            style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
          >
            Judge
          </label>
          <select
            className="m3-select"
            value={selectedJudgeModel}
            onChange={e => setSelectedJudgeModel(e.target.value)}
          >
            {availableJudges.map(j => <option key={j} value={j}>{j}</option>)}
          </select>
        </div>

        <span
          className="ml-auto text-xs font-medium tabular-nums px-3 py-1 rounded-full"
          style={{
            backgroundColor: 'var(--m3-surface-container-highest)',
            color: 'var(--m3-on-surface-variant)',
            letterSpacing: '0.1px',
          }}
        >
          {filteredFigures.length} figures
        </span>
      </div>

      {/* Main Content with Sidebar */}
      {currentFigure && currentJudge ? (
        <div className="flex-1 flex min-h-0 overflow-hidden">
          {/* Sidebar */}
          <FigureSidebar
            figureKeys={figureKeys}
            selectedKey={selectedFigure}
            onSelect={setSelectedFigure}
          />

          {/* Content area */}
          <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
            {/* Segmented Button - M3 Style */}
            <div
              className="px-6 py-3 flex items-center"
              style={{
                borderBottom: `1px solid var(--m3-outline-variant)`,
                backgroundColor: 'var(--m3-surface)',
              }}
            >
              <div
                className="inline-flex rounded-full overflow-hidden"
                style={{ border: `1px solid var(--m3-outline)` }}
              >
                {JUDGE_TYPES.map((jt, idx) => {
                  const isActive = activeJudge === jt
                  const hasData = currentJudgeResults?.[jt]
                  const score = currentJudgeResults?.[jt]?.mqm_score
                  return (
                    <button
                      key={jt}
                      onClick={() => setActiveJudge(jt)}
                      className="flex items-center gap-2 px-5 py-2 text-xs font-medium"
                      style={{
                        backgroundColor: isActive
                          ? 'var(--m3-secondary-container)'
                          : 'transparent',
                        color: isActive
                          ? 'var(--m3-on-secondary-container)'
                          : hasData
                            ? 'var(--m3-on-surface)'
                            : 'var(--m3-outline)',
                        borderRight: idx < JUDGE_TYPES.length - 1
                          ? `1px solid var(--m3-outline)`
                          : 'none',
                        cursor: hasData ? 'pointer' : 'not-allowed',
                        opacity: hasData ? 1 : 0.5,
                        transition: 'all 200ms var(--m3-easing-standard)',
                        letterSpacing: '0.1px',
                      }}
                      disabled={!hasData}
                    >
                      {isActive && (
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                      {!isActive && JUDGE_ICONS[jt]}
                      {JUDGE_LABELS[jt]}
                      {score != null && (
                        <span
                          className="px-2 py-0.5 rounded-full text-[10px] font-medium tabular-nums"
                          style={{
                            backgroundColor:
                              score >= 80 ? 'rgba(76,175,124,0.12)' :
                              score >= 60 ? 'rgba(232,180,63,0.12)' :
                              'rgba(232,64,63,0.12)',
                            color:
                              score >= 80 ? (isDark ? '#4caf7c' : '#1a6b3e') :
                              score >= 60 ? (isDark ? '#e8b43f' : '#8a6b00') :
                              (isDark ? '#e8403f' : '#ba1a1a'),
                          }}
                        >
                          {score}
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Two-column layout */}
            <div className="flex-1 flex min-h-0 overflow-hidden">
              {/* Left column: Figure image + Annotated text */}
              <div
                className="w-1/2 overflow-y-auto overflow-x-hidden min-w-0"
                style={{
                  borderRight: `1px solid var(--m3-outline-variant)`,
                }}
              >
                {/* Figure image */}
                <div
                  className="p-6"
                  style={{
                    backgroundColor: 'var(--m3-surface-container-low)',
                    borderBottom: `1px solid var(--m3-outline-variant)`,
                  }}
                >
                  <div className="mb-4 animate-fade-in-up">
                    <div className="flex items-start justify-between mb-2">
                      <h3
                        className="text-sm font-medium"
                        style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}
                      >
                        {currentFigure.figure_key}
                      </h3>
                      <span
                        className="text-[11px] font-medium px-2.5 py-1 rounded-full"
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
                        className="text-xs leading-relaxed mb-1"
                        style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.4px' }}
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
                  <div
                    className="rounded-xl overflow-hidden animate-scale-in"
                    style={{
                      border: `1px solid var(--m3-outline-variant)`,
                      backgroundColor: 'var(--m3-surface-container)',
                    }}
                  >
                    <img
                      src={`${FIGURES_BASE_URL}/${currentFigure.figure_image.replace('figures/', '')}`}
                      alt={currentFigure.figure_key}
                      className="w-full"
                      style={{ display: 'block' }}
                    />
                  </div>
                </div>

                {/* Annotated text */}
                <div
                  className="p-6"
                  style={{ backgroundColor: 'var(--m3-surface)' }}
                >
                  <div className="flex items-center gap-3 mb-5">
                    <h3
                      className="text-[11px] font-medium uppercase"
                      style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
                    >
                      Model Output
                    </h3>
                    <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
                  </div>
                  <div className="animate-fade-in-up">
                    <AnnotatedText
                      text={currentFigure.annotation}
                      errors={currentJudge.errors}
                      onErrorHover={setHoveredError}
                      onErrorClick={setFocusedError}
                      highlightedError={hoveredError}
                      highlightedCategory={highlightedCategory}
                    />
                  </div>
                </div>
              </div>

              {/* Right column: Error panel */}
              <div
                className="w-1/2 p-6 overflow-y-auto overflow-x-hidden min-w-0"
                style={{
                  backgroundColor: 'var(--m3-surface-container-low)',
                }}
              >
                <div className="flex items-center gap-3 mb-5">
                  <h3
                    className="text-[11px] font-medium uppercase"
                    style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
                  >
                    Evaluation
                  </h3>
                  <div className="flex-1 h-px" style={{ backgroundColor: 'var(--m3-outline-variant)' }} />
                </div>
                <ErrorPanel
                  errors={currentJudge.errors}
                  mqmScore={currentJudge.mqm_score}
                  errorCount={currentJudge.error_count}
                  onErrorHover={setHoveredError}
                  highlightedError={hoveredError}
                  onCategoryExpand={setHighlightedCategory}
                  focusedError={focusedError}
                />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex min-h-0">
          {/* Sidebar even when no figure selected */}
          <FigureSidebar
            figureKeys={figureKeys}
            selectedKey={selectedFigure}
            onSelect={setSelectedFigure}
          />
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
                {!currentFigure ? 'No figure selected' : 'No evaluation data for this judge type'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
