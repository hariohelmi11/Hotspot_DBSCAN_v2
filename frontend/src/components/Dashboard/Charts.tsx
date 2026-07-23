import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar, Pie, Line } from 'react-chartjs-2'
import type { DashboardData, RiskLevel } from '../../types'
import { RISK_COLORS, getIncidentTypeColor } from '../../types'

ChartJS.register(
  CategoryScale, LinearScale, BarElement, LineElement, PointElement,
  ArcElement, Title, Tooltip, Legend
)

interface Props {
  data: DashboardData | null
  loading: boolean
}

export default function Charts({ data, loading }: Props) {
  if (loading || !data) {
    return (
      <div className="row g-3">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="col-12 col-md-6">
            <div className="card border-0 shadow-sm p-4 text-center text-muted" style={{ height: 260 }}>
              Memuat grafik...
            </div>
          </div>
        ))}
      </div>
    )
  }

  // --- Tren Kejadian Tahunan ---
  const trendChart = {
    labels: data.trend.map(t => String(t.year)),
    datasets: [{
      label: 'Jumlah Kejadian',
      data: data.trend.map(t => t.count),
      borderColor: '#dc3545',
      backgroundColor: 'rgba(220,53,69,0.15)',
      fill: true,
      tension: 0.3,
    }],
  }

  // --- Distribusi Jenis Kejadian ---
  const typeColors = data.type_distribution.map(t => getIncidentTypeColor(t.incident_type))
  const typeChart = {
    labels: data.type_distribution.map(t => t.incident_type),
    datasets: [{
      label: 'Jumlah',
      data: data.type_distribution.map(t => t.count),
      backgroundColor: typeColors,
    }],
  }

  // --- Distribusi Risk Level ---
  const riskOrder = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
  const riskSorted = riskOrder
    .map(level => {
      const found = data.risk_distribution.find(r => r.risk_level === level)
      return { risk_level: level, count: found?.count ?? 0 }
    })
    .filter(r => r.count > 0)

  const riskChart = {
    labels: riskSorted.map(r => r.risk_level),
    datasets: [{
      data: riskSorted.map(r => r.count),
      backgroundColor: riskSorted.map(r => RISK_COLORS[r.risk_level as RiskLevel] ?? '#adb5bd'),
    }],
  }

  // --- Top 10 Wilayah ---
  const wilayahChart = {
    labels: data.top_wilayah.map(w => w.wilayah.replace('KOTA ADM. ', '')),
    datasets: [{
      label: 'Kejadian',
      data: data.top_wilayah.map(w => w.count),
      backgroundColor: '#0d6efd',
    }],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
  }

  // Opsi khusus bar distribusi jenis kejadian: sembunyikan label sumbu X
  const typeChartOptions = {
    ...chartOptions,
    scales: {
      x: { ticks: { display: false }, grid: { display: false } },
    },
  }

  return (
    <div className="row g-3">
      <div className="col-12 col-md-6">
        <div className="card border-0 shadow-sm p-3">
          <div className="fw-semibold mb-2 small text-muted">📈 Tren Kejadian Tahunan</div>
          <div style={{ height: 220 }}>
            <Line data={trendChart} options={{ ...chartOptions, plugins: { legend: { display: false } } }} />
          </div>
        </div>
      </div>

      <div className="col-12 col-md-6">
        <div className="card border-0 shadow-sm p-3">
          <div className="fw-semibold mb-2 small text-muted">📊 Distribusi Jenis Kejadian</div>
          <div style={{ height: 200 }}>
            <Bar data={typeChart} options={typeChartOptions} />
          </div>
          {/* Legenda warna per jenis kejadian */}
          <div className="d-flex flex-wrap gap-2 mt-2">
            {data.type_distribution.map((t, i) => (
              <div key={t.incident_type} className="d-flex align-items-center gap-1" style={{ fontSize: 11 }}>
                <span style={{
                  display: 'inline-block',
                  width: 10,
                  height: 10,
                  borderRadius: 2,
                  backgroundColor: typeColors[i],
                  flexShrink: 0,
                }} />
                <span className="text-muted" style={{ lineHeight: 1.2 }}>{t.incident_type}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="col-12 col-md-3">
        <div className="card border-0 shadow-sm p-3">
          <div className="fw-semibold mb-2 small text-muted">🎯 Distribusi Risk Level</div>
          <div style={{ height: 220 }}>
            <Pie data={riskChart} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
      </div>

      <div className="col-12 col-md-9">
        <div className="card border-0 shadow-sm p-3">
          <div className="fw-semibold mb-2 small text-muted">🏙️ Top 10 Wilayah Rawan</div>
          <div style={{ height: 220 }}>
            <Bar
              data={wilayahChart}
              options={{
                ...chartOptions,
                indexAxis: 'y' as const,
                plugins: { legend: { display: false } },
              }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
