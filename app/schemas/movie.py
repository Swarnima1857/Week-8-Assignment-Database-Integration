"""
schemas/movie.py — Request/response shapes for the movies collection
"""

from pydantic import BaseModel
from typing import List


class MovieCreate(BaseModel):
    title: str
    genre: List[str] = []
    cast: List[str] = []
    duration_min: int
    release_date: str    # format: "YYYY-MM-DD"
    language: str = ""
