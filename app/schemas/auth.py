from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    channel: str
    name: str
    phone: str
    email: EmailStr
    password: str

class ActivateRequest(BaseModel):
    channel: str
    email: EmailStr
    token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ForgotRequest(BaseModel):
    channel: str
    email: EmailStr

class ResetRequest(BaseModel):
    channel: str
    email: EmailStr
    token: str
    password: str