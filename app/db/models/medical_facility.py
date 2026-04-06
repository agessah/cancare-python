from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin, SoftDeleteMixin
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedicalFacility(AuditMixin, SoftDeleteMixin, Base, ActiveMixin):
    __tablename__ = "medical_facilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    county_id: Mapped[int] = mapped_column(ForeignKey("counties.id"), nullable=False)
    sub_county_id: Mapped[int] = mapped_column(ForeignKey("sub_counties.id"), nullable=False)
    county: Mapped["County"] = relationship("County", lazy="selectin")
    sub_county: Mapped["SubCounty"] = relationship("SubCounty", lazy="selectin")

    referrals: Mapped[List["Referral"]] = relationship(
        "Referral",
        back_populates="medical_facility",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
