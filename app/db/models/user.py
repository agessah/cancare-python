from sqlalchemy import String, Integer, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    CHP = "community_health_promoter"

# Optional: permissions per role
ROLE_PERMISSIONS = {
    Role.ADMIN: ["create_user", "delete_user", "update_user", "view_patient"],
    Role.DOCTOR: ["update_patient", "view_patient"],
    Role.CHP: ["view_self"],
}

class User(AuditMixin, Base, ActiveMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    #id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role),
        default=Role.CHP,
        nullable=False
    )