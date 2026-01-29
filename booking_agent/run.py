import asyncio

from graph.graph import booking_graph
from graph.state import BookingState


async def main():
    state = BookingState(
        trip_id="TRIP123",
        user_request="Book a flight from Delhi to Paris",
        source="DEL",
        destination="PAR",
        constraints={"date": "2026-03-10"},
    )

    result = await booking_graph.ainvoke(state)

    print("\nAvailable offers:")
    for o in result["ranked_offers"]:
        print(o)

    result["selected_offer_id"] = input("\nSelect offer_id: ").strip()

    while True:
        msg = input("\nSay something (or 'book'): ").strip()

        result["last_user_message"] = msg
        result = await booking_graph.ainvoke(result)

        #  Acknowledge intent
        if result.get("last_intent") == "coupon":
            if result.get("coupons"):
                print("\nCoupons found:")
                for c in result["coupons"]:
                    print(c)
            else:
                print("\n No coupons available for this offer.")

        elif result.get("last_intent") == "none":
            print("\n Okay, let me know if you want to proceed or look for discounts.")

        if result.get("final_confirmation"):
            final = await booking_graph.ainvoke(result)
            print("\n BOOKED:")
            print(final)
            break


if __name__ == "__main__":
    asyncio.run(main())
