from fastapi import APIRouter, Depends

from app.api.deps import get_gender_service
from app.schemas.gender import GenderResponse
from app.services import GenderService

router = APIRouter(prefix="/genders", tags=["Gender"])

@router.get("/", response_model=list[GenderResponse])
async def index(
    service:GenderService = Depends(get_gender_service)
):
    return await service.index()