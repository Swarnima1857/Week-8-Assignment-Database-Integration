"""
services/movie_service.py — Business logic for movies
"""

from datetime import datetime
from app.core.db import get_db
from app.utils.helpers import serialize
from app.schemas.movie import MovieCreate

db = get_db()


def create_movie(movie: MovieCreate):
    result = db.movies.insert_one({
        "title": movie.title,
        "genre": movie.genre,
        "cast": movie.cast,
        "duration_min": movie.duration_min,
        "release_date": datetime.strptime(movie.release_date, "%Y-%m-%d"),
        "language": movie.language
    })
    return {"inserted_id": str(result.inserted_id)}


def get_movies():
    return [serialize(m) for m in db.movies.find()]
