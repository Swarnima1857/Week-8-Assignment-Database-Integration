"""
services/show_service.py — Business logic for shows
"""

from datetime import datetime
from fastapi import HTTPException
from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.show import ShowCreate

db = get_db()


def create_show(show: ShowCreate):
    result = db.shows.insert_one({
        "movie_id": to_object_id(show.movie_id),
        "theater_id": to_object_id(show.theater_id),
        "screen_no": show.screen_no,
        "start_time": datetime.strptime(show.start_time, "%Y-%m-%dT%H:%M:%S"),
        "price": show.price,
        "seat_map": [s.dict() for s in show.seat_map]
    })
    return {"inserted_id": str(result.inserted_id)}


def get_shows():
    return [serialize(s) for s in db.shows.find()]


def available_seats(show_id: str):
    oid = to_object_id(show_id)
    show = db.shows.find_one({"_id": oid})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return [s for s in show.get("seat_map", []) if s["status"] == "available"]


def seat_stats(show_id: str):
    """$unwind example: break seat_map into per-seat documents, then group by status."""
    oid = to_object_id(show_id)
    pipeline = [
        {"$match": {"_id": oid}},
        {"$unwind": "$seat_map"},
        {"$group": {"_id": "$seat_map.status", "count": {"$sum": 1}}}
    ]
    results = list(db.shows.aggregate(pipeline))
    return {"show_id": show_id, "seat_breakdown": results}
