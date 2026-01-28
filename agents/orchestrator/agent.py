from agents.base.agent import BaseAgent
from agents.base.llm import LLMProvider
from agents.discovery.agent import DestinationDiscoveryAgent
from agents.orchestrator.args import Intent
import uuid

from agents.orchestrator.args import OrchestratorExtraction

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        self.llm = LLMProvider.get_llm()
        self.discovery_agent = DestinationDiscoveryAgent()

    def invoke(self, state: dict) -> dict:
        user_query = state["user_query"]

        prompt = f"""
        Extract the following from the user query:
        If location is not exactly mentioned than you give the answer from your knowledge.
        - user_query
        - trip_id (generate if missing)
        - location (exact location if mentioned in query or monument or city name exactly whichever is mentioned in the query)
        - constraints:
            - budget
            - intent (DISCOVERY, BOOKING, PLANNING)
            - category (restaurant, hotel, hostpitals, trains, flights, shopping mall, history, background)

        User query:
        {user_query}

        Return JSON only.
        """

        extracted: OrchestratorExtraction = (
            self.llm
            .with_structured_output(OrchestratorExtraction)
            .invoke(prompt)
        )
        user_query = extracted.user_query
        trip_id = extracted.trip_id or str(uuid.uuid4())
        intent = extracted.constraints.intent

        metadata = {
            **state,
            "trip_id": trip_id,
            "user_query": user_query,
            "location": extracted.location,
            "category": extracted.constraints.category,
            "budget": extracted.constraints.budget,
            "intent": intent
        }

        if intent == Intent.DISCOVERY:
            if not extracted.location or not extracted.constraints.category:
                return {
                    "trip_id": trip_id,
                    "user_query": user_query,
                    "intent": Intent.DISCOVERY,
                    "answer": "Please specify a location and a category for discovery."
                }

            discovery_result = self.discovery_agent.invoke({
                "trip_id": trip_id,
                "user_query": user_query,
                "category": extracted.constraints.category,
                "location": extracted.location,
            })

            if isinstance(discovery_result, dict):
                return {**metadata, **discovery_result}
            return {**metadata, "answer": discovery_result}

        # elif intent == Intent.BOOKING:
        #     return {
        #         **metadata,
        #         "answer": "Booking agent coming soon."
        #     }

        # elif intent == Intent.PLANNING:
        #     return {
        #         **metadata,
        #         "answer": "Planning agent coming soon."
        #     }

        # return {
        #     **metadata,
        #     "answer": "Unsupported intent."
        # }

