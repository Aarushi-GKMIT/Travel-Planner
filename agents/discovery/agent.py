from agents.base.agent import BaseAgent
from agents.base.llm import LLMProvider
from .tools import discover_places_tool
from .tools import discover_history_tool

class DestinationDiscoveryAgent(BaseAgent):

    def __init__(self):
        self.llm = LLMProvider.get_llm()
        self.tools = [discover_places_tool, discover_history_tool]

    def invoke(self, state: dict):
        prompt = f"""
        User wants to discover places or find history of a place or ask any general question.

        User_query: 
        {state['user_query']}

        Category: {state['category']}
        Location: {state['location']}
        """

        response = self.llm.bind_tools(self.tools).invoke(prompt)
       
        if hasattr(response, "content"):
            return response.content
        return response

