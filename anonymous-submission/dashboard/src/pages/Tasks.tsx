import { useState } from 'react'

const c = {
  bg: '#09090b', surface: '#131316', surfaceHover: '#1c1c21',
  surfaceActive: '#232329', surfaceRaised: '#18181b',
  border: 'rgba(255,255,255,0.06)', borderStrong: 'rgba(255,255,255,0.1)',
  fg: '#fafafa', muted: '#a1a1aa', dim: '#52525b', accent: '#3b82f6',
}

const CHART_TYPES = ['Bar Chart', 'Line Plot', 'Pie Chart'] as const

const PROMPTS: Record<string, string> = {
  'Bar Chart': `You are an annotator tasked with describing scientific bar charts in a structured but natural paragraph format.

Your goal is to objectively describe what is shown, using neutral and technical language. Avoid making inferences, comparisons, or drawing conclusions about the data.

For each bar chart, write a single paragraph that includes:

    A description of the overall purpose of the chart (what is being illustrated, compared, or represented)

    A description of the axes: indicate which axis contains the categories (horizontal or vertical), and describe the axis label, order, and scale type if present (e.g., linear, logarithmic). Then describe the value axis, including its label, scale, value range, units (if present), and tick label interval if numeric and regularly spaced

    A description of each bar (or grouped/stacked set of bars), including the label, color, and approximate value or length. Where possible, include representative values from the shortest and tallest bars or note consistent trends in height or length, using exact data from the chart

    If the chart contains grouped or stacked bars, explain how the grouping or stacking is visually arranged and what each component represents based on labels or legends

    Mention whether the bars are sorted in a specific way (e.g., descending, alphabetical), and whether any bars are visually emphasized (e.g., shaded, bolded, outlined, or annotated)

Avoid interpreting causes or trends, and do not compare categories unless the comparison is explicitly labeled. Focus solely on visual and labeled characteristics.

Write everything in a single, continuous paragraph without section headers or bullet points.`,
  'Line Plot': `You are an annotator tasked with describing scientific line plots in a structured but natural paragraph format.

Your goal is to clearly describe what is shown, without making inferences or drawing conclusions. Stick to objective features only. Use neutral, technical language.

For each plot, write a single paragraph that includes:

    A description of the overall purpose of the plot (what is being illustrated, compared, or represented)

    A description of the x-axis, including its label, scale type (e.g., linear or logarithmic), value range, units (if present), and tick label interval if numeric and regularly spaced

    A description of the y-axis, following the same structure as the x-axis

    A description of each line in the plot, including its color, marker shape, line style (e.g., solid, dashed), and how it changes across the x-axis. Where possible, include representative values at the start and end of the x-axis, and note any peaks, declines, or steady trends using exact data points from the plot (not inferred ones)

Avoid interpreting the cause of changes or making comparisons between lines. Do not include section titles; write everything in flowing sentences within a single paragraph per plot.
If multiple plots share the same axes, describe the axes together first, then write one paragraph per plot.`,
  'Pie Chart': `You are an annotator tasked with describing scientific pie charts in a structured but natural paragraph format.

Your goal is to objectively describe what is shown in the chart, using neutral and technical language. Avoid interpreting or explaining the significance of the proportions.

For each chart, write a single paragraph that includes:

    A description of the overall purpose of the chart (what is being represented or compared)

    The total number of slices (or categories) shown

    For each slice, include the label, color (if distinguishable), and approximate percentage or proportion if shown or easily estimated

    Mention whether the chart includes a legend, percentage labels inside the slices, or if any slices are visually emphasized (e.g. exploded, offset, or bolded)

    If the segments appear ordered in a particular way (e.g. descending size), note this as a visual observation, not interpretation

Write everything in a single, natural paragraph. Do not include section titles or bullet points. Avoid drawing conclusions or comparing slices beyond what is visually and explicitly presented.`,
}

interface ChecklistItem {
  id: string
  label: string
  dimension: 'Accuracy' | 'Completeness' | 'Clarity'
}

