from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_medical_facility_service
from app.schemas.medical_facility import MedicalFacilityResponse, MedicalFacilityPagedResponse
from app.services import MedicalFacilityService

router = APIRouter(prefix="/medical-facilities", tags=["MedicalFacilities"])

@router.get("", response_model=List[MedicalFacilityResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: MedicalFacilityService = Depends(get_medical_facility_service)
):
    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters={
            "county_id": county_id,
            "sub_county_id": sub_county_id,
        }
    )


@router.get("/paged", response_model=MedicalFacilityPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: MedicalFacilityService = Depends(get_medical_facility_service)
):
    return await service.index(
        skip=skip,
        limit=limit,
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