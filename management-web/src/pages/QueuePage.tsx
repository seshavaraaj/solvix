import { useCallback, useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

import { api } from '../api'
import { Confidence, ErrorBox, FlagChips, Loading } from '../components/bits'
import CaseActions from '../components/CaseActions'
import { formatAge, hoursSince } from '../format'
import { useI18n } from '../i18n'
import type { Report, Status } from '../types'

const TABS: Status[] = ['verified', 'approved', 'reported']

export default function QueuePage() {
  const { t } = useI18n()
  const [params, setParams] = useSearchParams()
  const tab = (TABS.includes(params.get('tab') as Status) ? params.get('tab') : 'verified') as Status
  const [rows, setRows] = useState<Report[] | null>(null)
  const [counts, setCounts] = useState<Partial<Record<Status, number>>>({})
  const [error, setError] = useState<unknown>(null)

  const load = useCallback(() => {
    setError(null)
    setRows(null)
    api
      .reports({ status: tab, sort: 'confidence' })
      .then(setRows)
      .catch(setError)
    api
      .summary()
      .then((s) => setCounts(s.by_status))
      .catch(() => {})
  }, [tab])

  useEffect(load, [load])

  return (
    <div className="page">
      <div className="tabs">
        {TABS.map((s) => (
          <button key={s} className={s === tab ? 'on' : ''} onClick={() => setParams({ tab: s })}>
            {t(`tab.${s}`)}
            <span className="count">{counts[s] ?? '·'}</span>
          </button>
        ))}
      </div>
      {tab === 'reported' && <p className="muted small">{t('fieldOnly')}</p>}

      {error ? (
        <ErrorBox error={error} onRetry={load} />
      ) : !rows ? (
        <Loading />
      ) : rows.length === 0 ? (
        <div className="state">{t('noRows')}</div>
      ) : (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>{t('confidence')}</th>
                <th>{t('village')}</th>
                <th>{t('asset')}</th>
                <th>{t('damage')}</th>
                <th>{t('flags')}</th>
                <th>{t('age')}</th>
                {tab !== 'reported' && <th>{t('actions')}</th>}
                <th />
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td>
                    <Confidence value={r.confidence} />
                  </td>
                  <td>
                    <div>{r.village ?? '—'}</div>
                    <div className="muted small">{r.district}</div>
                  </td>
                  <td>{t(`asset.${r.asset_type}`)}</td>
                  <td>{t(`damage.${r.damage_type}`)}</td>
                  <td>
                    <FlagChips flags={r.flags} />
                  </td>
                  <td className="nowrap">{formatAge(hoursSince(r.status_changed_at), t)}</td>
                  {tab !== 'reported' && (
                    <td>
                      <CaseActions report={r} onDone={load} compact />
                    </td>
                  )}
                  <td>
                    <Link to={`/cases/${r.id}`}>{t('openCase')} →</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
