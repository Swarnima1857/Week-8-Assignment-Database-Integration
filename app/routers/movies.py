"""
routers/movies.py — URL endpoints for /movies
"""

from fastapi import APIRouter
from app.schemas.movie import MovieCreate
from app.services import movie_service

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("", status_code=201)
def create_movie(movie: MovieCreate):
    return movie_service.create_movie(movie)


@router.get("")
def get_movies():
    return movie_service.get_movies()
