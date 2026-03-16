from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.email2 import send_token_email
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_token,
    decode_token
)
from app.db.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, payload: RegisterRequest):
        phone_exists = await UserRepository.get_by_phone(db, payload.phone)
        if phone_exists:
            raise HTTPException(400, "Phone number already exists!")

        email_exists = await UserRepository.get_by_email(db, payload.email)
        if email_exists:
            raise HTTPException(400, "Email address already exists!")

        user = User(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            password=hash_password(payload.password),
            activation_token=None,
            active=False
        )

        await UserRepository.create(db, user)
        await db.refresh(user)

        token = create_token(user.id, "activation")

        # Send activation email
        await send_token_email(user.email, token, "activation")

        return { "message": "User created. Please check your email to activate your account." }
    

    @staticmethod
    async def activate_account(db: AsyncSession, token: str):
        try:
            payload = decode_token(token)

            if payload.get("type") != "activation":
                raise HTTPException(status_code=400, detail="Invalid token type!")

            user_id = int(payload.get("sub"))

        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid or expired token!")

        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(400, "Invalid activation token!")

        if user.active:
            return { "message": "Account already activated!" }

        user.active = True
        await UserRepository.commit(db)

        return { "message": "Account activated successfully." }
    

    @staticmethod
    async def forgot_password(db: AsyncSession, email: str):
        user = await UserRepository.get_by_email(db, email)
        if not user:
            raise HTTPException(404, "User not found!")

        await UserRepository.commit(db)
        await db.refresh(user)

        token = create_token(user.id, "reset")

        # Send activation email
        await send_token_email(user.email, token, "reset")

        return { "message": "Password reset email sent. Please check your email to reset your password." }
    

    @staticmethod
    async def reset_password(db: AsyncSession, token: str, password: str):
        try:
            payload = decode_token(token)

            if payload.get("type") != "reset":
                raise HTTPException(status_code=400, detail="Invalid token type!")
            
            user_id = int(payload.get("sub"))

        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid or expired token!")

        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(400, "Invalid reset token!")

        user.password = hash_password(password)
        await UserRepository.commit(db)

        return { "message": "Password reset successful." }


    @staticmethod
    async def login(db: AsyncSession, phone: str, password: str):
        user = await UserRepository.get_by_phone(db, phone)

        if not user:
            raise HTTPException(401, "Invalid credentials")

        if not user.active:
            raise HTTPException(403, "Account not activated")

        if not verify_password(password, user.password):
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

        return { "access_token": token }