from app.schemas.common import CountyMiniResponse, SubCountyMiniResponse
from pydantic import BaseModel
from typing import List

class MedicalFacilityResponse(BaseModel):
    id: int
    name: str
    county: CountyMiniResponse
    sub_county: SubCountyMiniResponse
    active: bool

    class Config:
        from_attributes = True


class MedicalFacilityResponseWrapper(BaseModel):
    data: List[MedicalFacilityResponse]


MedicalFacilityResponse.model_rebuild()