import type { FeatureCollection } from 'geojson'

import type { Report, ReportDetail, Stuck, Summary, User } from './types'

function normalizeBase(raw: string): string {
  const url = raw.trim().replace(/\/+$/, '')
  return /^https?:\/\//.test(url) ? url : `https://${url}`
}

export const API_BASE = normalizeBase(import.meta.env.VITE_API_URL || 'http://localhost:8000')

const TOKEN_KEY = 'meetpu.token'

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token: string | null) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* storage unavailable: session lasts until reload */
  }
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (init.body && !(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers })
  if (res.status === 401) {
    setToken(null)
    window.dispatchEvent(new Event('meetpu:logout'))
  }
  if (!res.ok) {
    let msg = res.statusText
    try {
      const body = await res.json()
      msg = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
    } catch {
      /* not JSON */
    }
    throw new ApiError(res.status, msg)
  }
  return res.json() as Promise<T>
}

export const photoUrl = (path: string | null) => (path ? `${API_BASE}${path}` : null)

export const api = {
  login: (username: string, password: string) =>
    request<{ access_token: string; user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  me: () => request<User>('/auth/me'),

  reports: (params: Record<string, string | undefined> = {}) => {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => v && qs.set(k, v))
    return request<Report[]>(`/reports?${qs}`)
  },
  report: (id: string) => request<ReportDetail>(`/reports/${id}`),
  approve: (id: string, note?: string) =>
    request<ReportDetail>(`/reports/${id}/approve`, { method: 'POST', body: JSON.stringify({ note }) }),
  reject: (id: string, note: string) =>
    request<ReportDetail>(`/reports/${id}/reject`, { method: 'POST', body: JSON.stringify({ note }) }),
  pay: (id: string, amount_inr?: number, note?: string) =>
    request<ReportDetail>(`/reports/${id}/pay`, {
      method: 'POST',
      body: JSON.stringify({ amount_inr, note }),
    }),

  summary: () => request<Summary>('/dashboard/summary'),
  stuck: (district?: string) =>
    request<Stuck>(`/dashboard/stuck${district ? `?district=${encodeURIComponent(district)}` : ''}`),

  floodEvents: () => request<{ active_event: string; events: { event_name: string; source: string }[] }>('/flood-layer'),
  floodLayer: (event: string) => request<FeatureCollection>(`/flood-layer/${encodeURIComponent(event)}`),

  async exportPdna(district?: string) {
    const res = await fetch(
      `${API_BASE}/export/pdna${district ? `?district=${encodeURIComponent(district)}` : ''}`,
      { headers: { Authorization: `Bearer ${getToken() ?? ''}` } },
    )
    if (!res.ok) throw new ApiError(res.status, res.statusText)
    const name =
      res.headers.get('Content-Disposition')?.match(/filename="(.+)"/)?.[1] ?? 'meetpu-pdna.csv'
    const url = URL.createObjectURL(await res.blob())
    const a = document.createElement('a')
    a.href = url
    a.download = name
    a.click()
    URL.revokeObjectURL(url)
  },
}
