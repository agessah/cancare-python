from typing import List, Optional

from app.db.models.user import Role
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    active: bool
    role: Role

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    phone: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Role = Role.CHP


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role]


class UserOut(UserBase):
    id: int
    role: Role

    class Config:
        orm_mode = True


class UserResponseWrapper(BaseModel):
    data: UserResponse


UserResponse.model_rebuild()