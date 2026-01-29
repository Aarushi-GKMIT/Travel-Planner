from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class BookingState(BaseModel):
    trip_id: str
    user_request: str
    source: str
    destination: str
    constraints: dict

    booking_type: Optional[Literal["flight", "train"]] = None
    ranked_offers: List[dict] = []

    selected_offer_id: Optional[str] = None
    last_user_message: Optional[str] = None
    last_intent: Optional[str] = None

    coupons: List[dict] = []

    final_confirmation: Optional[bool] = None
    status: Literal[
        "INIT", "INTENT_DETECTED", "OFFERS_READY", "AWAITING_USER", "BOOKED", "FAILED"
    ] = "INIT"

    error: Optional[str] = None
    booking_result: Optional[Dict] = None
