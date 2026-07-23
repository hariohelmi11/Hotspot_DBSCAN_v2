import { useEffect } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet.heat'
import type { GeoJSONCollection } from '../../types'

interface Props {
  incidentsGeoJSON: GeoJSONCollection | null
}

export default function HeatmapLayer({ incidentsGeoJSON }: Props) {
  const map = useMap()

  useEffect(() => {
    if (!incidentsGeoJSON?.features.length) return

    const points: [number, number, number][] = incidentsGeoJSON.features
      .filter(f => f.geometry?.coordinates)
      .map(f => {
        const [lon, lat] = f.geometry.coordinates
        const severity = (f.properties as Record<string, unknown>).severity_score as number ?? 1
        return [lat, lon, severity / 5]
      })

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const heat = (L as any).heatLayer(points, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
      gradient: { 0.4: '#28a745', 0.6: '#ffc107', 0.8: '#fd7e14', 1.0: '#dc3545' },
    })

    heat.addTo(map)
    return () => { heat.remove() }
  }, [map, incidentsGeoJSON])

  return null
}
