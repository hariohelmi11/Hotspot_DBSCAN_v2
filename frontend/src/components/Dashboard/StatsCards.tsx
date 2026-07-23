import type { DashboardData } from '../../types'

interface Props {
  data: DashboardData | null
  loading: boolean
}

export default function StatsCards({ data, loading }: Props) {
  if (loading) {
    return (
      <div className="row g-3 mb-3">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="col-6 col-md-3">
            <div className="card border-0 shadow-sm p-3 placeholder-glow">
              <span className="placeholder col-6 mb-2"></span>
              <span className="placeholder col-10 placeholder-lg"></span>
            </div>
          </div>
        ))}
      </div>
    )
  }

  const stats = data?.stats

  const cards = [
    { label: 'Total Kejadian', value: stats?.total_incidents ?? 0, color: 'primary', icon: '📋' },
    { label: 'Total Hotspot', value: stats?.total_hotspots ?? 0, color: 'warning', icon: '🔥' },
    { label: 'Area High Risk', value: stats?.high_risk_areas ?? 0, color: 'danger', icon: '⚠️' },
    { label: 'Area Critical', value: stats?.critical_areas ?? 0, color: 'dark', icon: '🚨' },
  ]

  return (
    <div className="row g-3 mb-3">
      {cards.map(card => (
        <div key={card.label} className="col-6 col-md-3">
          <div className={`card border-0 shadow-sm border-start border-5 border-${card.color}`}>
            <div className="card-body py-3">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <div className="text-muted small">{card.label}</div>
                  <div className={`fs-3 fw-bold text-${card.color}`}>
                    {card.value.toLocaleString('id-ID')}
                  </div>
                </div>
                <div className="fs-1 opacity-25">{card.icon}</div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
