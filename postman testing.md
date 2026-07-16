### Postman Testing

---
### Create Users
## Request

```json
{
  "name": "Ushma",
  "email": "ushma1@example.com",
  "phone": "1213141516",
  "addresses": [{
      "label": "Home",
      "city": "Lucknow",
      "pincode": "909090"
  }]
}
```
## Output
```json
{
    "inserted_id": "6a588cc2585c32db50059fe4"
}
```
## Get Users Output
```json
[
    {
        "_id": "6a460df5e93c9d3bc43afec8",
        "name": "Virat Kohli",
        "email": "viratkohli1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "London",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-02T07:06:29.737000"
    },
    {
        "_id": "6a46121b72a8351d14dce22c",
        "name": "Rohit Sharma",
        "email": "rohitsharma45@gmail.com",
        "phone": "5060708090",
        "addresses": [
            {
                "label": "Home",
                "city": "Mumbai",
                "pincode": "567890"
            }
        ],
        "created_at": "new Date()"
    },
    {
        "_id": "6a47b9ee55684eb5f0e983b1",
        "name": "Swarnima",
        "email": "swarnima1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "hometown",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-03T13:32:30.069000"
    },
    {
        "_id": "6a47ba2455684eb5f0e983b2",
        "name": "string",
        "email": "string1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "hometown",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-03T13:33:24.255000"
    },
    {
        "_id": "6a4b82ed2d810ac969846c31",
        "name": "Mr.Kieko",
        "email": "kieko1@gmail.com",
        "phone": "1234567890",
        "addresses": [
            {
                "label": "Home",
                "city": "Hmirpur",
                "pincode": "000000"
            }
        ],
        "created_at": "2026-07-06T10:26:53.268000"
    },
    {
        "_id": "6a588cc2585c32db50059fe4",
        "name": "Ushma",
        "email": "ushma1@example.com",
        "phone": "1213141516",
        "addresses": [
            {
                "label": "Home",
                "city": "Lucknow",
                "pincode": "909090"
            }
        ],
        "created_at": "2026-07-16T07:48:18.172000"
    }
]
```
## Get/Users/Users ID

```json
{
    "_id": "6a588cc2585c32db50059fe4",
    "name": "Ushma",
    "email": "ushma1@example.com",
    "phone": "1213141516",
    "addresses": [
        {
            "label": "Home",
            "city": "Lucknow",
            "pincode": "909090"
        }
    ],
    "created_at": "2026-07-16T07:48:18.172000"
}
```
## PUT/Users/Users ID

```json

  "name": "Ushma",
  "email": "ushma1@example.com",
  "phone": "1213141516",
  "addresses": [{
      "label": "Home",
      "city": "Kanpur",
      "pincode": "909090"
  }]
}
```
## PUT OUTPUT

```json
{
    "matched": 1,
    "modified": 0
}
```
---
### Aggregations

## Unwind Aggregation
## $unwind example: break the screens array into individual documents.

# Get/Theaters (Output)

```json
[
    {
        "_id": "6a46260672a8351d14dce234",
        "name": "PVR Saket",
        "city": "Delhi",
        "screens": [
            {
                "screen_no": "1",
                "capacity": "120",
                "type": "IMAX"
            },
            {
                "screen_no": "2",
                "capacity": "80",
                "type": "Standard"
            }
        ]
    }
]
```
# Unwind aggregation

```json
[
    {
        "screen_no": "1",
        "capacity": "120",
        "type": "IMAX"
    },
    {
        "screen_no": "2",
        "capacity": "80",
        "type": "Standard"
    }
]
```
# Get/Shows (Output)

```json
[
    {
        "_id": "6a462ac072a8351d14dce23a",
        "movie_id": "6a46260672a8351d14dce234",
        "theater_id": "6a4625bbdfdd3fafe2aae15b",
        "screen_no": 1,
        "start_time": "2026-07-05T18:00:00",
        "price": 300,
        "seat_map": [
            {
                "seat_no": "A1",
                "status": "available"
            },
            {
                "seat_no": "A2",
                "status": "available"
            },
            {
                "seat_no": "A3",
                "status": "not available"
            }
        ]
    },
    {
        "_id": "6a4b934e3ac2189cde989ede",
        "movie_id": "6a4b89503ac2189cde989edd",
        "theater_id": "6a46260672a8351d14dce234",
        "screen_no": 1,
        "start_time": "2026-07-10T18:00:00",
        "price": 300,
        "seat_map": [
            {
                "seat_no": "A1",
                "status": "available"
            },
            {
                "seat_no": "A2",
                "status": "available"
            }
        ]
    }
]
```
# $unwind example: break seat_map into per-seat documents, then group by status.

