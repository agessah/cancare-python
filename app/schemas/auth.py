from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str

class ActivateRequest(BaseModel):
    channel: str
    token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ForgotRequest(BaseModel):
    channel: str
    email: str

class ResetRequest(BaseModel):
    channel: str
    token: str
    password: str