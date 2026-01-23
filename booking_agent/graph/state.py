from typing import List, Literal, Optional

from pydantic import BaseModel


class BookingState(BaseModel):
    trip_id: str
    source: str
    destination: str
    booking_type: Literal[
        "flight",
        "hotel",
        "train",
        "activity",
    ]
    constraints: dict

    offers: List[dict] = []
    ranked_offers: List[dict] = []

    user_choice: Optional[str] = None

    status: Literal[
        "INIT",
        "SEARCHED",
        "AWAITING_CONFIRMATION",
        "CONFIRMED",
        "FAILED",
    ] = "INIT"

    error: Optional[str] = None


class BookingDestination(BaseModel):
    trip_id: str
    source: str
    booking_type: str
    destination: str
    constraints: dict
