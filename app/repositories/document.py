from app.db.models import Document
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
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
            stmt = stmt.where(Document.deleted_at is None)

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