import { NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '../auth'
import { useI18n } from '../i18n'

export default function Layout() {
  const { user, logout } = useAuth()
  const { t, lang, setLang } = useI18n()

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <img src="/favicon.svg" alt="" width={28} height={28} />
          <div>
            <div className="brand-name">
              {t('appName')} <span className="brand-sub">{t('portal')}</span>
            </div>
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/" end>
            {t('nav.map')}
          </NavLink>
          <NavLink to="/queue">{t('nav.queue')}</NavLink>
          <NavLink to="/stuck">{t('nav.stuck')}</NavLink>
        </nav>
        <div className="topbar-right">
          <div className="lang" role="group" aria-label="Language">
            <button className={lang === 'en' ? 'on' : ''} onClick={() => setLang('en')}>
              EN
            </button>
            <button className={lang === 'ta' ? 'on' : ''} onClick={() => setLang('ta')}>
              தமிழ்
            </button>
          </div>
          <span className="who">{user?.name ?? user?.username}</span>
          <button className="btn ghost" onClick={logout}>
            {t('logout')}
          </button>
        </div>
      </header>
      <div className="notice">{t('mockNotice')}</div>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
