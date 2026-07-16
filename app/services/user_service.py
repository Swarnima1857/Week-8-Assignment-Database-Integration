"""
services/user_service.py — Business logic for users (talks to MongoDB directly)
"""

from datetime import datetime
from fastapi import HTTPException
from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.user import UserCreate, UserUpdate

db = get_db()


def create_user(user: UserCreate):
    # server-side business validation: no duplicate emails
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="A user with this email already exists")

    result = db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "addresses": [a.dict() for a in user.addresses],
        "created_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


def get_users():
    return [serialize(u) for u in db.users.find()]


def get_user(user_id: str):
    oid = to_object_id(user_id)
    user = db.users.find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize(user)


def update_user(user_id: str, user: UserUpdate):
    oid = to_object_id(user_id)
    updates = {k: v for k, v in user.dict().items() if v is not None}
    result = db.users.update_one({"_id": oid}, {"$set": updates})
    return {"matched": result.matched_count, "modified": result.modified_count}


def delete_user(user_id: str):
    oid = to_object_id(user_id)
    result = db.users.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}
