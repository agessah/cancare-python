from app.db.models import TeleConsultation
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class TeleConsultationRepository(BaseRepository[TeleConsultation]):
    def __init__(self, db):
        self.db = db
        super().__init__(TeleConsultation, db)


    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(TeleConsultation).options(
            selectinload(TeleConsultation.chw),
            selectinload(TeleConsultation.oncologist),
        )

        # Auto soft-delete filter
        if hasattr(TeleConsultation, "deleted_at"):
            stmt = stmt.where(TeleConsultation.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, TeleConsultation, filters)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, TeleConsultation, search, ["query", "response"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, TeleConsultation, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}