import { useState, useEffect, useRef } from 'react'
import {
  motion, useScroll, useTransform, useInView, useMotionValue, animate,
  AnimatePresence, LayoutGroup,
} from 'motion/react'
import DisconnectChart from '../components/landing/DisconnectChart'
import AriDumbbell from '../components/landing/AriDumbbell'
import ModelQuoteRail from '../components/landing/ModelQuoteRail'
import ThemeToggle from '../components/ThemeToggle'
import SciFigLogo from '../components/SciFigLogo'
import { useTheme } from '../theme'
import PaperFigure from '../components/landing/PaperFigure'
import GroupedBarChart from '../components/landing/GroupedBarChart'
import FigureProbeExplorer from '../components/landing/FigureProbeExplorer'
import { BENCHMARK_STATS, METHOD_CREDIBILITY } from '../data/landing_data'

const SPRING = { type: 'spring' as const, stiffness: 320, damping: 30, mass: 0.8 }

const c = {
  bg: 'var(--t-bg)',
  surface: 'var(--t-surface)',
  surfaceRaised: 'var(--t-surface-raised)',
  surfaceHover: 'var(--t-surface-hover)',
  border: 'var(--t-border)',
  borderStrong: 'var(--t-border-strong)',
  fg: 'var(--t-fg)',
  muted: 'var(--t-muted)',
  dim: 'var(--t-dim)',
  accent: 'var(--t-accent)',
}

interface NavSection { id: string; label: string }
const SECTIONS: NavSection[] = [
  { id: 'overview',    label: 'Overview' },
  { id: 'perception',  label: 'Perception' },
  { id: 'reasoning',   label: 'Reasoning' },
  { id: 'behaviour',   label: 'Behaviour' },
  { id: 'method',      label: 'Method' },
  { id: 'authors',     label: 'Authors' },
]

export default function Landing({ onExploreDataset }: { onExploreDataset: () => void }) {
  const [activeSection, setActiveSection] = useState('overview')

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(e => {
          if (e.isIntersecting) setActiveSection(e.target.id)
        })
      },
      { rootMargin: '-30% 0px -55% 0px' }
    )
    SECTIONS.forEach(s => {
      const el = document.getElementById(s.id)
      if (el) observer.observe(el)
    })
    return () => observer.disconnect()
  }, [])

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <div style={{ minHeight: '100vh', color: c.fg }}>
      <StickyNav
        active={activeSection}
        onJump={scrollTo}
        onExploreDataset={onExploreDataset}
      />

      <Hero onExploreDataset={onExploreDataset} />

      <Section id="overview" label="What we measure" subtitle="Three dimensions that benchmarks usually collapse into one.">
        <Overview />
      </Section>

      <Section id="perception" label="Perception & robustness" subtitle="Models describe scientific figures well — until the image is degraded.">
        <PerceptionSection />
      </Section>

      <Section id="reasoning" label="Reasoning" subtitle="Targeted capability questions widen the field — but barely hint at what comes next.">
        <ReasoningSection />
      </Section>

      <Section id="behaviour" label="The behaviour gap" subtitle="What models do when the evidence is missing or misleading.">
        <BehaviourSection onExploreDataset={onExploreDataset} />
      </Section>

      <Section id="method" label="Method credibility" subtitle="What backs these numbers up.">
        <MethodCredibility />
      </Section>

      <Section id="authors" label="Authors">
        <Authors />
      </Section>

      <Footer onExploreDataset={onExploreDataset} />
    </div>
  )
}

/* ── Sticky Nav ── */

