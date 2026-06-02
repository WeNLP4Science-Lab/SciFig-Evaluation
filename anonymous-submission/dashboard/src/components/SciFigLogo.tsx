/**
 * SciFig-Eval conceptual mark.
 *
 * Three horizontal bars suggesting a bar chart — the middle (longest) bar
 * has a gaussian-blurred segment on its right half, encoding the paper's
 * core hook: selectively blurred chart elements.
 *
 * Uses currentColor so it inherits from its container's text colour.
 * Set a unique `id` if rendering multiple instances on the same page
 * (the SVG filter is namespaced by it).
 */
export default function SciFigLogo({ size = 24, id = 'scifig-logo' }: {
  size?: number
  id?: string
}) {
  const filterId = `${id}-blur`
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      style={{ display: 'inline-block', verticalAlign: 'middle', flexShrink: 0 }}
      aria-label="SciFig-Eval"
    >
      <defs>
        <filter id={filterId} x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="0.8" />
        </filter>
      </defs>

      {/* Top bar */}
      <rect x="0" y="4"  width="13" height="3.4" rx="0.6" fill="currentColor" opacity="0.78" />

      {/* Middle (longest) bar — clear left half */}
      <rect x="0" y="10" width="11" height="3.4" rx="0.6" fill="currentColor" />

      {/* Middle bar — blurred right half (encodes selective blur) */}
      <g filter={`url(#${filterId})`}>
        <rect x="10.5" y="9.6" width="10" height="4.2" rx="1.2" fill="currentColor" opacity="0.55" />
      </g>

      {/* Bottom bar */}
      <rect x="0" y="16.2" width="9"  height="3.4" rx="0.6" fill="currentColor" opacity="0.78" />
    </svg>
  )
}
