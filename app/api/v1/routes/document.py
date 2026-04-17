from app.api.deps import get_document_service
from app.schemas.base import ResponseUpsertWrapper
from app.schemas.document import DocumentResponse, DocumentResponseWrapper
from app.services import DocumentService
from fastapi import APIRouter, UploadFile, Form, File, Depends, Request, Query
from fastapi_pagination import Page

router = APIRouter()

@router.get("", response_model=DocumentResponseWrapper)
async def index(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    category_id: int = Query(None),
    type_id: int = Query(None),
    #current_user = Depends(require_role(Role.ADMIN)),
    #current_user = Depends(require_permission("delete_user")),
    service: DocumentService = Depends(get_document_service)
):
    filters = {
        "category_id": category_id,
        "type_id": type_id,
    }

    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/paged", response_model=Page[DocumentResponse])
async def paged(
    request: Request,
    search: str = Query(None),
    sort: str = Query(None),
    category_id: int = Query(None),
    type_id: int = Query(None),
    service: DocumentService = Depends(get_document_service)
):
    filters = {
        "category_id": category_id,
        "type_id": type_id,
    }

    return await service.index(
        request=request,
        search=search,
        sort=sort,
        filters=filters
    )


@router.get("/{resource_id}", response_model=DocumentResponse)
async def show(
    resource_id: int,
    service: DocumentService = Depends(get_document_service)
):
    return await service.show(resource_id)


@router.post("", response_model=ResponseUpsertWrapper[DocumentResponse], status_code=201)
async def create(
    file: UploadFile = File(...),
    name: str = Form(...),
    category_id: int = Form(...),
    type_id: int = Form(...),
    service: DocumentService = Depends(get_document_service)
):
    data = await service.create(file, {
        "category_id": category_id,
        "type_id": type_id,
        "name": name
    })

    return {"detail": "Record created successfully", "data": data}