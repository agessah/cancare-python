from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from app.schemas.patient import PatientResponse
from pydantic import BaseModel


class EncounterAssessmentResponse(BaseModel):
    id: int
    patient: PatientResponse
    painless_lump: bool
    nipple_discharge: bool
    skin_dimpling: bool
    nipple_retraction: bool
    redness: bool
    family_history: bool
    above_fifty: bool
    never_been_pregnant: bool
    late_menopause: bool
    alcohol_consumption: bool
    obesity: bool
    notes: str
    risk_score: Optional[Decimal] = None
    active: bool

    class Config:
        from_attributes = True

class EncounterAssessmentPagedResponse(BaseModel):
    total: int
    items: List[EncounterAssessmentResponse]

    class Config:
        from_attributes = True


class EncounterAssessmentBase(BaseModel):
    patient_id: int
    painless_lump: bool
    nipple_discharge: bool
    skin_dimpling: bool
    nipple_retraction: bool
    redness: bool
    family_history: bool
    above_fifty: bool
    never_been_pregnant: bool
    late_menopause: bool
    alcohol_consumption: bool
    obesity: bool
    notes: str
    #risk_score: Decimal

class EncounterAssessmentCreate(EncounterAssessmentBase):
    pass

class EncounterAssessmentUpdate(BaseModel):
    patient_id: int | None = None
    painless_lump: bool | None = None
    nipple_discharge: bool | None = None
    skin_dimpling: bool | None = None
    nipple_retraction: bool | None = None
    redness: bool | None = None
    family_history: bool | None = None
    above_fifty: bool | None = None
    never_been_pregnant: bool | None = None
    late_menopause: bool | None = None
    alcohol_consumption: bool | None = None
    obesity: bool | None = None
    notes: str | None = None
    #risk_score: Decimal | None = None

EncounterAssessmentResponse.model_rebuild()
EncounterAssessmentPagedResponse.model_rebuild()
EncounterAssessmentUpdate.model_rebuild()