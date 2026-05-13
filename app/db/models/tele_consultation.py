from sqlalchemy import String, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.enums.ConsultationStatus import ConsultationStatus
from app.db.models.mixins import AuditMixin, ActiveMixin

class TeleConsultation(AuditMixin, Base, ActiveMixin):
    __tablename__ = "tele_consultations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    chw_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    oncologist_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    query: Mapped[str] = mapped_column(String(255), nullable=False)
    response: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ConsultationStatus] = mapped_column(
        SqlEnum(ConsultationStatus, name="consultation_status_enum"),
        nullable=False
    )

    patient: Mapped["Patient"] = relationship("Patient", lazy="selectin")
    chw: Mapped["User"] = relationship(
        "User",
        foreign_keys=[chw_id],
        lazy="selectin"
    )
    oncologist: Mapped["User"] = relationship(
        "User",
        foreign_keys=[oncologist_id],
        lazy="selectin"
    )