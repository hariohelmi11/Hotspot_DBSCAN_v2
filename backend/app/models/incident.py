from sqlalchemy import Column, BigInteger, Integer, Date, String, Text, Float, TIMESTAMP
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.database import Base


class PublicOrderIncident(Base):
    __tablename__ = "public_order_incidents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    incident_date = Column(Date)
    incident_year = Column(Integer, index=True)
    location_name = Column(Text)
    district = Column(String(100))
    subdistrict = Column(String(100))
    incident_type = Column(String(100))
    severity_score = Column(Integer)
    source = Column(String(50))
    article_url = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)
    hotspot_cluster_id = Column(BigInteger, nullable=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
