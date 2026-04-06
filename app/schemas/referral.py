from __future__ import annotations

from typing import List

from app.schemas.level import LevelResponse
from app.schemas.medical_facility import MedicalFacilityResponse
from app.schemas.patient import PatientResponse
from pydantic import BaseModel


class ReferralResponse(BaseModel):
    id: int
    patient: PatientResponse
    medical_facility: MedicalFacilityResponse
    notes: str
    urgency_level: LevelResponse
    active: bool

    class Config:
        from_attributes = True

class ReferralPagedResponse(BaseModel):
    total: int
    items: List[ReferralResponse]

    class Config:
        from_attributes = True


class ReferralBase(BaseModel):
    patient_id: int
    medical_facility_id: int
    notes: str
    urgency_level_id: int

class ReferralCreate(ReferralBase):
    pass

class ReferralUpdate(BaseModel):
    patient_id: int | None = None
    medical_facility_id: int | None = None
    notes: str | None = None
    urgency_level_id: int | None = None

ReferralResponse.model_rebuild()
ReferralPagedResponse.model_rebuild()
ReferralUpdate.model_rebuild()