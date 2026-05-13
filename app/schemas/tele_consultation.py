from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel

from app.db.enums.ConsultationStatus import ConsultationStatus
from app.schemas.patient import PatientResponse
from app.schemas.user import UserResponse


class TeleConsultationResponse(BaseModel):
    id: int
    patient: PatientResponse
    chw: UserResponse
    oncologist: Optional[UserResponse] = None
    query: str
    response: Optional[str] = None
    status: ConsultationStatus
    active: bool

    class Config:
        from_attributes = True


class TeleConsultationBase(BaseModel):
    patient_id: int
    query: str
    response: str | None = None


class TeleConsultationCreate(TeleConsultationBase):
    pass


class TeleConsultationUpdate(BaseModel):
    patient_id: int | None = None
    query: str | None = None
    response: str | None = None


class TeleConsultationResponseWrapper(BaseModel):
    data: List[TeleConsultationResponse]


TeleConsultationResponse.model_rebuild()
TeleConsultationUpdate.model_rebuild()