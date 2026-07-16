"""
services/review_service.py — Business logic for reviews
"""

from datetime import datetime
from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.review import ReviewCreate, ReviewUpdate

db = get_db()


def create_review(review: ReviewCreate):
    result = db.reviews.insert_one({
        "movie_id": to_object_id(review.movie_id),
        "user_id": to_object_id(review.user_id),
        "rating": review.rating,
        "comment": review.comment,
        "created_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


def reviews_with_user():
    """$lookup example: join reviews with the user who wrote them."""
    pipeline = [
        {"$lookup": {"from": "users", "localField": "user_id",
                      "foreignField": "_id", "as": "user_info"}}
    ]
    results = [serialize(doc) for doc in db.reviews.aggregate(pipeline)]
    for r in results:
        r["user_info"] = [serialize(u) for u in r.get("user_info", [])]
    return results


def update_review(review_id: str, review: ReviewUpdate):
    oid = to_object_id(review_id)
    updates = {k: v for k, v in review.dict().items() if v is not None}
    result = db.reviews.update_one({"_id": oid}, {"$set": updates})
    return {"modified": result.modified_count}


def delete_review(review_id: str):
    oid = to_object_id(review_id)
    result = db.reviews.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}
