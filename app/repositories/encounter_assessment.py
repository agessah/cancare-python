from app.db.models import EncounterAssessment
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort

from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class EncounterAssessmentRepository(BaseRepository[EncounterAssessment]):
    def __init__(self, db):
        self.db = db
        super().__init__(EncounterAssessment, db)

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None,
    ):
        stmt = select(EncounterAssessment).options(
            selectinload(EncounterAssessment.patient)
        )

        # Auto soft-delete filter
        if hasattr(EncounterAssessment, "deleted_at"):
            stmt = stmt.where(EncounterAssessment.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, EncounterAssessment, filters)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, EncounterAssessment, search, ["notes"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, EncounterAssessment, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}