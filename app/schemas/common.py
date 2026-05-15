from datetime import date
from decimal import Decimal
from typing import Optional, List

from app.db.enums.ConsultationStatus import ConsultationStatus
from pydantic import BaseModel


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PermissionOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LevelMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FollowUpStatusMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GenderMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CountyMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SubCountyMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DocumentCategoryMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MediaTypeMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserMiniResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    active: bool
    roles: List[RoleOut] = []

    class Config:
        from_attributes = True


class MedicalFacilityMiniResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PatientMiniResponse(BaseModel):
    id: int
    name: str
    phone: str
    date_of_birth: date
    gender: GenderMiniResponse
    location: str
    county: CountyMiniResponse
    sub_county: SubCountyMiniResponse
    active: bool

    class Config:
        from_attributes = True


class EncounterAssessmentMiniResponse(BaseModel):
    id: int
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





class TeleConsultationMiniResponse(BaseModel):
    id: int
    #patient: PatientResponse
    chw: UserMiniResponse
    oncologist: Optional[UserMiniResponse] = None
    query: str
    response: Optional[str] = None
    status: ConsultationStatus
    active: bool

    class Config:
        from_attributes = True

class FollowUpMiniResponse(BaseModel):
    id: int
    #referral: ReferralMiniResponse
    status: FollowUpStatusMiniResponse
    notes: str
    active: bool

    class Config:
        from_attributes = True


class ReferralMiniResponse(BaseModel):
    id: int
    medical_facility: MedicalFacilityMiniResponse
    notes: str
    urgency_level: LevelMiniResponse
    follow_ups: List[FollowUpMiniResponse]
    active: bool

    class Config:
        from_attributes = True