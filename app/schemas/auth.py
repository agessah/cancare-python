from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str

class ActivateRequest(BaseModel):
    token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ForgotRequest(BaseModel):
    email: str

class ResetRequest(BaseModel):
    token: str
    password: str