import json

import langchain
from config import settings
from graph.state import BookingState
from langchain.messages import HumanMessage, SystemMessage
from langchain_core.globals import set_debug
from langchain_openai import ChatOpenAI
from prompts import CONVERSATION_PROMPT, INTENT_PROMPT, RANK_PROMPT
from services.tools import (
    book_offer,
    search_coupons_tool,
    search_flights,
)

# set_debug(True)
# langchain.debug = True

classifier_llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model="gpt-4.1-mini",
    temperature=0,
    verbose=True,
)

coupon_llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model="gpt-4.1-mini",
    temperature=0,
).bind_tools([search_coupons_tool])


def safe_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None


async def infer_intent_node(state: BookingState):
    res = classifier_llm.invoke(
        [
            SystemMessage(content=INTENT_PROMPT),
            HumanMessage(content=state.user_request),
        ]
    )

    data = safe_json(res.content)
    if not data or "booking_type" not in data:
        state.status = "FAILED"
        state.error = "Intent detection failed"
        return state

    state.booking_type = data["booking_type"]
    state.status = "INTENT_DETECTED"
    return state


async def search_node(state: BookingState):
    state.ranked_offers = await search_flights(
        state.source,
        state.destination,
        state.constraints,
    )
    state.status = "OFFERS_READY"
    return state


async def rank_node(state: BookingState):
    res = classifier_llm.invoke(
        [
            SystemMessage(content=RANK_PROMPT),
            HumanMessage(content=str(state.ranked_offers)),
        ]
    )

    ranked = safe_json(res.content)
    if ranked:
        state.ranked_offers = ranked

    state.status = "AWAITING_USER"
    return state


async def conversation_node(state: BookingState):
    if not state.last_user_message:
        return state

    intent_res = classifier_llm.invoke(
        [
            SystemMessage(content=CONVERSATION_PROMPT),
            HumanMessage(content=state.last_user_message),
        ]
    )

    intent_data = safe_json(intent_res.content)
    if not intent_data:
        return state

    intent = intent_data.get("intent")
    state.last_intent = intent

    if intent == "coupon":
        tool_res = coupon_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are allowed to call tools.\n"
                        "If coupons are available, you MUST call the coupon search tool.\n"
                        "If no coupons are available, respond normally."
                    )
                ),
                HumanMessage(
                    content=f"Check for coupons for offer {state.selected_offer_id}"
                ),
            ]
        )

        if tool_res.tool_calls:
            call = tool_res.tool_calls[0]

            if call["name"] == "search_coupons_tool":
                state.coupons = search_coupons_tool.invoke(call["args"])

    elif intent == "confirm":
        state.final_confirmation = True

    return state


async def book_node(state: BookingState):
    if not state.final_confirmation:
        return state

    booking = await book_offer(state.selected_offer_id)

    state.status = "BOOKED"
    state.booking_result = booking

    return state