function StickyNav({ active, onJump, onExploreDataset }: {
  active: string
  onJump: (id: string) => void
  onExploreDataset: () => void
}) {
  const { theme } = useTheme()
  const { scrollY } = useScroll()
  const bgOpacity = useTransform(scrollY, [0, 80], [0, 0.92])
  const borderOpacity = useTransform(scrollY, [0, 80], [0, 1])

  // Theme-aware glass colours
  const navBgRGB = theme === 'dark' ? '9,9,11' : '250,250,247'
  const navBorderRGB = theme === 'dark' ? '255,255,255' : '28,25,23'
  const baseBorderAlpha = theme === 'dark' ? 0.06 : 0.08

  return (
    <motion.nav
      style={{
        position: 'sticky', top: 0, zIndex: 30,
        background: useTransform(bgOpacity, v => `rgba(${navBgRGB},${v})`),
        borderBottom: useTransform(borderOpacity, v => `1px solid rgba(${navBorderRGB},${baseBorderAlpha * v})`),
        backdropFilter: 'blur(14px)',
      }}
    >
      <div style={{
        maxWidth: 1180, margin: '0 auto',
        padding: '14px 32px',
        display: 'flex', alignItems: 'center', gap: 28,
      }}>
        <motion.button
          onClick={() => onJump('overview')}
          whileHover={{ opacity: 0.85 }}
          style={{
            background: 'none', border: 'none', cursor: 'pointer',
            display: 'flex', alignItems: 'center', gap: 9,
            padding: 0, fontFamily: 'inherit',
            color: c.fg,
          }}
        >
          <SciFigLogo size={22} id="nav-logo" />
          <span style={{ fontSize: 13, fontWeight: 600, color: c.fg }}>
            SciFig-Eval
          </span>
        </motion.button>

        <LayoutGroup id="anchor-nav">
          <div style={{ flex: 1, display: 'flex', gap: 2, justifyContent: 'center' }}>
            {SECTIONS.map(s => {
              const isActive = active === s.id
              return (
                <motion.button
                  key={s.id}
                  onClick={() => onJump(s.id)}
                  whileTap={{ scale: 0.96 }}
                  transition={SPRING}
                  style={{
                    position: 'relative',
                    padding: '6px 12px', borderRadius: 6,
                    background: 'none', border: 'none', cursor: 'pointer',
                    fontFamily: 'inherit', fontSize: 12, fontWeight: 500,
                    zIndex: 1,
                  }}
                >
                  {isActive && (
                    <motion.span
                      layoutId="anchor-pill"
                      transition={SPRING}
                      style={{
                        position: 'absolute', inset: 0,
                        borderRadius: 6,
                        background: 'var(--t-overlay-medium)',
                        border: '1px solid var(--t-overlay-strong)',
                        zIndex: -1,
                      }}
                    />
                  )}
                  <motion.span
                    animate={{ color: isActive ? c.fg : c.muted }}
                    transition={{ duration: 0.18 }}
                  >
                    {s.label}
                  </motion.span>
                </motion.button>
              )
            })}
          </div>
        </LayoutGroup>

        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <NavCTA label="Paper" comingSoon />
          <NavCTA label="Dataset" onClick={onExploreDataset} primary />
        </div>
      </div>
    </motion.nav>
  )
}

function NavCTA({ label, primary, external, comingSoon, onClick }: {
  label: string; primary?: boolean; external?: boolean; comingSoon?: boolean; onClick?: () => void
}) {
  return (
    <motion.button
      onClick={comingSoon ? undefined : onClick}
      whileHover={comingSoon ? undefined : { y: -1 }}
      whileTap={comingSoon ? undefined : { scale: 0.95 }}
      transition={SPRING}
      style={{
        padding: '6px 14px', borderRadius: 7,
        fontFamily: 'inherit', fontSize: 12, fontWeight: 500,
        cursor: comingSoon ? 'default' : 'pointer',
        display: 'flex', alignItems: 'center', gap: 6,
        background: primary ? c.fg : 'transparent',
        color: primary ? c.bg : c.fg,
        border: primary ? 'none' : `1px solid ${c.borderStrong}`,
        opacity: comingSoon ? 0.55 : 1,
      }}
    >
      {label}
      {comingSoon && (
        <span style={{
          fontSize: 8.5, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.06em',
          padding: '2px 5px', borderRadius: 3,
          background: 'var(--t-overlay-medium)',
          border: '1px solid var(--t-overlay-strong)',
          lineHeight: 1,
        }}>
          Soon
        </span>
      )}
      {external && !comingSoon && (
        <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
          <path d="M3 9l6-6M5 3h4v4" />
        </svg>
      )}
    </motion.button>
  )
}

/* ── Hero ── */

