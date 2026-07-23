export interface Hotspot {
  id: number
  cluster_display_id: string
  cluster_label: number
  total_incidents: number
  dominant_type: string
  risk_score: number
  hotspot_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  radius_meters: number
  analysis_year: number
  centroid_lat: number
  centroid_lon: number
}

export interface HotspotDetail extends Hotspot {
  incidents: IncidentSummary[]
  historical: {
    '2024'?: number
    '2025'?: number
    '2026'?: number
    trend?: string
  }
}

export interface IncidentSummary {
  id: number
  incident_date: string | null
  incident_year: number
  incident_type: string
  location_name: string
  district: string
  subdistrict: string
  severity_score: number
  source: string
  article_url: string | null
}

export interface Incident extends IncidentSummary {
  latitude: number | null
  longitude: number | null
  hotspot_cluster_id: number | null
}

export interface DashboardStats {
  total_incidents: number
  total_hotspots: number
  high_risk_areas: number
  critical_areas: number
}

export interface DashboardData {
  stats: DashboardStats
  trend: { year: number; count: number }[]
  type_distribution: { incident_type: string; count: number }[]
  risk_distribution: { risk_level: string; count: number }[]
  top_wilayah: { wilayah: string; count: number }[]
}

export interface FilterState {
  year: number | null
  district: string | null
  subdistrict: string | null
  incident_type: string | null
  source: string | null
}

export interface ActiveLayers {
  markers: boolean
  heatmap: boolean
  hotspots: boolean
}

export interface GeoJSONPoint {
  type: 'Point'
  coordinates: [number, number]
}

export interface GeoJSONFeature<P = Record<string, unknown>> {
  type: 'Feature'
  geometry: GeoJSONPoint
  properties: P
}

export interface GeoJSONCollection<P = Record<string, unknown>> {
  type: 'FeatureCollection'
  features: GeoJSONFeature<P>[]
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export const RISK_COLORS: Record<RiskLevel, string> = {
  LOW: '#28a745',
  MEDIUM: '#ffc107',
  HIGH: '#fd7e14',
  CRITICAL: '#dc3545',
}

/**
 * Warna per jenis kejadian — dipakai konsisten di marker peta & grafik bar.
 * Keyword-based: cocokkan dengan includes() pada incident_type.toUpperCase()
 */
export const INCIDENT_TYPE_COLORS: Record<string, string> = {
  'PKL':             '#dc3545',   // merah
  'PENYALAHGUNAAN':  '#fd7e14',   // oranye
  'PAK OGAH':        '#ffc107',   // kuning
  'TAWURAN':         '#28a745',   // hijau
  'PENGEMIS':        '#0dcaf0',   // biru muda
  'KRIMINALITAS':    '#6f42c1',   // ungu
  'PENGAMEN':        '#20c997',   // teal
  'PEDAGANG':        '#0d6efd',   // biru
  'ORMAS':           '#adb5bd',   // abu
  'MANUSIA SILVER':  '#343a40',   // gelap
}

export function getIncidentTypeColor(type: string): string {
  const upper = (type ?? '').toUpperCase()
  for (const [key, color] of Object.entries(INCIDENT_TYPE_COLORS)) {
    if (upper.includes(key)) return color
  }
  return '#6c757d'
}
