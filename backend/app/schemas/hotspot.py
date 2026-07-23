from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HotspotResponse(BaseModel):
    id: int
    cluster_display_id: Optional[str] = None
    cluster_label: Optional[int] = None
    total_incidents: Optional[int] = None
    dominant_type: Optional[str] = None
    risk_score: Optional[float] = None
    hotspot_level: Optional[str] = None
    radius_meters: Optional[float] = None
    analysis_year: Optional[int] = None
    centroid_lat: Optional[float] = None
    centroid_lon: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HotspotDetailResponse(HotspotResponse):
    incidents: List[dict] = []
    historical: dict = {}


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict


class GeoJSONCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]