function Hero({ onExploreDataset }: { onExploreDataset: () => void }) {
  const figs   = useCountUp(BENCHMARK_STATS.figures, 1.6)
  const models = useCountUp(BENCHMARK_STATS.models, 1.3)
  const evals  = useCountUp(BENCHMARK_STATS.total_evaluations, 1.9)

  return (
    <div style={{ position: 'relative', overflow: 'hidden', borderBottom: `1px solid ${c.border}` }}>
      <AuroraGlow />

      <div style={{
        position: 'relative',
        maxWidth: 1180, margin: '0 auto',
        padding: '120px 32px 24px',
        textAlign: 'center',
      }}>
        {/* Eyebrow — conceptual logo + wordmark */}
        <motion.div
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          style={{
            display: 'inline-flex', alignItems: 'center', gap: 9,
            margin: '0 0 28px',
            color: c.muted,
          }}
        >
          <SciFigLogo size={22} id="hero-logo" />
          <span style={{
            fontSize: 14, fontWeight: 500, color: c.fg,
            letterSpacing: '-0.005em',
          }}>
            SciFig-Eval
          </span>
        </motion.div>

        {/* Big centered headline */}
        <HeroHeadline text="How Do VLMs Behave When Blind or Misled?" />

        {/* Subhead */}
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.85, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          style={{
            fontSize: 'clamp(16px, 1.3vw, 19px)',
            color: c.muted, lineHeight: 1.55,
            margin: '32px auto 0', maxWidth: 720,
            fontWeight: 400,
          }}
        >
          Behavioural Evaluation of VLMs on Scientific Figures —{' '}
          <Num value={figs} /> figures, <Num value={models} /> frontier models,{' '}
          <Num value={evals} />+ evaluations.
        </motion.p>

        {/* Centered pill CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          style={{
            marginTop: 40,
            display: 'flex', gap: 14, justifyContent: 'center', alignItems: 'center',
            flexWrap: 'wrap',
          }}
        >
          <HeroCTA label="Start exploring" primary onClick={onExploreDataset} />
          <HeroCTA label="Read about the paper" arrow comingSoon />
        </motion.div>
      </div>

      {/* Model quote rail — sits under hero, partial overflow on the sides */}
      <div style={{
        position: 'relative',
        paddingTop: 64, paddingBottom: 72,
      }}>
        <ModelQuoteRail />
      </div>
    </div>
  )
}

function HeroHeadline({ text }: { text: string }) {
  const words = text.split(' ')
  return (
    <motion.h1
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.045, delayChildren: 0.15 } },
      }}
      style={{
        fontSize: 'clamp(42px, 6.6vw, 92px)',
        fontWeight: 700, letterSpacing: '-0.035em',
        color: c.fg, lineHeight: 1.0, margin: 0,
        display: 'flex', flexWrap: 'wrap', gap: '0.18em',
        justifyContent: 'center',
        maxWidth: 1080, marginInline: 'auto',
      }}
    >
      {words.map((w, i) => (
        <motion.span
          key={i}
          variants={{
            hidden: { opacity: 0, y: 28, filter: 'blur(10px)' },
            visible: {
              opacity: 1, y: 0, filter: 'blur(0px)',
              transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
            },
          }}
          style={{ display: 'inline-block', willChange: 'transform, opacity, filter' }}
        >
          {w}
        </motion.span>
      ))}
    </motion.h1>
  )
}

function HeroCTA({ label, primary, icon, arrow, comingSoon, onClick }: {
  label: string
  primary?: boolean
  icon?: 'grid' | 'paper' | 'code'
  arrow?: boolean
  comingSoon?: boolean
  onClick?: () => void
}) {
  return (
    <motion.button
      onClick={comingSoon ? undefined : onClick}
      whileHover={comingSoon ? undefined : { scale: 1.03 }}
      whileTap={comingSoon ? undefined : { scale: 0.97 }}
      transition={SPRING}
      style={{
        padding: primary ? '12px 24px' : '11px 20px',
        borderRadius: 999,
        fontFamily: 'inherit', fontSize: 14, fontWeight: 500,
        cursor: comingSoon ? 'default' : 'pointer',
        display: 'inline-flex', alignItems: 'center', gap: 8,
        background: primary ? c.fg : 'transparent',
        color: primary ? c.bg : c.fg,
        border: 'none',
        opacity: comingSoon ? 0.5 : 1,
      }}
    >
      <CTAIcon kind={icon} primary={primary} />
      {label}
      {arrow && (
        <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 4h7v7" />
          <path d="M5 11L12 4" />
        </svg>
      )}
      {comingSoon && (
        <span style={{
          fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
          letterSpacing: '0.08em',
          padding: '3px 8px', borderRadius: 999,
          background: 'var(--t-overlay-medium)',
          border: '1px solid var(--t-overlay-strong)',
          lineHeight: 1,
        }}>
          Soon
        </span>
      )}
    </motion.button>
  )
}

