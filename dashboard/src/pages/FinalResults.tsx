// @ts-nocheck
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'

type TabId = 'overview' | 'atomic_mqm' | 'transforms' | 'capability' | 'resistance' | 'admittance' | 'cot' | 'ablation'

const TABS: { id: TabId; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'atomic_mqm', label: 'Atomic MQM' },
  { id: 'transforms', label: 'Transforms' },
  { id: 'capability', label: 'Capability' },
  { id: 'resistance', label: 'Resistance' },
  { id: 'admittance', label: 'Admittance' },
  { id: 'cot', label: 'Chain-of-Thought' },
  { id: 'ablation', label: 'Prompt Ablation' },
]

const LANG_SHORT: Record<string, string> = {
  'bulgarian_only': 'BG',
  'chinese_only': 'CN',
  'english_only': 'EN',
  'german_only': 'DE',
  'multi_language': 'Multi',
}

const LANG_KEYS = ['bulgarian_only', 'chinese_only', 'english_only', 'german_only', 'multi_language']

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-8">
      <h3 className="text-sm font-semibold uppercase tracking-wider mb-4" style={{ color: 'var(--m3-on-surface-variant)' }}>{title}</h3>
      {children}
    </div>
  )
}

function Table({ rows, columns, sortBy }: { rows: any[]; columns: { key: string; label: string; fmt?: (v: any) => string }[]; sortBy?: string }) {
  const sorted = useMemo(() => {
    if (!sortBy) return rows
    return [...rows].sort((a, b) => (b[sortBy] ?? -1) - (a[sortBy] ?? -1))
  }, [rows, sortBy])

  return (
    <div className="overflow-x-auto rounded-lg" style={{ border: '1px solid var(--m3-outline-variant)' }}>
      <table className="w-full text-xs">
        <thead>
          <tr style={{ backgroundColor: 'var(--m3-surface-container)', borderBottom: '1px solid var(--m3-outline-variant)' }}>
            <th className="text-left px-3 py-2 font-semibold" style={{ color: 'var(--m3-on-surface-variant)' }}>#</th>
            {columns.map(c => (
              <th key={c.key} className="text-left px-3 py-2 font-semibold" style={{ color: 'var(--m3-on-surface-variant)' }}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, i) => (
            <tr key={i} style={{ borderBottom: '1px solid var(--m3-outline-variant)', backgroundColor: i % 2 === 0 ? 'var(--m3-surface)' : 'var(--m3-surface-container-low)' }}>
              <td className="px-3 py-2 font-mono tabular-nums" style={{ color: 'var(--m3-outline)' }}>{i + 1}</td>
              {columns.map(c => (
                <td key={c.key} className="px-3 py-2" style={{ color: 'var(--m3-on-surface)' }}>
                  {c.fmt ? c.fmt(row[c.key]) : (row[c.key] ?? '—')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

const fmtScore = (v: any) => v != null ? Number(v).toFixed(2) : '—'
const fmtPct = (v: any) => v != null ? `${(Number(v) * 100).toFixed(1)}%` : '—'
const fmtDelta = (v: any) => {
  if (v == null) return '—'
  const n = Number(v)
  return `${n > 0 ? '+' : ''}${n.toFixed(2)}`
}

/** Pivot rows with a 'language' field into one row per model with language columns */
function pivotByLanguage(rows: any[], valueKey: string, models: string[]): any[] {
  const map: Record<string, any> = {}
  for (const r of rows) {
    if (!map[r.model]) map[r.model] = { model: r.model }
    map[r.model][r.language] = r[valueKey]
  }
  // Compute overall avg
  for (const m of Object.values(map)) {
    const vals = LANG_KEYS.map(l => m[l]).filter(v => v != null)
    m.overall = vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null
  }
  return models.filter(m => map[m]).map(m => map[m])
}

export default function FinalResults() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<TabId>('overview')

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/final_results.json`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const models = data?.models || []

  // Pivoted atomic MQM by language
  const atomicByLang = useMemo(() =>
    data?.atomic_mqm?.by_model_language ? pivotByLanguage(data.atomic_mqm.by_model_language, 'mqm_score', models) : []
  , [data, models])

  // Pivoted capability by language (gpt-4o judge)
  const capByLang = useMemo(() =>
    data?.capability_by_language ? pivotByLanguage(
      data.capability_by_language.filter((r: any) => r.judge === 'gpt-4o'),
      'all', models
    ) : []
  , [data, models])

  // Pivoted prompt ablation
  const ablationPivoted = useMemo(() => {
    if (!data?.prompt_ablation) return []
    const conditions = ['C1_native', 'C2_english', 'C2p_english_native_out']
    return conditions.map(cond => ({
      condition: cond,
      rows: pivotByLanguage(
        data.prompt_ablation.filter((r: any) => r.condition === cond),
        'mqm_score', models
      )
    }))
  }, [data, models])

  // CoT pivoted by experiment
  const cotPivoted = useMemo(() => {
    if (!data?.cot_comparison) return []
    const exps = ['capability', 'hallucination', 'active_admittance', 'inductance']
    return exps.map(exp => {
      const grouped: Record<string, any> = {}
      data.cot_comparison.filter((r: any) => r.experiment === exp).forEach((r: any) => {
        if (!grouped[r.model]) grouped[r.model] = { model: r.model, nc: [], cot: [], delta: [] }
        if (r.non_cot != null) grouped[r.model].nc.push(r.non_cot)
        if (r.cot != null) grouped[r.model].cot.push(r.cot)
        if (r.delta != null) grouped[r.model].delta.push(r.delta)
      })
      return {
        experiment: exp,
        rows: models.filter(m => grouped[m]).map(m => ({
          model: m,
          non_cot: grouped[m].nc.length ? grouped[m].nc.reduce((a: number, b: number) => a + b, 0) / grouped[m].nc.length : null,
          cot: grouped[m].cot.length ? grouped[m].cot.reduce((a: number, b: number) => a + b, 0) / grouped[m].cot.length : null,
          delta: grouped[m].delta.length ? grouped[m].delta.reduce((a: number, b: number) => a + b, 0) / grouped[m].delta.length : null,
        }))
      }
    })
  }, [data, models])

  // Pivoted atomic MQM transforms
  const atomicByTransform = useMemo(() => {
    if (!data?.atomic_mqm?.by_model_transform) return []
    const map: Record<string, any> = {}
    data.atomic_mqm.by_model_transform.forEach((r: any) => {
      if (!map[r.model]) map[r.model] = { model: r.model }
      map[r.model][r.transform] = r.mqm_score
    })
    return models.filter(m => map[m]).map(m => map[m])
  }, [data, models])

  const langCols = LANG_KEYS.map(k => ({ key: k, label: LANG_SHORT[k], fmt: fmtScore }))

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="animate-spin w-8 h-8 rounded-full border-2" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
    </div>
  )
  if (!data) return <div className="p-8" style={{ color: 'var(--m3-error)' }}>Failed to load results</div>

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <header className="px-6 h-14 flex items-center gap-4" style={{ borderBottom: '1px solid var(--m3-outline-variant)' }}>
        <Link to="/evaluation" className="text-xs font-medium px-2 py-1 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>← Back</Link>
        <h1 className="text-base font-semibold" style={{ color: 'var(--m3-on-surface)' }}>Final Results</h1>
        <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' }}>
          {models.length} models
        </span>
      </header>

      <div className="px-6 py-2 flex gap-1 flex-wrap" style={{ borderBottom: '1px solid var(--m3-outline-variant)', backgroundColor: 'var(--m3-surface-container-low)' }}>
        {TABS.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className="px-3 py-1.5 rounded-full text-xs font-medium transition-all"
            style={{
              backgroundColor: activeTab === tab.id ? 'var(--m3-primary)' : 'transparent',
              color: activeTab === tab.id ? 'var(--m3-on-primary)' : 'var(--m3-on-surface-variant)',
            }}>
            {tab.label}
          </button>
        ))}
      </div>

      <div className="p-6 max-w-7xl mx-auto">

        {activeTab === 'overview' && (<>
          <Section title="Overall Capability Leaderboard">
            <Table rows={data.capability} sortBy="avg" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
              { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
              { key: 'avg', label: 'Average', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="A-R-I Behavioural Profile">
            <Table rows={models.map(m => ({
              model: m,
              admittance: data.active_admittance.find((r: any) => r.model === m)?.avg,
              resistance: data.caption_bias.find((r: any) => r.model === m)?.avg,
              inductance: data.inductance.find((r: any) => r.model === m)?.avg,
            }))} columns={[
              { key: 'model', label: 'Model' },
              { key: 'admittance', label: 'Admittance (A)', fmt: fmtScore },
              { key: 'resistance', label: 'Resistance (R)', fmt: fmtScore },
              { key: 'inductance', label: 'Inductance (I)', fmt: fmtScore },
            ]} />
          </Section>
        </>)}

        {activeTab === 'atomic_mqm' && (<>
          <Section title="Atomic MQM by Language (Mistral Judge, Original)">
            <Table rows={atomicByLang} sortBy="overall" columns={[
              { key: 'model', label: 'Model' },
              ...langCols,
              { key: 'overall', label: 'Overall', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Atomic MQM by Transform (Mistral Judge)">
            <Table rows={atomicByTransform} sortBy="original" columns={[
              { key: 'model', label: 'Model' },
              { key: 'original', label: 'Original', fmt: fmtScore },
              { key: 'jpeg_compression', label: 'JPEG', fmt: fmtScore },
              { key: 'noise', label: 'Noise', fmt: fmtScore },
              { key: 'aspect_ratio', label: 'Aspect', fmt: fmtScore },
              { key: 'low_contrast', label: 'Low Con', fmt: fmtScore },
              { key: 'rotation', label: 'Rotation', fmt: fmtScore },
              { key: 'original_in_paper', label: 'In-Paper', fmt: fmtScore },
              { key: 'blurred_in_paper', label: 'Blur-Paper', fmt: fmtScore },
            ]} />
          </Section>
        </>)}

        {activeTab === 'transforms' && (
          <Section title="Transform MQM (Standard MQM, Avg of Both Judges)">
            <Table rows={data.transform_mqm} sortBy="original" columns={[
              { key: 'model', label: 'Model' },
              { key: 'original', label: 'Original', fmt: fmtScore },
              { key: 'jpeg_compression', label: 'JPEG', fmt: fmtScore },
              { key: 'noise', label: 'Noise', fmt: fmtScore },
              { key: 'aspect_ratio', label: 'Aspect', fmt: fmtScore },
              { key: 'low_contrast', label: 'Low Con', fmt: fmtScore },
              { key: 'rotation', label: 'Rotation', fmt: fmtScore },
              { key: 'original_in_paper', label: 'In-Paper', fmt: fmtScore },
              { key: 'blurred_in_paper', label: 'Blur-Paper', fmt: fmtScore },
            ]} />
          </Section>
        )}

        {activeTab === 'capability' && (<>
          <Section title="Capability (Overall)">
            <Table rows={data.capability} sortBy="avg" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
              { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
              { key: 'avg', label: 'Average', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Capability by Language (GPT-4o Judge)">
            <Table rows={capByLang} sortBy="overall" columns={[
              { key: 'model', label: 'Model' },
              ...langCols,
              { key: 'overall', label: 'Overall', fmt: fmtScore },
            ]} />
          </Section>
        </>)}

        {activeTab === 'resistance' && (<>
          <Section title="Caption Bias Resistance">
            <Table rows={data.caption_bias} sortBy="avg" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
              { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
              { key: 'avg', label: 'Average', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Prompt Reverse Consistency">
            <Table rows={data.prompt_reverse} sortBy="score" columns={[
              { key: 'model', label: 'Model' },
              { key: 'score', label: 'Score', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Hallucination Resistance">
            <Table rows={data.hallucination} sortBy="avg_overall" columns={[
              { key: 'model', label: 'Model' },
              { key: 'avg_overall', label: 'Overall', fmt: fmtScore },
              { key: 'avg_contra', label: 'Contra', fmt: fmtScore },
              { key: 'avg_inexist', label: 'Inexist', fmt: fmtScore },
              { key: 'avg_unanswerable', label: 'Unansw', fmt: fmtScore },
            ]} />
          </Section>
        </>)}

        {activeTab === 'admittance' && (<>
          <Section title="Active Admittance">
            <Table rows={data.active_admittance} sortBy="avg" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o_admittance', label: 'GPT-4o', fmt: fmtScore },
              { key: 'mistral-large-3_admittance', label: 'Mistral', fmt: fmtScore },
              { key: 'avg', label: 'Average', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Passive Admittance">
            <Table rows={data.passive_admittance} sortBy="gpt-4o_selective_blur" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o_axis_blurred', label: 'Axis (4o)', fmt: fmtScore },
              { key: 'gpt-4o_selective_blur', label: 'Select (4o)', fmt: fmtScore },
              { key: 'mistral-large-3_axis_blurred', label: 'Axis (Mis)', fmt: fmtScore },
              { key: 'mistral-large-3_selective_blur', label: 'Select (Mis)', fmt: fmtScore },
            ]} />
          </Section>
          <Section title="Inductance">
            <Table rows={data.inductance} sortBy="avg" columns={[
              { key: 'model', label: 'Model' },
              { key: 'gpt-4o_score', label: 'GPT-4o', fmt: fmtScore },
              { key: 'mistral-large-3_score', label: 'Mistral', fmt: fmtScore },
              { key: 'avg', label: 'Average', fmt: fmtScore },
            ]} />
          </Section>
        </>)}

        {activeTab === 'cot' && (<>
          {cotPivoted.map(({ experiment, rows }) => (
            <Section key={experiment} title={`CoT vs Non-CoT: ${experiment.replace(/_/g, ' ')}`}>
              <Table rows={rows} sortBy="delta" columns={[
                { key: 'model', label: 'Model' },
                { key: 'non_cot', label: 'Non-CoT', fmt: fmtScore },
                { key: 'cot', label: 'CoT', fmt: fmtScore },
                { key: 'delta', label: 'Δ', fmt: fmtDelta },
              ]} />
            </Section>
          ))}
        </>)}

        {activeTab === 'ablation' && (<>
          {ablationPivoted.map(({ condition, rows }) => (
            <Section key={condition} title={`Prompt Ablation: ${condition.replace(/_/g, ' ')}`}>
              <Table rows={rows} sortBy="overall" columns={[
                { key: 'model', label: 'Model' },
                ...langCols,
                { key: 'overall', label: 'Overall', fmt: fmtScore },
              ]} />
            </Section>
          ))}
        </>)}

      </div>
    </div>
  )
}
