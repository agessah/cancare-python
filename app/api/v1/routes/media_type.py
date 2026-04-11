from app.schemas.base import ResponseListWrapper
from fastapi import APIRouter, Depends

from app.api.deps import get_media_type_service
from app.schemas.media_type import MediaTypeResponse
from app.services import MediaTypeService

router = APIRouter()

@router.get("/", response_model=ResponseListWrapper[MediaTypeResponse])
async def index(
    service:MediaTypeService = Depends(get_media_type_service)
):
    return await service.index()