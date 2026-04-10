from typing import List

from app.schemas.base import SuccessResponse
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_follow_up_service
from app.schemas.follow_up import FollowUpResponse, FollowUpPagedResponse, FollowUpCreate, FollowUpUpdate
from app.services import PatientService, FollowUpService
from app.core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("", response_model=List[FollowUpResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    referral_id: int = Query(None),
    status_id: int = Query(None),
    service:
    FollowUpService = Depends(get_follow_up_service)
):
    filters = {
        "referral_id": referral_id,
        "status_id": status_id
    }

    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=FollowUpPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    sort: str = Query(None),
    referral_id: int = Query(None),
    status_id: int = Query(None),
    service: FollowUpService = Depends(get_follow_up_service)
):
    filters = {
        "referral_id": referral_id,
        "status_id": status_id
    }

    return await service.index(
        skip=skip,
        limit=limit,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/{resource_id}", response_model=FollowUpResponse)
async def show(
    resource_id: int,
    service: FollowUpService = Depends(get_follow_up_service)
):
    return await service.show(resource_id)


@router.post("", response_model=SuccessResponse, status_code=201)
async def create(
    payload: FollowUpCreate,
    service: FollowUpService = Depends(get_follow_up_service)
):
    return await service.create(payload)


@router.put("/{resource_id}", response_model=SuccessResponse)
async def update(
    resource_id: int,
    payload: FollowUpUpdate,
    service: FollowUpService = Depends(get_follow_up_service)
):
    return await service.update(resource_id, payload)



