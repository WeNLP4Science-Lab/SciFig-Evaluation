import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

interface ResultRow {
  model: string
  [key: string]: unknown
}

interface Results {
  capability: ResultRow[]
  caption_bias: ResultRow[]
  prompt_reverse: ResultRow[]
  hallucination: ResultRow[]
  passive_admittance: ResultRow[]
  active_admittance: ResultRow[]
  transform_mqm: ResultRow[]
}

function ScoreCell({ value, good = 0.7, bad = 0.3 }: { value: unknown; good?: number; bad?: number }) {
  if (value == null) return <td className="px-3 py-2 text-xs" style={{ color: 'var(--m3-outline)' }}>—</td>
  const v = value as number
  const color = v >= good ? 'var(--m3-primary)' : v >= bad ? 'var(--m3-on-surface)' : 'var(--m3-error)'
  const weight = v >= good ? 600 : 400
  return <td className="px-3 py-2 text-xs tabular-nums" style={{ color, fontWeight: weight }}>{v.toFixed(2)}</td>
}

function IntCell({ value }: { value: unknown }) {
  if (value == null) return <td className="px-3 py-2 text-xs" style={{ color: 'var(--m3-outline)' }}>—</td>
  return <td className="px-3 py-2 text-xs tabular-nums" style={{ color: 'var(--m3-on-surface)' }}>{value as number}</td>
}

