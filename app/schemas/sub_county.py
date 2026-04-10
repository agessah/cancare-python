from typing import List

from pydantic import BaseModel


class SubCountyResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True


class SubCountyResponseWrapper(BaseModel):
    data: List[SubCountyResponse]


SubCountyResponse.model_rebuild()