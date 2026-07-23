import { CircleMarker, Tooltip, Popup } from 'react-leaflet'
import type { GeoJSONCollection, RiskLevel } from '../../types'
import { RISK_COLORS } from '../../types'

interface Props {
  hotspotsGeoJSON: GeoJSONCollection | null
  onHotspotClick: (id: number) => void
}

export default function HotspotLayer({ hotspotsGeoJSON, onHotspotClick }: Props) {
  if (!hotspotsGeoJSON?.features.length) return null

  return (
    <>
      {hotspotsGeoJSON.features.map((feature, idx) => {
        const [lon, lat] = feature.geometry.coordinates
        const p = feature.properties as Record<string, unknown>
        const id = p.id as number ?? idx
        const level = (p.hotspot_level as RiskLevel) ?? 'LOW'
        const color = RISK_COLORS[level] ?? '#6c757d'
        const radius = Math.max(12, Math.min(40, ((p.radius_meters as number) ?? 200) / 15))

        return (
          <CircleMarker
            key={id}
            center={[lat, lon]}
            radius={radius}
            pathOptions={{
              color,
              fillColor: color,
              fillOpacity: 0.35,
              weight: 2,
            }}
            eventHandlers={{
              click: () => onHotspotClick(id),
            }}
          >
            <Tooltip sticky>
              <div style={{ minWidth: 150 }}>
                <div className="fw-bold border-bottom pb-1 mb-1">
                  ━━━━━━━━━━━━━━<br />
                  {p.cluster_display_id as string}<br />
                  ━━━━━━━━━━━━━━
                </div>
                <div>{p.total_incidents as number} Kejadian</div>
                <div>
                  Risk Level:{' '}
                  <span style={{ color, fontWeight: 'bold' }}>{level}</span>
                </div>
                <div>Jenis Dominan: <strong>{p.dominant_type as string}</strong></div>
              </div>
            </Tooltip>
            <Popup>
              <div>
                <strong>{p.cluster_display_id as string}</strong><br />
                Jumlah Kejadian: {p.total_incidents as number}<br />
                Risk Score: {p.risk_score as number}<br />
                Jenis Dominan: {p.dominant_type as string}<br />
                <button
                  className="btn btn-sm btn-danger mt-2 w-100"
                  onClick={() => onHotspotClick(id)}
                >
                  Klik untuk detail →
                </button>
              </div>
            </Popup>
          </CircleMarker>
        )
      })}
    </>
  )
}
