import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { FIGURES_BASE_URL } from '../config'
import { useTheme } from '../ThemeContext'

const ALL_MODELS = [
  'gemini-3.1-pro', 'gpt-5.2',
  'qwen3-vl-235b-a22b', 'qwen3-vl-32b', 'qwen3-vl-30b-a3b', 'qwen3-vl-8b',
  'llama4-maverick', 'llama4-scout',
  'gemma3-27b-it', 'gemma3-12b-it', 'gemma3-4b-it', 'phi-4-multimodal',
]

const TRANSFORMS = [
  'original', 'jpeg_compression', 'noise', 'aspect_ratio',
  'low_contrast', 'rotation', 'original_in_paper', 'blurred_in_paper',
]

const TRANSFORM_LABELS: Record<string, string> = {
  original: 'Original', jpeg_compression: 'JPEG', noise: 'Noise',
  aspect_ratio: 'Aspect Ratio', low_contrast: 'Low Contrast',
  rotation: 'Rotation', original_in_paper: 'In-Paper', blurred_in_paper: 'Blur In-Paper',
}

const SUBFOLDERS = ['bulgarian_only', 'chinese_only', 'english_only', 'german_only', 'multi_language']

interface ErrorItem {
  category: string
  sub_type: string
  severity: string
  text_span: string | null
  evidence: string
}

interface TransformData {
  description?: string
  descriptions_by_lang?: Record<string, string>
  [key: string]: unknown
}

interface FigureData {
  subfolder: string
  models: Record<string, Record<string, TransformData>>
}

function Badge({ label, variant }: { label: string; variant: 'success' | 'error' | 'tertiary' | 'neutral' }) {
  const colors = {
    success: { bg: 'var(--m3-primary-container)', fg: 'var(--m3-on-primary-container)' },
    error: { bg: 'var(--m3-error-container)', fg: 'var(--m3-on-error-container)' },
    tertiary: { bg: 'var(--m3-tertiary-container)', fg: 'var(--m3-on-tertiary-container)' },
    neutral: { bg: 'var(--m3-surface-container-highest)', fg: 'var(--m3-on-surface-variant)' },
  }
  const c = colors[variant]
  return <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: c.bg, color: c.fg }}>{label}</span>
}

