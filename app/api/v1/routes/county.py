from app.api.deps import get_county_service
from app.schemas.county import CountyResponse, CountyResponseWrapper
from app.services import CountyService
from fastapi import APIRouter, Depends, Query, Request
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=CountyResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    service: CountyService = Depends(get_county_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort
    )


@router.get("/paged", response_model=Page[CountyResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    service: CountyService = Depends(get_county_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort
    )


@router.get("/{resource_id}", response_model=CountyResponse)
async def show(resource_id: int, service: CountyService = Depends(get_county_service)):
    return await service.show(resource_id)