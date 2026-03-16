from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin

class County(AuditMixin, Base, ActiveMixin):
    __tablename__ = "counties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    town: Mapped[str] = mapped_column(String(50), nullable=False)

    subcounties: Mapped[list["SubCounty"]] = relationship(
        "SubCounty",
        back_populates="county",
        cascade="all, delete-orphan",
        lazy="selectin"
    )