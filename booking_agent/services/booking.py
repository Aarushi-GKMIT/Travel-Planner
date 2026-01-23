import uuid


async def execute_booking(offer: dict, trip_id: str):
    return {
        "booking_id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "provider": offer["provider"],
        "offer_id": offer["offer_id"],
        "status": "CONFIRMED",
    }
