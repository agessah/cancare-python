from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        # onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    @declared_attr
    def created_by_user(cls):
        return relationship(
            "User",
            foreign_keys=lambda: [cls.created_by],
            lazy="selectin"
        )

    @declared_attr
    def updated_by_user(cls):
        return relationship(
            "User",
            foreign_keys=lambda: [cls.updated_by],
            lazy="selectin"
        )

class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=None,
        nullable=True
    )

class ActiveMixin:
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        #server_default=text("false"),
        server_default="false",
        nullable=False
    )