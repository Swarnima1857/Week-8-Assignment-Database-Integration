"""
utils/helpers.py — Small reusable functions used across services
"""

from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from fastapi import HTTPException


def serialize(doc):
    """Convert MongoDB's ObjectId/datetime into JSON-friendly strings."""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        if isinstance(value, list):
            doc[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return doc


def to_object_id(id_str):
    """Convert a string ID from a URL/request into a Mongo ObjectId, or raise a clean 400 error."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
