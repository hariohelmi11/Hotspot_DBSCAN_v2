import { useState } from 'react'
import { jobsApi } from '../services/api'

type JobStatus = 'idle' | 'running' | 'done' | 'error'

export default function AdminPage() {
  const [etlStatus, setEtlStatus] = useState<JobStatus>('idle')
  const [etlSource, setEtlSource] = useState('all')
  const [etlYear, setEtlYear] = useState(2024)
  const [dbscanStatus, setDbscanStatus] = useState<JobStatus>('idle')
  const [dbscanYear, setDbscanYear] = useState<number | null>(null)
  const [message, setMessage] = useState('')

  const runEtl = async () => {
    setEtlStatus('running')
    setMessage('')
    try {
      const result = await jobsApi.runEtl(etlSource, etlYear)
      setMessage(`ETL triggered: ${JSON.stringify(result)}`)
      setEtlStatus('done')
    } catch (e) {
      setMessage(`ETL Error: ${(e as Error).message}`)
      setEtlStatus('error')
    }
  }

  const runDbscan = async () => {
    setDbscanStatus('running')
    setMessage('')
    try {
      const result = await jobsApi.runDbscan(dbscanYear)
      setMessage(`DBSCAN triggered: ${JSON.stringify(result)}`)
      setDbscanStatus('done')
    } catch (e) {
      setMessage(`DBSCAN Error: ${(e as Error).message}`)
      setDbscanStatus('error')
    }
  }

  return (
    <div className="container py-4">
      <h4 className="fw-bold mb-4">⚙️ Admin Panel</h4>

      {message && (
        <div className="alert alert-info alert-dismissible" role="alert">
          <code>{message}</code>
          <button type="button" className="btn-close" onClick={() => setMessage('')} />
        </div>
      )}

      <div className="row g-4">
        {/* ETL Panel */}
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-header fw-bold bg-primary text-white">
              📥 Jalankan ETL Pipeline
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label">Sumber Data</label>
                <select
                  className="form-select"
                  value={etlSource}
                  onChange={e => setEtlSource(e.target.value)}
                >
                  <option value="all">Semua (Pemerintah + News)</option>
                  <option value="government">Pemerintah (data-rawan.xls)</option>
                  <option value="news">News Scraping</option>
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Tahun</label>
                <select
                  className="form-select"
                  value={etlYear}
                  onChange={e => setEtlYear(Number(e.target.value))}
                >
                  <option value={2024}>2024</option>
                  <option value={2025}>2025</option>
                  <option value={2026}>2026</option>
                </select>
              </div>
              <button
                className="btn btn-primary w-100"
                onClick={runEtl}
                disabled={etlStatus === 'running'}
              >
                {etlStatus === 'running' ? (
                  <><span className="spinner-border spinner-border-sm me-2" />Berjalan...</>
                ) : 'Jalankan ETL'}
              </button>
              {etlStatus === 'done' && <div className="text-success mt-2 small">✅ ETL dipicu di background</div>}
            </div>
          </div>
        </div>

        {/* DBSCAN Panel */}
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-header fw-bold bg-danger text-white">
              🔬 Jalankan Analisis DBSCAN
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label">Tahun Analisis</label>
                <select
                  className="form-select"
                  value={dbscanYear ?? ''}
                  onChange={e => setDbscanYear(e.target.value ? Number(e.target.value) : null)}
                >
                  <option value="">Semua Tahun</option>
                  <option value={2024}>2024</option>
                  <option value={2025}>2025</option>
                  <option value={2026}>2026</option>
                </select>
              </div>
              <div className="alert alert-warning small py-2">
                ⚠️ Proses ini akan menghapus hotspot lama dan membuat ulang berdasarkan data terkini.
              </div>
              <button
                className="btn btn-danger w-100"
                onClick={runDbscan}
                disabled={dbscanStatus === 'running'}
              >
                {dbscanStatus === 'running' ? (
                  <><span className="spinner-border spinner-border-sm me-2" />Berjalan...</>
                ) : 'Jalankan DBSCAN'}
              </button>
              {dbscanStatus === 'done' && <div className="text-success mt-2 small">✅ DBSCAN dipicu di background</div>}
            </div>
          </div>
        </div>
      </div>

      {/* API Docs link */}
      <div className="mt-4 text-muted small">
        📖 <a href="/docs" target="_blank" rel="noopener noreferrer">Buka Swagger API Docs</a>
      </div>
    </div>
  )
}
