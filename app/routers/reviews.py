"""
routers/reviews.py — URL endpoints for /reviews
"""

from fastapi import APIRouter
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", status_code=201)
def create_review(review: ReviewCreate):
    return review_service.create_review(review)


@router.get("/with-user")
def reviews_with_user():
    return review_service.reviews_with_user()


@router.put("/{review_id}")
def update_review(review_id: str, review: ReviewUpdate):
    return review_service.update_review(review_id, review)


@router.delete("/{review_id}")
def delete_review(review_id: str):
    return review_service.delete_review(review_id)
