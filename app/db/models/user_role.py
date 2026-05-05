from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id = mapped_column(ForeignKey("roles.id"), primary_key=True)