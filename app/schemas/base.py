from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseListWrapper(GenericModel, Generic[T]):
    data: List[T]

class ResponseUpsertWrapper(GenericModel, Generic[T]):
    detail: str
    data: T