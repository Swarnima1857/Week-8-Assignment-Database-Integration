"""
routers/theaters.py — URL endpoints for /theaters
"""

from fastapi import APIRouter
from app.schemas.theater import TheaterCreate
from app.services import theater_service

router = APIRouter(prefix="/theaters", tags=["Theaters"])


@router.post("", status_code=201)
def create_theater(theater: TheaterCreate):
    return theater_service.create_theater(theater)


@router.get("")
def get_theaters():
    return theater_service.get_theaters()


@router.get("/{theater_id}/screen-utilization")
def screen_utilization(theater_id: str):
    return theater_service.screen_utilization(theater_id)
