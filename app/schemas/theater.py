"""
schemas/theater.py — Request/response shapes for the theaters collection
"""

from pydantic import BaseModel
from typing import List


class Screen(BaseModel):
    screen_no: int
    capacity: int
    type: str


class TheaterCreate(BaseModel):
    name: str
    city: str
    screens: List[Screen] = []