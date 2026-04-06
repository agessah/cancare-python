from fastapi import APIRouter, Depends

from app.api.deps import get_document_category_service
from app.schemas.document_category import DocumentCategoryResponse
from app.services import DocumentCategoryService

router = APIRouter(prefix="/document-categories", tags=["DocumentCategory"])

@router.get("/", response_model=list[DocumentCategoryResponse])
async def index(
    service:DocumentCategoryService = Depends(get_document_category_service)
):
    return await service.index()