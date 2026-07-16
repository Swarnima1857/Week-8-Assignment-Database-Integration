"""
services/ai_summary_service.py — Business logic for ai_summaries
"""

from datetime import datetime
from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.ai_summary import AISummaryCreate

db = get_db()


def create_ai_summary(summary: AISummaryCreate):
    result = db.ai_summaries.insert_one({
        "movie_id": to_object_id(summary.movie_id),
        "summary_text": summary.summary_text,
        "sentiment": summary.sentiment,
        "based_on_review_ids": [to_object_id(r) for r in summary.based_on_review_ids],
        "model_used": summary.model_used,
        "generated_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


def get_ai_summaries():
    return [serialize(s) for s in db.ai_summaries.find()]
