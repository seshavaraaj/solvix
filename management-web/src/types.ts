export type Status = 'reported' | 'verified' | 'rejected' | 'approved' | 'paid'

export const STATUSES: Status[] = ['reported', 'verified', 'rejected', 'approved', 'paid']

export interface User {
  id: number
  phone: string | null
  username: string | null
  role: string
  name: string | null
  district: string | null
  taluk: string | null
}

export interface Flag {
  code: string
  message: string
  ref?: string
  distance_m?: number
}

export interface Report {
  id: string
  asset_id: number
  asset_type: string
  reporter_id: number
  reporter_name: string | null
  reporter_phone: string | null
  damage_type: string
  severity_hint: number | null
  description: string | null
  lat: number
  lon: number
  district: string | null
  taluk: string | null
  village: string | null
  captured_at: string | null
  exif_lat: number | null
  exif_lon: number | null
  exif_taken_at: string | null
  photo_url: string | null
  in_flood_extent: boolean | null
  confidence: number
  flags: Flag[]
  status: Status
  status_changed_at: string
  payment_ref: string | null
  synthetic: boolean
  created_at: string
}

export interface HistoryItem {
  id: number
  from_status: Status | null
  to_status: Status
  actor_id: number | null
  actor_name: string | null
  actor_role: string | null
  evidence_ref: string | null
  note: string | null
  created_at: string
}

export interface Grievance {
  id: number
  text: string
  status: string
  created_at: string
}

export interface ReportDetail extends Report {
  history: HistoryItem[]
  grievances: Grievance[]
}

export interface Summary {
  total: number
  by_status: Record<Status, number>
  in_flood_extent: number
  outside_flood_extent: number
  flagged: number
  open_grievances: number
}

export interface StuckRow {
  status: Status
  count: number
  stuck: number
  oldest_hours: number
}

export interface Stuck {
  thresholds_hours: Partial<Record<Status, number>>
  by_status: StuckRow[]
  by_area: (StuckRow & { district: string; village: string })[]
  stuck_cases: {
    id: string
    status: Status
    district: string | null
    village: string | null
    age_hours: number
    limit_hours: number
  }[]
}
