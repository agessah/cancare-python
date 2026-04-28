from app.api.deps import get_tele_consultation_service
from app.core.security import get_current_user
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.tele_consultation import (
    TeleConsultationResponse,
    TeleConsultationCreate,
    TeleConsultationUpdate,
    TeleConsultationResponseWrapper
)
from app.services import TeleConsultationService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=TeleConsultationResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    referral_id: int = Query(None),
    status_id: int = Query(None),
    service:
    TeleConsultationService = Depends(get_tele_consultation_service)
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

@router.get("/paged", response_model=Page[TeleConsultationResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    referral_id: int = Query(None),
    status_id: int = Query(None),
    service: TeleConsultationService = Depends(get_tele_consultation_service)
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


@router.get("/{resource_id}", response_model=TeleConsultationResponse)
async def show(
    resource_id: int,
    service: TeleConsultationService = Depends(get_tele_consultation_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ResponseUpsertWrapper[TeleConsultationResponse], status_code=201)
async def create(
    payload: TeleConsultationCreate,
    current_user: dict = Depends(get_current_user),
    service: TeleConsultationService = Depends(get_tele_consultation_service)
):
    data = await service.create(payload, current_user)
    return {"detail": "Record created successfully", "data": data}


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[TeleConsultationResponse])
async def update(
    resource_id: int,
    payload: TeleConsultationUpdate,
    current_user: dict = Depends(get_current_user),
    service: TeleConsultationService = Depends(get_tele_consultation_service)
):
    data = await service.update(resource_id, payload, current_user)
    return {"detail": "Record updated successfully", "data": data}