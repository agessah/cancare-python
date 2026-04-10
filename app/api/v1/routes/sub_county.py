from app.api.deps import get_sub_county_service
from app.schemas.sub_county import SubCountyResponse, SubCountyResponseWrapper
from app.services import SubCountyService
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=SubCountyResponseWrapper)
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


@router.get("/paged", response_model=Page[SubCountyResponse])
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