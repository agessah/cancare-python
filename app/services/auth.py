from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_token,
    decode_token, generate_otp
)
from app.repositories import UserRepository, RoleRepository
from app.schemas.auth import RegisterRequest, ActivateRequest, ForgotRequest, ResetRequest, LoginRequest
from app.services.email_service import EmailService
from fastapi import HTTPException
from jose import JWTError


class AuthService:
    def __init__(
            self,
            repo: UserRepository,
            role_repo: RoleRepository,
            email_service
    ):
        self.repo = repo
        self.role_repo = role_repo
        self.email_service = email_service


    async def register(self, payload: RegisterRequest, es: EmailService):
        phone_exists = await self.repo.get_by_phone(payload.phone)
        if phone_exists:
            raise HTTPException(400, "Phone number already exists!")

        email_exists = await self.repo.get_by_email(payload.email)
        if email_exists:
            raise HTTPException(400, "Email address already exists!")

        data = payload.model_dump()
        channel = data.pop("channel")
        password = data.pop("password")
        role_ids = data.pop("role_ids", [])

        if channel == "mobile":
            otp = generate_otp()

            data["password"] = hash_password(password)
            data["token"] = hash_password(otp)
            data["active"] = False

            user = await self.repo.create(data)
            await es.send_otp(user.email, otp, "Verification Code")

        else :
            data["password"] = hash_password(password)
            data["active"] = False

            user = await self.repo.create(data)

            token = create_token(user.id, "activation")
            await es.send_link(user.email, token, "activation")

        #Attach roles
        roles = await self.role_repo.get_roles(role_ids)
        if roles:
            await self.repo.sync_roles(user, roles)

        return { "message": "User created. Please check your email to activate your account." }
    

    async def activate_account(self, payload: ActivateRequest):
        if payload.channel == "mobile":
            user = await self.repo.get_by_email(payload.email)
            if not user:
                raise HTTPException(404, "User not found!")

            if not verify_password(payload.token, user.token):
                raise HTTPException(401, "Invalid or expired token!")

            user.token = None

        else:
            try:
                payload = decode_token(payload.token)

                if payload.get("type") != "activation":
                    raise HTTPException(status_code=400, detail="Invalid token type!")

                user_id = int(payload.get("sub"))

                user = await self.repo.get_by_id(user_id)
                if not user:
                    raise HTTPException(400, "Invalid activation token!")

            except JWTError:
                raise HTTPException(status_code=400, detail="Invalid or expired token!")

        if user.active:
            raise HTTPException(409,"Account already activated!")

        data = {
            "token": None,
            "active": True
        }

        await self.repo.update(user.id, data)

        return { "message": "Account activated successfully." }
    

    async def forgot_password(self, payload: ForgotRequest, es: EmailService):
        user = await self.repo.get_by_email(payload.email)
        if not user:
            raise HTTPException(404, "User not found!")

        if payload.channel == "mobile":
            otp = generate_otp()

            await self.repo.update(user.id, { "token": hash_password(otp) })

            await es.send_otp(user.email, otp, "Reset Code")

        else:
            token = create_token(user.id, "reset")

            # Send activation email
            await es.send_link(user.email, token, "reset")

        return { "message": "Password reset email sent. Please check your email to reset your password." }
    

    async def reset_password(self, payload: ResetRequest):
        if payload.channel == "mobile":

            user = await self.repo.get_by_email(payload.email)
            if not user:
                raise HTTPException(404, "User not found!")

            if not verify_password(payload.token, user.token):
                raise HTTPException(401, "Invalid or expired token!")

        else:

            try:
                payload = decode_token(payload.token)

                if payload.get("type") != "reset":
                    raise HTTPException(status_code=400, detail="Invalid token type!")

                user_id = int(payload.get("sub"))

            except JWTError:
                raise HTTPException(status_code=400, detail="Invalid or expired token!")

            user = await self.repo.get_by_id(user_id)
            if not user:
                raise HTTPException(400, "Invalid reset token!")

        data = {
            "token": None,
            "password": hash_password(payload.password)
        }

        await self.repo.update(user.id, data)

        return { "message": "Password reset successful." }


    async def login(self, payload: LoginRequest):
        user = await self.repo.get_by_username(payload.username)

        if not user:
            raise HTTPException(401, "Invalid credentials")

        if not user.active:
            raise HTTPException(403, "Account not activated")

        if not verify_password(payload.password, user.password):
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

        return { "access_token": token }