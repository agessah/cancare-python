from app.api.deps import get_patient_service
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.patient import PatientResponse, PatientCreate, PatientUpdate, PatientResponseWrapper
from app.services import PatientService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=PatientResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    gender_id: int = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    #current_user = Depends(require_role(Role.ADMIN)),
    #current_user = Depends(require_permission("delete_user")),
    service: PatientService = Depends(get_patient_service)
):
    filters = {
        "gender_id": gender_id,
        "county_id": county_id,
        "sub_county_id": sub_county_id,
    }

    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/paged", response_model=Page[PatientResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    gender_id: int = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: PatientService = Depends(get_patient_service)
):
    filters = {
        "gender_id": gender_id,
        "county_id": county_id,
        "sub_county_id": sub_county_id,
    }

    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/{resource_id}", response_model=PatientResponse)
async def show(
    resource_id: int,
    service: PatientService = Depends(get_patient_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ResponseUpsertWrapper[PatientResponse], status_code=201)
async def create(
    payload: PatientCreate,
    service: PatientService = Depends(get_patient_service)
):
    data = await service.create(payload)
    return  {"detail": "Record created successfully", "data": data}


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[PatientResponse])
async def update(
    resource_id: int,
    payload: PatientUpdate,
    service: PatientService = Depends(get_patient_service)
):
    data = await service.update(resource_id, payload)
    return {"detail": "Record updated successfully", "data": data}