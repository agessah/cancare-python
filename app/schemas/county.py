from pydantic import BaseModel
from typing import List

class CountyResponse(BaseModel):
    id: int
    code: str
    name: str
    town: str
    active: bool

    class Config:
        from_attributes = True

class CountyPagedResponse(BaseModel):
    total: int
    items: List[CountyResponse]

    class Config:
        from_attributes = True


CountyResponse.model_rebuild()
CountyPagedResponse.model_rebuild()