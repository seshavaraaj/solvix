import type { CSSProperties } from 'react'

import { confidenceTone, STATUS_COLOR } from '../format'
import { useI18n } from '../i18n'
import type { Flag, Status } from '../types'

export function StatusBadge({ status }: { status: Status }) {
  const { t } = useI18n()
  return (
    <span className="badge" style={{ '--c': STATUS_COLOR[status] } as CSSProperties}>
      <span className="dot" />
      {t(`status.${status}`)}
    </span>
  )
}

export function Confidence({ value }: { value: number }) {
  return (
    <span className={`conf conf-${confidenceTone(value)}`} title="Rule-based score. Sorts the queue only.">
      {value}
    </span>
  )
}

export function FlagChips({ flags, verbose = false }: { flags: Flag[]; verbose?: boolean }) {
  const { t } = useI18n()
  if (!flags.length) return <span className="muted">{t('noFlags')}</span>
  return (
    <span className="flags">
      {flags.map((f) => (
        <span key={f.code} className="flag" title={f.message}>
          {t(`flag.${f.code}`)}
          {verbose && f.distance_m ? ` · ${f.distance_m} m` : ''}
        </span>
      ))}
    </span>
  )
}

export function Loading() {
  const { t } = useI18n()
  return <div className="state">{t('loading')}</div>
}

export function ErrorBox({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  const { t } = useI18n()
  return (
    <div className="state error">
      <strong>{t('error')}</strong>
      <span>{error instanceof Error ? error.message : String(error)}</span>
      {onRetry && (
        <button className="btn" onClick={onRetry}>
          {t('retry')}
        </button>
      )}
    </div>
  )
}
