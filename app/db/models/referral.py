from sqlalchemy import Integer, Boolean, ForeignKey, Text, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin, SoftDeleteMixin


class Referral(AuditMixin, SoftDeleteMixin, Base, ActiveMixin):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    medical_facility_id: Mapped[int] = mapped_column(ForeignKey("medical_facilities.id"), nullable=False)
    urgency_level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="referrals", lazy="selectin")
    medical_facility: Mapped["MedicalFacility"] = relationship("MedicalFacility", back_populates="referrals", lazy="selectin")
    urgency_level: Mapped["Level"] = relationship("Level", lazy="selectin")

    follow_ups: Mapped[List["FollowUp"]] = relationship(
        "FollowUp",
        back_populates="referral",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


