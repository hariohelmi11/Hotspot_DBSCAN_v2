from pydantic import BaseModel
from typing import List


class DashboardStats(BaseModel):
    total_incidents: int
    total_hotspots: int
    high_risk_areas: int
    critical_areas: int


class TrendData(BaseModel):
    year: int
    count: int


class TypeDistribution(BaseModel):
    incident_type: str
    count: int


class RiskDistribution(BaseModel):
    risk_level: str
    count: int


class TopWilayah(BaseModel):
    wilayah: str
    count: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    trend: List[TrendData]
    type_distribution: List[TypeDistribution]
    risk_distribution: List[RiskDistribution]
    top_wilayah: List[TopWilayah]
