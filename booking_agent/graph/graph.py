from graph.nodes import (
    book_node,
    conversation_node,
    infer_intent_node,
    rank_node,
    search_node,
)
from graph.state import BookingState
from langgraph.graph import END, StateGraph

graph = StateGraph(BookingState)

graph.add_node("infer_intent", infer_intent_node)
graph.add_node("search", search_node)
graph.add_node("rank", rank_node)
graph.add_node("conversation", conversation_node)
graph.add_node("book", book_node)

graph.set_entry_point("infer_intent")

graph.add_edge("infer_intent", "search")
graph.add_edge("search", "rank")

graph.add_edge("rank", "conversation")

graph.add_conditional_edges(
    "conversation",
    lambda s: "book" if s.final_confirmation else END,
)

graph.add_edge("book", END)

booking_graph = graph.compile()
