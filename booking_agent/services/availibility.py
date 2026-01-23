async def search_flights(source: str, destination: str, constraints: dict):
    return [
        {
            "offer_id": "FLIGHT_001",
            "type": "flight",
            "provider": "IndiGo",
            "price": 5800,
            "currency": "INR",
            "details": {
                "from": source,
                "to": destination,
                "departure": "2026-03-12T06:00",
                "arrival": "2026-03-12T08:30",
                "duration": "2h 30m",
                "stops": 0,
                "class": constraints.get("class", "economy"),
            },
        },
        {
            "offer_id": "FLIGHT_002",
            "type": "flight",
            "provider": "Vistara",
            "price": 7200,
            "currency": "INR",
            "details": {
                "from": source,
                "to": destination,
                "departure": "2026-03-12T09:00",
                "arrival": "2026-03-12T11:15",
                "duration": "2h 15m",
                "stops": 0,
                "class": "economy",
            },
        },
    ]


async def search_hotels(destination: str, constraints: dict):
    nights = constraints.get("nights", 2)

    return [
        {
            "offer_id": "HOTEL_001",
            "type": "hotel",
            "provider": "Taj Hotels",
            "price": 12000 * nights,
            "currency": "INR",
            "details": {
                "hotel_name": "Taj Palace",
                "rating": 5,
                "nights": nights,
                "room_type": "Deluxe",
                "check_in": "2026-03-12",
                "check_out": "2026-03-14",
            },
        },
        {
            "offer_id": "HOTEL_002",
            "type": "hotel",
            "provider": "OYO",
            "price": 3500 * nights,
            "currency": "INR",
            "details": {
                "hotel_name": "OYO Central",
                "rating": 3,
                "nights": nights,
                "room_type": "Standard",
                "check_in": "2026-03-12",
                "check_out": "2026-03-14",
            },
        },
    ]


async def search_trains(source: str, destination: str, constraints: dict):
    return [
        {
            "offer_id": "TRAIN_001",
            "type": "train",
            "provider": "IRCTC",
            "price": 1500,
            "currency": "INR",
            "details": {
                "train_name": "Rajdhani Express",
                "from": source,
                "to": destination,
                "departure": "2026-03-12T16:00",
                "arrival": "2026-03-13T06:00",
                "class": "2A",
            },
        },
        {
            "offer_id": "TRAIN_002",
            "type": "train",
            "provider": "IRCTC",
            "price": 900,
            "currency": "INR",
            "details": {
                "train_name": "Shatabdi Express",
                "from": source,
                "to": destination,
                "departure": "2026-03-12T07:00",
                "arrival": "2026-03-12T13:30",
                "class": "CC",
            },
        },
    ]


async def search_activities(destination: str, constraints: dict):
    return [
        {
            "offer_id": "ACT_001",
            "type": "activity",
            "provider": "GetYourGuide",
            "price": 2500,
            "currency": "INR",
            "details": {
                "activity_name": "City Walking Tour",
                "duration": "3 hours",
                "language": "English",
                "date": "2026-03-13",
            },
        },
        {
            "offer_id": "ACT_002",
            "type": "activity",
            "provider": "Local Tours",
            "price": 4500,
            "currency": "INR",
            "details": {
                "activity_name": "Food & Culture Experience",
                "duration": "4 hours",
                "language": "English",
                "date": "2026-03-14",
            },
        },
    ]
