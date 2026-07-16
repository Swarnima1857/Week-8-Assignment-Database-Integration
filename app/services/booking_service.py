"""
services/booking_service.py — Business logic for bookings
"""

from datetime import datetime
from fastapi import HTTPException
from app.core.db import get_db
from app.utils.helpers import serialize, to_object_id
from app.schemas.booking import BookingCreate, PaymentStatusUpdate

db = get_db()


def create_booking(booking: BookingCreate):
    show_oid = to_object_id(booking.show_id)

    show = db.shows.find_one({"_id": show_oid})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    # server-side validation: seats must exist and be available
    seat_status = {s["seat_no"]: s["status"] for s in show.get("seat_map", [])}
    for seat_no in booking.seats_booked:
        if seat_no not in seat_status:
            raise HTTPException(status_code=400, detail=f"Seat {seat_no} does not exist on this show")
        if seat_status[seat_no] != "available":
            raise HTTPException(status_code=409, detail=f"Seat {seat_no} is already booked")

    result = db.bookings.insert_one({
        "user_id": to_object_id(booking.user_id),
        "show_id": show_oid,
        "seats_booked": booking.seats_booked,
        "total_amount": booking.total_amount,
        "payment": booking.payment.dict(),
        "booked_at": datetime.utcnow()
    })

    for seat_no in booking.seats_booked:
        db.shows.update_one(
            {"_id": show_oid, "seat_map.seat_no": seat_no},
            {"$set": {"seat_map.$.status": "booked"}}
        )
    return {"inserted_id": str(result.inserted_id)}


def get_bookings():
    return [serialize(b) for b in db.bookings.find()]


def bookings_with_user():
    """$lookup example: join bookings with the user who made them."""
    pipeline = [
        {"$lookup": {"from": "users", "localField": "user_id",
                      "foreignField": "_id", "as": "user_info"}}
    ]
    results = [serialize(doc) for doc in db.bookings.aggregate(pipeline)]
    for r in results:
        r["user_info"] = [serialize(u) for u in r.get("user_info", [])]
    return results


def update_payment_status(booking_id: str, payload: PaymentStatusUpdate):
    oid = to_object_id(booking_id)
    result = db.bookings.update_one({"_id": oid}, {"$set": {"payment.status": payload.status}})
    return {"modified": result.modified_count}


def delete_booking(booking_id: str):
    oid = to_object_id(booking_id)
    result = db.bookings.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}
