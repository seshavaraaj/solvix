import maplibregl, { type GeoJSONSource, type Map as MlMap } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import type { FeatureCollection } from 'geojson'

import { api, photoUrl } from '../api'
import { Confidence, ErrorBox, FlagChips, StatusBadge } from '../components/bits'
import CaseActions from '../components/CaseActions'
import { formatDateTime, STATUS_COLOR } from '../format'
import { useI18n } from '../i18n'
import { STATUSES, type Report, type ReportDetail, type Status, type Summary } from '../types'

const BASEMAP = 'https://tiles.openfreemap.org/styles/positron'
const CHENNAI: [number, number] = [80.17, 13.03]

function toGeoJSON(reports: Report[]): FeatureCollection {
  return {
    type: 'FeatureCollection',
    features: reports.map((r) => ({
      type: 'Feature',
      id: r.id,
      properties: { id: r.id, status: r.status, flagged: r.flags.length > 0 },
      geometry: { type: 'Point', coordinates: [r.lon, r.lat] },
    })),
  }
}

export default function MapPage() {
  const { t, lang } = useI18n()
  const mapEl = useRef<HTMLDivElement>(null)
  const map = useRef<MlMap | null>(null)
  const [mapReady, setMapReady] = useState(false)

  const [reports, setReports] = useState<Report[]>([])
  const [summary, setSummary] = useState<Summary | null>(null)
  const [error, setError] = useState<unknown>(null)
  const [statuses, setStatuses] = useState<Set<Status>>(new Set(STATUSES))
  const [district, setDistrict] = useState('')
  const [flaggedOnly, setFlaggedOnly] = useState(false)
  const [showFlood, setShowFlood] = useState(true)
  const [selected, setSelected] = useState<ReportDetail | null>(null)

  const load = useCallback(() => {
    setError(null)
    Promise.all([api.reports({ limit: '5000', sort: 'newest' }), api.summary()])
      .then(([r, s]) => {
        setReports(r)
        setSummary(s)
      })
      .catch(setError)
  }, [])

  useEffect(load, [load])

  // Create the map once.
  useEffect(() => {
    if (!mapEl.current) return
    const m = new maplibregl.Map({ container: mapEl.current, style: BASEMAP, center: CHENNAI, zoom: 10 })
    m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')
    m.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left')
    m.on('load', async () => {
      m.addSource('reports', { type: 'geojson', data: toGeoJSON([]) })
      try {
        const { active_event } = await api.floodEvents()
        const flood = await api.floodLayer(active_event)
        m.addSource('flood', { type: 'geojson', data: flood })
        m.addLayer({ id: 'flood-fill', type: 'fill', source: 'flood', paint: { 'fill-color': '#1d6fb8', 'fill-opacity': 0.22 } })
        m.addLayer({ id: 'flood-line', type: 'line', source: 'flood', paint: { 'line-color': '#1d6fb8', 'line-width': 1.5 } })
        const bounds = new maplibregl.LngLatBounds()
        const walk = (c: unknown): void => {
          if (Array.isArray(c) && typeof c[0] === 'number') bounds.extend(c as [number, number])
          else if (Array.isArray(c)) c.forEach(walk)
        }
        flood.features.forEach((f) => f.geometry.type !== 'GeometryCollection' && walk(f.geometry.coordinates))
        if (!bounds.isEmpty()) m.fitBounds(bounds, { padding: 60, duration: 0 })
      } catch {
        /* no flood layer loaded: map still works */
      }
      m.addLayer({
        id: 'reports',
        type: 'circle',
        source: 'reports',
        paint: {
          'circle-radius': ['interpolate', ['linear'], ['zoom'], 9, 4, 14, 9],
          'circle-color': [
            'match', ['get', 'status'],
            ...STATUSES.flatMap((s) => [s, STATUS_COLOR[s]]),
            '#888',
          ] as unknown as string,
          'circle-stroke-color': ['case', ['get', 'flagged'], '#111', '#fff'] as unknown as string,
          'circle-stroke-width': ['case', ['get', 'flagged'], 2, 1] as unknown as number,
        },
      })
      m.on('click', 'reports', (e) => {
        const id = e.features?.[0]?.properties?.id as string | undefined
        if (id) api.report(id).then(setSelected).catch(setError)
      })
      m.on('mouseenter', 'reports', () => (m.getCanvas().style.cursor = 'pointer'))
      m.on('mouseleave', 'reports', () => (m.getCanvas().style.cursor = ''))
      setMapReady(true)
    })
    map.current = m
    return () => {
      m.remove()
      map.current = null
    }
  }, [])

  const districts = useMemo(
    () => [...new Set(reports.map((r) => r.district).filter(Boolean) as string[])].sort(),
    [reports],
  )

  const visible = useMemo(
    () =>
      reports.filter(
        (r) =>
          statuses.has(r.status) &&
          (!district || r.district === district) &&
          (!flaggedOnly || r.flags.length > 0),
      ),
    [reports, statuses, district, flaggedOnly],
  )

  useEffect(() => {
    if (!mapReady || !map.current) return
    ;(map.current.getSource('reports') as GeoJSONSource | undefined)?.setData(toGeoJSON(visible))
  }, [visible, mapReady])

  useEffect(() => {
    const m = map.current
    if (!mapReady || !m) return
    for (const id of ['flood-fill', 'flood-line']) {
      if (m.getLayer(id)) m.setLayoutProperty(id, 'visibility', showFlood ? 'visible' : 'none')
    }
  }, [showFlood, mapReady])

  const toggleStatus = (s: Status) =>
    setStatuses((prev) => {
      const next = new Set(prev)
      if (next.has(s)) next.delete(s)
      else next.add(s)
      return next
    })

  const onActionDone = (updated: ReportDetail) => {
    setSelected(updated)
    load()
  }

  return (
    <div className="map-page">
      {summary && (
        <div className="stats">
          <div className="stat">
            <span className="stat-v">{summary.total}</span>
            <span className="stat-l">{t('total')}</span>
          </div>
          {STATUSES.map((s) => (
            <div className="stat" key={s}>
              <span className="stat-v" style={{ color: STATUS_COLOR[s] }}>
                {summary.by_status[s]}
              </span>
              <span className="stat-l">{t(`status.${s}`)}</span>
            </div>
          ))}
          <div className="stat">
            <span className="stat-v">{summary.flagged}</span>
            <span className="stat-l">{t('flagged')}</span>
          </div>
          <div className="stat">
            <span className="stat-v">{summary.open_grievances}</span>
            <span className="stat-l">{t('openGrievances')}</span>
          </div>
        </div>
      )}

      <div className="filters">
        {STATUSES.map((s) => (
          <label key={s} className={`chip ${statuses.has(s) ? 'on' : ''}`}>
            <input type="checkbox" checked={statuses.has(s)} onChange={() => toggleStatus(s)} />
            <span className="dot" style={{ background: STATUS_COLOR[s] }} />
            {t(`status.${s}`)}
          </label>
        ))}
        <select value={district} onChange={(e) => setDistrict(e.target.value)}>
          <option value="">{t('allDistricts')}</option>
          {districts.map((d) => (
            <option key={d}>{d}</option>
          ))}
        </select>
        <label className={`chip ${flaggedOnly ? 'on' : ''}`}>
          <input type="checkbox" checked={flaggedOnly} onChange={(e) => setFlaggedOnly(e.target.checked)} />
          {t('flaggedOnly')}
        </label>
        <label className={`chip ${showFlood ? 'on' : ''}`}>
          <input type="checkbox" checked={showFlood} onChange={(e) => setShowFlood(e.target.checked)} />
          <span className="swatch flood" />
          {t('floodLayer')}
        </label>
        <span className="muted small">
          {visible.length} {t('reports')}
        </span>
      </div>

      {error ? <ErrorBox error={error} onRetry={load} /> : null}

      <div className="map-body">
        <div ref={mapEl} className="map" />
        <aside className="side">
          {!selected ? (
            <p className="muted">{t('selectReport')}</p>
          ) : (
            <div className="case-mini">
              <div className="row-between">
                <StatusBadge status={selected.status} />
                <button className="btn ghost small" onClick={() => setSelected(null)} aria-label="Close">
                  ✕
                </button>
              </div>
              <h3>
                {t(`asset.${selected.asset_type}`)} · {t(`damage.${selected.damage_type}`)}
              </h3>
              <p className="muted small">
                {[selected.village, selected.taluk, selected.district].filter(Boolean).join(', ')}
              </p>
              {selected.photo_url ? (
                <img className="evidence" src={photoUrl(selected.photo_url)!} alt={t('evidence')} />
              ) : (
                <div className="evidence empty">{t('noPhoto')}</div>
              )}
              <dl className="kv">
                <dt>{t('confidence')}</dt>
                <dd>
                  <Confidence value={selected.confidence} />
                </dd>
                <dt>{t('flags')}</dt>
                <dd>
                  <FlagChips flags={selected.flags} verbose />
                </dd>
                <dt>{t('reportedAt')}</dt>
                <dd>{formatDateTime(selected.created_at, lang)}</dd>
              </dl>
              <CaseActions report={selected} onDone={onActionDone} compact />
              <Link className="btn block" to={`/cases/${selected.id}`}>
                {t('openCase')} →
              </Link>
            </div>
          )}
        </aside>
      </div>
    </div>
  )
}
