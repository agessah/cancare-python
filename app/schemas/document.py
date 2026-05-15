from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic.generics import GenericModel
from app.schemas.common import DocumentCategoryMiniResponse, MediaTypeMiniResponse


class DocumentResponse(BaseModel):
    id: int
    updated_at: datetime
    category: DocumentCategoryMiniResponse
    type: MediaTypeMiniResponse
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


class DocumentStatistics(BaseModel):
    category_id: int
    category_name: str
    total: float


DocumentResponse.model_rebuild()