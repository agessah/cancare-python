from app.api.deps import get_user_service
from app.core.security import get_current_user, require_role
from app.db.models.user import Role
from app.schemas.user import UserResponse
from app.services import UserService

from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/profile", response_model=UserResponse)
async def profile(
    current_user=Depends(get_current_user)
):
    return current_user