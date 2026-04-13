from app.api.deps import get_encounter_assessment_service
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.encounter_assessment import (
    EncounterAssessmentResponse,
    EncounterAssessmentCreate,
    EncounterAssessmentUpdate,
    EncounterAssessmentResponseWrapper
)
from app.services import EncounterAssessmentService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()


@router.get("", response_model=EncounterAssessmentResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    gender_id: int = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
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

@router.get("/paged", response_model=Page[EncounterAssessmentResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    gender_id: int = Query(None),
    county_id: int = Query(None),
    sub_county_id: int = Query(None),
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
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


@router.get("/{resource_id}", response_model=EncounterAssessmentResponse)
async def show(
    resource_id: int,
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ResponseUpsertWrapper[EncounterAssessmentResponse], status_code=201)
async def create(
    payload: EncounterAssessmentCreate,
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
):
    return await service.create(payload)


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[EncounterAssessmentResponse])
async def update(
    resource_id: int,
    payload: EncounterAssessmentUpdate,
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
):
    return await service.update(resource_id, payload)