from typing import TypedDict, List, Dict, Optional, Any

class DiscoveryState(TypedDict, total=False):
    user_query: str
    category: str
    location: str
    messages: List[str]
    constraints: Dict[str,Any]
    answer: Optional[str]



