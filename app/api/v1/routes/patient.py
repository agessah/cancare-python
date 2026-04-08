from typing import List

from app.db.models.user import Role
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_patient_service
from app.schemas.patient import PatientResponse, PatientPagedResponse, PatientCreate, PatientUpdate
from app.services import PatientService
from app.core.security import get_current_user, require_role, require_permission

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[PatientResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    gender_id: int = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    #current_user = Depends(require_role(Role.ADMIN)),
    current_user = Depends(require_permission("delete_user")),
    service: PatientService = Depends(get_patient_service)
):
    filters = {
        "gender_id": gender_id,
        "county_id": county_id,
        "sub_county_id": sub_county_id,
    }

    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=PatientPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
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
        skip=skip,
        limit=limit,
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


@router.post("", response_model=PatientResponse, status_code=201)
async def create(
    payload: PatientCreate,
    service: PatientService = Depends(get_patient_service)
):
    return await service.create(payload)


@router.put("/{resource_id}", response_model=PatientResponse)
async def update(
    resource_id: int,
    payload: PatientUpdate,
    service: PatientService = Depends(get_patient_service)
):
    return await service.update(resource_id, payload)



