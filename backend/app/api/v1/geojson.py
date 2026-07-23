from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_session
from app.repositories.hotspot_repository import HotspotRepository
from app.repositories.incident_repository import IncidentRepository

router = APIRouter()


@router.get("/hotspots")
def hotspots_geojson(
    year: Optional[int] = Query(None),
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    repo = HotspotRepository(db)
    hotspots = repo.get_all(year=year, risk_level=risk_level)

    features = []
    for h in hotspots:
        if h.centroid_lat is None or h.centroid_lon is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [h.centroid_lon, h.centroid_lat],
            },
            "properties": {
                "id": h.id,
                "cluster_display_id": h.cluster_display_id,
                "total_incidents": h.total_incidents,
                "dominant_type": h.dominant_type,
                "risk_score": float(h.risk_score) if h.risk_score else 0.0,
                "hotspot_level": h.hotspot_level,
                "radius_meters": h.radius_meters,
                "analysis_year": h.analysis_year,
            },
        })
    return {"type": "FeatureCollection", "features": features}


@router.get("/incidents")
def incidents_geojson(
    year: Optional[int] = Query(None),
    district: Optional[str] = Query(None),
    incident_type: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    repo = IncidentRepository(db)
    _, incidents = repo.get_all(
        year=year,
        district=district,
        incident_type=incident_type,
        source=source,
        page=1,
        page_size=2000,
    )

    features = []
    for i in incidents:
        if i.latitude is None or i.longitude is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [i.longitude, i.latitude],
            },
            "properties": {
                "id": i.id,
                "incident_type": i.incident_type,
                "incident_date": str(i.incident_date) if i.incident_date else None,
                "location_name": i.location_name,
                "district": i.district,
                "subdistrict": i.subdistrict,
                "severity_score": i.severity_score,
                "source": i.source,
                "latitude": i.latitude,
                "longitude": i.longitude,
            },
        })
    return {"type": "FeatureCollection", "features": features}
