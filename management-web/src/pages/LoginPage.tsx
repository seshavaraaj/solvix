import { useState, type FormEvent } from 'react'

import { useAuth } from '../auth'
import { useI18n } from '../i18n'

export default function LoginPage() {
  const { login } = useAuth()
  const { t, lang, setLang } = useI18n()
  const [username, setUsername] = useState('collector')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setErr(null)
    try {
      await login(username, password)
    } catch (e) {
      setErr(e instanceof Error && e.message ? e.message : t('loginFailed'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submit}>
        <div className="login-top">
          <img src="/favicon.svg" alt="" width={44} height={44} />
          <div className="lang" role="group" aria-label="Language">
            <button type="button" className={lang === 'en' ? 'on' : ''} onClick={() => setLang('en')}>
              EN
            </button>
            <button type="button" className={lang === 'ta' ? 'on' : ''} onClick={() => setLang('ta')}>
              தமிழ்
            </button>
          </div>
        </div>
        <h1>
          {t('appName')} <span className="brand-sub">{t('portal')}</span>
        </h1>
        <p className="tagline">{t('tagline')}</p>
        <label>
          {t('username')}
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
        </label>
        <label>
          {t('password')}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            autoFocus
          />
        </label>
        {err && <div className="form-error">{err}</div>}
        <button className="btn primary block" disabled={busy}>
          {t('login')}
        </button>
        <p className="muted small">{t('loginHint')}</p>
      </form>
    </div>
  )
}
