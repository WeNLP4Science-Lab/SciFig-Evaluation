import { useState } from 'react'
import type { MQMError } from '../types'
import { CATEGORY_COLORS, CATEGORY_COLORS_LIGHT } from '../types'
import { useTheme } from '../ThemeContext'

interface Span {
  start: number
  end: number
  error: MQMError
  errorIdx: number
}

function buildSpans(text: string, errors: MQMError[]): Span[] {
  const spans: Span[] = []
  for (let i = 0; i < errors.length; i++) {
    const err = errors[i]
    if (!err.text_span) continue
    let idx = text.indexOf(err.text_span)
    if (idx === -1) {
      idx = text.toLowerCase().indexOf(err.text_span.toLowerCase())
    }
    if (idx === -1) {
      const normSpan = err.text_span.replace(/\s+/g, ' ').trim()
      const normText = text.replace(/\s+/g, ' ')
      const normIdx = normText.toLowerCase().indexOf(normSpan.toLowerCase())
      if (normIdx !== -1) {
        let origPos = 0, normPos = 0
        while (normPos < normIdx && origPos < text.length) {
          if (/\s/.test(text[origPos]) && origPos + 1 < text.length && /\s/.test(text[origPos + 1])) {
            origPos++
            continue
          }
          origPos++
          normPos++
        }
        idx = origPos
      }
    }
    if (idx !== -1) {
      spans.push({ start: idx, end: idx + err.text_span.length, error: err, errorIdx: i })
    }
  }
  spans.sort((a, b) => a.start - b.start || b.end - a.end)
  const filtered: Span[] = []
  let lastEnd = -1
  for (const s of spans) {
    if (s.start >= lastEnd) {
      filtered.push(s)
      lastEnd = s.end
    }
  }
  return filtered
}

interface Props {
  text: string
  errors: MQMError[]
  onErrorHover?: (idx: number | null) => void
  onErrorClick?: (idx: number) => void
  highlightedError?: number | null
  highlightedCategory?: string | null
}

export default function AnnotatedText({ text, errors, onErrorHover, onErrorClick, highlightedError, highlightedCategory }: Props) {
  const [activeSpan, setActiveSpan] = useState<number | null>(null)
  const { isDark } = useTheme()
  const spans = buildSpans(text, errors)
  const catColors = isDark ? CATEGORY_COLORS : CATEGORY_COLORS_LIGHT

  const parts: React.ReactElement[] = []
  let cursor = 0

  for (const span of spans) {
    if (span.start > cursor) {
      parts.push(
        <span key={`t-${cursor}`} style={{ color: 'var(--m3-on-surface)' }}>
          {text.slice(cursor, span.start)}
        </span>
      )
    }

    const cat = catColors[span.error.category] || { main: '#928f99', container: 'rgba(146,143,153,0.12)', onContainer: '#c8c5d0' }
    const isCategoryHighlighted = highlightedCategory != null && span.error.category === highlightedCategory
    const isActive = activeSpan === span.errorIdx || highlightedError === span.errorIdx || isCategoryHighlighted

    parts.push(
      <span
        key={`s-${span.start}`}
        className="cursor-pointer relative"
        style={{
          backgroundColor: isActive ? cat.container : 'transparent',
          borderBottom: `2px solid ${isActive ? cat.main : cat.main + '60'}`,
          padding: '1px 2px',
          borderRadius: 'var(--m3-shape-xs)',
          color: 'var(--m3-on-surface)',
          transition: 'all 200ms var(--m3-easing-standard)',
        }}
        onClick={() => onErrorClick?.(span.errorIdx)}
        onMouseEnter={() => {
          setActiveSpan(span.errorIdx)
          onErrorHover?.(span.errorIdx)
        }}
        onMouseLeave={() => {
          setActiveSpan(null)
          onErrorHover?.(null)
        }}
      >
        {text.slice(span.start, span.end)}
        {(activeSpan === span.errorIdx || highlightedError === span.errorIdx) && (
          <span
            className="error-tooltip absolute bottom-full left-0 mb-2 px-3 py-2 rounded-lg text-xs whitespace-nowrap z-10 max-w-xs"
            style={{
              backgroundColor: 'var(--m3-inverse-surface)',
              color: 'var(--m3-inverse-on-surface)',
              boxShadow: '0 4px 8px 3px rgba(0,0,0,0.15), 0 1px 3px 0 rgba(0,0,0,0.3)',
            }}
          >
            <span className="flex items-center gap-2">
              <span
                className="w-2 h-2 rounded-full flex-shrink-0"
                style={{ backgroundColor: cat.main }}
              />
              <span className="font-medium">{span.error.sub_type}</span>
              <span
                className="px-1.5 py-0.5 rounded text-[10px] font-medium"
                style={{
                  backgroundColor: span.error.severity === 'Major'
                    ? 'rgba(232,64,63,0.2)'
                    : 'rgba(232,180,63,0.2)',
                  color: span.error.severity === 'Major'
                    ? (isDark ? '#f2b8b5' : '#ba1a1a')
                    : (isDark ? '#ffd9b3' : '#b3590a'),
                }}
              >
                {span.error.severity}
              </span>
            </span>
          </span>
        )}
      </span>
    )
    cursor = span.end
  }

  if (cursor < text.length) {
    parts.push(
      <span key={`t-${cursor}`} style={{ color: 'var(--m3-on-surface)' }}>
        {text.slice(cursor)}
      </span>
    )
  }

  return (
    <div
      className="text-sm leading-7 whitespace-pre-wrap"
      style={{
        fontFamily: "'Inter', sans-serif",
        letterSpacing: '0.25px',
      }}
    >
      {parts}
    </div>
  )
}
