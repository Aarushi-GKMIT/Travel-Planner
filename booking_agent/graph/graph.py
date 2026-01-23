from langgraph.graph import END, StateGraph

from booking_agent.graph.nodes import book_node, rank_node, search_node
from booking_agent.graph.state import BookingState

graph = StateGraph(BookingState)

graph.add_node("search", search_node)
graph.add_node("rank", rank_node)
graph.add_node("book", book_node)

graph.set_entry_point("search")
graph.add_edge("search", "rank")

graph.add_conditional_edges("rank", lambda state: "book" if state.user_choice else END)

graph.add_edge("book", END)

booking_graph = graph.compile()
