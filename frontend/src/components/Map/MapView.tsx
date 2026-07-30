import { useEffect } from 'react'
import { MapContainer, TileLayer, LayersControl, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet.fullscreen/dist/Control.FullScreen.css'
import { FullScreen } from 'leaflet.fullscreen'
import 'leaflet/dist/leaflet.css'
import MarkerLayer from './MarkerLayer'
import HotspotLayer from './HotspotLayer'
import HeatmapLayer from './HeatmapLayer'
import FilterPanel from '../Filter/FilterPanel'
import type { GeoJSONCollection, ActiveLayers, FilterState } from '../../types'

// Fix default Leaflet icon URLs for bundlers
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

interface Props {
  hotspotsGeoJSON: GeoJSONCollection | null
  incidentsGeoJSON: GeoJSONCollection | null
  activeLayers: ActiveLayers
  onLayersChange: (layers: ActiveLayers) => void
  onHotspotClick: (id: number) => void
  filters: FilterState
  onFilterChange: (filters: FilterState) => void
}

// Jakarta center
const JAKARTA_CENTER: [number, number] = [-6.2, 106.816666]
const DEFAULT_ZOOM = 11

function FullscreenControl() {
  const map = useMap()
  useEffect(() => {
    const control = new FullScreen({
      position: 'bottomleft',
      title: 'Expand',
      titleCancel: 'Exit fullscreen mode',
      forceSeparateButton: true,
      fullscreenElement: document.querySelector('.map-row') as HTMLElement || false,
    })
    map.addControl(control)
    return () => {
      map.removeControl(control)
    }
  }, [map])
  return null
}

export default function MapView({
  hotspotsGeoJSON,
  incidentsGeoJSON,
  activeLayers,
  onLayersChange,
  onHotspotClick,
  filters,
  onFilterChange,
}: Props) {
  return (
    <div className="map-wrapper">
      {/* Layer toggles & Filters */}
      <div className="map-layer-controls d-flex flex-wrap gap-3 align-items-center">
        <div className="d-flex gap-1 border-end pe-3">
          {(Object.keys(activeLayers) as (keyof ActiveLayers)[]).map(key => (
            <button
              key={key}
              className={`btn btn-sm me-1 ${activeLayers[key] ? 'btn-dark' : 'btn-outline-dark'}`}
              onClick={() => onLayersChange({ ...activeLayers, [key]: !activeLayers[key] })}
            >
              {key === 'markers' ? '📍 Marker' : key === 'heatmap' ? '🌡️ Heatmap' : '🔥 Hotspot'}
            </button>
          ))}
        </div>
        <FilterPanel filters={filters} onFilterChange={onFilterChange} />
      </div>

      <MapContainer
        center={JAKARTA_CENTER}
        zoom={DEFAULT_ZOOM}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom
      >
        <FullscreenControl />
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="OpenStreetMap">
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="CartoDB Dark">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://carto.com/">CARTO</a>'
            />
          </LayersControl.BaseLayer>
        </LayersControl>

        {activeLayers.heatmap && <HeatmapLayer incidentsGeoJSON={incidentsGeoJSON} />}
        {activeLayers.markers && <MarkerLayer incidentsGeoJSON={incidentsGeoJSON} />}
        {activeLayers.hotspots && (
          <HotspotLayer
            hotspotsGeoJSON={hotspotsGeoJSON}
            onHotspotClick={onHotspotClick}
          />
        )}
      </MapContainer>
    </div>
  )
}