function CTAIcon({ kind, primary }: { kind?: 'grid' | 'paper' | 'code'; primary?: boolean }) {
  const stroke = primary ? c.bg : c.fg
  const props = { width: 13, height: 13, viewBox: '0 0 16 16', fill: 'none' as const, stroke, strokeWidth: 1.5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const }
  if (kind === 'grid') return (
    <svg {...props}>
      <rect x="2" y="2" width="5.5" height="5.5" rx="1" />
      <rect x="8.5" y="2" width="5.5" height="5.5" rx="1" />
      <rect x="2" y="8.5" width="5.5" height="5.5" rx="1" />
      <rect x="8.5" y="8.5" width="5.5" height="5.5" rx="1" />
    </svg>
  )
  if (kind === 'paper') return (
    <svg {...props}>
      <path d="M3 2h7l3 3v9H3z" />
      <path d="M10 2v3h3" />
      <path d="M5.5 9h5M5.5 11.5h3.5" />
    </svg>
  )
  if (kind === 'code') return (
    <svg {...props}>
      <path d="M6 4L2 8l4 4M10 4l4 4-4 4" />
    </svg>
  )
  return null
}

/* ── Aurora glow ── */

function AuroraGlow() {
  return (
    <>
      <motion.div
        animate={{ x: [0, 60, 0], y: [0, -20, 0] }}
        transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
        style={{
          position: 'absolute', top: -200, left: -100,
          width: 600, height: 600, borderRadius: '50%',
          background: 'radial-gradient(circle, var(--t-aurora-blue), transparent 65%)',
          filter: 'blur(60px)', pointerEvents: 'none',
        }}
      />
      <motion.div
        animate={{ x: [0, -50, 0], y: [0, 30, 0] }}
        transition={{ duration: 22, repeat: Infinity, ease: 'easeInOut' }}
        style={{
          position: 'absolute', top: -100, right: -150,
          width: 500, height: 500, borderRadius: '50%',
          background: 'radial-gradient(circle, var(--t-aurora-green), transparent 65%)',
          filter: 'blur(70px)', pointerEvents: 'none',
        }}
      />
    </>
  )
}

/* ── Section wrapper ── */

function Section({ id, label, subtitle, children }: {
  id: string; label: string; subtitle?: string; children: React.ReactNode
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  return (
    <section id={id} style={{ borderBottom: `1px solid ${c.border}`, scrollMarginTop: 64 }}>
      <div style={{ maxWidth: 1180, margin: '0 auto', padding: '80px 32px' }}>
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 18 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
        >
          <SectionHeading label={label} subtitle={subtitle} />
          {children}
        </motion.div>
      </div>
    </section>
  )
}

function SectionHeading({ label, subtitle }: { label: string; subtitle?: string }) {
  return (
    <div style={{ marginBottom: 40 }}>
      <h2 style={{
        fontSize: 'clamp(22px, 2.6vw, 30px)',
        fontWeight: 600, letterSpacing: '-0.02em',
        color: c.fg, lineHeight: 1.2, margin: 0,
      }}>
        {label}
      </h2>
      {subtitle && (
        <p style={{
          fontSize: 14.5, color: c.muted,
          marginTop: 10, lineHeight: 1.6, maxWidth: 680,
        }}>
          {subtitle}
        </p>
      )}
    </div>
  )
}

/* ── 01 · Overview ── */

function Overview() {
  const tiles = [
    {
      number: '01',
      label: 'Perception',
      heading: 'What does the model see?',
      body: 'MQM-scored open-ended descriptions of 250 figures, weighted by Accuracy, Completeness, and Clarity.',
      tag: 'measured today',
    },
    {
      number: '02',
      label: 'Reasoning',
      heading: 'Can it answer questions about what it sees?',
      body: '1,000 targeted capability questions spanning counting, computation, comparison, and pattern analysis.',
      tag: 'measured today',
    },
    {
      number: '03',
      label: 'Behaviour',
      heading: 'What does it do when evidence is missing or misleading?',
      body: 'The dimension benchmarks miss. We probe selective blur, false premises, and modified captions — surfacing failures invisible to accuracy scores.',
      tag: 'our contribution',
    },
  ]

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
      {tiles.map((t, i) => <NumberedTile key={t.number} {...t} index={i} />)}
    </div>
  )
}

