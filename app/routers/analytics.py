"""
routers/analytics.py — URL endpoints for dashboard-style aggregations ($facet)
"""

from fastapi import APIRouter
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/movies-dashboard")
def movies_dashboard():
    return analytics_service.movies_dashboard()
