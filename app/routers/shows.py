"""
routers/shows.py — URL endpoints for /shows
"""

from fastapi import APIRouter
from app.schemas.show import ShowCreate
from app.services import show_service

router = APIRouter(prefix="/shows", tags=["Shows"])


@router.post("", status_code=201)
def create_show(show: ShowCreate):
    return show_service.create_show(show)


@router.get("")
def get_shows():
    return show_service.get_shows()


@router.get("/{show_id}/available-seats")
def available_seats(show_id: str):
    return show_service.available_seats(show_id)


@router.get("/{show_id}/seat-stats")
def seat_stats(show_id: str):
    return show_service.seat_stats(show_id)
