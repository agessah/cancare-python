from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin

class SubCounty(AuditMixin, Base, ActiveMixin):
    __tablename__ = "sub_counties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    county_id: Mapped[int] = mapped_column(ForeignKey("counties.id"), nullable=False)
    county: Mapped["County"] = relationship("County", back_populates="subcounties", lazy="selectin")