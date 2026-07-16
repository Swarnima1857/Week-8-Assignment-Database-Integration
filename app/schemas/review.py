"""
schemas/review.py — Request/response shapes for the reviews collection
"""

from pydantic import BaseModel, Field
from typing import Optional


class ReviewCreate(BaseModel):
    movie_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str = ""


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
