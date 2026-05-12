import { useState, useEffect, useRef } from 'react'
import type { MQMError } from '../types'
import { CATEGORY_COLORS, CATEGORY_COLORS_LIGHT, SEVERITY_COLORS, SEVERITY_COLORS_LIGHT } from '../types'
import { useTheme } from '../ThemeContext'

interface Props {
  errors: MQMError[]
  mqmScore: number
  errorCount: number
  onErrorHover?: (idx: number | null) => void
  highlightedError?: number | null
  onCategoryExpand?: (category: string | null) => void
  focusedError?: number | null
}

function ScoreGauge({ score, isDark }: { score: number; isDark: boolean }) {
  const radius = 50
  const strokeWidth = 5
  const circumference = 2 * Math.PI * radius
  const progress = Math.max(0, Math.min(100, score)) / 100
  const offset = circumference * (1 - progress)

  const scoreColor =
    score >= 80 ? (isDark ? '#4caf7c' : '#1a6b3e') :
    score >= 60 ? (isDark ? '#e8b43f' : '#8a6b00') :
    (isDark ? '#e8403f' : '#ba1a1a')

  return (
    <div className="relative flex items-center justify-center">
      <svg width="120" height="120" viewBox="0 0 120 120" className="transform -rotate-90">
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke="var(--m3-outline-variant)"
          strokeWidth={strokeWidth}
          opacity={0.4}
        />
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke={scoreColor}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="score-ring"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className="text-3xl font-normal tabular-nums"
          style={{ color: scoreColor, letterSpacing: '-0.25px' }}
        >
          {score}
        </span>
        <span
          className="text-[11px] font-medium mt-0.5"
          style={{
            color: 'var(--m3-outline)',
            letterSpacing: '0.5px',
          }}
        >
          MQM
        </span>
      </div>
    </div>
  )
}

function ExpandChevron({ expanded }: { expanded: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="var(--m3-outline)"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{
        transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
        transition: 'transform 200ms var(--m3-easing-standard)',
        flexShrink: 0,
      }}
    >
      <polyline points="6 9 12 15 18 9" />
    </svg>
  )
}

