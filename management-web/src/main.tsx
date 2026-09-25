import { StrictMode, type ReactNode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { AuthProvider, useAuth } from './auth'
import Layout from './components/Layout'
import { Loading } from './components/bits'
import { I18nProvider, useI18n } from './i18n'
import CasePage from './pages/CasePage'
import LoginPage from './pages/LoginPage'
import MapPage from './pages/MapPage'
import QueuePage from './pages/QueuePage'
import StuckPage from './pages/StuckPage'
import './styles.css'

function LangAttr({ children }: { children: ReactNode }) {
  const { lang } = useI18n()
  document.documentElement.lang = lang
  return <>{children}</>
}

function Routed() {
  const { user, ready } = useAuth()
  if (!ready) return <Loading />
  if (!user) return <LoginPage />
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<MapPage />} />
        <Route path="queue" element={<QueuePage />} />
        <Route path="stuck" element={<StuckPage />} />
        <Route path="cases/:id" element={<CasePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <I18nProvider>
      <LangAttr>
        <AuthProvider>
          <BrowserRouter>
            <Routed />
          </BrowserRouter>
        </AuthProvider>
      </LangAttr>
    </I18nProvider>
  </StrictMode>,
)
