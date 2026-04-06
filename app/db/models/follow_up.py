from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin, SoftDeleteMixin
from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FollowUp(AuditMixin, SoftDeleteMixin, Base, ActiveMixin):
    __tablename__ = "follow_ups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    referral_id: Mapped[int] = mapped_column(ForeignKey("referrals.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("follow_up_statuses.id"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    referral: Mapped["Referral"] = relationship("Referral", back_populates="follow_ups", lazy="selectin")
    status: Mapped["FollowUpStatus"] = relationship(
        "FollowUpStatus", back_populates="follow_ups", lazy="selectin"
    )
