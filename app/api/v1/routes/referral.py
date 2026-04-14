from app.api.deps import get_referral_service
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.referral import ReferralResponse, ReferralCreate, ReferralUpdate, ReferralResponseWrapper
from app.services import ReferralService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=ReferralResponseWrapper)
async def index(
    request: Request,
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
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=Page[ReferralResponse])
async def paged(
    request: Request,
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
        request=request,
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


@router.post("", response_model=ResponseUpsertWrapper[ReferralResponse], status_code=201)
async def create(
    payload: ReferralCreate,
    service: ReferralService = Depends(get_referral_service)
):
    data = await service.create(payload)
    return {"detail": "Record created successfully", "data": data}


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[ReferralResponse])
async def update(
    resource_id: int,
    payload: ReferralUpdate,
    service: ReferralService = Depends(get_referral_service)
):
    data = await service.update(resource_id, payload)
    return {"detail": "Record updated successfully", "data": data}