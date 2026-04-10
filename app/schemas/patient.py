from __future__ import annotations
from datetime import date
from typing import List, Generic, TypeVar

from fastapi_pagination import Page

from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate as paginate_fn
from fastapi_pagination.bases import AbstractPage
from pydantic.generics import GenericModel

from app.schemas.sub_county import SubCountyResponse
from app.schemas.gender import GenderResponse
from pydantic import BaseModel

from app.schemas.county import CountyResponse

class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    date_of_birth: date
    gender: GenderResponse
    location: str
    county: CountyResponse
    sub_county: SubCountyResponse
    active: bool

    class Config:
        from_attributes = True


class PatientPagedResponse(BaseModel):
    total: int
    items: List[PatientResponse]

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    name: str
    date_of_birth: date
    gender_id: int
    phone: str
    location: str
    county_id: int
    sub_county_id: int

class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    gender_id: int | None = None
    phone: str | None = None
    location: str | None = None
    county_id: int | None = None
    sub_county_id: int | None = None


class PatientResponseWrapper(BaseModel):
    data: List[PatientResponse]


PatientResponse.model_rebuild()
PatientPagedResponse.model_rebuild()