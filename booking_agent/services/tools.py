import uuid

from langchain.tools import tool


@tool
def search_coupons_tool(offer_id: str) -> list:
    """
    Search for coupons applicable to a given booking offer.
    """
    return [
        {"code": "SAVE10", "discount": "10%"},
        {"code": "FLAT500", "discount": "₹500"},
    ]


@tool
def book_offer_tool(offer_id: str) -> dict:
    """
    Book the selected offer.
    """
    return {
        "booking_id": str(uuid.uuid4()),
        "offer_id": offer_id,
        "status": "CONFIRMED",
    }


async def search_flights(source, destination, constraints):
    return [
        {
            "offer_id": "FLIGHT_001",
            "provider": "IndiGo",
            "price": 5800,
            "currency": "INR",
        },
        {
            "offer_id": "FLIGHT_002",
            "provider": "Vistara",
            "price": 7200,
            "currency": "INR",
        },
    ]


async def search_trains(source, destination, constraints):
    return [
        {"offer_id": "TRAIN_001", "provider": "IRCTC", "price": 1500, "currency": "INR"}
    ]


async def book_offer(offer_id):
    return {
        "booking_id": str(uuid.uuid4()),
        "offer_id": offer_id,
        "status": "CONFIRMED",
    }
