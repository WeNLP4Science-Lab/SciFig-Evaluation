import { useState, useEffect, useMemo, useCallback } from 'react'

/* ── Types ── */

interface FigureEntry {
  id: string
  figure_type: string
  caption: string
  paper_title: string
  arxiv_id: string
  annotation_count: number
  annotations: string[]
}

type FilterType = 'All' | 'Bar Chart' | 'Line Plot' | 'Pie Chart'

const FILTERS: FilterType[] = ['All', 'Bar Chart', 'Line Plot', 'Pie Chart']

const TYPE_DOT: Record<string, string> = {
  'Bar Chart': '#f59e0b',
  'Line Plot': '#3b82f6',
  'Pie Chart': '#8b5cf6',
}
const TYPE_BG: Record<string, string> = {
  'Bar Chart': 'rgba(245,158,11,0.1)',
  'Line Plot': 'rgba(59,130,246,0.1)',
  'Pie Chart': 'rgba(139,92,246,0.1)',
}
const TYPE_SHORT: Record<string, string> = {
  'Bar Chart': 'Bar',
  'Line Plot': 'Line',
  'Pie Chart': 'Pie',
}

/* ── Shared inline style constants ── */

const c = {
  bg: '#09090b',
  surface: '#131316',
  surfaceHover: '#1c1c21',
  surfaceActive: '#232329',
  surfaceRaised: '#18181b',
  border: 'rgba(255,255,255,0.06)',
  borderStrong: 'rgba(255,255,255,0.1)',
  fg: '#fafafa',
  muted: '#a1a1aa',
  dim: '#52525b',
  accent: '#3b82f6',
}

/* ── Main Component ── */

import { figureInRange, isAnnotationMode, getSavedAuth } from '../auth'

