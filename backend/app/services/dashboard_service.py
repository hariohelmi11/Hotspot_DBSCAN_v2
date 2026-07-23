from sqlalchemy.orm import Session
from app.repositories.incident_repository import IncidentRepository
from app.repositories.hotspot_repository import HotspotRepository


def get_dashboard_data(db: Session, year: int = None) -> dict:
    incident_repo = IncidentRepository(db)
    hotspot_repo = HotspotRepository(db)

    total_incidents, _ = incident_repo.get_all(year=year, page_size=0)

    hotspots = hotspot_repo.get_all(year=year)
    total_hotspots = len(hotspots)
    high_risk = sum(1 for h in hotspots if h.hotspot_level in ("HIGH", "CRITICAL"))
    critical = sum(1 for h in hotspots if h.hotspot_level == "CRITICAL")

    trend = [
        {"year": row[0], "count": row[1]}
        for row in incident_repo.count_by_year()
        if row[0]
    ]

    type_dist = [
        {"incident_type": row[0] or "UNKNOWN", "count": row[1]}
        for row in incident_repo.count_by_type()[:10]
    ]

    risk_dist = [
        {"risk_level": row[0] or "UNKNOWN", "count": row[1]}
        for row in hotspot_repo.count_by_risk_level(year=year)
    ]

    top_wilayah = [
        {"wilayah": row[0] or "UNKNOWN", "count": row[1]}
        for row in incident_repo.count_by_district(limit=10)
    ]

    return {
        "stats": {
            "total_incidents": total_incidents,
            "total_hotspots": total_hotspots,
            "high_risk_areas": high_risk,
            "critical_areas": critical,
        },
        "trend": trend,
        "type_distribution": type_dist,
        "risk_distribution": risk_dist,
        "top_wilayah": top_wilayah,
    }
