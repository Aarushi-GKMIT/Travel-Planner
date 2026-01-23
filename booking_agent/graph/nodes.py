import json

from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from booking_agent.config import settings
from booking_agent.graph.state import BookingState
from booking_agent.prompts import BOOKING_SYSTEM_PROMPT
from booking_agent.services.availibility import (
    search_activities,
    search_flights,
    search_hotels,
    search_trains,
)
from booking_agent.services.booking import execute_booking

llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-4.1-mini", temperature=0)


async def search_node(state: BookingState):
    if state.booking_type == "flight":
        state.offers = await search_flights(
            state.source, state.destination, state.constraints
        )

    elif state.booking_type == "hotel":
        state.offers = await search_hotels(state.destination, state.constraints)

    elif state.booking_type == "train":
        state.offers = await search_trains(
            state.source, state.destination, state.constraints
        )

    elif state.booking_type == "activites":
        state.offers = await search_activities(state.destination, state.constraints)

    else:
        state.status = "FAILED"
        state.error = "unsupported_booking_type"

    state.status = "SEARCHED"
    return state


async def rank_node(state: BookingState):
    messages = [
        SystemMessage(content=BOOKING_SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Constraints:
{state.constraints}

Offers:
{state.offers}

Return ranked offers as JSON.
"""
        ),
    ]

    response = llm.invoke(messages)
    state.ranked_offers = json.loads(response.content)

    state.status = "AWAITING_CONFIRMATION"
    return state


async def book_node(state: BookingState):
    chosen = next(o for o in state.ranked_offers if o["offer_id"] == state.user_choice)

    result = await execute_booking(chosen, state.trip_id)
    state.status = "CONFIRMED"
    return result
