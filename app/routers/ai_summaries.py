"""
routers/ai_summaries.py — URL endpoints for /ai-summaries
"""

from fastapi import APIRouter
from app.schemas.ai_summary import AISummaryCreate
from app.services import ai_summary_service

router = APIRouter(prefix="/ai-summaries", tags=["AI Summaries"])


@router.post("", status_code=201)
def create_ai_summary(summary: AISummaryCreate):
    return ai_summary_service.create_ai_summary(summary)


@router.get("")
def get_ai_summaries():
    return ai_summary_service.get_ai_summaries()