const CHECKLISTS: Record<string, ChecklistItem[]> = {
  'Bar Chart': [
    { id: 'bc1', label: 'Chart purpose / what is being compared', dimension: 'Completeness' },
    { id: 'bc2', label: 'Category axis: label, categories listed, order', dimension: 'Completeness' },
    { id: 'bc3', label: 'Value axis: label, scale type, range, units, tick interval', dimension: 'Completeness' },
    { id: 'bc4', label: 'Each bar described: label, color, approximate value', dimension: 'Completeness' },
    { id: 'bc5', label: 'Grouped/stacked structure explained (if present)', dimension: 'Completeness' },
    { id: 'bc6', label: 'Legend / color-to-label mapping described', dimension: 'Completeness' },
    { id: 'bc7', label: 'Sorting order noted (descending, alphabetical, etc.)', dimension: 'Completeness' },
    { id: 'bc8', label: 'Visual emphasis noted (annotations, bold, outlines)', dimension: 'Completeness' },
    { id: 'bc11', label: 'Other elements if present: error bars, confidence intervals, truncated axis (non-zero baseline), reference lines, data annotations on bars, extrema callouts (max/min)', dimension: 'Completeness' },
  ],
  'Line Plot': [
    { id: 'lp1', label: 'Chart purpose / what is being illustrated', dimension: 'Completeness' },
    { id: 'lp2', label: 'X-axis: label, scale type, range, units, tick interval', dimension: 'Completeness' },
    { id: 'lp3', label: 'Y-axis: label, scale type, range, units, tick interval', dimension: 'Completeness' },
    { id: 'lp4', label: 'Each line described: color, marker shape, line style', dimension: 'Completeness' },
    { id: 'lp5', label: 'Line trajectory: start value, end value, peaks, declines', dimension: 'Completeness' },
    { id: 'lp6', label: 'Representative data points with exact values', dimension: 'Accuracy' },
    { id: 'lp7', label: 'Legend / color-to-label mapping described', dimension: 'Completeness' },
    { id: 'lp8', label: 'Subplots: shared axes described, then per-subplot', dimension: 'Completeness' },
    { id: 'lp11', label: 'Other elements if present: inflection points, crossover points between lines, convergence/divergence, dual y-axes, confidence intervals, shaded regions, rate of change (steep/gradual)', dimension: 'Completeness' },
  ],
  'Pie Chart': [
    { id: 'pc1', label: 'Chart purpose / what is being represented', dimension: 'Completeness' },
    { id: 'pc2', label: 'Total number of slices stated correctly', dimension: 'Accuracy' },
    { id: 'pc3', label: 'Each slice: label, color, percentage or proportion', dimension: 'Completeness' },
    { id: 'pc4', label: 'Legend presence noted', dimension: 'Completeness' },
    { id: 'pc5', label: 'Percentage label placement noted (inside/outside)', dimension: 'Completeness' },
    { id: 'pc6', label: 'Visual emphasis noted (exploded, offset, bold)', dimension: 'Completeness' },
    { id: 'pc7', label: 'Ordering noted (descending size, etc.)', dimension: 'Completeness' },
    { id: 'pc10', label: 'Other elements if present: nested/donut structure, estimated vs exact percentages distinguished, clockwise ordering, sum verification (=100%), leader lines, label placement strategy', dimension: 'Completeness' },
  ],
}

