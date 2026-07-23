from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.models.hotspot import HotspotCluster


class HotspotRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, hotspot_id: int) -> Optional[HotspotCluster]:
        return self.db.query(HotspotCluster).filter(HotspotCluster.id == hotspot_id).first()

    def get_all(
        self,
        year: Optional[int] = None,
        risk_level: Optional[str] = None,
    ) -> List[HotspotCluster]:
        query = self.db.query(HotspotCluster)
        if year:
            query = query.filter(HotspotCluster.analysis_year == year)
        if risk_level:
            query = query.filter(HotspotCluster.hotspot_level == risk_level.upper())
        return query.order_by(HotspotCluster.risk_score.desc()).all()

    def count_by_risk_level(self, year: Optional[int] = None):
        query = self.db.query(
            HotspotCluster.hotspot_level,
            func.count(HotspotCluster.id).label("count"),
        )
        if year:
            query = query.filter(HotspotCluster.analysis_year == year)
        return query.group_by(HotspotCluster.hotspot_level).all()

    def delete_by_year(self, year: int):
        self.db.query(HotspotCluster).filter(
            HotspotCluster.analysis_year == year
        ).delete(synchronize_session=False)
        self.db.commit()

    def create(self, hotspot_data: dict) -> HotspotCluster:
        hotspot = HotspotCluster(**hotspot_data)
        self.db.add(hotspot)
        self.db.flush()
        self.db.refresh(hotspot)
        return hotspot
