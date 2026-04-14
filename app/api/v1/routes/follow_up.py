from app.api.deps import get_follow_up_service
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.follow_up import FollowUpResponse, FollowUpCreate, FollowUpUpdate, FollowUpResponseWrapper
from app.services import FollowUpService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=FollowUpResponseWrapper)
async def index(
    request: Request,
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
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=Page[FollowUpResponse])
async def paged(
    request: Request,
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
        request=request,
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


@router.post("", response_model=ResponseUpsertWrapper[FollowUpResponse], status_code=201)
async def create(
    payload: FollowUpCreate,
    service: FollowUpService = Depends(get_follow_up_service)
):
    data = await service.create(payload)
    return {"detail": "Record created successfully", "data": data}


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[FollowUpResponse])
async def update(
    resource_id: int,
    payload: FollowUpUpdate,
    service: FollowUpService = Depends(get_follow_up_service)
):
    data = await service.update(resource_id, payload)
    return {"detail": "Record updated successfully", "data": data}