function NumberedTile({ number, label, heading, body, tag, index }: {
  number: string; label: string; heading: string; body: string;
  tag?: string; index: number
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })
  const isContribution = tag === 'our contribution'

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 16 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.08, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -3 }}
      style={{
        position: 'relative',
        padding: '24px 22px 22px',
        borderRadius: 12,
        border: `1px solid ${isContribution ? 'rgba(59,130,246,0.25)' : c.border}`,
        background: isContribution
          ? 'linear-gradient(180deg, rgba(59,130,246,0.04), transparent 80%)'
          : c.surface,
        overflow: 'hidden',
      }}
    >
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginBottom: 16,
      }}>
        <span style={{
          fontSize: 11, fontWeight: 600,
          color: isContribution ? c.accent : c.muted,
          fontFamily: 'JetBrains Mono, monospace',
          letterSpacing: '0.05em',
        }}>
          {number}
        </span>
        {tag && (
          <span style={{
            fontSize: 9, fontWeight: 600, textTransform: 'uppercase',
            letterSpacing: '0.06em',
            padding: '3px 8px', borderRadius: 4,
            color: isContribution ? c.accent : c.dim,
            background: isContribution ? 'rgba(59,130,246,0.1)' : c.surfaceRaised,
            border: isContribution ? '1px solid rgba(59,130,246,0.2)' : `1px solid ${c.border}`,
            lineHeight: 1,
          }}>
            {tag}
          </span>
        )}
      </div>

      <p style={{
        fontSize: 11, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.06em', color: c.muted, margin: '0 0 6px',
      }}>
        {label}
      </p>
      <h3 style={{
        fontSize: 17, fontWeight: 600, color: c.fg,
        lineHeight: 1.35, margin: '0 0 12px',
        letterSpacing: '-0.01em',
      }}>
        {heading}
      </h3>
      <p style={{ fontSize: 13, color: c.muted, lineHeight: 1.6, margin: 0 }}>
        {body}
      </p>
    </motion.div>
  )
}

/* ── 02 · Perception ── */

function PerceptionSection() {
  return (
    <>
      <p style={{
        fontSize: 15, color: c.muted, lineHeight: 1.65,
        maxWidth: 780, margin: '0 0 32px',
      }}>
        GPT-5.2 leads with MQM <strong style={{ color: c.fg }}>91.6</strong>; Gemini 3.1 Pro follows at <strong style={{ color: c.fg }}>90.2</strong> — a 1.4-point gap.
        Rotation is the only perceptual transform that materially hurts top models;
        noise is essentially free; selective blur lives in between.
      </p>

      <PaperFigure
        src="/landing/degradation-1.png"
        alt="MQM trajectories across conditions for 8 models"
        label="Paper · Fig. 2"
        legend={[
          { abbr: 'Base',  full: 'Baseline (caption + original figure)' },
          { abbr: 'NoCap', full: 'Same figure, no caption provided' },
          { abbr: 'Noise', full: 'Gaussian noise overlay' },
          { abbr: 'Rot',   full: 'Rotation perturbation' },
          { abbr: 'LowC',  full: 'Low-contrast image' },
          { abbr: 'InPap', full: 'Figure embedded in its source PDF page' },
          { abbr: 'CapB',  full: 'Caption bias (caption contains false claims)' },
          { abbr: 'AdmB',  full: 'Admittance blur (unrecoverable element)' },
          { abbr: 'IndB',  full: 'Inductance blur (inferable element)' },
        ]}
        caption="MQM trajectories across evaluation conditions on a matched 100-figure subset. GPT-5.2 (blue), Gemini (green), and Phi-4 (red) are highlighted; remaining models are grey. Rotation drops MQM by ~20 points across all models. Caption-bias remains near baseline — confirming the MQM judge does not flag false claims, which makes our behavioural probes necessary."
        highlights={[
          'Rotation ↓ ~20 MQM pts',
          'Noise ≈ 0 pts',
          'Admittance blur ↓ 8–10 pts',
          'Inductance blur ↓ 1–3 pts',
        ]}
        background="light"
      />
    </>
  )
}

