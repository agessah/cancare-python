from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from app.schemas.patient import PatientResponse
from pydantic import BaseModel


class EncounterAssessmentResponse(BaseModel):
    id: int
    patient: PatientResponse
    age: int
    above_fifty: bool
    painless_lump: bool
    nipple_discharge: bool
    skin_dimpling: bool
    nipple_retraction: bool
    redness_scaling: bool
    breast_pain: bool
    swollen_lymph_nodes: bool
    family_history: bool
    never_been_pregnant: bool
    late_menopause: bool
    bmi_risk: bool
    low_physical_activity: bool
    prior_screening: bool
    prior_benign_breast_disease: bool
    self_exam_irregularity: bool
    alcohol_risk: bool
    smoker: bool
    notes: str
    risk_score: Optional[Decimal] = None
    active: bool

    class Config:
        from_attributes = True


class EncounterAssessmentBase(BaseModel):
    patient_id: int
    painless_lump: bool
    nipple_discharge: bool
    skin_dimpling: bool
    nipple_retraction: bool
    redness_scaling: bool
    breast_pain: bool
    swollen_lymph_nodes: bool
    family_history: bool
    never_been_pregnant: bool
    late_menopause: bool
    bmi_risk: bool
    low_physical_activity: bool
    prior_screening: bool
    prior_benign_breast_disease: bool
    self_exam_irregularity: bool
    alcohol_risk: bool
    smoker: bool
    notes: str


class EncounterAssessmentCreate(EncounterAssessmentBase):
    pass


class EncounterAssessmentUpdate(BaseModel):
    patient_id: int | None = None
    painless_lump: bool | None = None
    nipple_discharge: bool | None = None
    skin_dimpling: bool | None = None
    nipple_retraction: bool | None = None
    redness_scaling: bool | None = None
    breast_pain: bool | None = None
    swollen_lymph_nodes: bool | None = None
    family_history: bool | None = None
    never_been_pregnant: bool | None = None
    late_menopause: bool | None = None
    bmi_risk: bool | None = None
    low_physical_activity: bool | None = None
    prior_screening: bool | None = None
    prior_benign_breast_disease: bool | None = None
    self_exam_irregularity: bool | None = None
    alcohol_risk: bool | None = None
    smoker: bool | None = None
    notes: str | None = None


class EncounterAssessmentResponseWrapper(BaseModel):
    data: List[EncounterAssessmentResponse]


class EncounterAssessmentResponse2(BaseModel):
    patient: dict
    score: int
    label: str
    guidelines: List[str]


EncounterAssessmentResponse.model_rebuild()
EncounterAssessmentUpdate.model_rebuild()