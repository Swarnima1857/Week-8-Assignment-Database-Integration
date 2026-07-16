"""
routers/bookings.py — URL endpoints for /bookings
"""

from fastapi import APIRouter
from app.schemas.booking import BookingCreate, PaymentStatusUpdate
from app.services import booking_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", status_code=201)
def create_booking(booking: BookingCreate):
    return booking_service.create_booking(booking)


@router.get("")
def get_bookings():
    return booking_service.get_bookings()


@router.get("/with-user")
def bookings_with_user():
    return booking_service.bookings_with_user()


@router.put("/{booking_id}/payment-status")
def update_payment_status(booking_id: str, payload: PaymentStatusUpdate):
    return booking_service.update_payment_status(booking_id, payload)


@router.delete("/{booking_id}")
def delete_booking(booking_id: str):
    return booking_service.delete_booking(booking_id)
