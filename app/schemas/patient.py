from __future__ import annotations

from datetime import date
from typing import List


from app.schemas.common import (
    CountyMiniResponse,
    SubCountyMiniResponse,
    GenderMiniResponse,
    #MedicalFacilityMiniResponse,
    EncounterAssessmentMiniResponse,
    ReferralMiniResponse,
    TeleConsultationMiniResponse
)
from pydantic import BaseModel
from pydantic.generics import GenericModel


class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    date_of_birth: date
    gender: GenderMiniResponse
    location: str
    county: CountyMiniResponse
    sub_county: SubCountyMiniResponse
    encounter_assessments: List[EncounterAssessmentMiniResponse]
    referrals: List[ReferralMiniResponse]
    consultations: List[TeleConsultationMiniResponse]
    active: bool

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    name: str
    date_of_birth: date
    gender_id: int
    phone: str
    location: str
    county_id: int
    sub_county_id: int


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    gender_id: int | None = None
    phone: str | None = None
    location: str | None = None
    county_id: int | None = None
    sub_county_id: int | None = None


class PatientResponseWrapper(BaseModel):
    data: List[PatientResponse]


PatientResponse.model_rebuild()