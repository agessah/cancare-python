from typing import List

from app.schemas.common import SubCountyMiniResponse
from pydantic import BaseModel


class CountyResponse(BaseModel):
    id: int
    code: str
    name: str
    town: str
    subcounties: List[SubCountyMiniResponse]
    active: bool

    class Config:
        from_attributes = True


class CountyResponseWrapper(BaseModel):
    data: List[CountyResponse]


CountyResponse.model_rebuild()