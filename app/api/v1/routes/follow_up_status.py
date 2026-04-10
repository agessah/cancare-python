from fastapi import APIRouter, Depends

from app.api.deps import get_follow_up_status_service
from app.schemas.follow_up_status import FollowUpStatusResponse
from app.services import FollowUpStatusService

router = APIRouter()

@router.get("/", response_model=list[FollowUpStatusResponse])
async def index(
    service:FollowUpStatusService = Depends(get_follow_up_status_service)
):
    return await service.index()