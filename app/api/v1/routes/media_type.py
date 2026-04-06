from fastapi import APIRouter, Depends

from app.api.deps import get_media_type_service
from app.schemas.media_type import MediaTypeResponse
from app.services import MediaTypeService

router = APIRouter(prefix="/media-types", tags=["MediaType"])

@router.get("/", response_model=list[MediaTypeResponse])
async def index(
    service:MediaTypeService = Depends(get_media_type_service)
):
    return await service.index()