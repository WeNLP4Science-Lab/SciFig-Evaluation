import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../ThemeContext'
import Reveal from 'reveal.js'
import 'reveal.js/dist/reveal.css'

/* Brand colours for model name text only */
const MODEL = {
  gpt: '#10A37F',
  claude: '#D97706',
  gemini: '#4285F4',
  gemma: '#E04E39',
  qwen: '#6366F1',
} as const

const FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

export default function Presentation() {
  const deckRef = useRef<HTMLDivElement>(null)
  const revealRef = useRef<Reveal | null>(null)
  const { isDark, toggleTheme, theme } = useTheme()
  const navigate = useNavigate()

  const bg = isDark ? '#121215' : '#FAFAFA'
  const fg = isDark ? '#E6E1E5' : '#1A1A2E'
  const fgMuted = isDark ? '#C8C5D0' : '#48464C'
  const accent = '#6750A4'
  const surface = isDark ? '#1E1E22' : '#FFFFFF'
  const border = isDark ? '#48464C' : '#C9C5D0'

  useEffect(() => {
    if (!deckRef.current) return

    const deck = new Reveal(deckRef.current, {
      hash: true,
      slideNumber: 'c/t',
      progress: true,
      controls: true,
      controlsTutorial: false,
      transition: 'fade',
      transitionSpeed: 'slow',
      backgroundTransition: 'fade',
      center: true,
      width: 1280,
      height: 720,
      margin: 0.06,
      minScale: 0.2,
      maxScale: 2.0,
    })

    deck.initialize()
    revealRef.current = deck

    return () => {
      try { deck.destroy() } catch { /* noop */ }
    }
  }, [])

  useEffect(() => {
    if (!deckRef.current) return
    const el = deckRef.current.querySelector('.slides') as HTMLElement | null
    if (el) el.style.color = fg
  }, [theme, fg])

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 9999, backgroundColor: bg }}>
      {/* Exit button */}
      <button
        onClick={() => navigate('/dataset/full')}
        style={{
          position: 'fixed', top: 16, left: 16, zIndex: 10000,
          width: 36, height: 36, borderRadius: '50%',
          border: `1px solid ${border}`, backgroundColor: surface,
          color: fg, cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 18, fontWeight: 300, opacity: 0.6, transition: 'opacity 200ms',
        }}
        onMouseEnter={e => { e.currentTarget.style.opacity = '1' }}
        onMouseLeave={e => { e.currentTarget.style.opacity = '0.6' }}
        title="Back to dashboard (Esc)"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>

      {/* Theme toggle */}
      <button
        onClick={toggleTheme}
        style={{
          position: 'fixed', top: 16, right: 16, zIndex: 10000,
          width: 36, height: 36, borderRadius: '50%',
          border: `1px solid ${border}`, backgroundColor: surface,
          color: fg, cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 16, opacity: 0.6, transition: 'opacity 200ms',
        }}
        onMouseEnter={e => { e.currentTarget.style.opacity = '1' }}
        onMouseLeave={e => { e.currentTarget.style.opacity = '0.6' }}
        title="Toggle theme"
      >
        {isDark ? (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        )}
      </button>

      {/* Reveal.js deck */}
      <div className="reveal" ref={deckRef} style={{ width: '100%', height: '100%', background: bg }}>
        <div className="slides" style={{ color: fg }}>

          {/* ---- SLIDE 1: Title ---- */}
          <section data-background-color={bg}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <div style={{ width: 48, height: 3, backgroundColor: accent, marginBottom: 48 }} />
              <h1 style={{
                fontSize: '1.8em', fontWeight: 800, letterSpacing: '-0.04em',
                color: fg, lineHeight: 1.15, maxWidth: '16em', textAlign: 'center', margin: '0 0 48px',
              }}>
                SciFig-Eval
              </h1>
              <p style={{
                fontSize: '0.72em', color: fgMuted, textAlign: 'center',
                lineHeight: 1.8, margin: 0, maxWidth: '28em',
              }}>
                A Multilingual Benchmark and Behavioural Framework<br />
                for Evaluating Vision-Language Models on Scientific Figures
              </p>
              <div style={{ marginTop: 48, textAlign: 'center', lineHeight: 2 }}>
                <div style={{ fontSize: '0.78em', fontWeight: 600, color: fg }}>Paul Osemudiame Oamen</div>
                <div style={{ fontSize: '0.62em', color: fgMuted }}>MSc Artificial Intelligence</div>
                <div style={{ fontSize: '0.62em', color: fgMuted }}>University of Aberdeen, 2026</div>
                <div style={{ fontSize: '0.58em', color: fgMuted, marginTop: 8 }}>
                  Supervisor: Dr Wei Zhao
                </div>
              </div>
            </div>
            <aside className="notes">
              Welcome. Today I present SciFig-Eval, a multilingual benchmark and behavioural framework for evaluating VLMs on scientific figures.
            </aside>
          </section>

          {/* ---- SLIDE 2: Where are VLMs deployed? ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 64px' }}>
              Where are VLMs being deployed today?
            </h2>
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr',
              gap: '48px 80px', maxWidth: '720px',
            }}>
              <div>
                <div style={{ fontSize: '1.4em', fontWeight: 700, color: fg }}>Consumer</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 8 }}>1.5B monthly Google Lens users</div>
              </div>
              <div>
                <div style={{ fontSize: '1.4em', fontWeight: 700, color: fg }}>Enterprise</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 8 }}>Microsoft Copilot across Office suite</div>
              </div>
              <div>
                <div style={{ fontSize: '1.4em', fontWeight: 700, color: fg }}>Healthcare</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 8 }}>950 FDA-approved AI/ML devices</div>
              </div>
              <div>
                <div style={{ fontSize: '1.4em', fontWeight: 700, color: fg }}>Autonomous</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 8 }}>Waymo: 71M rider-only miles driven</div>
              </div>
            </div>
            <aside className="notes">
              VLMs are everywhere. Billions of users interact with them daily across consumer, enterprise, healthcare, and autonomous systems.
            </aside>
          </section>

          {/* ---- SLIDE 3: Entering scientific research ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 64px' }}>
              How are they entering scientific research?
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 32, maxWidth: '640px' }}>
              <div>
                <div style={{ fontSize: '1.1em', fontWeight: 700, color: fg }}>Claude for Research</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 6 }}>Physicist completed a theoretical paper in 2 weeks</div>
              </div>
              <div>
                <div style={{ fontSize: '1.1em', fontWeight: 700, color: fg }}>Google Deep Research</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 6 }}>Agentic research with Gemini, generates charts inline</div>
              </div>
              <div>
                <div style={{ fontSize: '1.1em', fontWeight: 700, color: fg }}>OpenAI Deep Research</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 6 }}>Searches hundreds of sources, produces cited reports</div>
              </div>
              <div>
                <div style={{ fontSize: '1.1em', fontWeight: 700, color: fg }}>Elicit / Semantic Scholar</div>
                <div style={{ fontSize: '0.62em', color: fgMuted, marginTop: 6 }}>AI tools summarising research papers with figures</div>
              </div>
            </div>
            <aside className="notes">
              Scientific figures encode core quantitative arguments. When an AI reads a figure for a researcher, it needs to get it right.
            </aside>
          </section>

          {/* ---- SLIDE 4: Why isn't accuracy enough? (Tesla case) ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 48px' }}>
              Why isn't accuracy enough?
            </h2>
            <blockquote style={{
              fontSize: '1.1em', fontStyle: 'italic', color: fg, fontWeight: 400,
              lineHeight: 1.6, maxWidth: '20em', margin: '0 0 48px',
              borderLeft: `3px solid ${accent}`, paddingLeft: 24,
            }}>
              "Did not provide alerts when camera performance had deteriorated."
            </blockquote>
            <div style={{ fontSize: '0.62em', color: fgMuted, letterSpacing: '0.04em', marginBottom: 32 }}>
              -- NHTSA Investigation EA26002
            </div>
            <div style={{ fontSize: '0.78em', color: fg, fontWeight: 600 }}>
              9 crashes. 1 fatality. 3.2M vehicles under investigation.
            </div>
            <aside className="notes">
              The Tesla case demonstrates that a system performing well under normal conditions but failing silently under adverse conditions is dangerous. The same principle applies to VLMs reading scientific figures.
            </aside>
          </section>

          {/* ---- SLIDE 5A: Sunburst figure ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '1.8em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 28px' }}>
              Do current models actually fail this way?
            </h2>
            <div style={{ display: 'flex', gap: 32, alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <img src="/figures/multi_language/multi_fig_004.png" alt="Original sunburst" style={{ height: 320, borderRadius: 4, border: `1px solid ${border}` }} />
                <div style={{ fontSize: '0.55em', color: fgMuted, marginTop: 8 }}>Original</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <img src="/figures/adversarial/multi_language/multi_fig_004/selective_blur.png" alt="Selectively blurred" style={{ height: 320, borderRadius: 4, border: `1px solid ${border}` }} />
                <div style={{ fontSize: '0.55em', color: fgMuted, marginTop: 8 }}>Selective blur</div>
              </div>
            </div>
            <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 24, textAlign: 'center', maxWidth: '36em', margin: '24px auto 0' }}>
              One label blurred. We ask: what category sits between Movie Characters and Novel Characters?
            </div>
            <aside className="notes">
              This is the sunburst figure. We selectively blur one label and ask all models what it says.
            </aside>
          </section>

          {/* ---- SLIDE 5B: GPT-5.2 response ---- */}
          <section data-background-color={bg}>
            <blockquote style={{
              fontSize: '2.2em', fontStyle: 'italic', color: fg, fontWeight: 400,
              lineHeight: 1.4, maxWidth: '14em', margin: '80px 0 40px',
              borderLeft: `3px solid ${MODEL.gpt}`, paddingLeft: 32,
            }}>
              "Anime Characters."
            </blockquote>
            <div style={{ fontSize: '0.72em', color: fgMuted, maxWidth: '28em', lineHeight: 1.6 }}>
              <span style={{ color: MODEL.gpt, fontWeight: 600 }}>GPT-5.2</span> -- Full fabrication. No mention of blur.
            </div>
            <aside className="notes">
              GPT-5.2 invents a completely wrong answer with zero hedging.
            </aside>
          </section>

          {/* ---- SLIDE 5C: Claude response ---- */}
          <section data-background-color={bg}>
            <blockquote style={{
              fontSize: '1.8em', fontStyle: 'italic', color: fg, fontWeight: 400,
              lineHeight: 1.4, maxWidth: '16em', margin: '80px 0 40px',
              borderLeft: `3px solid ${MODEL.claude}`, paddingLeft: 32,
            }}>
              "TV Characters (partially visible as 'aracters')"
            </blockquote>
            <div style={{ fontSize: '0.72em', color: fgMuted, maxWidth: '28em', lineHeight: 1.6 }}>
              <span style={{ color: MODEL.claude, fontWeight: 600 }}>Claude Opus 4.6</span> -- Partial admittance. Still wrong.
            </div>
            <aside className="notes">
              Claude acknowledges partial visibility but still guesses wrong.
            </aside>
          </section>

          {/* ---- SLIDE 5D: Gemini response ---- */}
          <section data-background-color={bg}>
            <blockquote style={{
              fontSize: '1.6em', fontStyle: 'italic', color: fg, fontWeight: 400,
              lineHeight: 1.4, maxWidth: '18em', margin: '80px 0 40px',
              borderLeft: `3px solid ${MODEL.gemini}`, paddingLeft: 32,
            }}>
              "The label is partially obscured. Only 'aracters' is visible."
            </blockquote>
            <div style={{ fontSize: '0.72em', color: fgMuted, maxWidth: '28em', lineHeight: 1.6 }}>
              <span style={{ color: MODEL.gemini, fontWeight: 600 }}>Gemini 3.1 Pro</span> -- Full admittance. Reports only what it can see.
            </div>
            <aside className="notes">
              Gemini admits it cannot read the label and reports only what is visible. This is the trustworthy behaviour.
            </aside>
          </section>

          {/* ---- SLIDE 6: Research questions ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 56px' }}>
              What did we investigate?
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 28, maxWidth: '640px' }}>
              {[
                { rq: 'RQ1', q: 'How accurately do 13 frontier VLMs describe scientific figures across 4 languages?' },
                { rq: 'RQ2', q: 'How does visual degradation affect description quality?' },
                { rq: 'RQ3', q: 'Can models comprehend figures beyond description?' },
                { rq: 'RQ4', q: 'What are the behavioural profiles of VLMs under adversarial conditions?' },
              ].map((item, i) => (
                <div key={i} style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
                  <span style={{
                    fontSize: '1.4em', fontWeight: 800, color: accent,
                    flexShrink: 0, width: '2.4em',
                  }}>{item.rq}</span>
                  <span style={{ fontSize: '0.72em', color: fgMuted, lineHeight: 1.5 }}>{item.q}</span>
                </div>
              ))}
            </div>
            <aside className="notes">
              Four research questions spanning accuracy, robustness, comprehension, and behaviour.
            </aside>
          </section>

          {/* ---- SLIDE 7: Contributions ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 56px' }}>
              What are we contributing to knowledge?
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 36, maxWidth: '640px' }}>
              <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
                <span style={{ fontSize: '1.2em', fontWeight: 800, color: accent, flexShrink: 0 }}>C1</span>
                <span style={{ fontSize: '0.72em', color: fgMuted, lineHeight: 1.5 }}>
                  A multilingual benchmark of 1,005 scientific figures with expert annotations across 4 languages.
                </span>
              </div>
              <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
                <span style={{ fontSize: '1.2em', fontWeight: 800, color: accent, flexShrink: 0 }}>C2</span>
                <span style={{ fontSize: '0.72em', color: fgMuted, lineHeight: 1.5 }}>
                  The A-R-I behavioural framework for measuring admittance, resistance, and inductance.
                </span>
              </div>
              <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
                <span style={{ fontSize: '1.2em', fontWeight: 800, color: accent, flexShrink: 0 }}>C3</span>
                <span style={{ fontSize: '0.72em', color: fgMuted, lineHeight: 1.5 }}>
                  A 13-model empirical evaluation revealing that behavioural profiles diverge sharply from accuracy rankings.
                </span>
              </div>
            </div>
            <aside className="notes">
              Three contributions: the benchmark, the framework, and the evaluation.
            </aside>
          </section>

          {/* ---- SLIDE 8: Benchmark at a glance ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 48px' }}>
              How did we build the benchmark?
            </h2>
            <div style={{ fontSize: '5em', fontWeight: 800, color: accent, lineHeight: 1 }}>
              1,005
            </div>
            <div style={{ fontSize: '0.82em', color: fgMuted, marginTop: 12, marginBottom: 48 }}>
              scientific figures
            </div>
            <div style={{ display: 'flex', gap: 64, fontSize: '0.72em', color: fgMuted }}>
              <div>
                <span style={{ fontWeight: 700, color: fg }}>349</span> papers
              </div>
              <div>
                <span style={{ fontWeight: 700, color: fg }}>4</span> languages
              </div>
              <div>
                <span style={{ fontWeight: 700, color: fg }}>1,411</span> annotations
              </div>
              <div>
                <span style={{ fontWeight: 700, color: fg }}>45</span> adversarial figures
              </div>
            </div>
            <aside className="notes">
              The benchmark comprises 1,005 figures across four languages from native venues, not translated templates.
            </aside>
          </section>

          {/* ---- SLIDE 9: A-R-I framework ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 56px' }}>
              How do we measure behaviour?
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 36, maxWidth: '640px' }}>
              <div>
                <div style={{ fontSize: '1.6em', fontWeight: 800, color: accent }}>Admittance</div>
                <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 8 }}>Does the model admit when it cannot read something?</div>
              </div>
              <div>
                <div style={{ fontSize: '1.6em', fontWeight: 800, color: fg }}>Resistance</div>
                <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 8 }}>Does the model push back when given false information?</div>
              </div>
              <div>
                <div style={{ fontSize: '1.6em', fontWeight: 800, color: fg }}>Inductance</div>
                <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 8 }}>Can the model reason about what is missing from context?</div>
              </div>
            </div>
            <aside className="notes">
              The A-R-I framework measures three behavioural axes. Only Admittance gets the accent colour because it is the primary axis.
            </aside>
          </section>

          {/* ---- SLIDE 10: Evaluation setup ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 56px' }}>
              How did we run the evaluation?
            </h2>
            <div style={{ fontSize: '2em', fontWeight: 700, color: fg, lineHeight: 1.6 }}>
              13 models <span style={{ color: fgMuted, fontWeight: 400 }}>x</span> 2 judges <span style={{ color: fgMuted, fontWeight: 400 }}>x</span> 3 configurations
            </div>
            <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 32, lineHeight: 1.8, maxWidth: '36em' }}>
              Temperature = 0, structured prompts, 4 languages.<br />
              MQM evaluation with atomic fact checking and severity-capped penalties.<br />
              Human validation: ICC = .91, system-level rho greater than .95.
            </div>
            <aside className="notes">
              Three-stage pipeline: generation, MQM evaluation with dual judges, and results analysis.
            </aside>
          </section>

          {/* ---- SLIDE 11: RQ1 -- Description quality ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 40px' }}>
              How well do models describe figures?
            </h2>
            <div style={{ display: 'flex', gap: 80, alignItems: 'flex-start' }}>
              <div>
                <div style={{ fontSize: '5em', fontWeight: 800, color: accent, lineHeight: 1 }}>75.5</div>
                <div style={{ fontSize: '0.72em', color: fgMuted, marginTop: 8 }}>
                  GPT-5.2 MQM score
                </div>
              </div>
              <div style={{ paddingTop: 8 }}>
                <table style={{ borderCollapse: 'collapse', fontSize: '0.68em', lineHeight: 1.8 }}>
                  <thead>
                    <tr>
                      <th style={{ borderTop: `2px solid ${fg}`, borderBottom: `1px solid ${fg}`, padding: '6px 20px 6px 0', textAlign: 'left', fontWeight: 700, color: fg }}>Model</th>
                      <th style={{ borderTop: `2px solid ${fg}`, borderBottom: `1px solid ${fg}`, padding: '6px 20px', textAlign: 'right', fontWeight: 700, color: fg }}>MQM</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[
                      { model: 'GPT-5.2', score: '75.5', color: MODEL.gpt },
                      { model: 'Gemini 3.1 Pro', score: '73.8', color: MODEL.gemini },
                      { model: 'Claude Opus 4.6', score: '72.1', color: MODEL.claude },
                      { model: 'Qwen-235B', score: '70.9', color: MODEL.qwen },
                      { model: 'Qwen-32B', score: '68.4', color: MODEL.qwen },
                      { model: 'Gemma-27B', score: '58.2', color: MODEL.gemma },
                    ].map((r, i, arr) => (
                      <tr key={i}>
                        <td style={{
                          padding: '4px 20px 4px 0', color: r.color, fontWeight: 600,
                          borderBottom: i === arr.length - 1 ? `2px solid ${fg}` : `1px solid ${border}`,
                        }}>{r.model}</td>
                        <td style={{
                          padding: '4px 20px', textAlign: 'right', color: fg,
                          borderBottom: i === arr.length - 1 ? `2px solid ${fg}` : `1px solid ${border}`,
                        }}>{r.score}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 32 }}>
              The top 4 models cluster within 5 points.
            </div>
            <aside className="notes">
              GPT-5.2 leads but the top tier is tightly clustered. Numerical precision is the dominant error category.
            </aside>
          </section>

          {/* ---- SLIDE 12: RQ2 -- Robustness ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 48px' }}>
              How robust are they under degradation?
            </h2>
            <div style={{ fontSize: '1.3em', fontWeight: 700, color: fg, lineHeight: 1.5, maxWidth: '18em' }}>
              Robustness is independent of clean-condition accuracy.
            </div>
            <div style={{ fontSize: '0.72em', color: fgMuted, marginTop: 24, lineHeight: 1.8, maxWidth: '36em' }}>
              <span style={{ color: MODEL.qwen, fontWeight: 600 }}>Qwen-235B</span> is most robust (slope = 1.6), not GPT-5.2.<br />
              Rotation (-8.2) and low contrast (-7.1) cause the largest drops.<br />
              <span style={{ color: MODEL.gemini, fontWeight: 600 }}>Gemini</span> extracts contextual cues from page context (+5.7 with original-in-paper).
            </div>
            <aside className="notes">
              Rotation and low contrast cause the largest drops. Critically, robustness is independent of clean-condition accuracy.
            </aside>
          </section>

          {/* ---- SLIDE 13: RQ3 -- Comprehension ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 48px' }}>
              Can they comprehend beyond description?
            </h2>
            <div style={{ display: 'flex', gap: 48, alignItems: 'baseline' }}>
              <div>
                <div style={{ fontSize: '4em', fontWeight: 800, color: MODEL.gemini, lineHeight: 1 }}>.81</div>
                <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 8 }}>Gemini</div>
              </div>
              <div>
                <div style={{ fontSize: '4em', fontWeight: 800, color: MODEL.gpt, lineHeight: 1 }}>.78</div>
                <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 8 }}>GPT-5.2</div>
              </div>
            </div>
            <div style={{ fontSize: '0.82em', color: fg, fontWeight: 600, marginTop: 40, maxWidth: '28em' }}>
              Comprehension does not equal description.
            </div>
            <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 12, maxWidth: '36em', lineHeight: 1.6 }}>
              Gemini overtakes GPT-5.2 in comprehension tasks despite ranking lower on description quality.
            </div>
            <aside className="notes">
              Gemini leads comprehension, overtaking GPT-5.2. Description and comprehension are partially dissociated.
            </aside>
          </section>

          {/* ---- SLIDE 14A: Behavioural profiles -- GPT resistance gap ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 48px' }}>
              What do their behavioural profiles reveal?
            </h2>
            <div style={{ fontSize: '5em', fontWeight: 800, color: accent, lineHeight: 1 }}>.56</div>
            <div style={{ fontSize: '0.78em', color: fgMuted, marginTop: 12 }}>
              <span style={{ color: MODEL.gpt, fontWeight: 600 }}>GPT-5.2</span> resistance to false premises
            </div>
            <div style={{ fontSize: '0.68em', color: fgMuted, marginTop: 24, maxWidth: '32em', lineHeight: 1.6 }}>
              Leads accuracy but accepts false premises. Builds elaborate analyses on wrong data.
            </div>
            <aside className="notes">
              GPT-5.2 leads accuracy but has a significant resistance gap.
            </aside>
          </section>

          {/* ---- SLIDE 14B: Gemma silent fabrication ---- */}
          <section data-background-color={bg}>
            <div style={{ fontSize: '1.6em', fontWeight: 700, color: fg, lineHeight: 1.4, maxWidth: '16em', marginBottom: 40 }}>
              Near-zero admittance<br />at <span style={{ color: accent }}>all</span> scales.
            </div>
            <div style={{ fontSize: '0.78em', color: fgMuted, lineHeight: 1.6, maxWidth: '32em' }}>
              <span style={{ color: MODEL.gemma, fontWeight: 600 }}>Gemma</span> -- 4B, 12B, 27B -- scaling improves accuracy but not behavioural trustworthiness. The model never admits uncertainty regardless of parameter count.
            </div>
            <aside className="notes">
              Gemma fabricates at all scales. Scaling does not fix behavioural problems.
            </aside>
          </section>

          {/* ---- SLIDE 14C: The callback ---- */}
          <section data-background-color={bg}>
            <div style={{ fontSize: '1.6em', fontWeight: 700, color: fg, lineHeight: 1.5, maxWidth: '18em', marginBottom: 48 }}>
              Accuracy benchmarks cannot detect this.
            </div>
            <div style={{ fontSize: '1.6em', fontWeight: 700, color: accent, lineHeight: 1.5, maxWidth: '18em' }}>
              A-R-I can.
            </div>
            <aside className="notes">
              This is the key takeaway: accuracy metrics alone miss critical behavioural differences that A-R-I reveals.
            </aside>
          </section>

          {/* ---- SLIDE 15: What does this all mean? ---- */}
          <section data-background-color={bg}>
            <h2 style={{ fontSize: '2.4em', fontWeight: 800, letterSpacing: '-0.03em', color: fg, margin: '0 0 56px' }}>
              What does this all mean?
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 32, maxWidth: '640px' }}>
              <div style={{ fontSize: '0.78em', color: fg, lineHeight: 1.6 }}>
                SciFig-Eval fills the multilingual behavioural evaluation gap that no existing benchmark addresses.
              </div>
              <div style={{ fontSize: '0.78em', color: fg, lineHeight: 1.6 }}>
                A-R-I reveals failure modes invisible to accuracy metrics.
              </div>
              <div style={{ fontSize: '0.78em', color: fg, lineHeight: 1.6 }}>
                Trustworthy deployment requires behavioural profiling -- not just accuracy measurement.
              </div>
            </div>
            <aside className="notes">
              Revisit the three contributions with evidence. Behavioural profiling is essential for trustworthy deployment.
            </aside>
          </section>

          {/* ---- SLIDE 16: Thank You ---- */}
          <section data-background-color={bg}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <div style={{ width: 48, height: 3, backgroundColor: accent, marginBottom: 48 }} />
              <h2 style={{ fontSize: '3em', fontWeight: 800, letterSpacing: '-0.04em', color: fg, margin: '0 0 16px' }}>
                Thank You
              </h2>
              <div style={{ fontSize: '0.82em', color: fgMuted, fontStyle: 'italic', marginBottom: 48 }}>
                Soli Deo Gloria
              </div>
              <div style={{ fontSize: '0.68em', color: fgMuted, lineHeight: 1.8, textAlign: 'center', marginBottom: 40 }}>
                Thank you to Dr Wei Zhao, the annotation team,<br />
                and the Department of Computing Science.
              </div>
              <div style={{ display: 'flex', gap: 48, fontSize: '0.58em', color: fgMuted }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontWeight: 700, color: fg, marginBottom: 4 }}>Dashboard</div>
                  <div style={{ fontFamily: 'monospace', color: accent, fontSize: '0.9em' }}>
                    victorious-glacier-00483810f.2.azurestaticapps.net
                  </div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontWeight: 700, color: fg, marginBottom: 4 }}>Code</div>
                  <div style={{ fontFamily: 'monospace', color: accent, fontSize: '0.9em' }}>
                    github.com/WeNLP4Science-Lab/SciFig-Evaluation
                  </div>
                </div>
              </div>
            </div>
            <aside className="notes">
              Thank you. Questions welcome.
            </aside>
          </section>

        </div>
      </div>

      {/* Reveal.js style overrides */}
      <style>{`
        .reveal {
          font-family: ${FONT} !important;
        }
        .reveal .slides {
          text-align: left !important;
        }
        .reveal .slides section {
          padding: 48px 64px !important;
        }
        .reveal .controls {
          color: ${accent} !important;
        }
        .reveal .progress {
          height: 2px !important;
          color: ${accent} !important;
        }
        .reveal .progress span {
          background: ${accent} !important;
        }
        .reveal .slide-number {
          font-family: ${FONT} !important;
          font-size: 11px !important;
          color: ${fgMuted} !important;
          background: transparent !important;
          right: 16px !important;
          bottom: 12px !important;
        }
        .reveal .controls button {
          color: ${accent} !important;
        }
        .reveal section .fragment {
          transition: opacity 0.4s ease, transform 0.4s ease !important;
        }
        .reveal section .fragment:not(.visible) {
          opacity: 0 !important;
          transform: translateY(8px) !important;
        }
        .reveal section .fragment.visible {
          opacity: 1 !important;
          transform: translateY(0) !important;
        }
      `}</style>
    </div>
  )
}
