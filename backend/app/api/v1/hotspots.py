from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_session
from app.repositories.hotspot_repository import HotspotRepository
from app.repositories.incident_repository import IncidentRepository

router = APIRouter()


@router.get("")
def list_hotspots(
    year: Optional[int] = Query(None),
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    repo = HotspotRepository(db)
    hotspots = repo.get_all(year=year, risk_level=risk_level)
    return [_hotspot_dict(h) for h in hotspots]


@router.get("/{hotspot_id}")
def get_hotspot_detail(
    hotspot_id: int,
    db: Session = Depends(get_session),
):
    hotspot_repo = HotspotRepository(db)
    incident_repo = IncidentRepository(db)

    hotspot = hotspot_repo.get_by_id(hotspot_id)
    if not hotspot:
        raise HTTPException(status_code=404, detail="Hotspot not found")

    incidents = incident_repo.get_by_cluster(hotspot_id)
    historical = _build_historical(hotspot.cluster_label, hotspot_repo)

    result = _hotspot_dict(hotspot)
    result["incidents"] = [_incident_dict(i) for i in incidents[:50]]
    result["historical"] = historical
    return result


def _build_historical(cluster_label: int, repo: HotspotRepository) -> dict:
    historical: dict = {}
    for yr in [2024, 2025, 2026]:
        hotspots = repo.get_all(year=yr)
        match = next((h for h in hotspots if h.cluster_label == cluster_label), None)
        if match:
            historical[str(yr)] = match.total_incidents

    if len(historical) >= 2:
        years = sorted(historical.keys())
        first_val = historical[years[0]]
        last_val = historical[years[-1]]
        trend = "Meningkat" if last_val > first_val else "Menurun" if last_val < first_val else "Stabil"
    else:
        trend = "Data tidak cukup"

    historical["trend"] = trend
    return historical


def _hotspot_dict(h) -> dict:
    return {
        "id": h.id,
        "cluster_display_id": h.cluster_display_id,
        "cluster_label": h.cluster_label,
        "total_incidents": h.total_incidents,
        "dominant_type": h.dominant_type,
        "risk_score": float(h.risk_score) if h.risk_score else 0.0,
        "hotspot_level": h.hotspot_level,
        "radius_meters": h.radius_meters,
        "analysis_year": h.analysis_year,
        "centroid_lat": h.centroid_lat,
        "centroid_lon": h.centroid_lon,
    }


def _incident_dict(i) -> dict:
    return {
        "id": i.id,
        "incident_date": str(i.incident_date) if i.incident_date else None,
        "incident_year": i.incident_year,
        "incident_type": i.incident_type,
        "location_name": i.location_name,
        "district": i.district,
        "subdistrict": i.subdistrict,
        "severity_score": i.severity_score,
        "source": i.source,
        "article_url": i.article_url,
    }
