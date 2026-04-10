from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_referral_service
from app.schemas.referral import ReferralResponse, ReferralPagedResponse, ReferralCreate, ReferralUpdate
from app.services import ReferralService
from app.core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("", response_model=List[ReferralResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    patient_id: int = Query(None),
    medical_facility_id: int = Query(None),
    level_id: int = Query(None),
    service: ReferralService = Depends(get_referral_service)
):
    filters = {
        "patient_id": patient_id,
        "medical_facility_id": medical_facility_id,
        "level_id": level_id,
    }

    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=ReferralPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    sort: str = Query(None),
    patient_id: int = Query(None),
    medical_facility_id: int = Query(None),
    level_id: int = Query(None),
    service: ReferralService = Depends(get_referral_service)
):
    filters = {
        "patient_id": patient_id,
        "medical_facility_id": medical_facility_id,
        "level_id": level_id,
    }

    return await service.index(
        skip=skip,
        limit=limit,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/{resource_id}", response_model=ReferralResponse)
async def show(
    resource_id: int,
    service: ReferralService = Depends(get_referral_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ReferralResponse, status_code=201)
async def create(
    payload: ReferralCreate,
    service: ReferralService = Depends(get_referral_service)
):
    return await service.create(payload)


@router.put("/{resource_id}", response_model=ReferralResponse)
async def update(
    resource_id: int,
    payload: ReferralUpdate,
    service: ReferralService = Depends(get_referral_service)
):
    return await service.update(resource_id, payload)