function Table({ title, headers, rows, renderRow }: { title: string; headers: string[]; rows: ResultRow[]; renderRow: (row: ResultRow) => React.ReactNode }) {
  return (
    <div className="mb-8">
      <h3 className="text-sm font-medium mb-3" style={{ color: 'var(--m3-on-surface)' }}>{title}</h3>
      <div className="overflow-x-auto rounded-lg" style={{ border: `1px solid var(--m3-outline-variant)` }}>
        <table className="w-full">
          <thead>
            <tr style={{ backgroundColor: 'var(--m3-surface-container-high)' }}>
              {headers.map(h => (
                <th key={h} className="px-3 py-2 text-[10px] font-medium uppercase text-left" style={{ color: 'var(--m3-outline)', letterSpacing: '0.5px' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={row.model} style={{ backgroundColor: i % 2 === 0 ? 'var(--m3-surface)' : 'var(--m3-surface-container)' }}>
                {renderRow(row)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function AdversarialResults() {
  const [data, setData] = useState<Results | null>(null)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/adversarial_results.json`)
      .then(r => r.json())
      .then(d => setData(d as Results))
      .catch(() => {})
  }, [])

  if (!data) return <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--m3-surface)' }}><p style={{ color: 'var(--m3-on-surface-variant)' }}>Loading...</p></div>

  return (
    <div className="min-h-screen animate-fade-in" style={{ backgroundColor: 'var(--m3-surface)' }}>
      <header className="px-6 py-4 flex items-center" style={{ borderBottom: `1px solid var(--m3-outline-variant)` }}>
        <Link to="/evaluation" className="flex items-center gap-1.5 text-xs font-medium m3-state-hover px-2 py-1.5 -ml-2 rounded-lg" style={{ color: 'var(--m3-on-surface-variant)' }}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5" /><path d="M12 19l-7-7 7-7" /></svg>
          Back
        </Link>
        <h1 className="ml-4 text-sm font-medium" style={{ color: 'var(--m3-on-surface)' }}>Adversarial Experiment Results</h1>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">

        <Table
          title="1. Capability Questions (12 models × 2 judges)"
          headers={['Model', 'gpt-4o', 'mistral', 'Average']}
          rows={data.capability}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['gpt-4o']} good={0.7} bad={0.4} />
            <ScoreCell value={row['mistral-large-3']} good={0.7} bad={0.4} />
            <ScoreCell value={row['avg']} good={0.7} bad={0.4} />
          </>)}
        />

        <Table
          title="2. Caption Bias Resistance (B/(A+B) — higher = more resistant to false captions)"
          headers={['Model', 'gpt-4o', 'mistral', 'Average']}
          rows={data.caption_bias}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['gpt-4o']} />
            <ScoreCell value={row['mistral-large-3']} />
            <ScoreCell value={row['avg']} />
          </>)}
        />

        <Table
          title="3. Prompt Reverse (sycophancy resistance — 1.0 = consistent, 0.0 = agrees with everything)"
          headers={['Model', 'Score', 'Correct', 'Reversed', 'Agrees Both']}
          rows={data.prompt_reverse}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['score']} />
            <IntCell value={row['correct_consistent']} />
            <IntCell value={row['reversed']} />
            <IntCell value={row['agrees_both']} />
          </>)}
        />

        <Table
          title="4. Hallucination Probes (gpt-4o judge — by probe type)"
          headers={['Model', 'Contra', 'Inexist', 'Unanswerable', 'Overall']}
          rows={data.hallucination}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['avg_contra']} />
            <ScoreCell value={row['avg_inexist']} />
            <ScoreCell value={row['avg_unanswerable']} />
            <ScoreCell value={row['avg_overall']} />
          </>)}
        />

        <Table
          title="5. Passive Admittance — Axis Blur (gpt-4o judge)"
          headers={['Model', 'Score', 'Admits', 'Fabricates', 'Silent']}
          rows={data.passive_admittance}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['gpt-4o_axis_blurred']} />
            <IntCell value={row['gpt-4o_axis_blurred_admits']} />
            <IntCell value={row['gpt-4o_axis_blurred_fabricates']} />
            <IntCell value={row['gpt-4o_axis_blurred_silent']} />
          </>)}
        />

        <Table
          title="6. Passive Admittance — Selective Blur (gpt-4o judge)"
          headers={['Model', 'Score', 'Admits', 'Fabricates', 'Silent']}
          rows={data.passive_admittance}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['gpt-4o_selective_blur']} />
            <IntCell value={row['gpt-4o_selective_blur_admits']} />
            <IntCell value={row['gpt-4o_selective_blur_fabricates']} />
            <IntCell value={row['gpt-4o_selective_blur_silent']} />
          </>)}
        />

        <Table
          title="7. Active Admittance (direct questions about blurred elements)"
          headers={['Model', 'gpt-4o', 'mistral', 'Average', 'Admits', 'Fab ✓', 'Fab ✗']}
          rows={data.active_admittance}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['gpt-4o_admittance']} />
            <ScoreCell value={row['mistral-large-3_admittance']} />
            <ScoreCell value={row['avg']} />
            <IntCell value={row['gpt-4o_admits']} />
            <IntCell value={row['gpt-4o_fab_correct']} />
            <IntCell value={row['gpt-4o_fab_incorrect']} />
          </>)}
        />

        <Table
          title="8. Transform MQM (gpt-4o judge — description quality under visual degradation)"
          headers={['Model', 'Original', 'JPEG', 'Noise', 'Aspect', 'Low Con.', 'Rotation', 'In-Paper', 'Blur IP']}
          rows={data.transform_mqm}
          renderRow={row => (<>
            <td className="px-3 py-2 text-xs font-mono" style={{ color: 'var(--m3-on-surface)' }}>{row.model}</td>
            <ScoreCell value={row['original']} good={70} bad={50} />
            <ScoreCell value={row['jpeg_compression']} good={70} bad={50} />
            <ScoreCell value={row['noise']} good={70} bad={50} />
            <ScoreCell value={row['aspect_ratio']} good={70} bad={50} />
            <ScoreCell value={row['low_contrast']} good={70} bad={50} />
            <ScoreCell value={row['rotation']} good={70} bad={50} />
            <ScoreCell value={row['original_in_paper']} good={70} bad={50} />
            <ScoreCell value={row['blurred_in_paper']} good={70} bad={50} />
          </>)}
        />

      </main>
    </div>
  )
}
