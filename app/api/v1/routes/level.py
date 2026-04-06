from fastapi import APIRouter, Depends

from app.api.deps import get_level_service
from app.schemas.level import LevelResponse
from app.services import LevelService

router = APIRouter(prefix="/levels", tags=["Level"])

@router.get("/", response_model=list[LevelResponse])
async def index(
    service:LevelService = Depends(get_level_service)
):
    return await service.index()