from typing import TypedDict, Optional
from agents.orchestrator.args import Constraints

class OrchestratorState(TypedDict, total=False):
    user_query: str

    trip_id: Optional[str]
    location: Optional[str]
    constraints: Optional[Constraints] 
    answer: Optional[str]


