from app.schemas.base import ResponseListWrapper
from fastapi import APIRouter, Depends

from app.api.deps import get_gender_service
from app.schemas.gender import GenderResponse
from app.services import GenderService

router = APIRouter()

@router.get("/", response_model=ResponseListWrapper[GenderResponse])
async def index(
    service:GenderService = Depends(get_gender_service)
):
    return await service.index()