from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_encounter_assessment_service
from app.schemas.encounter_assessment import (
    EncounterAssessmentResponse,
    EncounterAssessmentPagedResponse,
    EncounterAssessmentCreate,
    EncounterAssessmentUpdate
)
from app.services import EncounterAssessmentService
from app.core.security import get_current_user

router = APIRouter(
    prefix="/encounter-assessments",
    tags=["EncounterAssessments"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[EncounterAssessmentResponse])
async def index(
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
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters=filters
    )

@router.get("/paged", response_model=EncounterAssessmentPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
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
        skip=skip,
        limit=limit,
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


@router.post("", response_model=EncounterAssessmentResponse, status_code=201)
async def create(
    payload: EncounterAssessmentCreate,
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
):
    return await service.create(payload)


@router.put("/{resource_id}", response_model=EncounterAssessmentResponse)
async def update(
    resource_id: int,
    payload: EncounterAssessmentUpdate,
    service: EncounterAssessmentService = Depends(get_encounter_assessment_service)
):
    return await service.update(resource_id, payload)