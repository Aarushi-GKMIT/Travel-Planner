from pydantic import BaseModel, Field

class DiscoverPlacesArgs(BaseModel):
    category: str = Field(
        description="Type of place such as hospital, mall, tourist place, restaurant"
    )
    location: str = Field(
        description="City or locality where places should be searched"
    )
    
class DiscoverHistoryArgs(BaseModel):
    query: str = Field(
        description="Query for historical or encyclopedic information about a place"
    )