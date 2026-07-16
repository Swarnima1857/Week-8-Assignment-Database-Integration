# Movie Ticket Booking System — MongoDB + FastAPI

A backend REST API for a movie ticket booking system, built with **FastAPI** and **MongoDB (PyMongo)**, following a layered architecture (routers → services → schemas).

---

## Tech Stack

- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Database:** MongoDB (via PyMongo)
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Testing:** Postman / Swagger UI

---

## Project Structure

```
movie_project/
├── app/
│   ├── core/
│   │   ├── config.py          # MongoDB URI, DB name
│   │   └── db.py              # Database connection handler
│   ├── routers/                # API endpoint definitions
│   │   ├── users.py
│   │   ├── movies.py
│   │   ├── theaters.py
│   │   ├── shows.py
│   │   ├── bookings.py
│   │   ├── reviews.py
│   │   ├── ai_summaries.py
│   │   └── analytics.py
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── theater.py
│   │   ├── show.py
│   │   ├── booking.py
│   │   ├── review.py
│   │   └── ai_summary.py
│   ├── services/                # Business logic + database operations
│   │   ├── user_service.py
│   │   ├── movie_service.py
│   │   ├── theater_service.py
│   │   ├── show_service.py
│   │   ├── booking_service.py
│   │   ├── review_service.py
│   │   ├── ai_summary_service.py
│   │   └── analytics_service.py
│   └── utils/
│       └── helpers.py           # serialize(), to_object_id()
├── main.py                      # App entry point — wires up all routers
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Make sure MongoDB is running locally
```bash
# Should be reachable at:
mongodb://localhost:27017/
```

### 3. Run the server
```bash
python3 -m uvicorn main:app --reload
```

### 4. Open API docs
```
http://localhost:8000/docs
```

---

## Database Design

### Collections
| Collection | Purpose |
|---|---|
| `users` | Customer accounts and saved addresses |
| `movies` | Movie catalogue |
| `theaters` | Theater and screen info |
| `shows` | A movie playing at a specific theater/screen/time, with seat map |
| `bookings` | Ticket bookings linking users to shows |
| `reviews` | User reviews of movies |
| `ai_summaries` | AI-generated summaries of movie reviews |

### Embed vs Reference decisions
- **Embedded:** `addresses` (in users), `genre`/`cast` (in movies), `screens` (in theaters), `seat_map` (in shows), `payment` (in bookings) — all small, bounded, and always read together with their parent.
- **Referenced:** `user_id`, `movie_id`, `theater_id`, `show_id` — used wherever the "many" side would otherwise make a parent document grow unbounded (e.g. one movie can have thousands of reviews).

---

## Schemas (Pydantic Models)

### `schemas/user.py`
```python
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
```

### `schemas/movie.py`
```python
from pydantic import BaseModel
from typing import List


class MovieCreate(BaseModel):
    title: str
    genre: List[str] = []
    cast: List[str] = []
    duration_min: int
    release_date: str    # format: "YYYY-MM-DD"
    language: str = ""
```

### `schemas/theater.py`
```python
from pydantic import BaseModel
from typing import List


class Screen(BaseModel):
    screen_no: int
    capacity: int
    type: str


class TheaterCreate(BaseModel):
    name: str
    city: str
    screens: List[Screen] = []
```

### `schemas/show.py`
```python
from pydantic import BaseModel
from typing import List


class Seat(BaseModel):
    seat_no: str
    status: str = "available"


class ShowCreate(BaseModel):
    movie_id: str
    theater_id: str
    screen_no: int = 1
    start_time: str    # format: "YYYY-MM-DDTHH:MM:SS"
    price: float
    seat_map: List[Seat] = []
```

### `schemas/booking.py`
```python
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
```

### `schemas/review.py`
```python
from pydantic import BaseModel, Field
from typing import Optional


class ReviewCreate(BaseModel):
    movie_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str = ""


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
```

### `schemas/ai_summary.py`
```python
from pydantic import BaseModel
from typing import List


class AISummaryCreate(BaseModel):
    movie_id: str
    summary_text: str
    sentiment: str = ""
    based_on_review_ids: List[str] = []
    model_used: str = "claude-sonnet-5"
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create a user (rejects duplicate emails) |
| GET | `/users` | List all users |
| GET | `/users/{id}` | Get one user |
| PUT | `/users/{id}` | Partially update a user |
| DELETE | `/users/{id}` | Delete a user |
| POST | `/movies` | Create a movie |
| GET | `/movies` | List all movies |
| POST | `/theaters` | Create a theater |
| GET | `/theaters` | List all theaters |
| GET | `/theaters/{id}/screen-utilization` | Screen breakdown (`$unwind`) |
| POST | `/shows` | Create a show |
| GET | `/shows` | List all shows |
| GET | `/shows/{id}/available-seats` | Available seats for a show |
| GET | `/shows/{id}/seat-stats` | Seat status counts (`$unwind` + `$group`) |
| POST | `/bookings` | Create a booking (validates seat availability) |
| GET | `/bookings` | List all bookings |
| GET | `/bookings/with-user` | Bookings joined with user info (`$lookup`) |
| PUT | `/bookings/{id}/payment-status` | Update payment status |
| DELETE | `/bookings/{id}` | Delete a booking |
| POST | `/reviews` | Create a review (rating 1–5 only) |
| GET | `/reviews/with-user` | Reviews joined with user info (`$lookup`) |
| PUT | `/reviews/{id}` | Update a review |
| DELETE | `/reviews/{id}` | Delete a review |
| POST | `/ai-summaries` | Create an AI-generated review summary |
| GET | `/ai-summaries` | List all AI summaries |
| GET | `/analytics/movies-dashboard` | Multiple stats in one query (`$facet`) |

