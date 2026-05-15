from __future__ import annotations

from typing import List

from app.schemas.common import ReferralMiniResponse, FollowUpStatusMiniResponse
from pydantic import BaseModel


class FollowUpResponse(BaseModel):
    id: int
    referral: ReferralMiniResponse
    status: FollowUpStatusMiniResponse
    notes: str
    active: bool

    class Config:
        from_attributes = True


class FollowUpBase(BaseModel):
    referral_id: int
    status_id: int
    notes: str


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    referral_id: int | None = None
    status_id: int | None = None
    notes: str | None = None


class FollowUpResponseWrapper(BaseModel):
    data: List[FollowUpResponse]


FollowUpResponse.model_rebuild()
FollowUpUpdate.model_rebuild()