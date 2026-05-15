from app.api.deps import get_user_service
from app.core.security import get_current_user
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.user import UserResponseWrapper, UserUpdate, UserCreate, UserResponse
from app.services import UserService

from fastapi import APIRouter, Depends, Request, Query
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=UserResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    #current_user = Depends(require_role(Role.ADMIN)),
    #current_user = Depends(require_permission("delete_user")),
    service: UserService = Depends(get_user_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort
    )


@router.get("/paged", response_model=Page[UserResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    service: UserService = Depends(get_user_service)
):
    return await service.index(
        request=request,
        search=search,
        sort=sort
    )


@router.get("/{resource_id}", response_model=UserResponse)
async def show(
    resource_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ResponseUpsertWrapper[UserResponse], status_code=201)
async def create(
    payload: UserCreate,
    service: UserService = Depends(get_user_service)
):
    data = await service.create(payload)
    return  {"detail": "Record created successfully", "data": data}


@router.put("/{resource_id}", response_model=ResponseUpsertWrapper[UserResponse])
async def update(
    resource_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    data = await service.update(resource_id, payload)
    return {"detail": "Record updated successfully", "data": data}

@router.get("/profile", response_model=UserResponseWrapper)
async def profile(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return await service.show(current_user.id)
