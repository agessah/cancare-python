from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

from app.api.deps import get_medical_facility_service
from app.schemas.medical_facility import MedicalFacilityResponse, MedicalFacilityResponseWrapper
from app.services import MedicalFacilityService

router = APIRouter()

@router.get("", response_model=MedicalFacilityResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: MedicalFacilityService = Depends(get_medical_facility_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters={
            "county_id": county_id,
            "sub_county_id": sub_county_id,
        }
    )


@router.get("/paged", response_model=Page[MedicalFacilityResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: MedicalFacilityService = Depends(get_medical_facility_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters={
            "county_id": county_id,
            "sub_county_id": sub_county_id
        }
    )


@router.get("/{resource_id}", response_model=MedicalFacilityResponse)
async def show(
        resource_id: int,
        service: MedicalFacilityService = Depends(get_medical_facility_service)
):
    return await service.show(resource_id)