from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class IncidentResponse(BaseModel):
    id: int
    incident_date: Optional[date] = None
    incident_year: Optional[int] = None
    location_name: Optional[str] = None
    district: Optional[str] = None
    subdistrict: Optional[str] = None
    incident_type: Optional[str] = None
    severity_score: Optional[int] = None
    source: Optional[str] = None
    article_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hotspot_cluster_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IncidentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[IncidentResponse]
