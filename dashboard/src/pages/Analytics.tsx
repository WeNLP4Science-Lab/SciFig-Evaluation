import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import type { DataManifest } from '../types'
import { DATA_BASE_URL } from '../config'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, ScatterChart, Scatter, Cell,
} from 'recharts'

const COLORS = {
  primary: '#6750a4',
  secondary: '#625b71',
  tertiary: '#7d5260',
  accuracy: '#e8403f',
  completeness: '#e88d3f',
  clarity: '#4caf7c',
  major: '#e8403f',
  minor: '#e8b43f',
  models: ['#6750a4', '#0077b6', '#00897b', '#e88d3f', '#e8403f', '#7b61ff', '#00c49f', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'],
  judges: ['#6750a4', '#0077b6', '#00897b', '#e88d3f'],
}

interface AnalyticsProps {
  manifestFile?: string
  title?: string
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div
      className="rounded-xl p-6"
      style={{
        backgroundColor: 'var(--m3-surface-container)',
        border: '1px solid var(--m3-outline-variant)',
      }}
    >
      <h3
        className="text-sm font-medium mb-5"
        style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.1px' }}
      >
        {title}
      </h3>
      {children}
    </div>
  )
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
          <circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-surface-variant)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      )}
    </button>
  )
}

export default function Analytics({ manifestFile = 'manifest.json', title = 'Analytics' }: AnalyticsProps) {
  const [manifest, setManifest] = useState<DataManifest | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedJudge, setSelectedJudge] = useState('')
  const [compareJudge, setCompareJudge] = useState('')
  const [judgeType, setJudgeType] = useState<'reference_free' | 'reference_with_image'>('reference_free')
  const [viewTab, setViewTab] = useState<'per_judge' | 'cross_judge'>('per_judge')
  const { isDark } = useTheme()

  useEffect(() => {
    const url = `${DATA_BASE_URL}/${manifestFile}`
    fetch(url)
      .then(r => r.json())
      .then((data: DataManifest) => {
        setManifest(data)
        if (data.judge_models?.length) {
          setSelectedJudge(data.judge_models[0])
          setCompareJudge(data.judge_models.length > 1 ? data.judge_models[1] : data.judge_models[0])
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [manifestFile])

  // Aggregate: MQM Score by Model
  const scoreByModel = useMemo(() => {
    if (!manifest) return []
    const acc: Record<string, { sum: number; count: number }> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      const score = jr.mqm_score ?? jr.mqm_score_avg
      if (score == null) continue
      if (!acc[fig.model_name]) acc[fig.model_name] = { sum: 0, count: 0 }
      acc[fig.model_name].sum += score
      acc[fig.model_name].count++
    }
    return Object.entries(acc)
      .map(([model, { sum, count }]) => ({ model, score: Math.round(sum / count * 10) / 10 }))
      .sort((a, b) => b.score - a.score)
  }, [manifest, selectedJudge, judgeType])

  // Aggregate: MQM Score by Language
  const scoreByLanguage = useMemo(() => {
    if (!manifest) return []
    const langMap: Record<string, string> = {
      bulgarian_only: 'Bulgarian', chinese_only: 'Chinese',
      english_only: 'English', german_only: 'German', multi_language: 'Multilingual',
    }
    const acc: Record<string, { sum: number; count: number }> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      const score = jr.mqm_score ?? jr.mqm_score_avg
      if (score == null) continue
      const lang = langMap[fig.subfolder] || fig.subfolder
      if (!acc[lang]) acc[lang] = { sum: 0, count: 0 }
      acc[lang].sum += score
      acc[lang].count++
    }
    return Object.entries(acc)
      .map(([language, { sum, count }]) => ({ language, score: Math.round(sum / count * 10) / 10 }))
      .sort((a, b) => b.score - a.score)
  }, [manifest, selectedJudge, judgeType])

  // Aggregate: Error Categories by Model
  const errorsByModel = useMemo(() => {
    if (!manifest) return []
    const acc: Record<string, { accuracy: number; completeness: number; clarity: number; total: number }> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      if (!acc[fig.model_name]) acc[fig.model_name] = { accuracy: 0, completeness: 0, clarity: 0, total: 0 }
      for (const err of (jr.errors || [])) {
        acc[fig.model_name].total++
        if (err.category === 'Accuracy') acc[fig.model_name].accuracy++
        else if (err.category === 'Completeness') acc[fig.model_name].completeness++
        else acc[fig.model_name].clarity++
      }
    }
    return Object.entries(acc)
      .map(([model, counts]) => ({ model, ...counts }))
      .sort((a, b) => a.total - b.total)
  }, [manifest, selectedJudge, judgeType])

  // Aggregate: Error Categories by Language
  const errorsByLanguage = useMemo(() => {
    if (!manifest) return []
    const langMap: Record<string, string> = {
      bulgarian_only: 'Bulgarian', chinese_only: 'Chinese',
      english_only: 'English', german_only: 'German', multi_language: 'Multilingual',
    }
    const acc: Record<string, { accuracy: number; completeness: number; clarity: number; total: number }> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      const lang = langMap[fig.subfolder] || fig.subfolder
      if (!acc[lang]) acc[lang] = { accuracy: 0, completeness: 0, clarity: 0, total: 0 }
      for (const err of (jr.errors || [])) {
        acc[lang].total++
        if (err.category === 'Accuracy') acc[lang].accuracy++
        else if (err.category === 'Completeness') acc[lang].completeness++
        else acc[lang].clarity++
      }
    }
    return Object.entries(acc)
      .map(([language, counts]) => ({ language, ...counts }))
      .sort((a, b) => b.total - a.total)
  }, [manifest, selectedJudge, judgeType])

  // Aggregate: Error sub-types
  const errorSubTypes = useMemo(() => {
    if (!manifest) return []
    const acc: Record<string, number> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      for (const err of (jr.errors || [])) {
        const key = err.sub_type || 'Unknown'
        acc[key] = (acc[key] || 0) + 1
      }
    }
    return Object.entries(acc)
      .map(([subType, count]) => ({ subType, count }))
      .sort((a, b) => b.count - a.count)
  }, [manifest, selectedJudge, judgeType])

  // Aggregate: Severity distribution
  const severityDist = useMemo(() => {
    if (!manifest) return []
    const acc: Record<string, { major: number; minor: number }> = {}
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      if (!acc[fig.model_name]) acc[fig.model_name] = { major: 0, minor: 0 }
      for (const err of (jr.errors || [])) {
        if (err.severity === 'Major') acc[fig.model_name].major++
        else acc[fig.model_name].minor++
      }
    }
    return Object.entries(acc)
      .map(([model, counts]) => ({ model, ...counts }))
      .sort((a, b) => (b.major + b.minor) - (a.major + a.minor))
  }, [manifest, selectedJudge, judgeType])

  // When selectedJudge changes, ensure compareJudge is different
  useEffect(() => {
    if (!manifest?.judge_models?.length) return
    if (!compareJudge || compareJudge === selectedJudge) {
      const other = manifest.judge_models.find(j => j !== selectedJudge)
      if (other) setCompareJudge(other)
    }
  }, [selectedJudge, manifest])

  // Score Agreement: scatter data between selected judge and compare judge
  const scatterData = useMemo(() => {
    if (!manifest || !selectedJudge || !compareJudge || selectedJudge === compareJudge) return { pairs: [], judgeA: '', judgeB: '' }
    const pairs: { scoreA: number; scoreB: number; model: string }[] = []
    for (const fig of manifest.figures) {
      const a = fig.judges[selectedJudge]?.[judgeType]
      const b = fig.judges[compareJudge]?.[judgeType]
      if (!a || !b) continue
      const sA = a.mqm_score ?? a.mqm_score_avg
      const sB = b.mqm_score ?? b.mqm_score_avg
      if (sA != null && sB != null) {
        pairs.push({ scoreA: sA, scoreB: sB, model: fig.model_name })
      }
    }
    return { pairs, judgeA: selectedJudge, judgeB: compareJudge }
  }, [manifest, selectedJudge, compareJudge, judgeType])

  // Heatmap: Model x Language
  const heatmapData = useMemo(() => {
    if (!manifest) return { rows: [] as { model: string;[key: string]: string | number }[], languages: [] as string[] }
    const langMap: Record<string, string> = {
      bulgarian_only: 'BG', chinese_only: 'ZH',
      english_only: 'EN', german_only: 'DE', multi_language: 'Multi',
    }
    const acc: Record<string, Record<string, { sum: number; count: number }>> = {}
    const langs = new Set<string>()
    for (const fig of manifest.figures) {
      const jr = fig.judges[selectedJudge]?.[judgeType]
      if (!jr) continue
      const score = jr.mqm_score ?? jr.mqm_score_avg
      if (score == null) continue
      const lang = langMap[fig.subfolder] || fig.subfolder
      langs.add(lang)
      if (!acc[fig.model_name]) acc[fig.model_name] = {}
      if (!acc[fig.model_name][lang]) acc[fig.model_name][lang] = { sum: 0, count: 0 }
      acc[fig.model_name][lang].sum += score
      acc[fig.model_name][lang].count++
    }
    const languages = Array.from(langs).sort()
    const rows = Object.entries(acc).map(([model, langScores]) => {
      const row: { model: string;[key: string]: string | number } = { model }
      for (const lang of languages) {
        const d = langScores[lang]
        row[lang] = d ? Math.round(d.sum / d.count * 10) / 10 : 0
      }
      return row
    })
    return { rows, languages }
  }, [manifest, selectedJudge, judgeType])

  // Cross-Judge: All judges MQM scores by model
  const allJudgesScoreByModel = useMemo(() => {
    if (!manifest || !manifest.judge_models) return []
    const acc: Record<string, Record<string, { sum: number; count: number }>> = {}
    for (const fig of manifest.figures) {
      if (!acc[fig.model_name]) acc[fig.model_name] = {}
      for (const judge of manifest.judge_models) {
        const jr = fig.judges[judge]?.[judgeType]
        if (!jr) continue
        const score = jr.mqm_score ?? jr.mqm_score_avg
        if (score == null) continue
        if (!acc[fig.model_name][judge]) acc[fig.model_name][judge] = { sum: 0, count: 0 }
        acc[fig.model_name][judge].sum += score
        acc[fig.model_name][judge].count++
      }
    }
    return Object.entries(acc).map(([model, judges]) => {
      const row: Record<string, string | number> = { model }
      for (const [judge, { sum, count }] of Object.entries(judges)) {
        row[judge] = Math.round(sum / count * 10) / 10
      }
      return row
    }).sort((a, b) => {
      const avgA = manifest.judge_models!.reduce((s, j) => s + ((a[j] as number) || 0), 0) / manifest.judge_models!.length
      const avgB = manifest.judge_models!.reduce((s, j) => s + ((b[j] as number) || 0), 0) / manifest.judge_models!.length
      return avgB - avgA
    })
  }, [manifest, judgeType])

  // Cross-Judge: Ref-Free vs Ref+Image per model (averaged across all judges)
  const refFreeVsImage = useMemo(() => {
    if (!manifest || !manifest.judge_models) return []
    const acc: Record<string, { freeSum: number; freeCount: number; imgSum: number; imgCount: number }> = {}
    for (const fig of manifest.figures) {
      if (!acc[fig.model_name]) acc[fig.model_name] = { freeSum: 0, freeCount: 0, imgSum: 0, imgCount: 0 }
      for (const judge of manifest.judge_models) {
        const free = fig.judges[judge]?.['reference_free']
        const img = fig.judges[judge]?.['reference_with_image']
        const freeScore = free?.mqm_score ?? free?.mqm_score_avg
        const imgScore = img?.mqm_score ?? img?.mqm_score_avg
        if (freeScore != null) { acc[fig.model_name].freeSum += freeScore; acc[fig.model_name].freeCount++ }
        if (imgScore != null) { acc[fig.model_name].imgSum += imgScore; acc[fig.model_name].imgCount++ }
      }
    }
    return Object.entries(acc).map(([model, d]) => ({
      model,
      'Ref-Free': d.freeCount ? Math.round(d.freeSum / d.freeCount * 10) / 10 : 0,
      'Ref+Image': d.imgCount ? Math.round(d.imgSum / d.imgCount * 10) / 10 : 0,
    })).sort((a, b) => b['Ref-Free'] - a['Ref-Free'])
  }, [manifest])

  // Cross-Judge: Ref-Free vs Ref+Image per judge
  const refFreeVsImageByJudge = useMemo(() => {
    if (!manifest || !manifest.judge_models) return []
    const acc: Record<string, { freeSum: number; freeCount: number; imgSum: number; imgCount: number }> = {}
    for (const fig of manifest.figures) {
      for (const judge of manifest.judge_models) {
        if (!acc[judge]) acc[judge] = { freeSum: 0, freeCount: 0, imgSum: 0, imgCount: 0 }
        const free = fig.judges[judge]?.['reference_free']
        const img = fig.judges[judge]?.['reference_with_image']
        const freeScore = free?.mqm_score ?? free?.mqm_score_avg
        const imgScore = img?.mqm_score ?? img?.mqm_score_avg
        if (freeScore != null) { acc[judge].freeSum += freeScore; acc[judge].freeCount++ }
        if (imgScore != null) { acc[judge].imgSum += imgScore; acc[judge].imgCount++ }
      }
    }
    return Object.entries(acc).map(([judge, d]) => ({
      judge,
      'Ref-Free': d.freeCount ? Math.round(d.freeSum / d.freeCount * 10) / 10 : 0,
      'Ref+Image': d.imgCount ? Math.round(d.imgSum / d.imgCount * 10) / 10 : 0,
    }))
  }, [manifest])

  const axisStyle = {
    fontSize: 11,
    fill: isDark ? '#938f99' : '#79747e',
  }

  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'
  const tooltipStyle = { backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="w-10 h-10 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--m3-on-surface-variant)' }}>Loading analytics</span>
      </div>
    </div>
  )

  if (!manifest) return null

  return (
    <div className="min-h-screen flex flex-col animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header
        className="px-6 h-16 flex items-center gap-4"
        style={{ borderBottom: `1px solid var(--m3-outline-variant)`, backgroundColor: 'var(--m3-surface)' }}
      >
        <Link to="/analytics" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
        </Link>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--m3-primary)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--m3-on-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 20V10" /><path d="M12 20V4" /><path d="M6 20v-6" />
            </svg>
          </div>
          <h1 className="text-base font-medium" style={{ color: 'var(--m3-on-surface)', letterSpacing: '0.15px' }}>{title}</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          {/* View tab toggle */}
          <div className="inline-flex rounded-full overflow-hidden" style={{ border: `1px solid var(--m3-outline)` }}>
            {(['per_judge', 'cross_judge'] as const).map((tab, idx) => (
              <button
                key={tab}
                onClick={() => setViewTab(tab)}
                className="px-4 py-1.5 text-xs font-medium"
                style={{
                  backgroundColor: viewTab === tab ? 'var(--m3-primary-container)' : 'transparent',
                  color: viewTab === tab ? 'var(--m3-on-primary-container)' : 'var(--m3-on-surface)',
                  borderRight: idx === 0 ? `1px solid var(--m3-outline)` : 'none',
                }}
              >
                {tab === 'per_judge' ? 'Per Judge' : 'Cross Judge'}
              </button>
            ))}
          </div>

          {/* Judge type toggle - shown in per-judge view */}
          {viewTab === 'per_judge' && (
            <div className="inline-flex rounded-full overflow-hidden" style={{ border: `1px solid var(--m3-outline)` }}>
              {(['reference_free', 'reference_with_image'] as const).map((jt, idx) => (
                <button
                  key={jt}
                  onClick={() => setJudgeType(jt)}
                  className="px-4 py-1.5 text-xs font-medium"
                  style={{
                    backgroundColor: judgeType === jt ? 'var(--m3-secondary-container)' : 'transparent',
                    color: judgeType === jt ? 'var(--m3-on-secondary-container)' : 'var(--m3-on-surface)',
                    borderRight: idx === 0 ? `1px solid var(--m3-outline)` : 'none',
                  }}
                >
                  {jt === 'reference_free' ? 'Ref-Free' : 'Ref+Image'}
                </button>
              ))}
            </div>
          )}

          {/* Judge selector - shown in per-judge view */}
          {viewTab === 'per_judge' && (
            <select className="m3-select" value={selectedJudge} onChange={e => setSelectedJudge(e.target.value)}>
              {(manifest.judge_models || []).map(j => <option key={j} value={j}>{j}</option>)}
            </select>
          )}
          <ThemeToggle />
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-7xl mx-auto space-y-6">

          {/* ===== CROSS-JUDGE VIEW ===== */}
          {viewTab === 'cross_judge' && (<>
            {/* All Judges Score Comparison */}
            <ChartCard title="MQM Score by Model — All Judges">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={allJudgesScoreByModel} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} tick={axisStyle} />
                  <YAxis type="category" dataKey="model" tick={axisStyle} width={95} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  {(manifest.judge_models || []).map((judge, i) => (
                    <Bar key={judge} dataKey={judge} fill={COLORS.judges[i % COLORS.judges.length]} radius={i === (manifest.judge_models?.length ?? 1) - 1 ? [0, 4, 4, 0] : undefined} />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            {/* Ref-Free vs Ref+Image Comparison */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Ref-Free vs Ref+Image — By Model">
                <p className="text-xs mb-3" style={{ color: 'var(--m3-on-surface-variant)' }}>
                  Averaged across all judges
                </p>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={refFreeVsImage} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                    <XAxis type="number" domain={[0, 100]} tick={axisStyle} />
                    <YAxis type="category" dataKey="model" tick={axisStyle} width={95} />
                    <Tooltip contentStyle={tooltipStyle} />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    <Bar dataKey="Ref-Free" fill="#6750a4" />
                    <Bar dataKey="Ref+Image" fill="#00897b" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard title="Ref-Free vs Ref+Image — By Judge">
                <p className="text-xs mb-3" style={{ color: 'var(--m3-on-surface-variant)' }}>
                  Averaged across all models
                </p>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={refFreeVsImageByJudge} margin={{ left: 10, right: 20, top: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                    <XAxis dataKey="judge" tick={axisStyle} />
                    <YAxis domain={[0, 100]} tick={axisStyle} />
                    <Tooltip contentStyle={tooltipStyle} />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    <Bar dataKey="Ref-Free" fill="#6750a4" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="Ref+Image" fill="#00897b" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>
          </>)}

          {/* ===== PER-JUDGE VIEW ===== */}
          {viewTab === 'per_judge' && (<>
          {/* Row 1: Score by Model + Score by Language */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="MQM Score by Model">
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={scoreByModel} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} tick={axisStyle} />
                  <YAxis type="category" dataKey="model" tick={axisStyle} width={95} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                    {scoreByModel.map((_, i) => (
                      <Cell key={i} fill={COLORS.models[i % COLORS.models.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="MQM Score by Language">
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={scoreByLanguage} margin={{ left: 10, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                  <XAxis dataKey="language" tick={axisStyle} />
                  <YAxis domain={[0, 100]} tick={axisStyle} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                    {scoreByLanguage.map((_, i) => (
                      <Cell key={i} fill={COLORS.models[i % COLORS.models.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>

          {/* Row 2: Error Categories by Model + by Language */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Error Categories by Model">
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={errorsByModel} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                  <XAxis type="number" tick={axisStyle} />
                  <YAxis type="category" dataKey="model" tick={axisStyle} width={95} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Bar dataKey="accuracy" stackId="a" fill={COLORS.accuracy} name="Accuracy" />
                  <Bar dataKey="completeness" stackId="a" fill={COLORS.completeness} name="Completeness" />
                  <Bar dataKey="clarity" stackId="a" fill={COLORS.clarity} name="Clarity" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Error Categories by Language">
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={errorsByLanguage} margin={{ left: 10, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                  <XAxis dataKey="language" tick={axisStyle} />
                  <YAxis tick={axisStyle} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Bar dataKey="accuracy" stackId="a" fill={COLORS.accuracy} name="Accuracy" />
                  <Bar dataKey="completeness" stackId="a" fill={COLORS.completeness} name="Completeness" />
                  <Bar dataKey="clarity" stackId="a" fill={COLORS.clarity} name="Clarity" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>

          {/* Row 3: Error Types + Severity */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Error Types">
              <ResponsiveContainer width="100%" height={360}>
                <BarChart data={errorSubTypes} layout="vertical" margin={{ left: 160, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                  <XAxis type="number" tick={axisStyle} />
                  <YAxis type="category" dataKey="subType" tick={{ ...axisStyle, fontSize: 10 }} width={155} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Bar dataKey="count" fill={COLORS.primary} radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Severity Distribution">
              <ResponsiveContainer width="100%" height={360}>
                <BarChart data={severityDist} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                  <XAxis type="number" tick={axisStyle} />
                  <YAxis type="category" dataKey="model" tick={axisStyle} width={95} />
                  <Tooltip contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Bar dataKey="major" stackId="a" fill={COLORS.major} name="Major" />
                  <Bar dataKey="minor" stackId="a" fill={COLORS.minor} name="Minor" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>

          {/* Row 4: Score Agreement + Heatmap */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Score Agreement">
              <div className="flex items-center gap-3 mb-3">
                <p className="text-xs" style={{ color: 'var(--m3-on-surface-variant)' }}>
                  {selectedJudge} vs
                </p>
                <select
                  className="m3-select"
                  value={compareJudge}
                  onChange={e => setCompareJudge(e.target.value)}
                >
                  {(manifest.judge_models || []).filter(j => j !== selectedJudge).map(j => (
                    <option key={j} value={j}>{j}</option>
                  ))}
                </select>
                <p className="text-xs ml-auto" style={{ color: 'var(--m3-outline)' }}>
                  Diagonal = perfect agreement
                </p>
              </div>
              <ResponsiveContainer width="100%" height={360}>
                <ScatterChart margin={{ left: 10, right: 20, top: 5, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                  <XAxis type="number" dataKey="scoreA" name={scatterData.judgeA} domain={[0, 100]} tick={axisStyle} label={{ value: scatterData.judgeA, position: 'bottom', offset: 0, style: axisStyle }} />
                  <YAxis type="number" dataKey="scoreB" name={scatterData.judgeB} domain={[0, 100]} tick={axisStyle} label={{ value: scatterData.judgeB, angle: -90, position: 'insideLeft', style: axisStyle }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: isDark ? '#2b2930' : '#fff', border: 'none', borderRadius: 12, fontSize: 12 }}
                    formatter={(value: any, name: any) => [value, name === 'scoreA' ? scatterData.judgeA : scatterData.judgeB]}
                    labelFormatter={(_, payload) => payload?.[0]?.payload?.model || ''}
                  />
                  <Legend wrapperStyle={{ fontSize: 10, paddingTop: 8 }} />
                  {(manifest.models || []).map((model, i) => {
                    const modelPairs = scatterData.pairs.filter(p => p.model === model)
                    if (!modelPairs.length) return null
                    return (
                      <Scatter key={model} name={model} data={modelPairs} fill={COLORS.models[i % COLORS.models.length]} fillOpacity={0.6} r={4} />
                    )
                  })}
                </ScatterChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Model x Language Heatmap">
              <div className="overflow-x-auto">
                <table className="w-full text-xs" style={{ borderCollapse: 'separate', borderSpacing: 2 }}>
                  <thead>
                    <tr>
                      <th className="text-left p-2" style={{ color: 'var(--m3-on-surface-variant)' }}>Model</th>
                      {heatmapData.languages.map(lang => (
                        <th key={lang} className="p-2 text-center" style={{ color: 'var(--m3-on-surface-variant)' }}>{lang}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {heatmapData.rows.map(row => (
                      <tr key={row.model}>
                        <td className="p-2 font-medium" style={{ color: 'var(--m3-on-surface)', fontSize: 10 }}>{row.model}</td>
                        {heatmapData.languages.map(lang => {
                          const val = row[lang] as number
                          let bg: string
                          let fg: string
                          if (val === 0) {
                            bg = 'var(--m3-surface-container-highest)'
                            fg = 'var(--m3-on-surface-variant)'
                          } else if (val >= 80) {
                            const intensity = (val - 80) / 20
                            bg = isDark
                              ? `rgba(76,175,124,${0.2 + intensity * 0.4})`
                              : `rgba(76,175,124,${0.12 + intensity * 0.35})`
                            fg = isDark ? '#a8f0c8' : '#1a6b3e'
                          } else if (val >= 60) {
                            const intensity = (val - 60) / 20
                            bg = isDark
                              ? `rgba(232,180,63,${0.2 + intensity * 0.4})`
                              : `rgba(232,180,63,${0.12 + intensity * 0.35})`
                            fg = isDark ? '#ffe08a' : '#8a6b00'
                          } else {
                            const intensity = Math.max(0, (60 - val) / 60)
                            bg = isDark
                              ? `rgba(232,64,63,${0.2 + intensity * 0.4})`
                              : `rgba(232,64,63,${0.12 + intensity * 0.35})`
                            fg = isDark ? '#ffb4ab' : '#ba1a1a'
                          }
                          return (
                            <td
                              key={lang}
                              className="p-2 text-center rounded-md font-medium tabular-nums"
                              style={{ backgroundColor: bg, color: fg, fontSize: 11 }}
                            >
                              {val || '-'}
                            </td>
                          )
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </ChartCard>
          </div>
          </>)}

        </div>
      </main>
    </div>
  )
}
