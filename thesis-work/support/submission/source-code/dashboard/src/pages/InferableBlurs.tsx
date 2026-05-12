import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import { FIGURES_BASE_URL } from '../config'

interface InferableItem {
  figure_key: string
  subfolder: string
  blurred_element: string
  reasoning: string
}

interface InferableData {
  fully_inferable: InferableItem[]
  partially_inferable: InferableItem[]
}

function Badge({ label, variant }: { label: string; variant: 'success' | 'tertiary' | 'neutral' }) {
  const bg = variant === 'success' ? 'var(--m3-primary-container)' : variant === 'tertiary' ? 'var(--m3-tertiary-container)' : 'var(--m3-surface-container-highest)'
  const fg = variant === 'success' ? 'var(--m3-on-primary-container)' : variant === 'tertiary' ? 'var(--m3-on-tertiary-container)' : 'var(--m3-on-surface-variant)'
  return <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: bg, color: fg }}>{label}</span>
}

export default function InferableBlurs() {
  const [data, setData] = useState<InferableData | null>(null)
  const [expandedImage, setExpandedImage] = useState<{ src: string; label: string } | null>(null)
  const { isDark } = useTheme()

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/inferable_elements.json`)
      .then(r => r.json())
      .then(d => setData(d as InferableData))
      .catch(() => {})
  }, [])

  if (!data) return <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}><p style={{ color: 'var(--m3-on-surface-variant)' }}>Loading...</p></div>

  const renderCard = (item: InferableItem, type: 'full' | 'partial') => (
    <div key={`${item.figure_key}-${type}`} className="rounded-xl overflow-hidden" style={{ backgroundColor: 'var(--m3-surface-container)', border: `1px solid var(--m3-outline-variant)` }}>
      <div className="flex gap-4 p-4">
        <div className="flex-shrink-0">
          <img
            src={`${FIGURES_BASE_URL}/adversarial/${item.subfolder}/${item.figure_key}/selective_blur.png`}
            alt="Selective blur"
            className="rounded-lg w-48 h-auto cursor-pointer"
            onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${item.subfolder}/${item.figure_key}/selective_blur.png`, label: `${item.figure_key} — Selective Blur` })}
          />
          <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Selective Blur</p>
        </div>
        <div className="flex-shrink-0">
          <img
            src={`${FIGURES_BASE_URL}/adversarial/${item.subfolder}/${item.figure_key}/original.png`}
            alt="Original"
            className="rounded-lg w-48 h-auto cursor-pointer"
            onClick={() => setExpandedImage({ src: `${FIGURES_BASE_URL}/adversarial/${item.subfolder}/${item.figure_key}/original.png`, label: `${item.figure_key} — Original` })}
          />
          <p className="text-[10px] mt-1 text-center" style={{ color: 'var(--m3-outline)' }}>Original</p>
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono font-medium" style={{ color: 'var(--m3-on-surface)' }}>{item.figure_key}</span>
            <Badge label={item.subfolder.replace('_only', '').replace('_', ' ')} variant="neutral" />
            <Badge label={type === 'full' ? 'FULLY INFERABLE' : 'PARTIALLY INFERABLE'} variant={type === 'full' ? 'success' : 'tertiary'} />
          </div>
          <div className="rounded-lg p-2 mb-2" style={{ backgroundColor: 'var(--m3-error-container)' }}>
            <p className="text-[10px] font-medium uppercase mb-0.5" style={{ color: 'var(--m3-on-error-container)', letterSpacing: '0.5px' }}>Blurred Element</p>
            <p className="text-xs" style={{ color: 'var(--m3-on-error-container)' }}>{item.blurred_element}</p>
          </div>
          <div className="rounded-lg p-2" style={{ backgroundColor: 'var(--m3-surface-container-high)' }}>
            <p className="text-[10px] font-medium uppercase mb-0.5" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>Why Inferable</p>
            <p className="text-xs leading-relaxed" style={{ color: 'var(--m3-on-surface)' }}>{item.reasoning}</p>
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <header className="px-6 py-4 flex items-center" style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}>
        <Link to="/dataset" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
          Back
        </Link>
        <h1 className="ml-4 text-sm font-medium" style={{ color: 'var(--m3-on-surface)' }}>Inferable Blurs — Inductance Candidates</h1>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-lg font-normal mb-2" style={{ color: 'var(--m3-on-surface)' }}>Fully Inferable ({data.fully_inferable.length})</h2>
          <p className="text-xs mb-4" style={{ color: 'var(--m3-on-surface-variant)' }}>Blurred elements that can be logically deduced from visible context alone</p>
          <div className="space-y-4">
            {data.fully_inferable.map(item => renderCard(item, 'full'))}
          </div>
        </div>

        <div>
          <h2 className="text-lg font-normal mb-2" style={{ color: 'var(--m3-on-surface)' }}>Partially Inferable ({data.partially_inferable.length})</h2>
          <p className="text-xs mb-4" style={{ color: 'var(--m3-on-surface-variant)' }}>Blurred elements where some aspects can be inferred but full identification requires domain knowledge</p>
          <div className="space-y-4">
            {data.partially_inferable.map(item => renderCard(item, 'partial'))}
          </div>
        </div>
      </main>

      {expandedImage && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center animate-fade-in"
          style={{ backgroundColor: isDark ? 'rgba(0,0,0,0.85)' : 'rgba(0,0,0,0.6)' }}
          onClick={() => setExpandedImage(null)}
        >
          <div className="relative max-w-5xl max-h-[90vh] p-4">
            <p className="text-xs font-medium mb-3 text-center" style={{ color: '#fff' }}>{expandedImage.label}</p>
            <img src={expandedImage.src} alt={expandedImage.label} className="max-w-full max-h-[80vh] rounded-xl" style={{ boxShadow: '0 25px 50px -12px rgba(0,0,0,0.5)' }} />
          </div>
        </div>
      )}
    </div>
  )
}
