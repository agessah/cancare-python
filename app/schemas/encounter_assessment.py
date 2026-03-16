from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from app.schemas.patient import PatientResponse

class EncounterAssessmentResponse(BaseModel):
    id: int
    patient: PatientResponse
    painless_lump: bool
    persistent_pain: bool
    skin_dimpling: bool
    nipple_discharge: bool
    family_history: bool
    above_fifty: bool
    post_menopausal: bool
    obesity: bool
    late_first_pregnancy: bool
    dense_tissue: bool
    notes: str
    risk_score: Decimal
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
    persistent_pain: bool
    skin_dimpling: bool
    nipple_discharge: bool
    family_history: bool
    above_fifty: bool
    post_menopausal: bool
    obesity: bool
    late_first_pregnancy: bool
    dense_tissue: bool
    notes: str
    risk_score: Decimal

class EncounterAssessmentCreate(EncounterAssessmentBase):
    pass

class EncounterAssessmentUpdate(BaseModel):
    patient_id: int | None = None
    painless_lump: bool | None = None
    persistent_pain: bool | None = None
    skin_dimpling: bool | None = None
    nipple_discharge: bool | None = None
    family_history: bool | None = None
    above_fifty: bool | None = None
    post_menopausal: bool | None = None
    obesity: bool | None = None
    late_first_pregnancy: bool | None = None
    dense_tissue: bool | None = None
    notes: str | None = None
    risk_score: decimal.Decimal | None = None


EncounterAssessmentResponse.model_rebuild()
EncounterAssessmentPagedResponse.model_rebuild()