"""
services/theater_service.py — Business logic for theaters
"""

from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.theater import TheaterCreate

db = get_db()


def create_theater(theater: TheaterCreate):
    result = db.theaters.insert_one({
        "name": theater.name,
        "city": theater.city,
        "screens": [s.dict() for s in theater.screens]
    })
    return {"inserted_id": str(result.inserted_id)}


def get_theaters():
    return [serialize(t) for t in db.theaters.find()]


def screen_utilization(theater_id: str):
    """$unwind example: break the screens array into individual documents."""
    oid = to_object_id(theater_id)
    pipeline = [
        {"$match": {"_id": oid}},
        {"$unwind": "$screens"},
        {"$project": {
            "_id": 0,
            "screen_no": "$screens.screen_no",
            "capacity": "$screens.capacity",
            "type": "$screens.type"
        }}
    ]
    return list(db.theaters.aggregate(pipeline))
