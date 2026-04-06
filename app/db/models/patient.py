from datetime import date
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin, SoftDeleteMixin


class Patient(AuditMixin, SoftDeleteMixin, Base, ActiveMixin):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id"), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    county_id: Mapped[int] = mapped_column(ForeignKey("counties.id"), nullable=False)
    sub_county_id: Mapped[int] = mapped_column(ForeignKey("sub_counties.id"), nullable=False)

    gender: Mapped["Gender"] = relationship("Gender", back_populates="patients", lazy="selectin")
    county: Mapped["County"] = relationship("County", lazy="selectin")
    sub_county: Mapped["SubCounty"] = relationship("SubCounty", lazy="selectin")
    encounter_assessments: Mapped[List["EncounterAssessment"]] = relationship(
        "EncounterAssessment",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    referrals: Mapped[List["Referral"]] = relationship(
        "Referral",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy="selectin"
    )