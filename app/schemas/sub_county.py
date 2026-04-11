from typing import List

#from app.schemas.county import CountyResponse
from pydantic import BaseModel


class SubCountyResponse(BaseModel):
    id: int
    name: str
    #county: List[CountyResponse]
    active: bool

    class Config:
        from_attributes = True


class SubCountyResponseWrapper(BaseModel):
    data: List[SubCountyResponse]


SubCountyResponse.model_rebuild()