from sqlalchemy import Column, BigInteger, String, Integer, Boolean, TIMESTAMP, Text
from sqlalchemy.sql import func
from app.database import Base


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    execution_time = Column(TIMESTAMP, server_default=func.now())
    source = Column(String(100))
    total_records = Column(Integer, default=0)
    success = Column(Boolean, default=False)
    error_message = Column(Text)
