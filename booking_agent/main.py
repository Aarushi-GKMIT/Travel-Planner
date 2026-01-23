from fastapi import FastAPI

from booking_agent.graph.graph import booking_graph
from booking_agent.graph.state import BookingDestination, BookingState

app = FastAPI()


@app.post("/booking/start")
async def start_booking(state: BookingDestination):
    result = await booking_graph.ainvoke(state)

    if result["status"] == "AWAITING_CONFIRMATION":
        return {"status": "awaiting_confirmation", "offers": result["ranked_offers"]}

    return result


@app.post("/booking/confirm")
async def confirm_booking(state: BookingState):
    return await booking_graph.ainvoke(state)
