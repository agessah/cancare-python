from app.api.deps import get_user_service
from app.core.security import get_current_user
from app.schemas.user import UserResponseWrapper
from app.services import UserService

from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/profile", response_model=UserResponseWrapper)
async def profile(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return await service.show(current_user.id)