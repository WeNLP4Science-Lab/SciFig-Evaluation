import { useState } from 'react'
import { ANNOTATORS, loginAPI, saveAuth, type Annotator, type AuthState } from '../auth'

const c = {
  bg: 'var(--t-bg)', surface: 'var(--t-surface)', border: 'var(--t-border)',
  borderStrong: 'var(--t-border-strong)', fg: 'var(--t-fg)', muted: 'var(--t-muted)',
  dim: 'var(--t-dim)', accent: 'var(--t-accent)',
}

export default function Login({ onLogin }: { onLogin: (auth: AuthState) => void }) {
  const [selectedAlias, setSelectedAlias] = useState<string>('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!selectedAlias || !password) return
    setLoading(true)
    setError('')
    try {
      const alias = selectedAlias as Annotator
      const res = await loginAPI(alias, password)
      if (res.ok) {
        const auth = { name: alias, password }
        saveAuth(auth)
        onLogin(auth)
      } else {
        setError(res.error || 'Login failed')
      }
    } catch {
      setError('Cannot connect to server')
    }
    setLoading(false)
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: c.bg,
    }}>
      <div style={{
        width: 360, padding: 32, borderRadius: 16,
        border: `1px solid ${c.border}`, background: c.surface,
      }}>
        <div style={{
          width: 36, height: 36, borderRadius: 10, background: c.accent,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          marginBottom: 20,
        }}>
          <span style={{ color: '#fff', fontSize: 14, fontWeight: 700 }}>SF</span>
        </div>

        <h2 style={{ fontSize: 18, fontWeight: 600, color: c.fg, margin: '0 0 4px' }}>
          Annotation Mode
        </h2>
        <p style={{ fontSize: 13, color: c.muted, margin: '0 0 24px' }}>
          Select your user ID and enter your password to begin annotating.
        </p>

        {/* User dropdown — aliases only */}
        <label style={{ fontSize: 11, fontWeight: 600, color: c.dim, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          User
        </label>
        <select
          value={selectedAlias}
          onChange={e => setSelectedAlias(e.target.value)}
          style={{
            width: '100%', height: 36, marginTop: 6, marginBottom: 16,
            padding: '0 10px', borderRadius: 6, fontSize: 13, fontFamily: 'inherit',
            background: c.bg, border: `1px solid ${c.border}`, color: c.fg,
            appearance: 'none', cursor: 'pointer',
          }}
        >
          <option value="" disabled>Select your user ID...</option>
          {ANNOTATORS.map(a => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>

        {/* Password */}
        <label style={{ fontSize: 11, fontWeight: 600, color: c.dim, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Password
        </label>
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          placeholder="Enter or create password"
          style={{
            width: '100%', height: 36, marginTop: 6, marginBottom: 20,
            padding: '0 10px', borderRadius: 6, fontSize: 13, fontFamily: 'inherit',
            background: c.bg, border: `1px solid ${c.border}`, color: c.fg,
            outline: 'none',
          }}
        />

        {error && (
          <p style={{ fontSize: 12, color: '#ef4444', marginBottom: 12 }}>{error}</p>
        )}

        <button
          onClick={handleSubmit}
          disabled={!selectedAlias || !password || loading}
          style={{
            width: '100%', height: 36, borderRadius: 6, border: 'none',
            background: selectedAlias && password ? c.accent : c.dim,
            color: '#fff', fontSize: 13, fontWeight: 500, fontFamily: 'inherit',
            cursor: selectedAlias && password ? 'pointer' : 'default',
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>

        <p style={{ fontSize: 11, color: c.dim, marginTop: 12, textAlign: 'center' }}>
          First time? Your password will be created automatically.
        </p>
      </div>
    </div>
  )
}
