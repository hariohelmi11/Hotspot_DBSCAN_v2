from fastapi import APIRouter, BackgroundTasks, Body
from typing import Optional

router = APIRouter()


@router.post("/etl/run")
def trigger_etl(
    source: str = Body("all", embed=True),
    year: int = Body(2024, embed=True),
):
    from app.database import SessionLocal
    from app.services.etl.pipeline import run_etl_pipeline
    db = SessionLocal()
    try:
        results = run_etl_pipeline(db, source=source, year=year)
        return {"status": "ETL pipeline completed", "source": source, "year": year, "results": results}
    finally:
        db.close()


@router.post("/dbscan/run")
def trigger_dbscan(
    year: Optional[int] = Body(None, embed=True),
):
    from app.database import SessionLocal
    from app.services.dbscan_service import run_dbscan
    db = SessionLocal()
    try:
        results = run_dbscan(db, year=year)
        return {"status": "DBSCAN analysis completed", "year": year, "results": results}
    finally:
        db.close()
