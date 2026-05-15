from typing import List

from pydantic import BaseModel
from app.schemas.common import CountyMiniResponse


class SubCountyResponse(BaseModel):
    id: int
    name: str
    county: CountyMiniResponse
    active: bool

    class Config:
        from_attributes = True


class SubCountyResponseWrapper(BaseModel):
    data: List[SubCountyResponse]


SubCountyResponse.model_rebuild()