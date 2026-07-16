"""
schemas/user.py — Request/response shapes for the users collection
"""

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional


class Address(BaseModel):
    label: str = "Home"
    city: str
    pincode: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    addresses: List[Address] = []

    @validator("phone")
    def phone_must_be_10_digits(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("phone must be exactly 10 digits")
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
