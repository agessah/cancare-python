from app.db.models import Document
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from app.db.models import DocumentCategory
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from app.schemas.document import DocumentStatistics
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db):
        self.db = db
        super().__init__(Document, db)


    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(Document).options(
            selectinload(Document.category),
            selectinload(Document.type),
        )

        # Auto soft-delete filter
        if hasattr(Document, "deleted_at"):
            stmt = stmt.where(Document.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, Document, filters)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, Document, search, ["name"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, Document, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}


    async def statistics(self):
        stmt = (
            #select(
             #   DocumentCategory.id.label("category_id"),
              #  DocumentCategory.name.label("category_name"),
               # func.count(Document.id).label("total")
            #)
            #.join(DocumentCategory, Document.category_id == DocumentCategory.id)
            #.group_by(DocumentCategory.id, DocumentCategory.name)
            #.order_by(DocumentCategory.name)

            select(
                DocumentCategory.id.label("category_id"),
                DocumentCategory.name.label("category_name"),
                func.coalesce(func.count(Document.id), 0).label("total")
            )
            .outerjoin(Document, Document.category_id == DocumentCategory.id)
            .group_by(DocumentCategory.id, DocumentCategory.name)
            .order_by(DocumentCategory.name)
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            DocumentStatistics(
                category_id=row.category_id,
                category_name=row.category_name,
                total=float(row.total or 0)
            )
            for row in rows
        ]