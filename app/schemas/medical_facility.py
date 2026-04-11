from app.schemas.county import CountyResponse
from app.schemas.sub_county import SubCountyResponse
from pydantic import BaseModel
from typing import List

class MedicalFacilityResponse(BaseModel):
    id: int
    name: str
    county: CountyResponse
    sub_county: SubCountyResponse
    active: bool

    class Config:
        from_attributes = True


class MedicalFacilityResponseWrapper(BaseModel):
    data: List[MedicalFacilityResponse]


MedicalFacilityResponse.model_rebuild()