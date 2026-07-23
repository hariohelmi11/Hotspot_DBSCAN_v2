import type { FilterState } from '../../types'

interface Props {
  filters: FilterState
  onFilterChange: (f: FilterState) => void
}

const YEARS = [2024, 2025, 2026]
const SOURCES = ['pemerintah', 'detik', 'kompas']
const INCIDENT_TYPES = ['TAWURAN', 'PKL', 'PENGEMIS', 'KRIMINALITAS', 'PREMANISME', 'MIRAS', 'GANGGUAN KETERTIBAN']

export default function FilterPanel({ filters, onFilterChange }: Props) {
  const set = (key: keyof FilterState, value: string | number | null) =>
    onFilterChange({ ...filters, [key]: value })

  return (
    <div className="filter-panel bg-white border-bottom px-3 py-2 d-flex flex-wrap gap-3 align-items-center">
      {/* Tahun */}
      <div className="d-flex align-items-center gap-2">
        <label className="form-label mb-0 fw-semibold small">Tahun</label>
        <select
          className="form-select form-select-sm"
          style={{ width: 110 }}
          value={filters.year ?? ''}
          onChange={e => set('year', e.target.value ? Number(e.target.value) : null)}
        >
          <option value="">Semua Tahun</option>
          {YEARS.map(y => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
      </div>

      {/* Jenis Kejadian */}
      <div className="d-flex align-items-center gap-2">
        <label className="form-label mb-0 fw-semibold small">Jenis Kejadian</label>
        <select
          className="form-select form-select-sm"
          style={{ width: 200 }}
          value={filters.incident_type ?? ''}
          onChange={e => set('incident_type', e.target.value || null)}
        >
          <option value="">Semua Jenis</option>
          {INCIDENT_TYPES.map(t => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      {/* Sumber Data */}
      <div className="d-flex align-items-center gap-2">
        <label className="form-label mb-0 fw-semibold small">Sumber Data</label>
        <select
          className="form-select form-select-sm"
          style={{ width: 140 }}
          value={filters.source ?? ''}
          onChange={e => set('source', e.target.value || null)}
        >
          <option value="">Semua Sumber</option>
          {SOURCES.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Wilayah */}
      <div className="d-flex align-items-center gap-2">
        <label className="form-label mb-0 fw-semibold small">Wilayah</label>
        <input
          type="text"
          className="form-control form-control-sm"
          style={{ width: 180 }}
          placeholder="Kota / Kecamatan..."
          value={filters.district ?? ''}
          onChange={e => set('district', e.target.value || null)}
        />
      </div>

      {/* Reset */}
      <button
        className="btn btn-sm btn-outline-secondary"
        onClick={() =>
          onFilterChange({ year: null, district: null, subdistrict: null, incident_type: null, source: null })
        }
      >
        Reset Filter
      </button>
    </div>
  )
}
