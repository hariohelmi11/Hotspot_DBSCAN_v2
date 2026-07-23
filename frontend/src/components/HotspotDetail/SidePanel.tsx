import type { HotspotDetail, RiskLevel } from '../../types'
import { RISK_COLORS } from '../../types'

interface Props {
  hotspot: HotspotDetail
  onClose: () => void
}

export default function SidePanel({ hotspot, onClose }: Props) {
  const levelColor = RISK_COLORS[hotspot.hotspot_level as RiskLevel] ?? '#6c757d'
  const hist = hotspot.historical

  return (
    <div className="side-panel bg-white border-start shadow">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center p-3 border-bottom bg-dark text-white">
        <span className="fw-bold">HOTSPOT DETAIL</span>
        <button className="btn-close btn-close-white" onClick={onClose} />
      </div>

      <div className="p-3 overflow-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>
        {/* Cluster ID badge */}
        <div className="text-center mb-3">
          <span className="badge fs-5 px-4 py-2" style={{ backgroundColor: levelColor }}>
            {hotspot.cluster_display_id}
          </span>
        </div>

        {/* Info rows */}
        <table className="table table-sm table-borderless mb-3">
          <tbody>
            <tr>
              <td className="text-muted small">Risk Level</td>
              <td>
                <span className="badge" style={{ backgroundColor: levelColor }}>
                  {hotspot.hotspot_level}
                </span>
              </td>
            </tr>
            <tr>
              <td className="text-muted small">Risk Score</td>
              <td><strong>{hotspot.risk_score.toFixed(0)}</strong></td>
            </tr>
            <tr>
              <td className="text-muted small">Total Kejadian</td>
              <td><strong>{hotspot.total_incidents}</strong></td>
            </tr>
            <tr>
              <td className="text-muted small">Jenis Dominan</td>
              <td><strong>{hotspot.dominant_type}</strong></td>
            </tr>
            <tr>
              <td className="text-muted small">Radius Cluster</td>
              <td>{hotspot.radius_meters?.toFixed(0)} Meter</td>
            </tr>
            <tr>
              <td className="text-muted small">Periode Data</td>
              <td>{hotspot.analysis_year}</td>
            </tr>
          </tbody>
        </table>

        {/* Historical Comparison */}
        <div className="card border-0 bg-light p-3 mb-3">
          <div className="fw-semibold mb-2 small">📅 Perbandingan Historis</div>
          {[2024, 2025, 2026].map(yr => {
            const count = hist[yr.toString() as '2024' | '2025' | '2026']
            return (
              <div key={yr} className="d-flex justify-content-between small py-1 border-bottom">
                <span className="text-muted">{yr}</span>
                <span className="fw-bold">{count !== undefined ? `${count} Kejadian` : '—'}</span>
              </div>
            )
          })}
          {hist.trend && (
            <div className="mt-2 text-center">
              <span className={`badge bg-${hist.trend === 'Meningkat' ? 'danger' : hist.trend === 'Menurun' ? 'success' : 'secondary'}`}>
                Trend: {hist.trend}
              </span>
            </div>
          )}
        </div>

        {/* Timeline Kejadian */}
        {hotspot.incidents.length > 0 && (
          <div>
            <div className="fw-semibold mb-2 small">🕐 Timeline Kejadian</div>
            <div className="timeline-list">
              {hotspot.incidents.slice(0, 20).map(inc => (
                <div key={inc.id} className="d-flex gap-2 py-2 border-bottom">
                  <div className="text-muted small" style={{ minWidth: 90 }}>
                    {inc.incident_date ?? `${inc.incident_year}`}
                  </div>
                  <div>
                    <div className="fw-semibold small">{inc.incident_type}</div>
                    <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                      {inc.location_name}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
