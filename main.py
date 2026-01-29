from fastapi import FastAPI, HTTPException

from booking_agent.graph.graph import booking_graph
from booking_agent.graph.state import BookingDestination, BookingState
from itinerary_agent.graph.graph import planner_graph
from itinerary_agent.graph.state import PlannerState

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


@app.post("/itinerary/plan")
async def plan_itinerary(payload: PlannerState):
    result = await planner_graph.ainvoke(payload)

    if result["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail={"status": result["status"], "error": result.get("error")},
        )

    return {
        "status": "success",
        "planned_destinations": result["planned_destinations"],
        "booking_intents": result["booking_intents"],
    }
