from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage


from .tools import discover_places_tool
from .tools import discover_history_tool
from .state import DiscoveryState


llm = ChatOpenAI(model="gpt-4.1-mini", verbose=True, temperature=0)
llm_with_tools = llm.bind_tools([discover_places_tool, discover_history_tool])
tool_node = ToolNode([discover_places_tool, discover_history_tool])

def discovery_adapter(state: dict) -> DiscoveryState:
    return {
        "category": state["constraints"]["category"],
        "location": state["location"],
        "messages": [],
        "constraints": state['constraints']
    }


def llm_node(state: DiscoveryState):
    prompt = f"""
    You are a travel discovery assistant.

    User intent:
    - Category: {state['category']}
    - Location: {state['location']}

    Decide intelligently:
    - if tool is not required, then answer directly from your knowledge for general questions.
    - Use tools only if external or factual lookup is required for example if someone wants to know about the history it should use a tool.

    """

    response = llm_with_tools.invoke(prompt)

    return {
        "messages": [response]
    }


def finalize_node(state: DiscoveryState):
    messages = state.get("messages", [])

    print(messages)

    if messages:
        last = messages[-1]
        answer = getattr(last, "content", str(last))
    else:
        answer = "Sorry, I couldn't find relevant information."

    return {
        "answer": answer
    }


graph = StateGraph(DiscoveryState)

graph.add_node("adapter", discovery_adapter)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)
graph.add_node("finalize", finalize_node)


graph.add_edge(START, "adapter")
graph.add_edge("adapter", "llm")
graph.add_edge("llm","tools")
graph.add_edge("tools", "finalize")
graph.add_edge("finalize", END)

discovery_graph = graph.compile()










