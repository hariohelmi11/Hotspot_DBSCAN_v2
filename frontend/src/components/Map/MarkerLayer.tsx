import { CircleMarker, Tooltip } from 'react-leaflet'
import type { GeoJSONCollection } from '../../types'
import { getIncidentTypeColor } from '../../types'

interface Props {
  incidentsGeoJSON: GeoJSONCollection | null
}

export default function MarkerLayer({ incidentsGeoJSON }: Props) {
  if (!incidentsGeoJSON?.features.length) return null

  return (
    <>
      {incidentsGeoJSON.features.map((feature, idx) => {
        const [lon, lat] = feature.geometry.coordinates
        const props = feature.properties as Record<string, unknown>
        const type = props.incident_type as string ?? 'UNKNOWN'
        const id = props.id as number ?? idx

        return (
          <CircleMarker
            key={id}
            center={[lat, lon]}
            radius={5}
            pathOptions={{
              color: getIncidentTypeColor(type),
              fillColor: getIncidentTypeColor(type),
              fillOpacity: 0.85,
              weight: 1,
            }}
          >
            <Tooltip sticky>
              <div style={{ minWidth: 210, fontSize: 12 }}>
                <div style={{ fontWeight: 'bold', fontSize: 13, marginBottom: 4, borderBottom: '1px solid rgba(255,255,255,0.3)', paddingBottom: 3 }}>
                  {type}
                </div>
                <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                  <tbody>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Tanggal</td>
                      <td>{(props.incident_date as string) ?? '—'}</td>
                    </tr>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Wilayah</td>
                      <td>{(props.district as string) ?? '—'}</td>
                    </tr>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Kecamatan</td>
                      <td>{(props.subdistrict as string) ?? '—'}</td>
                    </tr>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Kelurahan</td>
                      <td>{(props.location_name as string) ?? '—'}</td>
                    </tr>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Koordinat</td>
                      <td>
                        {typeof props.latitude === 'number' && typeof props.longitude === 'number'
                          ? `${(props.latitude as number).toFixed(6)}, ${(props.longitude as number).toFixed(6)}`
                          : '—'}
                      </td>
                    </tr>
                    <tr>
                      <td style={{ color: 'rgba(255,255,255,0.65)', paddingRight: 8, whiteSpace: 'nowrap' }}>Sumber</td>
                      <td>{(props.source as string) ?? '—'}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </Tooltip>
          </CircleMarker>
        )
      })}
    </>
  )
}
