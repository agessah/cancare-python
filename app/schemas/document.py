from __future__ import annotations

from typing import List

from app.schemas.document_category import DocumentCategoryResponse
from app.schemas.media_type import MediaTypeResponse
from pydantic import BaseModel
from pydantic.generics import GenericModel


class DocumentResponse(BaseModel):
    id: int
    category: DocumentCategoryResponse
    type: MediaTypeResponse
    name: str
    path: str
    active: bool

    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    category_id: int
    type_id: int
    name: str
    path: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    category_id: int | None = None
    type_id: int | None = None
    name: str | None = None
    path: str | None = None


class DocumentResponseWrapper(BaseModel):
    data: List[DocumentResponse]


DocumentResponse.model_rebuild()