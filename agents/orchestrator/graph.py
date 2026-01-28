from langgraph.graph import StateGraph, START, END
from agents.orchestrator.agent import OrchestratorAgent
from agents.orchestrator.state import OrchestratorState
from agents.discovery.graph import discovery_graph

orchestrator_agent = OrchestratorAgent()

def classify(state: OrchestratorState):
    result = orchestrator_agent.invoke(state)

    return{
        "user_query":result['user_query'],
        "trip_id":result['trip_id'],
        "location": result['location'],
        "constraints":{
            "budget":result['budget'],
            "intent":result['intent'],
            "category":result['category']
        }
    }

   
def route(state: OrchestratorState):
    return state['constraints']['intent']

graph = StateGraph(OrchestratorState)

graph.add_node("classify", classify)
graph.add_node("discovery", discovery_graph)

graph.add_edge(START, "classify")

graph.add_conditional_edges(
    "classify",
    route,
    { 
        "DISCOVERY":"discovery",
        "BOOKING": END,
        "PLANNING": END
    }
)

graph.add_edge("discovery", END)

orchestrator_graph = graph.compile()