/* ── 03 · Reasoning ── */

function ReasoningSection() {
  return (
    <>
      <p style={{
        fontSize: 15, color: c.muted, lineHeight: 1.65,
        maxWidth: 780, margin: '0 0 28px',
      }}>
        1,000 capability questions across counting, computation, comparison, and pattern analysis.
        Gemini and GPT-5.2 dominate. The field stratifies cleanly — but the per-category breakdown shows
        complementary strengths within the top pair: Gemini wins on visual extraction, GPT-5.2 on derived computation.
      </p>

      <GroupedBarChart />

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-10% 0px' }}
        transition={{ duration: 0.45 }}
        style={{
          marginTop: 24,
          padding: '14px 18px',
          borderRadius: 8,
          background: 'rgba(59,130,246,0.05)',
          border: '1px solid rgba(59,130,246,0.18)',
        }}
      >
        <p style={{
          fontSize: 13, color: c.fg, lineHeight: 1.55, margin: 0,
        }}>
          <strong style={{ color: c.accent, fontWeight: 600 }}>→</strong>{' '}
          And yet, when we add stress — blurred labels, false premises, modified captions —
          the rankings look <em style={{ fontStyle: 'italic' }}>nothing</em> like this.
        </p>
      </motion.div>
    </>
  )
}

/* ── 04 · Behaviour ── */

function BehaviourSection({ onExploreDataset }: { onExploreDataset: () => void }) {
  return (
    <>
      <p style={{
        fontSize: 15, color: c.muted, lineHeight: 1.65,
        maxWidth: 780, margin: '0 0 32px',
      }}>
        We borrow loosely from circuit analysis to name how models{' '}
        <em style={{ fontStyle: 'italic' }}>handle</em>,{' '}
        <em style={{ fontStyle: 'italic' }}>reject</em>, and{' '}
        <em style={{ fontStyle: 'italic' }}>reconstruct</em> visual evidence.
        Each axis targets a distinct deployment risk.
      </p>

      {/* A-R-I tiles */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 48 }}>
        <AriTile
          letter="A"
          label="Admittance"
          color="#ef4444"
          heading="Does it acknowledge what it cannot see?"
          probe="Selective blur · 228 figs"
          index={0}
        />
        <AriTile
          letter="R"
          label="Resistance"
          color="#a855f7"
          heading="Does it push back against false premises?"
          probe="Inexist · contra · unanswerable · 750 probes"
          index={1}
        />
        <AriTile
          letter="I"
          label="Inductance"
          color="#22c55e"
          heading="Can it infer when context permits?"
          probe="Selective blur · 215 figs"
          index={2}
        />
      </div>

      {/* Figure Probe Explorer — one image, all 4 probe families, bar chart per probe */}
      <SubHeading label="Probe library" body="One figure, every probe family — see how all 8 models perform on each." />
      <FigureProbeExplorer onExploreDataset={onExploreDataset} />

      {/* The Disconnect */}
      <SubHeading label="The perception–behaviour disconnect" body="Same MQM score. Wildly different admittance rates." topMargin />
      <DisconnectChart />

      {/* A-R-I Dumbbell */}
      <SubHeading label="A-R-I profiles" body="Hover any model to compare its behaviour across all three axes." topMargin />
      <AriDumbbell />
    </>
  )
}

function SubHeading({ label, body, topMargin }: { label: string; body: string; topMargin?: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-10% 0px' }}
      transition={{ duration: 0.45 }}
      style={{ marginTop: topMargin ? 56 : 0, marginBottom: 18 }}
    >
      <p style={{
        fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.1em', color: c.accent,
        margin: '0 0 8px', lineHeight: 1,
      }}>
        {label}
      </p>
      <p style={{
        fontSize: 18, color: c.fg, margin: 0,
        fontWeight: 500, lineHeight: 1.4,
        letterSpacing: '-0.01em',
      }}>
        {body}
      </p>
    </motion.div>
  )
}

