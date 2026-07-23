from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_session
from app.services.dashboard_service import get_dashboard_data

router = APIRouter()


@router.get("")
def get_dashboard(
    year: Optional[int] = Query(None, description="Filter by year (2024/2025/2026)"),
    db: Session = Depends(get_session),
):
    return get_dashboard_data(db, year=year)
