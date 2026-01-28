from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient()

@tool
def discover_places_tool(category: str, location: str) -> str:
    """
    Use this tool ONLY to find nearby or currently operating places,
    businesses, or attractions using live web search.
    
    Examples:
    - hospitals near Jaipur
    - malls in Delhi
    - tourist places in Udaipur

    DO NOT use this tool for history, culture, or background information.
    """

    query = f"{category} in {location}"

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=25,
        include_answer=True
    ).get("answer")

    return response

wiki_api = WikipediaAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=2000
)

wikipedia_tool = WikipediaQueryRun(api_wrapper=wiki_api)

@tool
def discover_history_tool(query: str) -> str:
    """
    Use this tool to retrieve historical, cultural, or encyclopedic
    information about a place from Wikipedia.

    Args:
        query: Query for historical or encyclopedic information about a place, monumnet (like city place, hawa mahal, etc ) or city

    Examples:
    - history of City Palace Jaipur
    - history of Jaipur
    - who built City Palace

    DO NOT use this tool to find nearby places or businesses.
    """
    return wikipedia_tool.run(query)





