from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id = mapped_column(ForeignKey("permissions.id"), primary_key=True)