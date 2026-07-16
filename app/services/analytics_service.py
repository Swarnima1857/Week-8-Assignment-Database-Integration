"""
services/analytics_service.py — $facet example (multiple aggregations in one query)
"""

from app.core.db import get_db

db = get_db()


def movies_dashboard():
    """
    $facet runs 3 independent aggregations in a SINGLE query:
      1. total movie count
      2. movie count grouped by genre
      3. movie count grouped by language
    """
    pipeline = [
        {"$facet": {
            "total_movies": [{"$count": "count"}],
            "by_genre": [
                {"$unwind": "$genre"},
                {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ],
            "by_language": [
                {"$group": {"_id": "$language", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
        }}
    ]
    result = list(db.movies.aggregate(pipeline))
    return result[0] if result else {}
