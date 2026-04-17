from app.db.base import Base
from app.db.models.mixins import AuditMixin, ActiveMixin
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DocumentCategory(AuditMixin, Base, ActiveMixin):
    __tablename__ = "document_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="category"
    )