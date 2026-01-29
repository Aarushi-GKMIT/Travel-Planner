INTENT_PROMPT = """
Classify booking intent.
Return JSON only:
{ "booking_type": "flight" | "train" }
"""

RANK_PROMPT = """
Rank offers best to worst.
Return JSON list only.
"""

CONVERSATION_PROMPT = """
You are assisting with a booking.

From the user's message, decide:

Return JSON ONLY in this format:
{
  "intent": "coupon" | "confirm" | "none"
}

Rules:
- If the user asks for discounts, coupons, deals → intent = "coupon"
- If the user says or the intent implies confirm, proceed, book, go ahead → intent = "confirm"
- Otherwise → intent = "none"

Do NOT explain.
"""
