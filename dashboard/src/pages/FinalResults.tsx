// @ts-nocheck
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../ThemeContext'

interface FinalResultsData {
  models: string[]
  judges: string[]
  capability: any[]
  caption_bias: any[]
  prompt_reverse: any[]
  hallucination: any[]
  passive_admittance: any[]
  active_admittance: any[]
  inductance: any[]
  transform_mqm: any[]
  atomic_mqm: { by_model_language: any[]; by_model_transform: any[] }
  capability_by_language: any[]
  cot_comparison: any[]
  prompt_ablation: any[]
}

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

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-8">
      <h3 className="text-sm font-semibold uppercase tracking-wider mb-4" style={{ color: 'var(--m3-on-surface-variant)' }}>{title}</h3>
      {children}
    </div>
  )
}

function LeaderboardTable({ rows, columns, sortBy }: { rows: any[]; columns: { key: string; label: string; fmt?: (v: any) => string }[]; sortBy?: string }) {
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
  const sign = n > 0 ? '+' : ''
  return `${sign}${n.toFixed(2)}`
}

export default function FinalResults() {
  const [data, setData] = useState<FinalResultsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<TabId>('overview')
  const { isDark } = useTheme()

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/final_results.json`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <div className="animate-spin w-8 h-8 rounded-full border-2" style={{ borderColor: 'var(--m3-outline-variant)', borderTopColor: 'transparent' }} />
    </div>
  )
  if (!data) return <div className="p-8" style={{ color: 'var(--m3-error)' }}>Failed to load results</div>

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--m3-surface)' }}>
      {/* Header */}
      <header className="px-6 h-14 flex items-center gap-4" style={{ borderBottom: '1px solid var(--m3-outline-variant)' }}>
        <Link to="/evaluation" className="text-xs font-medium px-2 py-1 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          ← Back
        </Link>
        <h1 className="text-base font-semibold" style={{ color: 'var(--m3-on-surface)' }}>Final Results</h1>
        <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: 'var(--m3-primary-container)', color: 'var(--m3-on-primary-container)' }}>
          {data.models.length} models
        </span>
      </header>

      {/* Tabs */}
      <div className="px-6 py-2 flex gap-1 flex-wrap" style={{ borderBottom: '1px solid var(--m3-outline-variant)', backgroundColor: 'var(--m3-surface-container-low)' }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="px-3 py-1.5 rounded-full text-xs font-medium transition-all"
            style={{
              backgroundColor: activeTab === tab.id ? 'var(--m3-primary)' : 'transparent',
              color: activeTab === tab.id ? 'var(--m3-on-primary)' : 'var(--m3-on-surface-variant)',
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-6 max-w-7xl mx-auto">

        {/* ====== OVERVIEW ====== */}
        {activeTab === 'overview' && (
          <>
            <Section title="Overall Leaderboard (Adversarial Subset, Avg of Both Judges)">
              <LeaderboardTable
                rows={data.capability}
                sortBy="avg"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'avg', label: 'Capability', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="A-R-I Behavioural Profile">
              <LeaderboardTable
                rows={data.models.map(m => {
                  const adm = data.active_admittance.find(r => r.model === m)
                  const cap = data.caption_bias.find(r => r.model === m)
                  const ind = data.inductance.find(r => r.model === m)
                  return {
                    model: m,
                    admittance: adm?.avg,
                    resistance: cap?.avg,
                    inductance: ind?.avg,
                  }
                })}
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'admittance', label: 'Admittance (A)', fmt: fmtScore },
                  { key: 'resistance', label: 'Resistance (R)', fmt: fmtScore },
                  { key: 'inductance', label: 'Inductance (I)', fmt: fmtScore },
                ]}
              />
            </Section>
          </>
        )}

        {/* ====== ATOMIC MQM ====== */}
        {activeTab === 'atomic_mqm' && (
          <>
            <Section title="Atomic MQM by Model and Language (Mistral Judge, Original)">
              <LeaderboardTable
                rows={data.atomic_mqm.by_model_language}
                sortBy="mqm_score"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'language', label: 'Language' },
                  { key: 'mqm_score', label: 'MQM', fmt: fmtScore },
                  { key: 'atom_accuracy', label: 'Atom Acc', fmt: fmtPct },
                  { key: 'atom_completeness', label: 'Atom Comp', fmt: fmtPct },
                  { key: 'n', label: 'N' },
                ]}
              />
            </Section>

            <Section title="Atomic MQM by Model and Transform (Mistral Judge)">
              <LeaderboardTable
                rows={data.atomic_mqm.by_model_transform}
                sortBy="mqm_score"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'transform', label: 'Transform' },
                  { key: 'mqm_score', label: 'MQM', fmt: fmtScore },
                  { key: 'atom_accuracy', label: 'Atom Acc', fmt: fmtPct },
                  { key: 'atom_completeness', label: 'Atom Comp', fmt: fmtPct },
                  { key: 'n', label: 'N' },
                ]}
              />
            </Section>
          </>
        )}

        {/* ====== TRANSFORMS ====== */}
        {activeTab === 'transforms' && (
          <Section title="Transform MQM (Standard MQM, Avg of Both Judges)">
            <LeaderboardTable
              rows={data.transform_mqm}
              sortBy="original"
              columns={[
                { key: 'model', label: 'Model' },
                { key: 'original', label: 'Original', fmt: fmtScore },
                { key: 'jpeg_compression', label: 'JPEG', fmt: fmtScore },
                { key: 'noise', label: 'Noise', fmt: fmtScore },
                { key: 'aspect_ratio', label: 'Aspect', fmt: fmtScore },
                { key: 'low_contrast', label: 'Low Con', fmt: fmtScore },
                { key: 'rotation', label: 'Rotation', fmt: fmtScore },
                { key: 'original_in_paper', label: 'In-Paper', fmt: fmtScore },
                { key: 'blurred_in_paper', label: 'Blur-Paper', fmt: fmtScore },
              ]}
            />
          </Section>
        )}

        {/* ====== CAPABILITY ====== */}
        {activeTab === 'capability' && (
          <>
            <Section title="Capability (Overall, Both Judges)">
              <LeaderboardTable
                rows={data.capability}
                sortBy="avg"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'gpt-4o', label: 'GPT-4o Judge', fmt: fmtScore },
                  { key: 'mistral-large-3', label: 'Mistral Judge', fmt: fmtScore },
                  { key: 'avg', label: 'Average', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="Capability by Language and Answer Type (GPT-4o Judge)">
              <LeaderboardTable
                rows={data.capability_by_language.filter(r => r.judge === 'gpt-4o')}
                sortBy="all"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'language', label: 'Language' },
                  { key: 'all', label: 'Overall', fmt: fmtScore },
                  { key: 'exact', label: 'Exact', fmt: fmtScore },
                  { key: 'approximate', label: 'Approx', fmt: fmtScore },
                  { key: 'open_ended', label: 'Open', fmt: fmtScore },
                ]}
              />
            </Section>
          </>
        )}

        {/* ====== RESISTANCE ====== */}
        {activeTab === 'resistance' && (
          <>
            <Section title="Caption Bias Resistance">
              <LeaderboardTable
                rows={data.caption_bias}
                sortBy="avg"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
                  { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
                  { key: 'avg', label: 'Average', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="Prompt Reverse Consistency">
              <LeaderboardTable
                rows={data.prompt_reverse}
                sortBy="score"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'score', label: 'Score', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="Hallucination Resistance">
              <LeaderboardTable
                rows={data.hallucination}
                sortBy="avg_overall"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'avg_overall', label: 'Overall', fmt: fmtScore },
                  { key: 'avg_contra', label: 'Contra', fmt: fmtScore },
                  { key: 'avg_inexist', label: 'Inexist', fmt: fmtScore },
                  { key: 'avg_unanswerable', label: 'Unansw', fmt: fmtScore },
                ]}
              />
            </Section>
          </>
        )}

        {/* ====== ADMITTANCE ====== */}
        {activeTab === 'admittance' && (
          <>
            <Section title="Active Admittance">
              <LeaderboardTable
                rows={data.active_admittance}
                sortBy="avg"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
                  { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
                  { key: 'avg', label: 'Average', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="Passive Admittance">
              <LeaderboardTable
                rows={data.passive_admittance}
                sortBy="gpt-4o_selective_blur"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'gpt-4o_axis_blurred', label: 'Axis (4o)', fmt: fmtScore },
                  { key: 'gpt-4o_selective_blur', label: 'Selective (4o)', fmt: fmtScore },
                  { key: 'mistral-large-3_axis_blurred', label: 'Axis (Mis)', fmt: fmtScore },
                  { key: 'mistral-large-3_selective_blur', label: 'Selective (Mis)', fmt: fmtScore },
                ]}
              />
            </Section>

            <Section title="Inductance">
              <LeaderboardTable
                rows={data.inductance}
                sortBy="avg"
                columns={[
                  { key: 'model', label: 'Model' },
                  { key: 'gpt-4o', label: 'GPT-4o', fmt: fmtScore },
                  { key: 'mistral-large-3', label: 'Mistral', fmt: fmtScore },
                  { key: 'avg', label: 'Average', fmt: fmtScore },
                ]}
              />
            </Section>
          </>
        )}

        {/* ====== COT ====== */}
        {activeTab === 'cot' && (
          <Section title="Chain-of-Thought vs Non-CoT (Avg of Both Judges)">
            <LeaderboardTable
              rows={(() => {
                const grouped: Record<string, any> = {}
                data.cot_comparison.forEach(r => {
                  const key = `${r.model}_${r.experiment}`
                  if (!grouped[key]) grouped[key] = { model: r.model, experiment: r.experiment, non_cot_vals: [], cot_vals: [], delta_vals: [] }
                  if (r.non_cot != null) grouped[key].non_cot_vals.push(r.non_cot)
                  if (r.cot != null) grouped[key].cot_vals.push(r.cot)
                  if (r.delta != null) grouped[key].delta_vals.push(r.delta)
                })
                return Object.values(grouped).map((g: any) => ({
                  model: g.model,
                  experiment: g.experiment,
                  non_cot: g.non_cot_vals.length ? (g.non_cot_vals.reduce((a: number, b: number) => a + b, 0) / g.non_cot_vals.length) : null,
                  cot: g.cot_vals.length ? (g.cot_vals.reduce((a: number, b: number) => a + b, 0) / g.cot_vals.length) : null,
                  delta: g.delta_vals.length ? (g.delta_vals.reduce((a: number, b: number) => a + b, 0) / g.delta_vals.length) : null,
                }))
              })()}
              columns={[
                { key: 'model', label: 'Model' },
                { key: 'experiment', label: 'Experiment' },
                { key: 'non_cot', label: 'Non-CoT', fmt: fmtScore },
                { key: 'cot', label: 'CoT', fmt: fmtScore },
                { key: 'delta', label: 'Δ', fmt: fmtDelta },
              ]}
            />
          </Section>
        )}

        {/* ====== PROMPT ABLATION ====== */}
        {activeTab === 'ablation' && (
          <Section title="Prompt-Language Ablation (Mistral Judge, Atomic MQM)">
            <LeaderboardTable
              rows={data.prompt_ablation}
              sortBy="mqm_score"
              columns={[
                { key: 'model', label: 'Model' },
                { key: 'condition', label: 'Condition' },
                { key: 'language', label: 'Language' },
                { key: 'mqm_score', label: 'MQM', fmt: fmtScore },
                { key: 'n', label: 'N' },
              ]}
            />
          </Section>
        )}

      </div>
    </div>
  )
}
