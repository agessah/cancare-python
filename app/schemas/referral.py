from __future__ import annotations

from typing import List

from app.schemas.common import LevelMiniResponse, PatientMiniResponse, MedicalFacilityMiniResponse, FollowUpMiniResponse
from pydantic import BaseModel


class ReferralResponse(BaseModel):
    id: int
    patient: PatientMiniResponse
    medical_facility: MedicalFacilityMiniResponse
    notes: str
    urgency_level: LevelMiniResponse
    follow_ups: List[FollowUpMiniResponse]
    active: bool

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


class ReferralResponseWrapper(BaseModel):
    data: List[ReferralResponse]


ReferralResponse.model_rebuild()
ReferralUpdate.model_rebuild()