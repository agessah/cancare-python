from app.api.deps import get_county_service
from app.schemas.county import CountyResponse, CountyPagedResponse
from app.services import CountyService
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/counties", tags=["Counties"])

@router.get("", response_model=list[CountyResponse])
async def index(
    search: str = Query(None),
    sort: str = Query(None),
    service: CountyService = Depends(get_county_service)
):
    return await service.index(
        skip=None,
        limit=None,
        search=search,
        sort=sort
    )


@router.get("/paged", response_model=CountyPagedResponse)
async def paged(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    sort: str = Query(None),
    service: CountyService = Depends(get_county_service)
):
    return await service.index(
        skip=skip,
        limit=limit,
        search=search,
        sort=sort
    )


@router.get("/{resource_id}", response_model=CountyResponse)
async def show(resource_id: int, service: CountyService = Depends(get_county_service)):
    return await service.show(resource_id)