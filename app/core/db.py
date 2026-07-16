"""
core/db.py — MongoDB connection handler
"""

from pymongo import MongoClient
from app.core.config import MONGO_URI, DB_NAME


def get_db():
    """Returns the database handle. Import this wherever a service needs the DB."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]