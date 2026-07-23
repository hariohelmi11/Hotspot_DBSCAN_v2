from sqlalchemy import Column, BigInteger, Integer, String, Numeric, Float, TIMESTAMP
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.database import Base


class HotspotCluster(Base):
    __tablename__ = "hotspot_clusters"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cluster_label = Column(Integer)
    cluster_display_id = Column(String(20))
    total_incidents = Column(Integer)
    dominant_type = Column(String(100))
    risk_score = Column(Numeric(10, 2))
    hotspot_level = Column(String(50))
    radius_meters = Column(Float)
    analysis_year = Column(Integer, index=True)
    centroid = Column(Geometry("POINT", srid=4326), nullable=True)
    centroid_lat = Column(Float)
    centroid_lon = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