export default function TransformEvaluation() {
  const [data, setData] = useState<Record<string, FigureData> | null>(null)
  const [selectedModel, setSelectedModel] = useState(ALL_MODELS[0])
  const [selectedTransform, setSelectedTransform] = useState(TRANSFORMS[0])
  const [selectedSubfolder, setSelectedSubfolder] = useState(SUBFOLDERS[2])
  const [selectedFigure, setSelectedFigure] = useState('')
  const [selectedJudge, setSelectedJudge] = useState('gpt-4o')
  const [expandedImage, setExpandedImage] = useState<{ src: string; label: string } | null>(null)
  const { isDark } = useTheme()

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/transform_evaluations.json`)
      .then(r => r.json())
      .then(d => setData(d))
      .catch(() => {})
  }, [])

  const figureKeys = useMemo(() => {
    if (!data) return []
    return Object.entries(data)
      .filter(([, v]) => v.subfolder === selectedSubfolder)
      .map(([k]) => k)
      .sort()
  }, [data, selectedSubfolder])

  useEffect(() => {
    if (figureKeys.length && !figureKeys.includes(selectedFigure)) {
      setSelectedFigure(figureKeys[0])
    }
  }, [figureKeys, selectedFigure])

  if (!data) return <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}><p style={{ color: 'var(--m3-on-surface-variant)' }}>Loading...</p></div>

  const figData = data[selectedFigure]
  const transformData = figData?.models?.[selectedModel]?.[selectedTransform]
  const score = transformData?.[`${selectedJudge}_score`] as number | undefined
  const errors = (transformData?.[`${selectedJudge}_errors`] || []) as ErrorItem[]
  const errorCount = (transformData?.[`${selectedJudge}_error_count`] || 0) as number
  const description = transformData?.description || ''
  const descsByLang = transformData?.descriptions_by_lang as Record<string, string> | undefined

  const getTransformImageUrl = (transform: string) => {
    if (transform === 'original') return `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original.png`
    if (transform === 'original_in_paper') return `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original_in_paper.jpeg`
    return `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/${transform}.png`
  }

  return (
    <div className="min-h-screen animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <header className="px-6 py-4 flex items-center gap-4" style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}>
        <Link to="/evaluation" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
          Back
        </Link>
        <h1 className="text-sm font-medium" style={{ color: 'var(--m3-on-surface)' }}>Transform MQM Evaluation</h1>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 border-r overflow-y-auto" style={{ borderColor: 'var(--m3-outline-variant)', height: 'calc(100vh - 57px)' }}>
          {/* Controls */}
          <div className="p-4 space-y-3" style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}>
            <div>
              <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)' }}>Model</label>
              <select value={selectedModel} onChange={e => setSelectedModel(e.target.value)} className="w-full text-xs p-1.5 rounded-lg" style={{ backgroundColor: 'var(--m3-surface-container)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)` }}>
                {ALL_MODELS.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            <div>
              <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)' }}>Judge</label>
              <div className="flex gap-1">
                {['gpt-4o', 'mistral-large-3'].map(j => (
                  <button key={j} onClick={() => setSelectedJudge(j)} className="text-[10px] font-medium px-2 py-1 rounded-full" style={{ backgroundColor: selectedJudge === j ? 'var(--m3-primary)' : 'var(--m3-surface-container-high)', color: selectedJudge === j ? 'var(--m3-on-primary)' : 'var(--m3-on-surface-variant)' }}>
                    {j === 'gpt-4o' ? 'GPT-4o' : 'Mistral'}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-[10px] font-medium uppercase mb-1 block" style={{ color: 'var(--m3-outline)' }}>Subfolder</label>
              <select value={selectedSubfolder} onChange={e => setSelectedSubfolder(e.target.value)} className="w-full text-xs p-1.5 rounded-lg" style={{ backgroundColor: 'var(--m3-surface-container)', color: 'var(--m3-on-surface)', border: `1px solid var(--m3-outline-variant)` }}>
                {SUBFOLDERS.map(s => <option key={s} value={s}>{s.replace('_only', '').replace('_', ' ')}</option>)}
              </select>
            </div>
          </div>

          {/* Figure list */}
          <div className="p-2">
            {figureKeys.map(fk => (
              <button key={fk} onClick={() => setSelectedFigure(fk)} className="w-full text-left px-3 py-2 rounded-lg text-xs mb-0.5" style={{ backgroundColor: selectedFigure === fk ? 'var(--m3-primary-container)' : 'transparent', color: selectedFigure === fk ? 'var(--m3-on-primary-container)' : 'var(--m3-on-surface-variant)' }}>
                {fk}
              </button>
            ))}
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 overflow-y-auto p-6" style={{ height: 'calc(100vh - 57px)' }}>
          {/* Transform toggle */}
          <div className="flex gap-1 mb-4 flex-wrap">
            {TRANSFORMS.map(t => (
              <button key={t} onClick={() => setSelectedTransform(t)} className="text-[10px] font-medium px-3 py-1.5 rounded-full" style={{ backgroundColor: selectedTransform === t ? 'var(--m3-primary)' : 'var(--m3-surface-container-high)', color: selectedTransform === t ? 'var(--m3-on-primary)' : 'var(--m3-on-surface-variant)' }}>
                {TRANSFORM_LABELS[t] || t}
              </button>
            ))}
          </div>

          {/* Image */}
          <div className="flex gap-4 mb-4">
            <div>
              <img
                src={getTransformImageUrl(selectedTransform)}
                alt={selectedTransform}
                className="rounded-lg max-h-64 w-auto cursor-pointer"
                onClick={() => setExpandedImage({ src: getTransformImageUrl(selectedTransform), label: `${selectedFigure} — ${TRANSFORM_LABELS[selectedTransform]}` })}
              />
              <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>{TRANSFORM_LABELS[selectedTransform]}</p>
            </div>
            {selectedTransform !== 'original' && (
              <div>
                <img
                  src={`${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original.png`}
                  alt="Original"
                  className="rounded-lg max-h-64 w-auto cursor-pointer"
                  onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${selectedSubfolder}/${selectedFigure}/original.png`, label: `${selectedFigure} — Original` })}
                />
                <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Original</p>
              </div>
            )}
          </div>

          {/* Score */}
          <div className="flex items-center gap-3 mb-4">
            <span className="text-lg font-medium tabular-nums" style={{ color: score != null && score >= 70 ? 'var(--m3-primary)' : score != null && score >= 50 ? 'var(--m3-on-surface)' : 'var(--m3-error)' }}>
              MQM: {score != null ? score.toFixed(1) : '—'}
            </span>
            <Badge label={`${errorCount} errors`} variant={errorCount <= 3 ? 'success' : errorCount <= 7 ? 'tertiary' : 'error'} />
            <Badge label={selectedModel} variant="neutral" />
            <Badge label={selectedJudge} variant="neutral" />
          </div>

          {/* Model Description */}
          {description && (
            <div className="rounded-lg p-4 mb-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
              <p className="text-[10px] font-medium uppercase mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Description</p>
              <p className="text-xs leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--m3-on-surface)' }}>{description}</p>
            </div>
          )}
          {descsByLang && Object.entries(descsByLang).map(([lang, desc]) => (
            <div key={lang} className="rounded-lg p-4 mb-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
              <p className="text-[10px] font-medium uppercase mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Model Description ({lang})</p>
              <p className="text-xs leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--m3-on-surface)' }}>{desc}</p>
            </div>
          ))}

          {/* No data */}
          {!description && !descsByLang && (
            <div className="rounded-lg p-6 text-center mb-4" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
              <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>No description available for {selectedModel} / {TRANSFORM_LABELS[selectedTransform]}</p>
            </div>
          )}

          {/* Errors */}
          {errors.length > 0 && (
            <div className="space-y-2">
              <p className="text-[10px] font-medium uppercase mb-2" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Errors ({errors.length})</p>
              {errors.map((err, i) => (
                <div key={i} className="rounded-lg p-3" style={{ backgroundColor: err.severity === 'Major' ? 'var(--m3-error-container)' : 'var(--m3-surface-container-high)', border: `1px solid var(--m3-outline-variant)` }}>
                  <div className="flex items-center gap-2 mb-1">
                    <Badge label={err.category} variant={err.category === 'Accuracy' ? 'error' : err.category === 'Completeness' ? 'tertiary' : 'neutral'} />
                    <Badge label={err.severity} variant={err.severity === 'Major' ? 'error' : 'neutral'} />
                    <span className="text-[10px] font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>{err.sub_type}</span>
                  </div>
                  {err.text_span && (
                    <p className="text-xs mb-1 px-2 py-1 rounded" style={{ backgroundColor: 'var(--m3-surface-container-highest)', color: 'var(--m3-error)', fontFamily: 'monospace' }}>"{err.text_span}"</p>
                  )}
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface-variant)' }}>{err.evidence}</p>
                </div>
              ))}
            </div>
          )}

          {score != null && errors.length === 0 && (
            <div className="rounded-lg p-4 text-center" style={{ backgroundColor: 'var(--m3-primary-container)', border: `1px solid var(--m3-outline-variant)` }}>
              <p className="text-xs" style={{ color: 'var(--m3-on-primary-container)' }}>No errors found — perfect score!</p>
            </div>
          )}
        </div>
      </div>

      {expandedImage && (
        <div className="fixed inset-0 z-50 flex items-center justify-center animate-fade-in" style={{ backgroundColor: isDark ? 'rgba(0,0,0,0.85)' : 'rgba(0,0,0,0.6)' }} onClick={() => setExpandedImage(null)}>
          <div className="relative max-w-5xl max-h-[90vh] p-4">
            <p className="text-xs font-medium mb-3 text-center" style={{ color: '#fff' }}>{expandedImage.label}</p>
            <img src={expandedImage.src} alt={expandedImage.label} className="max-w-full max-h-[80vh] rounded-xl" style={{ boxShadow: '0 25px 50px -12px rgba(0,0,0,0.5)' }} />
          </div>
        </div>
      )}
    </div>
  )
}
