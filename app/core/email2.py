from email.message import EmailMessage
import aiosmtplib

from app.core.config import settings


async def send_token_email(to_email: str, token: str, action: str):
    link, subject = (
        (f"{settings.FRONTEND_URL}/activate?token={token}", "Activate Your Account")
        if action == "activation"
        else (f"{settings.FRONTEND_URL}/reset?token={token}", "Reset Your Password")
    )

    content = (
        f"""
        Welcome!

        Please activate your account by clicking the link below:

        {link}

        If you did not register, ignore this email.
        """
        if action == "activation" else
        f"""
        You requested to reset your password.

        Click the link below to reset it:

        {link}

        If you did not request this, please ignore this email.
        """
    )

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASS,
    )