const DIM_COLORS: Record<string, { dot: string; bg: string }> = {
  Accuracy: { dot: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
  Completeness: { dot: '#3b82f6', bg: 'rgba(59,130,246,0.1)' },
  Clarity: { dot: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
}

export default function Tasks() {
  const [activeType, setActiveType] = useState<string>('Bar Chart')

  return (
    <div style={{ minHeight: '100vh' }}>
      {/* Header */}
      <header style={{ borderBottom: `1px solid ${c.border}` }}>
        <div className="page-container" style={{ paddingTop: 48, paddingBottom: 36 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <span style={{
              fontSize: 11, fontWeight: 600, letterSpacing: '0.08em',
              textTransform: 'uppercase', color: c.accent,
            }}>
              Tasks
            </span>
          </div>
          <h1 style={{
            fontSize: 28, fontWeight: 600, letterSpacing: '-0.02em',
            color: c.fg, lineHeight: 1.2, margin: 0,
          }}>
            Description Generation
          </h1>
          <p style={{
            fontSize: 14, color: c.muted, marginTop: 10, maxWidth: 600, lineHeight: 1.6,
          }}>
            VLMs are prompted to describe scientific figures. The atomic MQM checklist defines
            what a complete and accurate description should contain, per chart type.
          </p>
        </div>
      </header>

      {/* Chart type tabs */}
      <div style={{
        borderBottom: `1px solid ${c.border}`,
        position: 'sticky', top: 0, zIndex: 20,
        background: 'rgba(9,9,11,0.92)', backdropFilter: 'blur(12px)',
      }}>
        <div className="page-container" style={{ display: 'flex', gap: 0 }}>
          {CHART_TYPES.map(ct => (
            <button
              key={ct}
              onClick={() => setActiveType(ct)}
              style={{
                padding: '12px 20px', background: 'none', border: 'none',
                borderBottom: activeType === ct ? '2px solid #3b82f6' : '2px solid transparent',
                cursor: 'pointer', fontFamily: 'inherit',
                fontSize: 13, fontWeight: activeType === ct ? 500 : 400,
                color: activeType === ct ? c.fg : c.muted,
                transition: 'all 0.15s ease', marginBottom: -1,
              }}
            >
              {ct}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="page-container" style={{ paddingTop: 32, paddingBottom: 48 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
          {/* Left: Prompt */}
          <div>
            <SectionHeader>Prompt Instructions</SectionHeader>
            <div style={{
              borderRadius: 10, border: `1px solid ${c.border}`,
              background: c.surface, padding: 20,
            }}>
              <p style={{
                fontSize: 13, color: c.muted, lineHeight: 1.75, margin: 0,
                whiteSpace: 'pre-wrap',
              }}>
                {PROMPTS[activeType]}
              </p>
            </div>

            {/* MQM dimensions legend */}
            <div style={{ marginTop: 20 }}>
              <SectionHeader>MQM Scoring Dimensions</SectionHeader>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <DimCard
                  name="Accuracy"
                  desc="Are the stated facts correct? Values, labels, colors match the figure."
                  severity="Minor (small rounding) → Major (wrong value) → Critical (fabricated data)"
                />
                <DimCard
                  name="Completeness"
                  desc="Are all checklist items mentioned? Missing elements reduce the score."
                  severity="Minor (optional detail) → Major (key element omitted) → Critical (core structure missing)"
                />
                <DimCard
                  name="Clarity"
                  desc="Is the description understandable? Coherent structure, no ambiguity."
                  severity="Minor (awkward phrasing) → Major (confusing structure) → Critical (unintelligible)"
                />
              </div>
            </div>
          </div>

          {/* Right: Checklist */}
          <div>
            <SectionHeader>
              Atomic MQM Checklist — {activeType} ({CHECKLISTS[activeType].length} items)
            </SectionHeader>
            <div style={{
              borderRadius: 10, border: `1px solid ${c.border}`,
              background: c.surface, overflow: 'hidden',
            }}>
              {CHECKLISTS[activeType].map((item, i) => {
                return (
                  <div
                    key={item.id}
                    style={{
                      display: 'flex', alignItems: 'flex-start', gap: 12,
                      padding: '14px 16px',
                      borderBottom: i < CHECKLISTS[activeType].length - 1
                        ? `1px solid ${c.border}` : 'none',
                    }}
                  >
                    <span style={{
                      width: 22, height: 22, borderRadius: 6,
                      background: c.surfaceRaised, border: `1px solid ${c.border}`,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: 11, fontWeight: 600, color: c.dim, flexShrink: 0,
                      marginTop: 1,
                    }}>
                      {i + 1}
                    </span>
                    <div style={{ flex: 1 }}>
                      <p style={{ fontSize: 13, color: c.fg, margin: 0, lineHeight: 1.5 }}>
                        {item.label}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <p style={{
      fontSize: 11, fontWeight: 600, textTransform: 'uppercase',
      letterSpacing: '0.08em', color: '#52525b', marginBottom: 12,
      lineHeight: 1,
    }}>
      {children}
    </p>
  )
}

function DimCard({ name, desc, severity }: { name: string; desc: string; severity: string }) {
  const dim = DIM_COLORS[name]
  return (
    <div style={{
      borderRadius: 8, border: `1px solid ${c.border}`,
      background: c.surface, padding: '12px 14px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
        <span style={{
          width: 8, height: 8, borderRadius: '50%', background: dim.dot,
        }} />
        <span style={{ fontSize: 12, fontWeight: 600, color: c.fg }}>{name}</span>
      </div>
      <p style={{ fontSize: 12, color: c.muted, margin: '0 0 4px', lineHeight: 1.5 }}>{desc}</p>
      <p style={{ fontSize: 11, color: c.dim, margin: 0, lineHeight: 1.4 }}>{severity}</p>
    </div>
  )
}