# Get/shows/{show_id}/available-seats
```json
[
    {
        "seat_no": "A1",
        "status": "available"
    },
    {
        "seat_no": "A2",
        "status": "available"
    }
]
```
# Get/Shows/{show_id}/seat-satats
```json
{
    "show_id": "6a4b934e3ac2189cde989ede",
    "seat_breakdown": [
        {
            "_id": "available",
            "count": 2
        }
    ]
}
```
## Lookup Aggregation

# Get/bookings (Output)

```json
[
    {
        "_id": "6a4630c572a8351d14dce25b",
        "user_id": "6a460df5e93c9d3bc43afec8",
        "show_id": "6a462ac072a8351d14dce23a",
        "seats_booked": [
            "A1"
        ],
        "total_amount": 300,
        "payment": {
            "status": "success",
            "method": "UPI",
            "txn_id": "TXN001"
        },
        "booked_at": "1970-01-01T00:00:00"
    },
    {
        "_id": "6a4b95403ac2189cde989edf",
        "user_id": "6a4b82ed2d810ac969846c31",
        "show_id": "6a4b934e3ac2189cde989ede",
        "seats_booked": [
            "A1"
        ],
        "total_amount": 300,
        "payment": {
            "status": "success",
            "method": "UPI",
            "txn_id": "TXN001"
        },
        "booked_at": "2026-07-06T11:45:04.037000"
    }
]
```

# $lookup example: join bookings with the user who made them. (Get/bookings/with-user)

```json
[
    {
        "_id": "6a4630c572a8351d14dce25b",
        "user_id": "6a460df5e93c9d3bc43afec8",
        "show_id": "6a462ac072a8351d14dce23a",
        "seats_booked": [
            "A1"
        ],
        "total_amount": 300,
        "payment": {
            "status": "success",
            "method": "UPI",
            "txn_id": "TXN001"
        },
        "booked_at": "1970-01-01T00:00:00",
        "user_info": [
            {
                "_id": "6a460df5e93c9d3bc43afec8",
                "name": "Virat Kohli",
                "email": "viratkohli1@gmail.com",
                "phone": "1020304050",
                "addresses": [
                    {
                        "label": "Home",
                        "city": "London",
                        "pincode": "123456"
                    }
                ],
                "created_at": "2026-07-02T07:06:29.737000"
            }
        ]
    },
    {
        "_id": "6a4b95403ac2189cde989edf",
        "user_id": "6a4b82ed2d810ac969846c31",
        "show_id": "6a4b934e3ac2189cde989ede",
        "seats_booked": [
            "A1"
        ],
        "total_amount": 300,
        "payment": {
            "status": "success",
            "method": "UPI",
            "txn_id": "TXN001"
        },
        "booked_at": "2026-07-06T11:45:04.037000",
        "user_info": [
            {
                "_id": "6a4b82ed2d810ac969846c31",
                "name": "Mr.Kieko",
                "email": "kieko1@gmail.com",
                "phone": "1234567890",
                "addresses": [
                    {
                        "label": "Home",
                        "city": "Hmirpur",
                        "pincode": "000000"
                    }
                ],
                "created_at": "2026-07-06T10:26:53.268000"
            }
        ]
    }
]
```
# Get/reviews/ with-user (Output)

```json
[
    {
        "_id": "6a4633e272a8351d14dce26d",
        "movie_id": "6a4625bbdfdd3fafe2aae15b",
        "usr_id": "6a460df5e93c9d3bc43afec8",
        "rating": "4",
        "comment": "Great action, weak plot",
        "created_at": "2026-07-05T18:00:00.000Z",
        "user_info": []
    },
    {
        "_id": "6a4b963e3ac2189cde989ee0",
        "movie_id": "6a4b89503ac2189cde989edd",
        "user_id": "6a4b82ed2d810ac969846c31",
        "rating": 4,
        "comment": "Great action, amazing movie",
        "created_at": "2026-07-06T11:49:18.913000",
        "user_info": [
            {
                "_id": "6a4b82ed2d810ac969846c31",
                "name": "Mr.Kieko",
                "email": "kieko1@gmail.com",
                "phone": "1234567890",
                "addresses": [
                    {
                        "label": "Home",
                        "city": "Hmirpur",
                        "pincode": "000000"
                    }
                ],
                "created_at": "2026-07-06T10:26:53.268000"
            }
        ]
    }
]
```
## facet Aggregation

# $facet runs 3 independent aggregations in a SINGLE query:
# 1. total movie count
# 2. movie count grouped by genre
# 3. movie count grouped by language

# Get/analytics/movies-dashboard

```json
{
    "total_movies": [
        {
            "count": 2
        }
    ],
    "by_genre": [
        {
            "_id": "Action",
            "count": 2
        },
        {
            "_id": "Thriller",
            "count": 2
        }
    ],
    "by_language": [
        {
            "_id": "Hindi",
            "count": 2
        }
    ]
}
```
