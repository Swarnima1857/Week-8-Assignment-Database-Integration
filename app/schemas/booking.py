"""
schemas/booking.py — Request/response shapes for the bookings collection
"""

from pydantic import BaseModel
from typing import List, Optional


class Payment(BaseModel):
    status: str = "pending"
    method: Optional[str] = None
    txn_id: Optional[str] = None


class BookingCreate(BaseModel):
    user_id: str
    show_id: str
    seats_booked: List[str]
    total_amount: float
    payment: Payment = Payment()


class PaymentStatusUpdate(BaseModel):
    status: str
