import { useRef, useState } from 'react'

interface FigureSidebarProps {
  figureKeys: string[]
  selectedKey: string
  onSelect: (key: string) => void
}

function extractNumber(key: string): string {
  const match = key.match(/(\d+)$/)
  return match ? match[1] : key.slice(-3)
}

export default function FigureSidebar({ figureKeys, selectedKey, onSelect }: FigureSidebarProps) {
  const [isHovered, setIsHovered] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  return (
    <div
      className="flex-shrink-0 overflow-hidden"
      style={{
        width: isHovered ? 220 : 56,
        backgroundColor: 'var(--m3-surface-container-low)',
        borderRight: '1px solid var(--m3-outline-variant)',
        transition: 'width 250ms var(--m3-easing-standard)',
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        ref={scrollRef}
        className="h-full overflow-y-auto py-2"
        style={{ scrollbarWidth: 'thin' }}
      >
        {figureKeys.map((key) => {
          const isSelected = key === selectedKey
          const num = extractNumber(key)
          return (
            <button
              key={key}
              onClick={() => onSelect(key)}
              className="w-full flex items-center gap-3 px-2.5 py-1"
              style={{
                transition: 'background-color 200ms var(--m3-easing-standard)',
                minHeight: 44,
              }}
              onMouseEnter={(e) => {
                if (!isSelected) {
                  e.currentTarget.style.backgroundColor = 'color-mix(in srgb, var(--m3-on-surface) 8%, transparent)'
                }
              }}
              onMouseLeave={(e) => {
                if (!isSelected) {
                  e.currentTarget.style.backgroundColor = 'transparent'
                }
              }}
            >
              <div
                className="flex-shrink-0 flex items-center justify-center rounded-full"
                style={{
                  width: 36,
                  height: 36,
                  backgroundColor: isSelected
                    ? 'var(--m3-primary-container)'
                    : 'var(--m3-surface-container-high)',
                  color: isSelected
                    ? 'var(--m3-on-primary-container)'
                    : 'var(--m3-on-surface)',
                  fontSize: 12,
                  fontWeight: 500,
                  letterSpacing: '0.5px',
                  transition: 'all 200ms var(--m3-easing-standard)',
                }}
              >
                {num}
              </div>
              <span
                className="truncate text-left"
                style={{
                  fontSize: 12,
                  fontWeight: 500,
                  color: isSelected
                    ? 'var(--m3-on-primary-container)'
                    : 'var(--m3-on-surface-variant)',
                  letterSpacing: '0.1px',
                  opacity: isHovered ? 1 : 0,
                  transition: 'opacity 250ms var(--m3-easing-standard)',
                  whiteSpace: 'nowrap',
                }}
              >
                {key}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
