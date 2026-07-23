import { useState, useEffect } from 'react'
import { geoJsonApi } from '../services/api'
import type { GeoJSONCollection, FilterState } from '../types'

export function useIncidentsGeoJSON(filters: Partial<FilterState>) {
  const [data, setData] = useState<GeoJSONCollection | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    geoJsonApi.incidents(filters)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.year, filters.district, filters.incident_type, filters.source])

  return { data, loading }
}
