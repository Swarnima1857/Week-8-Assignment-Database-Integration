"""
routers/users.py — URL endpoints for /users (delegates to user_service)
"""

from fastapi import APIRouter
from app.schemas.user import UserCreate, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=201)
def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.get("")
def get_users():
    return user_service.get_users()


@router.get("/{user_id}")
def get_user(user_id: str):
    return user_service.get_user(user_id)


@router.put("/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: str):
    return user_service.delete_user(user_id)
