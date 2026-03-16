from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin

class Gender(AuditMixin, Base, ActiveMixin):
    __tablename__ = "genders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    patients: Mapped[list["Patient"]] = relationship(
        "Patient",
        back_populates="gender"
    )