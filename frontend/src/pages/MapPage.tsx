import { useState } from 'react'
import Header from '../components/Header'
import FilterPanel from '../components/Filter/FilterPanel'
import MapView from '../components/Map/MapView'
import StatsCards from '../components/Dashboard/StatsCards'
import Charts from '../components/Dashboard/Charts'
import SidePanel from '../components/HotspotDetail/SidePanel'
import AdminPage from './AdminPage'
import { useDashboard } from '../hooks/useDashboard'
import { useHotspotsGeoJSON } from '../hooks/useHotspots'
import { useIncidentsGeoJSON } from '../hooks/useIncidents'
import { hotspotsApi } from '../services/api'
import type { FilterState, HotspotDetail, ActiveLayers } from '../types'

const DEFAULT_FILTERS: FilterState = {
  year: null, district: null, subdistrict: null, incident_type: null, source: null,
}

export default function MapPage() {
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS)
  const [selectedHotspot, setSelectedHotspot] = useState<HotspotDetail | null>(null)
  const [sidePanelOpen, setSidePanelOpen] = useState(false)
  const [activeLayers, setActiveLayers] = useState<ActiveLayers>({
    markers: true, heatmap: true, hotspots: true,
  })
  const [activeTab, setActiveTab] = useState<'map' | 'admin'>('map')

  const { data: dashboardData, loading: dashboardLoading } = useDashboard(filters.year)
  const { data: hotspotsGeoJSON } = useHotspotsGeoJSON(filters)
  const { data: incidentsGeoJSON } = useIncidentsGeoJSON(filters)

  const handleHotspotClick = async (id: number) => {
    try {
      const detail = await hotspotsApi.getDetail(id)
      setSelectedHotspot(detail)
      setSidePanelOpen(true)
    } catch (e) {
      console.error('Failed to load hotspot detail:', e)
    }
  }

  return (
    <div className="app-layout">
      <Header />

      {/* Tab Navigation */}
      <div className="bg-white border-bottom px-3">
        <ul className="nav nav-tabs border-0">
          <li className="nav-item">
            <button
              className={`nav-link ${activeTab === 'map' ? 'active fw-semibold' : ''}`}
              onClick={() => setActiveTab('map')}
            >
              🗺️ Peta GIS
            </button>
          </li>
          <li className="nav-item">
            <button
              className={`nav-link ${activeTab === 'admin' ? 'active fw-semibold' : ''}`}
              onClick={() => setActiveTab('admin')}
            >
              ⚙️ Admin
            </button>
          </li>
        </ul>
      </div>

      {activeTab === 'admin' ? (
        <AdminPage />
      ) : (
        <>
          <FilterPanel filters={filters} onFilterChange={setFilters} />

          {/* Map + SidePanel row */}
          <div className="map-row">
            <div className={`map-container ${sidePanelOpen ? 'with-panel' : ''}`}>
              <MapView
                hotspotsGeoJSON={hotspotsGeoJSON}
                incidentsGeoJSON={incidentsGeoJSON}
                activeLayers={activeLayers}
                onLayersChange={setActiveLayers}
                onHotspotClick={handleHotspotClick}
              />
            </div>
            {sidePanelOpen && selectedHotspot && (
              <SidePanel hotspot={selectedHotspot} onClose={() => setSidePanelOpen(false)} />
            )}
          </div>

          {/* Dashboard */}
          <div className="dashboard-section container-fluid py-3 bg-light">
            <StatsCards data={dashboardData} loading={dashboardLoading} />
            <Charts data={dashboardData} loading={dashboardLoading} />
          </div>
        </>
      )}
    </div>
  )
}
