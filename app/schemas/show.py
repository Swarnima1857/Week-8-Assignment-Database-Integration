"""
schemas/show.py — Request/response shapes for the shows collection
"""

from pydantic import BaseModel
from typing import List


class Seat(BaseModel):
    seat_no: str
    status: str = "available"


class ShowCreate(BaseModel):
    movie_id: str
    theater_id: str
    screen_no: int = 1
    start_time: str    # format: "YYYY-MM-DDTHH:MM:SS"
    price: float
    seat_map: List[Seat] = []