export default function Dataset({ onSelectFigure }: { onSelectFigure: (id: string) => void }) {
  const [data, setData] = useState<FigureEntry[]>([])
  const [filter, setFilter] = useState<FilterType>('All')
  const [search, setSearch] = useState('')
  const [loaded, setLoaded] = useState<Set<string>>(new Set())

  useEffect(() => {
    fetch('/manifest.json').then(r => r.json()).then(setData)
  }, [])

  const annotateMode = isAnnotationMode()
  const auth = getSavedAuth()

  // Base dataset: filtered by annotator range in annotation mode
  const baseData = useMemo(() => {
    if (annotateMode && auth) {
      return data.filter(d => figureInRange(d.id, auth.name))
    }
    return data
  }, [data, annotateMode, auth])

  const filtered = useMemo(() => {
    let items = baseData
    if (filter !== 'All') items = items.filter(d => d.figure_type === filter)
    if (search.trim()) {
      const q = search.toLowerCase()
      items = items.filter(d =>
        d.id.includes(q) ||
        d.caption.toLowerCase().includes(q) ||
        d.paper_title.toLowerCase().includes(q)
      )
    }
    return items
  }, [baseData, filter, search])

  const counts = useMemo(() => {
    const r: Record<string, number> = { 'Bar Chart': 0, 'Line Plot': 0, 'Pie Chart': 0 }
    baseData.forEach(d => { if (d.figure_type in r) r[d.figure_type]++ })
    return r
  }, [baseData])

  const papers = useMemo(() => new Set(baseData.map(d => d.arxiv_id)).size, [baseData])
  const totalAnns = useMemo(() => baseData.reduce((s, d) => s + d.annotation_count, 0), [baseData])

  const markLoaded = useCallback((id: string) => {
    setLoaded(prev => new Set(prev).add(id))
  }, [])

  return (
    <div style={{ minHeight: '100vh' }}>
      {/* ── Header ── */}
      <header style={{ borderBottom: `1px solid ${c.border}` }}>
        <div className="page-container" style={{ paddingTop: 48, paddingBottom: 36 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <span style={{
              fontSize: 11, fontWeight: 600, letterSpacing: '0.08em',
              textTransform: 'uppercase', color: c.accent,
            }}>
              Dataset Explorer
            </span>
            <span style={{ width: 1, height: 12, background: c.borderStrong }} />
            <span style={{ fontSize: 11, color: c.dim }}>v1.0</span>
          </div>
          <h1 style={{
            fontSize: 28, fontWeight: 600, letterSpacing: '-0.02em',
            color: c.fg, lineHeight: 1.2, margin: 0,
          }}>
            SciFig-Eval Benchmark
          </h1>
          <p style={{
            fontSize: 14, color: c.muted, marginTop: 10,
            maxWidth: 540, lineHeight: 1.6,
          }}>
            250 scientific figures from peer-reviewed papers, each annotated with
            structured natural-language descriptions for evaluating vision-language models.
          </p>
        </div>
      </header>

      {/* ── Stats ── */}
      <div style={{ borderBottom: `1px solid ${c.border}` }}>
        <div className="page-container" style={{ paddingTop: 20, paddingBottom: 20 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12 }}>
            <Stat label="Figures" value={baseData.length} />
            <Stat label="Papers" value={papers} />
            <Stat label="Annotations" value={totalAnns} />
            <Stat label="Chart Types" value={3} />
            <Stat label="Annotators" value={4} />
          </div>
        </div>
      </div>

      {/* ── Toolbar ── */}
      <div style={{
        borderBottom: `1px solid ${c.border}`,
        position: 'sticky', top: 0, zIndex: 20,
        background: 'rgba(9,9,11,0.92)', backdropFilter: 'blur(12px)',
      }}>
        <div className="page-container" style={{
          height: 44, display: 'flex', alignItems: 'center', gap: 16,
        }}>
          {/* Filters */}
          <div style={{ display: 'flex', gap: 4 }}>
            {FILTERS.map(f => {
              const isActive = filter === f
              const count = f === 'All' ? baseData.length : counts[f]
              const dot = f !== 'All' ? TYPE_DOT[f] : undefined
              return (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    height: 28, padding: '0 10px', borderRadius: 6,
                    fontSize: 12, fontFamily: 'inherit', cursor: 'pointer',
                    border: isActive ? `1px solid ${c.borderStrong}` : '1px solid transparent',
                    background: isActive ? c.surfaceActive : 'transparent',
                    color: isActive ? c.fg : c.muted,
                    fontWeight: isActive ? 500 : 400,
                    transition: 'all 0.15s ease',
                  }}
                  onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = c.surfaceHover }}
                  onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = 'transparent' }}
                >
                  {dot && <span style={{ width: 6, height: 6, borderRadius: '50%', background: dot }} />}
                  <span>{f === 'All' ? 'All' : f}</span>
                  <span style={{ fontSize: 10, color: isActive ? c.muted : c.dim }}>{count}</span>
                </button>
              )
            })}
          </div>

          <div style={{ flex: 1 }} />

          {/* Search */}
          <div style={{ position: 'relative' }}>
            <svg style={{
              position: 'absolute', left: 9, top: '50%', transform: 'translateY(-50%)',
              width: 13, height: 13, pointerEvents: 'none',
            }} viewBox="0 0 16 16" fill="none" stroke={c.dim} strokeWidth="1.5" strokeLinecap="round">
              <circle cx="6.5" cy="6.5" r="4" /><path d="M10 10l3.5 3.5" />
            </svg>
            <input
              type="text"
              placeholder="Search figures..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{
                width: 220, height: 28, paddingLeft: 30, paddingRight: 10,
                fontSize: 12, borderRadius: 6, fontFamily: 'inherit',
                background: c.surface, border: `1px solid ${c.border}`,
                color: c.fg, outline: 'none',
              }}
              onFocus={e => e.currentTarget.style.borderColor = 'rgba(59,130,246,0.4)'}
              onBlur={e => e.currentTarget.style.borderColor = c.border}
            />
          </div>

          <span style={{
            fontSize: 11, color: c.dim, minWidth: 64, textAlign: 'right',
            fontVariantNumeric: 'tabular-nums',
          }}>
            {filtered.length} result{filtered.length !== 1 ? 's' : ''}
          </span>
        </div>
      </div>

      {/* ── Distribution Bar ── */}
      {baseData.length > 0 && (
        <div className="page-container" style={{ paddingTop: 24, paddingBottom: 4 }}>
          <div style={{
            display: 'flex', height: 5, borderRadius: 8, overflow: 'hidden',
            background: c.surface, border: `1px solid ${c.border}`,
          }}>
            {(['Bar Chart', 'Line Plot', 'Pie Chart'] as const).map(t => (
              <div key={t} style={{
                width: `${(counts[t] / baseData.length) * 100}%`,
                background: TYPE_DOT[t],
                opacity: filter === 'All' || filter === t ? 0.75 : 0.12,
                transition: 'opacity 0.3s ease',
              }} />
            ))}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginTop: 10 }}>
            {(['Bar Chart', 'Line Plot', 'Pie Chart'] as const).map(t => (
              <div key={t} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ width: 7, height: 7, borderRadius: '50%', background: TYPE_DOT[t] }} />
                <span style={{ fontSize: 11, color: c.dim }}>
                  {t}{' '}
                  <span style={{ color: c.muted, fontVariantNumeric: 'tabular-nums' }}>
                    {Math.round((counts[t] / baseData.length) * 100)}%
                  </span>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Grid ── */}
      <div className="page-container" style={{ paddingTop: 20, paddingBottom: 48 }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 12,
        }}>
          {filtered.map((item, i) => (
            <Card
              key={item.id}
              item={item}
              index={i}
              isLoaded={loaded.has(item.id)}
              onLoad={() => markLoaded(item.id)}
              onClick={() => onSelectFigure(item.id)}
            />
          ))}
        </div>

        {filtered.length === 0 && baseData.length > 0 && (
          <div style={{ textAlign: 'center', padding: '80px 0' }}>
            <p style={{ fontSize: 13, color: c.muted }}>No figures match your search</p>
            <button
              onClick={() => { setSearch(''); setFilter('All') }}
              style={{
                marginTop: 8, fontSize: 12, color: c.accent,
                background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'inherit',
              }}
            >
              Clear filters
            </button>
          </div>
        )}
      </div>

    </div>
  )
}

