from decimal import Decimal

from sqlalchemy import Integer, Boolean, ForeignKey, Text, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin, SoftDeleteMixin


class EncounterAssessment(AuditMixin, SoftDeleteMixin, Base, ActiveMixin):
    __tablename__ = "encounter_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    painless_lump: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    persistent_pain: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    skin_dimpling: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    nipple_discharge: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    family_history: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    above_fifty: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    post_menopausal: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    obesity: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    late_first_pregnancy: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    dense_tissue: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),  # up to 999.99
        nullable=True
    )

    patient: Mapped["Patient"] = relationship("Patient", back_populates="encounter_assessments", lazy="selectin")

    __table_args__ = (
        CheckConstraint(
            "risk_score >= 0 AND risk_score <= 100",
            name="check_risk_score_between_0_100"
        ),
    )
