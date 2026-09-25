import type { Status } from './types'

export const STATUS_COLOR: Record<Status, string> = {
  reported: '#d98e04',
  verified: '#2563eb',
  rejected: '#c0392b',
  approved: '#15803d',
  paid: '#7c3aed',
}

export function hoursSince(iso: string): number {
  return (Date.now() - new Date(iso).getTime()) / 3_600_000
}

export function formatAge(hours: number, t: (k: string) => string): string {
  if (hours < 48) return `${Math.round(hours)} ${t('hoursShort')}`
  return `${Math.round(hours / 24)} ${t('daysShort')}`
}

export function formatDateTime(iso: string | null, lang: string): string {
  if (!iso) return '—'
  return new Date(iso).toLocaleString(lang === 'ta' ? 'ta-IN' : 'en-IN', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function confidenceTone(c: number): 'good' | 'mid' | 'low' {
  if (c >= 80) return 'good'
  if (c >= 50) return 'mid'
  return 'low'
}
