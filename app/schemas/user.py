from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import RoleOut


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    active: bool
    #role: Role

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    phone: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_ids: List[int] = Field(default_factory=lambda: [1])


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_ids: Optional[List[int]] = None


class UserOut(UserBase):
    id: int
    roles: list[RoleOut] = []

    class Config:
        from_attributes = True


class UserResponseWrapper(BaseModel):
    data: List[UserResponse]


UserResponse.model_rebuild()