from sqlalchemy.orm import Session
from sqlalchemy import func, update
from typing import Optional, List
from app.models.incident import PublicOrderIncident


class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, incident_id: int) -> Optional[PublicOrderIncident]:
        return self.db.query(PublicOrderIncident).filter(
            PublicOrderIncident.id == incident_id
        ).first()

    def get_all(
        self,
        year: Optional[int] = None,
        district: Optional[str] = None,
        subdistrict: Optional[str] = None,
        incident_type: Optional[str] = None,
        source: Optional[str] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[int, List[PublicOrderIncident]]:
        query = self.db.query(PublicOrderIncident)
        if year:
            query = query.filter(PublicOrderIncident.incident_year == year)
        if district:
            query = query.filter(PublicOrderIncident.district.ilike(f"%{district}%"))
        if subdistrict:
            query = query.filter(PublicOrderIncident.subdistrict.ilike(f"%{subdistrict}%"))
        if incident_type:
            query = query.filter(PublicOrderIncident.incident_type.ilike(f"%{incident_type}%"))
        if source:
            query = query.filter(PublicOrderIncident.source == source)
        total = query.count()
        if page_size == 0:
            return total, []
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return total, items

    def get_by_cluster(self, hotspot_cluster_id: int) -> List[PublicOrderIncident]:
        return self.db.query(PublicOrderIncident).filter(
            PublicOrderIncident.hotspot_cluster_id == hotspot_cluster_id
        ).order_by(PublicOrderIncident.incident_date.desc()).all()

    def get_all_with_coords(self, year: Optional[int] = None) -> List[PublicOrderIncident]:
        query = self.db.query(PublicOrderIncident).filter(
            PublicOrderIncident.latitude.isnot(None),
            PublicOrderIncident.longitude.isnot(None),
        )
        if year:
            query = query.filter(PublicOrderIncident.incident_year == year)
        return query.all()

    def count_by_year(self):
        return self.db.query(
            PublicOrderIncident.incident_year,
            func.count(PublicOrderIncident.id).label("count"),
        ).group_by(PublicOrderIncident.incident_year).order_by(
            PublicOrderIncident.incident_year
        ).all()

    def count_by_type(self):
        return self.db.query(
            PublicOrderIncident.incident_type,
            func.count(PublicOrderIncident.id).label("count"),
        ).group_by(PublicOrderIncident.incident_type).order_by(
            func.count(PublicOrderIncident.id).desc()
        ).all()

    def count_by_district(self, limit: int = 10):
        return self.db.query(
            PublicOrderIncident.district,
            func.count(PublicOrderIncident.id).label("count"),
        ).group_by(PublicOrderIncident.district).order_by(
            func.count(PublicOrderIncident.id).desc()
        ).limit(limit).all()

    def bulk_insert(self, incidents: List[dict]):
        self.db.bulk_insert_mappings(PublicOrderIncident, incidents)
        self.db.commit()

    def bulk_update_cluster(self, mappings: List[dict]):
        """Bulk update hotspot_cluster_id. Each dict: {id, hotspot_cluster_id}"""
        self.db.bulk_update_mappings(PublicOrderIncident, mappings)

    def reset_clusters(self, year: Optional[int] = None):
        query = self.db.query(PublicOrderIncident)
        if year:
            query = query.filter(PublicOrderIncident.incident_year == year)
        query.update({"hotspot_cluster_id": None}, synchronize_session=False)
        self.db.commit()
