from __future__ import annotations

from typing import List

from app.schemas.follow_up_status import FollowUpStatusResponse
from app.schemas.referral import ReferralResponse
from pydantic import BaseModel


class FollowUpResponse(BaseModel):
    id: int
    referral: ReferralResponse
    status: FollowUpStatusResponse
    notes: str
    active: bool

    class Config:
        from_attributes = True

class FollowUpPagedResponse(BaseModel):
    total: int
    items: List[FollowUpResponse]

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

FollowUpResponse.model_rebuild()
FollowUpPagedResponse.model_rebuild()
FollowUpUpdate.model_rebuild()