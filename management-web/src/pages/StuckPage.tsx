import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../api'
import { ErrorBox, Loading, StatusBadge } from '../components/bits'
import { formatAge, STATUS_COLOR } from '../format'
import { useI18n } from '../i18n'
import type { Stuck } from '../types'

export default function StuckPage() {
  const { t } = useI18n()
  const [district, setDistrict] = useState('')
  const [districts, setDistricts] = useState<string[]>([])
  const [data, setData] = useState<Stuck | null>(null)
  const [error, setError] = useState<unknown>(null)
  const [exporting, setExporting] = useState(false)

  const load = useCallback(() => {
    setError(null)
    setData(null)
    api
      .stuck(district || undefined)
      .then((d) => {
        setData(d)
        if (!district) setDistricts([...new Set(d.by_area.map((a) => a.district))].sort())
      })
      .catch(setError)
  }, [district])

  useEffect(load, [load])

  const doExport = async () => {
    setExporting(true)
    try {
      await api.exportPdna(district || undefined)
    } catch (e) {
      setError(e)
    } finally {
      setExporting(false)
    }
  }

  const stuckAreas = data?.by_area.filter((a) => a.stuck > 0).sort((a, b) => b.stuck - a.stuck) ?? []

  return (
    <div className="page">
      <div className="row-between wrap">
        <h2>{t('stuckTitle')}</h2>
        <div className="toolbar">
          <select value={district} onChange={(e) => setDistrict(e.target.value)}>
            <option value="">{t('allDistricts')}</option>
            {districts.map((d) => (
              <option key={d}>{d}</option>
            ))}
          </select>
          <button className="btn primary" onClick={doExport} disabled={exporting}>
            ⬇ {t('exportPdna')}
          </button>
        </div>
      </div>
      <p className="muted small">{t('exportNote')}</p>

      {error ? <ErrorBox error={error} onRetry={load} /> : null}
      {!data ? (
        !error && <Loading />
      ) : (
        <>
          <div className="stage-cards">
            {data.by_status.map((s) => {
              const limit = data.thresholds_hours[s.status]
              return (
                <div className="stage" key={s.status} style={{ borderTopColor: STATUS_COLOR[s.status] }}>
                  <StatusBadge status={s.status} />
                  <div className="stage-count">{s.count}</div>
                  {limit != null ? (
                    <>
                      <div className={`stage-stuck ${s.stuck ? 'bad' : ''}`}>
                        {s.stuck} {t('stuckCount')}
                      </div>
                      <div className="muted small">
                        {t('stuckAfter')} {formatAge(limit, t)} · {t('oldest')} {formatAge(s.oldest_hours, t)}
                      </div>
                    </>
                  ) : (
                    <div className="muted small">—</div>
                  )}
                </div>
              )
            })}
          </div>

          <div className="two-col">
            <section className="card">
              <h3>{t('byArea')}</h3>
              {stuckAreas.length === 0 ? (
                <p className="muted">{t('noneStuck')}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>{t('district')}</th>
                      <th>{t('village')}</th>
                      <th>{t('status')}</th>
                      <th>{t('stuckCount')}</th>
                      <th>{t('oldest')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stuckAreas.map((a) => (
                      <tr key={`${a.district}-${a.village}-${a.status}`}>
                        <td>{a.district}</td>
                        <td>{a.village}</td>
                        <td>
                          <StatusBadge status={a.status} />
                        </td>
                        <td>
                          <strong>{a.stuck}</strong> / {a.count}
                        </td>
                        <td className="nowrap">{formatAge(a.oldest_hours, t)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </section>

            <section className="card">
              <h3>{t('overdue')}</h3>
              {data.stuck_cases.length === 0 ? (
                <p className="muted">{t('noneStuck')}</p>
              ) : (
                <ul className="overdue">
                  {data.stuck_cases.slice(0, 15).map((c) => (
                    <li key={c.id}>
                      <Link to={`/cases/${c.id}`}>
                        <StatusBadge status={c.status} />
                        <span>
                          {c.village}, {c.district}
                        </span>
                        <span className="over">
                          {formatAge(c.age_hours, t)}
                          <span className="muted"> / {formatAge(c.limit_hours, t)}</span>
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        </>
      )}
    </div>
  )
}