function AriTile({ letter, label, color, heading, probe, index }: {
  letter: string; label: string; color: string; heading: string; probe: string; index: number
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-15% 0px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 14 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.08, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -3 }}
      style={{
        position: 'relative',
        padding: '22px 20px 20px',
        borderRadius: 12,
        border: `1px solid ${c.border}`,
        background: c.surface,
        overflow: 'hidden',
      }}
    >
      <div style={{
        position: 'absolute', top: -10, right: -8,
        fontSize: 92, fontWeight: 700,
        color, opacity: 0.07,
        letterSpacing: '-0.04em', lineHeight: 1,
        pointerEvents: 'none',
      }}>
        {letter}
      </div>

      <p style={{
        position: 'relative',
        fontSize: 11, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.08em', color, margin: '0 0 8px',
      }}>
        {label}
      </p>
      <h3 style={{
        position: 'relative',
        fontSize: 15.5, fontWeight: 600, color: c.fg,
        lineHeight: 1.35, margin: '0 0 14px',
        letterSpacing: '-0.005em',
      }}>
        {heading}
      </h3>
      <p style={{
        position: 'relative',
        fontSize: 10.5, color: c.dim,
        fontFamily: 'JetBrains Mono, monospace',
        letterSpacing: '0.03em', margin: 0,
        paddingTop: 10, borderTop: `1px solid ${c.border}`,
      }}>
        {probe}
      </p>
    </motion.div>
  )
}

/* ── 05 · Method credibility ── */

function MethodCredibility() {
  const items = [
    { number: '01', label: 'Probe-designer ablation',  value: 'GPT-4o vs Mistral L3',  detail: 'Caption bias unchanged (.89); resistance δ = −0.16' },
    { number: '02', label: 'Cross-judge validation',   value: `ρ = ${METHOD_CREDIBILITY.cross_judge_rho.toFixed(3)}`,  detail: 'Model rankings preserved exactly (n = 344)' },
    { number: '03', label: 'Split-half reliability',   value: `ρ = ${METHOD_CREDIBILITY.split_half_rho.toFixed(3)}`,  detail: '100 random 125/125 splits over 250 figures' },
    { number: '04', label: 'Inter-annotator agreement', value: `α = ${METHOD_CREDIBILITY.krippendorff_alpha.toFixed(2)}`, detail: `Krippendorff's α on ${METHOD_CREDIBILITY.human_validation_pairs} pairs · 3 annotators` },
    { number: '05', label: 'Scale validation',         value: `σ ≤ ${METHOD_CREDIBILITY.scale_validation_max_deviation.toFixed(2)}`, detail: '100-figure subset matches 250-figure full set' },
  ]

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12 }}>
      {items.map((it, i) => <MethodTile key={it.number} {...it} index={i} />)}
    </div>
  )
}

function MethodTile({ number, label, value, detail, index }: {
  number: string; label: string; value: string; detail: string; index: number
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: '-10% 0px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 12 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.06, duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -2 }}
      style={{
        padding: 16,
        borderRadius: 10, border: `1px solid ${c.border}`,
        background: c.surface,
      }}
    >
      <span style={{
        fontSize: 10, fontWeight: 600,
        color: c.dim, fontFamily: 'JetBrains Mono, monospace',
      }}>
        {number}
      </span>
      <p style={{
        fontSize: 9.5, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.06em', color: c.muted,
        margin: '12px 0 8px', lineHeight: 1.3,
      }}>
        {label}
      </p>
      <p style={{
        fontSize: 18, fontWeight: 600, color: c.fg,
        margin: '0 0 8px', lineHeight: 1,
        fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.015em',
      }}>
        {value}
      </p>
      <p style={{
        fontSize: 11, color: c.dim, lineHeight: 1.5, margin: 0,
      }}>
        {detail}
      </p>
    </motion.div>
  )
}

/* ── 06 · Authors ── */

