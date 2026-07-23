import axios from 'axios'
import type { DashboardData, HotspotDetail, Hotspot, GeoJSONCollection, FilterState } from '../types'

const http = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
})

function cleanParams(params: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== null && v !== undefined && v !== '')
  )
}

export const dashboardApi = {
  get: (year?: number | null): Promise<DashboardData> =>
    http.get('/dashboard', { params: cleanParams({ year }) }).then(r => r.data),
}

export const hotspotsApi = {
  list: (filters: Partial<FilterState> = {}): Promise<Hotspot[]> =>
    http.get('/hotspots', { params: cleanParams(filters as Record<string, unknown>) }).then(r => r.data),

  getDetail: (id: number): Promise<HotspotDetail> =>
    http.get(`/hotspots/${id}`).then(r => r.data),
}

export const geoJsonApi = {
  hotspots: (filters: Partial<FilterState> = {}): Promise<GeoJSONCollection> =>
    http.get('/geojson/hotspots', { params: cleanParams(filters as Record<string, unknown>) }).then(r => r.data),

  incidents: (filters: Partial<FilterState> = {}): Promise<GeoJSONCollection> =>
    http.get('/geojson/incidents', { params: cleanParams(filters as Record<string, unknown>) }).then(r => r.data),
}

export const jobsApi = {
  runEtl: (source = 'all', year = 2024) =>
    http.post('/etl/run', { source, year }).then(r => r.data),

  runDbscan: (year?: number | null) =>
    http.post('/dbscan/run', { year }).then(r => r.data),
}
