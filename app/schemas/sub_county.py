from pydantic import BaseModel
from typing import List

class SubCountyResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True

class SubCountyPagedResponse(BaseModel):
    total: int
    items: List[SubCountyResponse]

    class Config:
        from_attributes = True


SubCountyResponse.model_rebuild()
SubCountyPagedResponse.model_rebuild()