function Authors() {
  return (
    <div style={{
      padding: '32px 28px',
      borderRadius: 12, border: `1px solid ${c.border}`,
      background: c.surface,
      textAlign: 'center',
    }}>
      <p style={{
        fontSize: 11, fontWeight: 600, textTransform: 'uppercase',
        letterSpacing: '0.1em', color: c.muted,
        margin: '0 0 14px',
      }}>
        Anonymous · under review
      </p>
      <p style={{
        fontSize: 14, color: c.muted, lineHeight: 1.6,
        margin: 0, maxWidth: 540, marginInline: 'auto',
      }}>
        Author names, affiliations, acknowledgements, and funding statement will be revealed upon acceptance.
      </p>
    </div>
  )
}

/* ── Footer ── */

function Footer({ onExploreDataset }: { onExploreDataset: () => void }) {
  const [copied, setCopied] = useState(false)
  const bibtex = `@inproceedings{scifigeval,
  title     = {How Do VLMs Behave When Blind or Misled?
               Behavioural Evaluation of VLMs on Scientific Figures},
  author    = {Anonymous},
  booktitle = {Anonymous Submission, Under Review},
  year      = {2026},
}`

  const copyBibtex = async () => {
    try {
      await navigator.clipboard.writeText(bibtex)
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    } catch { /* noop */ }
  }

  return (
    <footer>
      <div style={{
        maxWidth: 1180, margin: '0 auto',
        padding: '64px 32px 48px',
      }}>
        <div style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40,
          alignItems: 'start', marginBottom: 40,
        }}>
          <div>
            <h3 style={{
              fontSize: 20, fontWeight: 600, color: c.fg,
              margin: '0 0 12px', letterSpacing: '-0.015em',
            }}>
              Want the full story?
            </h3>
            <p style={{
              fontSize: 14, color: c.muted, lineHeight: 1.6,
              margin: '0 0 20px', maxWidth: 440,
            }}>
              Read the paper for the complete methodology, ablations, error taxonomy, and per-model deep dives.
              Or browse every probe interactively.
            </p>
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <HeroCTA label="Explore the dataset" primary onClick={onExploreDataset} icon="grid" />
              <HeroCTA label="Read the paper" icon="paper" comingSoon />
            </div>
          </div>

          <div>
            <div style={{
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              marginBottom: 10,
            }}>
              <p style={{
                fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
                letterSpacing: '0.1em', color: c.dim, margin: 0,
              }}>
                Cite
              </p>
              <motion.button
                onClick={copyBibtex}
                whileTap={{ scale: 0.94 }}
                transition={SPRING}
                style={{
                  fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase',
                  letterSpacing: '0.06em',
                  padding: '4px 10px', borderRadius: 5,
                  background: copied ? 'rgba(34,197,94,0.12)' : c.surface,
                  color: copied ? '#22c55e' : c.muted,
                  border: `1px solid ${copied ? 'rgba(34,197,94,0.25)' : c.border}`,
                  cursor: 'pointer', fontFamily: 'inherit',
                  display: 'flex', alignItems: 'center', gap: 6,
                }}
              >
                {copied ? 'Copied' : 'Copy BibTeX'}
              </motion.button>
            </div>
            <pre style={{
              fontSize: 11, lineHeight: 1.65,
              color: c.muted, background: c.surface,
              padding: 16, borderRadius: 8,
              border: `1px solid ${c.border}`,
              fontFamily: 'JetBrains Mono, monospace',
              overflow: 'auto', margin: 0,
              whiteSpace: 'pre',
            }}>
              {bibtex}
            </pre>
          </div>
        </div>

        <div style={{
          paddingTop: 24, borderTop: `1px solid ${c.border}`,
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          fontSize: 11, color: c.dim,
        }}>
          <span>SciFig-Eval Benchmark</span>
          <span>Made with care for the research community.</span>
        </div>
      </div>
    </footer>
  )
}

/* ── Helpers ── */

function Num({ value }: { value: string }) {
  return (
    <span style={{
      color: c.fg, fontWeight: 600, fontVariantNumeric: 'tabular-nums',
    }}>{value}</span>
  )
}

function useCountUp(target: number, duration = 1.4): string {
  const mv = useMotionValue(0)
  const [display, setDisplay] = useState(0)
  useEffect(() => {
    if (target === 0) return
    const controls = animate(mv, target, {
      duration,
      ease: [0.22, 1, 0.36, 1],
      onUpdate: v => setDisplay(Math.round(v)),
    })
    return () => controls.stop()
  }, [target, duration, mv])
  return display.toLocaleString()
}