/* ── Stat Card ── */

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div style={{
      borderRadius: 8, border: `1px solid ${c.border}`, background: c.surface,
      padding: '14px 16px',
    }}>
      <p style={{
        fontSize: 10, fontWeight: 600, color: c.dim,
        textTransform: 'uppercase', letterSpacing: '0.06em',
        lineHeight: 1, margin: 0,
      }}>
        {label}
      </p>
      <p style={{
        fontSize: 22, fontWeight: 600, color: c.fg,
        marginTop: 8, lineHeight: 1, margin: '8px 0 0',
        fontVariantNumeric: 'tabular-nums',
      }}>
        {value.toLocaleString()}
      </p>
    </div>
  )
}

/* ── Figure Card ── */

function Card({ item, index, isLoaded, onLoad, onClick }: {
  item: FigureEntry; index: number; isLoaded: boolean
  onLoad: () => void; onClick: () => void
}) {
  const [hovered, setHovered] = useState(false)
  const dot = TYPE_DOT[item.figure_type] || '#888'
  const bg = TYPE_BG[item.figure_type] || 'rgba(136,136,136,0.1)'

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        borderRadius: 10,
        border: `1px solid ${hovered ? c.borderStrong : c.border}`,
        background: c.surface,
        overflow: 'hidden',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        animation: `fadeIn 0.35s ease-out ${Math.min(index * 20, 200)}ms both`,
        transition: 'border-color 0.2s ease',
      }}
    >
      {/* Thumbnail */}
      <div style={{
        position: 'relative', aspectRatio: '4/3', background: c.bg, overflow: 'hidden',
      }}>
        {!isLoaded && (
          <div style={{
            position: 'absolute', inset: 0,
            background: `linear-gradient(90deg, ${c.surface} 25%, ${c.surfaceHover} 50%, ${c.surface} 75%)`,
            backgroundSize: '200% 100%',
            animation: 'shimmer 1.5s ease-in-out infinite',
          }} />
        )}
        <img
          src={`/figures/${item.id}.png`}
          alt={item.caption || item.id}
          loading="lazy"
          onLoad={onLoad}
          style={{
            width: '100%', height: '100%', objectFit: 'contain', padding: 12,
            opacity: isLoaded ? 1 : 0, transition: 'opacity 0.3s ease',
          }}
        />
        {/* Hover overlay */}
        <div style={{
          position: 'absolute', inset: 0,
          background: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(2px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          opacity: hovered ? 1 : 0, transition: 'opacity 0.2s ease',
        }}>
          <span style={{
            fontSize: 11, fontWeight: 500, color: 'rgba(255,255,255,0.9)',
            padding: '6px 14px', borderRadius: 6,
            background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.1)',
          }}>
            View details
          </span>
        </div>
      </div>

      {/* Meta */}
      <div style={{
        padding: '10px 12px', borderTop: `1px solid ${c.border}`,
        flex: 1, display: 'flex', flexDirection: 'column',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
          <span style={{
            fontSize: 11, fontFamily: 'JetBrains Mono, monospace', fontWeight: 500, color: c.muted,
          }}>
            {item.id}
          </span>
          <span style={{
            fontSize: 9, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em',
            padding: '3px 7px', borderRadius: 4, color: dot, background: bg,
            lineHeight: 1, flexShrink: 0,
          }}>
            {TYPE_SHORT[item.figure_type] || item.figure_type}
          </span>
        </div>
        {item.caption && (
          <p style={{
            fontSize: 11, color: c.dim, lineHeight: 1.5,
            marginTop: 6, overflow: 'hidden',
            display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
          }}>
            {item.caption}
          </p>
        )}
      </div>
    </div>
  )
}

