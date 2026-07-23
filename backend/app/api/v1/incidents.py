from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_session
from app.repositories.incident_repository import IncidentRepository

router = APIRouter()


@router.get("")
def list_incidents(
    year: Optional[int] = Query(None),
    district: Optional[str] = Query(None),
    subdistrict: Optional[str] = Query(None),
    incident_type: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, le=500),
    db: Session = Depends(get_session),
):
    repo = IncidentRepository(db)
    total, items = repo.get_all(
        year=year,
        district=district,
        subdistrict=subdistrict,
        incident_type=incident_type,
        source=source,
        page=page,
        page_size=page_size,
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_serialize(i) for i in items],
    }


@router.get("/{incident_id}")
def get_incident(incident_id: int, db: Session = Depends(get_session)):
    repo = IncidentRepository(db)
    incident = repo.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return _serialize(incident)


def _serialize(i) -> dict:
    return {
        "id": i.id,
        "incident_date": str(i.incident_date) if i.incident_date else None,
        "incident_year": i.incident_year,
        "location_name": i.location_name,
        "district": i.district,
        "subdistrict": i.subdistrict,
        "incident_type": i.incident_type,
        "severity_score": i.severity_score,
        "source": i.source,
        "article_url": i.article_url,
        "latitude": i.latitude,
        "longitude": i.longitude,
        "hotspot_cluster_id": i.hotspot_cluster_id,
    }
