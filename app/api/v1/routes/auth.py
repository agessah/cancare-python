from app.api.deps import get_email_service, get_auth_service
from app.schemas.auth import RegisterRequest, ActivateRequest, ForgotRequest, ResetRequest, LoginRequest
from app.services import AuthService
from app.services.email_service import EmailService
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/register")
async def register(
    payload: RegisterRequest,
    es: EmailService = Depends(get_email_service),
    service: AuthService = Depends(get_auth_service)
):
    return await service.register(payload, es)


@router.post("/activate-account")
async def activate_account(
    payload: ActivateRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.activate_account(payload)


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotRequest,
    es: EmailService = Depends(get_email_service),
    service: AuthService = Depends(get_auth_service)
):
    return await service.forgot_password(payload, es)


@router.post("/reset-password")
async def reset_password(
    payload: ResetRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.reset_password(payload)


@router.post("/login")
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login(payload)