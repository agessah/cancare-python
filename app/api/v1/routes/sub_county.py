from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_sub_county_service
from app.schemas.sub_county import SubCountyResponse, SubCountyPagedResponse
from app.services import SubCountyService

router = APIRouter()

@router.get("", response_model=List[SubCountyResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    service: SubCountyService = Depends(get_sub_county_service)
):
    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort,
        filters={ "county_id": county_id }
    )


@router.get("/paged", response_model=SubCountyPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    sort: str = Query(None),
    county_id: int = Query(None),
    service: SubCountyService = Depends(get_sub_county_service)
):
    return await service.index(
        skip=skip,
        limit=limit,
        search=search,
        sort=sort,
        filters={"county_id": county_id}
    )


@router.get("/{resource_id}", response_model=SubCountyResponse)
async def show(resource_id: int, service: SubCountyService = Depends(get_sub_county_service)):
    return await service.show(resource_id)