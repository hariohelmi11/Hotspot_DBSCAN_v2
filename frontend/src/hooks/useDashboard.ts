import { useState, useEffect } from 'react'
import { dashboardApi } from '../services/api'
import type { DashboardData } from '../types'

export function useDashboard(year: number | null) {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    dashboardApi.get(year)
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [year])

  return { data, loading, error }
}
