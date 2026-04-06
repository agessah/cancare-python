from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin

class Level(AuditMixin, Base, ActiveMixin):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)