export default function ErrorPanel({ errors, mqmScore, errorCount, onErrorHover, highlightedError, onCategoryExpand, focusedError }: Props) {
  const [expandedCat, setExpandedCat] = useState<string | null>(null)
  const errorRefs = useRef<Record<string, HTMLDivElement | null>>({})

  const toggleCategory = (cat: string) => {
    const next = expandedCat === cat ? null : cat
    setExpandedCat(next)
    onCategoryExpand?.(next)
  }
  const [expandedErrors, setExpandedErrors] = useState<Set<string>>(new Set())
  const { isDark } = useTheme()

  const catColors = isDark ? CATEGORY_COLORS : CATEGORY_COLORS_LIGHT
  const sevColors = isDark ? SEVERITY_COLORS : SEVERITY_COLORS_LIGHT

  const toggleErrorExpand = (key: string) => {
    setExpandedErrors(prev => {
      const next = new Set(prev)
      if (next.has(key)) {
        next.delete(key)
      } else {
        next.add(key)
      }
      return next
    })
  }

  // Group errors by category
  const grouped: Record<string, { errors: MQMError[]; indices: number[] }> = {}
  errors.forEach((err, i) => {
    if (!grouped[err.category]) {
      grouped[err.category] = { errors: [], indices: [] }
    }
    grouped[err.category].errors.push(err)
    grouped[err.category].indices.push(i)
  })

  // Use all errors grouped by category (including NON_ANNOTATABLE in their category)
  const groupedFiltered = grouped

  // When an error is clicked in AnnotatedText, expand its category + details + scroll
  useEffect(() => {
    if (focusedError == null) return
    const err = errors[focusedError]
    if (!err) return

    const cat = err.category
    // Find the index within the category group
    const group = grouped[cat]
    if (!group) return
    const idxInGroup = group.indices.indexOf(focusedError)
    if (idxInGroup === -1) return

    const errorKey = `cat-${cat}-${idxInGroup}`

    // Expand category
    setExpandedCat(cat)
    onCategoryExpand?.(cat)

    // Expand the specific error
    setExpandedErrors(prev => {
      const next = new Set(prev)
      next.add(errorKey)
      return next
    })

    // Scroll within the closest scrollable parent only (avoid scrollIntoView which scrolls all ancestors)
    requestAnimationFrame(() => {
      const el = errorRefs.current[errorKey]
      if (!el) return
      let scrollParent: HTMLElement | null = el.parentElement
      while (scrollParent) {
        const style = getComputedStyle(scrollParent)
        if (style.overflowY === 'auto' || style.overflowY === 'scroll') break
        scrollParent = scrollParent.parentElement
      }
      if (scrollParent) {
        const elRect = el.getBoundingClientRect()
        const parentRect = scrollParent.getBoundingClientRect()
        const offset = elRect.top - parentRect.top - parentRect.height / 2 + elRect.height / 2
        scrollParent.scrollBy({ top: offset, behavior: 'smooth' })
      }
    })
  }, [focusedError])

  return (
    <div className="space-y-6 animate-fade-in min-w-0">
      {/* Score + Summary */}
      <div className="flex items-center gap-5">
        <ScoreGauge score={mqmScore} isDark={isDark} />
        <div className="flex-1">
          <div className="flex items-baseline gap-2 mb-3">
            <span
              className="text-2xl font-normal tabular-nums"
              style={{ color: 'var(--m3-on-surface)', letterSpacing: '-0.25px' }}
            >
              {errorCount}
            </span>
            <span
              className="text-sm font-medium"
              style={{ color: 'var(--m3-on-surface-variant)', letterSpacing: '0.25px' }}
            >
              {errorCount === 1 ? 'error' : 'errors'} found
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {Object.entries(grouped).map(([cat, { errors: catErrors }]) => {
              const c = catColors[cat] || { main: '#928f99', container: 'rgba(146,143,153,0.12)', onContainer: '#c8c5d0' }
              return (
                <span
                  key={cat}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium"
                  style={{
                    backgroundColor: c.container,
                    color: c.main,
                    letterSpacing: '0.5px',
                  }}
                >
                  {catErrors.length} {cat}
                </span>
              )
            })}
          </div>
        </div>
      </div>

      {/* Category Chips - M3 Filter Chips (only show categories that have non-NON_ANNOTATABLE errors) */}
      <div className="flex flex-wrap gap-2">
        {Object.entries(groupedFiltered).map(([cat, { errors: catErrors }]) => {
          const c = catColors[cat] || { main: '#928f99', container: 'rgba(146,143,153,0.12)', onContainer: '#c8c5d0' }
          const isExpanded = expandedCat === cat
          return (
            <button
              key={cat}
              onClick={() => toggleCategory(cat)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium cursor-pointer"
              style={{
                backgroundColor: isExpanded
                  ? c.container
                  : 'var(--m3-surface-container-high)',
                border: `1px solid ${isExpanded ? c.main + '40' : 'var(--m3-outline-variant)'}`,
                color: isExpanded ? c.main : 'var(--m3-on-surface-variant)',
                transition: 'all 200ms var(--m3-easing-standard)',
                letterSpacing: '0.1px',
              }}
            >
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: c.main }}
              />
              {cat}
              <span
                className="px-1.5 py-0.5 rounded-full text-[10px] font-medium tabular-nums"
                style={{
                  backgroundColor: isExpanded
                    ? c.main + '20'
                    : 'var(--m3-surface-container-highest)',
                  color: isExpanded ? c.main : 'var(--m3-on-surface-variant)',
                }}
              >
                {catErrors.length}
              </span>
            </button>
          )
        })}
      </div>

      {/* Expanded Category Errors - M3 Filled Card (filtered: no NON_ANNOTATABLE) */}
      {expandedCat && groupedFiltered[expandedCat] && (
        <div
          className="rounded-xl overflow-hidden animate-scale-in"
          style={{
            backgroundColor: 'var(--m3-surface-container)',
            border: `1px solid var(--m3-outline-variant)`,
          }}
        >
          <div
            className="px-4 py-3 text-xs font-medium tracking-wide flex items-center gap-2"
            style={{
              color: (catColors[expandedCat] || { main: '#928f99' }).main,
              borderBottom: `1px solid var(--m3-outline-variant)`,
              letterSpacing: '0.5px',
            }}
          >
            <span
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: (catColors[expandedCat] || { main: '#928f99' }).main }}
            />
            {expandedCat}
          </div>
          <div>
            {groupedFiltered[expandedCat].errors.map((err, i) => {
              const globalIdx = groupedFiltered[expandedCat].indices[i]
              const isHighlighted = highlightedError === globalIdx
              const sev = sevColors[err.severity] || { bg: 'rgba(128,128,128,0.12)', text: '#999', border: 'rgba(128,128,128,0.2)' }
              const errorKey = `cat-${expandedCat}-${i}`
              const isErrorExpanded = expandedErrors.has(errorKey)
              return (
                <div
                  key={i}
                  ref={el => { errorRefs.current[errorKey] = el }}
                  className="px-4 py-3 min-w-0 overflow-hidden"
                  style={{
                    backgroundColor: isHighlighted
                      ? 'color-mix(in srgb, var(--m3-primary) 8%, transparent)'
                      : 'transparent',
                    borderBottom: i < groupedFiltered[expandedCat].errors.length - 1
                      ? `1px solid var(--m3-outline-variant)`
                      : 'none',
                    transition: 'background-color 200ms var(--m3-easing-standard)',
                  }}
                  onMouseEnter={() => onErrorHover?.(globalIdx)}
                  onMouseLeave={() => onErrorHover?.(null)}
                >
                  <div className="flex items-center gap-2 mb-1.5">
                    <span
                      className="font-medium text-sm"
                      style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}
                    >
                      {err.sub_type}
                    </span>
                    <span
                      className="px-2 py-0.5 rounded-full text-[10px] font-medium"
                      style={{
                        backgroundColor: sev.bg,
                        color: sev.text,
                        border: `1px solid ${sev.border}`,
                        letterSpacing: '0.5px',
                      }}
                    >
                      {err.severity}
                    </span>
                    <span
                      className="text-xs font-medium tabular-nums ml-auto"
                      style={{ color: 'var(--m3-outline)' }}
                    >
                      -{err.weight}
                    </span>
                    <button
                      onClick={() => toggleErrorExpand(errorKey)}
                      className="p-0.5 rounded m3-state-hover"
                      style={{ lineHeight: 0 }}
                    >
                      <ExpandChevron expanded={isErrorExpanded} />
                    </button>
                  </div>
                  <p
                    className="text-xs leading-relaxed"
                    style={{
                      color: 'var(--m3-on-surface-variant)',
                      letterSpacing: '0.4px',
                      display: isErrorExpanded ? 'block' : '-webkit-box',
                      WebkitLineClamp: isErrorExpanded ? undefined : 2,
                      WebkitBoxOrient: isErrorExpanded ? undefined : 'vertical',
                      overflow: 'hidden',
                      wordBreak: 'break-word',
                      overflowWrap: 'anywhere',
                    }}
                  >
                    {err.evidence}
                  </p>
                  {/* Expanded details */}
                  <div
                    style={{
                      maxHeight: isErrorExpanded ? 200 : 0,
                      overflow: 'hidden',
                      overflowX: 'hidden',
                      transition: 'max-height 200ms var(--m3-easing-standard)',
                    }}
                  >
                    {err.text_span && (
                      <div className="mt-2">
                        <span
                          className="text-[10px] font-medium uppercase"
                          style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
                        >
                          Text Span
                        </span>
                        <p
                          className="text-xs font-mono mt-0.5"
                          style={{
                            color: 'var(--m3-on-surface-variant)',
                            whiteSpace: 'pre-wrap',
                            wordBreak: 'break-word',
                          }}
                        >
                          &quot;{err.text_span}&quot;
                        </p>
                      </div>
                    )}
                    <div className="mt-2">
                      <span
                        className="text-[10px] font-medium uppercase"
                        style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}
                      >
                        Weight Contribution
                      </span>
                      <p
                        className="text-xs font-medium tabular-nums mt-0.5"
                        style={{ color: 'var(--m3-on-surface-variant)' }}
                      >
                        -{err.weight} ({err.severity})
                      </p>
                    </div>
                  </div>
                  {/* Show truncated text_span when collapsed */}
                  {!isErrorExpanded && err.text_span && (
                    <p
                      className="text-xs mt-1.5 font-mono"
                      style={{
                        color: 'var(--m3-outline)',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        maxWidth: '100%',
                      }}
                    >
                      &quot;{err.text_span}&quot;
                    </p>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}

    </div>
  )
}
