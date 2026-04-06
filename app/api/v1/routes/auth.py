from app.api.deps import get_email_service
from app.services.email_service import EmailService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, ActivateRequest, ForgotRequest, ResetRequest, LoginRequest
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
        payload: RegisterRequest,
        db: AsyncSession = Depends(get_db),
        es: EmailService = Depends(get_email_service)
):
    return await AuthService.register(es, db, payload)


@router.post("/activate-account")
async def activate_account(payload: ActivateRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.activate_account(db, payload.token)


@router.post("/forgot-password")
async def forgot_password(payload: ForgotRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.forgot_password(db, payload.email)

@router.post("/reset-password")
async def reset_password(
    payload: ResetRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.reset_password(db,payload. token, payload.password)


@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(db, payload.username, payload.password)
