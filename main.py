"""
main.py — Application entry point.
Creates the FastAPI app and plugs in every router.

Run: python3 -m uvicorn main:app --reload
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from app.routers import users, movies, theaters, shows, bookings, reviews, ai_summaries, analytics

app = FastAPI(title="Movie Ticket Booking System API")

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(theaters.router)
app.include_router(shows.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(ai_summaries.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Movie Ticket Booking System API is running"}