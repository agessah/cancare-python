from app.api.deps import get_email_service
from app.services.email_service import EmailService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, ActivateRequest, ForgotRequest, ResetRequest, LoginRequest
from app.services import AuthService

router = APIRouter()

@router.post("/register")
async def register(
        request: RegisterRequest,
        db: AsyncSession = Depends(get_db),
        es: EmailService = Depends(get_email_service)
):
    return await AuthService.register(es, db, request)


@router.post("/activate-account")
async def activate_account(request: ActivateRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.activate_account(db, request)


@router.post("/forgot-password")
async def forgot_password(
        request: ForgotRequest,
        db: AsyncSession = Depends(get_db),
        es: EmailService = Depends(get_email_service)
):
    return await AuthService.forgot_password(es, db, request)

@router.post("/reset-password")
async def reset_password(
    request: ResetRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.reset_password(db, request)


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(db, request.username, request.password)
