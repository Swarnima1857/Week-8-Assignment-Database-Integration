"""
schemas/ai_summary.py — Request/response shapes for the ai_summaries collection
"""

from pydantic import BaseModel
from typing import List


class AISummaryCreate(BaseModel):
    movie_id: str
    summary_text: str
    sentiment: str = ""
    based_on_review_ids: List[str] = []
    model_used: str = "claude-sonnet-5"
