from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin

class Document(AuditMixin, Base, ActiveMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("document_categories.id"), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("media_types.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    path: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    category: Mapped["DocumentCategory"] = relationship(
        "DocumentCategory", back_populates="documents", lazy="selectin"
    )
    type: Mapped["MediaType"] = relationship(
        "MediaType", back_populates="documents", lazy="selectin"
    )