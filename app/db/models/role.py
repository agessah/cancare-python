from app.db.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin"
    )