---

## Advanced Aggregation Used

| Operator | Where | What it does |
|---|---|---|
| `$lookup` | `bookings/with-user`, `reviews/with-user` | Joins two collections, like a SQL JOIN |
| `$unwind` | `shows/{id}/seat-stats`, `theaters/{id}/screen-utilization` | Breaks an embedded array into individual documents so they can be grouped/counted |
| `$facet` | `analytics/movies-dashboard` | Runs several aggregation pipelines in a single query, returning multiple reports at once |

---

## Server-Side Validation

- **Duplicate email check** — `POST /users` rejects an email that already exists in the database.
- **Phone format check** — phone must be exactly 10 digits.
- **Rating range check** — reviews only accept a rating between 1 and 5 (`Field(..., ge=1, le=5)`).
- **Seat availability check** — `POST /bookings` rejects a booking if any requested seat is already booked or doesn't exist on that show.

---

## Testing

All endpoints were tested manually using **Postman**:
- Successful create/read/update/delete flows for every collection.
- Validation failure cases (duplicate email, invalid phone length, out-of-range rating, double-booking a seat) confirmed to return proper error responses.
- Aggregation endpoints (`$lookup`, `$unwind`, `$facet`) confirmed to return correctly joined/grouped data.

---

## Sample Outputs

### 1. Create User — `POST /users`
**Request:**
```json
{
  "name": "Mr.Kieko",
  "email": "kieko1@gmail.com",
  "phone": "1213141516",
  "addresses": [{"label": "Home", "city": "Hmirpur", "pincode": "000000"}]
}
```
**Response (201 Created):**
```json
{
  "inserted_id": "6a4b82ed2d810ac969846c31"
}
```

### 2. Get All Users — `GET /users`
**Response (200 OK):**
```json
[
  {
    "_id": "6a4b82ed2d810ac969846c31",
    "name": "Mr.Kieko",
    "email": "kieko1@gmail.com",
    "phone": "1213141516",
    "addresses": [{"label": "Home", "city": "Hmirpur", "pincode": "000000"}],
    "created_at": "2026-07-06T10:26:53.268000"
  }
]
```

### 3. `$lookup` — `GET /bookings/with-user`
**Response (200 OK):**
```json
[
  {
    "_id": "6a4b95403ac2189cde989edf",
    "user_id": "6a4b82ed2d810ac969846c31",
    "show_id": "6a4b934e3ac2189cde989ede",
    "seats_booked": ["A1"],
    "total_amount": 300,
    "payment": { "status": "success", "method": "UPI", "txn_id": "TXN001" },
    "user_info": [
      {
        "_id": "6a4b82ed2d810ac969846c31",
        "name": "Mr.Kieko",
        "email": "kieko1@gmail.com"
      }
    ]
  }
]
```
*Confirms the join worked — each booking now carries the full user document under `user_info`.*

### 4. `$unwind` + `$group` — `GET /shows/{id}/seat-stats`
**Response (200 OK):**
```json
{
  "show_id": "6a4b934e3ac2189cde989ede",
  "seat_breakdown": [
    { "_id": "booked", "count": 1 },
    { "_id": "available", "count": 1 }
  ]
}
```
*Confirms the seat_map array was correctly broken apart and grouped by status.*

### 5. `$facet` — `GET /analytics/movies-dashboard`
**Response (200 OK):**
```json
{
  "total_movies": [
    { "count": 2 }
  ],
  "by_genre": [
    { "_id": "Action", "count": 2 },
    { "_id": "Thriller", "count": 2 }
  ],
  "by_language": [
    { "_id": "Hindi", "count": 2 }
  ]
}
```
*Confirms `$facet` ran three independent aggregations — a total count, a genre breakdown, and a language breakdown — in a single database query.*

### 6. Validation — Duplicate Email — `POST /users`
**Response (400 Bad Request):**
```json
{
  "detail": "A user with this email already exists"
}
```

### 7. Validation — Invalid Phone Format — `POST /users`
**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "phone"],
      "msg": "Value error, phone must be exactly 10 digits"
    }
  ]
}
```

### 8. Validation — Rating Out of Range — `POST /reviews`
**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "rating"],
      "msg": "Input should be less than or equal to 5"
    }
  ]
}
```

### 9. Validation — Seat Already Booked — `POST /bookings`
**Response (409 Conflict):**
```json
{
  "detail": "Seat A1 is already booked"
}
```

> **Note:** Replace the sample IDs/values above with your own actual output — take a real screenshot from Postman for each of these 9 cases for the assignment submission.

---

## Author's Note

This project was built as part of a weekly database integration assignment, covering MongoDB schema design, CRUD operations, server-side validation, and advanced aggregation pipelines.
