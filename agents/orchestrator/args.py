from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Intent(str, Enum):
    DISCOVERY = "DISCOVERY"
    BOOKING = "BOOKING"
    PLANNING = "PLANNING"

class Constraints(BaseModel):
    budget: Optional[int]
    intent: Optional[str]
    category: Optional[str]

class OrchestratorExtraction(BaseModel):
    user_query: str
    trip_id: Optional[str]
    location: Optional[str]
    constraints: Constraints

