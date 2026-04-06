from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

import aiosmtplib
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent.parent

class EmailService:

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(BASE_DIR / "templates")),
            autoescape=select_autoescape(["html", "xml"])
        )

    def render(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)

        # inject global defaults
        context.update({
            "app_name": "Cancer Care",
            "year": datetime.now().year
        })

        return template.render(**context)

    async def send_email(self, to_email: str, subject: str, html_content: str):
        message = MIMEText(html_content, "html")
        message["Subject"] = subject
        message["From"] = settings.SMTP_USER
        message["To"] = to_email

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
        )

    async def send_otp(self, to_email: str, otp: str, title: str):
        html = self.render(
            "email/otp.html",
            {
                "title": title,
                "otp": otp,
                "expiry_minutes": 10
            }
        )

        await self.send_email(
            to_email=to_email,
            subject="Your "+title,
            html_content=html
        )