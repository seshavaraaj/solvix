import { useCallback, useEffect, useState, type CSSProperties } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { api, photoUrl } from '../api'
import { Confidence, ErrorBox, FlagChips, Loading, StatusBadge } from '../components/bits'
import CaseActions from '../components/CaseActions'
import { formatDateTime, STATUS_COLOR } from '../format'
import { useI18n } from '../i18n'
import type { ReportDetail } from '../types'

const fmtCoord = (lat: number | null, lon: number | null) =>
  lat == null || lon == null ? '—' : `${lat.toFixed(5)}, ${lon.toFixed(5)}`

export default function CasePage() {
  const { id } = useParams()
  const { t, lang } = useI18n()
  const navigate = useNavigate()
  const [report, setReport] = useState<ReportDetail | null>(null)
  const [error, setError] = useState<unknown>(null)

  const load = useCallback(() => {
    if (!id) return
    setError(null)
    api.report(id).then(setReport).catch(setError)
  }, [id])

  useEffect(load, [load])

  if (error) return <ErrorBox error={error} onRetry={load} />
  if (!report) return <Loading />

  const r = report
  const flood =
    r.in_flood_extent == null ? t('unknownFlood') : r.in_flood_extent ? t('inFlood') : t('outFlood')

  return (
    <div className="page case">
      <button className="link muted small" onClick={() => navigate(-1)}>
        ← {t('back')}
      </button>
      <div className="case-head">
        <div>
          <h2>
            {t(`asset.${r.asset_type}`)} · {t(`damage.${r.damage_type}`)}
          </h2>
          <p className="muted">
            {[r.village, r.taluk, r.district].filter(Boolean).join(', ')} · <code>{r.id.slice(0, 8)}</code>
            {r.synthetic && <span className="tag">{t('synthetic')}</span>}
          </p>
        </div>
        <StatusBadge status={r.status} />
      </div>

      <div className="case-grid">
        <section className="card">
          <h3>{t('evidence')}</h3>
          {r.photo_url ? (
            <a href={photoUrl(r.photo_url)!} target="_blank" rel="noreferrer">
              <img className="evidence large" src={photoUrl(r.photo_url)!} alt={t('evidence')} />
            </a>
          ) : (
            <div className="evidence empty">{t('noPhoto')}</div>
          )}
          {r.description && <p>{r.description}</p>}
        </section>

        <section className="card">
          <h3>{t('flags')}</h3>
          <div className="conf-row">
            <Confidence value={r.confidence} /> <span className="muted small">{t('confidence')}</span>
          </div>
          <FlagChips flags={r.flags} verbose />
          <dl className="kv">
            <dt>{t('location')}</dt>
            <dd>{fmtCoord(r.lat, r.lon)}</dd>
            <dt>{t('photoGps')}</dt>
            <dd>{fmtCoord(r.exif_lat, r.exif_lon)}</dd>
            <dt>{t('floodLayer')}</dt>
            <dd>{flood}</dd>
            <dt>{t('capturedAt')}</dt>
            <dd>{formatDateTime(r.exif_taken_at ?? r.captured_at, lang)}</dd>
            <dt>{t('reportedAt')}</dt>
            <dd>{formatDateTime(r.created_at, lang)}</dd>
            <dt>{t('reporter')}</dt>
            <dd>
              {r.reporter_name ?? '—'} {r.reporter_phone && <span className="muted">({r.reporter_phone})</span>}
            </dd>
            <dt>{t('severity')}</dt>
            <dd>{r.severity_hint ?? '—'} / 5</dd>
            {r.payment_ref && (
              <>
                <dt>{t('paymentRef')}</dt>
                <dd>
                  <code>{r.payment_ref}</code>
                </dd>
              </>
            )}
          </dl>
          <CaseActions report={r} onDone={setReport} />
        </section>

        <section className="card">
          <h3>{t('history')}</h3>
          <ol className="timeline">
            {r.history.map((h) => (
              <li key={h.id} style={{ '--c': STATUS_COLOR[h.to_status] } as CSSProperties}>
                <div className="tl-head">
                  <strong>{t(`status.${h.to_status}`)}</strong>
                  <span className="muted small">{formatDateTime(h.created_at, lang)}</span>
                </div>
                <div className="small">
                  {t('by')} {h.actor_name ?? '—'}
                  {h.actor_role && <span className="muted"> · {h.actor_role}</span>}
                </div>
                {h.note && <div className="tl-note">{h.note}</div>}
              </li>
            ))}
          </ol>
        </section>

        <section className="card">
          <h3>{t('grievances')}</h3>
          {r.grievances.length === 0 ? (
            <p className="muted">{t('noGrievances')}</p>
          ) : (
            <ul className="grievances">
              {r.grievances.map((g) => (
                <li key={g.id}>
                  <div className="row-between">
                    <span className="tag">{g.status}</span>
                    <span className="muted small">{formatDateTime(g.created_at, lang)}</span>
                  </div>
                  <p>{g.text}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  )
}
