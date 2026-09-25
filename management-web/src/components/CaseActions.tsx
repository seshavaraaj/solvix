import { useState } from 'react'

import { api } from '../api'
import { useI18n } from '../i18n'
import type { Report, ReportDetail } from '../types'

type Mode = 'approve' | 'reject' | 'pay' | null

/** Approve / reject / mock-pay buttons with an inline note form. Renders nothing when no action fits the status. */
export default function CaseActions({
  report,
  onDone,
  compact = false,
}: {
  report: Report
  onDone: (updated: ReportDetail) => void
  compact?: boolean
}) {
  const { t } = useI18n()
  const [mode, setMode] = useState<Mode>(null)
  const [note, setNote] = useState('')
  const [amount, setAmount] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  if (report.status !== 'verified' && report.status !== 'approved') return null

  const submit = async () => {
    if (mode === 'reject' && !note.trim()) {
      setErr(t('noteRequired'))
      return
    }
    setBusy(true)
    setErr(null)
    try {
      const n = note.trim() || undefined
      const updated =
        mode === 'approve'
          ? await api.approve(report.id, n)
          : mode === 'reject'
            ? await api.reject(report.id, note.trim())
            : await api.pay(report.id, amount ? Number(amount) : undefined, n)
      setMode(null)
      setNote('')
      setAmount('')
      onDone(updated)
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e))
    } finally {
      setBusy(false)
    }
  }

  if (!mode) {
    return (
      <div className={`actions ${compact ? 'compact' : ''}`}>
        {report.status === 'verified' && (
          <>
            <button className="btn primary" onClick={() => setMode('approve')}>
              {t('approve')}
            </button>
            <button className="btn danger" onClick={() => setMode('reject')}>
              {t('reject')}
            </button>
          </>
        )}
        {report.status === 'approved' && (
          <button className="btn pay" onClick={() => setMode('pay')}>
            {t('pay')}
          </button>
        )}
      </div>
    )
  }

  return (
    <div className="action-form">
      {mode === 'pay' && (
        <label>
          {t('amount')}
          <input type="number" min={0} value={amount} onChange={(e) => setAmount(e.target.value)} />
        </label>
      )}
      <label>
        {t('note')}
        <textarea
          rows={2}
          value={note}
          placeholder={t('notePlaceholder')}
          onChange={(e) => setNote(e.target.value)}
          autoFocus
        />
      </label>
      {err && <div className="form-error">{err}</div>}
      <div className="actions">
        <button
          className={`btn ${mode === 'reject' ? 'danger' : mode === 'pay' ? 'pay' : 'primary'}`}
          disabled={busy}
          onClick={submit}
        >
          {t('confirm')}: {t(mode === 'pay' ? 'pay' : mode)}
        </button>
        <button className="btn ghost" disabled={busy} onClick={() => setMode(null)}>
          {t('cancel')}
        </button>
      </div>
    </div>
  )
}
